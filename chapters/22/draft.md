# 22장. Minimum Viable AI Software Factory

지금까지 책에서는 많은 구성요소를 다뤘다.

- Durable Task
- Control Plane
- Worker
- Harness
- Context
- Verification
- Evidence
- Recovery
- Governance
- Observability
- Platform

이 목록만 보면 Software Factory를 시작하기 전에 거대한 Platform부터 만들어야 할 것처럼 보인다.

그럴 필요는 없다.

오히려 처음부터 Multi-Agent, Automatic Work Selection, Self-improvement까지 넣으면 무엇이 실제로 필요한지 확인하기 어렵다.

첫 Factory는 작아야 한다.

> 반복 가능하고 Acceptance를 정의할 수 있는 한 가지 Work를 안정적으로 처리하는 것부터 시작한다.

---

## 22.1 첫 Use Case를 고른다

첫 Task는 화려할 필요가 없다.

좋은 후보:

- Documentation 수정
- Test 추가
- Dependency Update
- CI Failure Triage
- 작은 Bug Fix
- Static/Lint Fix

공통점:

- Scope가 비교적 좁다.
- 반복해서 발생한다.
- Verification을 만들기 쉽다.
- 실패 Blast Radius가 작다.

나쁜 첫 후보:

- 전체 Architecture 재설계
- 모호한 신규 Product
- Production Emergency Auto-remediation
- Acceptance를 정의하기 어려운 대규모 Refactor

첫 Use Case의 목표는 Agent Capability를 자랑하는 것이 아니다.

Factory Boundary가 실제로 동작하는지 확인하는 것이다.

---

## 22.2 최소 구조

Minimum Viable Factory는 다음 정도면 된다.

~~~text
Human selects Task
        ↓
Durable Task
        ↓
Isolated Worker
        ↓
Coding Agent
        ↓
Deterministic Verification
        ↓
Evidence
        ↓
Human Review
~~~

Agent 하나면 충분하다.

Automatic Backlog Selection도 필요 없다.

Auto-merge도 필요 없다.

그럼에도 Interactive Agent와 다른 중요한 성질이 생긴다.

- Task State가 남는다.
- Worker가 분리된다.
- Verification이 있다.
- Evidence가 남는다.
- 동일 Workflow를 반복할 수 있다.

---

## 22.3 Phase 0: Agent-ready Repository

Factory보다 먼저 Repository를 본다.

다음 질문에 답하기 어렵다면 Agent도 고생한다.

~~~text
Build command는?
Targeted test는?
Environment setup은?
Architecture boundary는?
Generated file은?
Owner는?
~~~

Factory가 Repository Chaos를 자동으로 해결해줄 것이라고 기대하면 안 된다.

오히려 Chaos를 빠르게 반복할 수 있다.

먼저 다음을 정리한다.

- canonical build
- fast test
- setup
- docs
- ownership
- basic runtime

---

## 22.4 Phase 1: Reproducible Worker

다음 목표:

> 같은 Task가 다른 Worker에서도 실행 가능한가?

필요:

- clean checkout
- known runtime
- dependencies
- scoped credential
- test command

아직 Fleet Scheduler는 필요 없다.

Worker 하나가 재현 가능하면 된다.

---

## 22.5 Phase 2: Evidence Contract

Scale 전에 Result Format을 만든다.

~~~text
Task ID
Result Commit
Changed Files
Verification
Artifacts
Known Risk
~~~

이것이 없으면 Worker 수가 늘었을 때 사람이 결과를 비교하기 어려워진다.

---

## 22.6 Phase 3: Durable Task State

다음으로 Work State를 Session 밖으로 꺼낸다.

~~~text
READY
RUNNING
VERIFYING
AWAITING_HUMAN
DONE
FAILED
~~~

Attempt와 Retry도 기록한다.

이 시점부터 Worker Loss와 Task Loss를 분리할 수 있다.

---

## 22.7 Phase 4: Retry와 Resume

Happy Path가 반복적으로 안정적이라면 Failure Recovery를 넣는다.

시험:

~~~text
Worker kill
Network failure
Verification failure
Approval delay
~~~

확인:

- Task State 보존
- Retry Budget 유지
- Evidence 연결
- Duplicate Side Effect 없음

---

## 22.8 Phase 5: Event Trigger

Human이 직접 Start하지 않아도 되는 Work를 연결한다.

예:

- CI Failure
- Issue Status
- Schedule

중요:

~~~text
Auto Start
≠ Auto Merge
~~~

Work Source 자동화와 Acceptance Authority는 별개다.

---

## 22.9 Phase 6: Parallel Worker

Queue가 실제로 쌓이기 시작했을 때 Worker를 늘린다.

먼저 측정한다.

~~~text
Ready Task 충분?
Review Capacity?
CI Capacity?
Conflict Rate?
~~~

이 조건이 없으면 Worker 증가가 가치가 없다.

---

## 22.10 Phase 7: Risk-based Automation

Task Risk에 따라 정책을 다르게 한다.

예:

~~~text
Docs
→ auto verify
→ auto merge possible

Business Logic
→ human review

Auth / Payment / Migration
→ stronger verification
→ specialist approval
~~~

이때부터 Autonomy를 Task Class별로 올린다.

---

## 22.11 Work Selection Automation은 뒤에 둔다

Backlog에서 어떤 Task를 할지 Agent가 고르는 것은 높은 수준의 Autonomy다.

잘못된 Task를 완벽하게 실행해도 가치가 없다.

그래서 보통 다음보다 뒤에 둔다.

~~~text
Reliability
→ Observability
→ Recovery
→ Scale
→ Autonomy
~~~

이 순서는 절대 법칙이 아니라 안전한 도입 후보 순서다.

---

## 22.12 Measure Before Automation

자동화 전 Baseline을 남긴다.

예:

~~~text
cycle time
human intervention
retry
acceptance
review time
CI time
cost
~~~

이 데이터가 없으면 다음 질문에 답하기 어렵다.

> Factory를 도입한 뒤 실제로 좋아졌는가?

---

## 예: CI Failure Fix부터 시작하기

첫 Use Case:

~~~text
CI unit test failure
~~~

Flow:

~~~text
Human selects failure
      ↓
Task
      ↓
Worker
      ↓
Agent diagnosis/fix
      ↓
targeted test
      ↓
Evidence
      ↓
Human Review
~~~

10~20개 Task를 반복한다.

확인:

- First-pass Acceptance
- Retry
- Human Review Time
- False Fix
- Worker Setup Time

문제가 관찰된 뒤에 다음 Capability를 추가한다.

---

## Minimum Viable Factory 체크

~~~text
1. 반복 가능한 Work가 있는가?
2. Acceptance를 자동/반자동으로 확인할 수 있는가?
3. Worker를 재현할 수 있는가?
4. Result Evidence가 표준화돼 있는가?
5. Task State가 Session 밖에 있는가?
6. 실패를 관찰할 수 있는가?
7. Human Review가 감당 가능한가?
~~~

처음부터 7개 모두 완벽할 필요는 없다.

하지만 빠진 것이 무엇인지 알고 시작해야 한다.

---

## 다음 질문

Minimum Viable Factory의 구조는 이해했다.

그렇다면 책 전체 원칙을 실제로 눈으로 확인할 수 있는 작은 Reference Implementation은 어떤 모습이어야 할까.

다음 장에서는 **Reference Factory**를 설계하고 Happy Path보다 Failure Scenario를 중심으로 검증한다.

---

## 참고 자료

- DORA, *Platform Engineering Capability*  
  https://dora.dev/capabilities/platform-engineering/
- CNCF, *Platform Engineering Maturity Model*  
  https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  https://openai.com/index/harness-engineering/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
