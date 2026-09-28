# Concept

기준일: 2026-09-28

## 현재 작업 제목

**AI Software Factory**

최종 제목과 부제는 아직 확정하지 않는다.

이 문서는 research 단계에서 수집한 산업 사례, 학술 연구, 실패 사례, DevSecOps / Platform Engineering 자료를 바탕으로 책 전체의 중심 개념을 고정한다.

---

# 중심 주제

이 책의 중심 주제는 **AI Coding Agent를 개인 개발 보조도구가 아니라 반복 가능한 소프트웨어 생산 시스템 안의 실행 주체로 배치하는 방법**이다.

이 책은 특정 Coding Agent 제품 사용 설명서가 아니다.

또한 "개발자를 AI로 대체하는 방법"을 주장하는 책도 아니다.

핵심 질문은 다음과 같다.

> AI Agent에게 소프트웨어 작업을 위임하면서도, 작업 상태와 권한과 검증을 통제하고 실패를 복구하며 검증된 변경을 지속적으로 전달하려면 어떤 생산 시스템이 필요한가?

독자가 마지막에 답할 수 있어야 하는 질문:

> 이 작업을 Agent에게 어떻게 위임하고, 어디까지 자율적으로 실행하게 하며, 무엇으로 완료를 검증하고, 언제 사람이 개입해야 하는가?

---

# 핵심 정의

책에서 사용할 기본 정의:

> **AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.**

이를 구조로 표현하면 다음과 같다.

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
Isolated Worker / Runtime
      ↓
AI Agent + Context + Tools
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

핵심은 Agent 수가 아니다.

```text
AI Software Factory
≠ Multi-Agent System

AI Software Factory
≠ Coding Agent Farm

AI Software Factory
≠ CI/CD with an LLM
```

Agent는 Factory의 중요한 Worker지만 Factory 전체는 아니다.

---

# 최소 구성요소

Research 단계에서 산업 자료와 학술 연구 양쪽에서 반복적으로 확인된 최소 요소는 다음 일곱 가지다.

## 1. Durable Work

Task는 한 번의 Prompt나 Agent Session보다 오래 살아야 한다.

Task에 연결될 수 있는 상태:

- Goal
- Scope
- Acceptance Criteria
- Dependency
- Status
- Attempt
- Worker
- Revision
- Verification
- Artifact
- Approval
- Failure / Recovery

핵심 원칙:

> Agent Session은 사라질 수 있지만 Task State는 사라져서는 안 된다.

---

## 2. Delegated Execution

Agent는 단순 답변 생성기가 아니라 실제 실행환경에서 작업한다.

예:

- Repository checkout
- File edit
- Shell
- Build
- Test
- Browser
- Service execution
- Git
- External tools

따라서 Worker Runtime과 실행환경은 Factory의 일부다.

---

## 3. Controlled Autonomy

모든 판단을 Agent에게 맡기지 않는다.

책에서는 다음 경계를 유지한다.

### System이 맡기 좋은 것

- Task state
- Dependency
- Retry count
- Timeout
- Permission
- Budget
- Required verification
- Approval state
- Deployment order

### Agent가 맡기 좋은 것

- Repository exploration
- Diagnosis
- Hypothesis
- Implementation strategy
- Safe tool selection
- Open-ended problem solving

핵심 원칙:

> 이미 알고 있는 규칙은 시스템이 강제하고, 불확실한 판단과 탐색에 Agent autonomy를 사용한다.

---

## 4. Independent Verification

Agent가 "완료했다"고 말하는 것은 완료 조건이 아니다.

```text
Agent proposes
      ↓
Verifier checks
      ↓
Evidence produced
      ↓
Policy / Human accepts
```

Verification 후보:

- compile
- lint
- unit test
- integration test
- E2E
- browser/runtime validation
- screenshot/video
- security scan
- performance check
- evaluator agent
- human acceptance

핵심 원칙:

> Completion Claim과 Completion Authority를 분리한다.

---

## 5. Recoverability

Production Agent는 실패한다는 전제로 설계한다.

실패 후보:

- model turn failure
- tool failure
- harness crash
- worker loss
- network failure
- timeout
- verification failure
- policy denial
- context loss
- implementation drift

Recovery 후보:

```text
Tool Retry
→ Step Retry
→ Agent Nudge
→ Subtask Retry
→ Worker Restart
→ Reassignment
→ Human Escalation
```

핵심 원칙:

> AI Software Factory의 신뢰성은 한 번에 성공하는 능력보다 실패 후에도 Task를 보존하고 이어가는 능력에서 나온다.

---

## 6. Acceptance and Governance

Execution Authority와 Acceptance Authority를 같은 것으로 보지 않는다.

Agent가 다음을 수행할 수 있어도:

- code 작성
- test 실행
- PR 생성

다음 권한은 별도로 설계할 수 있다.

- requirement approval
- risky action approval
- merge
- deploy
- production mutation

Task risk에 따라 Human / Policy / Automated Gate를 다르게 둔다.

핵심 원칙:

> Autonomy는 하나의 숫자가 아니라 권한별로 분리해서 설계한다.

---

## 7. Feedback

Factory의 결과는 한 Task에서 끝나지 않는다.

피드백 후보:

- failed verification
- rejected PR
- review comment
- production defect
- incident
- flaky test
- slow environment
- missing tool
- unclear documentation

피드백은 다음으로 돌아갈 수 있다.

- Product Task
- Regression Test
- Skill
- Tool
- Documentation
- Environment
- Policy
- Eval

핵심 원칙:

> Factory는 작업을 수행할 뿐 아니라 작업에서 발견한 실패를 다음 작업과 생산 시스템 개선에 반영해야 한다.

Feedback이 반드시 완전 자동일 필요는 없다.

---

# Factory Capability와 Model Capability를 분리한다

책 전체에서 다음 구분을 유지한다.

```text
Model Capability
≠ Agent Capability
≠ Factory Capability
```

Model 외 Factory 성능 변수:

- Requirement quality
- Task size
- Context quality
- Tool design
- Repository legibility
- Worker environment
- Orchestration
- Verification
- Recovery
- Security
- Human decision
- Platform quality

따라서 모델 benchmark 하나로 Factory의 능력을 판단하지 않는다.

---

# Requirement와 Task가 Prompt보다 중요해진다

Interactive Agent의 기본 단위:

```text
Prompt
→ Response / Session
```

Factory의 기본 단위:

```text
Durable Task
→ State
→ Attempts
→ Evidence
→ Acceptance
```

큰 작업에서는 다음 artifact가 중요하다.

```text
Intent
→ Requirement
→ Acceptance
→ Design
→ Task
→ Verification
```

다만 Requirement 생성 자체를 Agent가 해야 한다는 뜻은 아니다.

Authoritative Product Intent와 Acceptance Authority는 조직이 정한다.

---

# Requirement Layer를 책의 범위에 포함하는 이유

AI Software Factory를 단순 Issue-to-PR 자동화로 제한하지 않는다.

잘못된 Requirement를 완벽하게 자동 구현하는 것은 생산성이 아니다.

따라서 책은 다음을 다룬다.

- Requirement ambiguity
- Specification
- Acceptance Criteria
- Task decomposition
- Ready Contract
- Traceability

하지만 Product Strategy 자체의 자동화를 핵심 범위로 확대하지 않는다.

---

# CI/CD와의 관계

CI/CD는 Factory의 핵심 subsystem이다.

```text
Code Change
→ Build
→ Test
→ Package
→ Release
→ Deploy
```

AI Software Factory는 이보다 앞뒤가 넓다.

```text
Intent
→ Task
→ Agent Work
→ CI/CD
→ Delivery
→ Feedback
```

핵심 구분:

> CI/CD는 정의된 변경을 검증하고 전달한다. Factory는 작업을 관리하고 Agent에게 실행을 위임하며 실패를 수정하고 검증된 변경으로 수렴시킨다.

---

# DevOps / DevSecOps와의 관계

AI Software Factory는 DevOps를 대체하지 않는다.

기존 DevOps 원칙:

- small batch
- automation
- continuous feedback
- observability
- shared ownership
- secure delivery

은 Agent 시대에도 그대로 중요하다.

책에서는 AI Software Factory를 **DevSecOps lifecycle 안에 AI Agent가 first-class worker로 들어가는 진화**로 본다.

---

# Platform Engineering과의 관계

Platform Engineering:

> 조직에 안전하고 표준화된 생산 capability와 Golden Path를 제공한다.

Software Factory:

> 그 capability를 이용해 실제 Work Item을 검증된 software change로 변환한다.

```text
Developer Platform
provides
- environment
- CI/CD
- secrets
- deployment
- observability
- policy
- catalog

Software Factory
uses them for
- Task
- execution
- verification
- recovery
- delivery
```

Platform과 Factory는 경쟁 개념이 아니다.

좋은 Internal Developer Platform은 좋은 AI Software Factory의 기반이 된다.

---

# Agent Platform과의 관계

Agent Platform은 coding에 국한되지 않는 범용 infrastructure다.

예:

- Runtime
- Identity
- Gateway
- Tools
- Memory
- Observability

AI Software Factory는 Software Delivery domain에 특화된다.

추가 domain object:

- Requirement
- Repository
- Branch
- Commit
- Build
- Test
- PR
- Artifact
- Release
- Deployment
- Acceptance

핵심 구분:

> Agent Platform은 Agent를 실행한다. Software Factory는 Software Work를 완료한다.

---

# Harness Engineering의 위치

Harness는 Agent가 일을 할 수 있게 만드는 실행 구조다.

포함 후보:

- Instructions
- Skills
- Context
- Tools
- MCP
- Shell
- Browser
- Sandbox
- Result filtering
- Subagents

책에서는 Harness를 Factory의 Worker/Execution Layer를 구성하는 핵심 요소로 다룬다.

하지만 Harness 자체를 Factory 전체와 동일시하지 않는다.

---

# Context 원칙

책에서는 "Context를 많이 넣는다"를 좋은 전략으로 보지 않는다.

연구 근거에 따라 다음을 기본 원칙으로 둔다.

> Progressive, Relevant, Minimal Context.

Agent가 필요한 것을 찾아갈 수 있도록 한다.

```text
Small Entry Context
→ Repository Map
→ Relevant Docs
→ Skill
→ Tool / MCP
→ Runtime Evidence
```

반드시 지켜야 하는 규칙은 Context에만 두지 않는다.

```text
Guidance
→ Instructions

Reusable Procedure
→ Skill

External Capability
→ Tool / MCP

Mandatory Rule
→ Hook / Policy / Permission
```

---

# Multi-Agent의 위치

Multi-Agent는 Factory의 필수조건이 아니다.

먼저:

- strong single worker
- durable state
- verification
- recovery

를 갖춘다.

Multi-Agent가 유리한 경우:

- independent modules
- independent research
- independent verification
- low file overlap

불리한 경우:

- shared schema
- same core file
- strict sequential dependency
- high coordination

핵심 원칙:

> 병렬화의 대상은 Agent가 아니라 독립 Task다.

---

# Human의 역할

이 책은 "사람이 사라지는 Factory"를 기본 전제로 하지 않는다.

사람의 역할은 점차 다음 쪽으로 이동할 수 있다.

기존 비중:

- 직접 구현
- 명령 실행
- 반복 테스트

증가할 비중:

- Intent
- Architecture
- Specification
- Acceptance
- Risk decision
- Policy
- Exception handling
- Factory improvement

핵심 원칙:

> Agent에게 실행을 위임해도 의미와 위험의 최종 책임까지 자동으로 위임되는 것은 아니다.

---

# Human Attention을 생산 자원으로 본다

Factory의 목적은 Agent 수를 늘리는 것이 아니다.

개발자의 scarce resource는 시간뿐 아니라 attention이다.

측정 후보:

```text
Human Attention
----------------
Accepted Change
```

따라서 Agent session을 여러 개 띄워 사람이 직접 관리하게 만드는 구조는 장기적으로 확장되지 않을 수 있다.

Orchestrator는 compute뿐 아니라 human attention도 관리한다.

---

# Factory의 최적화 단위

다음 지표를 단독 목표로 삼지 않는다.

- Agent count
- Token
- Lines of Code
- PR count
- Benchmark score

더 중요한 후보:

- Accepted Change
- Cycle Time
- Human Intervention
- Review Time
- Verification Pass
- Retry
- Revert / Escaped Defect
- Cost per Accepted Change

책의 기본 관점:

> AI Software Factory는 코드 생성량이 아니라 검증된 소프트웨어 변경이 사용자에게 도달하는 전체 흐름을 최적화한다.

---

# Minimum Viable AI Software Factory

처음부터 Multi-Agent autonomous organization을 만들 필요가 없다.

최소 형태:

```text
Human selects Task
        ↓
Durable Task Record
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

이 구조에도 이미 Factory의 핵심 성질이 있다.

- repeatable work
- durable state
- delegated execution
- isolation
- verification
- evidence
- acceptance

고도화 순서 후보:

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

핵심 원칙:

> Reliability → Observability → Recovery → Scale → Autonomy

---

# Self-improvement의 위치

Self-improvement는 강력하지만 최소 정의에는 포함하지 않는다.

Factory가 개선할 수 있는 것:

- Docs
- Skills
- Tools
- Test
- Sandbox image
- Routing
- Task template
- Policy

그러나 Factory가 자기:

- evaluator
- security policy
- acceptance threshold

까지 자유롭게 수정하게 두면 reward hacking과 policy erosion 위험이 있다.

따라서 Factory meta-change는:

- version
- eval
- shadow
- canary
- approval
- rollback

대상으로 다룬다.

---

# Security의 기본 관점

Agent를 완전히 신뢰할 수 있게 만드는 것을 목표로 하지 않는다.

대신:

> Agent를 덜 신뢰해도 안전하게 운영 가능한 경계를 만든다.

기본 수단:

- sandbox
- filesystem isolation
- network policy
- scoped credential
- branch protection
- secret scanning
- deterministic hook
- approval
- audit

Prompt-only security를 사용하지 않는다.

---

# Failure를 정상 상태로 본다

Factory architecture의 상당 부분은 Agent가 성공할 때보다 실패할 때 필요하다.

실패는 다음 상태로 표현될 수 있다.

- RETRYABLE
- BLOCKED
- AWAITING_HUMAN
- REASSIGN
- FAILED
- DONE

핵심:

> Human escalation은 Factory 실패가 아니라 정상적인 state transition이다.

---

# Closed-loop의 위치

책의 장기적인 Factory 모델은 다음과 같다.

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

하지만 최소 Factory에서 Production Signal이 자동으로 새 Task를 만들 필요는 없다.

자동 Work Selection은 고급 autonomy로 분리한다.

---

# 이 책의 핵심 원칙

책 전체에서 다음 원칙을 유지한다.

1. **Model Capability와 Factory Capability를 분리한다.**
2. **Prompt보다 Durable Task를 중심에 둔다.**
3. **Requirement와 Acceptance를 구현보다 먼저 명확히 한다.**
4. **정형화 가능한 규칙은 시스템이 강제한다.**
5. **불확실한 탐색과 판단에 Agent autonomy를 사용한다.**
6. **Agent self-report와 완료 판정을 분리한다.**
7. **Verification은 실행 루프 내부에 둔다.**
8. **Context Window를 durable state로 사용하지 않는다.**
9. **Worker는 잃을 수 있어도 Task는 잃지 않는다.**
10. **병렬화의 대상은 Agent가 아니라 독립 Task다.**
11. **Execution Authority와 Acceptance Authority를 분리한다.**
12. **Autonomy가 높을수록 Isolation과 Evidence를 강화한다.**
13. **Factory의 성능은 Accepted Change 기준으로 본다.**
14. **Agent뿐 아니라 Review / CI / Integration 병목도 관리한다.**
15. **Factory 자체의 변경도 Software처럼 versioning하고 검증한다.**

---

# 현재 책의 핵심 범위

## 반드시 다룬다

- AI Software Factory 정의
- Coding Agent → Worker
- Requirement / Specification / Acceptance
- Durable Task
- Orchestration
- Worker / Sandbox
- Harness / Context / Skills / MCP
- Verification / Evidence
- Retry / Resume / Reassignment
- Human Gate / Governance
- Security / Isolation / Agent Identity
- Observability
- Metrics / Economics
- Review / Integration bottleneck
- CI/CD / Platform Engineering 연결
- Multi-Agent가 유효한 조건과 한계
- Minimum Viable Factory
- Closed-loop feedback
- Factory maturity / autonomy

## 핵심이 아닌 고급 주제

- Fully autonomous product management
- Autonomous merge everywhere
- Self-modifying Factory
- Agent OS
- General-purpose enterprise Agent Platform
- Model training / fine-tuning
- Foundation model internals
- Agent memory architecture 일반론

필요하면 마지막 전망 또는 advanced topic에서 제한적으로 다룬다.

---

# 제품 사용 원칙

OpenAI, Anthropic, GitHub, WorkOS, Stripe, StrongDM, Factory.ai, Cursor, Jules, Kiro, OpenHands 등의 사례는 원칙을 설명하는 concrete example로 사용한다.

제품 자체가 책의 architecture가 되지 않는다.

다음은 research 문서에 기준일과 함께 남긴다.

- 제품 기능
- 가격
- model
- concurrency
- session limit

본문은 제품이 바뀌어도 남는 원칙을 중심으로 쓴다.

---

# 연구 결과를 사용하는 규칙

산업 자료:

- 실제 운영 pattern 근거

학술 자료:

- 일반화 가능한 주장 검증
- 반례
- evaluation

Vendor 내부 생산성 수치:

- 해당 회사 사례로만 표현

Preprint:

- publication 상태와 방법론 한계를 명시

Benchmark:

- 실제 조직 생산성과 동일시하지 않음

---

# 독자가 최종적으로 할 수 있어야 하는 것

독자는 자신의 조직/프로젝트에서 다음을 판단할 수 있어야 한다.

- AI Software Factory가 필요한가
- Coding Agent만으로 충분한가
- 어떤 Task부터 Factory에 넣을 것인가
- Task를 어떻게 durable하게 관리할 것인가
- 어디까지 deterministic workflow로 둘 것인가
- 어디에 Agent judgment를 사용할 것인가
- 어떤 Worker / Sandbox가 필요한가
- 어떤 Context / Skill / Tool이 필요한가
- 완료를 어떤 Evidence로 판단할 것인가
- Agent 실패를 어떻게 retry/resume/reassign할 것인가
- 어떤 작업에 Human Gate가 필요한가
- Multi-Agent를 언제 사용해야 하는가
- 어떤 지표로 Factory를 평가할 것인가
- 기존 CI/CD와 Platform Engineering을 어떻게 활용할 것인가
- Autonomy를 어떤 순서로 높일 것인가

최종적으로 독자가 다음 질문에 답할 수 있어야 한다.

> 이 작업을 Agent에게 맡길 수 있는가?

그리고 더 중요한 다음 질문까지 답할 수 있어야 한다.

> 맡길 수 있다면, 어떤 상태·권한·검증·복구 구조 안에서 맡겨야 하는가?

---

# Concept 이후 단계

다음 단계는 `planning/scope.md`다.

Scope에서는 이 Concept을 기준으로:

- 핵심 본문
- Advanced Topic
- 후속 주제
- 의도적으로 제외할 주제

를 명확히 분리한다.

그 후 `planning/toc.md`에서 Part / Chapter 구조를 설계한다.
