# Table of Contents

기준일: 2026-09-28

이 목차는 `planning/concept.md`와 `planning/scope.md`를 기준으로 설계한다.

제품별 기능 설명이 아니라 **AI Software Factory를 실제로 설계하고 운영하는 사고 흐름**을 따른다.

---

# 책의 중심 질문

> AI Agent에게 소프트웨어 작업을 위임하면서도, 작업 상태와 권한과 검증을 통제하고 실패를 복구하며 검증된 변경을 지속적으로 전달하려면 어떤 생산 시스템이 필요한가?

독자가 마지막에 답할 수 있어야 하는 질문:

- 어떤 Task를 Factory에 넣어야 하는가?
- Prompt와 Durable Task는 어떻게 다른가?
- Requirement와 Acceptance를 어디까지 구조화해야 하는가?
- 어떤 것은 시스템이 강제하고 어떤 것은 Agent에게 맡겨야 하는가?
- Worker와 Sandbox는 어떻게 구성해야 하는가?
- Agent에게 어떤 Context와 Tool을 줘야 하는가?
- Agent가 완료했다고 했을 때 무엇으로 검증할 것인가?
- Worker가 죽거나 Agent가 실패했을 때 어떻게 이어갈 것인가?
- 어떤 작업에 Human Gate가 필요한가?
- Multi-Agent는 언제 실제 이득이 있는가?
- Agent가 빨라진 뒤 Review/CI/Integration 병목은 어떻게 관리할 것인가?
- Factory를 어떤 지표로 평가할 것인가?
- 기존 CI/CD와 Platform Engineering을 어떻게 재사용할 것인가?
- 어느 순서로 Autonomy를 높일 것인가?

---

# 전체 흐름

```text
Coding Agent의 한계 이해
        ↓
AI Software Factory 정의
        ↓
Intent / Requirement / Acceptance
        ↓
Durable Task
        ↓
Control Plane
        ↓
Worker / Sandbox
        ↓
Harness / Context / Tool
        ↓
Controlled Autonomy
        ↓
Verification / Evidence
        ↓
Failure / Recovery
        ↓
Governance / Security
        ↓
Parallelism / Review / Integration
        ↓
Observability / Metrics
        ↓
Event-driven / Closed-loop
        ↓
Minimum Viable Factory
        ↓
Maturity / Autonomy
```

---

# Part I. Coding Agent에서 Software Factory로

## 1장. Coding Agent가 좋아진 뒤 무엇이 병목이 되는가

### 목적

AI Coding Agent의 코드 생성 능력이 빠르게 향상된 뒤 왜 새로운 시스템 문제가 등장하는지 설명한다.

### 핵심 질문

> Agent가 코드를 잘 쓰는데 왜 Software Factory가 필요한가?

### 핵심 내용

- Coding Assistant → Coding Agent
- Interactive Session의 장점과 한계
- 여러 Agent Session을 사람이 직접 관리할 때 생기는 Context Switching
- Agent throughput 증가와 Review / CI 병목
- Model Capability와 System Capability
- Test PASS와 실제 Acceptance의 차이
- AI 생산성 연구가 서로 다른 결론을 내는 이유
- Human Attention을 scarce resource로 보는 관점

### 사례

- OpenAI Harness / Symphony
- Stripe Minions
- METR productivity research
- Microsoft / DORA

### 핵심 메시지

> Coding speed가 빨라졌다고 Software Delivery 전체가 자동으로 빨라지는 것은 아니다.

---

## 2장. AI Software Factory란 무엇인가

### 목적

책 전체에서 사용할 최소 정의를 제시한다.

### 기본 정의

> AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.

### 최소 구성요소

```text
Durable Work
Delegated Execution
Controlled Autonomy
Independent Verification
Recoverability
Acceptance / Governance
Feedback
```

### 구분

```text
AI Software Factory
≠ Multi-Agent System
≠ Coding Agent Farm
≠ CI/CD with an LLM
```

### 짧은 역사 배경

Traditional Software Factory의 역사는 "왜 Factory라는 표현이 다시 등장하는가"를 설명하는 정도로만 사용한다.

---

## 3장. CI/CD, DevOps, Platform Engineering, Agent Platform과의 경계

### 목적

AI Software Factory가 기존 Software Engineering 체계와 어떤 관계인지 명확히 한다.

### 핵심 구분

```text
CI/CD
= 정의된 변경의 Build/Test/Delivery

Platform Engineering
= 안전하고 표준화된 생산 Capability 제공

Agent Platform
= Agent Runtime / Identity / Tool / Observability 제공

AI Software Factory
= Software Work를 검증된 변경으로 완료
```

### 다룰 내용

- NIST DevSecOps Software Factory reference
- Platform Golden Path
- Internal Developer Platform
- Agent Platform / Runtime
- Factory가 기존 시스템을 대체하지 않는 이유

### 핵심 메시지

> AI Software Factory는 DevOps를 버리고 새로 만드는 것이 아니라 기존 Delivery System에 Agent를 first-class worker로 넣는 진화다.

---

# Part II. Work를 정의하는 시스템

## 4장. Prompt가 아니라 Requirement와 Acceptance에서 시작한다

### 목적

Agent에게 일을 시키기 전에 무엇을 만들어야 하는지 명확히 정의하는 방법을 설명한다.

### 흐름

```text
Intent
→ Requirement
→ Clarification
→ Acceptance Criteria
→ Design Constraint
→ Task
```

### 핵심 내용

- 모호한 Issue가 Coding Agent 성능을 제한하는 이유
- Requirement-first / Design-first
- Acceptance Criteria
- Requirement Generator와 Acceptance Authority 분리
- Machine-checkable acceptance
- Specification Traceability

### 연구

- REAgent
- GitHub Spec Kit
- Kiro
- Human-AI Context Gap

### 핵심 메시지

> 잘못 정의된 일을 완벽하게 자동화하는 것은 생산성이 아니다.

---

## 5장. Durable Task: Session보다 오래 살아남는 작업 단위

### 목적

Factory의 기본 단위를 Prompt/Session이 아니라 Durable Task로 전환한다.

### Task 상태 후보

- Goal
- Scope
- Acceptance
- Dependency
- Priority
- Status
- Attempt
- Worker
- Workspace
- Base Revision
- Result Revision
- Verification
- Evidence
- Approval
- Failure
- Carryover

### 핵심 구분

```text
Prompt = interaction
Session = execution context
Task = durable work item
```

### 다룰 내용

- Context Window를 Task DB로 쓰면 안 되는 이유
- Task state와 Agent session state 분리
- Task graph
- Ready / Blocked / Running / Verifying / Awaiting Human / Done

---

## 6장. Task 크기, 분해, Dependency

### 목적

Factory가 처리하기 좋은 Work Unit을 설계한다.

### 핵심 내용

- 너무 작은 Task의 overhead
- 너무 큰 Task의 context / retry / review cost
- Task decomposition
- Dependency graph
- Retry scope
- Reviewable change size
- File/module ownership
- Runtime-structured decomposition
- Large Task와 Large PR를 분리하는 방법

### 핵심 메시지

> Task를 작게 만드는 것이 목적이 아니라 독립적으로 실행·검증·복구 가능한 단위로 만드는 것이 목적이다.

---

# Part III. Factory의 실행 구조

## 7장. Control Plane과 Execution Plane

### 목적

Factory 전체 architecture의 중심 경계를 설명한다.

### Control Plane

- Task lifecycle
- Scheduler
- Assignment
- Dependency
- Retry
- Approval
- Recovery
- Event history

### Execution Plane

- Worker
- Workspace
- Agent
- Tools
- Build/Test
- Runtime

### 기본 구조

```text
Durable Task
      ↓
Control Plane
      ↓
Worker Provisioning
      ↓
Execution Plane
```

### 핵심 메시지

> Worker가 Task를 소유하는 것이 아니라 Control Plane이 Task 완료 책임을 가진다.

---

## 8장. Worker, Sandbox, Workspace

### 목적

AI Agent가 실제로 일하는 execution environment를 설계한다.

### 핵심 내용

- Clean checkout
- Branch / Worktree
- Container / VM
- Filesystem isolation
- Prepared Environment
- Cache
- Snapshot
- Browser / Service
- Persistent Worker vs Ephemeral Worker

### 판단 기준

- reproducibility
- cold start
- state contamination
- long-running continuity
- security

### 핵심 메시지

> Worker는 잃을 수 있어도 Task는 잃지 않는다.

---

## 9장. Harness Engineering: Agent가 일할 수 있는 환경 만들기

### 목적

Model 이외의 execution system이 Agent 성능에 미치는 영향을 설명한다.

### Harness 구성

- Instruction
- Skill
- Tool
- Search
- Shell
- Browser
- MCP
- Result Filter
- Subagent
- Model Routing
- Execution Loop
- Review / Enforcement Gate
- Feedback Injection

### 연구

- OpenAI Harness Engineering
- SWE-agent ACI
- OpenHands SDK
- Caylent DevBench

### 핵심 메시지

> 더 좋은 Model과 더 좋은 Harness는 다른 개선 축이다.

---

## 10장. Context Engineering과 Agent Legibility

### 목적

Agent가 필요한 정보만 정확하게 찾게 만든다.

### 기본 원칙

> Progressive, Relevant, Minimal Context.

### 다룰 내용

- Repository Map
- Architecture docs
- Software Catalog
- AGENTS.md / CLAUDE.md
- Application legibility
- Logs / Metrics / Traces
- Tool output size
- Context freshness
- Context file empirical research

### 구조

```text
Entry Context
→ Relevant Docs
→ Skill
→ Tool
→ Runtime Evidence
```

### 핵심 메시지

> More Context는 Better Agent와 같은 말이 아니다.

---

## 11장. Controlled Autonomy: 무엇을 시스템에 두고 무엇을 Agent에게 맡길 것인가

### 목적

책 전체의 핵심 설계 철학을 구체화한다.

### System이 강제

- state
- dependency
- timeout
- retry
- budget
- permission
- required verification
- approval

### Agent가 판단

- exploration
- diagnosis
- hypothesis
- implementation strategy
- debugging sequence

### 연구

- Agentless
- Deterministic vs LLM-controlled orchestration
- Runtime-structured Task decomposition

### 핵심 메시지

> 이미 알고 있는 Rule은 code로 강제하고, 불확실한 Judgment에 Agent를 사용한다.

---

# Part IV. 결과를 믿을 수 있게 만드는 시스템

## 12장. Verification: Agent가 완료했다고 말한 뒤부터가 시작이다

### 목적

Agent self-report와 실제 completion을 분리한다.

### Verification 계층

```text
Static
→ Deterministic Tests
→ Runtime
→ Behavioral Evidence
→ Independent Evaluator
→ Human Acceptance
```

### 다룰 내용

- Build / Lint / Typecheck
- Unit / Integration / Contract
- E2E
- Browser
- Architecture Conformance
- Scope Conformance
- Security
- Benchmark
- Evaluator Agent

### 반례

- Building to the Test
- Reward Hacking
- SWE-bench PASS vs Maintainer Merge
- Lucky Pass

### 핵심 메시지

> Test PASS도 하나의 Evidence일 뿐 User Intent 전체와 동일하지 않다.

---

## 13장. Evidence Contract: 완료를 설명하지 말고 증명한다

### 목적

Factory Result를 표준화한다.

### Result 후보

```text
Task
Commit
Declared Scope
Changed Files

Verification
- command
- result
- duration

Behavior
- screenshot
- video
- endpoint result

Observability
- log
- trace

Known Limitation
Remaining Risk
```

### 다룰 내용

- Commit SHA
- Test result
- Screenshot / Video
- Artifact
- Before / After
- Demos over Diffs
- Evidence와 Provenance의 차이

### 핵심 메시지

> Agent의 자연어 보고보다 검증 가능한 Artifact가 먼저다.

---

## 14장. Failure와 Recovery: 실패를 정상 상태로 설계한다

### 목적

Production Agent가 실패한다는 전제로 Factory를 설계한다.

### Failure class

- Agent drift
- Tool failure
- Harness crash
- Worker loss
- Network
- Timeout
- Verification failure
- Policy denial
- Context loss

### Recovery ladder

```text
Tool Retry
→ Step Retry
→ Agent Nudge
→ Subtask Retry
→ Worker Restart
→ Reassignment
→ Human Escalation
```

### 핵심 내용

- Retry Budget
- Failure fingerprint
- Checkpoint
- Carryover
- Uncommitted work
- Resume vs Restart

### 핵심 메시지

> 한 번에 성공하는 능력보다 실패 후에도 Task를 보존하는 능력이 Factory reliability를 결정한다.

---

## 15장. Durable Execution: Crash를 넘어 이어지는 Work

### 목적

Long-running Agent가 분산 시스템 문제가 되는 이유를 설명한다.

### 다룰 내용

- Event history
- Checkpoint
- Replay
- Resume
- Async Human Wait
- Idempotency
- Duplicate Side Effect
- Replay-safe Tool
- Different-worker continuation

### 사례

- Microsoft Durable Task
- Temporal
- Google Agent Executor

### 핵심 메시지

```text
Memory
≠ Durable Execution
```

---

## 16장. Security, Identity, Governance

### 목적

Autonomy를 늘리기 전에 Blast Radius를 줄인다.

### Security

- Filesystem isolation
- Network policy
- Scoped credential
- Secret scan
- Branch protection
- Broker / Proxy
- Prompt injection boundary

### Identity / Governance

- initiating principal
- Agent identity
- delegated authority
- approval
- audit
- provenance

### 핵심 메시지

> Agent를 완전히 신뢰하게 만드는 것이 아니라 덜 신뢰해도 운영 가능한 경계를 만든다.

---

# Part V. 여러 Worker와 전체 Flow 관리

## 17장. Parallel Worker와 Multi-Agent: 언제 병렬화할 것인가

### 목적

Agent 수를 늘리는 것과 Useful Parallelism을 구분한다.

### 좋은 병렬화

- independent modules
- independent tests
- documentation
- separate research

### 나쁜 병렬화

- same schema
- same core file
- strict sequence
- hidden dependency

### 다룰 내용

- Fan-out / Fan-in
- Parent / Subagent
- Planner / Evaluator
- Ownership
- Conflict
- Correlated error
- Resource stampede

### 핵심 메시지

> 병렬화의 대상은 Agent가 아니라 독립 Task다.

---

## 18장. Review, CI, Integration: Coding 다음 병목

### 목적

Agent throughput이 증가한 뒤 downstream bottleneck을 관리한다.

### 다룰 내용

- Review Queue
- Verification Queue
- CI Capacity
- Merge Conflict
- Giant PR
- Stacked PR
- WIP Limit
- Integration branch
- Fan-in validation

### 핵심 사고 모델

```text
Factory Throughput
≈ min(
  Ready Work,
  Worker Capacity,
  Verification Capacity,
  Review Capacity,
  Integration Capacity,
  Deployment Capacity
)
```

### 핵심 메시지

> Worker를 늘리는 것이 Factory throughput 증가와 같지 않다.

---

## 19장. Observability와 Metrics: 무엇을 측정할 것인가

### 목적

Factory의 실제 성능을 Agent benchmark가 아니라 system-level metric으로 본다.

### Observability

- Task
- Attempt
- Worker
- Agent
- Tool
- Verification
- Human interaction
- Cost
- Failure

### Metrics

- Cycle time
- Execution time
- Human blocking time
- Review time
- Intervention
- Retry
- Acceptance
- Revert
- Escaped defect
- Cost per accepted change

### 핵심 메시지

> Token과 Agent Run이 아니라 검증된 변경이 전달되는 전체 Flow를 측정한다.

---

# Part VI. Factory를 조직의 Software Delivery System으로 확장하기

## 20장. Event-driven Factory와 Closed-loop SDLC

### 목적

사람의 Prompt 없이도 Factory가 Work Signal을 받을 수 있는 구조를 설명한다.

### Signal

- Issue
- CI Failure
- Review
- Vulnerability
- Scheduled maintenance
- Production incident

### 기본 흐름

```text
Signal
→ Diagnose
→ Scope
→ Risk
→ Task
→ Execute
→ Verify
→ Deliver
```

### Closed Loop

```text
Operate
→ Observe
→ Learn
→ New Work
→ Plan
```

### 핵심 메시지

> Signal을 바로 Agent Action으로 연결하지 않는다.

---

## 21장. Developer Platform과 Golden Path를 Factory가 사용하게 만들기

### 목적

Factory가 기존 Platform Engineering 자산을 재사용하도록 설계한다.

### Platform 제공

- Environment
- CI/CD
- Secrets
- Deployment
- Observability
- Software Catalog
- Golden Path
- Policy

### Agent-ready Platform

- machine-readable contract
- stable identifiers
- idempotent operations
- structured errors
- scoped identity

### 핵심 메시지

> Platform은 Capability를 제공하고 Factory는 Work를 흐르게 한다.

---

# Part VII. Minimum Viable Factory에서 Adaptive Factory까지

## 22장. Minimum Viable AI Software Factory

### 목적

처음부터 거대한 autonomous multi-agent system을 만들지 않고 가장 작은 Factory를 구축한다.

### 최소 구조

```text
Human selects Task
        ↓
Durable Task
        ↓
Isolated Worker
        ↓
Coding Agent
        ↓
Deterministic Verification
        ↓
Evidence
        ↓
Human Review
```

### 구축 순서

1. Agent-ready Repository
2. Reproducible Worker
3. Evidence Contract
4. Durable Task State
5. Retry / Resume
6. Event Trigger
7. Parallel Worker
8. Risk-based Automation

### 핵심 메시지

> Reliability → Observability → Recovery → Scale → Autonomy

---

## 23장. 실전 Reference Factory 만들기

### 목적

책 전체의 원칙을 작은 reference implementation으로 통합한다.

### 최소 흐름

```text
Task Create
→ Queue
→ Worker
→ Repository Workspace
→ Agent
→ Verification
→ Evidence
→ Human Gate
→ Done
```

### 반드시 실험할 시나리오

- Normal success
- Verification failure → Retry
- Worker kill → Resume
- Worker A loss → Worker B Reassignment
- Human approval
- Two independent tasks → Parallel
- Same-file conflict
- Evidence output

### 구현 원칙

- 특정 AI vendor에 종속되지 않게 설계
- 특정 workflow engine tutorial로 만들지 않음
- Runmesh는 case study / 실험 근거로 사용할 수 있으나 표준 구현으로 취급하지 않음

---

## 24장. Factory Maturity와 Autonomy를 어떻게 올릴 것인가

### 목적

조직이 한 번에 완전 자율화를 시도하지 않고 단계적으로 확장하게 한다.

### Maturity 후보

```text
M0 Interactive Agent
M1 Repeatable Worker
M2 Durable Factory
M3 Parallel Factory
M4 Event-driven Factory
M5 Adaptive Factory
```

### Autonomy 축

- Work Selection
- Planning
- Execution
- Verification
- Acceptance
- Merge / Deploy

Maturity와 Autonomy를 같은 척도로 합치지 않는다.

### 핵심 메시지

> 높은 Autonomy는 목표가 아니라 충분한 Reliability와 Verification 위에서 선택하는 운영 정책이다.

---

# Epilogue. Software Engineering에서 Software Production으로

### 목적

AI 시대 개발자의 역할과 Software Factory의 장기적 의미를 정리한다.

### 다룰 내용

- Humans steer, Agents execute의 한계와 의미
- Intent / Architecture / Acceptance / Risk
- Agent가 늘수록 Orchestration이 Software가 되는 이유
- Human Attention
- Socio-Technical System
- Self-improvement는 어디까지 가능한가

### 마지막 질문

> 앞으로 좋은 개발자는 더 많은 코드를 직접 작성하는 사람인가, 아니면 더 많은 검증된 변화를 안전하게 생산할 수 있는 시스템을 만드는 사람인가?

정답을 단정하지 않고 책에서 다룬 원칙을 바탕으로 독자가 자신의 조직에 맞게 판단하도록 마무리한다.

---

# Part 구조 요약

```text
Part I
왜 Factory가 필요한가

Part II
Factory가 처리할 Work를 어떻게 정의하는가

Part III
Agent가 어디서 어떻게 일하는가

Part IV
결과를 어떻게 믿고 실패를 어떻게 복구하는가

Part V
여러 Worker와 전체 Flow를 어떻게 관리하는가

Part VI
기존 Software Delivery System과 어떻게 연결하는가

Part VII
어떻게 작은 Factory부터 시작해 확장하는가
```

---

# 책 전체의 반복 패턴

각 장에서 가능한 한 같은 질문 구조를 사용한다.

1. 문제는 무엇인가
2. Interactive Agent만으로 왜 부족한가
3. Factory에서는 어떤 상태/경계를 추가하는가
4. 실패하면 어떤 문제가 생기는가
5. 어떤 Evidence로 검증하는가
6. 언제 Human이 개입하는가
7. 실제 산업/연구 사례는 무엇인가

---

# Case Study 배치 원칙

제품별 Chapter를 만들지 않는다.

예:

- Symphony → Durable Task / Control Plane 사례
- WorkOS Horizon → Event-driven Orchestration
- Stripe Minions → Unattended Execution + Human Review
- Anthropic → Long-running / Security / Multi-Agent
- GitHub → Hooks / Fleet / Review
- Factory.ai → Evidence / Software Factory framing
- Cursor → Worker / Browser Evidence
- Kiro / Spec Kit → Requirement / Specification
- OpenHands / SWE-agent → Harness / ACI

제품이 바뀌어도 Chapter 논리가 유지되어야 한다.

---

# Research 배치 원칙

논문은 "연구 소개" 자체가 목적이 아니다.

각 장의 설계 판단을 검증하거나 반례를 제공하는 방식으로 사용한다.

예:

- Agentless → Autonomy가 항상 좋은가?
- REAgent → Requirement 품질 영향
- Building to the Test → Test pass의 한계
- AgentLens → Lucky Pass
- AI Agents That Matter → Cost/Benchmark
- Human-Agent PR Studies → Execution vs Acceptance Authority
- AGENTS.md studies → Context의 한계

---

# 역사 배치

Traditional Software Factory 역사는 2장 초반에 짧게 배치한다.

목적:

> 왜 "Factory"라는 이름이 다시 등장했는가?

독립 Part 또는 긴 역사 장으로 확장하지 않는다.

---

# Advanced Topic 배치

다음은 본문 중 Box / Appendix / Advanced Section으로 제한한다.

- A2A / ACP
- Dynamic Model Routing
- Deep Workflow Engine internals
- Formal Verification
- Advanced Agent IAM
- Swarm / Debate / Market scheduling
- Self-modifying Factory

---

# 목차 단계에서 의도적으로 하지 않은 것

- 제품별 Part
- Agent Framework 비교
- 모델별 Benchmark 순위
- Fully Autonomous Organization 서사
- 모든 장에 Multi-Agent를 넣는 구성
- Foundation Model 설명에 많은 지면 사용
- Prompt Engineering 입문
- Kubernetes / DevOps 입문

---

# Chapter Plan 단계 규칙

다음 단계에서는 각 장마다 `chapters/NN/plan.md`를 만든다.

각 plan에 최소 포함:

- 장의 목적
- 독자가 답할 질문
- 핵심 주장
- 반드시 사용할 research source
- 반례
- 도식
- 실전 예제
- 포함/제외 경계
- 다음 장으로 연결

Draft는 Chapter Plan 승인 후 작성한다.
