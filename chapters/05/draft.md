# 5장. Durable Task: Session보다 오래 살아남는 작업 단위

Agent에게 일을 맡겼다.

20분 동안 Repository를 탐색했고 파일 세 개를 수정했다.

테스트 하나가 아직 실패한다.

그 순간 Worker가 죽었다.

다시 시작했을 때 가장 먼저 필요한 것은 무엇일까.

더 좋은 Model이 아니다.

**어디까지 했는지 알 수 있는 작업 상태**다.

Interactive Agent에서는 Session이 작업의 중심이 되기 쉽다.

Software Factory에서는 충분하지 않다.

이 책에서는 Prompt와 Session보다 오래 살아남으며 상태, 시도, 검증, 결과를 가진 작업 단위를 **Durable Task**라고 부른다.

여기서 Durable Task는 이 책의 개념어다. Microsoft의 `Durable Task`라는 workflow runtime/product와 이름이 겹치지만 같은 뜻은 아니다. Microsoft Durable Task는 15장에서 durable execution의 구현 사례로 따로 다룬다.

---

## 5.1 Prompt, Session, Task

세 가지는 비슷해 보이지만 lifetime이 다르다.

~~~text
Prompt
= 한 번의 interaction

Session
= Agent가 일하는 execution context

Task
= 완료까지 추적되는 durable work item
~~~

Prompt는 사라져도 된다.

Session도 종료될 수 있다.

Task는 완료되거나 명시적으로 종료될 때까지 남아야 한다.

예를 들어 다음 요청을 생각해 보자.

~~~text
expired JWT를 401로 처리
~~~

Prompt에는 이 문장이 들어갈 수 있다.

Session에는 Repository 탐색, Tool Call, 실패 로그, 수정 결과가 쌓인다.

Task에는 더 오래 남아야 할 정보가 있다.

- Goal
- Scope
- Acceptance
- Status
- Attempt
- Worker
- Base Revision
- Verification
- Evidence
- Approval
- Failure Reason

Session이 새로 만들어져도 이 정보는 유지돼야 한다.

---

## 5.2 Task 최소 스키마

Durable Task를 처음부터 거대한 schema로 만들 필요는 없다.

다만 다음 범주는 구분하는 편이 좋다.

### Identity

~~~text
task_id
project_id
~~~

### Intent

~~~text
goal
scope
acceptance
~~~

### Scheduling

~~~text
priority
dependency
risk
required_capability
~~~

### Execution

~~~text
status
attempt_id
worker_id
workspace
base_revision
current_revision
~~~

### Verification

~~~text
verification_profile
verification_result
evidence
~~~

### Governance

~~~text
approval_state
approved_by
~~~

### Recovery

~~~text
failure_class
retry_count
carryover
~~~

모든 조직이 같은 필드를 가질 필요는 없다.

중요한 것은 이 정보가 Agent transcript 안에만 존재하지 않는 것이다.

---

## 5.3 Task와 Attempt를 분리한다

Task를 운영 단위로 만들려면 Attempt를 별도로 봐야 한다.

다음 상황을 생각해 보자.

~~~text
Task T-100
Goal: expired JWT → 401
~~~

첫 번째 Worker가 작업했지만 Verification에 실패했다.

~~~text
Attempt A1
Worker: W1
Result: failed
Reason: integration test failed
~~~

두 번째 Attempt에서 같은 Task를 다시 수행할 수 있다.

~~~text
Attempt A2
Worker: W2
Result: passed
~~~

Task는 하나다.

시도는 둘이다.

~~~text
Task T-100
├─ Attempt A1 → FAILED
└─ Attempt A2 → PASSED
~~~

이 구조가 필요한 이유는 단순하다.

실패한 Attempt도 정보이기 때문이다.

- 어떤 Worker에서 실패했는가
- 어떤 Command가 실패했는가
- 몇 번 Retry했는가
- 같은 Failure가 반복되는가
- 어떤 변경이 이미 만들어졌는가

Retry할 때 Task 자체를 새로 만들면 이 history가 끊긴다.

그러면 시스템은 같은 실패를 처음 보는 것처럼 반복할 수 있다.

---

## 5.4 Task 상태 전이

Factory에서는 Task 상태를 Agent의 자연어 설명과 분리하는 편이 좋다.

예를 들어 다음 정도의 상태가 있을 수 있다.

~~~text
READY
  ↓
RUNNING
  ↓
VERIFYING
  ↓
AWAITING_HUMAN
  ↓
DONE
~~~

실패 경로도 필요하다.

~~~text
RUNNING
  ├→ BLOCKED
  ├→ RETRY
  └→ FAILED
~~~

각 상태는 의미가 달라야 한다.

### READY

실행 조건이 충족됐다.

### RUNNING

현재 Attempt가 실행 중이다.

### VERIFYING

구현은 끝났고 required verification을 수행 중이다.

### AWAITING_HUMAN

Agent가 할 수 있는 일은 끝났고 승인이나 판단을 기다린다.

### BLOCKED

Dependency나 외부 조건 때문에 진행할 수 없다.

### RETRY

현재 Attempt는 종료됐고 새 Attempt가 필요하다. 실제 구현에서는 `RETRY_SCHEDULED`처럼 대기 상태와 실행 가능 상태를 더 세분화할 수 있다.

### DONE

Acceptance와 required gate를 모두 통과했다.

Agent가 "완료"라고 말해도 바로 DONE으로 가지 않는다.

상태 전이는 System Policy가 결정해야 한다.

---

## 5.5 Task가 Worker보다 오래 살아야 한다

Worker는 여러 이유로 사라질 수 있다.

- process crash
- VM restart
- timeout
- deploy
- network loss
- preemption
- manual stop

이때 Task state가 Worker 안에만 있다면 Work도 같이 사라진다.

좋은 구조는 반대다.

~~~text
Task State
= durable

Worker
= replaceable
~~~

Worker가 죽으면 Control Plane은 다음을 확인할 수 있어야 한다.

- Task는 RUNNING이었는가
- Attempt는 어디까지 갔는가
- Commit이 남아 있는가
- uncommitted change가 있는가
- 마지막 Verification은 무엇인가
- Retry 가능한 Failure인가

그리고 필요하면 새 Worker를 배정한다.

~~~text
Worker A lost
      ↓
Task remains
      ↓
Worker B assigned
~~~

이 구조가 가능하려면 Task state와 execution state를 분리해야 한다.

---

## 5.6 Context Window를 Task Database로 쓰지 않는다

Agent Session에는 많은 정보가 있다.

- 탐색한 파일
- 실패 로그
- 수정 이유
- 다음 행동

그래서 transcript 자체를 작업 저장소처럼 사용하고 싶어진다.

하지만 문제가 있다.

Context는 길이 제한이 있다.

Compaction이 발생할 수 있다.

Session이 교체될 수 있다.

다른 Worker가 같은 형식으로 이어받는다는 보장도 없다.

따라서 중요한 상태는 외부 durable artifact로 꺼내야 한다.

예:

~~~text
Task Store
Git
Artifact Store
Verification Result
~~~

Context Window는 reasoning을 위한 공간이다.

Durable Task State는 운영을 위한 기록이다.

둘을 섞지 않는다.

---

## 5.7 Carryover: 다른 Worker가 이어받을 수 있는가

단순히 다음 정보만 남겨서는 충분하지 않을 수 있다.

~~~text
Worker lost.
~~~

새 Worker가 실제로 이어받으려면 더 많은 정보가 필요하다.

~~~text
Goal
- expired JWT → 401

Completed
- AuthService 수정
- target unit test PASS

Remaining
- integration test failure

Changed Files
- AuthService.java
- AuthServiceTest.java

Current Revision
- abc123

Uncommitted Changes
- patch artifact://task-100/a1.patch

Latest Failure
- AuthIntegrationTest.expiredToken

Next Action
- inspect exception mapping
~~~

이것이 Carryover다.

Carryover의 품질을 평가하는 가장 좋은 질문은 간단하다.

> 다른 Worker가 이전 Worker의 도움 없이 이어갈 수 있는가?

이 질문에 답할 수 없다면 Task state가 충분히 durable하지 않은 것이다.

---

## 예: Verification 실패 후 새 Attempt

~~~text
Task T-100
Status: VERIFYING

Attempt A1
Worker: W1
Verification: FAIL
Reason: integration test
~~~

System은 A1을 닫는다.

~~~text
Task T-100
Status: RETRY
retry_count: 1
~~~

다음 Worker에게는 원래 Goal과 함께 실패 Evidence가 전달된다.

~~~text
Attempt A2
Worker: W2
Input:
- original acceptance
- A1 changes
- failed test
- failure summary
~~~

A2가 통과하면 Task는 VERIFYING을 거쳐 DONE으로 이동한다.

Task는 처음부터 새로 만들어지지 않는다.

---

## 다음 질문

Durable Task를 만들었다고 끝은 아니다.

Task가 너무 크면 Context와 Retry 비용이 커진다.

너무 작으면 Worker 시작과 Context 전달 비용이 더 커진다.

Task끼리 Dependency가 있으면 아무 순서로나 실행할 수도 없다.

다음 장에서는 **어떤 크기로 Task를 나누고 어떤 Dependency를 표현해야 하는가**를 다룬다.

---

## 참고 자료

- OpenAI, *An open-source spec for Codex orchestration: Symphony*  
  https://openai.com/index/open-source-codex-orchestration-symphony/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Anthropic, *Effective harnesses for long-running agents*  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Microsoft, *Durable Task for AI agents*  
  https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents
