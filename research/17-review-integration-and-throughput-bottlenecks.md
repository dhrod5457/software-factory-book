# Review, Integration, and Throughput Bottlenecks

기준일: 2026-09-28

AI coding agent가 implementation throughput을 크게 높이면 병목은 사라지지 않는다.

대개 다음 단계로 이동한다.

```text
Implementation
→ Review
→ CI
→ Integration
→ Release
→ Product Acceptance
```

이 문서는 Factory의 downstream bottleneck을 조사한다.

---

## 1. Code Generation은 이미 유일한 병목이 아니다

GitHub는 2026년 enterprise coding-agent 관련 글에서 code generation은 쉬워지고 병목이 shipping으로 이동했다고 설명한다.

주요 영역:

- review
- security
- governance
- deploy

출처:

- https://github.blog/ai-and-ml/github-copilot/github-recognized-as-a-leader-in-the-gartner-magic-quadrant-for-enterprise-ai-coding-agents-for-the-third-year-in-a-row/

Gartner 인용 수치는 GitHub가 인용한 외부 forecast이므로 책의 사실 주장에는 신중하게 사용한다.

---

## 2. Human Review Capacity

Agent가 하루에 더 많은 PR을 만들면 reviewer throughput은 자동으로 늘지 않는다.

문제:

- review queue
- stale PR
- context switching
- large diff
- duplicate agent PR
- inconsistent quality

따라서 Agent throughput을 늘리기 전에 review architecture가 필요하다.

---

## 3. AI Review도 완전한 해결책이 아니다

GitHub는 Copilot Code Review 사용량이 크게 증가했다고 공개했다.

하지만 review agent도:

- false positive
- missed issue
- instruction sensitivity
- context cost

문제가 있다.

출처:

- https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/
- https://github.blog/ai-and-ml/github-copilot/better-tools-made-copilot-code-review-worse-heres-how-we-actually-improved-it/

---

## 4. Reviewability를 Production Requirement로 본다

Agent Task의 완료조건에 code correctness뿐 아니라 reviewability를 포함할 수 있다.

예:

- diff size
- logical commit
- PR description
- evidence
- no unrelated change
- ownership boundary

즉:

```text
Correct but unreviewable
```

은 Factory 품질 문제다.

---

## 5. Stacked PR Pattern

큰 feature를 작은 ordered PR chain으로 분리한다.

장점:

- layer별 review
- parallel review 가능
- 변경 목적 명확
- rollback/failure localization

단점:

- dependency management
- stack rebase
- merge ordering

GitHub는 tooling으로 이 cost를 줄이는 방향을 제공한다.

출처:

- https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/
- https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/

---

## 6. Merge Conflict is a Scheduling Signal

Multi-agent shared codebase에서는 conflict를 merge 단계에서 뒤늦게 해결하는 것보다 scheduler가 사전에 줄이는 편이 낫다.

입력:

- files
- modules
- schema
- ownership
- dependency

예:

```text
T1 touches auth/schema.sql
T2 touches auth/schema.sql

→ parallel penalty
```

Task planner가 file-level impact를 완벽히 예측할 수 없으므로 runtime conflict detection도 필요하다.

---

## 7. Integration Branch / Staging Area

Parallel Agent output을 모두 main에 직접 merge하지 않고 integration area에서 fan-in할 수 있다.

```text
Worker A ─┐
Worker B ─┼→ Integration → Regression → Main
Worker C ─┘
```

적합:

- coordinated feature
- shared schema
- large migration

단 independence가 높은 task에는 불필요한 overhead가 될 수 있다.

---

## 8. CI Capacity

Agent가 병렬로 PR을 만들면 CI workload도 증가한다.

Factory scheduler에 CI resource를 고려할 수 있다.

예:

- targeted test first
- full regression only after candidate
- deduplicate build
- cache
- batch integration test

Agent 수만 제한하지 말고 downstream capacity를 고려한다.

---

## 9. Verification Queue

비싼 검증:

- E2E
- browser
- security scan
- full regression
- performance benchmark

은 모든 attempt마다 실행하기 어렵다.

단계별 gate:

```text
Cheap Check
→ Targeted Test
→ Candidate
→ Expensive Verification
```

이렇게 Agent iteration cost와 quality를 균형 잡는다.

---

## 10. Security Scan as Universal Downstream Gate

GitHub는 Copilot뿐 아니라 third-party coding agent output에도 동일한 security validation을 적용한다.

- CodeQL
- dependency checks
- secret scanning

이 구조는 Author Agent와 Verification Platform 분리를 보여준다.

출처:

- https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/

---

## 11. Maintainer Review vs Automated Grader

METR 결과는 automated test를 통과한 patch도 maintainer가 merge하지 않을 수 있음을 보여준다.

리뷰 이유:

- code quality
- unintended behavior
- repo convention
- broader integration

따라서 review는 현재도 다른 종류의 signal이다.

출처:

- https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/

---

## 12. Agent-to-Agent Review

OpenAI Harness Engineering은 agent-to-agent review의 비중을 늘린 사례를 공개했다.

가능한 pattern:

```text
Implementer
→ Reviewer Agent
→ Fix
→ Deterministic Check
→ Human / Policy Gate
```

장점:

- cheap first review
- reviewer workload 감소

위험:

- correlated error
- same model bias
- review theater

따라서 independent evidence와 병행한다.

---

## 13. AI-to-AI Review Is Emerging

2026 arXiv 연구는 agent-authored PR에 AI reviewer가 붙는 실제 GitHub activity를 대규모로 분석했다.

아직 cross-product AI-to-AI review는 minority지만 absolute volume이 증가하고 있다고 보고한다.

자료:

- https://arxiv.org/abs/2608.21311

이 자료는 최신 preprint이며 결론을 과도하게 일반화하지 않는다.

---

## 14. Circuit Breaker

Factory에서 review queue가 overload되면 무조건 새 Task를 계속 시작하지 않는다.

가능한 policy:

```text
if review_queue > threshold:
    slow new implementation
    prioritize verification/review
```

이것은 manufacturing flow control과 유사하다.

Work-in-progress limit이 Agent Factory에도 필요할 수 있다.

---

## 15. WIP Limit

Kanban/Lean의 기존 원칙을 그대로 복사할 필요는 없지만 다음 아이디어는 유효하다.

- Running Task 제한
- Awaiting Review 제한
- Pending Integration 제한

왜냐하면 Agent가 매우 싸게 생성되면 WIP가 폭발하기 쉽기 때문이다.

---

## 16. Duplicate Work

여러 agent가 같은 issue나 비슷한 improvement를 동시에 발견할 수 있다.

필요:

- task deduplication
- ownership
- lease
- semantic similarity check

특히 proactive agent가 많아지면 중요해진다.

---

## 17. Review Evidence Package

Reviewer가 repository를 직접 재현하지 않아도 1차 판단할 수 있도록:

- summary
- change scope
- tests
- screenshot
- video
- benchmark
- risk
- known limitation

을 자동 생성할 수 있다.

목적:

> Human judgment 제거가 아니라 judgment startup cost를 낮춘다.

---

## 18. Risk-based Review

모든 PR을 같은 깊이로 review하지 않는다.

예:

### Low risk

- docs
- generated file
- test-only

→ automated + light review

### Medium

- business logic

→ agent review + human

### High

- auth
- payment
- migration
- infrastructure

→ specialist + stronger verification

---

## 19. Integration Acceptance

각 PR이 맞아도 합쳐진 system이 틀릴 수 있다.

따라서 Fan-in 이후:

- integration test
- system E2E
- migration compatibility
- performance

검증이 필요하다.

```text
Local Correctness
≠ Global Correctness
```

---

## 20. Factory Throughput Equation 후보

개념적으로:

```text
Factory Throughput
≈ min(
  Task Ready Rate,
  Worker Capacity,
  Verification Capacity,
  Review Capacity,
  Integration Capacity,
  Deployment Capacity
)
```

정확한 수학식이라기보다 bottleneck 사고 모델이다.

Agent Worker를 늘려도 min stage가 그대로면 throughput은 늘지 않는다.

---

# 핵심 후보 메시지

> Coding Agent 시대의 핵심 운영 문제는 코드를 더 빨리 생성하는 것이 아니라 생성 속도에 맞춰 review, verification, integration을 확장하는 것이다.

> Factory는 Agent를 최대한 많이 실행하는 시스템이 아니라 전체 파이프라인의 WIP를 조절하는 시스템이어야 한다.

> Reviewability와 integration cost도 Agent Task의 품질 속성으로 다뤄야 한다.
