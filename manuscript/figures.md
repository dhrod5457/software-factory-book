# Figure Plan

기준일: 2026-09-28

텍스트 Diagram 중 출판용 Figure로 승격할 후보를 정리한다.

원칙:

- 장식용 그림은 만들지 않는다.
- 같은 개념을 여러 장에서 다시 그리지 않는다.
- 책 전체 논리를 재사용할 수 있는 Figure를 우선한다.
- 제품 UI Screenshot보다 오래 유지되는 architecture diagram을 우선한다.

---

## F01. Model → Agent → Factory Capability

배치: 1장

목적:

개인 Model Benchmark와 실제 Software Delivery System Capability를 분리한다.

구조:

```text
Model Capability
      ↓
Agent Capability
      ↓
Factory Capability
```

재사용:

- 9장 Harness
- 19장 Metrics

---

## F02. AI Software Factory Reference Loop

배치: 2장

책 전체의 대표 Figure.

```text
Intent / Signal
      ↓
Requirement / Specification
      ↓
Task / Acceptance
      ↓
Durable Control Plane
      ↓
Controlled Orchestration
      ↓
Worker / Sandbox
      ↓
Agent + Context + Tools
      ↓
Implementation
      ↓
Independent Verification
      ↓
Evidence
      ↓
Acceptance / Governance
      ↓
Delivery
      ↓
Feedback
      ↺
```

재사용:

- 책 소개
- 20장 Closed-loop
- Epilogue

---

## F03. Work Artifact Traceability

배치: 4장

```text
Requirement
→ Design
→ Task
→ Commit
→ Verification
→ Evidence
```

목적:

Prompt가 아니라 durable work artifact chain을 설명한다.

---

## F04. Task / Attempt / Worker State Model

배치: 5장

개념:

```text
Task
├─ Attempt A1 → Worker W1 → Failed
└─ Attempt A2 → Worker W2 → Passed
```

같이 표시:

- Task state
- Attempt history
- Worker replaceability

재사용:

- 7장
- 14장
- 23장

---

## F05. Control Plane vs Execution Plane

배치: 7장

```text
Durable Task
      ↓
Control Plane
      ↓
Assignment / Policy
      ↓
Execution Plane
      ↓
Result / Evidence
      ↺
```

목적:

책의 가장 중요한 architecture boundary 중 하나.

---

## F06. Worker Isolation Boundary

배치: 8장

Layer:

```text
Source
Process
Network
Credential
Runtime State
External Resource
```

Ephemeral/Persistent 선택을 같은 그림 안의 축으로 표현한다.

---

## F07. Harness / Context / Runtime 관계

배치: 9~10장 사이

```text
Task
 ↓
Harness
 ├─ Instructions
 ├─ Context
 ├─ Tool Interface
 └─ Feedback
 ↓
Model
 ↓
Tools
 ↓
Runtime / Repository
```

주의:

Sandbox와 Harness를 같은 Layer로 그리지 않는다.

---

## F08. Controlled Autonomy Stack

배치: 11장

```text
Organization Policy
        ↓
Factory Control Plane
        ↓
Workflow / Task Graph
        ↓
Agent Harness
        ↓
Model Decision
        ↓
Tool Action
```

위쪽은 durable / deterministic,
아래쪽은 adaptive / probabilistic하다는 축을 함께 표시한다.

---

## F09. Verification Pyramid

배치: 12장

```text
Static
Deterministic Test
Runtime Verification
Behavioral Evidence
Independent Evaluator
Human Acceptance
```

비용과 검증 범위가 함께 증가하는 그림.

주의:

상위 단계가 항상 더 좋은 것은 아니라는 주석 필요.

---

## F10. Evidence vs Provenance

배치: 13장

왼쪽:

```text
Evidence
- test
- screenshot
- benchmark
```

오른쪽:

```text
Provenance
- task
- agent
- revision
- policy
- approval
```

가운데 Result Revision으로 연결.

---

## F11. Recovery Ladder

배치: 14장

```text
Tool Retry
→ Step Retry
→ Agent Intervention
→ Subtask Retry
→ Worker Restart
→ Reassignment
→ Human Escalation
```

축:

- recovery scope
- cost
- state loss risk

---

## F12. Durable Execution Timeline

배치: 15장

```text
Run
→ Side Effect
→ Crash
→ Replay
→ Resume
```

Idempotency key / Event history / Checkpoint를 함께 표시.

---

## F13. Agent Security Delegation

배치: 16장

```text
Human Principal
      ↓ delegates
Task
      ↓
Agent Identity
      ↓
Scoped Capability
      ↓
Tool / Platform
```

Approval과 Audit를 옆 축으로 둔다.

---

## F14. Parallel Fan-out / Fan-in

배치: 17장

```text
Task Graph
  ├→ Worker A
  ├→ Worker B
  └→ Worker C
        ↓
   Integration Gate
```

같은 그림에 Conflict / Shared Resource 표시.

---

## F15. Factory Throughput Bottleneck

배치: 18장

```text
Factory Throughput
≈ min(
  Ready Work,
  Worker Capacity,
  Verification,
  Review,
  Integration,
  Deployment
)
```

1장의 병목 이동 설명에도 축소판 사용 가능.

---

## F16. Task Timeline / Observability

배치: 19장

```text
READY
→ RUNNING
→ VERIFYING
→ AWAITING_HUMAN
→ DONE
```

각 상태에 duration을 붙여 Agent time과 Human wait를 분리한다.

---

## F17. Signal → Task Conversion

배치: 20장

```text
Signal
→ Diagnose
→ Scope
→ Risk
→ Acceptance
→ Task
→ Execute
```

Alert ≠ Task 메시지를 시각화한다.

---

## F18. Factory ↔ Developer Platform

배치: 21장

```text
Factory
→ Golden Path / Platform API
→ CI/CD / Environment / Secret / Deploy / Observability
→ Infrastructure
```

Human Portal과 Agent API가 같은 Capability를 사용하도록 표현한다.

---

## F19. Minimum Viable Factory

배치: 22장

```text
Human selects Task
→ Durable Task
→ Isolated Worker
→ Agent
→ Verification
→ Evidence
→ Review / Policy
```

책의 실전 시작점.

---

## F20. Reference Factory Acceptance Scenarios

배치: 23장

Matrix 형태:

| Scenario | Expected behavior |
| --- | --- |
| Normal | DONE |
| Verification fail | bounded retry |
| Worker kill | task survives |
| Reassignment | partial work reused |
| Human wait | suspend/resume |
| Parallel independent | concurrent success |
| Conflict | detect/replan |

---

## F21. Maturity × Autonomy Matrix

배치: 24장

X축:

- Factory capability / maturity

Y축:

- decision authority / autonomy

핵심 메시지:

> Maturity와 Autonomy는 같은 축이 아니다.

책의 마지막 핵심 Figure.
