# 18장. Review, CI, Integration: Coding 다음 병목

Agent가 코드를 빠르게 만들기 시작하면 조직의 병목은 사라지지 않는다.

다음 단계로 이동한다.

~~~text
Implementation
→ Review
→ CI
→ Integration
→ Release
~~~

Worker가 많아질수록 이 이동은 더 빨라진다.

그래서 Factory는 Coding Capacity만 늘리면 안 된다.

전체 파이프라인의 Capacity를 봐야 한다.

> 이 책에서는 Correct but unreviewable change도 Factory 품질 문제로 본다.

---

## 18.1 Bottleneck Migration

예를 들어 하루에 다음 처리량을 가진 팀이 있다고 하자.

~~~text
Implementation: 30 changes/day
Review:          6 changes/day
CI:             12 changes/day
Integration:     8 changes/day
~~~

전체 흐름은 Review에 막힌다.

~~~text
Factory Throughput
≈ min(
  Implementation,
  Review,
  CI,
  Integration
)
~~~

Worker를 더 늘려 Implementation을 60 changes/day로 올려도 전체 처리량은 크게 변하지 않는다.

오히려 WIP만 늘어난다.

---

## 18.2 Reviewability를 품질 속성으로 본다

Agent가 만든 코드가 기능적으로 맞더라도 Review가 매우 어렵다면 Delivery Cost가 커진다.

Reviewability에는 다음이 영향을 준다.

- Diff Size
- Logical Commit
- Unrelated Change
- Naming
- Scope
- Evidence
- PR Description
- Ownership Boundary

예를 들어 Task는 작았는데 Agent가 주변 코드를 대규모 Refactor했다고 하자.

Test는 PASS한다.

하지만 Reviewer는 원래 변경과 Refactor를 분리해 읽어야 한다.

Factory 관점에서는 이런 결과도 품질 문제다.

~~~text
Correct
but
Unreviewable
~~~

---

## 18.3 Giant PR 문제

Agent는 장시간 실행되면 큰 Diff를 만들기 쉽다.

특히 “이 Feature 전체를 구현하라”는 Task는 하나의 거대한 Pull Request로 끝날 수 있다.

문제:

- Review Cognitive Load
- Merge Conflict
- Failure Localization
- Rollback
- Ownership

큰 Product Task가 꼭 큰 PR이어야 하는 것은 아니다.

~~~text
Large Task
≠ One Large PR
~~~

필요하면 Delivery Artifact를 Layer로 나눈다.

~~~text
PR1 foundational refactor
  ↓
PR2 behavior change
  ↓
PR3 migration
  ↓
PR4 cleanup
~~~

Stacked PR는 이런 구조를 지원하는 하나의 방식이다. GitHub도 2026년 7월 Stacked Pull Requests를 public preview로 공개하고, 8월에는 AI-generated giant PR를 dependency-ordered stack으로 나누는 engineering workflow를 소개했다. 이는 Reviewability를 개선하는 하나의 구현 사례이지 모든 큰 변경을 stack으로 만들어야 한다는 뜻은 아니다.

단, Dependency와 Rebase Cost가 생긴다.

따라서 “작게 쪼개기”가 목표가 아니라 **Review 가능한 변경 단위**를 만드는 것이 목표다.

---

## 18.4 Verification Queue

Agent가 수정할 때마다 모든 검증을 실행하면 CI가 포화될 수 있다.

예:

~~~text
20 Workers
×
full regression 15 min
×
multiple attempts
~~~

비싼 E2E와 Security Scan까지 매 Attempt 실행하면 Queue가 길어진다.

그래서 Verification을 단계화할 수 있다.

~~~text
Cheap Check
→ Targeted Test
→ Candidate
→ Expensive Verification
~~~

예:

~~~text
Edit
→ compile
→ target unit

Candidate
→ integration
→ full regression
→ security
~~~

초기 Feedback은 빠르게 주고, 비싼 검증은 Candidate에 집중한다.

---

## 18.5 CI도 Capacity다

Factory Scheduler가 Worker Availability만 보면 부족하다.

CI Capacity도 Resource다.

예:

~~~text
Worker Slots: 20
CI Full Regression Slots: 3
Browser E2E Slots: 2
Performance Benchmark Slots: 1
~~~

Task를 20개 동시에 시작하면 후반부에서 모두 대기할 수 있다.

이 경우 Scheduler는 다음 정책을 둘 수 있다.

~~~text
if expensive_verification_queue > threshold:
    slow new work
~~~

Implementation을 늦추는 것이 비효율처럼 보일 수 있다.

하지만 전체 Cycle Time과 WIP는 오히려 좋아질 수 있다.

---

## 18.6 WIP Limit

Agent 실행 비용이 낮아지면 Work를 시작하는 것이 너무 쉬워진다.

그러면 다음 상태가 폭발할 수 있다.

~~~text
RUNNING
AWAITING_REVIEW
PENDING_INTEGRATION
~~~

각 상태에 Limit를 둘 수 있다.

예:

~~~text
RUNNING <= 10
AWAITING_REVIEW <= 6
PENDING_INTEGRATION <= 4
~~~

정답 숫자는 조직마다 다르다.

중요한 것은 Start Rate를 Downstream Capacity와 연결하는 것이다.

---

## 18.7 Review Queue가 길어지면 생기는 비용

Review가 늦어지면 단순 대기 시간만 늘어나는 것이 아니다.

- Base Branch가 변한다.
- Conflict가 늘어난다.
- Reviewer Context가 사라진다.
- Agent가 만든 전제가 오래된다.
- Duplicate Work가 생길 수 있다.

그래서 Review Wait는 Factory Reliability에도 영향을 준다.

---

## 18.8 AI Reviewer가 모든 문제를 해결하지 않는다

AI Reviewer를 붙이면 Review Capacity를 늘릴 수 있다.

좋은 사용 방식:

~~~text
Implementer
→ AI Review
→ Fix
→ Deterministic Check
→ Human / Policy Gate
~~~

사람이 보기 전에 cheap first pass를 수행할 수 있다.

하지만 AI Review도 다음 문제가 있다.

- False Positive
- Missed Issue
- Context Sensitivity
- Correlated Error
- Review Theater

9장에서 본 GitHub의 2026년 Copilot Code Review 사례처럼 Reviewer Agent도 Tool 변경만으로 자동 개선되지 않는다. Tool, Instruction, 탐색 Workflow를 함께 평가해야 한다. 따라서 AI Reviewer를 Human Review의 단순 대체재가 아니라 별도의 Harness와 Eval이 필요한 검증 주체로 보는 편이 안전하다.

---

## 18.9 Integration Acceptance

각 PR이 맞아도 합친 결과가 틀릴 수 있다.

~~~text
Local Correctness
≠ Global Correctness
~~~

예:

~~~text
PR A
→ DB column rename
→ local PASS

PR B
→ API contract update
→ local PASS

Integrated
→ migration compatibility FAIL
~~~

Fan-in 이후 다음 검증이 필요할 수 있다.

- Integration Test
- System E2E
- Migration Compatibility
- Performance
- Security

Parallel Factory에서는 Integration이 독립 Stage가 된다.

---

## 18.10 Review Evidence Package

13장의 Evidence Contract는 Reviewer Capacity와 직접 연결된다.

Reviewer가 다음 Package를 받는다고 하자.

~~~text
Goal
Scope
Result Commit
Changed Files
Verification
Before/After
Known Risk
~~~

Repository를 처음부터 탐색하는 비용이 줄어든다.

목표는 Human Judgment를 제거하는 것이 아니라 **Judgment Startup Cost를 낮추는 것**이다.

---

## 예: 30개 PR과 6개 Review Capacity

가상 상황:

~~~text
Agent output
30 PR/day

Reviewer capacity
6 PR/day
~~~

매일 24개가 Queue에 추가된다.

5일이면 120개 가까운 Pending Work가 쌓일 수 있다.

이때 해결책은 Agent를 더 빠르게 만드는 것이 아니다.

가능한 대응:

~~~text
- WIP limit
- Task start throttling
- AI first review
- smaller reviewable changes
- risk-based review
- evidence package
~~~

Factory는 Worker Utilization이 아니라 전체 Flow를 최적화해야 한다.

---

## 다음 질문

어디가 병목인지 알려면 관찰해야 한다.

Agent 실행 시간만 봐서는 Review Queue와 Human Wait를 알 수 없다.

Token Cost만 봐서는 Retry와 Rework를 알 수 없다.

다음 장에서는 **Factory Observability와 Metrics**를 다룬다.

---

## 참고 자료

- GitHub Engineering, *Turn one giant AI-generated pull request to a reviewable stack*  
  https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/
- GitHub, *Stacked pull requests are now in public preview*  
  https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/
- METR, *Many SWE-bench-Passing PRs Would Not Be Merged into Main*  
  https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
- GitHub, *Better tools made Copilot code review worse*  
  https://github.blog/ai-and-ml/github-copilot/better-tools-made-copilot-code-review-worse-heres-how-we-actually-improved-it/
