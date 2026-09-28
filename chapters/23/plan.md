# 23장 설계 - 실전 Reference Factory 만들기

## 장의 목표

앞 장의 원칙을 작은 reference implementation으로 통합한다. 특정 vendor 제품 튜토리얼이 아니라 Task state, Worker isolation, Agent execution, Verification, Evidence, Human Gate, Recovery를 눈으로 확인할 수 있는 실험 시스템을 설계한다.

이 장의 핵심 질문:

> 책의 원칙을 최소 코드로 어떻게 검증할 것인가?

> Happy path뿐 아니라 어떤 실패 시나리오를 반드시 실험해야 하는가?

---

## 핵심 주장

> Reference Factory의 목적은 기능 수가 아니라 핵심 경계와 failure semantics를 재현하는 것이다.

> 실전 예제는 normal success보다 worker loss, verification failure, reassignment, conflict를 보여줘야 한다.

> Runmesh 같은 실제 구현 경험은 case study로 활용하되 책의 표준 정답으로 만들지 않는다.

---

## 독자가 얻는 것

- Reference Factory의 최소 component를 설계할 수 있다.
- Task/Attempt/Worker/Evidence data flow를 실제로 연결할 수 있다.
- Crash/retry/reassignment acceptance test를 작성할 수 있다.
- 특정 vendor 종속성을 최소화한 예제를 구성할 수 있다.

---

## 반드시 사용할 Research

- `research/02-factory-architecture-patterns.md`
- `research/04-orchestration-task-state-and-continuity.md`
- `research/05-verification-evidence-and-human-gates.md`
- `research/20-durable-execution-and-workflow-reliability.md`
- `research/23-minimum-viable-ai-software-factory.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Happy path demo만 보여주는 실전 장
- Agent UI 데모를 Factory 구현으로 착각
- Reference implementation을 production-ready platform으로 과장
- 실험 결과를 보편적 산업 사실로 일반화

---

# 절 구성

## 23.1 Reference Architecture

Task Store, Queue/Scheduler, Worker, Workspace, Agent Adapter, Verifier, Evidence Store, Human Gate의 최소 component를 정의한다.

## 23.2 Data Model

Task, Attempt, Assignment, Verification, Artifact/Evidence, Approval의 관계를 최소 스키마로 만든다.

## 23.3 Normal Success

Task create → assign → work → verify → evidence → approve → done 전체 흐름을 먼저 검증한다.

## 23.4 Failure Scenarios

verification fail → retry, worker kill → resume, worker A loss → B reassign, approval wait를 실험한다.

## 23.5 Parallel / Conflict

독립 Task 2개 병렬과 same-file conflict를 모두 실행해 useful parallelism의 차이를 보여준다.

## 23.6 Evidence Output

commit, changed files, command results, screenshot/log artifact 등을 하나의 manifest로 반환한다.

## 23.7 Case Study와 Reference 구분

실제 Runmesh 경험의 continuity gap, approval, isolation 사례를 ‘관찰 사례’로 소개하되 구현 의존성을 제거한다.


---

## 필요한 구조 / 그림

1. Reference Factory component diagram
2. Task/Attempt/Worker data model
3. Acceptance scenario sequence diagrams

---

## 실전 예제 / 실험

- Worker kill 중간 주입 후 DONE까지 continuity 측정
- 두 Task가 서로 다른 module을 수정할 때 parallel success
- same file 수정 시 conflict detection 후 serialize/replan

---

## 본문에서 의도적으로 다루지 않을 내용

- 완전한 웹 대시보드
- Kubernetes production deployment
- 특정 LLM SDK 사용법 전체
- Runmesh 제품 매뉴얼

---

## 앞뒤 장 연결

24장에서는 Reference Factory를 어떤 maturity/autonomy 순서로 확장할지 조직 관점의 roadmap으로 정리한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
