# 06장 설계 - Task 크기, 분해, Dependency

## 장의 목표

Durable Task를 독립 실행·검증·복구 가능한 단위로 만드는 기준을 다룬다. 작게 쪼개는 것 자체가 목표가 아니라 failure/retry/review boundary를 설계하는 문제로 설명한다.

이 장의 핵심 질문:

> 좋은 Task 크기는 무엇으로 판단할 것인가?

> 언제 Task를 병렬화할 수 있고 언제 순서를 강제해야 하는가?

---

## 핵심 주장

> Task decomposition은 prompt-writing 기법이 아니라 execution graph 설계 문제다.

> 좋은 Task는 독립적으로 실행·검증·복구할 수 있고 review 가능한 결과를 만든다.

> Static decomposition만으로는 retry cost가 줄지 않을 수 있으며 dependency/failure semantics가 중요하다.

---

## 독자가 얻는 것

- Task가 너무 작거나 너무 큰 경우의 비용을 비교할 수 있다.
- Dependency Graph를 구성할 수 있다.
- Retry Scope와 Review Boundary를 Task size에 연결할 수 있다.
- Parallel candidate를 식별할 수 있다.

---

## 반드시 사용할 Research

- `research/04-orchestration-task-state-and-continuity.md`
- `research/10-requirements-specification-and-task-planning.md`
- `research/17-review-integration-and-throughput-bottlenecks.md`
- `research/24-academic-foundations-of-agentic-software-engineering.md`
- `research/26-orchestration-science-control-vs-autonomy.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- ‘작을수록 좋다’는 절대 규칙
- 큰 Feature를 하나의 Agent Task/PR로 끝내는 Giant PR
- Task를 나눴지만 실패 때 downstream 전체를 다시 실행하는 static decomposition

---

# 절 구성

## 06.1 Task Size의 양쪽 비용

작은 Task는 startup/context/orchestration overhead, 큰 Task는 context/failure/review blast radius가 증가함을 설명한다.

## 06.2 독립성 기준

Scope, expected files, validation, external dependency, shared schema를 기준으로 독립 실행 가능성을 판단한다.

## 06.3 Dependency Graph

단순 List보다 DAG가 실제 scheduling과 parallelism에 적합한 이유를 설명한다.

## 06.4 Retry Boundary

Task/subtask 경계가 failed work만 재실행할 수 있게 만드는 구조와 runtime-structured decomposition 연구를 연결한다.

## 06.5 Review Boundary

Large Task가 Large PR일 필요는 없고 stacked/incremental delivery로 reviewability를 확보할 수 있음을 설명한다.

## 06.6 병렬화 후보 판단

같은 파일/schema/architecture decision을 공유하는 Task는 branch가 달라도 독립적이지 않다는 기준을 제시한다.


---

## 필요한 구조 / 그림

1. Task size와 overhead/failure cost의 U자형 개념도
2. Requirement→Task DAG
3. Monolithic / Static Decomposition / Runtime-Structured Decomposition 비교

---

## 실전 예제 / 실험

- Auth 개선을 architecture decision, expired-token fix, refresh-token test, regression으로 분리
- DB schema migration과 API 변경의 dependency graph

---

## 본문에서 의도적으로 다루지 않을 내용

- Multi-Agent 운영 상세
- Scheduler 알고리즘
- WIP/Review queue 상세

---

## 앞뒤 장 연결

7장부터는 정의된 Task를 실제로 운영하는 Control Plane과 Execution Plane 구조로 넘어간다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
