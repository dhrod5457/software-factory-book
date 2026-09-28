# 23장. 실전 Reference Factory 만들기

지금까지의 Architecture가 실제로 필요한지 확인하려면 작은 구현이 필요하다.

단, 목표는 Production-ready Platform을 만드는 것이 아니다.

특정 Vendor SDK 사용법을 배우는 것도 아니다.

이 장에서 제안하는 Reference Factory의 목적은 책에서 설명한 **경계와 Failure Semantics를 실험 가능한 형태로 만드는 것**이다. 여기서 제시하는 Scenario는 아직 보편적인 benchmark가 아니라 구현을 검증하기 위한 acceptance suite 후보다.

그래서 기능 수보다 다음이 중요하다.

- Task가 Session 밖에 남는가
- Worker가 격리되는가
- Verification이 독립적인가
- Evidence가 남는가
- Worker Loss에서 복구되는가
- Conflict를 감지하는가

---

## 23.1 Reference Architecture

최소 Component:

~~~text
Task Store
Queue / Scheduler
Worker
Workspace
Agent Adapter
Verifier
Evidence Store
Human Gate
~~~

Flow:

~~~text
Task Create
→ Queue
→ Assign
→ Worker
→ Agent
→ Verification
→ Evidence
→ Human Gate
→ DONE
~~~

특정 LLM Vendor에 종속되지 않도록 Agent Adapter를 분리한다.

### 작은 구현 사례: GitHub-native Hub-and-Spoke

Reference Architecture를 처음 접하면 별도 Dashboard와 복잡한 Queue부터 필요하다고 느낄 수 있다.

하지만 가장 작은 구현은 기존 개발 Workflow를 Control Surface로 재사용할 수 있다.

한 공개 tutorial에서는 여러 Project Repository의 GitHub Issue를 중앙 Factory가 받아 Worker에 배정하고, 결과 Pull Request를 원래 Repository로 돌려보내는 구조를 사용한다.

~~~text
Repo A ─┐
Repo B ─┼→ Factory Ingress
Repo C ─┘       ↓
             Dispatcher
                ↓
            Worker Fleet
                ↓
       PR → Original Repo
~~~

Issue Label은 사람이 보는 상태를 표현한다.

~~~text
ready
→ factory running
→ factory review
~~~

이 구조의 의미는 GitHub가 반드시 Factory DB가 되어야 한다는 것이 아니다.

7장에서 구분했듯 다음 책임은 여전히 분리해서 생각하는 편이 낫다.

~~~text
Issue / PR
= Work Intent + Human Collaboration + Control Surface

Task Store
= authoritative durable execution state

Worker
= temporary execution
~~~

작은 Factory에서는 이 책임이 한 제품 안에 구현될 수도 있다. Reference Factory에서는 제품 선택보다 **책임 경계가 유지되는지**를 먼저 검증한다.

---

## 23.2 최소 Data Model

### Task

~~~text
id
goal
scope
acceptance
status
dependency
risk
~~~

### Attempt

~~~text
id
task_id
worker_id
status
started_at
ended_at
failure
~~~

### Assignment

~~~text
task_id
worker_id
lease
~~~

### Verification

~~~text
task_id
attempt_id
check
status
artifact
~~~

### Evidence

~~~text
result_revision
changed_files
artifacts
known_risk
~~~

### Approval

~~~text
task_id
state
actor
timestamp
~~~

이 정도면 책의 핵심 구조를 실험할 수 있다.

---

## 23.3 Scenario 1: Normal Success

가장 먼저 Happy Path를 검증한다.

~~~text
Task READY
→ Worker assigned
→ Agent edits
→ commit
→ verification PASS
→ evidence
→ human approve
→ DONE
~~~

검증할 것:

- State Transition 정확
- Result Revision 연결
- Evidence와 Commit 일치
- Worker Release

---

## 23.4 Failure와 Recovery Scenario

**Scenario 2 — Verification Failure**

Agent가 Candidate를 만들었지만 Test가 실패한다.

~~~text
Attempt A1
→ Verification FAIL
~~~

System은 Task를 바로 FAILED로 끝내지 않고 Policy를 본다.

~~~text
retry_count < budget
→ RETRY
→ Attempt A2
~~~

확인:

- A1 history 보존
- Failed Test가 A2 Carryover에 포함
- 같은 Failure 반복 시 escalation

---

**Scenario 3 — Worker Kill**

Task 수행 중 Worker Process를 강제로 죽인다.

예:

~~~text
Agent edited 2 files
unit test PASS
integration pending
→ kill worker
~~~

확인:

- Task가 사라지지 않는가
- Attempt가 Worker Lost로 닫히는가
- Commit/Patch가 남는가
- 새 Worker가 이어갈 수 있는가

이 책의 관점에서는 이 Scenario가 특히 중요하다. Happy Path만으로는 Durable Task와 Worker 교체 가능성의 필요성을 확인하기 어렵기 때문이다.

---

**Scenario 4 — Worker A → Worker B Reassignment**

Worker A의 Partial Work를 Worker B가 이어받는다.

약한 구현:

~~~text
Worker B
→ starts from scratch
~~~

강한 구현:

~~~text
Worker B
→ restores commit/patch
→ reads carryover
→ continues remaining verification
~~~

측정:

~~~text
reused work
lost work
resume time
duplicate work
~~~

---

**Scenario 5 — Human Approval**

Task가 Verification을 통과한다.

~~~text
VERIFYING
→ AWAITING_HUMAN
~~~

Worker를 해제한다.

몇 분 또는 몇 시간 뒤 Approval Event가 들어온다.

~~~text
APPROVED
→ DONE / MERGE
~~~

확인:

- Worker를 계속 점유하지 않음
- Approval State durable
- Approver Audit 남음

---

## 23.5 Parallel과 Conflict Scenario

**Scenario 6 — Independent Parallel Tasks**

Task A와 B가 다른 Module을 수정한다.

~~~text
Task A → Worker A
Task B → Worker B
~~~

둘을 동시에 실행한다.

측정:

- total elapsed time
- conflict
- CI queue
- review load

Parallelism이 실제 이득인지 본다.

---

**Scenario 7 — Same-file Conflict**

Task C와 D가 같은 File을 수정한다.

~~~text
Task C → UserService.java
Task D → UserService.java
~~~

두 Worker가 동시에 작업한다.

Factory는 다음 중 하나를 해야 한다.

- 사전 Serialize
- Conflict 감지
- Replan
- Integration Failure

중요한 것은 Conflict가 “놀라운 사고”가 아니라 예상 가능한 Scenario라는 점이다.

---

## 23.6 Evidence Output

각 Task 결과는 같은 Manifest를 반환한다.

예:

~~~json
{
  "taskId": "T-100",
  "attemptId": "A2",
  "resultRevision": "abc123",
  "changedFiles": [
    "AuthService.java"
  ],
  "verification": [
    {
      "name": "auth-unit",
      "status": "passed"
    }
  ],
  "artifacts": [],
  "knownRisk": []
}
~~~

Human Review 화면은 이 Manifest를 사용한다.

---

## 23.7 Reference Implementation에서 일부러 만들지 않는 것

다음은 없어도 된다.

- 완성된 Web Dashboard
- Kubernetes Cluster
- Multi-region
- Advanced IAM
- 20개 Agent Role
- Auto Product Planning

이 기능들은 Factory 원칙을 검증하는 데 필수적이지 않다.

---

## 23.8 Case Study와 Reference를 구분한다

실제 구현 경험은 유용하다.

예를 들어 한 Factory 구현에서 다음이 관찰됐다고 하자.

~~~text
Worker A loss
→ Task recovered
→ Worker B completed
but
→ Worker A uncommitted work not reused
~~~

이것은 중요한 Continuity Gap 사례다.

하지만 특정 구현의 Failure를 모든 Factory의 일반 사실로 표현하면 안 된다.

책에서는 다음처럼 구분한다.

~~~text
Reference Principle
- cross-worker continuation requires durable partial work

Case Study
- 특정 구현에서는 carryover가 interruption reason만 전달해
  Worker B가 처음부터 다시 작업했다
~~~

자체 구현인 Runmesh의 경험도 같은 방식으로 사용한다. 특정 구현의 결과는 Case Study로 표시하고, 일반 원칙의 근거는 다른 공개 사례·연구와 분리한다.

---

## Reference Factory Acceptance

최소 Acceptance:

~~~text
A. Normal Task completes
B. Verification failure retries within budget
C. Worker kill does not lose Task
D. Different Worker can continue
E. Human Approval can suspend/resume
F. Independent Tasks run in parallel
G. Conflict is detected
H. Evidence is linked to result revision
~~~

이 Scenario를 통과하면 책이 주장하는 핵심 경계가 해당 Reference Implementation에서 동작한다는 근거가 된다. Production readiness나 다른 조직에서의 일반적 우수성을 증명하는 것은 아니다.

---

## 다음 질문

Reference Factory가 동작한다.

그다음에는 무엇을 자동화해야 할까.

Worker를 늘릴까.

Event Trigger를 붙일까.

Agent가 Backlog에서 스스로 Work를 선택하게 할까.

다음 장에서는 Factory의 **Maturity와 Autonomy를 서로 다른 축으로 분리해** 확장 순서를 정리한다.

---

## 참고 자료

- OpenAI, *Symphony*  
  https://openai.com/index/open-source-codex-orchestration-symphony/
- WorkOS, *Project Horizon*  
  https://workos.com/blog/project-horizon
- Microsoft, *Durable Task for AI agents*  
  https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents
- Anthropic, *Effective harnesses for long-running agents*  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- *I Built the Simplest Software Factory*, YouTube video / user-provided transcript  
  https://www.youtube.com/watch?v=AsvzMlLyQ38
