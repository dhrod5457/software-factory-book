# 15장. Durable Execution: Crash를 넘어 이어지는 Work

Agent Task가 몇 초 안에 끝난다면 실행 상태를 크게 고민하지 않아도 된다.

하지만 작업이 수십 분, 수 시간, 며칠까지 길어지면 상황이 달라진다.

그동안 다음 일이 생길 수 있다.

- Worker process가 죽는다.
- Runtime이 재시작된다.
- Network가 끊긴다.
- 외부 API 응답이 유실된다.
- Human Approval을 몇 시간 기다린다.
- 같은 Tool Call이 중복 실행된다.

이 순간부터 Long-running Agent는 단순한 Prompting 문제가 아니다.

분산 시스템 문제에 가까워진다.

> Context를 저장하는 것과 실행을 복구하는 것은 다른 문제다.

이 장에서는 Agent Memory가 아니라 **Durable Execution**을 다룬다.

---

## 15.1 Memory와 Execution State는 다르다

Agent Session을 저장하면 이전 대화를 다시 읽을 수 있다.

하지만 다음 질문에는 답하지 못할 수 있다.

- 어떤 Step이 실제로 완료됐는가
- 어떤 외부 Side Effect가 이미 발생했는가
- 어디부터 다시 실행해야 하는가
- 같은 Tool Call을 다시 해도 안전한가
- 어떤 Human Event를 기다리고 있는가

예를 들어 Agent가 Pull Request를 생성하려고 했다.

~~~text
create_pull_request()
~~~

GitHub에서는 실제로 PR이 만들어졌다.

하지만 Network가 끊겨 Runtime은 응답을 받지 못했다.

다시 시작한 Agent가 같은 Tool을 호출하면 두 번째 PR이 생길 수 있다.

Conversation History를 저장해도 이 문제는 해결되지 않는다.

필요한 것은 **실행 결과와 Side Effect History**다.

---

## 15.2 Event History

Durable Execution에서는 중요한 상태 변화와 외부 행동을 기록한다.

예:

~~~text
TaskStarted
WorkerAssigned
CheckoutCompleted
PatchCreated
UnitTestPassed
PullRequestCreateRequested
PullRequestCreated
ApprovalRequested
~~~

Runtime이 중간에 죽더라도 Event History를 보고 이미 완료된 Step을 알 수 있다.

~~~text
Replay
→ completed step skip
→ incomplete step continue
~~~

여기서 Replay는 Agent가 같은 문장을 다시 생성한다는 뜻이 아니다.

Workflow Runtime이 **어떤 실행이 이미 완료됐는지 재구성**하는 것이다.

---

## 15.3 Checkpoint

모든 Event만으로 실제 Workspace를 복구하기 어려울 수 있다.

그래서 Checkpoint를 둔다.

Coding Task에서는 Git Commit 자체가 좋은 Checkpoint가 될 수 있다.

~~~text
Workspace
→ incremental commit
→ durable Git state
~~~

하지만 Git만으로는 충분하지 않다.

Git에 없는 상태가 있기 때문이다.

- 현재 Attempt
- Approval 상태
- Tool Result
- External Side Effect
- Retry Count
- Pending Timer

그래서 보통 다음 두 상태가 필요하다.

~~~text
Git State
+
Orchestration State
~~~

필요하면 Patch, Filesystem Snapshot, Artifact도 추가할 수 있다.

Checkpoint Granularity는 Task마다 다를 수 있다.

너무 자주 만들면 overhead가 크다.

너무 드물면 crash 때 잃는 작업이 커진다.

---

## 15.4 Exactly-once를 기대하지 않는다

외부 Side Effect에 완전한 Exactly-once를 보장하기는 어렵다.

다음 상황을 보자.

~~~text
Factory
→ deploy(version=abc123)

Deployment Platform
→ success

Network response
→ lost

Factory
→ retry deploy(version=abc123)
~~~

두 번째 호출이 안전한지는 Tool Contract에 달려 있다.

그래서 Idempotency가 중요하다.

예:

~~~text
deploy(
  operation_id="T100-A2-deploy",
  revision="abc123"
)
~~~

같은 operation_id로 재호출하면 Platform은 이전 결과를 반환할 수 있다.

~~~text
status: already_completed
deployment_id: dep-882
~~~

이 구조는 다음 작업에도 필요하다.

- Pull Request create
- Issue update
- Email
- DB mutation
- Release
- Payment-like internal operation

---

## 15.5 Replay-safe Tool

Agent Tool도 Durable Runtime을 고려해 설계할 수 있다.

나쁜 예:

~~~text
create_pr(title, body)
~~~

응답이 유실되면 재호출 시 duplicate 가능성이 있다.

더 나은 예:

~~~text
create_pr(
  operation_id,
  repository,
  head,
  base,
  title
)
~~~

Tool은 같은 operation_id를 인식한다.

~~~text
if already executed:
    return previous result
~~~

이 원칙은 Agent-native Platform Interface에서 중요하다.

Agent가 Tool을 자유롭게 호출할수록 Runtime이 duplicate Side Effect를 막아야 한다.

---

## 15.6 Human Approval은 Async Event다

Human-in-the-loop를 synchronous process로 생각하면 Resource를 낭비한다.

예:

~~~text
Worker
→ Plan complete
→ waits 8 hours
→ human approve
→ continues
~~~

Worker를 8시간 유지할 필요가 없다.

더 좋은 구조는 다음과 같다.

~~~text
Task
→ ApprovalRequested
→ Worker released
→ Task suspended

8 hours later

Human Approval Event
→ Task resumed
→ Worker assigned
~~~

Human은 Durable Workflow에 들어오는 asynchronous signal로 볼 수 있다.

이 구조가 있으면 Approval Wait와 Compute Occupancy를 분리할 수 있다.

---

## 15.7 Durable Runtime과 Agent Harness의 책임

둘을 구분해보자.

### Agent Harness

질문:

~~~text
다음에 무엇을 해야 하는가?
~~~

책임:

- Context
- Tool Selection
- Agent Loop
- Reasoning
- Implementation

### Durable Runtime

질문:

~~~text
이 Work가 현실의 Crash와 Wait를 살아남게 하려면?
~~~

책임:

- Event History
- Retry
- Timer
- Wait
- Signal
- Cancellation
- Idempotency
- Resume

개념적으로 다음처럼 볼 수 있다.

~~~text
Factory Control Plane
        ↓
Durable Runtime
        ↓
Agent Harness
        ↓
Worker / Sandbox
~~~

구현에 따라 Layer가 합쳐질 수 있다.

중요한 것은 책임을 구분하는 것이다.

---

## 15.8 제품이 아니라 책임 분리로 본다

Temporal, Microsoft Durable Task, Google Agent Executor 같은 시스템은 서로 구현이 다르다.

이 책에서 중요한 것은 특정 제품 API가 아니다.

공통적으로 다음 문제를 다룬다는 점이다.

- long-running state
- retry
- resume
- event
- human wait
- crash recovery

Factory가 직접 모든 것을 구현할 수도 있다.

하지만 lease, timer, retry, history, idempotency는 전형적인 distributed systems 문제다.

규모가 커지기 전에 기존 Durable Workflow Infrastructure를 검토할 가치가 있다.

---

## 15.9 Crash Test를 Acceptance Scenario로 만든다

Factory Reliability를 Happy Path만으로 평가하면 부족하다.

일부러 실패를 주입해볼 수 있다.

~~~text
Worker process kill
VM kill
Network disconnect
Orchestrator restart
Approval delay
Tool timeout
~~~

검증할 항목:

~~~text
Task state preserved?
Retry budget preserved?
Duplicate PR created?
Uncommitted work lost?
Evidence still linked?
Different Worker resume possible?
~~~

이런 시험은 Agent Benchmark보다 Factory Reliability를 더 직접적으로 보여줄 수 있다.

---

## 15.10 Resume Quality

Agent Reliability를 Success Rate만으로 보면 부족하다.

장기 Task에서는 다음도 중요하다.

~~~text
Resume Quality
~~~

예를 들어 Worker A가 80%까지 작업하고 죽었다.

Worker B가 처음부터 다시 한다면 Task는 최종적으로 성공할 수 있다.

하지만 Continuity는 약하다.

더 강한 기준은 다음이다.

> 다른 Worker가 이전 Worker의 유효한 작업을 보존하고 이어받을 수 있는가?

이 기준은 5장에서 다룬 Durable Task와 연결된다.

Durable Task State가 있어도 Workspace/Checkpoint State가 없으면 실제 작업은 다시 시작할 수 있다.

---

## 예: Duplicate PR 방지

Attempt A1:

~~~text
operation_id: T100-pr-create
create PR
→ GitHub success
→ response lost
~~~

Runtime Restart.

Attempt A2가 다시 요청한다.

~~~text
create_pr(
  operation_id="T100-pr-create"
)
~~~

Tool은 기존 결과를 반환한다.

~~~text
status: already_exists
pr: #381
~~~

이것이 Durable Execution이 Tool Contract까지 영향을 주는 예다.

---

## 다음 질문

Work가 Crash와 Wait를 견딜 수 있게 됐다.

이제 더 오래, 더 많은 권한으로 Agent를 실행할 수 있다.

그만큼 위험도 커진다.

Agent가 어떤 Credential을 가져야 하는가.

Untrusted Issue 내용이 Tool Call로 이어지면 어떻게 막을 것인가.

다음 장에서는 **Security, Identity, Governance**를 다룬다.

---

## 참고 자료

- Microsoft, *Durable Task for AI agents*  
  https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents
- Temporal, *AI and Durable Execution*  
  https://docs.temporal.io/ai
- Google Cloud, *Agent Executor: Google’s distributed agent runtime*  
  https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime
- Anthropic, *Effective harnesses for long-running agents*  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
