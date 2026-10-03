# 18장. Review, CI, Integration: Coding 다음 병목

에이전트가 코드를 빠르게 만들기 시작하면 조직의 병목은 사라지지 않는다. 다음 단계로 이동한다.

~~~text
Implementation
→ Review
→ CI
→ Integration
→ Release
~~~

워커가 많아질수록 이 이동은 더 빨라진다. 그래서 생산 시스템은 코딩 처리 능력만 늘리면 안 된다. 전체 파이프라인의 처리 능력을 봐야 한다.

> 이 책에서는 기능은 맞아도 사람이 검토하기 어려운 변경을 생산 시스템의 품질 문제로 본다.

---

## 18.1 Bottleneck Migration

예를 들어 하루에 다음 처리량을 가진 팀이 있다고 하자.

~~~text
Implementation: 30 changes/day
Review:          6 changes/day
CI:             12 changes/day
Integration:     8 changes/day
~~~

전체 흐름은 검토에 막힌다.

~~~text
Factory Throughput
≈ min(
  Implementation,
  Review,
  CI,
  Integration
)
~~~

워커를 더 늘려 구현을 60 건/일로 올려도 전체 처리량은 크게 변하지 않는다. 오히려 WIP만 늘어난다.

---

## 18.2 Reviewability를 품질 속성으로 본다

에이전트가 만든 코드가 기능적으로 맞더라도 검토가 매우 어렵다면 전달 비용이 커진다. 검토 용이성에는 다음이 영향을 준다.

- 변경 내역 크기
- 논리적으로 묶인 커밋
- 관련 없는 변경
- 이름 지정
- 범위
- 근거
- 변경 검토 요청 설명
- 담당 관계 경계

예를 들어 작업은 작았는데 에이전트가 주변 코드를 대규모로 구조를 개선했다고 하자. 테스트는 PASS한다. 하지만 검토자는 원래 변경과 구조 개선을 분리해 읽어야 한다. 생산 시스템 관점에서는 이런 결과도 품질 문제다.

~~~text
Correct
but
Unreviewable
~~~

---

## 18.3 Giant PR 문제

에이전트는 장시간 실행되면 큰 변경 내역을 만들기 쉽다. 특히 “이 기능 전체를 구현하라”는 작업은 하나의 거대한 변경 검토 요청으로 끝날 수 있다.

문제:

- 검토 이해하는 데 드는 부담
- 병합 충돌
- 실패 원인 위치 파악
- 이전 상태로 복구
- 담당 관계

큰 제품 작업이 꼭 큰 PR이어야 하는 것은 아니다.

~~~text
Large Task
≠ One Large PR
~~~

필요하면 전달 산출물을 계층으로 나눈다.

~~~text
PR1 foundational refactor
  ↓
PR2 behavior change
  ↓
PR3 migration
  ↓
PR4 cleanup
~~~

순서대로 연결한 변경 검토 요청은 이런 구조를 지원하는 하나의 방식이다. GitHub도 2026년 7월 Stacked Pull Requests를 공개 미리보기로 공개하고, 8월에는 AI가 만든 대규모 변경 검토 요청을 의존 순서에 따라 연결한 묶음으로 나누는 개발 작업 흐름을 소개했다. 이는 검토 용이성을 개선하는 하나의 구현 사례이지 모든 큰 변경을 연결된 묶음으로 만들어야 한다는 뜻은 아니다. 단, 의존 관계와 변경의 기준 브랜치 갱신 비용이 생긴다. 따라서 “작게 쪼개기”가 목표가 아니라 **검토 가능한 변경 단위**를 만드는 것이 목표다.

---

## 18.4 Verification Queue

에이전트가 수정할 때마다 모든 검증을 실행하면 CI가 포화될 수 있다.

예:

~~~text
20 Workers
×
full regression 15 min
×
multiple attempts
~~~

비싼 E2E와 보안 검사까지 매 시도 실행하면 대기열이 길어진다. 그래서 검증을 단계화할 수 있다.

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

초기 피드백은 빠르게 주고, 비싼 검증은 후보에 집중한다.

---

## 18.5 CI도 Capacity다

생산 시스템 작업 배정기가 워커 사용 가능 여부만 보면 부족하다. CI 처리 능력도 자원이다.

예:

~~~text
Worker Slots: 20
CI Full Regression Slots: 3
Browser E2E Slots: 2
Performance Benchmark Slots: 1
~~~

작업을 20개 동시에 시작하면 후반부에서 모두 대기할 수 있다. 이 경우 작업 배정기는 다음 정책을 둘 수 있다.

~~~text
if expensive_verification_queue > threshold:
    slow new work
~~~

구현을 늦추는 것이 비효율처럼 보일 수 있다. 하지만 전체 처리 시간과 WIP는 오히려 좋아질 수 있다.

---

## 18.6 WIP Limit

에이전트 실행 비용이 낮아지면 작업을 시작하는 것이 너무 쉬워진다. 그러면 다음 상태가 폭발할 수 있다.

~~~text
RUNNING
AWAITING_REVIEW
PENDING_INTEGRATION
~~~

각 상태에 한도를 둘 수 있다.

예:

~~~text
RUNNING <= 10
AWAITING_REVIEW <= 6
PENDING_INTEGRATION <= 4
~~~

정답 숫자는 조직마다 다르다. 중요한 것은 뒤에 이어질 검토와 통합 단계가 감당할 수 있는 만큼 새 작업을 시작하는 것이다.

---

## 18.7 Review Queue가 길어지면 생기는 비용

검토가 늦어지면 단순 대기 시간만 늘어나는 것이 아니다.

- 기준 브랜치가 변한다.
- 충돌이 늘어난다.
- 검토자 맥락 정보가 사라진다.
- 에이전트가 만든 전제가 낡는다.
- 중복 작업이 생길 수 있다.

그래서 검토 대기 시간은 생산 시스템 신뢰성에도 영향을 준다.

---

## 18.8 AI Reviewer가 모든 문제를 해결하지 않는다

AI 검토자를 붙이면 검토 처리 능력을 늘릴 수 있다.

좋은 사용 방식:

~~~text
Implementer
→ AI Review
→ Fix
→ Deterministic Check
→ Human / Policy Gate
~~~

사람이 보기 전에 비용이 낮은 첫 검토를 수행할 수 있다. 하지만 AI 검토도 다음 문제가 있다.

- 잘못된 경고
- 놓친 이슈
- 맥락 정보 민감도
- 서로 연관된 오류
- 검토 겉모습만 갖춘 검토

9장에서 본 GitHub의 2026년 Copilot Code Review 사례처럼 검토자 에이전트도 도구 변경만으로 자동 개선되지 않는다. 도구, 지시사항, 탐색 작업 흐름을 함께 평가해야 한다. 따라서 AI 검토자를 사람의 검토를 단순히 대신하는 도구가 아니라 별도의 하네스와 평가가 필요한 검증 주체로 보는 편이 안전하다.

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

결과를 다시 합치는 단계 이후 다음 검증이 필요할 수 있다.

- 통합 테스트
- 시스템 E2E
- 마이그레이션 호환성
- 성능
- 보안

병렬 생산 시스템에서는 통합이 독립 단계가 된다.

---

## 18.10 Review Evidence Package

13장의 증거 계약은 검토자 처리 능력과 직접 연결된다.

검토자가 다음 묶음을 받는다고 하자.

~~~text
Goal
Scope
Result Commit
Changed Files
Verification
Before/After
Known Risk
~~~

저장소를 처음부터 탐색하는 비용이 줄어든다. 목표는 사람의 판단을 제거하는 것이 아니라 **판단 시작 비용을 낮추는 것**이다.

---

## 예: 30개 PR과 6개 Review Capacity

가상 상황:

~~~text
Agent output
30 PR/day

Reviewer capacity
6 PR/day
~~~

매일 24개가 대기열에 추가된다.

5일이면 120개 가까운 대기 중인 작업이 쌓일 수 있다.

이때 해결책은 에이전트를 더 빠르게 만드는 것이 아니다.

가능한 대응:

~~~text
- WIP limit
- Task start throttling
- AI first review
- smaller reviewable changes
- risk-based review
- evidence package
~~~

생산 시스템은 워커 사용률이 아니라 전체 흐름을 최적화해야 한다.

---

## 다음 질문

어디가 병목인지 알려면 관찰해야 한다. 에이전트 실행 시간만 봐서는 검토 대기열과 사람의 판단을 기다리는 시간을 알 수 없다. 토큰 비용만 봐서는 재시도와 재작업을 알 수 없다. 다음 장에서는 **생산 시스템 관측 가능성과 지표**를 다룬다.

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
