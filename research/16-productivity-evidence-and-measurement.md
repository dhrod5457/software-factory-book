# Productivity Evidence and Measurement

기준일: 2026-09-28

AI coding productivity에 대해서는 서로 다른 결론의 자료가 존재한다.

이것은 모순이라기보다:

- 시점
- 모델
- Task
- developer expertise
- workflow
- metric

이 다르기 때문이다.

Software Factory 책에서는 하나의 "생산성 향상 %"를 찾지 않는다.

---

## 1. Microsoft / Accenture / Fortune 100 RCT

2025 Microsoft Research publication은 세 회사의 randomized field experiments를 통합 분석했다.

- 4,867 developers
- AI coding assistant access
- completed tasks 기준

통합 결과에서는 AI tool 사용군의 completed tasks가 평균적으로 더 높게 관찰됐다.

보고값:

- 약 26% 증가
- less experienced developer가 더 높은 adoption / gain 경향

중요:

이 연구는 주로 code-completion assistant 시기의 자료이며 2026 asynchronous agent factory와 동일한 workflow는 아니다.

출처:

- https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/

---

## 2. METR 2025 RCT - Experienced OSS Developers

METR는 숙련된 open-source developer 16명이 자기 repository의 실제 task를 수행하도록 randomized study를 했다.

결과:

- AI 사용 시 평균적으로 작업 시간이 19% 증가
- 개발자 본인은 AI가 약 20% 빠르게 했다고 인식

중요한 점:

- early-2025 tools
- mature repository
- highly experienced developer
- 평균 약 2시간 task

이 결과를 2026 agent tool에 그대로 일반화하면 안 된다.

그러나 중요한 교훈:

> Perceived productivity와 measured productivity가 다를 수 있다.

출처:

- https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/

---

## 3. METR 2026 Follow-up - Measurement Itself Became Harder

METR는 late-2025 tools를 대상으로 후속 RCT를 시도했지만 methodology issue 때문에 결과 신뢰성이 낮다고 판단했다.

주요 이유:

- AI 없이 일하기 싫어하는 developer가 study 참여를 거부
- selection bias
- 여러 agent를 동시에 사용하면서 task-level time 측정 어려움

중요한 변화:

> Agentic workflow는 한 개발자-한 Task-한 stopwatch 방식의 생산성 측정을 깨뜨린다.

출처:

- https://metr.org/blog/2026-02-24-uplift-update/

---

## 4. Old Tasks vs New Tasks vs Value

METR는 productivity uplift를 최소 세 가지로 구분한다.

### Uplift on old tasks

AI 이전에 하던 일을 얼마나 빨리 하는가.

### Uplift on new tasks

AI가 있으므로 새롭게 하게 된 Task를 얼마나 싸게 할 수 있는가.

### Uplift in value

Task mix 자체가 변한 뒤 총 value가 얼마나 달라졌는가.

이 distinction은 Software Factory에서 매우 중요하다.

Factory가 가치가 있었던 이유가:

- 기존 작업을 빠르게 함

뿐 아니라:

- 예전에는 비용 때문에 안 하던 test/documentation/refactoring을 수행

하는 것일 수 있다.

출처:

- https://metr.org/blog/2026-05-08-task-substitution-and-uplift/

---

## 5. Self-reported 2026 Uplift

METR는 349 technical workers 설문에서 AI 사용으로 인한 value uplift를 조사했다.

median self-report:

- value: 약 1.4~2x
- speed: 더 높은 수치

그러나 METR 자신도:

- convenience sample
- selection bias
- quantitative self-report difficulty

를 명확히 지적한다.

따라서 book에서는 perception evidence로만 사용한다.

출처:

- https://metr.org/blog/2026-05-11-ai-usage-survey/

---

## 6. Factory Productivity는 개인 생산성과 다르다

예:

```text
Developer coding time -50%
but
Review queue +200%
CI queue +300%
Defect +20%
```

이면 조직 throughput 개선은 제한적일 수 있다.

따라서 측정 hierarchy:

```text
Agent Efficiency
↓
Developer Productivity
↓
Team Flow
↓
Delivery Performance
↓
Business Value
```

각 단계는 동일하지 않다.

---

## 7. DORA의 System-level Perspective

DORA는 AI가 기존 organization system의 강점과 약점을 증폭한다고 본다.

AI code production이 증가해도:

- review
- testing
- security
- deployment

이 bottleneck이면 전체 delivery gain이 제한된다.

출처:

- https://dora.dev/research/2025/dora-report/
- https://dora.dev/insights/balancing-ai-tensions/

---

## 8. Agent Throughput와 Human Attention

OpenAI Symphony에서는 individual engineer가 interactive coding-agent session을 여러 개 관리하면서 human attention/context switching이 bottleneck이 됐다고 설명한다.

따라서 Factory의 productivity metric에는:

- concurrent agent count

보다:

- human attention per accepted task

가 더 중요할 수 있다.

출처:

- https://openai.com/index/open-source-codex-orchestration-symphony/

---

## 9. Production-scale Agent Workload

Microsoft Research는 2026년 6월 GitHub Copilot production trace를 분석했다.

규모:

- 3.2M users
- 13M sessions
- 761M LLM calls
- 95T tokens

관찰:

- user turn 사이 idle time
- 한 user turn 안에서 여러 LLM/tool loop
- 매우 long-tailed token/tool usage
- context compaction/model switch가 cache behavior에 영향

이것은 agent runtime을 일반 chat serving과 동일하게 최적화하면 안 된다는 근거다.

출처:

- https://www.microsoft.com/en-us/research/publication/agentic-coding-in-the-wild-characterizing-github-copilot-at-production-scale/

---

## 10. Token Cost는 매우 가변적

Microsoft Research 2026 study는 SWE-bench Verified agent trajectories를 분석했다.

주요 보고:

- agentic coding task가 매우 많은 token 소비
- 같은 task도 run에 따라 token 사용량 차이 큼
- 더 많은 token이 항상 더 높은 accuracy로 연결되지 않음
- model이 자기 token cost를 사전 예측하는 능력도 제한적

Factory implication:

```text
Fixed Token Budget
보다는
Budget + Progress + Outcome
```

기반 control이 필요할 수 있다.

출처:

- https://www.microsoft.com/en-us/research/publication/how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks/

---

## 11. Efficiency를 Token으로만 측정하지 않는다

GitHub는 2026년 coding agent efficiency 글에서 token count 단독 최적화가 잘못될 수 있다고 설명한다.

너무 짧은 tool output:

- 추가 call 증가
- 필요한 context 누락
- total work 증가

목표:

> Complete the task efficiently, not minimize every individual interaction.

출처:

- https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/

---

## 12. Recommended Metric Set

### Task Flow

- cycle time
- queue time
- execution time
- verification time
- approval wait
- total completion

### Human Cost

- steering minutes
- review minutes
- intervention count
- takeover count

### Quality

- first-pass acceptance
- retry
- reject
- revert
- escaped defects

### Cost

- model
- compute
- CI
- sandbox
- storage
- review
- rework

### Value

- accepted change
- shipped feature
- defect resolved
- maintenance removed

---

## 13. Core Economic Metric Candidate

```text
Cost per Accepted Change
```

구성:

```text
(model + compute + review + retry + CI + rework)
/
accepted production-quality changes
```

이 metric도 완벽하지 않지만 token/unit보다 Factory-level에 가깝다.

---

## 14. Human Attention per Accepted Change

Software Factory의 핵심 목적 후보:

```text
Human Attention
----------------
Accepted Change
```

을 낮추는 것.

Human을 제거하는 것이 아니라:

- routine steering
- environment setup
- repetitive validation

을 줄이고 high-value decision으로 집중한다.

---

## 15. Latency vs Throughput

### Latency

한 Task가 얼마나 빨리 끝나는가.

### Throughput

단위 시간에 얼마나 많은 independent accepted work가 처리되는가.

Cloud/asynchronous agent의 장점은 latency보다 throughput에 있을 수 있다.

---

## 16. Parallelism Efficiency

```text
Useful Parallelism
= parallel completed tasks
- conflict
- duplicate work
- review overload
- repeated context
```

Agent count 자체는 metric이 아니다.

---

## 17. New Work Creation

AI 때문에 새롭게 가능해진 work도 측정한다.

예:

- 추가 tests
- docs update
- dependency maintenance
- migration validation
- screenshot QA
- accessibility audit
- log investigation

기존 backlog 처리량만 측정하면 Factory value를 과소평가할 수도 있다.

---

## 18. Measurement Principle

책에서는 "AI는 개발자를 X% 빠르게 한다"는 단일 문장을 피한다.

대신:

> AI의 생산성 효과는 개발자, Task, workflow, measurement boundary에 따라 크게 다르며, Software Factory에서는 individual coding speed보다 accepted work의 end-to-end flow를 측정해야 한다.

---

# 핵심 후보 메시지

> 생산성은 Agent가 얼마나 빨리 타이핑하는지가 아니라 사람이 더 적은 주의를 사용하면서 더 많은 검증된 변경을 전달할 수 있는지로 봐야 한다.

> Agentic workflow에서는 Task mix 자체가 바뀌기 때문에 기존 시간 절약 지표만으로 가치를 측정하기 어렵다.

> Factory의 경제성을 측정하려면 token cost뿐 아니라 review, compute, retry, verification, rework를 함께 봐야 한다.
