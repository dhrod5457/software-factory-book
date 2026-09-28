# 15장 설계 - Durable Execution: Crash를 넘어 이어지는 Work

## 장의 목표

Long-running Agent 작업을 distributed systems 문제로 바라보고 state persistence, event history, checkpoint, idempotency, async human wait를 설명한다.

이 장의 핵심 질문:

> Agent memory를 저장하는 것과 실행을 복구하는 것은 왜 다른가?

> 외부 side effect가 있는 Tool을 안전하게 Retry하려면 무엇이 필요한가?

---

## 핵심 주장

> Memory와 Durable Execution은 다른 문제다.

> Long-running Agent는 crash, deploy, timeout, human wait를 견디는 workflow reliability layer가 필요하다.

> Duplicate side effect를 막으려면 idempotency와 operation identity가 Tool contract에 들어가야 한다.

---

## 독자가 얻는 것

- Durable Execution의 책임을 설명할 수 있다.
- Checkpoint와 event history를 구분할 수 있다.
- Idempotent tool design을 이해할 수 있다.
- Human approval을 asynchronous event로 모델링할 수 있다.

---

## 반드시 사용할 Research

- `research/20-durable-execution-and-workflow-reliability.md`
- `research/04-orchestration-task-state-and-continuity.md`
- `research/24-academic-foundations-of-agentic-software-engineering.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Context transcript를 저장했으니 resume 가능하다고 가정
- 외부 API 성공 후 응답 유실 상황에서 무조건 retry
- Approval wait 동안 worker/process를 계속 점유

---

# 절 구성

## 15.1 Memory ≠ Execution State

conversation context와 completed step/side effect history를 구분한다.

## 15.2 Event History와 Checkpoint

어떤 일이 이미 완료되었는지 기록하고 재시작 시 어디부터 이어갈지 결정하는 원리를 설명한다.

## 15.3 Idempotency와 Duplicate Side Effect

PR create, deploy, email, DB mutation에서 operation_id/deduplication이 필요한 이유를 예로 든다.

## 15.4 Human Wait

ApprovalRequested 후 worker를 해제하고 event 수신 시 resume하는 async pattern을 설명한다.

## 15.5 Durable Runtime 사례

Temporal, Durable Task, Google Agent Executor를 제품 튜토리얼이 아니라 책임 분리 사례로 소개한다.

## 15.6 Crash Test

worker kill, daemon restart, network disconnect를 deliberate acceptance scenario로 만들 것을 제안한다.


---

## 필요한 구조 / 그림

1. Agent Harness vs Durable Workflow Runtime layer
2. External API partial-success duplicate side effect sequence
3. Approval suspend/resume sequence

---

## 실전 예제 / 실험

- PR create operation_id로 duplicate PR 방지
- Worker kill 후 event history 기준 resume
- 24시간 후 human approval이 들어와 Task 재개

---

## 본문에서 의도적으로 다루지 않을 내용

- Temporal/Durable Task API 튜토리얼
- distributed consensus
- event sourcing 구현 상세

---

## 앞뒤 장 연결

16장에서는 Durable하게 오래 일하는 Agent에 어떤 권한과 보안 경계를 부여해야 하는지 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
