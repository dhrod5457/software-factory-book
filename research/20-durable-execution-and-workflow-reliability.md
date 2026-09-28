# Durable Execution and Workflow Reliability

기준일: 2026-09-28

AI Software Factory의 Task가 몇 초가 아니라 수십 분, 수 시간, 수일 동안 실행되기 시작하면 단순 Agent framework만으로 해결되지 않는 문제가 나타난다.

- worker crash
- deploy/restart
- network timeout
- rate limit
- human approval wait
- external API partial failure
- duplicate side effect

이 문서는 **Durable Execution**을 Factory의 reliability layer로 조사한다.

---

# 1. Session Memory와 Durable Execution은 다르다

Session memory:

- conversation
- context
- prior result

Durable execution:

- 어떤 step이 실제 완료됐는가
- 어떤 tool side effect가 발생했는가
- 어디부터 재개할 것인가
- retry 시 같은 external action을 중복하지 않는가

```text
Memory
≠ Execution State
```

---

# 2. Microsoft Durable Task

Microsoft는 Agent가:

- hours/days/weeks 실행
- external tools 호출
- HITL wait
- infrastructure failure 생존

하려면 durable execution이 필요하다고 명시한다.

Durable Task가 제공:

- state persistence
- checkpoint
- distributed coordination
- automatic recovery
- retry

중요한 구분:

> Durable Task는 Agent Framework가 아니다.

어떤 Agent framework와도 결합 가능하다.

출처:

- https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents

---

# 3. Deterministic Workflow와 Agent-directed Workflow

Microsoft는 두 종류 모두 Durable Execution 위에 둘 수 있다고 설명한다.

### Deterministic

```text
Code decides flow
LLM is a step
```

### Agent-directed

```text
Agent decides tool/order/completion
Runtime preserves execution
```

이 구분이 중요하다.

Durability를 위해 Agent autonomy 자체를 제거할 필요는 없다.

---

# 4. Temporal

Temporal은 long-running workflow를 event history 기반으로 재생해 crash 이후 복구한다.

Agent에 적용할 때:

- Workflow = reliable orchestration
- Activity = LLM/tool/external I/O

로 분리한다.

Non-deterministic Agent behavior는 Activity boundary 밖에 두고 결과를 기록한다.

출처:

- https://docs.temporal.io/ai
- https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal

---

# 5. Google Agent Executor

Google은 2026년 Agent Executor를 distributed Agent Runtime으로 공개했다.

목적:

- agent execution
- resumption
- distributed deployment

핵심:

- event log
- snapshot
- outage/HITL 이후 resume

Agent뿐 아니라:

- harness
- skill
- tool
- sandbox

에도 durable actor model을 적용할 수 있다고 설명한다.

출처:

- https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime

---

# 6. Vercel eve

Vercel은 agent production runtime에 다음을 기본 capability로 묶었다.

- durable execution
- sandboxed compute
- HITL approval
- subagents
- evals

출처:

- https://vercel.com/blog/introducing-eve

이것은 Agent Framework가 reasoning loop만 제공하는 단계에서 production runtime까지 확대되는 흐름을 보여준다.

---

# 7. Durable Execution Layer의 책임

후보:

- event history
- checkpoint
- retry
- timeout
- timer
- wait
- signal
- cancellation
- compensation
- idempotency
- task queue
- worker routing

Agent logic과 분리하면:

```text
Agent
= What should I do?

Durable Runtime
= Make sure the work survives reality.
```

---

# 8. Exactly-once 환상

Distributed system에서 arbitrary side effect에 완전한 exactly-once를 보장하기 어렵다.

예:

```text
Agent calls external API
API succeeds
network response lost
runtime retries
→ duplicated side effect
```

필요:

- idempotency key
- deduplication
- transactional outbox
- external operation status lookup
- compensation

Factory에서도 중요하다.

특히:

- PR create
- issue update
- deploy
- email
- DB mutation

---

# 9. Tool Call을 Replay-safe하게 만든다

가능한 tool interface:

```text
execute(operation_id, ...)
```

같은 operation_id로 재호출되면:

- previous result 반환
- duplicate mutation 방지

이런 API가 Agent-native platform에서 중요해질 수 있다.

---

# 10. Checkpoint Granularity

너무 자주:

- storage/event overhead

너무 드물게:

- retry cost 증가
- progress loss

Checkpoint 후보:

- model turn
- tool call
- commit
- test phase
- task substep

Task type별로 조절 가능하다.

---

# 11. Git 자체도 Checkpoint다

Coding Factory에서는 Git이 특별한 durable checkpoint 역할을 할 수 있다.

```text
Workspace
→ Incremental Commit
→ External Durable State
```

하지만 Git만으로는 부족하다.

Git에 없는 상태:

- attempt
- approval
- tool result
- external mutation
- runtime
- pending human input

따라서:

```text
Git State
+ Orchestration State
```

가 필요하다.

---

# 12. Human-in-the-loop는 Async Event

사람 승인을 runtime process를 붙잡아 둔 채 기다리면 비효율적이다.

더 나은 구조:

```text
Task
→ ApprovalRequested
→ Runtime suspended / released
→ Human approves later
→ Event
→ Resume
```

이 관점에서 Human은 durable workflow에 들어오는 asynchronous signal이다.

---

# 13. Crash Recovery Test가 필요하다

Factory acceptance scenario에 의도적인 failure injection을 포함할 수 있다.

- worker process kill
- VM kill
- network disconnect
- orchestrator restart
- approval delay
- tool timeout

검증:

- duplicate side effect 없음
- progress 보존
- retry budget 유지
- final evidence 연결

---

# 14. Resume와 Restart 구분

### Restart

처음부터 새로 실행.

### Resume

이미 완료된 work를 인정하고 중단 지점 이후 진행.

장기 Task일수록 차이가 크다.

```text
Agent Reliability
= Success Rate
+ Resume Quality
```

---

# 15. Reassignment는 Resume보다 어렵다

같은 Agent runtime resume:

- state format 일치

다른 Worker 재배정:

- workspace
- credentials
- files
- context
- partial work

까지 reconstruct해야 한다.

따라서 Factory의 강한 continuity 기준은:

> 다른 Worker가 이어받을 수 있는가?

가 될 수 있다.

---

# 16. Workflow Engine과 Factory Orchestrator

같은 것이 아니다.

Workflow engine:

- durable execution primitive

Factory orchestrator:

- domain-level task selection
- software dependency
- branch conflict
- verification policy
- worker role
- human approval

Factory orchestrator가 Temporal/Durable Task/Agent Executor 같은 runtime을 사용할 수 있다.

---

# 17. Build or Buy

직접 구현하기 쉬운 것처럼 보이지만:

- retry
- lease
- timer
- idempotency
- crash recovery
- history compaction

은 distributed systems 문제다.

Factory가 모든 것을 직접 만들기 전에 durable workflow infrastructure를 검토해야 한다.

---

# 18. Reference Layer

```text
Factory Control Plane
      ↓
Durable Workflow Runtime
      ↓
Agent Harness
      ↓
Worker/Sandbox
      ↓
External Systems
```

또는 구현에 따라 Agent Harness와 Durable Runtime 관계가 반대/통합될 수도 있다.

중요한 것은 책임 분리다.

---

# 핵심 후보 메시지

> Long-running Agent를 만드는 순간 AI Software Factory는 분산 시스템이 된다.

> Context를 저장하는 것과 실행을 복구하는 것은 다른 문제다.

> Agent framework는 reasoning loop를 제공할 수 있지만 Task가 crash·deploy·HITL을 넘어 살아남게 하는 reliability layer는 별도로 필요할 수 있다.

> Factory의 continuity를 평가할 때 성공한 happy path보다 중간에 Worker를 죽여 보는 시험이 더 중요하다.
