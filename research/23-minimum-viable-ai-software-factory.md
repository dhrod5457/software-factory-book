# Minimum Viable AI Software Factory

기준일: 2026-09-28

AI Software Factory라는 이름 때문에 처음부터 거대한 autonomous platform을 구축하려는 것은 위험하다.

Platform Engineering의 경험에서도 Big Bang platform은 대표적인 anti-pattern이다.

DORA는 "minimum viable platform"부터 시작할 것을 권한다.

이 문서는 AI Software Factory에도 같은 원칙을 적용할 수 있는지 조사한다.

출처:

- https://dora.dev/capabilities/platform-engineering/
- https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/

---

# 1. Factory를 만들기 전에 Repeatable Work가 있어야 한다

첫 질문:

> 반복해서 발생하며 완료조건을 정의할 수 있는 작업은 무엇인가?

좋은 초기 후보:

- documentation
- test addition
- dependency update
- CI failure triage
- small bug
- lint/static fix

나쁜 초기 후보:

- 전체 architecture 재설계
- 모호한 신규 product
- production emergency autonomous control

---

# 2. 최소 Factory는 Multi-Agent가 필요하지 않다

최소 구성 후보:

```text
Human selects Task
      ↓
Durable Task Record
      ↓
One Isolated Worker
      ↓
Coding Agent
      ↓
Deterministic Verification
      ↓
Evidence
      ↓
Human Review
```

이것만으로도 Interactive Assistant와 다른 Factory 특성이 생긴다.

- task state
- asynchronous execution
- isolation
- evidence
- repeatability

---

# 3. Phase 0 - Agent-ready Repository

먼저:

- build command
- targeted tests
- documentation
- setup
- environment
- ownership

이 명확해야 한다.

Factory가 repository chaos를 자동으로 해결해 줄 것이라고 기대하지 않는다.

---

# 4. Phase 1 - Reproducible Worker

목표:

같은 Task가 어느 Worker에서도 실행 가능.

필요:

- clean checkout
- runtime
- dependency
- test
- secrets boundary

아직 scheduler/fleet 불필요.

---

# 5. Phase 2 - Evidence Contract

Agent result를 standardized result로 만든다.

예:

```text
Task ID
Commit
Changed Files
Verification
Artifacts
Known Risk
```

이 단계가 없으면 scale 이후 사람이 결과를 비교하기 어렵다.

---

# 6. Phase 3 - Durable Task State

상태:

- ready
- running
- verifying
- awaiting human
- done
- failed

attempt/retry도 기록.

이때부터 session loss에서 Task를 복구할 수 있다.

---

# 7. Phase 4 - Event-driven Trigger

Human manual trigger 외에:

- CI failure
- issue
- schedule

를 연결.

중요:

자동 시작과 자동 merge를 동일시하지 않는다.

---

# 8. Phase 5 - Parallel Worker

먼저 실제 queue를 측정한다.

병렬화 조건:

- 충분한 independent task
- downstream review capacity
- CI capacity

없으면 Worker 증가가 가치가 없다.

---

# 9. Phase 6 - Risk-based Automation

Task class별:

- approval
- verification
- permission
- auto merge

정책을 다르게 한다.

---

# 10. Phase 7 - Work Selection Automation

마지막 쪽에 둔다.

- backlog selection
- proactive issue
- incident-derived work

왜 늦게?

잘못된 Task를 완벽하게 자동 실행하는 것은 생산성이 아니다.

---

# 11. Maturity 후보

### M0 - Interactive Agent

Human이 session 직접 운전.

### M1 - Repeatable Worker

Task + isolated execution + evidence.

### M2 - Durable Factory

queue + state + retry + recovery.

### M3 - Parallel Factory

worker scheduling + dependency.

### M4 - Event-driven Factory

external signals → task execution.

### M5 - Adaptive Factory

work selection + routing + self-improvement.

이 taxonomy는 연구용 초안이며 업계 표준이 아니다.

---

# 12. 각 단계의 성공 조건

## M1

"Agent가 좋은 코드를 썼는가?"보다:

> 10개의 작은 Task를 같은 방식으로 처리할 수 있는가?

## M2

> Worker를 죽여도 Task가 정상 복구되는가?

## M3

> Worker 2~5개를 늘렸을 때 accepted throughput이 증가하는가?

## M4

> 잘못된 event가 unsafe action으로 연결되지 않는가?

## M5

> Factory 개선이 실제 quality/cost improvement를 가져오는가?

---

# 13. Minimum Viable Verification

초기부터 완벽한 evaluator platform이 필요하지 않다.

최소:

- build
- targeted tests
- full regression 조건
- diff/evidence
- human review

Task에 맞는 자동 검증이 없으면 해당 Task를 Factory 대상에서 제외할 수 있다.

---

# 14. Minimum Viable Observability

처음부터 full tracing platform을 만들지 않아도 된다.

최소:

- Task timeline
- Worker
- Attempt
- status
- command/test result
- failure reason
- duration
- token/cost

이후 필요에 따라 span/tool trace 확장.

---

# 15. Minimum Viable Security

최소한:

- isolated workspace
- protected main branch
- scoped repo credential
- secret scan
- network policy
- dangerous action human gate

Prompt 규칙만으로 시작하지 않는다.

---

# 16. Avoid Premature Autonomy

초기 Factory에서 중요한 것은 자율성 최대화가 아니라 reliability baseline이다.

```text
Reliability
→ Observability
→ Recovery
→ Scale
→ Autonomy
```

순서를 후보로 본다.

---

# 17. Avoid Premature Multi-Agent

여러 role Agent를 처음부터 추가하면:

- coordination
- context duplication
- debugging

비용이 커진다.

먼저 strong single worker + verification을 측정한다.

필요한 failure가 관찰된 뒤:

- planner
- evaluator
- reviewer

를 분리한다.

---

# 18. Measure Before Automation

초기 측정:

- Task duration
- human intervention
- retry
- acceptance
- review time
- CI time
- cost

이 baseline 없이 "자동화 후 좋아졌다"를 판단하기 어렵다.

---

# 19. Factory Backlog

Factory 자체도 product처럼 backlog를 갖는다.

예:

- slow bootstrap
- weak test
- missing context
- flaky environment
- unsafe permission
- review bottleneck

WorkOS/OpenAI 사례처럼 실제 Task에서 나타난 friction을 우선 개선한다.

---

# 20. Adoption Principle

DORA의 Minimum Viable Platform 원칙을 Factory에 적용하면:

> 가장 빈번하고 반복 가능하며 현재 가장 많은 개발자 주의를 잡아먹는 한 가지 workflow부터 자동화한다.

Factory를 만드는 것 자체가 목적이 아니다.

---

# 핵심 후보 메시지

> 첫 AI Software Factory는 수십 개 Agent를 가진 autonomous organization일 필요가 없다.

> Durable Task 하나를 Isolated Worker가 Evidence와 함께 반복 처리하는 구조만으로도 Factory의 최소 성질을 만들 수 있다.

> Autonomy는 첫 기능이 아니라 reliability, verification, observability가 확보된 뒤 점진적으로 올리는 운영 속성으로 보는 편이 안전하다.

> Software Factory도 Internal Developer Platform처럼 Big Bang보다 Minimum Viable Factory로 시작하는 것이 현실적이다.
