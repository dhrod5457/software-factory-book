# 7장. Control Plane과 Execution Plane

Part II에서는 Work를 실행 가능한 형태로 만들었다.

Requirement와 Acceptance를 정하고, Durable Task로 상태를 남기고, Dependency Graph를 만들었다.

이제 실제 실행이 필요하다.

여기서 가장 먼저 분리해야 할 것이 있다.

**Task를 관리하는 시스템**과 **Task를 실행하는 Worker**다.

이 책에서는 앞쪽을 Control Plane, 뒤쪽을 Execution Plane이라고 부른다.

~~~text
Durable Task
      ↓
Control Plane
      ↓
Assignment
      ↓
Execution Plane
      ↓
Result / Evidence
      ↓
Control Plane
~~~

이 경계를 분리하지 않으면 Worker가 곧 Task가 된다.

Worker가 죽으면 Work도 사라지고, Session이 끊기면 상태도 끊긴다.

Factory에서는 반대여야 한다.

> Task의 완료 책임은 Worker가 아니라 시스템에 있어야 한다.

---

## 7.1 Control Plane이 관리해야 하는 상태

Control Plane은 코드를 직접 작성하는 주체가 아니다.

주요 책임은 **Work의 상태와 흐름을 관리하는 것**이다.

예를 들면 다음과 같다.

- Task lifecycle
- Ready / Blocked 상태
- Dependency
- Priority
- Assignment
- Worker lease
- Attempt
- Retry
- Approval
- Verification 상태
- Result reference
- Event history

한 Task를 다음처럼 볼 수 있다.

~~~text
Task T-200
Status: READY
Dependency: T-190 done
Required Worker: backend-java
Risk: medium
~~~

Scheduler가 Worker를 배정하면 상태가 바뀐다.

~~~text
Task T-200
Status: RUNNING
Attempt: A1
Worker: W7
~~~

Worker가 코드를 바꾸고 결과를 돌려주면 다시 상태가 바뀐다.

~~~text
Task T-200
Status: VERIFYING
Result Revision: abc123
~~~

검증이 통과했지만 Human Review가 필요하면:

~~~text
Task T-200
Status: AWAITING_HUMAN
~~~

이 상태는 Agent가 자연어로 기억하는 것이 아니라 시스템에 저장된다.

그래야 Worker가 바뀌어도 같은 Task를 계속 추적할 수 있다.

---

## 7.2 Execution Plane의 책임

Execution Plane은 실제 작업이 일어나는 곳이다.

다음과 같은 요소가 들어간다.

- Repository checkout
- Workspace
- Branch / Worktree
- Agent Harness
- Shell
- Build Tool
- Test Runner
- Browser
- Local Service
- Temporary File

Execution Plane은 Task를 **수행**한다.

하지만 가능한 한 durable한 orchestration state는 적게 가진다.

예를 들어 Worker가 다음 정보를 유일하게 갖고 있으면 위험하다.

~~~text
현재 Task가 무엇인지
Retry가 몇 번째인지
Human Approval이 필요한지
다음 Dependency가 무엇인지
~~~

이 정보는 Worker가 아니라 Control Plane이 가져야 한다.

Worker는 다음 정도를 받아 실행하면 된다.

~~~text
Task Input
- goal
- scope
- acceptance
- base revision
- worker profile
- verification profile
~~~

그리고 결과를 반환한다.

~~~text
Task Result
- result revision
- changed files
- verification output
- evidence
- failure / blocker
~~~

이 구조가 되면 Worker는 교체 가능해진다.

---

## 7.3 Issue Tracker와 Execution State는 같은 것이 아니다

많은 조직에서 Issue Tracker는 이미 Work의 출발점이다.

그래서 다음 흐름은 자연스럽다.

~~~text
Issue
→ Factory Task
→ Worker
~~~

OpenAI Symphony나 WorkOS Horizon처럼 Issue Tracker를 Work의 control surface로 활용하는 공개 사례도 있다. 다만 Symphony의 공개 spec도 dispatch·retry·reconciliation을 위한 authoritative orchestrator runtime state를 별도로 둔다. “Issue Tracker를 Control Plane으로 쓴다”는 표현을 runtime state까지 모두 Issue에 저장한다는 뜻으로 해석하면 안 된다.

하지만 Issue Tracker 하나에 모든 runtime state를 넣으려 하면 문제가 생긴다.

Issue에는 다음 정보가 잘 맞는다.

- Goal
- Priority
- Owner
- Product Context
- Acceptance
- Dependency

반면 다음은 실행 중 자주 변하는 상태다.

- Current Attempt
- Worker Lease
- Workspace ID
- Verification Run
- Retry Count
- Runtime Failure
- Heartbeat

이런 정보까지 Issue comment나 custom field로 표현할 수는 있다.

문제는 그것이 항상 좋은 모델은 아니라는 것이다.

실행 상태는 훨씬 더 자주 바뀌고, atomic update와 recovery semantics가 필요하다.

그래서 실무에서는 다음처럼 나눌 수 있다.

~~~text
Issue Tracker
= Work Intent / Human Collaboration

Task Store
= Durable Execution State

Worker Runtime
= Temporary Execution
~~~

셋이 같은 제품일 수도 있다.

작은 구현에서는 GitHub Issue의 Label과 Comment를 Human-facing Control Surface로 사용할 수도 있다.

~~~text
ready
→ running
→ review
~~~

이렇게 하면 별도 Dashboard 없이도 사람이 현재 흐름을 볼 수 있다.

다만 이 편리함 때문에 다음 두 개를 같은 것으로 보면 안 된다.

~~~text
Human-facing State
≠ Authoritative Runtime State
~~~

Issue Label은 사람이 이해하기 좋은 Projection일 수 있다. Worker Lease, Retry Count, Attempt History 같은 실행 의미까지 같은 표현에 억지로 담을 필요는 없다.

중요한 것은 책임을 구분하는 것이다.

---

## 7.4 Scheduler와 Agent를 구분한다

어떤 Task를 언제 누구에게 줄 것인가.

어떤 구현 전략으로 해결할 것인가.

둘은 다른 문제다.

예를 들어 다음 Task가 있다고 하자.

~~~text
T1
- Java backend
- internal network 필요
- auth module
- medium risk
~~~

어느 Worker에 배정할지는 다음 정보로 결정할 수 있다.

- Worker capability
- Queue
- Dependency
- Risk
- Resource availability

이것은 Scheduler의 문제다.

반면 Worker 안에 들어간 Agent는 다음을 판단한다.

- 어떤 Class를 먼저 읽을지
- 어떤 Test를 실행할지
- Exception mapping을 어디서 바꿀지
- 어떤 구현이 가장 적절한지

이것은 Agent judgment다.

둘을 섞으면 Scheduler 판단까지 Prompt에 들어가기 쉽다.

~~~text
너는 지금 Queue 상태를 보고
적절한 Task를 선택하고
Retry 횟수도 기억하고
필요하면 다른 Worker를...
~~~

이런 구조는 상태가 transcript 안에 숨어 버린다.

이미 알고 있는 scheduling rule은 시스템에 두는 편이 낫다.

---

## 7.5 Worker를 disposable하게 만들려면 무엇을 밖으로 꺼내야 하는가

Execution Plane을 disposable하게 만들고 싶다면 먼저 물어야 한다.

> Worker를 지금 없애도 다시 이어갈 수 있는가?

필요한 state가 Worker 밖에 있어야 한다.

최소한 다음은 외부화하는 편이 좋다.

### Task State

~~~text
Task Store
- status
- attempt
- retry
- approval
~~~

### Source State

~~~text
Git
- base revision
- commit
- branch
~~~

### Partial Work

~~~text
Checkpoint / Patch / Snapshot
~~~

### Verification

~~~text
Verification Result
- command
- exit
- failed tests
- artifact reference
~~~

### Evidence

~~~text
Artifact Store
- screenshot
- log
- benchmark
~~~

Worker는 이 durable state를 받아 execution을 수행한다.

이 구조가 있으면 다음이 가능하다.

~~~text
Worker A
→ crash

Control Plane
→ detects loss
→ closes Attempt A1
→ creates Attempt A2

Worker B
→ restores Task state
→ continues
~~~

물론 실제로 "continue"하려면 uncommitted work까지 어떻게 보존할지 결정해야 한다.

이 문제는 14~15장에서 더 깊게 다룬다.

여기서 중요한 것은 원칙이다.

**Compute는 잃을 수 있어도 Work State는 잃지 않는다.**

---

## Human Approval을 기다릴 때 Worker를 계속 잡고 있어야 할까

다음 상황을 생각해보자.

Agent가 Production Migration Plan을 만들었다.

검증까지 끝났다.

이제 DBA 승인을 기다려야 한다.

Worker를 6시간 동안 계속 실행할 이유가 있을까.

Control Plane이 Task 상태를 durable하게 갖고 있다면 다음처럼 할 수 있다.

~~~text
Task
RUNNING
  ↓
VERIFYING
  ↓
AWAITING_HUMAN

Worker
→ released
~~~

승인이 들어오면 새 Worker를 배정할 수 있다.

~~~text
Approval Event
      ↓
Task READY
      ↓
New Worker
~~~

이 구조는 긴 Human Wait를 execution resource와 분리한다.

---

## Control Plane과 Execution Plane의 최소 경계

Minimum Viable Factory라면 거대한 orchestration platform이 없어도 된다.

다음 정도면 시작할 수 있다.

~~~text
Control Plane
- Task DB
- simple queue
- attempt state
- retry count
- approval state

Execution Plane
- one worker process
- isolated worktree
- coding agent
- build/test
~~~

이 정도만으로도 중요한 효과가 생긴다.

- Worker가 Task의 유일한 state owner가 아니다.
- Retry history를 남길 수 있다.
- Human Wait에서 Worker를 해제할 수 있다.
- 나중에 Worker를 여러 개로 확장할 수 있다.

---

## 다음 질문

Control Plane과 Execution Plane을 나눴다.

이제 Execution Plane 안을 더 자세히 봐야 한다.

Worker는 어떤 filesystem을 가져야 하는가.

매번 새로 만들 것인가.

Dependency와 Browser를 매 Task 다시 설치할 것인가.

Warm 상태를 재사용하면 무엇이 위험한가.

다음 장에서는 **Worker, Sandbox, Workspace**를 다룬다.

---

## 참고 자료

- OpenAI, *An open-source spec for Codex orchestration: Symphony*  
  https://openai.com/index/open-source-codex-orchestration-symphony/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands*  
  https://www.anthropic.com/engineering/managed-agents
- Microsoft, *Durable Task for AI agents*  
  https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents
- *I Built the Simplest Software Factory*, YouTube video / user-provided transcript  
  https://www.youtube.com/watch?v=AsvzMlLyQ38
