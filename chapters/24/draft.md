# 24장. Factory Maturity와 Autonomy를 어떻게 올릴 것인가

소프트웨어 생산 시스템을 만들기 시작하면 곧 다음 질문이 생긴다.

> 어디까지 자동화해야 하는가?

워커가 하나일 때는 쉽다. 여러 워커를 붙이고 이벤트 시작 조건을 연결하고 할 일 목록 선택까지 자동화하려 하면 “우리 생산 시스템은 몇 단계인가”를 말하고 싶어진다. 하지만 여기서 하나를 조심해야 한다. 생산 시스템이 운영 기능을 얼마나 갖췄는지를 나타내는 **성숙도(Maturity)**와 에이전트에게 판단 권한을 얼마나 맡겼는지를 나타내는 **자율성(Autonomy)**은 같은 것이 아니다. 사람의 검토가 있다고 해서 낮은 성숙도인 것은 아니다.

반대로 에이전트가 스스로 작업을 선택하고 병합한다고 해서 높은 신뢰성을 가진 것도 아니다. 이 책에서는 두 축을 분리한다.

---

## 24.1 Maturity와 Autonomy는 다른 축이다

### Maturity

질문:

> 생산 시스템이 어떤 운영 환경 수행 능력을 갖췄는가?

예:

- 지속 작업
- 재시도
- 중단 지점부터 재개
- 병렬 워커
- 이벤트 시작 조건
- 관측 가능성

### Autonomy

질문:

> 어떤 결정 권한을 에이전트·시스템에 위임했는가?

예:

- 작업 선택
- 계획 수립
- 실행
- 검증
- 수용 판단
- 병합 / 배포

둘은 독립적이다. 예를 들어 매우 성숙한 중단 뒤에도 유지되는 생산 시스템이 있어도 병합은 항상 사람이 할 수 있다. 반대로 간단한 스크립트가 자동으로 코드를 만들고 병합할 수는 있지만 복구와 감사가 약할 수 있다.

---

## 24.2 M0~M5 Maturity 후보

다음은 여러 운영 기능의 조합을 설명하기 위해 이 책에서 사용하는 **분류 체계**다. 반드시 따라야 하는 규범을 뜻하지 않는다. 업계 표준, 인증 모델, 조직 평가 점수가 아니다. 번호가 높다고 더 좋은 조직을 뜻하지 않으며, 실제 조직은 여러 단계의 특성을 동시에 가질 수 있다.

### M0. Interactive Agent

~~~text
Human
→ Agent Session
→ Result
~~~

특징:

- 사람이 세션 직접 관리
- 지속 작업 없음
- 수동 검증

### M1. Repeatable Worker

~~~text
Task
→ Isolated Worker
→ Agent
→ Verification
→ Evidence
~~~

특징:

- 반복 가능한 실행
- 기본 격리
- 결과 형식 규약

### M2. Durable Factory

추가:

- 작업 저장소
- 시도
- 재시도
- 중단 지점부터 재개
- 사람의 판단을 기다리는 시간
- 복구

워커 중단과 작업 손실이 분리된다.

### M3. Parallel Factory

추가:

- 여러 워커
- 의존 관계
- 작업 배정기
- 충돌
- 처리 능력 관리

### M4. Event-driven Factory

추가:

- CI / 이슈 / 일정 / 운영 환경 신호
- 자동 작업 접수
- 닫힌 순환을 이루는 피드백

### M5. Adaptive Factory

추가 후보:

- 작업 선택 보조
- 동적 경로 선택
- 생산 시스템 개선 순환
- 통제된 자체 개선

M5는 가장 높은 “좋음”을 의미하지 않는다. 필요한 조직에만 적합할 수 있다.

---

## 24.3 Autonomy Authority Matrix

자율성을 하나의 숫자로 만들지 않는다. 결정별로 본다. 예시 표는 다음과 같이 만들 수 있다.

| Decision | Human | Agent | System/Policy |
| --- | --- | --- | --- |
| Work Selection | A | C | R |
| Planning | A/C | R | |
| Execution | C | R | |
| Verification | C | R | R |
| Acceptance | A | C | Gate |
| Merge / Deploy | A/R | C | Gate |

A = Accountable  
R = Responsible  
C = Consulted

이 표는 권장 RACI가 아니라 권한을 분리해서 생각하기 위한 예시다. 작업 위험도와 조직 책임 구조에 따라 값은 달라진다.

---

## 24.4 같은 조직도 Task마다 Autonomy가 다르다

예:

### Documentation

~~~text
Work Selection: system
Execution: agent
Verification: automated
Acceptance: automated
Merge: automated
~~~

### Business Logic

~~~text
Work Selection: human/system
Execution: agent
Verification: automated + agent
Acceptance: human
Merge: human
~~~

### Production Migration

~~~text
Work Selection: human
Planning: agent + human
Execution: controlled tool
Verification: strong automated
Acceptance: specialist human
Deploy: explicit approval
~~~

조직 전체에 “자율성 수준 4” 같은 하나의 숫자를 붙이면 이 차이를 놓친다.

---

## 24.5 다음 단계로 가기 전 확인할 것

성숙도를 올릴 때 성공률 하나만 보지 않는다. 예를 들어 M2에서 M3로 가기 전에 다음을 확인할 수 있다.

~~~text
Task independence 충분?
Retry 안정적?
Review queue 여유?
CI capacity 충분?
Conflict rate 낮음?
Evidence standardized?
~~~

워커를 늘렸는데 검토가 이미 병목이면 M3 확장이 오히려 WIP를 늘릴 수 있다. M3에서 M4로 갈 때는 다른 질문이 필요하다.

~~~text
Signal quality 충분?
Deduplication 있음?
Unsafe event 차단?
Task readiness 자동 판정 가능?
~~~

---

## 24.6 Autonomy 승급 조건

에이전트에게 더 많은 권한을 줄 때 다음 조건을 볼 수 있다.

~~~text
1. Failure가 관찰 가능한가?
2. Recovery가 가능한가?
3. Verification이 독립적인가?
4. Blast Radius가 제한되는가?
5. Audit 가능한가?
6. Human Escalation이 가능한가?
7. Downstream Capacity가 감당 가능한가?
~~~

이 조건이 약한데 자율성만 높이면 위험이 커진다.

> 높은 자율성은 목표가 아니라 신뢰성과 권한·책임 관리 체계 위에서 선택하는 운영 정책이다.

---

## 24.7 Risk-based Autonomy

자율성은 위험에 따라 달라져야 한다.

예:

~~~text
Docs
→ auto merge 가능

Unit Test
→ automated acceptance 가능

Feature Code
→ human review

Auth / Payment
→ specialist review

Production Migration
→ explicit approval
~~~

위험도에 따른 정책은 “사람이 항상 있어야 한다”와 “사람이 없어야 한다” 사이의 현실적인 운영 모델이다.

---

## 24.8 Self-improvement Authority는 늦게 넓힌다

생산 시스템 개선 자체는 초기부터 일어날 수 있다. 사람이 반복 실패를 보고 문서나 스킬을 수정하는 것도 생산 시스템 개선이다. 중요한 것은 자체 개선을 막연한 “에이전트가 스스로 더 똑똑해진다”로 표현하지 않는 것이다. 실제 생산 시스템에서는 실행 결과와 사람의 수정을 관찰해 **개선 후보를 만드는 순환**으로 설계할 수 있다. Zach Lloyd는 예로 코드 검토 에이전트의 의견을 숙련된 엔지니어가 수정했을 때 관찰자 에이전트가 그 수정을 관찰하고 다음 실행을 위해 검토 스킬을 개선하는 스킬 순환을 제시한다.

~~~text
Agent Execution
      ↓
Observable Result
      ↓
Human Correction / Verification Failure
      ↓
Observer
      ↓
Failure Pattern / Improvement Candidate
      ↓
Prompt / Skill / Rule / Context Candidate
~~~

여기까지는 개선 **후보 생성**이다. 이 책의 생산 시스템에서는 후보가 곧바로 실제 운영 중인 생산 시스템을 바꾸지 않는다.

~~~text
Observe
→ Propose
→ Evaluate
→ Shadow
→ Approve
→ Promote
→ Monitor
~~~

즉 자체 개선도 일반 소프트웨어 변경처럼 검증과 최종 수용 권한을 가져야 한다. 이 원칙이 없으면 생산 시스템은 자신의 성공 기준을 낮추는 방향으로도 “개선”될 수 있다.

2026년 공개 사례에는 Factory.ai의 Signals처럼 세션에서 반복되는 불편과 장애를 분석해 개선 이슈와 수정으로 연결하는 피드백 순환 구현이 있고, Anthropic도 Agent Skills를 소개하며 장기적으로 에이전트가 스킬을 직접 생성·편집·평가하는 방향을 언급했다. 전자는 한 회사의 제품 구현이고, 후자는 당시 “향후 탐색”으로 제시한 방향이다. 이를 일반적인 스스로 개선하는 생산 시스템이 이미 확립됐다는 근거로 보지는 않는다.

따라서 생산 시스템이 **자기 구성 변경을 스스로 제안하고 적용하는 권한**은 더 늦게 넓히는 편이 안전하다.

예:

- 스킬 개선
- 도구 추가
- 맥락 정보 개선
- 워커 이미지 개선
- 평가 추가
- 경로 선택 정책 개선

이런 순환은 강력하다.

~~~text
Factory Work
→ Friction
→ Improvement Task
→ Better Factory
~~~

하지만 생산 시스템이 자신의 평가 기준과 보안 정책까지 자유롭게 바꾸면 문제가 생긴다.

예:

~~~text
test too hard
→ weaken test

approval slows work
→ disable approval
~~~

이런 변화는 “개선”처럼 보일 수 있지만 실제로는 권한과 책임 관리 붕괴다.

---

### Learned Skill은 Candidate로 시작한다

일부 에이전트 제품은 사람이 브라우저에서 작업 흐름을 한 번 보여주면 이를 스킬로 저장하거나, 에이전트에게 스킬을 생성·수정하게 할 수 있는 방향을 제공한다. 이 기능은 생산 시스템 개선 순환의 좋은 입력이 될 수 있다. 하지만 에이전트가 새 스킬을 만들었다고 곧바로 실제 운영 중인 생산 시스템의 표준 스킬로 승격하면 안 된다.

~~~text
Observed Workflow
      ↓
Candidate Skill
      ↓
Eval
      ↓
Human / Policy Review
      ↓
Version
      ↓
Shadow / Canary
      ↓
Production
~~~

이 구분은 자체 개선에서 중요하다. 에이전트가 자신의 반복 작업을 더 잘 수행하도록 절차를 제안하는 것은 비교적 낮은 위험의 개선일 수 있다. 반면 다음 변경은 피해 범위가 크다.

- 검증 약화
- 승인 제거
- 권한 확대
- 보안 규칙 수정
- 평가자 기준 변경

따라서 "에이전트가 학습한다"는 표현보다 어떤 변경이 후보로 생성되고 누가 실제 운영의 기준 설정으로 승격하는가를 명확히 하는 편이 안전하다.

### Session Friction을 Improvement Candidate로 바꾼다

자체 개선을 처음부터 생산 시스템이 자기 코드를 마음대로 수정하는 기능으로 볼 필요는 없다. 더 현실적인 출발점은 실제 에이전트 세션과 작업 시간 기록에서 반복되는 불편과 장애를 찾는 것이다. WorkOS가 설명한 향후 방향도 이쪽에 가깝다. 자체 인프라를 더 많이 소유하고 세션을 관찰하면서 다음과 같은 질문을 찾으려 한다.

- 에이전트가 반복해서 같은 실수를 하는가
- 새 스킬이 필요한가
- 기존 스킬이 저장소 변화 때문에 낡았는가
- 도구나 맥락 정보 탐색이 반복해서 막히는가
- 격리 환경 자체가 병목인가

이를 생산 시스템 개선 순환으로 표현하면:

~~~text
Execution
→ Friction Signal
→ Improvement Candidate
→ Skill / Tool / Context / Infrastructure Change
→ Eval
→ Promotion
~~~

이 접근의 장점은 자체 개선의 입력이 추상적인 "더 똑똑해져라"가 아니라 관찰 가능한 실패와 반복 비용이라는 점이다. 단, 발표에서 메모리 계층과 일부 자체 개선 기능은 향후 방향으로 설명된 부분이므로 현재 실제 운영 능력으로 일반화하지 않는다.

## 24.9 Meta-change는 별도 Class로 관리한다

생산 시스템 설정 변경:

- 시스템 지시사항
- 스킬
- 도구
- 후크
- 평가자
- 모델 선택 규칙
- 격리 환경 이미지
- 네트워크 정책

이 변경은 일반 제품 코드보다 큰 피해 범위를 가질 수 있다. 따라서 다음을 고려한다.

~~~text
Eval
→ Shadow
→ Canary
→ Approval
→ Rollout
→ Rollback
~~~

특히 평가자와 보안 정책 변경은 더 강한 통과 조건이 필요할 수 있다.

---

## 24.10 Shadow Mode

새 하네스나 정책을 바로 판단의 기준으로 사용하지 않는다.

~~~text
Production Factory
→ real task
→ authoritative result

Candidate Factory
→ same / sampled task
→ shadow result

Compare
→ quality
→ cost
→ safety
~~~

후보가 충분히 안정적이면 승격한다. 자체 개선을 운영 환경에서 바로 자기 자신에게 적용하는 것보다 안전하다.

---

## 24.11 조직별 목표는 다르다

### Small Team 예시

단일 워커, 근거, 사람의 검토 중심의 M1~M2 성질만으로도 충분한 경우가 있다.

### Platform Team 예시

여러 프로젝트와 워커 구성, 이벤트 시작 조건, 정책, 관측 가능성 때문에 M2~M4 성질이 함께 필요할 수 있다.

### Regulated Enterprise 예시

운영 수행 능력은 높아도 자율성은 일부 결정에서 의도적으로 낮게 유지할 수 있다.

예:

- 실행 자동화된
- 수용 판단 사람
- 배포 이중 승인

이것은 뒤처진 구조가 아니다. 위험 모델에 맞는 구조다.

---

## 24.12 이 책의 도입 순서

지금까지의 내용을 한 줄로 정리하면 다음과 같다.

~~~text
Agent-ready Repository
→ Reproducible Worker
→ Verification
→ Evidence
→ Durable Task
→ Recovery
→ Observability
→ Parallelism
→ Event Trigger
→ Risk-based Autonomy
→ Guarded Self-improvement
~~~

더 짧게 줄이면:

~~~text
Reliability baseline
→ Recovery + Observability
→ Scale
→ Autonomy
~~~

실제 조직에서는 일부 순서가 바뀔 수 있다. 이 도식은 성숙도 점수가 아니라 의존 관계를 설명하는 휴리스틱이다. 중요한 것은 자율성을 첫 번째 목표로 두지 않는 것이다.

---

## 마지막 질문

이 책의 기술적 여정은 여기까지다. 하지만 남는 질문이 있다. 에이전트가 점점 더 많은 구현을 수행한다면 개발자의 일은 무엇이 되는가. 소프트웨어 공학은 코드 작성에서 무엇으로 확장되는가. 에필로그에서는 **소프트웨어 공학에서 소프트웨어 생산 시스템 설계로 넓어지는 역할**을 정리한다.

---

## 참고 자료

- Cursor, *Work with Grok Bot*  
  https://cursor.com/docs/grok-bot/work
- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  https://openai.com/index/harness-engineering/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Factory.ai, *Signals*  
  https://factory.ai/news/factory-signals
- Anthropic, *Agent Skills*  
  https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Warp / Zach Lloyd, *Software Engineering Is Becoming Factory Engineering*  
  https://www.youtube.com/watch?v=tUPPVhBBcoM
