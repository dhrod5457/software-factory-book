# 20장. Event-driven Factory와 Closed-loop SDLC

지금까지의 생산 시스템은 대부분 사람이 작업을 시작하는 구조였다. 하지만 실제 소프트웨어 전달에서는 새로운 작업이 사람의 지시문으로만 생기지 않는다.

- CI 실패
- 보안 알림
- 의존 패키지 갱신
- 검토 의견
- 정기 유지보수
- 운영 환경 장애
- 문서와 실제 상태의 불일치

이런 신호를 작업 소스로 사용할 수 있다. 문제는 이런 신호를 확인하자마자 에이전트가 곧바로 행동하도록 만들면 위험하다는 것이다.

~~~text
Alert
→ Agent
→ Production Change
~~~

이 구조에서는 잘못된 알림, 중복 신호, 일시적 장애가 실제 변경으로 이어질 수 있다. 그래서 이벤트 기반 생산 시스템에서는 중간에 해석 단계가 필요하다.

> 알림은 작업이 아니다.

---

## 20.1 Task Source를 확장한다

생산 시스템이 받을 수 있는 작업 소스는 다양하다.

~~~text
Human Request
Issue
CI Failure
Review
Vulnerability
Schedule
Production Signal
~~~

이 신호는 모두 같은 의미가 아니다. 예를 들어 CI 실패는 재현 가능한 공학 문제에 가까울 수 있다. 반면 CPU 사용량 급증 하나는 아직 작업이 아니다. 원인이 코드인지, 요청량인지, 인프라인지도 모른다. 그래서 작업 접수는 신호를 먼저 분류해야 한다.

---

## 20.2 Signal에서 Task로

좋은 흐름은 다음에 가깝다.

~~~text
Signal
→ Diagnose
→ Scope
→ Risk
→ Acceptance
→ Task
→ Execute
~~~

예를 들어 운영 환경 응답 지연 알림이 발생했다. 바로 코드 변경을 시작하지 않는다. 먼저 진단 작업을 만든다.

~~~text
Goal
- latency 증가 원인 확인

Input
- traces
- metrics
- deployment revision

Acceptance
- top bottleneck identified
- evidence attached
~~~

진단 결과가 코드 이슈로 확인되면 그다음 수정 작업을 만든다. 이렇게 하면 알림과 행동 사이에 의미 있는 경계가 생긴다.

---

## 20.3 Event-driven은 Fully Autonomous와 다르다

이벤트가 자동으로 작업을 생성해도 병합까지 자동일 필요는 없다. Google이 2025년 12월 Jules에 공개한 Suggested Tasks와 Scheduled Tasks도 이 구분을 보여준다. Suggested Tasks는 개선 후보를 제안해 사용자가 review/approve/dismiss하도록 했고, Render 연동의 deployment-failure 대응도 수정을 만든 뒤 변경 검토 요청을 열어 검토를 남겼다.

예:

~~~text
CI Failure
→ auto task create
→ Agent fix
→ verification
→ human review
~~~

또는 위험이 낮은 작업에서는:

~~~text
docs drift
→ auto task
→ agent fix
→ deterministic verification
→ auto merge by policy
~~~

즉 이벤트 기반 실행은 **작업 시작 방식**에 관한 개념이다. 자율성은 별도 축이다.

---

## 20.4 Closed-loop SDLC

소프트웨어 전달은 배포에서 끝나지 않는다.

~~~text
Plan
→ Build
→ Test
→ Release
→ Deploy
→ Operate
→ Observe
→ Learn
↺
~~~

운영 환경에서 나온 신호는 다시 요구사항, 테스트, 작업으로 돌아갈 수 있다.

예:

~~~text
Production Bug
→ Regression Test
→ Fix Task
→ Verification
→ Deploy
~~~

또는:

~~~text
Repeated Agent Failure
→ Missing Skill 발견
→ Factory Improvement Task
~~~

이 책에서는 이런 운영·관찰 결과가 다시 요구사항·테스트·작업으로 돌아가는 구조를 운영 결과를 개발로 되돌리는 순환 구조라고 부른다. 기존 DevSecOps의 지속적인 피드백을 에이전트 작업 접수까지 확장한 개념이다. Warp의 생산 시스템 순환도 같은 방향의 사례다. Lloyd는 에이전트가 코드 전달에서 멈추지 않고, 배포 결과가 오작동하는지 또는 실제로 사용되는지를 관찰하고 그 출력을 다시 생산 시스템의 위쪽 입력으로 보내야 한다고 설명한다.

여기서 중요한 것은 특정 공급업체 작업 흐름이 아니라 **전달 이후의 관찰이 다음 작업의 원인이 되는 경계**다.

---

### Continuous Planning Loop: 실행 중 배운 것으로 Plan을 다시 본다

닫힌 순환은 운영 환경에서만 시작하지 않는다. WorkOS는 Linear 작업 티켓의 의존 관계를 따라 다음 작업을 자동으로 시작하는 것뿐 아니라, 하나의 작업 티켓이 끝날 때 현재 프로젝트를 다시 평가해 빠진 작업이 생겼는지 에이전트에게 확인시키는 흐름을 설명한다. 구현은 새로운 정보를 만든다.

~~~text
Plan
→ Task
→ Execution
→ New Knowledge
→ Plan Re-evaluation
→ Task Graph Update
~~~

처음 만든 계획을 바꿀 수 없는 약속으로 취급하면 구현 중 발견한 빠진 내용을 반영하지 못한다. 반대로 에이전트가 매 단계 마음대로 앞으로의 계획을 바꾸게 하면 작업 범위가 흔들린다. 따라서 계획 재평가도 권한을 나눈다.

~~~text
Agent
→ missing task / dependency / risk 제안

System
→ task graph consistency / policy 확인

Human or Policy
→ scope-changing proposal 승인
~~~

이 순환을 뒤의 두 순환과 구분하면 생산 시스템 피드백 구조가 더 선명해진다.

~~~text
Execution Learning Loop
Task → New Knowledge → Plan

Product Feedback Loop
Operate → Signal → Requirement

Factory Improvement Loop
Execution Friction → Factory Capability
~~~

## 20.5 Product Loop와 Factory Loop를 구분한다

두 가지 피드백 순환이 있다.

### Product Loop

~~~text
Production Problem
→ Product Code Fix
~~~

예:

- 응답 지연 버그
- 검증 버그
- UI 결함

### Factory Loop

~~~text
Factory Friction
→ Factory Capability Improvement
~~~

예:

- 느린 워커 초기 준비
- 빠진 도구
- 간헐적으로 실패하는 검증
- 오래된 맥락 정보
- 부실한 검증 근거 묶음

둘을 섞지 않는다. 제품 문제가 생산 시스템 설정 변경으로 잘못 이어지거나, 생산 시스템 문제를 제품 코드 수정으로 해결하려 하면 혼란이 생긴다.

---

## 20.6 Noise를 Work로 증폭시키지 않는다

운영 환경에서는 불필요한 신호가 많이 섞일 수 있다. 모든 알림을 작업으로 만들면 할 일 목록이 폭발한다.

예:

~~~text
same alert × 100
→ 100 tasks
~~~

필요한 제어:

- 중복 제거
- 재실행 대기 시간
- 묶어서 처리
- 확신도 기준
- 불필요한 알림 억제
- 변경 한도

예:

~~~text
same fingerprint
within 10m
→ one diagnosis task
~~~

---

## 20.7 Oscillation

자동 문제 수정이나 자동 복구 성격의 순환이 잘못 설계되면 반복 변경이 발생할 수 있다.

~~~text
Agent
→ config increase

Metric improves briefly

Another signal
→ config decrease

Repeat
~~~

이런 상태가 반복해서 오가는 진동 현상을 막기 위해 다음이 필요하다.

- 관찰 관찰 기간
- 이전 상태로 복구 규칙
- 변경 한도
- 사람에게 판단 요청
- state/history

자동화가 많아질수록 “언제 아무것도 하지 않을 것인가”도 중요하다.

---

## 20.8 예: Nightly Test Failure

~~~text
02:00 Nightly Test FAIL
      ↓
Event received
      ↓
Deduplicate
      ↓
Task created
      ↓
Agent diagnoses
      ↓
Fix
      ↓
Targeted verification
      ↓
Regression test added
      ↓
Human / Policy Gate
~~~

좋은 점은 실패가 단순히 고쳐지고 끝나지 않는다는 것이다. 같은 문제가 다시 생기지 않도록 기존 기능이 깨지지 않았는지 확인하는 회귀 테스트가 생산 시스템 자산으로 남는다.

---

## 20.9 Production Signal을 바로 Code Fix로 보내지 않는다

응답 지연 알림 예:

나쁜 흐름:

~~~text
latency high
→ Agent edits code
→ deploy
~~~

더 안전한 흐름:

~~~text
latency high
→ trace analysis
→ bottleneck identified
→ scope
→ risk
→ fix task
→ verification
→ deploy gate
~~~

이 구조는 속도를 조금 늦출 수 있다. 대신 잘못된 자동 수정의 피해 범위를 줄인다.

---

## 20.10 Routine은 Trigger이고 Task는 Work다

클라우드 에이전트 제품은 일정이나 외부 이벤트로 반복 작업을 시작하는 기능을 제공하기 시작했다. Cursor의 Grok Bot Routines는 시간 일정뿐 아니라 Slack, GitHub, Linear, Sentry, PagerDuty, 이메일, Webhook 같은 이벤트를 시작 조건으로 사용할 수 있다고 문서화한다. 이 기능은 이벤트 기반 생산 시스템과 닮아 있다. 하지만 다음을 그대로 같다고 보면 안 된다.

~~~text
Routine Trigger
≠ Durable Task
~~~

정기 실행 기능은 "언제 시작할 것인가"를 표현하는 데 강하다. 생산 시스템의 지속 작업은 시작 이후의 책임을 가진다.

~~~text
Trigger
→ Intake
→ Deduplicate
→ Risk / Scope
→ Durable Task
→ Attempt
→ Verification
→ Evidence
→ Acceptance
~~~

예를 들어 GitHub 이벤트가 들어왔다는 이유만으로 같은 수정 작업을 매번 새로 만들면 중복 작업이 발생한다. 일정이 실행됐다는 사실만으로 이전 실행의 외부에 남는 변경이 안전하게 처리됐다는 보장도 없다. 따라서 이벤트·정기 실행 기능을 생산 시스템에 연결할 때는 다음 질문이 추가된다.

- 같은 신호를 어떻게 중복 제거하는가
- 이전 실행이 아직 진행 중이면 어떻게 하는가
- 실패한 실행을 재시도할지 다음 일정까지 기다릴지
- 외부 시스템에 남는 변경이 반복 실행해도 안전한가
- 어떤 이벤트는 진단만 만들고 어떤 이벤트는 수정 작업까지 만드는가

이벤트 시작 조건이 편리해질수록 작업 접수와 지속 실행의 책임을 시작 조건 계층 밖에 남겨두는 것이 중요하다.

## 다음 질문

이벤트 기반 생산 시스템이 작업을 만들기 시작하면 더 많은 플랫폼 기능이 필요해진다. 데이터베이스 준비, 배포, 비밀 정보, 관측 가능성을 에이전트가 직접 구현하게 해야 할까. 다음 장에서는 기존 **개발자 플랫폼과 표준 개발 경로를 생산 시스템이 어떻게 활용하는가**를 다룬다.

---

## 참고 자료

- Cursor, *Routines*  
  https://prod.cursor.com/help/grok-bot/routines
- NIST NCCoE, *DevSecOps Notional Reference Model*  
  https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Google, *Jules proactive updates*  
  https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/
- Warp / Zach Lloyd, *Software Engineering Is Becoming Factory Engineering*  
  https://www.youtube.com/watch?v=tUPPVhBBcoM
