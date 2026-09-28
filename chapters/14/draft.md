# 14장. Failure와 Recovery: 실패를 정상 상태로 설계한다

Software Factory에서 실패는 예외가 아니다.

Agent가 틀릴 수 있다.

Tool이 실패할 수 있다.

Network가 끊길 수 있다.

Worker가 죽을 수 있다.

Test가 flaky할 수 있다.

권한이 부족할 수도 있다.

문제는 실패 자체가 아니다.

**실패 종류를 구분하지 못하고 항상 같은 방식으로 다시 실행하는 것**이 더 큰 문제다.

예를 들어 Container Registry가 잠시 503을 반환했다.

이때 Coding Agent에게 “문제를 고쳐라”라고 다시 시키면 엉뚱한 코드 변경을 시작할 수 있다.

반대로 실제 Unit Test가 깨졌는데 단순 Tool Retry만 반복해도 해결되지 않는다.

그래서 Recovery는 다음 두 질문에서 시작한다.

> 무엇이 실패했는가?

> 어느 범위부터 다시 해야 하는가?

---

## 14.1 Failure Taxonomy

Factory에서 Failure를 몇 가지 범주로 나눌 수 있다.

### Tool Failure

예:

- GitHub API 502
- Registry timeout
- Log API temporary error

코드 자체와 무관할 수 있다.

### Harness Failure

예:

- Tool schema mismatch
- malformed output
- context assembly failure
- Agent adapter crash

### Worker Failure

예:

- process crash
- VM termination
- disk full
- out-of-memory

### Network Failure

예:

- package registry unavailable
- internal API timeout
- transient DNS error

### Verification Failure

예:

- unit test fail
- integration test fail
- security scan fail

실제 코드 문제일 가능성이 있다.

### Permission Failure

예:

- protected branch push denied
- production credential unavailable
- network policy deny

### Agent Drift

예:

- Scope 밖 파일 수정
- Acceptance와 무관한 Refactoring
- 같은 잘못된 가설 반복

### Environment Failure

예:

- stale cache
- polluted test DB
- wrong runtime version

이 분류가 완벽할 필요는 없다.

중요한 것은 모든 Failure를 “Agent 실패” 하나로 합치지 않는 것이다.

---

## 14.2 Recovery Ladder

Failure가 났다고 바로 Worker 전체를 새로 만들 필요는 없다.

가장 작은 범위부터 복구할 수 있다.

~~~text
Tool Retry
→ Step Retry
→ Agent Nudge
→ Subtask Retry
→ Worker Restart
→ Reassignment
→ Human Escalation
~~~

### Tool Retry

외부 API의 일시적 오류.

### Step Retry

특정 Build/Test Step만 다시 실행.

### Agent Nudge

방향은 맞지만 작은 오해가 있을 때 correction을 준다.

### Subtask Retry

실패한 Task Segment만 다시 수행.

### Worker Restart

Worker 상태가 오염됐거나 process가 죽었을 때.

### Reassignment

다른 Worker가 같은 Task를 이어받는다.

### Human Escalation

자동 복구가 의미 없거나 위험할 때 사람에게 넘긴다.

Recovery Scope가 커질수록 비용도 커진다.

그래서 가능한 한 작은 범위를 선택한다.

---

## 14.3 Infinite Retry를 막는다

다음 구조는 위험하다.

~~~text
while failed:
    retry()
~~~

같은 Failure가 반복되면 비용만 늘고 side effect도 커질 수 있다.

그래서 Retry Budget이 필요하다.

예:

~~~text
max_retries: 2
~~~

하지만 Count만으로는 부족할 수 있다.

같은 Failure가 반복되는지도 봐야 한다.

이를 위해 이 책에서는 반복 오류를 식별할 수 있는 **Failure Fingerprint**를 두는 방식을 사용한다. 이것 역시 특정 업계 표준이 아니라 동일 실패의 반복 여부를 판단하기 위한 설계 패턴이다.

예:

~~~text
type: integration-test
test: AuthIntegrationTest.expiredToken
exception: IllegalStateException
~~~

Attempt가 바뀌어도 같은 Fingerprint가 반복된다면 단순 Retry보다 Escalation이나 다른 Recovery가 필요하다.

~~~text
A1
→ same fingerprint

A2
→ same fingerprint

System
→ stop retry
→ escalate
~~~

---

## 14.4 Restart, Resume, Reassign은 다르다

세 단어는 비슷해 보이지만 의미가 다르다.

### Restart

처음부터 다시 시작한다.

~~~text
Task
→ new attempt
→ start from base revision
~~~

장점:

- clean state

단점:

- 이미 완료한 Work를 잃는다.

### Resume

이미 완료한 Work를 인정하고 중단 지점 이후부터 이어간다.

~~~text
Task
→ restore checkpoint
→ continue
~~~

장점:

- 재작업 감소

단점:

- checkpoint quality가 필요하다.

### Reassign

다른 Worker가 이어받는다.

~~~text
Worker A lost
→ Worker B continues
~~~

이 경우 Resume보다 더 어렵다.

다른 Worker가 partial state까지 이해할 수 있어야 하기 때문이다.

---

## 14.5 Carryover Contract

다른 Worker가 이어받으려면 “왜 중단됐는가”만으로는 부족하다.

다음 정보가 필요할 수 있다.

~~~text
Goal
Completed Work
Changed Files
Current Revision
Uncommitted Diff
Latest Verification
Failed Command
Failure Fingerprint
Known Blocker
Next Action
~~~

예:

~~~text
Goal
- expired JWT → 401

Completed
- AuthService 수정
- unit test PASS

Remaining
- integration test FAIL

Uncommitted
- patch artifact://T-100/A1.patch

Failure
- AuthIntegrationTest.expiredToken
- IllegalStateException

Next
- inspect exception mapping
~~~

Carryover의 품질은 다음 질문으로 평가할 수 있다.

> 새로운 Worker가 이전 Worker와 대화하지 않고 이어갈 수 있는가?

---

## 14.6 Infra Failure와 Code Failure를 섞지 않는다

예를 들어 다음 오류가 발생했다.

~~~text
docker pull registry.example.com/app:latest
→ 503 Service Unavailable
~~~

이 Failure는 Application Code와 무관할 수 있다.

Coding Agent에게 다시 “고쳐라”라고 하면 Agent는 다음을 시도할 수 있다.

- Dockerfile 수정
- Dependency 변경
- Build Script 변경

실제 원인은 Registry 장애인데 코드가 바뀐다.

반대로 다음 Failure는 코드 문제일 수 있다.

~~~text
AuthServiceTest.expiredToken
expected: 401
actual: 500
~~~

이 경우 Agent Fix가 적절하다.

Failure Classification이 없으면 복구가 잘못된 Layer에서 일어난다.

---

## 14.7 Targeted Intervention

Recovery는 Retry 아니면 Human Takeover 두 가지만 있는 것이 아니다.

2026년 arXiv preprint인 Wink 연구는 production traffic에서 수집한 10,000개 이상의 coding-agent trajectory를 바탕으로 외부 Observer가 작은 Intervention으로 복구하는 패턴을 연구했다. 저자들은 분석 대상에서 Specification Drift, Reasoning Problem, Tool Call Failure 같은 misbehavior가 전체 trajectory의 약 30%에서 관찰됐고, 한 번의 intervention이 필요한 사례 중 90%를 Wink가 해결했다고 보고했다. 이 수치는 해당 production 환경과 taxonomy에서 나온 결과이며 일반적인 coding-agent 실패율로 해석하면 안 된다.

개념적으로 다음과 같다.

~~~text
Primary Agent
      ↓
Trajectory
      ↓
Observer
      ↓
Targeted Correction
      ↓
Primary Agent continues
~~~

예를 들어 Agent가 Scope 밖 Directory로 가기 시작했다고 하자.

전체 Worker를 버리는 대신 다음과 같은 Nudge를 줄 수 있다.

~~~text
변경 범위를 auth module로 제한하라.
현재 수정한 frontend 파일은 되돌려라.
~~~

이 방식은 Full Restart보다 비용이 낮을 수 있다.

모든 Task에 Observer Agent가 필요하다는 뜻은 아니다.

중요한 것은 Recovery에도 여러 Granularity가 있다는 것이다.

---

## 14.8 Human Escalation은 실패가 아니다

자동화 시스템에서는 Human Escalation을 실패처럼 보기 쉽다.

하지만 실제 Factory에서는 정상적인 상태일 수 있다.

예:

- Requirement ambiguity
- Architecture decision 필요
- Security exception 필요
- Production risk 높음
- Retry budget 소진
- 동일 Failure 반복

이 경우 다음 상태가 적절할 수 있다.

~~~text
Task
→ BLOCKED / AWAITING_HUMAN
~~~

사람이 결정을 내린 뒤 다시 READY로 돌아간다.

~~~text
Human Decision
→ Task READY
→ new attempt
~~~

Human Escalation이 있다는 이유로 Factory가 덜 자율적인 것은 아니다.

잘못된 자동화를 멈출 수 있다는 점에서 오히려 reliability가 높을 수 있다.

---

## 14.9 Recovery Policy 예시

다음처럼 Failure Class마다 정책을 둘 수 있다.

~~~text
registry_timeout
→ tool retry
→ max 3
→ exponential backoff

unit_test_failure
→ agent fix
→ max 2 attempts

worker_lost
→ resume if checkpoint exists
→ otherwise reassign

permission_denied
→ no retry
→ human/policy escalation

same_failure_repeated
→ stop
→ escalation
~~~

이 Policy는 Agent Prompt에만 두지 않는다.

Control Plane이 소유하는 편이 좋다.

---

## 다음 질문

Retry와 Resume를 설계했어도 한 가지 어려운 문제가 남는다.

외부 API 호출이 실제로 성공했는데 응답만 유실되면 어떻게 할까.

PR을 이미 만들었는데 Runtime이 그 사실을 모르고 다시 Create하면 어떻게 할까.

Human Approval을 하루 동안 기다리는 동안 Worker를 계속 붙잡고 있어야 할까.

다음 장에서는 Long-running Work를 현실의 Crash와 Wait에서 살아남게 만드는 **Durable Execution**을 다룬다.

---

## 참고 자료

- Anthropic, *Effective harnesses for long-running agents*  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Microsoft, *Durable Task for AI agents*  
  https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents
- *Wink: Recovering from Misbehaviors in Coding Agents*  
  https://arxiv.org/abs/2602.17037
- Anthropic, *Patterns and problems in emerging multiagent systems*  
  https://www.anthropic.com/research/multiagent-systems
