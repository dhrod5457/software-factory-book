# 19장 설계 - Observability와 Metrics: 무엇을 측정할 것인가

## 장의 목표

Factory를 운영 가능한 시스템으로 만들기 위해 Task, Attempt, Worker, Verification, Human Interaction을 관찰하고 system-level metric으로 개선하는 방법을 다룬다.

이 장의 핵심 질문:

> Agent가 돌아가고 있다는 것 말고 무엇을 관찰해야 하는가?

> 어떤 지표가 Factory 성능을 가장 잘 설명하는가?

---

## 핵심 주장

> Factory observability의 중심은 raw chain-of-thought가 아니라 externally observable state와 action이다.

> Token, PR count, Agent execution time만으로는 Factory 생산성을 판단할 수 없다.

> Accepted Change, cycle time, human attention, retry/rework를 함께 봐야 한다.

---

## 독자가 얻는 것

- Task/Attempt/Worker/Verification observability model을 만들 수 있다.
- Agent execution time과 human blocking time을 구분할 수 있다.
- Factory dashboard 최소 상태를 정의할 수 있다.
- Cost per Accepted Change 같은 system-level metric을 설계할 수 있다.

---

## 반드시 사용할 Research

- `research/07-observability-metrics-and-economics.md`
- `research/16-productivity-evidence-and-measurement.md`
- `research/17-review-integration-and-throughput-bottlenecks.md`
- `research/28-benchmark-science-and-evaluation-methodology.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Token 사용량 감소를 곧 생산성 향상으로 보는 오류
- Agent success rate만 보고 review/revert를 무시
- raw chain-of-thought 수집을 observability의 핵심으로 보는 접근
- Benchmark 점수를 조직 delivery metric으로 사용

---

# 절 구성

## 19.1 무엇을 관찰할 것인가

Task, Attempt, Worker, Agent turn, Tool call, Verification, Human interaction, Cost, Failure를 계층별로 정의한다.

## 19.2 Task Timeline

READY → RUNNING → VERIFYING → AWAITING_HUMAN → DONE/FAILED의 시간 분해로 queue/execution/review delay를 구분한다.

## 19.3 Factory Metrics

cycle time, queue time, intervention rate, first-pass acceptance, retry, revert, escaped defect를 제시한다.

## 19.4 Human Attention

review minutes, steering minutes, takeover count를 accepted change 단위와 연결한다.

## 19.5 Economics

model + compute + sandbox + CI + review + retry + rework를 포함한 total cost 사고 모델을 설명한다.

## 19.6 Dashboard의 최소 단위

거대한 observability platform보다 Task 상태, Worker, Attempt, Evidence, Failure reason, duration, cost부터 시작한다.


---

## 필요한 구조 / 그림

1. Task timeline decomposition
2. Agent-level metric vs Factory-level metric hierarchy
3. Cost per Accepted Change composition

---

## 실전 예제 / 실험

- Task 실행 10분, Review 대기 8시간인 사례
- Agent A는 token 적지만 retry 4회, Agent B는 token 많지만 first-pass accept인 비용 비교

---

## 본문에서 의도적으로 다루지 않을 내용

- Observability vendor 비교
- LLM tracing product 튜토리얼
- 기업 KPI 전체

---

## 앞뒤 장 연결

20장에서는 Observability에서 들어오는 CI/Production signal이 어떻게 새로운 Task로 변환되는지 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
