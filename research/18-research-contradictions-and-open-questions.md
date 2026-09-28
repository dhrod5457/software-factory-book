# Research Contradictions and Open Questions

기준일: 2026-09-28

AI Software Factory는 아직 빠르게 변하는 분야다.

현재 자료에는 서로 다른 결론과 운영 철학이 존재한다.

책에서는 이를 억지로 하나의 정답으로 합치지 않고 **대립 가설**로 관리한다.

---

# 1. Human Review는 사라지는가?

## 방향 A - Review를 유지

Stripe:

- unattended implementation
- human PR review

WorkOS:

- autonomous execution
- human merge approval

NIST:

- AI-generated output review / validation / accountable approval 강조

## 방향 B - Review를 축소/대체

StrongDM:

- scenario validation 중심
- human code review 제거 방향

OpenAI:

- agent-to-agent review 증가
- 일부 human review burden 축소

## 열린 질문

> 어느 정도의 executable acceptance / provenance / runtime validation이 있어야 human source review를 생략할 수 있는가?

---

# 2. Multi-Agent가 Single Agent보다 좋은가?

## Multi-agent 근거

- Anthropic C compiler
- GitHub Fleet
- Google Antigravity teamwork
- parallel independent search

## 반례

Anthropic multiagent research:

- dependency가 강한 software project에서 conflict
- PR merge collapse
- coordination overhead
- correlated behavior

## 열린 질문

> Task coupling이 어느 수준일 때 parallel agents의 이득이 coordination cost보다 커지는가?

---

# 3. Workflow를 강하게 규정해야 하는가?

## Structured Workflow

Spec Kit:

```text
Specify → Plan → Tasks → Implement
```

Kiro:

```text
Requirement → Design → Tasks
```

장점:

- traceability
- review
- predictability

## Flexible Agent Objective

Anthropic automated research agent experiment는 human-prescribed workflow가 agent flexibility를 불필요하게 제한하고 성능을 떨어뜨리는 경우를 보고한다.

OpenAI Symphony도 rigid state machine보다 objective + tools/context 방식으로 이동했다고 설명한다.

## 열린 질문

> 어떤 것은 state machine이 강제하고, 어떤 것은 Agent에게 맡겨야 하는가?

후보:

System이 강제:
- policy
- state
- dependency
- acceptance gate

Agent가 결정:
- search path
- implementation strategy
- debugging sequence

---

# 4. Test를 많이 만들면 Autonomy가 해결되는가?

## 긍정

- deterministic feedback
- scalable verification
- rapid agent iteration

## 반례

Microsoft:

- Building to the Test

Reward hacking research:

- test/evaluator manipulation
- held-out behavior gap

METR:

- benchmark pass와 maintainer merge 차이

## 열린 질문

> 테스트를 늘리는 것보다 validation diversity를 늘리는 것이 더 중요한가?

---

# 5. Agent Self-evaluation은 믿을 수 있는가?

## 긍정

- iterative self-test
- internal critic
- generated test

## 반례

Anthropic long-running harness:

- self-evaluation overly positive 가능
- separate evaluator 필요

Microsoft AgentLens:

- final pass가 좋은 trajectory를 의미하지 않음

## 열린 질문

> 동일 model의 second pass가 독립 evaluation이라고 볼 수 있는가?

---

# 6. Productivity는 얼마나 증가하는가?

## Positive evidence

Microsoft/Accenture/Fortune 100 RCT:

- completed task 증가

2026 technical worker self-report:

- 큰 perceived/value uplift

Vendor 사례:

- OpenAI / Stripe / WorkOS의 높은 throughput 보고

## Negative / mixed evidence

METR early-2025 experienced OSS RCT:

- AI 사용 시 19% slowdown

METR late-2025 follow-up:

- selection bias 때문에 정확한 측정 자체가 어려움

## 열린 질문

> Software Factory가 개인 productivity가 아니라 team-level accepted throughput을 얼마나 변화시키는가?

---

# 7. Persistent Worker vs Ephemeral Worker

## Ephemeral

장점:

- clean
- reproducible
- safe

## Persistent

장점:

- warm
- expensive setup 유지
- continuity

## 열린 질문

> 어떤 state를 cache하고 어떤 state를 매 Task reset해야 하는가?

---

# 8. One Model vs Model Routing

## One Model

- predictable
- simpler
- less routing overhead

## Routing

- task/model fit
- cost optimization
- specialization

문제:

- routing error
- cache invalidation
- evaluation complexity

## 열린 질문

> Router quality가 어느 수준 이상이어야 model diversity가 이득인가?

---

# 9. Agent가 다음 Task를 선택해야 하는가?

## Human-selected

- product intent
- accountability
- priority

## Proactive Agent

- maintenance
- dependency
- documentation
- test gap
- vulnerability

Google Jules 등은 proactive/scheduled direction을 보여준다.

## 열린 질문

> Work Selection Autonomy와 Work Execution Autonomy를 별도 수준으로 관리해야 하는가?

현재 답 후보는 YES지만 추가 사례가 필요하다.

---

# 10. Requirement도 Agent가 작성해야 하는가?

## 장점

- ambiguity discovery
- decomposition
- rapid draft

## 위험

- original intent drift
- plausible but wrong requirement
- requirement와 generated test가 동시에 같은 오해를 공유

## 열린 질문

> Requirement generator와 acceptance authority를 분리해야 하는가?

---

# 11. Agent-generated Tests를 Trust할 수 있는가?

Agent가 구현과 test를 모두 생성하면 같은 blind spot을 공유할 수 있다.

해결 후보:

- independent test generator
- existing test baseline
- property-based test
- held-out oracle
- human acceptance

---

# 12. Factory가 스스로 개선해야 하는가?

## 장점

- compounding harness quality
- repeated friction codification
- skills/tool improvement

## 위험

- reward hacking
- evaluator weakening
- policy erosion
- self-reinforcing wrong assumptions

## 열린 질문

> Factory meta-change에 어떤 shadow/canary/approval이 필요한가?

---

# 13. Autonomous Merge

조건 후보:

- low risk
- deterministic acceptance
- reversible
- strong provenance
- no sensitive path

하지만 evidence가 아직 충분하지 않다.

Industry examples는 human merge gate를 유지하는 경우가 많다.

---

# 14. Benchmark Capability vs Production Capability

OpenAI:

- benchmark contamination / broken task 문제

METR:

- test pass와 maintainer merge gap

Microsoft:

- lucky pass
- building to test

따라서:

```text
Benchmark Capability
<=> Useful Signal

but

Benchmark Score
!= Production Autonomy
```

---

# 15. AI-generated Code의 Long-term Maintainability

현재 empirical preprint가 나오기 시작했지만 아직 장기 데이터가 부족하다.

열린 질문:

- maintainability
- architecture drift
- technical debt
- knowledge ownership
- debugging cost

책에서는 아직 강한 결론을 피한다.

---

# 16. Human Skill Erosion

DORA와 개발자 연구에서:

- speed
- capability

뿐 아니라:

- learning
- expertise
- agency

문제가 제기된다.

Software Factory가 senior expertise를 더 가치 있게 만들 수도 있고 junior learning path를 줄일 수도 있다.

조직설계 자료가 더 필요하다.

---

# 17. Agent Identity Standard

NIST가 2026년 본격적으로 agent identity/authorization을 다루기 시작했다.

아직 실무 표준이 정착되지 않았다.

열린 질문:

- workload identity
- delegated authority
- signing
- agent provenance
- cross-agent trust

---

# 18. Factory Definition의 경계

아직 가장 큰 열린 질문.

### Narrow Definition

```text
Coding Agents
+ Orchestration
+ Verification
```

### Broad Definition

```text
Intent
→ Requirement
→ Planning
→ Implementation
→ Verification
→ Delivery
→ Operation Feedback
```

현재 자료는 Broad Definition 쪽으로 기울지만 최종 concept 단계에서 결정한다.

---

# 현재 연구에서 가장 강한 합의 후보

서로 다른 vendor/researcher 자료에서 반복되는 부분:

1. Agent output 자체를 신뢰하지 않고 evidence가 필요하다.
2. Task state를 Agent session 밖에 durable하게 유지하는 것이 중요하다.
3. execution environment isolation이 autonomy의 전제다.
4. Agent 수를 늘리기 전에 task independence가 필요하다.
5. test pass와 user intent satisfaction은 동일하지 않다.
6. human attention이 새로운 bottleneck이 될 수 있다.
7. coding throughput만 늘리면 review/CI/integration bottleneck이 커질 수 있다.
8. Factory capability는 model capability보다 넓다.
9. governance와 audit은 enterprise adoption에서 핵심이다.
10. requirement/acceptance quality가 implementation automation의 상한을 만든다.

---

# Concept 단계로 넘기기 전에 남은 질문

- Software Factory의 최소 구성요소는 무엇인가?
- "Factory"와 "Agent Platform"을 어떻게 구분하는가?
- Requirement/PM layer를 정의에 반드시 포함할 것인가?
- CI/CD와 Factory의 경계는 무엇인가?
- Human Gate를 정의의 필수요소로 볼 것인가, 선택 policy로 볼 것인가?
- Self-improvement를 핵심요소로 볼 것인가, 고급 단계로 볼 것인가?
- Autonomy Level taxonomy를 책 자체 개념으로 도입할 것인가?
- 실전 예제에서 어느 규모까지 구현할 것인가?
