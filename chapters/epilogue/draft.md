# Epilogue. Software Engineering에서 Software Production으로

이 책은 “AI가 코드를 얼마나 잘 쓰는가”에서 시작하지 않았다.

오히려 Coding Agent가 충분히 좋아진 다음에 생기는 문제에서 시작했다.

코드 생성이 빨라지면 Review가 밀렸다.

Agent를 여러 개 실행하면 Human Attention이 부족해졌다.

Session이 길어지면 State가 사라졌다.

Test가 통과해도 User Intent를 놓칠 수 있었다.

Worker가 죽으면 Work Continuity가 깨졌다.

Autonomy를 높이면 Security와 Governance가 더 중요해졌다.

그래서 책의 관심은 자연스럽게 Model 밖으로 이동했다.

~~~text
Model
→ Agent
→ Harness
→ Worker
→ Control Plane
→ Verification
→ Governance
→ Delivery System
~~~

이 변화는 개발자의 역할에도 영향을 준다.

---

## 구현에서 Intent와 Verification으로 이동하는 Attention

Agent가 더 많은 구현을 수행하면 사람이 하는 일이 사라지는 것처럼 보일 수 있다.

실제로는 일부 Attention의 위치가 바뀐다.

기존:

~~~text
Code 작성
Command 실행
Test 반복
~~~

Factory가 담당할 수 있는 영역:

~~~text
Task Execution
Environment Setup
Repeated Verification
State Tracking
~~~

사람의 Attention은 다음 쪽으로 이동할 수 있다.

~~~text
Intent
Requirement
Architecture
Acceptance
Risk
Exception
Policy
Factory Improvement
~~~

이 이동이 모든 조직에서 같은 속도로 일어나는 것은 아니다.

하지만 공개 사례와 연구에서 반복되는 방향 중 하나다.

---

## Coding Skill은 사라지지 않는다

Agent가 코드를 작성한다고 Code를 이해할 필요가 없어지는 것은 아니다.

오히려 다음 능력은 계속 중요하다.

- Architecture
- Debugging
- Test Design
- Security
- Performance
- Production Judgment

Agent 결과를 검증하려면 기술적 깊이가 필요하다.

Factory 자체를 설계하려면 더 넓은 System Thinking이 필요하다.

“코드를 직접 적게 쓴다”와 “코드를 몰라도 된다”는 다른 말이다.

---

## Agent Management도 Software가 된다

Agent가 하나일 때는 사람이 직접 관리할 수 있다.

여러 개가 되면 다음 작업이 늘어난다.

- Start
- Monitor
- Retry
- Review
- Conflict
- Approval

사람에게 Terminal Window를 더 주는 방식으로는 확장되지 않는다.

그래서 이 관리 자체를 Software로 만든다.

~~~text
Queue
Policy
Scheduler
Verification
Evidence
Recovery
Dashboard
~~~

이것이 Software Factory의 중요한 의미 중 하나다.

Agent가 많아질수록 Orchestration과 Governance도 새로운 Software Engineering 대상이 된다.

---

## Human과 Agent를 역할이 아니라 Authority로 본다

“Agent는 구현하고 Human은 리뷰한다”는 구분도 너무 단순하다.

더 유용한 질문은 Decision Authority다.

~~~text
Who selects work?
Who plans?
Who executes?
Who verifies?
Who accepts risk?
Who merges?
Who deploys?
~~~

Task에 따라 답이 다를 수 있다.

Docs는 대부분 자동화할 수 있고, Production Migration은 Human Authority를 강하게 유지할 수 있다.

이 구조에서는 Human-in-the-loop가 중간마다 버튼을 누르는 방식이 아니다.

책임과 위험을 적절한 위치에 배치하는 Governance다.

---

## 생산성도 다시 정의해야 한다

Agent 시대에는 다음 숫자가 쉽게 늘어난다.

- Token
- Agent Run
- Pull Request
- Generated Code

하지만 이 책에서 반복해서 본 것은 다른 단위다.

~~~text
Accepted Change
~~~

더 구체적으로는 다음 질문이다.

> 사람이 감당 가능한 Attention과 비용 안에서 검증된 소프트웨어 변경이 지속적으로 전달되는가?

그래서 다음을 함께 본다.

- Cycle Time
- Review
- Retry
- Rework
- Revert
- Defect
- Cost
- Human Attention

Coding Speed는 이 시스템의 한 부분이다.

---

## Factory도 하나의 Product다

Software Factory는 한 번 만들고 끝나는 Infrastructure가 아니다.

실제 Work를 처리하면서 부족한 점이 드러난다.

~~~text
Missing Test
Flaky Environment
Poor Context
Slow Worker
Unsafe Permission
Review Bottleneck
~~~

이 Friction을 다시 Factory Backlog로 넣을 수 있다.

~~~text
Factory Work
→ Friction
→ Improvement
→ Better Factory
~~~

다만 Self-improvement를 무제한으로 자동화하면 위험하다.

Factory가 자신의 Evaluator를 약하게 만들거나 Security Policy를 제거하면 생산성이 좋아진 것처럼 보일 수 있다.

그래서 Factory 자체도 Versioning, Evaluation, Review, Rollback이 필요하다.

---

## Software Engineering에서 Software Production으로

Software Engineering이 코드 작성만을 의미한 적은 없다.

Requirement, Design, Test, Deployment, Operation까지 항상 포함했다.

AI Agent는 이 범위를 더 분명하게 만든다.

Implementation의 일부가 위임되면 다른 단계의 중요성이 더 잘 보인다.

~~~text
Intent
→ Work Design
→ Delegated Execution
→ Verification
→ Acceptance
→ Operation
→ Feedback
~~~

앞으로 좋은 Engineer의 한 형태는 더 많은 코드를 직접 작성하는 사람이 아닐 수도 있다.

대신 다음을 잘하는 사람일 수 있다.

- 좋은 Work를 정의한다.
- Agent가 일할 수 있는 Environment를 만든다.
- Rule과 Judgment를 분리한다.
- Completion을 검증 가능하게 만든다.
- Failure가 Work Loss로 이어지지 않게 한다.
- Human Attention이 필요한 곳을 선택한다.
- Factory 자체를 개선한다.

그렇다고 직접 구현 능력이 가치 없어진다는 뜻은 아니다.

이 시스템을 설계하고 실패를 진단하려면 여전히 깊은 Software Engineering이 필요하다.

---

## 마지막에 남는 네 가지 질문

Factory를 도입하려는 조직은 기술보다 먼저 다음을 답할 수 있어야 한다.

> 우리는 어떤 Work를 Agent에게 위임할 것인가?

> 그 Agent가 실패해도 안전한가?

> 완료를 누가 무엇으로 판단하는가?

> Agent가 늘어날수록 사람의 Attention은 실제로 더 가치 있는 판단에 쓰이고 있는가?

이 질문에 하나의 정답은 없다.

Repository, Risk, Team, Product가 다르기 때문이다.

이 책의 목적도 Fully Autonomous Organization이라는 하나의 종착점을 제시하는 것이 아니다.

더 현실적인 목표는 다음에 가깝다.

> **Agent에게 Work를 위임하되, State와 Verification과 Responsibility를 잃지 않는 Software Production System을 만드는 것.**

그 시스템이 각 조직에서 어디까지 자동화될지는 사람이 결정해야 한다.
