# 17장 설계 - Parallel Worker와 Multi-Agent: 언제 병렬화할 것인가

## 장의 목표

여러 Agent를 동시에 실행하면 무조건 throughput이 증가한다는 가정을 버리고 Task independence, ownership, merge conflict, correlated error를 기준으로 useful parallelism을 판단한다.

이 장의 핵심 질문:

> 어떤 Task는 병렬화하고 어떤 Task는 순차 실행해야 하는가?

> Multi-Agent가 Single Agent보다 나빠질 수 있는 이유는 무엇인가?

---

## 핵심 주장

> 병렬화의 대상은 Agent가 아니라 독립 Task다.

> Agent 수 증가에는 coordination, duplicated context, merge conflict, shared-resource cost가 따른다.

> 동일 model/context의 여러 Agent는 독립 의견이 아니라 correlated error를 만들 수 있다.

---

## 독자가 얻는 것

- Parallel candidate를 식별할 수 있다.
- Fan-out/Fan-in 구조를 설계할 수 있다.
- Ownership/Dependency/Conflict를 scheduling input으로 사용할 수 있다.
- Planner/Evaluator 역할과 Worker parallelism을 구분할 수 있다.

---

## 반드시 사용할 Research

- `research/02-factory-architecture-patterns.md`
- `research/14-failure-modes-and-antipatterns.md`
- `research/17-review-integration-and-throughput-bottlenecks.md`
- `research/18-research-contradictions-and-open-questions.md`
- `research/26-orchestration-science-control-vs-autonomy.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- More Agents = More Throughput
- Same-model Committee를 독립 검증으로 보는 오류
- shared schema/core file 작업을 동시에 배정
- 제한 resource polling으로 stampede 발생

---

# 절 구성

## 17.1 Useful Parallelism의 조건

독립 scope, low file overlap, independent verification, no strict dependency를 기준으로 제시한다.

## 17.2 Fan-out / Fan-in

같은 base revision에서 여러 Task를 실행하고 integration/verification에서 다시 합치는 구조를 설명한다.

## 17.3 Ownership과 Conflict

file/module/schema ownership을 scheduling signal로 사용하되 완벽한 예측은 불가능하므로 runtime conflict detection도 필요함을 설명한다.

## 17.4 Correlated Error

동일 model/context agent가 같은 mistake를 반복할 수 있음을 Anthropic 연구로 설명한다.

## 17.5 Parent/Subagent와 Task Worker

한 Task 내부 subagent 분해와 여러 durable Task worker parallelism을 구분한다.

## 17.6 Concurrency Budget

Worker count뿐 아니라 CI, review, shared API, cost capacity를 함께 고려한다.


---

## 필요한 구조 / 그림

1. Task DAG에서 parallelizable branches 표시
2. Fan-out/Fan-in with integration gate
3. Useful Parallelism = work - conflict/duplication/review overload 개념식

---

## 실전 예제 / 실험

- Backend unit test, frontend E2E, docs를 병렬 실행
- 세 Agent가 같은 UserService를 바꾸며 conflict 나는 사례
- Evaluator Agent를 다른 context/model로 분리하는 예

---

## 본문에서 의도적으로 다루지 않을 내용

- Swarm/debate framework 비교
- dynamic team formation
- market-based scheduling

---

## 앞뒤 장 연결

18장에서는 Parallel Worker가 만든 결과가 Review/CI/Integration 단계에서 새로운 병목을 만드는 문제를 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
