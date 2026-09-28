# 05장 설계 - Durable Task: Session보다 오래 살아남는 작업 단위

## 장의 목표

Factory의 중심 상태 모델을 정의한다. Prompt/Session을 작업 단위로 보는 관점에서 벗어나 Goal, Attempt, Worker, Evidence, Approval, Failure를 가진 Durable Task를 설계한다.

이 장의 핵심 질문:

> 왜 Agent Session이 아니라 Task가 Factory의 기본 단위여야 하는가?

> Task에 어떤 상태를 남겨야 다른 Worker가 이어받을 수 있는가?

---

## 핵심 주장

> Agent Session은 ephemeral할 수 있지만 Task State는 ephemeral하면 안 된다.

> Task는 Goal뿐 아니라 Attempts, Verification, Evidence, Approval, Failure history를 포함해야 운영 단위가 된다.

> Context Window는 durable state 저장소가 아니다.

---

## 독자가 얻는 것

- Prompt, Session, Task를 구분할 수 있다.
- Durable Task의 최소 필드를 설계할 수 있다.
- Task 상태 전이를 정의할 수 있다.
- Attempt와 Task 결과를 분리할 수 있다.

---

## 반드시 사용할 Research

- `research/02-factory-architecture-patterns.md`
- `research/04-orchestration-task-state-and-continuity.md`
- `research/20-durable-execution-and-workflow-reliability.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Chat history를 작업 이력 전체로 사용하는 패턴
- Worker process가 죽으면 Task도 유실되는 구조
- Retry 때 Task 자체를 새로 만들어 이력을 끊는 구조

---

# 절 구성

## 05.1 Prompt, Session, Task

세 단위의 lifetime과 책임을 비교한다. Prompt는 interaction, Session은 execution context, Task는 durable work item으로 정의한다.

## 05.2 Task 최소 스키마

ID, Goal, Scope, Acceptance, Dependency, Status, Attempt, Worker, Workspace, Revision, Verification, Evidence, Approval, Failure/Carryover를 설명한다.

## 05.3 Task와 Attempt 분리

한 Task가 여러 Attempt를 가질 수 있고 실패 Attempt도 audit/evidence로 남아야 하는 이유를 설명한다.

## 05.4 상태 전이

READY → RUNNING → VERIFYING → AWAITING_HUMAN → DONE과 BLOCKED/FAILED/RETRY 경로를 제시한다.

## 05.5 Task가 Worker보다 오래 살아야 하는 이유

Worker loss, daemon restart, reassignment 상황에서 authoritative state가 외부에 있어야 함을 설명한다.

## 05.6 Carryover

중단 이유뿐 아니라 completed work, changed files, uncommitted changes, latest verification, blockers, next action이 필요함을 소개한다.


---

## 필요한 구조 / 그림

1. Prompt vs Session vs Task lifetime 비교
2. Task / Attempt / Worker 관계 ER 스타일 그림
3. Task state machine

---

## 실전 예제 / 실험

- Worker A가 중단된 뒤 Worker B가 동일 Task를 이어받는 상태 예
- Verification failure 후 Attempt 1을 닫고 Attempt 2를 생성하는 예

---

## 본문에서 의도적으로 다루지 않을 내용

- Scheduler 구현
- workflow engine event sourcing internals
- Task decomposition 상세

---

## 앞뒤 장 연결

6장에서는 Durable Task를 어떤 크기로 나누고 Dependency Graph를 어떻게 구성할지 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
