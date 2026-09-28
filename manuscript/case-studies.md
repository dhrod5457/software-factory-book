# Case Study Box Plan

기준일: 2026-09-28

제품/회사 사례가 본문 일반 원칙을 지배하지 않도록 별도 Box로 분리할 후보를 정리한다.

---

## C01. OpenAI Symphony - Human Attention에서 Task Orchestration으로

추천 장: 1장 또는 7장

사용 근거:

- interactive session 관리 부담
- issue-driven orchestration
- orchestrator runtime state

주의:

- 내부 운영 수치를 업계 일반 한계로 쓰지 않는다.

---

## C02. WorkOS Horizon - Durable Control Plane과 Disposable Execution

추천 장: 2장 / 7장

사용:

- durable task/control state
- sandbox execution
- issue tracker integration

주의:

- Horizon architecture를 Factory 정답으로 제시하지 않는다.

---

## C03. Anthropic Managed Agents - Brain / Hands Separation

추천 장: 8~9장

사용:

- Session / Harness / Sandbox separation
- execution environment boundary

---

## C04. OpenAI Harness Engineering - Agent Legibility

추천 장: 9~10장

사용:

- giant AGENTS.md 실패
- repository as system of record
- agent-readable docs/runtime

---

## C05. GitHub Copilot Code Review - Better Tool, Worse Result

추천 장: 9장

사용:

- Tool upgrade regression
- instruction/workflow adaptation
- end-to-end harness evaluation

핵심:

> Tool capability 증가가 task quality 증가를 자동 보장하지 않는다.

---

## C06. Microsoft Building to the Test

추천 장: 12장

사용:

- visible test overfitting
- requested architecture vs observable validation

형식:

Research Box.

---

## C07. METR Maintainer Review

추천 장: 12장 / 18장

사용:

- grader PASS vs maintainer merge judgment

주의:

- single-shot patch 평가 한계 명시.

---

## C08. Microsoft AgentLens - Lucky Pass

추천 장: 12장

사용:

- outcome-only evaluation의 한계
- trajectory/process signal

---

## C09. Anthropic Multi-Agent Simulation

추천 장: 17장

사용:

- merge conflict
- conformity
- polling stampede
- file ownership strategy

주의:

- controlled simulation임을 Box 상단에 명시.

---

## C10. Microsoft / METR Productivity Contrast

추천 장: 1장

두 연구를 같은 “AI 생산성 수치”로 합치지 않고 measurement boundary 비교 Box로 만든다.

왼쪽:

Microsoft 2025 field experiment

오른쪽:

METR 2025 experienced OSS RCT

핵심:

> AI productivity는 population / task / workflow / metric에 따라 달라진다.

---

## C11. NIST Agent Identity Direction

추천 장: 16장

사용:

- identity
- authorization
- auditing

주의:

- Initial Public Draft / ongoing project
- 확정 표준 아님.

---

## C12. Google Agent Executor / Microsoft Durable Task

추천 장: 15장

용도:

- long-running durability를 Agent memory와 분리
- event history / checkpoint / resume

Vendor comparison 자체가 목적이 아니라 responsibility boundary 사례.

---

## C13. Google Jules Proactive Work

추천 장: 20장

사용:

- suggested task
- scheduled task
- deployment failure → PR

핵심:

> Event-driven work intake와 autonomous acceptance는 다른 축이다.

---

## C14. Runmesh Continuity Gap

추천 장: 23장

사례:

- Worker A loss
- Task 자체는 recover
- Worker B가 완료
- A의 uncommitted change는 전달되지 않아 재작업

교훈:

> Durable Task state alone is insufficient when useful workspace state cannot cross workers.

주의:

- 자체 구현 case study임을 명시
- 일반 원칙의 독립 근거로 사용하지 않는다.
