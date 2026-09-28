# 24장. Factory Maturity와 Autonomy를 어떻게 올릴 것인가

Software Factory를 만들기 시작하면 곧 다음 질문이 생긴다.

> 어디까지 자동화해야 하는가?

Worker가 하나일 때는 쉽다.

여러 Worker를 붙이고 Event Trigger를 연결하고 Backlog Selection까지 자동화하려 하면 “우리 Factory는 몇 단계인가”를 말하고 싶어진다.

하지만 여기서 하나를 조심해야 한다.

Factory의 **Maturity**와 Agent의 **Autonomy**는 같은 것이 아니다.

Human Review가 있다고 해서 낮은 Maturity인 것은 아니다.

반대로 Agent가 스스로 Task를 선택하고 Merge한다고 해서 높은 Reliability를 가진 것도 아니다.

이 책에서는 두 축을 분리한다.

---

## 24.1 Maturity와 Autonomy는 다른 축이다

### Maturity

질문:

> Factory System이 어떤 Production Capability를 갖췄는가?

예:

- Durable Task
- Retry
- Resume
- Parallel Worker
- Event Trigger
- Observability

### Autonomy

질문:

> 어떤 Decision Authority를 Agent/System에 위임했는가?

예:

- Work Selection
- Planning
- Execution
- Verification
- Acceptance
- Merge / Deploy

둘은 독립적이다.

예를 들어 매우 성숙한 Durable Factory가 있어도 Merge는 항상 Human이 할 수 있다.

반대로 간단한 Script가 자동으로 Code를 만들고 Merge할 수는 있지만 Recovery와 Audit이 약할 수 있다.

---

## 24.2 M0~M5 Maturity 후보

다음은 이 책에서 복잡한 Capability 조합을 설명하기 위해 사용하는 **비규범적 Taxonomy**다.

업계 표준, 인증 모델, 조직 평가 점수가 아니다. 번호가 높다고 더 좋은 조직을 뜻하지 않으며, 실제 조직은 여러 단계의 특성을 동시에 가질 수 있다.

### M0. Interactive Agent

~~~text
Human
→ Agent Session
→ Result
~~~

특징:

- 사람이 Session 직접 관리
- durable task 없음
- 수동 verification

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
- 기본 Isolation
- Result Contract

### M2. Durable Factory

추가:

- Task Store
- Attempt
- Retry
- Resume
- Human Wait
- Recovery

Worker Loss와 Task Loss가 분리된다.

### M3. Parallel Factory

추가:

- Multiple Workers
- Dependency
- Scheduler
- Conflict
- Capacity Management

### M4. Event-driven Factory

추가:

- CI / Issue / Schedule / Production Signal
- automatic task intake
- closed-loop feedback

### M5. Adaptive Factory

추가 후보:

- Work Selection Assistance
- Dynamic Routing
- Factory Improvement Loop
- guarded self-improvement

M5는 가장 높은 “좋음”을 의미하지 않는다.

필요한 조직에만 적합할 수 있다.

---

## 24.3 Autonomy Authority Matrix

Autonomy를 하나의 숫자로 만들지 않는다.

Decision별로 본다.

예시 Matrix는 다음과 같이 만들 수 있다.

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

이 표는 권장 RACI가 아니라 Authority를 분리해서 생각하기 위한 예시다. Task Risk와 조직 책임 구조에 따라 값은 달라진다.

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

조직 전체에 “Autonomy Level 4” 같은 하나의 숫자를 붙이면 이 차이를 놓친다.

---

## 24.5 다음 단계로 가기 전 확인할 것

Maturity를 올릴 때 Success Rate 하나만 보지 않는다.

예를 들어 M2에서 M3로 가기 전에 다음을 확인할 수 있다.

~~~text
Task independence 충분?
Retry 안정적?
Review queue 여유?
CI capacity 충분?
Conflict rate 낮음?
Evidence standardized?
~~~

Worker를 늘렸는데 Review가 이미 병목이면 M3 확장이 오히려 WIP를 늘릴 수 있다.

M3에서 M4로 갈 때는 다른 질문이 필요하다.

~~~text
Signal quality 충분?
Deduplication 있음?
Unsafe event 차단?
Task readiness 자동 판정 가능?
~~~

---

## 24.6 Autonomy 승급 조건

Agent에게 더 많은 Authority를 줄 때 다음 조건을 볼 수 있다.

~~~text
1. Failure가 관찰 가능한가?
2. Recovery가 가능한가?
3. Verification이 독립적인가?
4. Blast Radius가 제한되는가?
5. Audit 가능한가?
6. Human Escalation이 가능한가?
7. Downstream Capacity가 감당 가능한가?
~~~

이 조건이 약한데 Autonomy만 높이면 위험이 커진다.

> 높은 Autonomy는 목표가 아니라 Reliability와 Governance 위에서 선택하는 운영 정책이다.

---

## 24.7 Risk-based Autonomy

Autonomy는 Risk에 따라 달라져야 한다.

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

Risk-based Policy는 “Human이 항상 있어야 한다”와 “Human이 없어야 한다” 사이의 현실적인 운영 모델이다.

---

## 24.8 Self-improvement Authority는 늦게 넓힌다

Factory 개선 자체는 초기부터 일어날 수 있다. 사람이 반복 실패를 보고 문서나 Skill을 수정하는 것도 Factory Improvement다.

다만 Factory가 **자기 구성 변경을 스스로 제안하고 적용하는 Authority**는 더 늦게 넓히는 편이 안전하다.

예:

- Skill 개선
- Tool 추가
- Context 개선
- Worker Image 개선
- Eval 추가
- Routing Policy 개선

이런 Loop는 강력하다.

~~~text
Factory Work
→ Friction
→ Improvement Task
→ Better Factory
~~~

하지만 Factory가 자신의 평가 기준과 Security Policy까지 자유롭게 바꾸면 문제가 생긴다.

예:

~~~text
test too hard
→ weaken test

approval slows work
→ disable approval
~~~

이런 변화는 “개선”처럼 보일 수 있지만 실제로는 Governance 붕괴다.

---

## 24.9 Meta-change는 별도 Class로 관리한다

Factory Configuration 변경:

- System Instruction
- Skill
- Tool
- Hook
- Evaluator
- Model Routing
- Sandbox Image
- Network Policy

이 변경은 일반 Product Code보다 큰 Blast Radius를 가질 수 있다.

따라서 다음을 고려한다.

~~~text
Eval
→ Shadow
→ Canary
→ Approval
→ Rollout
→ Rollback
~~~

특히 Evaluator와 Security Policy 변경은 더 강한 Gate가 필요할 수 있다.

---

## 24.10 Shadow Mode

새 Harness나 Policy를 바로 Authoritative하게 사용하지 않는다.

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

Candidate가 충분히 안정적이면 승격한다.

Self-improvement를 Production에서 바로 자기 자신에게 적용하는 것보다 안전하다.

---

## 24.11 조직별 목표는 다르다

### Small Team 예시

Single Worker, Evidence, Human Review 중심의 M1~M2 성질만으로도 충분한 경우가 있다.

### Platform Team 예시

여러 Project와 Worker Profile, Event Trigger, Policy, Observability 때문에 M2~M4 성질이 함께 필요할 수 있다.

### Regulated Enterprise 예시

운영 Capability는 높아도 Autonomy는 일부 Decision에서 의도적으로 낮게 유지할 수 있다.

예:

- execution automated
- acceptance human
- deploy dual approval

이것은 뒤처진 구조가 아니다.

Risk Model에 맞는 구조다.

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

실제 조직에서는 일부 순서가 바뀔 수 있다. 이 도식은 maturity score가 아니라 dependency를 설명하는 휴리스틱이다.

중요한 것은 Autonomy를 첫 번째 목표로 두지 않는 것이다.

---

## 마지막 질문

이 책의 기술적 여정은 여기까지다.

하지만 남는 질문이 있다.

Agent가 점점 더 많은 Implementation을 수행한다면 개발자의 일은 무엇이 되는가.

Software Engineering은 Code Authoring에서 무엇으로 확장되는가.

Epilogue에서는 **Software Engineering에서 Software Production System Engineering으로 넓어지는 역할**을 정리한다.

---

## 참고 자료

- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  https://openai.com/index/harness-engineering/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Factory.ai, *Signals*  
  https://factory.ai/news/factory-signals
- Anthropic, *Agent Skills*  
  https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
