# 2장. AI Software Factory란 무엇인가

1장에서 본 문제는 단순했다.

Coding Agent가 빨라져도 Software Delivery 전체가 같은 속도로 빨라지는 것은 아니다. 작업이 늘어나면 Review, CI, Integration, Human Attention 같은 다른 단계가 병목이 된다.

그렇다면 어디까지 갖춰야 Software Factory라고 부를 수 있을까.

Software Factory는 Agent를 여러 개 띄우는 시스템과 같은 말이 아니다. 완전 자율 Merge가 가능한 시스템만 Factory인 것도 아니다. CI/CD에 LLM 호출을 하나 추가했다고 자동으로 Factory가 되는 것도 아니다.

이 책에서는 다음과 같이 정의한다.

> **AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.**

정의에서 중요한 것은 Agent 수가 아니다.

**Durable Work, 실행 위임, 독립된 검증, 실패 복구, 지속적인 전달**이다.

Agent는 중요한 Worker지만 Factory 전체는 아니다.

---

## 2.1 왜 다시 Factory라는 표현인가

Software Factory라는 말은 AI 시대에 처음 등장한 것이 아니다. Software Engineering은 오래전부터 반복 가능한 프로세스, 자동화, 표준화, 재사용 가능한 자산을 통해 생산성을 높이려 해왔다.

이 책은 그 역사를 길게 다루지 않는다.

여기서 Factory라는 표현이 유용한 이유는 하나다.

> 작업을 개인의 순간적인 수행이 아니라 반복 가능한 시스템의 흐름으로 본다.

Interactive Agent를 개인 도구로 사용할 때는 작업 상태가 개발자의 머릿속과 Session 안에 있어도 된다.

```text
Developer
→ Prompt
→ Agent Session
→ Result
```

하지만 Task가 길어지고 Worker가 여러 개가 되고 재시도와 Human Wait가 생기면 다음 상태를 누군가는 알아야 한다.

- Task의 목표와 완료 기준
- 어떤 Revision에서 시작했는가
- 어떤 Attempt가 실패했는가
- 누가 작업 중인가
- 어떤 검증이 통과했는가
- 무엇이 아직 남았는가
- 누가 승인해야 하는가

이 상태를 한 Agent Session에만 둘 수는 없다.

이때부터 개발은 Session의 연속이 아니라 **Work가 시스템을 통과하는 흐름**에 가까워진다.

AI 시대에 Factory라는 표현이 다시 유용해지는 이유도 여기에 있다.

---

## 2.2 최소 정의를 검증해 보기

정의에 일부러 넣지 않은 것이 있다.

- Agent 수
- 특정 Model
- 특정 Agent Framework
- Fully Autonomous Merge
- Automatic Backlog Selection
- Self-improvement

이 기능들은 강력할 수 있지만 Factory의 필수조건은 아니다.

예를 들어 다음과 같은 구조를 생각해보자.

```text
Human selects Task
      ↓
Durable Task Record
      ↓
One Isolated Worker
      ↓
Coding Agent
      ↓
Deterministic Verification
      ↓
Evidence
      ↓
Human Review
```

Agent는 하나뿐이고 Task도 사람이 선택하며 Merge도 사람이 승인한다.

그래도 Interactive Agent와 중요한 차이가 있다.

작업 상태가 Session 밖에 남고, 실행환경이 분리되며, 결과가 검증되고, Worker가 실패해도 같은 Task를 재시도하거나 재배정할 수 있다.

반대로 Agent를 20개 띄워도 모든 Session 상태를 사람이 직접 기억하고, 완료 판단을 Agent의 “완료했습니다”라는 응답에 의존한다면 생산 시스템은 약하다.

> Factory의 핵심은 Agent의 개수가 아니라 Work가 시스템 안에서 어떻게 관리되는가에 있다.

---

## 2.3 일곱 개 핵심 설계 속성

이 책에서는 이후 장에서 반복해서 사용할 설계 속성을 일곱 가지로 정리한다.

모두 첫 구현부터 완비해야 한다는 뜻은 아니다. 22장의 Minimum Viable Factory에서는 이 가운데 필요한 일부만으로 시작한다.

### 1. Durable Work

기본 단위는 Prompt보다 오래 살아남는 Task다.

```text
Prompt
= interaction

Task
= durable work item
```

Task에는 Goal, Scope, Acceptance, Status, Attempt, Worker, Verification, Evidence 같은 정보가 연결될 수 있다.

핵심 원칙은 단순하다.

> Worker는 잃을 수 있어도 Task는 잃지 않는다.

자세한 상태 모델은 5장에서 다룬다.

### 2. Delegated Execution

Agent는 답변만 만드는 것이 아니라 실제 실행환경에서 일한다.

Repository를 읽고 수정하며 Build, Test, Browser, Git, 외부 Tool을 사용한다.

따라서 Agent에게는 Model뿐 아니라 Worker와 실행환경이 필요하다. 이 경계는 7~9장에서 다룬다.

### 3. Controlled Autonomy

모든 결정을 Agent에게 맡기지 않는다.

Task 상태, Retry Budget, Permission, 필수 검증처럼 이미 규칙이 있는 것은 시스템이 관리하고, Repository 탐색, 원인 진단, 구현 전략처럼 사전 규칙화하기 어려운 판단은 Agent에 맡길 수 있다.

```text
Known Rule
→ System

Uncertain Search / Judgment
→ Agent
```

11장에서 이 경계를 자세히 다룬다.

### 4. Independent Verification

Agent가 완료했다고 말하는 것과 Task가 실제로 완료된 것은 다르다.

```text
Agent Result
→ Verification
→ Evidence
→ Acceptance
```

Compile, Test, Runtime Check, Screenshot, Security Scan, Evaluator, Human Review 등 Task 위험에 맞는 검증이 필요하다.

핵심은 Agent의 자기 보고와 완료 판정을 분리하는 것이다.

### 5. Recoverability

Agent, Tool, Worker, Network는 실패할 수 있다.

따라서 Task는 Retry, Restart, Resume, Reassignment, Human Escalation 같은 복구 경로를 가질 수 있어야 한다.

Happy Path보다 실패 후 같은 Work를 일관되게 이어갈 수 있는지가 더 중요하다.

### 6. Acceptance / Governance

실행 권한과 최종 위험을 받아들이는 권한은 다르다.

```text
Work Selection
Planning
Execution
Verification
Acceptance
Merge / Deploy
```

Task 위험에 따라 Human, Agent, Policy가 서로 다른 권한을 가질 수 있다.

Factory는 Human Review를 없애는 시스템이 아니라 **Acceptance Authority를 명확히 하는 시스템**으로 보는 편이 낫다.

### 7. Feedback

Task 실행에서는 계속 새로운 정보가 나온다.

- missing test
- flaky environment
- 반복되는 review comment
- production defect
- 부족한 Tool
- 불명확한 Requirement

이 정보는 Product Fix나 Factory Improvement로 되돌아갈 수 있다.

Feedback이 자동이어야 한다는 뜻은 아니다. 중요한 것은 실행 결과가 다음 개선에 사용할 수 있는 상태로 남는다는 것이다.

---

## 2.4 Factory가 아닌 것

정의를 더 명확하게 하려면 무엇과 다른지 봐야 한다.

### Multi-Agent System

여러 Agent가 있다고 Factory가 되는 것은 아니다.

Multi-Agent는 Scheduling Pattern이나 구현 전략일 수 있다. Minimum Viable Factory는 Agent 하나로도 성립할 수 있다.

```text
More Agents
≠ More Factory
```

### Agent Framework

Agent Framework는 Model Loop, Tool, Memory, Subagent 같은 실행 기반을 제공할 수 있다.

Factory는 그보다 넓은 Software Delivery 상태를 다룬다.

```text
Requirement
Task
Repository
Commit
Build
Test
Approval
Release
Deployment
```

### Coding Agent Farm

여러 Agent Session을 사람이 각각 관리하면 Human Attention이 사실상 Control Plane 역할을 한다.

중앙 Task State, 검증 규칙, Retry Policy, Evidence가 없다면 Agent 수가 늘수록 관리 부담도 커질 수 있다.

### CI/CD + LLM

CI/CD는 Factory의 중요한 기반이다.

```text
Source Change
→ Build
→ Test
→ Release
→ Deploy
```

Factory는 여기에 Requirement/Task, Agent Work, Retry/Approval, Feedback까지 연결할 수 있다. 기존 CI/CD를 대체하기보다 사용한다.

### Fully Autonomous Organization

Software Factory는 사람이 없는 개발 조직을 뜻하지 않는다.

Task 선택, Architecture, Acceptance, Merge, Deploy 권한을 사람이 유지해도 Factory는 성립한다.

완전 자율화는 필수조건이 아니라 운영 정책의 한 선택지다.

---

## 2.5 하나의 Loop로 본다

지금까지의 요소를 연결하면 책 전체의 Reference Loop가 된다.

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

처음부터 모든 요소를 구현할 필요는 없다.

작은 팀은 다음 정도로 시작할 수 있다.

```text
Human selects Task
→ Task Record
→ One Worker
→ Coding Agent
→ Build / Test
→ Evidence
→ Human Review
```

중요한 것은 기능 목록보다 순서다.

Reliability와 Verification을 확인하기 전에 Agent 수나 Decision Authority부터 크게 늘리면 실패 원인을 구분하기 어려워진다.

이후 장에서는 이 Loop를 Work 정의, 실행 구조, 검증과 복구, 전체 Flow 운영 순서로 분해한다.

---

Software Factory는 기존 Software Engineering을 버리고 새 시스템으로 교체하는 개념이 아니다.

이미 조직에는 Git, Issue Tracker, CI/CD, Test, Deployment, Monitoring, Developer Platform 같은 자산이 있다.

그렇다면 다음 질문이 생긴다.

> AI Software Factory는 기존 CI/CD, DevOps, Platform Engineering, Agent Platform과 어디에서 겹치고 어디에서 달라지는가?

먼저 기존 Delivery System과의 경계를 정리한다.

---

## 참고 자료

- OpenAI, *An open-source spec for Codex orchestration: Symphony*  
  https://openai.com/index/open-source-codex-orchestration-symphony/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands*  
  https://www.anthropic.com/engineering/managed-agents
- NIST NCCoE, *Notional Reference Model for DevSecOps*  
  https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
- DORA, *Platform Engineering Capability*  
  https://dora.dev/capabilities/platform-engineering/
