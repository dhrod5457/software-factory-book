# 11장 설계 - Controlled Autonomy: 무엇을 시스템에 두고 무엇을 Agent에게 맡길 것인가

## 장의 목표

Factory에서 deterministic control과 probabilistic Agent judgment의 경계를 설계한다. 높은 autonomy 자체를 목표로 하지 않고 known rules는 system, open-ended search는 Agent에 둔다.

이 장의 핵심 질문:

> 어떤 결정을 Agent에게 맡겨야 하는가?

> 언제 deterministic workflow가 LLM-controlled workflow보다 낫나?

---

## 핵심 주장

> 이미 알고 있는 규칙과 상태는 deterministic system이 책임지는 편이 일반적으로 더 안정적이다.

> Agent autonomy는 unknown search, diagnosis, implementation strategy처럼 사전 규칙화하기 어려운 영역에 집중해야 한다.

> Autonomy는 binary switch가 아니라 decision authority의 분배 문제다.

---

## 독자가 얻는 것

- Rule/Heuristic/Judgment를 구분할 수 있다.
- System control과 Agent judgment의 boundary를 설계할 수 있다.
- Deterministic, Agent-directed, Hybrid orchestration을 비교할 수 있다.
- LLM loop에 state machine을 숨겨 넣는 anti-pattern을 식별할 수 있다.

---

## 반드시 사용할 Research

- `research/18-research-contradictions-and-open-questions.md`
- `research/24-academic-foundations-of-agentic-software-engineering.md`
- `research/26-orchestration-science-control-vs-autonomy.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- 더 Agentic할수록 더 좋다는 가정
- Retry count, permission, budget을 자연어 prompt로만 관리하는 구조
- 정형화 가능한 migration workflow까지 LLM이 매번 새로 계획하게 하는 방식

---

# 절 구성

## 11.1 세 가지 Control Model

Deterministic Pipeline, Agent-controlled, Hybrid Runtime을 비교한다.

## 11.2 Rule / Heuristic / Judgment

main push 금지 같은 Rule, worker routing 같은 Heuristic, implementation strategy 같은 Judgment를 구분한다.

## 11.3 System이 소유해야 할 상태

Task state, dependency, timeout, retry, permission, budget, required verification, approval을 external authority로 둔다.

## 11.4 Agent가 잘하는 영역

code exploration, diagnosis, hypothesis, debugging path, implementation alternative를 설명한다.

## 11.5 연구 근거

Agentless와 deterministic-vs-LLM orchestration 연구를 통해 autonomy가 cost/variance를 늘릴 수 있음을 보여준다.

## 11.6 Recovery Scope

Tool Retry → Step Retry → Agent Nudge → Worker restart로 가장 작은 recovery boundary를 선택하는 원칙을 소개한다.


---

## 필요한 구조 / 그림

1. Control hierarchy: Organization Policy → Control Plane → Workflow → Harness → Model → Tool
2. Rule/Heuristic/Judgment matrix
3. Deterministic vs Agent-directed vs Hybrid comparison

---

## 실전 예제 / 실험

- DB migration pipeline은 deterministic, failing test root cause 분석은 Agent judgment로 분리
- Agent가 retry count를 무시하고 loop에 빠지는 예와 external retry budget 비교

---

## 본문에서 의도적으로 다루지 않을 내용

- Autonomy maturity 전체 taxonomy
- self-improvement
- multi-agent coordination 상세

---

## 앞뒤 장 연결

12장에서는 Agent가 만든 결과를 system이 어떤 Verification Layer로 판정할지 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
