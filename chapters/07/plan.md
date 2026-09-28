# 07장 설계 - Control Plane과 Execution Plane

## 장의 목표

AI Software Factory의 핵심 architecture boundary를 정의한다. Durable Task의 authoritative state를 관리하는 Control Plane과 실제 코드/도구 실행이 일어나는 Execution Plane을 분리해 이해시킨다.

이 장의 핵심 질문:

> Task의 완료 책임은 Worker에게 있는가, 시스템에게 있는가?

> 왜 Orchestrator와 Agent Runtime을 분리해야 하는가?

---

## 핵심 주장

> Control Plane이 Task lifecycle과 completion responsibility를 소유하고 Worker는 교체 가능한 execution resource여야 한다.

> Task state와 execution compute를 분리하면 crash/reassignment/retry를 설계하기 쉬워진다.

---

## 독자가 얻는 것

- Control Plane과 Execution Plane의 책임을 구분할 수 있다.
- Task scheduler, assignment, retry, approval을 Agent prompt 밖으로 뺄 수 있다.
- Worker loss가 Task loss로 이어지지 않는 구조를 설계할 수 있다.

---

## 반드시 사용할 Research

- `research/02-factory-architecture-patterns.md`
- `research/04-orchestration-task-state-and-continuity.md`
- `research/19-boundaries-devops-platform-engineering-agent-platform.md`
- `research/20-durable-execution-and-workflow-reliability.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Agent session 자체를 control plane으로 사용하는 구조
- Worker local state만 authoritative하게 두는 구조
- Issue tracker만으로 runtime execution state까지 모두 표현하려는 과도한 단순화

---

# 절 구성

## 07.1 Control Plane이 관리해야 하는 상태

Task lifecycle, readiness, dependency, scheduling, assignment, retry, approval, result, event history를 정리한다.

## 07.2 Execution Plane의 책임

Workspace, Agent harness, tools, build/test, browser/service execution을 담당하고 durable business state는 최소화한다.

## 07.3 Issue Tracker와 Execution State

Issue가 work intake/control input이 될 수 있지만 worker lease, attempt, verification state까지 담기 어려운 이유를 설명한다.

## 07.4 Scheduler와 Agent를 구분한다

어떤 Task를 언제 누구에게 줄지는 control decision이고, Task 내부 구현 전략은 Agent judgment라는 경계를 설명한다.

## 07.5 Disposable Execution

Worker를 교체 가능한 자원으로 만들려면 어떤 state가 외부화되어야 하는지 Task/Workspace/Artifact 관점에서 설명한다.


---

## 필요한 구조 / 그림

1. Control Plane ↔ Execution Plane architecture
2. Task → Assignment → Worker → Result → Task state 흐름
3. Issue Tracker / Task Store / Worker Runtime 경계

---

## 실전 예제 / 실험

- Worker process kill 후 새 Worker가 Task Store에서 상태를 읽고 재시작하는 흐름
- Human approval 대기 동안 Worker를 해제하고 Task만 AWAITING_HUMAN으로 유지하는 예

---

## 본문에서 의도적으로 다루지 않을 내용

- 구체 Scheduler 알고리즘
- 분산 합의
- 특정 orchestration 제품 사용법

---

## 앞뒤 장 연결

8장에서는 Execution Plane의 핵심 단위인 Worker, Sandbox, Workspace를 구체화한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
