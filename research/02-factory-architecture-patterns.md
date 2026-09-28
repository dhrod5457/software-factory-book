# AI Software Factory Architecture Patterns

기준일: 2026-09-28

이 문서는 특정 제품 구조를 복제하기 위한 문서가 아니다.

OpenAI, Anthropic, WorkOS, Factory.ai, Cursor, GitHub, OpenHands에서 반복해서 나타나는 구조를 비교해 **AI Software Factory의 공통 아키텍처 패턴**을 추출한다.

## 1. 가장 중요한 변화: Agent보다 System

AI coding assistant의 기본 단위는 대화나 session이다.

AI Software Factory에서는 기본 단위가 달라진다.

```text
Interactive Agent
Human
→ Prompt
→ Session
→ Result

Software Factory
Intent
→ Durable Task
→ Orchestrator
→ Worker Runtime
→ Agent
→ Verification
→ Evidence
→ Gate
→ Next State
```

OpenAI Symphony는 이 변화를 명시적으로 보여준다.

- coding session이나 PR 자체가 목적이 아니라 deliverable이 목적
- issue tracker를 control plane으로 사용
- active issue마다 dedicated workspace/agent를 연결
- human이 여러 agent session을 직접 micromanage하지 않도록 supervisor가 관리

출처:

- OpenAI, An open-source spec for Codex orchestration: Symphony
  - https://openai.com/index/open-source-codex-orchestration-symphony/

## 2. Control Plane과 Execution Plane 분리

여러 사례에서 가장 강하게 반복되는 패턴이다.

### Control Plane

책임:

- Task 상태
- dependency
- owner / worker
- retry
- approval
- event
- artifact reference
- policy
- scheduling
- recovery

### Execution Plane

책임:

- checkout
- file edit
- command execution
- build
- test
- browser
- temporary services

WorkOS Horizon은 이를 거의 직접적으로 설명한다.

```text
Orchestrator
= durable control plane

Sandbox
= disposable execution primitive
```

이 분리가 필요한 이유:

- sandbox는 실패하거나 폐기될 수 있다.
- Task 상태는 sandbox와 함께 사라지면 안 된다.
- 재시작/재배정 시 다른 worker가 같은 Task를 이어갈 수 있어야 한다.
- worker credential과 orchestrator credential의 권한을 분리할 수 있다.

출처:

- WorkOS, The self-driving codebase: Building Horizon at WorkOS
  - https://workos.com/blog/project-horizon

## 3. Session / Harness / Sandbox 분리

Anthropic Managed Agents는 세 요소를 명시적으로 분리한다.

```text
Session
= durable append-only event/log state

Harness
= model loop + context + tool routing

Sandbox
= computation + filesystem + command execution
```

이 구조에서:

- sandbox가 죽어도 session은 남는다.
- harness가 죽어도 durable session에서 복구할 수 있다.
- 필요할 때만 sandbox를 provision할 수 있다.
- 하나의 brain이 여러 execution environment를 다룰 수 있다.
- 특정 sandbox 구현에 harness가 종속되지 않는다.

Anthropic은 이를 "brain"과 "hands"의 분리로 설명한다.

Factory 설계 관점에서 중요한 점은 VM/container 자체보다 **durable state가 어디에 존재하는가**다.

출처:

- Anthropic, Scaling Managed Agents: Decoupling the brain from the hands
  - https://www.anthropic.com/engineering/managed-agents

## 4. OpenAI도 Harness와 Compute를 분리

OpenAI Agents API / Agents SDK도 같은 방향으로 정리되고 있다.

Agents API:

- managed session
- orchestration
- context compaction
- recovery
- subagents
- sandbox 선택

Sandbox:

- hosted
- self-hosted
- partner provider
- no sandbox

Agents SDK의 설명에서도 agent state를 execution container 밖으로 이동하면 다음이 가능하다고 설명한다.

- container failure 이후 rehydration
- 여러 sandbox 사용
- subagent별 isolation
- 필요할 때만 sandbox 사용

출처:

- https://openai.com/index/introducing-the-agents-api/
- https://openai.com/index/the-next-evolution-of-the-agents-sdk/
- https://developers.openai.com/api/docs/guides/agents-api/overview
- https://developers.openai.com/api/docs/guides/agents/sandboxes

## 5. Issue Tracker / Task Tracker가 Control Plane이 되는 패턴

OpenAI Symphony:

```text
Linear Issue
→ Agent Workspace
→ Work
→ Review State
```

WorkOS Horizon:

```text
Linear
→ Webhook
→ Orchestrator
→ Sandbox
→ PR
→ Merge Event
→ Dependency Re-evaluation
```

이 패턴의 의미:

Issue tracker가 단순 사람이 보는 backlog가 아니라 agent 실행의 durable input source가 된다.

Task에 필요한 최소 상태 후보:

- Task ID
- Goal
- Acceptance criteria
- Dependency
- Priority
- Status
- Assigned worker
- Attempt
- Workspace
- Base revision
- Result revision
- Verification
- Artifact
- Approval
- Failure / retry reason

## 6. Worker는 IDE가 아니라 Runtime이 된다

Cursor Cloud Agents:

- agent마다 isolated VM
- repository
- dependencies
- secrets
- network access
- terminal
- browser
- full desktop
- 병렬 실행

Google Jules:

- repository를 secure cloud VM에 clone
- asynchronous task execution
- diff/plan/result 반환

OpenHands:

- local
- Docker
- VM
- cloud backend
- ephemeral workspace
- automation server

이 사례들은 worker runtime을 단순 "원격 IDE"보다 **독립 실행 가능한 disposable/persistent compute unit**로 보는 근거가 된다.

출처:

- https://cursor.com/docs/cloud-agent
- https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/
- https://github.com/OpenHands/OpenHands
- https://github.com/OpenHands/software-agent-sdk

## 7. Persistent Worker와 Disposable Worker는 둘 다 존재

두 종류의 운영 모델이 있다.

### Disposable Worker

장점:

- clean state
- isolation
- reproducibility
- 낮은 cross-task contamination

적합:

- CI-like task
- security-sensitive task
- 독립 feature
- deterministic validation

### Persistent Worker

Factory.ai Droid Computers 사례:

- installed packages 유지
- cloned repository 유지
- credentials 유지
- running services
- checkpoint / restore
- resume

장점:

- cold start 감소
- 장시간 프로젝트 continuity
- 복잡한 environment 재설치 비용 감소

위험:

- state contamination
- stale dependency
- credential accumulation
- reproducing failures harder

Factory 설계에서 중요한 것은 하나를 정답으로 고르는 것이 아니라 **Task별로 clean state와 warm state를 선택하는 것**이다.

출처:

- https://factory.ai/news/factory-desktop

## 8. Multi-Agent는 Architecture가 아니라 Scheduling Pattern

GitHub Fleet:

- parent agent가 복잡한 작업을 independent subtasks로 분해
- subagents 병렬 실행
- dependency가 적을수록 효과적
- parent가 결과 reconcile/verify

Anthropic C compiler:

- 16 agents
- shared codebase
- tests 중심 convergence
- 약 2,000 Claude Code sessions

OpenAI Agents API:

- subagent가 독립 context를 가짐
- root agent가 결과를 조정

공통점:

> Agent 수가 많다는 사실보다 어떤 Task가 독립적으로 실행 가능한지가 중요하다.

출처:

- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet
- https://www.anthropic.com/engineering/building-c-compiler
- https://openai.com/index/introducing-the-agents-api/

## 9. 이벤트 기반 실행

Software Factory가 24/7 동작하려면 사람이 매번 prompt를 입력할 필요가 없다.

Trigger 후보:

- Issue created
- Issue status changed
- PR opened
- Review comment
- CI failure
- Production alert
- dependency update
- scheduled maintenance
- docs drift
- security scan
- customer signal

Google Jules는 2025년 말 Suggested Tasks / Scheduled Tasks / self-healing deployment 방향을 공개했다.

Factory.ai는 schedule/trigger 기반 automation을 Software Factory의 기본 구성으로 제공한다.

OpenHands는 automation repository에서:

- schedule
- webhook
- run history
- dispatch
- sandbox lifecycle

을 분리한다.

출처:

- https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/
- https://factory.ai/product/software-factory
- https://github.com/OpenHands/OpenHands

## 10. Reference Architecture 후보

현재 자료를 기반으로 한 임시 모델:

```text
[Intent / Signals]
      ↓
[Work Intake]
      ↓
[Specification / Acceptance]
      ↓
[Task Graph]
      ↓
================ CONTROL PLANE ================
[Scheduler / Orchestrator]
  - durable task state
  - dependencies
  - attempts
  - approvals
  - policy
  - routing
  - recovery
      ↓
================ EXECUTION PLANE ===============
[Worker Provisioner]
      ↓
[Isolated / Persistent Workspace]
      ↓
[Agent Harness]
  - context
  - tools
  - skills
  - MCP
  - subagents
      ↓
[Hands]
  - filesystem
  - shell
  - browser
  - services
  - external systems
      ↓
================ VERIFICATION ==================
[Deterministic Checks]
[Runtime / Browser Checks]
[Evaluator Agent]
[Security / Policy]
      ↓
[Evidence / Artifacts]
      ↓
[Human or Automated Gate]
      ↓
[Merge / Deploy / Close]
      ↓
[Observability / Feedback]
      ↺
```

## 11. 연구 가설

### 가설 A

AI Software Factory의 핵심 시스템 경계는 Agent 자체가 아니라 **Task State + Orchestration + Execution Boundary**다.

### 가설 B

장기적으로 session은 implementation detail이 되고, Task가 사용자/조직이 보는 주된 단위가 될 가능성이 높다.

### 가설 C

Worker를 disposable하게 만들수록 durable state를 worker 밖으로 꺼내야 한다.

### 가설 D

Agent capability가 향상될수록 rigid workflow state machine보다 objective + policy + tools 방식이 유리할 수 있다.

OpenAI Symphony도 초기 rigid state-machine식 접근보다 agent에게 objective와 tools/context를 주는 쪽으로 이동했다고 설명한다.

### 가설 E

Factory 아키텍처의 품질은 "한 번 성공"보다 crash/retry/reassignment 뒤에도 같은 Task가 일관되게 완료되는지로 평가해야 한다.
