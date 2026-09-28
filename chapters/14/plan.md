# 14장 설계 - Failure와 Recovery: 실패를 정상 상태로 설계한다

## 장의 목표

Agent failure를 예외적인 사고가 아니라 정상적인 state transition으로 모델링한다. failure class와 recovery scope를 나누고 가장 작은 단위에서 복구하도록 한다.

이 장의 핵심 질문:

> Agent가 실패했을 때 언제 Retry하고 언제 Reassign하거나 Human에게 올릴 것인가?

> 같은 실패를 무한 반복하지 않으려면 무엇이 필요한가?

---

## 핵심 주장

> Retry는 동일한 명령의 반복이 아니라 failure classification과 budget을 가진 정책이어야 한다.

> Human escalation은 Factory 실패가 아니라 정상적인 recovery state다.

> 가장 작은 recovery scope를 선택할수록 비용과 side effect를 줄일 수 있다.

---

## 독자가 얻는 것

- Failure taxonomy를 만들 수 있다.
- Retry/Restart/Resume/Reassignment를 구분할 수 있다.
- Retry budget과 failure fingerprint를 설계할 수 있다.
- Carryover에 필요한 정보를 정의할 수 있다.

---

## 반드시 사용할 Research

- `research/04-orchestration-task-state-and-continuity.md`
- `research/14-failure-modes-and-antipatterns.md`
- `research/20-durable-execution-and-workflow-reliability.md`
- `research/24-academic-foundations-of-agentic-software-engineering.md`
- `research/26-orchestration-science-control-vs-autonomy.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Infinite Retry
- Infra failure를 코드 Agent에게 보내 수정시키는 오류
- 중단 이유 한 줄만 carryover하고 실제 partial work를 잃는 경우
- Retry와 Reassignment를 같은 것으로 보는 혼동

---

# 절 구성

## 14.1 Failure Taxonomy

tool, harness, worker, network, timeout, verification, permission, drift, environment failure를 구분한다.

## 14.2 Recovery Ladder

Tool Retry → Step Retry → Agent Nudge → Subtask Retry → Worker Restart → Reassignment → Human Escalation 순으로 설명한다.

## 14.3 Retry Budget와 Failure Fingerprint

동일 실패를 반복하지 않도록 fingerprint, max retries, cooldown, escalation 조건을 둔다.

## 14.4 Restart vs Resume vs Reassign

처음부터 다시 하는 것, 중단 지점에서 잇는 것, 다른 Worker가 이어받는 것의 차이를 설명한다.

## 14.5 Carryover Contract

completed work, changed files, uncommitted diff, last verification, failed command, blocker, next action을 포함한다.

## 14.6 Targeted Intervention

Wink 연구를 활용해 full restart보다 observer가 작은 correction을 주는 recovery pattern을 소개한다.


---

## 필요한 구조 / 그림

1. Failure classification → Recovery decision tree
2. Recovery ladder
3. Task/Attempt history with retry budget

---

## 실전 예제 / 실험

- Registry timeout은 infra retry, failing unit test는 Agent fix로 분기
- Worker A가 죽은 뒤 patch/commit을 Worker B가 이어받는 예

---

## 본문에서 의도적으로 다루지 않을 내용

- Durable workflow internals
- Chaos engineering 전체
- incident management 일반론

---

## 앞뒤 장 연결

15장에서는 이 Recovery가 process crash와 long wait를 넘어 동작하게 하는 Durable Execution 기반을 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
