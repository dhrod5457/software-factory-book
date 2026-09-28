# Scope

기준일: 2026-09-28

## 범위 원칙

이 책의 중심은 **AI Coding Agent를 반복 가능한 소프트웨어 생산 시스템의 Worker로 배치하고, Task·권한·검증·복구·전달을 어떻게 설계할 것인가**이다.

새로운 주제를 추가할 때 다음 질문으로 판단한다.

> 이 내용이 독자가 실제 AI Software Factory를 설계·도입·운영하는 데 직접 도움이 되는가?

- YES: 핵심 본문
- 직접 필요하지만 구현 깊이가 높은 내용: Advanced Topic
- 흥미롭지만 핵심 흐름을 벗어남: `planning/future-topics.md`
- 일반 Agent/AI 이론에 가까움: 제외

책은 "모든 개발을 완전 자율화하는 법"이 아니라 **어떤 작업을 어떤 통제 구조 안에서 Agent에게 위임할 것인가**를 다룬다.

---

# 대상 독자

주 대상:

- Senior Software Engineer
- Tech Lead / Architect
- Platform Engineer
- DevOps / DevSecOps Engineer
- Engineering Manager
- AI Coding Agent를 팀 단위로 확장하려는 개발자

독자는 다음을 이미 알고 있다고 가정한다.

- Git / Branch / Pull Request
- Build / Test / CI/CD
- 기본적인 Backend / Frontend 개발 흐름
- Container 또는 독립 실행환경의 개념
- LLM / Coding Agent의 기본 사용 경험

다음은 사전 지식으로 요구하지 않는다.

- Multi-Agent 연구
- MCP / A2A / ACP 세부 사양
- Kubernetes internals
- Foundation Model 학습
- Distributed workflow engine 구현
- Formal verification

---

# 책의 중심 질문

책 전체는 다음 질문을 반복해서 답한다.

> 이 작업을 Agent에게 맡길 수 있는가?

그리고 더 중요한 다음 질문:

> 맡길 수 있다면, 어떤 Task 상태·권한·실행환경·검증·복구 구조 안에서 맡겨야 하는가?

---

# 핵심 본문 범위

## 1. AI Software Factory의 정의와 경계

반드시 다룬다.

- Coding Assistant → Coding Agent → Factory Worker
- Prompt / Session과 Durable Task의 차이
- AI Software Factory 최소 정의
- CI/CD와의 차이
- DevOps / DevSecOps와의 관계
- Platform Engineering과의 관계
- Agent Platform / Runtime과의 관계
- Multi-Agent System과의 차이

핵심 메시지:

> Agent Platform은 Agent를 실행한다. Software Factory는 Software Work를 완료한다.

---

## 2. Intent → Requirement → Task

Factory는 코딩 단계에서 시작하지 않는다.

다룰 내용:

- Intent
- Requirement
- Specification
- Acceptance Criteria
- Design constraint
- Task decomposition
- Dependency
- Ready Contract
- Requirement → Task → Verification traceability

Agent가 Requirement를 자동 작성하는 것은 필수가 아니다.

핵심은 **작업이 실행 가능한 상태인지**를 정의하는 것이다.

다루지 않을 것:

- Product Strategy 자동화
- 시장 조사 Agent
- Roadmap 자동 결정
- CEO/PM 대체론

---

## 3. Durable Task

책의 핵심 개념 중 하나다.

다룰 상태:

- Task ID
- Goal
- Scope
- Acceptance
- Dependency
- Priority
- Status
- Attempt
- Worker
- Workspace
- Base / Result Revision
- Verification
- Evidence
- Approval
- Failure / Carryover

핵심:

```text
Prompt = interaction
Task = durable work
```

Context Window나 chat history를 Task database처럼 사용하는 패턴을 피한다.

---

## 4. Control Plane

Factory의 중심 architecture로 다룬다.

책에서 Control Plane이 책임지는 것:

- Task lifecycle
- readiness
- dependency
- scheduling
- assignment
- retry
- timeout
- approval
- recovery
- result state
- event history

Control Plane이 직접 code를 작성해야 한다는 의미는 아니다.

핵심:

> Worker가 아닌 시스템이 Task 완료 책임을 가진다.

---

## 5. Controlled Autonomy

이 책의 핵심 설계 철학으로 다룬다.

### Deterministic Control

- state
- retry
- timeout
- permission
- dependency
- budget
- required checks
- approval

### Agent Judgment

- exploration
- diagnosis
- hypothesis
- implementation strategy
- debugging
- safe tool choice

다룰 연구:

- Agentless
- deterministic vs LLM-controlled orchestration
- runtime-structured decomposition

핵심:

> 이미 알고 있는 규칙을 LLM에게 다시 추론시키지 않는다.

---

## 6. Worker / Sandbox / Runtime

Agent가 실제 일을 수행하는 실행환경을 다룬다.

필수 개념:

- Repository checkout
- Isolated workspace
- Branch / Worktree
- Container / VM
- Prepared environment
- Build tools
- Browser
- Internal network
- Cache
- Snapshot
- Persistent vs Ephemeral worker

깊은 Container/Kubernetes 구현 튜토리얼로 확장하지 않는다.

---

## 7. Harness Engineering

Agent가 성공할 수 있는 실행 구조를 다룬다.

- Instructions
- Repository map
- Skills
- Tools
- MCP
- Shell
- Browser
- Search
- Result filtering
- Subagents
- Model routing 개념
- execution loop
- review / enforcement gate
- feedback injection

Harness를 Tool 묶음으로만 설명하지 않는다.

~~~text
Specification
→ Plan
→ Execute
→ Review
→ Feedback
↺
~~~

Review에는 Task에 따라 Functional, Architecture, Scope, Security Conformance가 포함될 수 있다.

핵심:

> Model을 바꾸는 것과 Harness를 개선하는 것을 구분한다.

> Skill / Tool과 Harness를 구분하고, Harness와 Factory 전체도 구분한다.

제품별 설정법보다 architecture pattern을 중심으로 한다.

---

## 8. Context Engineering / Agent Legibility

다룰 내용:

- Progressive Context
- Relevant Context
- Minimal Context
- Repository legibility
- Application legibility
- Software Catalog
- Architecture docs
- AGENTS.md / CLAUDE.md
- Tool output size
- Context freshness

핵심:

```text
More Context
≠ Better Agent
```

AGENTS.md를 거대한 지식 저장소로 쓰는 방법은 권하지 않는다.

---

## 9. Tool / Skill / Hook / MCP 구분

책에서 역할을 분리해 설명한다.

```text
Guidance
→ Instruction

Reusable Procedure
→ Skill

External Capability
→ Tool / MCP

Mandatory Enforcement
→ Hook / Policy / Permission
```

MCP protocol 상세 구현은 핵심이 아니다.

Agent가 조직 system에 안전하게 접근하는 interface 관점에서만 다룬다.

---

## 10. Verification

가장 중요한 본문 영역 중 하나다.

다룰 계층:

### Static

- compile
- lint
- typecheck

### Deterministic

- unit
- integration
- contract
- migration test

### Runtime

- service boot
- API
- E2E

### Behavioral Evidence

- browser
- screenshot
- video
- logs
- metrics
- traces

### Independent Evaluation

- evaluator agent
- architecture conformance
- scope conformance
- security review
- human acceptance

핵심:

> Agent self-report와 완료 판정을 분리한다.

---

## 11. Evidence

Factory Result Contract를 다룬다.

후보:

- Commit SHA
- Changed files
- Exact commands
- Test results
- Benchmark
- Screenshot
- Video
- Log / Trace reference
- Known limitation
- Remaining risk

UI 작업에서는 Demos over Diffs를 사례로 사용한다.

코드 Review를 없애는 주장으로 확장하지 않는다.

---

## 12. Failure / Retry / Resume / Reassignment

Production Factory의 핵심으로 다룬다.

Failure class:

- Tool failure
- Agent drift
- Harness crash
- Worker loss
- Network
- Timeout
- Verification failure
- Policy denial
- Context loss

Recovery ladder:

```text
Tool Retry
→ Step Retry
→ Agent Nudge
→ Subtask Retry
→ Worker Restart
→ Reassignment
→ Human Escalation
```

반드시 포함:

- Retry Budget
- Carryover
- Checkpoint
- Uncommitted work
- Duplicate side effect
- Idempotency
- Different-worker continuation

깊은 workflow engine 구현은 Advanced Topic으로 둔다.

---

## 13. Durable Execution

개념은 핵심 본문에 포함한다.

다룰 내용:

- state persistence
- checkpoint
- event history
- resume
- async human wait
- idempotency
- replay-safe tool

Temporal, Durable Task, Agent Executor는 사례로 소개한다.

특정 workflow engine 사용법 책으로 확대하지 않는다.

---

## 14. Human Gate / Governance

다룰 권한 축:

- Work Selection Authority
- Planning Authority
- Execution Authority
- Verification Authority
- Acceptance Authority
- Merge Authority
- Deploy Authority

핵심:

> Execution Authority와 Acceptance Authority를 분리한다.

다룰 운영 방식:

- Risk-based Gate
- AWAITING_HUMAN
- escalation
- reviewer capacity
- approval evidence

---

## 15. Security / Isolation

핵심 본문으로 다룬다.

- Filesystem isolation
- Network isolation
- Scoped credential
- Branch protection
- Secret scanning
- Tool allow/deny
- Broker / Proxy
- Prompt injection boundary
- Untrusted external context
- Agent identity
- Audit

핵심:

> Agent를 완전히 신뢰하는 대신 덜 신뢰해도 안전한 환경을 만든다.

일반 AI Security 전체로 확장하지 않는다.

---

## 16. Agent Identity / Provenance

실제 조직 적용에 필요한 정도까지 다룬다.

- initiating principal
- Agent identity
- delegated authority
- Task scope
- credential expiry
- audit
- commit/artifact provenance
- approval lineage

IAM 표준 세부 구현은 Advanced Topic으로 제한한다.

---

## 17. Observability

다룰 대상:

- Task
- Attempt
- Worker
- Agent turns
- Tool calls
- Verification
- Human interaction
- Cost
- Failure

핵심 dashboard 후보:

```text
Ready
Running
Blocked
Awaiting Human
Verifying
Done
Failed
```

Raw chain-of-thought 저장을 observability 요구사항으로 삼지 않는다.

Externally observable state/action을 기록한다.

---

## 18. Metrics / Economics

다음 지표를 비판적으로 다룬다.

### 낮은 수준

- Token
- Turn
- Agent execution time

### Factory 수준

- Cycle time
- Human blocking time
- Review time
- Intervention rate
- Retry
- Acceptance
- Revert
- Escaped defect
- Cost per accepted change

핵심:

> Agent Run이 아니라 Accepted Change에 가까운 단위를 최적화한다.

정확한 단일 productivity %를 제시하는 책으로 만들지 않는다.

---

## 19. Review / Integration / CI Bottleneck

Agent가 빨라졌을 때 병목이 이동하는 문제를 다룬다.

- Review Queue
- CI Capacity
- Verification Queue
- Merge Conflict
- Giant PR
- Stacked PR
- WIP Limit
- Integration test
- Fan-in

핵심:

> Worker를 늘리는 것이 Factory throughput 증가와 같지 않다.

---

## 20. Multi-Agent

중요하지만 최소 정의는 아니다.

다룰 내용:

- parallel independent Task
- parent/subagent
- planner/evaluator
- ownership
- dependency
- conflict
- correlated error
- resource stampede

핵심:

> 병렬화의 대상은 Agent가 아니라 독립 Task다.

Multi-Agent Framework 비교는 하지 않는다.

---

## 21. Event-driven Factory

다룰 Trigger:

- Issue
- CI Failure
- Review
- Vulnerability
- Scheduled maintenance
- Production signal

다만:

```text
Event
→ Agent Action
```

을 바로 연결하지 않는다.

```text
Signal
→ Diagnose
→ Scope
→ Risk
→ Task
→ Execute
```

형태를 기본으로 한다.

---

## 22. Closed-loop SDLC

장기적인 Factory model로 다룬다.

```text
Intent
→ Plan
→ Task
→ Execute
→ Verify
→ Deliver
→ Operate
→ Observe
→ Learn
↺
```

핵심:

- Production failure → Regression Test
- Review failure → Eval
- Repeated friction → Skill / Tool / Docs
- Incident → Backlog

자동 self-healing을 기본 전제로 두지 않는다.

---

## 23. Platform Engineering 연결

반드시 다룬다.

Platform이 제공:

- environment
- CI/CD
- secrets
- deployment
- observability
- software catalog
- golden path
- policy

Factory가 사용:

- Task execution
- verification
- delivery
- recovery

핵심:

> Platform은 생산 capability를 제공하고 Factory는 Work를 흐르게 한다.

---

## 24. Minimum Viable AI Software Factory

실전 도입의 중심 장으로 사용할 가능성이 높다.

최소 형태:

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

고도화 순서:

```text
Agent-ready Repository
→ Reproducible Worker
→ Evidence Contract
→ Durable Task State
→ Retry / Resume
→ Event Trigger
→ Parallel Workers
→ Risk-based Automation
→ Work Selection Automation
→ Self-improvement
```

핵심:

> Reliability → Observability → Recovery → Scale → Autonomy

---

## 25. Factory Maturity / Autonomy

책 자체 taxonomy로 사용할 수 있지만 업계 표준처럼 쓰지 않는다.

후보:

### M0 Interactive Agent
### M1 Repeatable Worker
### M2 Durable Factory
### M3 Parallel Factory
### M4 Event-driven Factory
### M5 Adaptive Factory

Autonomy는 별도 축으로 설명한다.

- Work selection
- Planning
- Execution
- Verification
- Acceptance
- Merge/Deploy

Maturity와 Autonomy를 같은 척도로 합치지 않는다.

---

# 실전 예제 범위

책에 실전 예제가 필요하다.

예제는 특정 vendor SDK 사용법이 아니라 **Factory principle을 확인하는 작은 reference implementation**을 목표로 한다.

예제에서 보여줄 최소 흐름:

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

추가 실험:

- Worker kill → Resume
- Verification failure → Retry
- Human approval
- Two independent tasks in parallel
- Same-file conflict
- Evidence output

특정 구현 언어와 프레임워크는 TOC/Chapter Plan 단계에서 확정한다.

Runmesh는 실제 경험과 case study로 사용할 수 있지만 책의 표준 구현이나 제품 홍보물이 되지 않도록 한다.

---

# Case Study 사용 범위

다음 유형을 사용할 수 있다.

## 산업 사례

- OpenAI
- Anthropic
- GitHub
- WorkOS
- Stripe
- StrongDM
- Factory.ai
- Cursor
- Jules
- Kiro
- OpenHands

## 연구 사례

- SWE-agent
- Agentless
- SWE-bench 계열
- AIware
- METR
- DORA
- NIST

## 자체 실험 사례

- durable task
- worker isolation
- retry
- approval
- continuity gap
- evidence
- scheduling

자체 실험은 일반 사실이 아니라 "실제 구현에서 관찰한 사례"로 명시한다.

---

# Advanced Topic으로 제한할 범위

다음은 중요하지만 핵심 흐름을 해치지 않도록 깊이를 제한한다.

## 1. Durable Workflow Engine 내부 구현

- event sourcing
- replay algorithm
- lease internals
- distributed consensus

개념과 설계 판단까지만.

## 2. Advanced Multi-Agent

- dynamic team formation
- debate
- swarm
- emergent organization
- market-based scheduling

기본 Factory 구현에는 필요하지 않다.

## 3. Model Routing

- quality/cost routing
- fallback
- cache impact

architecture pattern까지만.

## 4. Agent-to-Agent Protocol

- A2A
- ACP

상호운용성 개념까지만.

MCP는 Tool/Data integration 때문에 상대적으로 더 많이 다룰 수 있다.

## 5. Self-improvement

- Skill generation
- Eval-driven improvement
- Signals

가능성과 안전 경계까지만.

## 6. Formal Methods

- formal specification
- proof
- model checking

Factory의 미래 검증 방향 정도로 제한한다.

## 7. Enterprise IAM

- workload identity
- delegated authorization

핵심 원리까지만.

---

# 명시적으로 핵심 범위에서 제외할 내용

다음은 독립 장으로 만들지 않는다.

- Foundation Model 학습 원리
- Fine-tuning 튜토리얼
- RAG 일반론
- Vector Database 일반론
- Prompt Engineering 입문
- 일반 Chatbot 개발
- AI Agent Framework 종합 비교
- LangChain / CrewAI / AutoGen 사용법
- MCP Server 개발 입문
- Kubernetes 입문
- CI/CD 입문
- DevOps 입문
- Platform Engineering 입문서 전체
- General-purpose Agent OS
- Personal AI Assistant
- Browser-use 일반 자동화
- RPA
- Product Management 자동화
- 조직 전체를 AI Agent로 대체한다는 미래론
- AGI 전망
- 모델별 벤치마크 순위 나열
- 특정 제품 가격/플랜 비교

필요한 개념은 Software Factory 이해에 필요한 정도만 설명한다.

---

# 별도 후속 주제로 이동할 내용

`planning/future-topics.md`에 보존한다.

대표 주제:

- Autonomous Product Factory
- Self-modifying Factory
- Agent OS
- Agent Governance Platform
- Agent Security Platform
- Agent Observability Platform
- Cross-organization Agent Federation
- Advanced A2A orchestration
- Autonomous incident remediation
- Formal verification of agent-produced changes
- AI-native organization design
- Agent labor economics
- Long-term developer skill transformation

---

# 제품 의존성 관리

제품은 원칙을 설명하는 사례로 사용한다.

본문 작성 규칙:

### 본문

- architecture pattern
- failure pattern
- design principle

### Research

- exact model
- price
- version
- context size
- concurrency
- product limitation

제품명이 사라져도 chapter의 논리가 유지되어야 한다.

---

# 최신 정보 관리

빠르게 변하는 정보:

- Model
- Product name
- Pricing
- Session limit
- Protocol version
- Benchmark score

는 research 문서에서 기준일과 출처를 관리한다.

본문 핵심 주장에는 안정적인 principle을 우선한다.

---

# 역사 범위

Traditional Software Factory의 역사는 짧게만 다룬다.

목적:

> 왜 AI 시대에 다시 "Factory"라는 표현이 등장하는가?

설명에 필요한 배경까지만.

책의 상당 부분을:

- 1960s software crisis
- Japanese Software Factory
- CASE tools
- Software Product Lines

역사로 사용하지 않는다.

필요하면 Introduction의 짧은 section 또는 appendix 수준으로 제한한다.

---

# 독자에게 약속하지 않을 것

이 책은 다음을 약속하지 않는다.

- Fully autonomous development organization
- Zero-human software engineering
- 특정 Agent를 쓰면 N배 생산성
- 모든 Task의 자동화
- 특정 architecture가 유일한 정답
- benchmark score가 production capability를 보장
- human review가 곧 사라짐

---

# 책의 성공 기준

책을 읽은 독자가 자신의 조직에서 다음을 설계할 수 있어야 한다.

1. 어떤 Task를 Factory 대상으로 할지 분류
2. Ready Contract / Acceptance 정의
3. Durable Task state 설계
4. Control Plane 책임 결정
5. Worker / Sandbox 경계 설계
6. Context / Tool / Skill 구성
7. Deterministic rule과 Agent judgment 분리
8. Verification / Evidence Contract 설계
9. Retry / Resume / Reassignment policy 정의
10. Human Gate / Risk policy 정의
11. Security / Identity / Audit 경계 설정
12. Factory observability와 metric 정의
13. Parallelism이 실제 이득인지 판단
14. CI/CD와 Developer Platform을 재사용
15. Minimum Viable Factory부터 점진적으로 확장

최종적으로 독자는 다음을 설명할 수 있어야 한다.

> 우리 조직에서 AI Software Factory는 무엇을 자동화하고, 무엇을 자동화하지 않으며, Agent에게 어떤 실행권을 주고 어떤 검증과 책임 구조 안에서 운영할 것인가?

---

# TOC 설계 규칙

다음 단계 `planning/toc.md`에서는 이 Scope를 기준으로 한다.

목차는 다음 흐름을 우선한다.

```text
왜 필요한가
→ 무엇인가
→ Work를 어떻게 정의하는가
→ Agent가 어디서 일하는가
→ 어떻게 통제하는가
→ 어떻게 검증하는가
→ 실패하면 어떻게 하는가
→ 어떻게 확장하는가
→ 조직에서 어떻게 운영하는가
```

제품별 Chapter 구조는 피한다.

예:

```text
Part 1 OpenAI
Part 2 Anthropic
Part 3 GitHub
```

처럼 구성하지 않는다.

제품 사례는 각 원칙 안에 배치한다.
