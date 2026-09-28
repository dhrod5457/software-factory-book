# 22장 설계 - Minimum Viable AI Software Factory

## 장의 목표

조직이 처음부터 거대한 autonomous multi-agent platform을 만들지 않고, 반복 가능한 Task 하나를 durable하게 실행·검증·review하는 최소 구조부터 시작하는 방법을 제시한다.

이 장의 핵심 질문:

> 첫 Software Factory는 어디까지 만들어야 하는가?

> 어떤 순서로 capability를 추가해야 실패 위험과 과잉투자를 줄일 수 있는가?

---

## 핵심 주장

> Minimum Viable Factory는 Multi-Agent나 automatic work selection 없이도 성립한다.

> Autonomy보다 reliability baseline, evidence, observability, recovery를 먼저 구축해야 한다.

> 가장 빈번하고 반복 가능하며 acceptance가 정의되는 workflow 하나부터 시작하는 것이 현실적이다.

---

## 독자가 얻는 것

- 첫 Factory use case를 고를 수 있다.
- MVP 구성요소를 설계할 수 있다.
- Capability 도입 순서를 정할 수 있다.
- Premature multi-agent/autonomy를 피할 수 있다.

---

## 반드시 사용할 Research

- `research/23-minimum-viable-ai-software-factory.md`
- `research/19-boundaries-devops-platform-engineering-agent-platform.md`
- `research/16-productivity-evidence-and-measurement.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Big Bang Agent Platform
- 처음부터 automatic backlog selection/self-improvement 시도
- Observability 없이 Worker 수부터 늘리기
- 자동 검증이 없는 모호한 Task를 첫 use case로 선택

---

# 절 구성

## 22.1 첫 Use Case 고르기

docs, test addition, dependency update, CI failure triage, small bug처럼 반복 가능하고 acceptance가 정의되는 일을 추천한다.

## 22.2 최소 구조

Human selects Task → Durable Task → Isolated Worker → Agent → Deterministic Verification → Evidence → Human Review 흐름을 제시한다.

## 22.3 Agent-ready Repository

build/test/docs/setup이 명확하지 않으면 Factory가 repository chaos를 증폭할 수 있음을 설명한다.

## 22.4 Evidence와 Durable State 먼저

scale 전에 result contract와 task state를 표준화해 결과 비교와 recovery 기반을 만든다.

## 22.5 고도화 순서

Reproducible Worker → Evidence → Durable State → Retry/Resume → Event Trigger → Parallel → Risk-based Automation 순을 제시한다.

## 22.6 Measure Before Automation

cycle time, intervention, retry, acceptance, review time, cost baseline을 먼저 수집한다.


---

## 필요한 구조 / 그림

1. Minimum Viable Factory reference flow
2. Capability maturity staircase
3. Reliability→Observability→Recovery→Scale→Autonomy sequence

---

## 실전 예제 / 실험

- CI failure fix 하나만 Factory use case로 시작
- 문서 drift 자동 수정과 human review
- single worker에서 안정화 후 2-worker parallel test

---

## 본문에서 의도적으로 다루지 않을 내용

- 완전 autonomous organization
- general agent platform 구축
- 복잡한 maturity scoring

---

## 앞뒤 장 연결

23장에서는 이 Minimum Viable Factory를 작은 reference implementation으로 실제 시나리오까지 연결한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
