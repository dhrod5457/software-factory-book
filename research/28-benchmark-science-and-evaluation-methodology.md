# Benchmark Science and Evaluation Methodology for Software Engineering Agents

기준일: 2026-09-28

Agentic Software Engineering 발전 속도가 빨라지면서 benchmark 자체가 engineering research 대상이 되고 있다.

이 문서는 특정 leaderboard가 아니라 **어떻게 Agent/Factory를 제대로 평가할 것인가**를 정리한다.

---

# 1. SWE-bench의 공헌과 한계

SWE-bench는 real GitHub issue + repository + test를 결합해 repository-level coding agent evaluation의 기반을 만들었다.

큰 공헌:

- snippet code generation을 넘어감
- environment interaction
- real repository
- executable grading

하지만 이후 문제:

- contamination
- flawed tests
- binary outcome
- task quality

가 드러났다.

따라서 하나의 benchmark에 의존하지 않는다.

---

# 2. SWE-Lancer: Economic / Managerial Task

ICML 2025 SWE-Lancer:

- 1,400+ freelance SWE tasks
- 실제 payout 총액 약 $1M
- $50 bug fix부터 $32,000 feature까지
- managerial proposal selection 포함
- end-to-end test를 experienced SWE가 triple verification

출처:

- https://proceedings.mlr.press/v267/miserendino25a.html
- https://arxiv.org/abs/2502.12115

Factory 연결:

Software Factory는 coding task뿐 아니라:

- technical judgment
- proposal selection

도 평가해야 한다.

---

# 3. Agent Eval은 Accuracy + Cost를 함께 봐야 한다

AI Agents That Matter는 agent benchmark의 문제를 지적한다.

핵심:

- accuracy만 보고 cost 무시
- 단순 repeated baseline이 복잡한 agent보다 cost/accuracy에서 나을 수 있음
- holdout 부족
- benchmark overfitting
- reproducibility 부족

출처:

- AI Agents That Matter
  - TMLR 2025
  - https://arxiv.org/abs/2407.01502

Factory 연결:

```text
Best Accuracy
!=
Best Production System
```

---

# 4. SWE-smith: Training Task Generation

SWE-smith는 real codebase에서 software engineering training task를 자동 생성한다.

- 128 repositories
- 약 50k instances

아이디어:

기존 test를 깨뜨리는 mutation을 만들어 task를 생성.

출처:

- https://arxiv.org/abs/2504.21798

Factory 연결:

내부 조직에서도 production bug / mutation / historical patch에서 Eval Task를 자동 생성할 수 있는 가능성을 보여준다.

---

# 5. SWE-rebench: Fresh / Decontaminated Evaluation

SWE-rebench:

- 21,000+ interactive Python SWE tasks
- automated pipeline
- fresh GitHub task 공급
- contamination-free evaluation 목표

연구는 일부 model의 SWE-bench Verified 성능이 contamination 때문에 부풀려질 가능성을 보여준다.

출처:

- https://arxiv.org/abs/2505.20411

Factory 연결:

Static Eval Suite만 유지하면 Agent가 개선된 것인지 benchmark familiarity가 증가한 것인지 분리하기 어렵다.

---

# 6. Dialogue SWE-Bench: Human Interaction Evaluation

기존 benchmark:

```text
Task given
→ fully autonomous
→ result
```

Dialogue SWE-Bench:

```text
Task
↔ User dialogue
→ clarification / collaboration
→ result
```

출처:

- https://arxiv.org/abs/2606.13995

Factory 연결:

Human-in-the-loop workflow를 평가하려면 autonomous benchmark만으로 부족하다.

---

# 7. SWE-Explore: Repository Exploration Evaluation

최종 patch가 아니라:

- relevant code coverage
- ranking
- context efficiency

를 평가.

출처:

- https://arxiv.org/abs/2606.07297

Factory 연결:

Agent pipeline의 subsystem을 분해해 eval할 수 있다.

---

# 8. RACE-Bench: Intermediate Reasoning / Feature Addition

RACE-Bench는 feature addition task에:

- issue understanding
- file localization
- implementation task
- step decomposition

같은 structured intermediate reference를 추가한다.

출처:

- https://arxiv.org/abs/2603.26337

Factory 연결:

Outcome failure만 보면 어디가 실패했는지 알 수 없다.

```text
Task Failure
→ Requirement?
→ Localization?
→ Plan?
→ Implementation?
→ Verification?
```

diagnostic eval이 필요하다.

---

# 9. Benchmark Unit은 Model이 아닐 수 있다

2026 RuBench 연구는 deployed product configuration을 평가하면서 실제 제품이 일부 Task에서 requested model 대신 다른 model로 fallback한 사례를 audit했다.

저자의 핵심 관점:

> 실제 사용자는 Model이 아니라 Product Configuration을 사용한다.

출처:

- https://arxiv.org/abs/2607.06411

Factory 연결:

평가 단위 후보:

```text
Model
vs
Agent Harness
vs
Product Config
vs
Factory
```

명확히 구분한다.

---

# 10. Performance Benchmark도 Infrastructure Sensitive

2026 performance optimization benchmark audit는:

- machine variance
- scoring rule
- reference patch

에 따라 ranking이 흔들릴 수 있음을 보였다.

출처:

- https://arxiv.org/abs/2607.01211

Factory 연결:

성능 benchmark 결과는 execution environment와 함께 기록해야 한다.

---

# 11. Process Quality도 평가 대상

RigorBench(ASE 2026 TRUST)는 outcome-only coding benchmark의 한계를 문제 삼는다.

연구 관점:

정답을 냈더라도:

- reckless trial-and-error
- planning 없음
- verification 없음
- recovery 없음

이면 reliable engineering agent라고 보기 어렵다.

출처:

- ASE 2026 TRUST
  - RigorBench: Benchmarking Engineering Process Discipline in Autonomous AI Coding Agents
  - https://conf.researchr.org/details/ase-2026/trust-2026-papers/4/

Factory 연결:

Task result 외에 trajectory discipline을 측정할 필요가 있다.

---

# 12. Factory-level Eval Matrix

## Specification

- ambiguity detection
- requirement completeness
- acceptance quality

## Exploration

- localization
- context efficiency

## Planning

- dependency
- decomposition

## Execution

- implementation
- tool use

## Verification

- test quality
- behavioral validation

## Reliability

- crash
- retry
- resume
- reassignment

## Collaboration

- steerability
- clarification
- reviewability

## Governance

- permission
- approval
- audit

## Economics

- cost
- human attention
- time

---

# 13. Offline Eval + Online Production Measurement

Offline:

- reproducible
- safe
- regression

Online:

- actual task distribution
- real infra
- human interaction

둘 다 필요하다.

```text
Offline Eval
→ Pre-deploy confidence

Online Metrics
→ Real-world validity
```

---

# 14. Fresh Eval Generation

Factory가 자기 production history에서 다음을 만들 수 있다.

- failed task
- rejected PR
- rollback
- incident
- escaped defect

→ sanitized Eval Case.

이것이 compounding improvement loop의 기반이 된다.

---

# 15. Benchmark Governance

Eval suite 자체도 변경 관리해야 한다.

- version
- task provenance
- hidden tests
- contamination
- scorer
- environment image

Agent가 Eval definition을 자유롭게 수정하면 reward hacking 위험이 생긴다.

---

# 핵심 후보 메시지

> AI Software Factory를 평가하려면 하나의 SWE-bench 점수가 아니라 specification, exploration, execution, verification, recovery, collaboration, cost를 분리해 측정해야 한다.

> Agentic system의 실제 평가 단위는 Model이 아니라 Model + Harness + Environment + Policy인 경우가 많다.

> 좋은 Factory는 benchmark를 소비하는 시스템을 넘어 production failure를 새로운 Eval로 변환하는 시스템이 되어야 한다.
