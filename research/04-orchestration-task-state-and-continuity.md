# Orchestration, Task State, and Continuity

기준일: 2026-09-28

AI Software Factory에서 가장 쉽게 과소평가되는 문제는 code generation이 아니라 **작업의 지속성**이다.

한 agent session이 성공하는 것과 Factory가 Task를 끝까지 책임지는 것은 다르다.

## 1. Prompt와 Task를 분리한다

```text
Prompt
= interaction input

Task
= durable unit of work
```

Task에는 대화문보다 더 많은 상태가 필요하다.

후보:

- ID
- Goal
- Scope
- Acceptance
- Dependencies
- Priority
- State
- Attempt count
- Worker
- Workspace
- Base revision
- Current revision
- Verification
- Artifact
- Approval
- Failure reason
- Carryover
- Timeline

이 구분은 Symphony의 session → deliverable 중심 전환과 잘 맞는다.

출처:

- https://openai.com/index/open-source-codex-orchestration-symphony/

## 2. Orchestrator의 책임

Orchestrator가 코드를 직접 작성할 필요는 없다.

주요 책임:

- work discovery
- eligibility
- dependency resolution
- worker allocation
- workspace provisioning
- role/model routing
- retry
- timeout
- recovery
- human approval
- result collection
- event persistence

## 3. Issue Tracker as Control Plane

Symphony는 Linear board를 control plane으로 사용한다.

장점:

- 사람과 agent가 같은 work state를 본다.
- 기존 PM workflow와 연결 가능
- "어떤 session이 살아 있는가"보다 "어떤 deliverable이 끝났는가"에 집중

한계:

일반 issue tracker만으로 다음 세부 상태가 부족할 수 있다.

- attempts
- runtime ID
- sandbox
- lease
- retry reason
- partial progress
- evidence
- verification

따라서 실제 Factory에서는 issue tracker + execution state store가 분리될 수 있다.

## 4. Event-driven Orchestration

WorkOS Horizon:

- Linear status change
- webhook
- orchestrator
- sandbox
- PR
- merge webhook
- dependent issue re-evaluation

이 흐름은 polling prompt보다 event-driven factory에 가깝다.

Event 후보:

```text
TaskCreated
TaskReady
TaskAssigned
AttemptStarted
WorkerStarted
ProgressUpdated
VerificationStarted
VerificationPassed
VerificationFailed
ApprovalRequested
Approved
Rejected
RetryScheduled
WorkerLost
AttemptEnded
TaskDone
```

## 5. Session Continuity

Anthropic long-running harness가 제기한 기본 문제:

> 다음 session은 이전 session이 무엇을 했는지 자동으로 기억하지 않는다.

해결에 사용한 것:

- initializer agent
- feature list
- progress file
- git history
- incremental task
- explicit next-step artifacts

Factory에서는 이를 더 일반화해야 한다.

```text
Session continuity
≠ model memory

Session continuity
= durable externalized work state
```

출처:

- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

## 6. Harness Failure와 Sandbox Failure도 고려

Anthropic Managed Agents:

- session state를 harness 밖에 둠
- harness가 crash해도 session log로 복구
- sandbox가 crash하면 새 sandbox를 provision 가능

OpenAI Agents SDK:

- external state
- snapshot
- rehydration
- new container에서 continuation

이는 Factory의 failure model을 확장한다.

```text
Possible failure:
- Model turn failure
- Tool failure
- Harness crash
- Sandbox crash
- Machine loss
- Network loss
- Process timeout
- Agent drift
- Verification failure
- Permission denial
```

출처:

- https://www.anthropic.com/engineering/managed-agents
- https://openai.com/index/the-next-evolution-of-the-agents-sdk/

## 7. Carryover에는 무엇이 들어가야 하는가

최소 carryover 후보:

- Task goal
- completed subtasks
- unresolved subtasks
- current branch/commit
- changed files
- uncommitted changes 여부
- latest verification
- failed commands
- decision summary
- blockers
- next recommended action

중요:

자연어 summary만으로 충분하지 않을 수 있다.

구조화된 state와 실제 working tree state가 함께 필요하다.

## 8. Uncommitted Work 문제

Agent A가 유효한 변경을 만들었지만 commit 전 runtime이 사라지면:

### Option 1 - Discard and retry

단순하지만 계산 비용 증가.

### Option 2 - Persist workspace volume

복구 가능하지만 stale/corrupt state 위험.

### Option 3 - Incremental checkpoint commit

Git을 checkpoint로 사용.

### Option 4 - Patch artifact

diff/patch를 external artifact로 저장.

### Option 5 - Filesystem snapshot

sandbox snapshot/restore.

Factory는 Task별로 recovery cost와 contamination risk를 비교해야 한다.

## 9. Retry와 Reassignment를 분리한다

Retry:

같은 worker/runtime가 다시 시도.

Reassignment:

다른 worker가 Task를 이어받음.

다른 failure semantics를 가진다.

재배정 시 필요:

- state reconstruction
- previous attempt evidence
- previous changes
- failure reason
- conflict prevention

## 10. Retry Budget

무한 retry는 autonomy가 아니라 비용 누수다.

후보 정책:

- max attempts
- max same-error attempts
- max token
- max wall time
- max compute
- escalation after policy denial
- escalation after repeated verification failure

Anthropic Auto Mode도 deny-and-continue를 사용하지만 3 consecutive denials 또는 20 total denials에서 human escalation/termination을 둔다.

출처:

- https://www.anthropic.com/engineering/claude-code-auto-mode

## 11. Dependency-aware Scheduling

Task A가 Task B의 schema/API를 바꾸는 경우 단순 parallel execution은 위험하다.

Task graph:

```text
A ─┬→ C
   └→ D
B ───→ D
```

Scheduler는:

- READY
- BLOCKED
- RUNNING
- VERIFYING
- AWAITING_HUMAN
- DONE
- FAILED

같은 상태를 사용해 dependency를 관리할 수 있다.

## 12. Parallelization Criteria

GitHub Fleet의 가이드와 일치하는 일반 조건:

좋음:

- different modules
- different files
- independent research
- independent tests
- independent validation

나쁨:

- shared schema
- same migration
- same core file
- strict sequence
- hidden runtime dependency

출처:

- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet

## 13. Proactive Work Selection

Google Jules Suggested Tasks / Scheduled Tasks는 agent가 사람이 직접 prompt하지 않은 maintenance work까지 제안/실행하는 방향을 보여준다.

그러나 "agent가 다음 Task를 스스로 선택한다"에는 추가 policy가 필요하다.

후보:

- source whitelist
- severity threshold
- risk class
- code ownership
- budget
- allowed paths
- allowed deployment target
- merge authority

출처:

- https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/

## 14. Work Selection과 Work Execution을 분리

Factory autonomy는 두 질문으로 나뉜다.

### 무엇을 할 것인가

- backlog selection
- issue creation
- priority
- decomposition

### 어떻게 할 것인가

- implementation
- testing
- debugging
- refactoring

두 번째가 가능하다고 첫 번째까지 자동화해야 하는 것은 아니다.

이 구분은 위험관리와 조직 권한 설계에서 중요하다.

## 15. 현재 Architecture Principle 후보

> Agent session은 ephemeral할 수 있지만 Task state는 ephemeral하면 안 된다.

> Task 완료의 책임은 특정 Worker가 아니라 Orchestrator가 가져야 한다.

> Reassignment 가능한 Task만 진정한 Factory Task라고 볼 수 있는가를 검토할 가치가 있다.

> Human escalation은 failure가 아니라 정상적인 state transition으로 모델링해야 한다.
