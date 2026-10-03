# 23장. 실전 Reference Factory 만들기

지금까지의 설계 구조가 실제로 필요한지 확인하려면 작은 구현이 필요하다. 단, 목표는 운영에 사용할 수 있는 플랫폼을 만드는 것이 아니다. 특정 공급업체 SDK 사용법을 배우는 것도 아니다. 이 장에서 제안하는 참조 구현(Reference Factory)의 목적은 책에서 설명한 **책임 경계와 실패했을 때의 처리 방식을 실험으로 확인할 수 있게 만드는 것**이다. 여기서 제시하는 시나리오는 보편적인 성능 평가 기준이 아니라 구현이 요구 조건을 만족하는지 확인하기 위한 시험 묶음의 후보다. 그래서 기능 수보다 다음이 중요하다.

- 작업이 세션 밖에 남는가
- 워커가 격리되는가
- 검증이 독립적인가
- 근거가 남는가
- 워커 중단에서 복구되는가
- 충돌을 감지하는가

---

## 23.1 Reference Architecture

최소 구성요소:

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

흐름:

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

특정 LLM 공급업체에 종속되지 않도록 에이전트 연결 어댑터를 분리한다.

### 작은 구현 사례: GitHub-native Hub-and-Spoke

참조 설계 구조를 처음 접하면 별도 대시보드와 복잡한 대기열부터 필요하다고 느낄 수 있다. 하지만 가장 작은 구현은 기존 개발 작업 흐름을 조작 화면으로 재사용할 수 있다. 한 공개 구현 예제에서는 여러 프로젝트 저장소의 GitHub 이슈를 중앙 생산 시스템이 받아 워커에 배정하고, 결과 변경 검토 요청을 원래 저장소로 돌려보내는 구조를 사용한다.

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

이슈 라벨은 사람이 보는 상태를 표현한다.

~~~text
ready
→ factory running
→ factory review
~~~

이 구조의 의미는 GitHub가 반드시 생산 시스템 DB가 되어야 한다는 것이 아니다.

7장에서 구분했듯 다음 책임은 여전히 분리해서 생각하는 편이 낫다.

~~~text
Issue / PR
= Work Intent + Human Collaboration + Control Surface

Task Store
= authoritative durable execution state

Worker
= temporary execution
~~~

작은 생산 시스템에서는 이 책임이 한 제품 안에 구현될 수도 있다. 참조 생산 시스템에서는 제품 선택보다 **책임 경계가 유지되는지**를 먼저 검증한다.

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

가장 먼저 정상 실행 경로를 검증한다.

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

- 상태 전이 정확
- 결과 코드 버전 연결
- 근거와 커밋 일치
- 워커 릴리스

---

## 23.4 Failure와 Recovery Scenario

**시나리오 2 — 검증 실패**

에이전트가 후보를 만들었지만 테스트가 실패한다.

~~~text
Attempt A1
→ Verification FAIL
~~~

시스템은 작업을 바로 FAILED로 끝내지 않고 정책을 본다.

~~~text
retry_count < budget
→ RETRY
→ Attempt A2
~~~

확인:

- A1 이력 보존
- 실패한 테스트가 A2 인계 정보에 포함
- 같은 실패 반복 시 사람에게 판단 요청

---

**시나리오 3 — 워커 강제 종료**

작업 수행 중 워커 프로세스를 강제로 종료한다.

예:

~~~text
Agent edited 2 files
unit test PASS
integration pending
→ kill worker
~~~

확인:

- 작업이 사라지지 않는가
- 시도가 워커 중단으로 닫히는가
- Commit/Patch가 남는가
- 새 워커가 이어갈 수 있는가

이 책의 관점에서는 이 시나리오가 특히 중요하다. 정상 실행 경로만으로는 지속 작업과 워커 교체 가능성의 필요성을 확인하기 어렵기 때문이다.

---

**시나리오 4 — 워커 A에서 워커 B로 재배정**

워커 A의 일부 완료한 작업을 워커 B가 이어받는다.

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

**시나리오 5 — 사람의 승인**

작업이 검증을 통과한다.

~~~text
VERIFYING
→ AWAITING_HUMAN
~~~

워커를 해제한다. 몇 분 또는 몇 시간 뒤 승인 이벤트가 들어온다.

~~~text
APPROVED
→ DONE / MERGE
~~~

확인:

- 워커를 계속 점유하지 않음
- 승인 상태가 중단 뒤에도 유지됨
- 승인자 감사 남음

---

## 23.5 Parallel과 Conflict Scenario

**시나리오 6 — 독립적인 병렬 작업**

작업 A와 B가 다른 모듈을 수정한다.

~~~text
Task A → Worker A
Task B → Worker B
~~~

둘을 동시에 실행한다.

측정:

- 전체 소요 시간
- 충돌
- CI 대기열
- 검토 부담

병렬 실행이 실제 이득인지 본다.

---

**시나리오 7 — 같은 파일의 충돌**

작업 C와 D가 같은 파일을 수정한다.

~~~text
Task C → UserService.java
Task D → UserService.java
~~~

두 워커가 동시에 작업한다. 생산 시스템은 다음 중 하나를 해야 한다.

- 사전 순차 실행
- 충돌 감지
- 재계획
- 통합 실패

중요한 것은 충돌이 “놀라운 사고”가 아니라 예상 가능한 시나리오라는 점이다.

---

## 23.6 Evidence Output

각 작업 결과는 같은 목록 파일을 반환한다.

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

사람의 검토 화면은 이 목록 파일을 사용한다.

---

## 23.7 Reference Implementation에서 일부러 만들지 않는 것

다음은 없어도 된다.

- 완성된 웹 대시보드
- Kubernetes 클러스터
- 여러 지역 배포
- 고급 접근 권한 관리
- 20개 에이전트 역할
- 자동 제품 계획 수립

이 기능들은 생산 시스템 원칙을 검증하는 데 필수적이지 않다.

---

## 23.8 Case Study와 Reference를 구분한다

실제 구현 경험은 유용하다. 예를 들어 한 생산 시스템 구현에서 다음이 관찰됐다고 하자.

~~~text
Worker A loss
→ Task recovered
→ Worker B completed
but
→ Worker A uncommitted work not reused
~~~

이것은 중요한 연속성 단절 사례다. 하지만 특정 구현의 실패를 모든 생산 시스템의 일반 사실로 표현하면 안 된다. 책에서는 다음처럼 구분한다.

~~~text
Reference Principle
- cross-worker continuation requires durable partial work

Case Study
- 특정 구현에서는 carryover가 interruption reason만 전달해
  Worker B가 처음부터 다시 작업했다
~~~

자체 구현인 Runmesh의 경험도 같은 방식으로 사용한다. 특정 구현의 결과는 사례 연구로 표시하고, 일반 원칙의 근거는 다른 공개 사례·연구와 분리한다.

---

## 23.9 Operator Surface

참조 생산 시스템이 내부적으로 작업 저장소, 작업 배정기, 워커, 검증, 승인을 갖추면 사용자가 보는 화면도 복잡하게 만들기 쉽다. 하지만 운영자에게 필요한 핵심 행동은 의외로 적다.

~~~text
Create
Observe
Approve
Intervene
Inspect Evidence
~~~

최근 지속형 에이전트 제품이 복잡한 클라우드 실행 기반과 외부 연결 도구를 단순한 메시지 인터페이스 뒤에 숨기는 것은 중요한 UX 신호다. 생산 시스템도 내부 복잡도를 그대로 사람에게 노출할 필요는 없다. 참조 생산 시스템에서는 다음 구조를 목표로 한다.

~~~text
                Factory Internals
Task Store / Scheduler / Worker / Retry / Policy
Verification / Evidence / Event History
                        ↓
                 Operator Surface
Create | Observe | Approve | Intervene | Inspect
~~~

단순한 화면은 상태를 숨긴다는 뜻이 아니다. 오히려 사용자가 다음 질문에 빠르게 답할 수 있어야 한다.

- 지금 무엇이 실행 중인가
- 어디에서 진행 불가 상태됐는가
- 사람 결정이 필요한 것은 무엇인가
- 에이전트가 무엇을 변경했는가
- 무엇으로 완료를 증명했는가
- 실패하면 어디서 이어지는가

대시보드에 내부에서 일어난 일을 모두 나열하기보다, 사람이 다음 행동을 결정하는 데 필요한 상태와 근거를 먼저 보여주는 것이 중요하다. 생산 시스템 구조가 복잡해질수록 운영자 화면은 더 의도적으로 단순해져야 한다.

## Reference Factory Acceptance

최소 수용 기준:

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

이 시나리오를 통과하면 책이 주장하는 핵심 경계가 해당 참조 구현에서 동작한다는 근거가 된다. 운영 환경 준비 상태나 다른 조직에서의 일반적 우수성을 증명하는 것은 아니다.

---

## 다음 질문

참조 생산 시스템이 동작한다. 그다음에는 무엇을 자동화해야 할까. 워커를 늘릴까. 이벤트 시작 조건을 붙일까. 에이전트가 할 일 목록에서 스스로 작업을 선택하게 할까. 다음 장에서는 생산 시스템의 **성숙도와 자율성을 서로 다른 축으로 분리해** 확장 순서를 정리한다.

---

## 참고 자료

- Cursor, *Grok Bot*  
  https://cursor.com/docs/grok-bot
- Cursor, *Work with Grok Bot*  
  https://cursor.com/docs/grok-bot/work
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
