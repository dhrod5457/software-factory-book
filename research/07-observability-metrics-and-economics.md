# Observability, Metrics, and Economics

기준일: 2026-09-28

AI Software Factory를 평가할 때 가장 위험한 실수는 다음이다.

```text
Agent가 코드를 많이 만들었다
= Factory 생산성이 높다
```

이 등식은 성립하지 않는다.

Factory는 전체 value stream과 quality까지 측정해야 한다.

## 1. Observability의 대상

일반 software observability와 agent observability는 겹치지만 동일하지 않다.

Factory에서 기록할 후보:

### Task

- created
- ready
- assigned
- started
- verified
- approved
- done
- failed

### Attempt

- attempt ID
- worker
- model
- start/end
- retry reason

### Agent

- turns
- tool calls
- subagents
- context compaction
- tokens
- model switch

### Execution

- commands
- exit code
- CPU
- RAM
- wall time
- sandbox events

### Verification

- tests
- failures
- artifacts
- evaluator result

### Human

- steering count
- review time
- approval
- rejection
- takeover

## 2. Trace가 필요하다

OpenAI Agents API는:

- session event stream
- saved history
- turns
- subagent activity
- tool calls
- token usage
- trace export

를 제공한다.

이런 정보는 debugging뿐 아니라 Factory 개선에 필요하다.

출처:

- https://developers.openai.com/api/docs/guides/agents-api/observability
- https://developers.openai.com/api/docs/guides/agents-api/tracing

## 3. Factory.ai의 Observability 정의

Factory.ai는 Software Factory architecture에서 observability/replayability를 일곱 번째 component로 둔다.

기록 대상:

- input
- prompt
- model version
- tool call
- output
- full trace

그리고 trace를:

- audit
- reproduction
- eval
- benchmark

입력으로 본다.

출처:

- https://factory.ai/articles/what-is-a-software-factory-architecture

## 4. DORA: AI는 시스템을 증폭한다

DORA 2025의 주요 관점:

> AI의 효과는 개별 도구보다 조직의 기존 delivery system quality에 크게 좌우된다.

특히:

- AI는 initial code generation을 빠르게 할 수 있음
- 절약된 시간이 audit/verification으로 이동 가능
- 높은 AI adoption은 throughput 증가와 instability 증가가 동시에 나타날 수 있음
- platform quality가 낮으면 individual productivity gain이 downstream bottleneck에 흡수될 수 있음

출처:

- https://dora.dev/research/2025/dora-report/
- https://dora.dev/insights/balancing-ai-tensions/
- https://dora.dev/capabilities/platform-engineering/

## 5. Factory Metric은 Agent Metric보다 위에 있어야 한다

### Agent metric

- task success
- tokens
- turns
- command count
- eval score

### Factory metric

- cycle time
- lead time
- merge rate
- rollback
- escaped defect
- review load
- blocked time
- cost per accepted change
- developer intervention
- incident rate

### Business metric

- feature adoption
- customer outcome
- revenue/cost
- reliability
- support volume

한 단계 metric을 다음 단계 결과와 혼동하지 않는다.

## 6. Developer Blocking Time

Agent runtime이 40분이어도 human이 40분 기다린 것은 아닐 수 있다.

분리:

```text
Agent Execution Time
Human Blocking Time
Human Review Time
Total Task Cycle Time
```

비동기 Factory의 가치는 raw execution speed보다 human attention 절약에 있을 수 있다.

OpenAI Symphony도 여러 agent session을 사람이 직접 관리할 때 context switching이 병목이 되었다고 설명한다.

출처:

- https://openai.com/index/open-source-codex-orchestration-symphony/

## 7. Human Intervention Rate

중요 metric 후보:

```text
Interventions / Completed Tasks
```

세부:

- question
- steering
- approval
- manual fix
- takeover
- retry trigger

단 intervention이 낮다고 무조건 좋은 것은 아니다.

위험 task에서는 적절한 gate가 필요하다.

## 8. Acceptance Rate

Agent가 만든 PR 수보다:

```text
Accepted Changes / Proposed Changes
```

가 중요하다.

추가 후보:

- accepted without edits
- accepted with human edits
- rejected
- abandoned
- reverted

## 9. Cost per Accepted Change

AI 비용을 token만으로 측정하지 않는다.

```text
Total Cost
= Model
+ Compute
+ Sandbox
+ CI
+ Storage
+ Review
+ Retry
+ Failure/Rework
```

핵심:

```text
Cost per Attempt
보다
Cost per Accepted Change
```

가 유용하다.

## 10. Model Routing

Factory.ai는 production Droid routing에서 frontier model 고정 대비 aggregate cost를 58% 줄였다고 자체 보고한다.

중요한 architecture claim:

- gateway는 개별 completion만 봄
- harness는 task/session history와 outcome을 봄
- model routing은 harness가 더 많은 context를 가짐

이 수치는 Factory.ai 내부 결과이므로 일반화하지 않는다.

출처:

- https://factory.ai/news/model-routing-belongs-in-the-harness

## 11. Throughput Trap

Agent throughput이 크게 증가하면 병목이 이동한다.

가능한 다음 병목:

- code review
- CI
- integration test
- QA
- release
- product acceptance

즉:

```text
Coding bottleneck solved
→ Review bottleneck
→ Verification bottleneck
→ Integration bottleneck
```

Factory는 병목을 전체 system에서 관찰해야 한다.

## 12. Benchmark Score를 Factory Metric으로 쓰지 않는다

SWE-bench 같은 benchmark는 model/agent capability 비교에는 유용하지만 조직 생산성을 직접 측정하지 않는다.

특히:

- task distribution 다름
- infra 다름
- context 다름
- review 과정 없음
- organizational dependency 없음
- security/gate 없음

## 13. Infrastructure Noise

Anthropic은 agentic coding eval에서 infrastructure configuration이 score에 영향을 줄 수 있음을 보였다.

예:

- CPU
- RAM
- kill threshold
- time limit
- egress
- cluster reliability

Terminal-Bench 실험에서는 resource setup에 따라 차이가 leaderboard gap보다 클 수 있었다.

핵심:

> Agent benchmark는 model만 측정하는 것이 아니라 harness + environment를 함께 측정할 수 있다.

출처:

- https://www.anthropic.com/engineering/infrastructure-noise

## 14. Evals와 Production Metrics 연결

Eval:

- controlled
- repeatable
- regression detection

Production:

- real task distribution
- real users
- real infra
- unexpected failures

좋은 Factory 개선:

```text
Production Failure
→ Failure Class
→ Eval Case
→ Harness/Tool Fix
→ Regression Suite
→ Deploy
```

Anthropic agent eval guide도 실제 failure에서 20~50 task 정도로 시작할 수 있다고 권장한다.

출처:

- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

## 15. Factory Dashboard 후보

### Flow

- backlog
- ready
- running
- blocked
- awaiting human
- done

### Worker

- active
- idle
- lost
- utilization

### Quality

- verification pass
- retry
- rejection
- revert
- defect

### Human Load

- review queue
- approval wait
- intervention

### Cost

- token
- compute
- task cost
- accepted-change cost

### Reliability

- worker loss
- resume success
- orchestration error
- infra error

## 16. 핵심 후보 메시지

> AI Software Factory가 최적화해야 할 대상은 Token이나 PR 수가 아니라 검증된 소프트웨어 변경이 사용자에게 도달하는 전체 흐름이다.

> Agent가 빨라질수록 병목은 downstream으로 이동한다.

> Factory의 성능은 모델 성능과 infrastructure/harness 성능을 분리해서 측정해야 한다.
