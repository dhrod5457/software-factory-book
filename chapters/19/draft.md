# 19장. Observability와 Metrics: 무엇을 측정할 것인가

Factory를 운영하기 시작하면 곧 숫자가 쌓인다.

- Agent 실행시간
- Token
- Tool Call
- Worker 사용률
- Test 결과
- Pull Request 수

문제는 이 숫자들이 많다고 Factory 상태를 이해할 수 있는 것은 아니라는 점이다.

예를 들어 Agent 실행시간이 절반으로 줄었다.

좋은 변화처럼 보인다.

그런데 Review Queue가 두 배로 늘고 Revert가 증가했다면 전체 Delivery는 좋아지지 않았을 수 있다.

Factory Observability의 목적은 Agent를 감시하는 것이 아니다.

> Work가 어디에서 멈추고, 어떤 비용과 실패를 거쳐, 얼마나 많은 Human Attention을 사용해 Accepted Change가 되는지 보는 것이다.

---

## 19.1 무엇을 관찰할 것인가

Factory Observability는 여러 Layer를 가진다.

### Task

~~~text
created
ready
assigned
running
verifying
awaiting_human
done
failed
~~~

### Attempt

~~~text
attempt_id
worker
model
start/end
retry_reason
failure_class
~~~

### Worker

~~~text
active
idle
lost
resource
profile
~~~

### Agent / Harness

~~~text
turns
tool_calls
context_compaction
model_switch
~~~

### Execution

~~~text
commands
exit_code
wall_time
cpu
memory
~~~

### Verification

~~~text
checks
pass/fail
duration
artifact
~~~

### Human

~~~text
steering
review
approval
rejection
takeover
~~~

### Cost

~~~text
model
compute
sandbox
CI
storage
review
rework
~~~

이 Layer들을 구분하면 Failure가 어디에서 생겼는지 더 정확히 볼 수 있다.

---

## 19.2 Raw Chain-of-Thought가 Observability의 중심은 아니다

Factory를 관찰한다고 Agent의 내부 Reasoning 전체를 저장해야 하는 것은 아니다.

운영에 더 중요한 것은 externally observable event다.

예:

~~~text
TaskAssigned
ToolInvoked
VerificationFailed
RetryScheduled
ApprovalRequested
WorkerLost
TaskDone
~~~

이 이벤트만으로도 많은 질문에 답할 수 있다.

- 왜 Task가 늦었는가
- 어떤 Tool이 반복 실패했는가
- Human Wait가 얼마나 길었는가
- 같은 Failure가 몇 번 반복됐는가

내부 Reasoning Transcript를 Audit Source of Truth로 삼지 않는다.

---

## 19.3 Task Timeline을 쪼개서 본다

Task가 10시간 걸렸다고 하자.

이 숫자만으로는 원인을 알 수 없다.

다음처럼 나눌 수 있다.

~~~text
READY              30m
RUNNING             12m
VERIFYING            8m
AWAITING_HUMAN       8h
RETRY               20m
DONE
~~~

Total Cycle Time은 길지만 Agent 실행은 짧다.

이 경우 병목은 Model이 아니다.

Human Wait다.

다른 Task는 반대일 수 있다.

~~~text
READY                1m
RUNNING              4h
VERIFYING            5m
DONE
~~~

여기서는 Agent/Harness/Task Size를 봐야 한다.

따라서 다음 시간을 분리한다.

~~~text
Queue Time
Execution Time
Verification Time
Human Wait
Retry / Rework
Total Cycle Time
~~~

---

## 19.4 Agent Metric과 Factory Metric을 구분한다

Agent-level Metric:

- Task success
- Token
- Turns
- Tool Calls
- Eval Score

Factory-level Metric:

- Cycle Time
- First-pass Acceptance
- Retry
- Review Wait
- Revert
- Escaped Defect
- Intervention
- Cost per Accepted Change

Business-level Metric:

- Feature Adoption
- Reliability
- Support Volume
- Revenue / Cost

계층을 섞지 않는다.

~~~text
Agent Efficiency
        ↓
Team Flow
        ↓
Delivery Performance
        ↓
Business Outcome
~~~

한 단계 개선이 다음 단계 개선을 보장하지 않는다.

---

## 19.5 First-pass Acceptance

Agent가 Candidate를 많이 만드는 것보다 실제로 얼마나 적은 수정으로 받아들여지는지가 중요할 수 있다.

예:

~~~text
100 Proposed Changes

60 accepted without edit
20 accepted after human edit
10 rejected
10 abandoned
~~~

이 데이터는 단순 PR Count보다 더 많은 정보를 준다.

특히 다음 지표가 유용하다.

~~~text
First-pass Acceptance Rate
~~~

Retry가 많고 Human Edit가 크다면 Agent output throughput은 높아도 Factory efficiency는 낮을 수 있다.

---

## 19.6 Human Attention

Agent가 비동기로 일할수록 Human Time을 따로 봐야 한다.

후보:

- steering minutes
- review minutes
- approval wait
- intervention count
- takeover count

개념적으로 다음 Metric을 생각할 수 있다.

~~~text
Human Attention
----------------
Accepted Change
~~~

표준 지표는 아니다.

하지만 Factory가 실제로 사람의 반복적인 Attention을 줄이고 있는지 보는 데 도움이 된다.

---

## 19.7 Token을 비용과 생산성의 대리변수로 쓰지 않는다

Agent A:

~~~text
tokens: low
retries: 4
human fix: 30 min
~~~

Agent B:

~~~text
tokens: high
retries: 0
human fix: 2 min
~~~

Token만 보면 A가 더 싸다.

전체 비용은 다를 수 있다.

~~~text
Total Cost
=
Model
+ Compute
+ Sandbox
+ CI
+ Review
+ Retry
+ Rework
~~~

그래서 하나의 후보로 다음을 사용할 수 있다.

~~~text
Cost per Accepted Change
~~~

완벽한 Metric은 아니다.

Task Value와 Risk가 다르기 때문이다.

하지만 Cost per Token이나 Cost per Attempt보다 Factory 수준에 가깝다.

---

## 19.8 Benchmark와 Production Metric을 분리한다

SWE-bench 같은 Benchmark는 중요하다.

Model/Harness의 Capability를 비교하고 Regression을 찾을 수 있다.

하지만 실제 Factory에는 Benchmark에 없는 요소가 있다.

- 조직의 Repository
- 실제 Dependency
- Human Review
- CI Queue
- Permission
- Security Gate
- Production Failure
- Cost

그래서 다음 등식은 성립하지 않는다.

~~~text
Benchmark Score
=
Production Capability
~~~

Benchmark는 Signal이다.

Production Metric은 실제 Work Distribution을 보여준다.

둘 다 필요하다.

---

## 19.9 Production Failure를 Eval로 되돌린다

Observability의 가장 큰 가치는 Dashboard가 아니라 Learning Loop에 있다.

예:

~~~text
Production Failure
→ Failure Class
→ Eval Case
→ Harness / Tool Fix
→ Regression Test
→ Deploy
~~~

같은 문제가 반복되면 Factory 자체를 개선할 수 있다.

예:

- 특정 Context가 항상 누락된다.
- Browser Worker가 stale state를 남긴다.
- Agent가 같은 Test를 반복한다.
- Reviewer가 같은 Comment를 남긴다.

이 정보는 Skill, Tool, Documentation, Policy 개선으로 이어질 수 있다.

---

## 19.10 Minimum Viable Dashboard

처음부터 거대한 Observability Platform이 필요하지는 않다.

최소 Dashboard는 다음 질문에 답하면 된다.

### Flow

~~~text
Backlog
Ready
Running
Blocked
Awaiting Human
Done
Failed
~~~

### Worker

~~~text
Active
Idle
Lost
~~~

### Quality

~~~text
Verification Pass
Retry
Reject
Revert
~~~

### Human Load

~~~text
Review Queue
Approval Wait
Intervention
~~~

### Cost

~~~text
Task Cost
Accepted-change Cost
~~~

이 정도만 있어도 운영 개선을 시작할 수 있다.

---

## 예: 10분 실행, 8시간 Review Wait

Task A:

~~~text
Agent execution: 10m
Verification: 5m
Review wait: 8h
Review: 10m
~~~

Model을 20% 빠르게 바꿔도 End-to-End 개선은 거의 없다.

오히려 Review Queue를 줄이는 것이 더 효과적일 수 있다.

Task B:

~~~text
Agent execution: 2h
Retry: 3
Review wait: 5m
~~~

여기서는 Task Specification, Harness, Model, Failure Recovery를 봐야 한다.

Observability가 있어야 두 문제를 구분할 수 있다.

---

## 19.11 Factory Metric Set

초기에는 다음 정도면 충분하다.

~~~text
Flow
- cycle_time
- queue_time
- execution_time
- verification_time
- human_wait

Quality
- first_pass_acceptance
- retry
- reject
- revert

Human
- intervention_count
- review_minutes

Cost
- task_cost
- accepted_change_cost
~~~

Factory가 커지면 더 추가한다.

Metric은 측정 가능한 것을 많이 모으기 위해 만드는 것이 아니다.

**운영 결정을 바꾸기 위해 만든다.**

---

## 다음 질문

Factory가 충분히 관찰되기 시작하면 새로운 가능성이 생긴다.

사람이 매번 Task를 직접 만들지 않아도 CI Failure, Vulnerability, Production Signal이 Work Source가 될 수 있다.

하지만 Alert를 곧바로 Agent Action으로 연결하면 위험하다.

다음 장에서는 **Event-driven Factory와 Closed-loop SDLC**를 다룬다.

---

## 참고 자료

- DORA, *2025 DORA Report*  
  https://dora.dev/research/2025/dora-report/
- Microsoft Research, *Agentic Coding in the Wild*  
  https://www.microsoft.com/en-us/research/publication/agentic-coding-in-the-wild-characterizing-github-copilot-at-production-scale/
- GitHub, *How we make AI coding more cost-efficient without sacrificing task quality*  
  https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/
- Anthropic, *Demystifying evals for AI agents*  
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
