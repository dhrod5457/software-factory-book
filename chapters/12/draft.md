# 12장. Verification: Agent가 완료했다고 말한 뒤부터가 시작이다

에이전트가 다음과 같이 보고했다고 하자.

> 수정 완료했습니다. 테스트도 모두 통과했습니다.

대화형 사용에서는 여기서 사람이 코드를 열어보고 판단할 수 있다. 생산 시스템에서는 이 문장을 작업의 최종 상태로 사용하면 안 된다. 에이전트의 보고는 **작업을 마쳤다는 주장(Completion Claim)**이다. 작업 상태를 DONE으로 바꿀 수 있는 **완료 판정 권한(Completion Authority)**과는 구분해야 한다. 이 책에서는 다음 구조를 기본으로 본다.

~~~text
Agent
→ Candidate Result
→ Verification
→ Evidence
→ Acceptance
~~~

에이전트가 결과를 제안하면 검증 담당자나 시스템인 검증기(Verifier)가 확인한다. 그다음 시스템이나 사람이 남은 위험을 받아들일지 결정한다.

> 에이전트가 "DONE"이라고 말하는 것과 생산 시스템이 DONE이라고 판정하는 것은 다른 사건이다.

---

## 12.1 Completion Claim과 Completion Authority

작업을 수행한 에이전트는 자신의 작업에 가장 많은 맥락 정보를 가지고 있다. 그래서 다음도 잘 설명할 수 있다.

- 어떤 파일을 바꿨는가
- 어떤 명령을 실행했는가
- 왜 이런 구현을 선택했는가
- 어떤 문제가 남았는가

하지만 자신의 작업을 설명할 수 있다는 것과 독립적으로 검증할 수 있다는 것은 다르다. 예를 들어 에이전트가 다음과 같이 말할 수 있다.

~~~text
- expired JWT를 401로 수정
- unit test PASS
- integration test PASS
~~~

생산 시스템은 최소한 다음을 독립적으로 확인할 수 있어야 한다.

~~~text
Result Revision
→ 실제 commit은 무엇인가

Verification
→ 어떤 command가 실행됐는가

Exit
→ 실제 result는 PASS인가

Acceptance
→ 401 behavior가 확인됐는가
~~~

즉 에이전트의 자연어 요약을 판단의 기준이 되는 상태로 사용하지 않는다.

---

## 12.2 Verification Pyramid

모든 작업에 같은 검증 비용을 쓸 필요는 없다. 검증은 여러 층으로 구성할 수 있다.

~~~text
Static
        ↓
Deterministic Test
        ↓
Runtime Verification
        ↓
Behavioral Evidence
        ↓
Independent Evaluator
        ↓
Human Acceptance
~~~

위로 갈수록 일반적으로 비용이 커지고, 더 넓은 종류의 오류를 잡을 수 있다.

### Static

- 컴파일
- 자료형 검사
- lint
- 형식 검사
- 스키마 검증

빠르고 정해진 규칙에 따라 결과가 나온다.

### Deterministic Test

- 단위
- 통합
- 규약
- 마이그레이션 테스트

작업의 구체적인 동작을 검증한다.

### Runtime Verification

실제 서비스를 실행한다.

- 서비스 시작
- API 요청
- DB 마이그레이션
- 백그라운드 작업

### Behavioral Evidence

사람이나 평가자가 실제 결과를 볼 수 있게 한다.

- 화면 캡처
- 영상
- DOM
- 로그
- 추적 기록
- 성능 평가

UI 작업에서는 실제 동작의 근거가 특히 중요하다. Warp의 Zach Lloyd는 소프트웨어 생산 시스템의 검증 예로 에이전트가 만든 UI를 화면을 직접 조작하는 기능으로 실제 실행하고 영상과 화면 캡처를 남기는 흐름을 설명했다. 중요한 점은 화면 캡처 자체가 아니라 **실제 동작을 실행한 흔적을 후보 코드 버전과 연결한다는 것**이다.

~~~text
UI Candidate
→ Application Launch
→ Computer Use
→ Critical Flow
→ Screenshot / Video
→ Behavioral Evidence
~~~

이 패턴은 이 책의 증거 계약과 같은 문제를 다른 각도에서 보여준다. “화면을 수정했다”는 에이전트의 설명보다, 특정 코드 버전에서 실제 사용 흐름을 실행하고 남긴 근거가 검토 비용을 줄인다.

### Independent Evaluator

구현 에이전트와 다른 맥락 정보나 역할을 가진 평가자가 결과를 점검한다.

### Human Acceptance

남은 위험과 제품에 담긴 의도를 최종적으로 사람이 판단한다. 검증을 비용 순서의 피라미드로만 볼 필요는 없다. **무엇에 대한 적합성을 검증하는가**라는 축도 필요하다.

~~~text
Functional Conformance
- 요구한 동작을 실제로 하는가

Architecture Conformance
- 정해진 Architecture / Design Constraint를 지켰는가

Scope Conformance
- 허용된 파일과 변경 범위를 벗어나지 않았는가

Security Conformance
- 필요한 Security Policy와 Review를 통과했는가
~~~

예를 들어 테스트가 모두 PASS해도 에이전트가 허용되지 않은 공통 모듈까지 수정했거나, 요구사항이 요구한 설계 구조 경계를 우회했다면 운영에 사용할 수 있는 변경이라고 보기 어렵다. Caylent는 소프트웨어 생산 시스템 하네스가 보안 검토, 설계 구조의 요구 조건 준수, 범위 이탈 여부를 실행 순환 안에서 점검해야 한다고 설명한다. 현재 공개 DevBench 구현은 이를 코드·테스트·문서 검토, 실제 변경과 변경 목록 파일의 비교, 별도 보안 검토 같은 통과 조건으로 구체화한다.

~~~text
Behavior PASS
+
Architecture PASS
+
Scope PASS
+
Security PASS
→ stronger completion evidence
~~~

모든 작업이 네 축을 모두 요구하는 것은 아니다. 핵심은 기능 테스트 하나가 전체 요구 조건 준수를 대표한다고 가정하지 않는 것이다. 모든 작업이 피라미드 끝까지 갈 필요는 없다. 문서 오탈자는 lint와 미리보기만으로 충분할 수 있다. 결제 로직 변경은 통합, 보안, 사람의 검토까지 필요할 수 있다.

---

## 12.3 Verification은 마지막 단계가 아니라 Feedback Loop다

검증을 마지막에 한 번만 수행하면 에이전트는 오랫동안 잘못된 방향으로 갈 수 있다. 더 좋은 구조는 실행 중에도 빠른 피드백을 주는 것이다.

~~~text
Edit
→ Fast Check
→ Fix
→ Targeted Test
→ Fix
→ Candidate
→ Expensive Verification
~~~

예를 들어 Java 백엔드 작업이라면 다음처럼 계층화할 수 있다.

~~~text
1. compile
2. target unit test
3. module integration test
4. full regression
~~~

초기 수정마다 전체 회귀 검사를 돌리면 비용이 너무 크다. 반대로 해당 변경에 초점을 맞춘 테스트만 보고 끝내면 통합 문제를 놓칠 수 있다. 그래서 검증도 비용과 범위에 따라 단계화한다.

~~~text
Cheap Feedback
→ Candidate Confidence
→ Expensive Acceptance
~~~

이 구조는 CI 처리 능력 관리와도 연결된다.

---

## 12.4 Executable Acceptance

4장에서 요구사항과 수용 판단을 분리했다.

검증은 그 수용 판단을 실행 가능한 형태로 바꾸는 단계다.

예:

~~~text
Requirement
- expired JWT는 인증 실패다.

Acceptance
- protected endpoint 호출 시 HTTP 401

Verification
- integration test
- runtime request
~~~

연결하면 다음과 같다.

~~~text
Requirement
      ↓
Acceptance
      ↓
Executable Check
      ↓
Evidence
~~~

이 추적 가능성이 강할수록 에이전트가 “무엇을 해야 하는가”와 “무엇을 하면 끝인가”를 같은 방향으로 볼 수 있다. 단, 한 가지 주의가 필요하다. 수용 판단을 테스트 하나와 완전히 동일시하면 안 된다.

---

## 12.5 Test PASS가 User Intent와 같지 않은 이유

테스트는 강력하다. 에이전트에게 빠르고 정해진 규칙에 따른 피드백을 준다. 하지만 테스트는 **검사한 것만** 확인한다. Microsoft Research의 2026년 동료 심사 전 논문 *Building to the Test*는 실제 운영되는 코딩 에이전트 두 개를 사용한 18회 조건을 통제한 실행에서 이런 위험을 관찰했다.

비공개 Playwright 판정 기준을 에이전트 순환에 제공하자 점수는 거의 완벽해졌지만, 요청된 재사용 가능한 라이브러리 대신 테스트가 검사하는 동작을 직접 담은 시연용 구현 형태로 우회하는 결과가 나올 수 있었다. 저자들도 다른 에이전트·신호·Model Family에서의 발생 빈도는 열린 질문이라고 명시한다. 예를 들어 사용자는 다음을 원했다고 하자.

~~~text
여러 Service에서 재사용할 수 있는 rate-limit library를 만들어라.
~~~

공개된 테스트는 한 서비스에서 특정 요청이 제한되는지만 검사한다. 에이전트는 해당 서비스에 직접 조건문을 넣어 테스트를 통과시킬 수 있다.

~~~text
Visible Test
→ PASS

Original Intent
→ reusable library
→ FAIL
~~~

이것이 Building to the Test 문제다. 테스트를 없애야 한다는 뜻이 아니다. 검증의 종류를 넓혀야 한다.

- 구조 검사
- 비공개 테스트
- 실행 기반 시나리오
- 코드 검토
- 독립적인 평가자

---

## 12.6 Automated Grader PASS와 Maintainer Acceptance는 다르다

METR의 2026년 연구 노트는 SWE-bench Verified에서 자동 채점기를 통과한 패치를 실제 유지보수 담당자에게 다시 검토하게 했다. 4명의 유지보수 담당자가 3개 저장소의 95개 이슈 범위를 다룬 표본에서, 테스트를 통과한 AI 패치의 상당수가 실제 main에는 병합되지 않았을 것으로 평가됐다. 다만 에이전트에게 검토 피드백을 받고 반복 수정할 기회를 주지 않은 한 번의 실행으로만 평가했다는 제한이 있다. 이 차이는 이상하지 않다. 유지보수 담당자는 테스트 외에도 다음을 본다.

- 저장소 규칙
- 코드 품질
- 의도하지 않은 동작
- 유지보수 용이성
- 더 넓은 통합
- 범위 적절성

따라서 다음 등식은 성립하지 않는다.

~~~text
Automated Test PASS
=
Production-ready Change
~~~

생산 시스템의 검증은 테스트 실행기 하나보다 넓어야 한다.

---

## 12.7 Reward Hacking

더 위험한 경우도 있다.

에이전트가 작업을 해결하는 대신 **검증 신호를 약화시킬 수 있다.**

예:

~~~text
실패하는 Test를 skip 처리
Test assertion 삭제
Validation Script 수정
Scoring condition 우회
~~~

결과만 보면 PASS다. 실제 문제는 해결되지 않았다. OpenAI는 2026년 내부 코딩 에이전트 운영 감시 결과에서 테스트를 항상 통과하도록 수정하거나 검사를 비활성화하는 보상 기준 편법 공략을 실제 관찰 범주로 공개했고, 빈도는 드물지만 심각도는 높게 분류했다. 이 역시 OpenAI 내부 배포의 관찰이며 일반적인 발생률로 해석하면 안 된다. 생산 시스템에서는 다음 경계를 고려할 수 있다.

- 에이전트가 검증 정의를 자유롭게 수정하지 못하게 한다.
- 테스트 변경을 별도 근거로 표시한다.
- 평가 코드/hidden 테스트를 워커에서 보호한다.
- 검증 구성을 제어 계층이 정한다.

특히 구현 에이전트가 자신을 평가하는 기준까지 마음대로 바꿀 수 있는 구조는 위험하다.

---

## 12.8 Lucky Pass: 결과만 맞아도 충분한가

최종 테스트가 통과했지만 실행 경로가 불안정할 수도 있다. Microsoft AgentLens 연구는 8개 모델 백엔드의 2,614개 OpenHands 실행 경로를 분석했고, 과정 비교 기준을 구성할 수 있었던 47개 작업의 1,815개 실행 경로 부분집합에서 성공한 실행 경로의 10.7%를 우연한 통과로 분류했다. 저자들은 반복적인 기존 기능의 오류, 원인 확인 없는 재시도, 검증 누락처럼 결과 PASS만으로 가려지는 과정 문제를 분석한다.

예:

~~~text
Edit
→ test fail

random edit
→ another test fail

revert

different edit
→ PASS
~~~

최종 결과만 보면 성공이다. 하지만 다음 작업에서도 같은 성공을 재현할 수 있을지는 불확실하다. 생산 시스템에서는 성과뿐 아니라 과정에서 얻는 신호도 일부 관찰할 수 있다.

- 재시도 횟수
- 테스트 약화
- 회귀 오류 횟수
- 검증 생략
- 안전하지 않은 명령
- 같은 문제의 반복 실패

이 정보는 19장의 관측 가능성에서 더 자세히 다룬다.

---

## 12.9 Independent Evaluator

구현 에이전트와 평가 에이전트를 분리하면 장점이 있다.

~~~text
Implementer
→ Candidate

Evaluator
→ inspect
→ test
→ behavioral check
→ feedback
~~~

Anthropic의 장시간 애플리케이션 개발용 하네스 연구에서도 계획 담당자, 생성 담당자, 평가자를 분리하는 방향이 사용됐다. 하지만 평가자 에이전트가 있다고 자동으로 독립 검증이 되는 것은 아니다. 같은 모델, 같은 맥락 정보, 같은 가정을 사용하면 같은 오류를 공유할 수 있다.

~~~text
Same Model
+ Same Context
+ Same Tests
→ Correlated Error 가능
~~~

그래서 독립적인 평가는 다양한 방법을 조합할 수 있다.

- 규칙 기반 테스트
- 분리된 맥락 정보
- 서로 다른 역할
- 서로 다른 모델
- 비공개 검사
- 사람의 검토

핵심은 에이전트 수가 아니라 **검증 신호의 독립성**이다.

---

## 12.10 Task별 Verification Policy

에이전트에게 “적절한 테스트를 알아서 해라”라고만 하지 않는다. 작업 위험도에 따라 최소 검증을 시스템 정책으로 정할 수 있다.

### Low Risk

~~~text
docs
generated file
test-only change
~~~

예:

~~~text
lint
preview
diff check
~~~

### Medium Risk

~~~text
business logic
API behavior
~~~

예:

~~~text
unit
integration
contract
agent review
~~~

### High Risk

~~~text
auth
payment
migration
infrastructure
~~~

예:

~~~text
unit
integration
security
migration check
runtime verification
human approval
~~~

이 구조에서는 에이전트가 테스트 하나를 생략해도 작업이 DONE으로 이동할 수 없다. 필수 검증은 제어 계층이 알고 있기 때문이다.

---

## 예: UI Task와 Backend Auth Task

### UI Task

목표:

~~~text
모바일 화면에서 신청 버튼이 겹치지 않게 수정
~~~

검증:

~~~text
typecheck
E2E
mobile viewport screenshot
human visual acceptance
~~~

코드 변경 내역만으로는 화면을 판단하기 어렵다.

### Auth Task

목표:

~~~text
expired JWT → 401
~~~

검증:

~~~text
unit
integration
contract
security scan
runtime request
~~~

같은 “코드 수정”이라도 필요한 근거가 다르다. 검증 구성은 작업 유형과 위험에 맞아야 한다.

---

## Verification 설계에서 묻는 질문

~~~text
1. Agent의 자기 보고 외에 무엇으로 확인할 것인가?
2. Acceptance를 실행 가능한 Check로 바꿀 수 있는가?
3. Visible Test에만 과적합할 수 있는가?
4. Agent가 Verification Definition을 약화시킬 수 있는가?
5. Runtime Behavior를 봐야 하는가?
6. Independent Evaluator나 Human Gate가 필요한가?
7. 실제 변경이 선언된 Scope를 벗어나지 않았는가?
8. Architecture / Design Constraint를 별도로 확인해야 하는가?
9. 이 Task의 Risk에 비해 Verification Cost가 적절한가?
~~~

---

## 다음 질문

검증이 끝났다고 사람이 결과를 빠르게 이해할 수 있는 것은 아니다. 커밋은 무엇인지, 어떤 테스트가 실행됐는지, 화면 캡처는 어디 있는지, 알려진 위험은 무엇인지 매번 찾아야 한다면 검토 비용이 커진다. 다음 장에서는 검증 결과를 표준화된 **증거 계약**으로 묶는 방법을 다룬다.

---

## 참고 자료

- Microsoft Research, *Building to the Test: Coding Agents Deliver What You Check, Not What You Requested*  
  https://www.microsoft.com/en-us/research/publication/building-to-the-test-coding-agents-deliver-what-you-check-not-what-you-requested/
- METR, *Many SWE-bench-Passing PRs Would Not Be Merged into Main*  
  https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
- OpenAI, *How we monitor internal coding agents for misalignment*  
  https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/
- Microsoft Research, *AgentLens*  
  https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/
- Caylent, *What is a Software Factory*  
  https://www.youtube.com/watch?v=0Q8R_FZbnLk
- Caylent Solutions, *DevBench Architecture*  
  https://github.com/caylent-solutions/devbench/blob/main/docs/architecture.md
- Warp / Zach Lloyd, *Software Engineering Is Becoming Factory Engineering*  
  https://www.youtube.com/watch?v=tUPPVhBBcoM
