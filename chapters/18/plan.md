# 18장 설계 - Review, CI, Integration: Coding 다음 병목

## 장의 목표

Agent implementation throughput이 증가한 뒤 downstream capacity가 전체 Factory throughput을 제한하는 과정을 설명하고 WIP, reviewability, CI/verification capacity를 함께 관리한다.

이 장의 핵심 질문:

> Agent가 PR을 더 많이 만들면 왜 팀이 더 느려질 수 있는가?

> Factory Scheduler가 Review/CI Capacity까지 봐야 하는 이유는 무엇인가?

---

## 핵심 주장

> Factory throughput은 가장 느린 downstream stage에 의해 제한될 수 있다.

> Correct but unreviewable change도 Factory quality problem이다.

> WIP limit과 staged verification은 Agent 시대에도 중요하다.

---

## 독자가 얻는 것

- Review/CI/Integration bottleneck을 측정할 수 있다.
- Giant PR를 stacked/incremental delivery로 줄일 수 있다.
- Verification queue와 CI capacity를 scheduling에 반영할 수 있다.
- Review Evidence Package로 human attention을 줄일 수 있다.

---

## 반드시 사용할 Research

- `research/17-review-integration-and-throughput-bottlenecks.md`
- `research/14-failure-modes-and-antipatterns.md`
- `research/16-productivity-evidence-and-measurement.md`
- `research/25-human-agent-collaboration-and-responsibility-research.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Agent count만 늘리면 throughput이 선형 증가한다는 가정
- Giant autonomous PR
- 모든 attempt마다 full regression/E2E를 실행해 CI를 포화시키는 방식
- AI reviewer를 human review의 완전 대체로 보는 주장

---

# 절 구성

## 18.1 Bottleneck Migration

Implementation이 빨라지면 Review, CI, Integration, Deploy가 min capacity stage가 되는 흐름을 설명한다.

## 18.2 Reviewability

diff size, logical commit, evidence, no unrelated change를 Task quality attribute로 본다.

## 18.3 Verification Queue

Cheap Check → Targeted Test → Candidate → Expensive Verification 단계로 비용을 분산하는 방식을 설명한다.

## 18.4 Stacked / Incremental Delivery

큰 Feature를 작은 reviewable change로 나누되 dependency cost가 있음을 함께 설명한다.

## 18.5 WIP Limit

RUNNING, AWAITING_REVIEW, PENDING_INTEGRATION에 capacity limit을 두어 work explosion을 막는 개념을 제시한다.

## 18.6 Integration Acceptance

각 PR이 맞아도 합친 시스템이 틀릴 수 있어 fan-in 이후 integration/system verification이 필요함을 설명한다.


---

## 필요한 구조 / 그림

1. Factory throughput bottleneck pipeline
2. WIP states and limits
3. Cheap→Expensive verification funnel

---

## 실전 예제 / 실험

- Agent PR 30개/일, reviewer 처리량 6개/일인 queue 시뮬레이션
- Full E2E 대신 targeted test 후 candidate에만 full regression 적용

---

## 본문에서 의도적으로 다루지 않을 내용

- Kanban/Lean 입문
- CI product configuration tutorial
- 코드리뷰 일반론 전체

---

## 앞뒤 장 연결

19장에서는 이런 전체 Flow를 관찰하고 개선하기 위해 무엇을 기록하고 어떤 metric을 볼지 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
