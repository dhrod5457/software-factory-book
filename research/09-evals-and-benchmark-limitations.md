# Evals and Benchmark Limitations

기준일: 2026-09-28

AI Software Factory 책에서 benchmark는 중요하지만 중심 목표는 아니다.

이 문서의 목적:

- agent capability 측정
- harness 비교
- regression
- 실제 Factory performance

를 구분한다.

## 1. SWE-bench

SWE-bench는 실제 GitHub issue 기반 software engineering task를 agent가 수정하고 test로 평가하는 대표 benchmark다.

중요한 기여:

- repository-level
- executable verification
- real issue style
- agent tool use

하지만 실제 조직 workflow 전체를 측정하지 않는다.

## 2. SWE-bench Verified

500개 human-validated task subset.

검증:

- problem clarity
- test correctness
- solvability

출처:

- https://www.swebench.com/verified.html

## 3. Benchmark Saturation / Contamination

Frontier coding agent 성능이 빠르게 올라가면서 benchmark 자체의 분별력이 줄어들 수 있다.

문제:

- training contamination
- known solutions
- repeated optimization against benchmark
- test artifacts

따라서 score 상승을 그대로 "실제 engineering autonomy" 상승으로 보면 안 된다.

## 4. SWE-bench Pro 문제

OpenAI는 2026-07 SWE-Bench Pro를 상세 audit하고 약 30% task에 심각한 문제 가능성이 있다고 보고했다.

문제 유형:

- prompt에 없는 구현을 요구하는 strict tests
- underspecified prompt
- low-coverage tests
- misleading prompt

출처:

- https://openai.com/index/separating-signal-from-noise-coding-evaluations/

## 5. SWE-Bench Pro Verified

2026-09 연구에서는:

- reward hacking
- hidden evaluation leakage
- task quality issue

를 보완한 verified variant가 제안되었다.

출처:

- https://arxiv.org/abs/2609.08149

이 자료는 최신 연구이므로 후속 peer review/업데이트를 계속 확인한다.

## 6. Terminal-Bench

Terminal environment에서 end-to-end technical task를 평가.

장점:

- command
- package
- build
- environment interaction

단 infra configuration 영향을 크게 받을 수 있다.

## 7. Infrastructure Noise

Anthropic 실험:

동일 model/harness에서도 resource configuration이 결과에 영향을 준다.

요인:

- RAM
- CPU
- hard limit
- runtime kill
- time
- cluster error

핵심:

```text
Observed Benchmark Score
= Model
+ Harness
+ Environment
+ Infrastructure
+ Task Quality
+ Randomness
```

즉 leaderboard 소수점 차이를 과신하지 않는다.

출처:

- https://www.anthropic.com/engineering/infrastructure-noise

## 8. Evals for Agent System

Anthropic의 Agent Eval 정의:

- Task
- Trial
- Grader
- Transcript/Trace

Grader:

### Code-based

- test
- static analysis
- exact check

### Model-based

- rubric
- quality
- instruction following

### Human

- calibration
- subjective quality
- safety

좋은 eval은 하나의 grader만 쓰지 않을 수 있다.

출처:

- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

## 9. Multiple Trials

Agent output은 non-deterministic하다.

따라서:

```text
1 Task × 1 Run
```

만으로 system quality를 판단하지 않는다.

가능하면:

- pass@1
- repeated trials
- variance
- confidence

를 고려한다.

## 10. Task Difficulty Calibration

너무 쉬운 eval:

모델 차이를 못 봄.

너무 어려운 eval:

모두 실패.

Factory 내부 eval은 실제 production task distribution에서 failure를 모아 점진적으로 난이도를 올리는 것이 유용하다.

Anthropic은 초기에는 20~50 real failure case부터 시작하는 것도 가능하다고 설명한다.

## 11. Eval과 Acceptance Test

구분:

```text
Eval:
Agent/Factory가 전반적으로 좋은가?

Acceptance:
이번 Task 결과가 요구사항을 만족하는가?
```

동일한 test case 형식을 사용할 수 있어도 목적이 다르다.

## 12. METR Time Horizon

METR는 human expert가 걸리는 시간 기준으로 model/agent가 task를 성공할 가능성이 있는 horizon을 추적한다.

Factory에서 유용한 질문:

- single agent horizon
- decomposition 후 system horizon
- retry/evaluator 포함 horizon

을 구분할 수 있는가?

출처:

- https://metr.org/time-horizons/

## 13. Factory-level Evaluation

단일 agent benchmark를 넘어 다음 scenario가 필요하다.

### Recovery

- worker kill
- restart
- resume

### Reassignment

- Worker A partial
- Worker B continuation

### Dependency

- A 완료 후 B unlock

### Approval

- dangerous action blocks

### Parallel

- multiple independent tasks

### Conflict

- same file overlap

### Verification

- false completion caught

### Security

- prompt injection
- secret exfiltration
- protected resource

### Observability

- trace/evidence completeness

## 14. Long-running Software Task Evaluation

Factory.ai 2026 large-software-task 연구는 단순 specification만으로는 "done"이 무엇인지 충분하지 않을 수 있다고 지적한다.

큰 software task는:

- 실행
- inspection
- comparison
- behavior check

까지 completion standard가 필요하다.

출처:

- https://factory.ai/news/what-it-takes-for-coding-agents-to-complete-large-software-tasks

## 15. Benchmark와 실제 조직의 Gap

Benchmark에서 빠지는 요소:

- ambiguous requirement
- changing requirement
- multiple repos
- ownership
- legacy env
- VPN
- deployment
- compliance
- code review
- approval
- incident
- coordination
- customer feedback
- long-term maintainability

따라서 책에서는 benchmark를 "Factory가 가능한가"의 단독 근거로 사용하지 않는다.

## 16. 내부 Eval Suite 후보

### Agent Capability

- bug fix
- test
- refactor
- feature

### Harness Capability

- tool use
- context retrieval
- long log
- browser

### Factory Reliability

- crash
- retry
- resume
- reassignment

### Quality

- functional
- regression
- security
- maintainability

### Policy

- forbidden operation
- secret
- approval

### Economics

- latency
- tokens
- compute
- cost per accepted result

## 17. 핵심 후보 메시지

> AI Software Factory는 모델 benchmark score가 높은 시스템이 아니라 실제 조직 Task를 반복적으로, 검증 가능하게, 복구 가능하게 처리하는 시스템이다.

> Agentic benchmark는 end-to-end system test에 가까워지고 있으며 model과 infrastructure를 완전히 분리하기 어렵다.

> Factory를 평가하려면 happy path뿐 아니라 crash, retry, reassignment, approval, security를 포함해야 한다.
