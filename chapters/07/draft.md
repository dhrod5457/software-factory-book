# 7장. Control Plane과 Execution Plane

Part II에서는 작업을 실행 가능한 형태로 만들었다. 요구사항과 수용 판단을 정하고, 지속 작업으로 상태를 남기고, 의존 관계 그래프를 만들었다. 이제 실제 실행이 필요하다. 여기서 가장 먼저 분리해야 할 것이 있다.

**작업을 관리하는 시스템**과 **작업을 실행하는 워커**다.

이 책에서는 작업 상태와 흐름을 관리하는 쪽을 제어 계층(Control Plane), 실제 작업을 수행하는 쪽을 실행 계층(Execution Plane)이라고 부른다.

~~~text
Durable Task
      ↓
Control Plane
      ↓
Assignment
      ↓
Execution Plane
      ↓
Result / Evidence
      ↓
Control Plane
~~~

이 경계를 분리하지 않으면 워커가 곧 작업이 된다. 워커가 죽으면 작업도 사라지고, 세션이 끊기면 상태도 끊긴다. 생산 시스템에서는 반대여야 한다.

> 작업의 완료 책임은 워커가 아니라 시스템에 있어야 한다.

---

## 7.1 Control Plane이 관리해야 하는 상태

제어 계층은 코드를 직접 작성하는 주체가 아니다. 주요 책임은 **작업의 상태와 흐름을 관리하는 것**이다. 예를 들면 다음과 같다.

- 작업 생애주기
- 실행 준비가 된 상태 / 진행 불가 상태 상태
- 의존 관계
- 우선순위
- 배정
- 워커 작업 점유권
- 시도
- 재시도
- 승인
- 검증 상태
- 결과 참조
- 이벤트 이력

한 작업을 다음처럼 볼 수 있다.

~~~text
Task T-200
Status: READY
Dependency: T-190 done
Required Worker: backend-java
Risk: medium
~~~

작업 배정기가 워커를 배정하면 상태가 바뀐다.

~~~text
Task T-200
Status: RUNNING
Attempt: A1
Worker: W7
~~~

워커가 코드를 바꾸고 결과를 돌려주면 다시 상태가 바뀐다.

~~~text
Task T-200
Status: VERIFYING
Result Revision: abc123
~~~

검증이 통과했지만 사람의 검토가 필요하면:

~~~text
Task T-200
Status: AWAITING_HUMAN
~~~

이 상태는 에이전트가 자연어로 기억하는 것이 아니라 시스템에 저장된다. 그래야 워커가 바뀌어도 같은 작업을 계속 추적할 수 있다.

---

## 7.2 Execution Plane의 책임

실행 계층은 실제 작업이 일어나는 곳이다. 다음과 같은 요소가 들어간다.

- 저장소 코드 가져오기
- 작업 공간
- 브랜치 / Worktree
- 에이전트 하네스
- 셸
- 빌드 도구
- 테스트 실행기
- 브라우저
- 로컬 서비스
- 임시 파일

실행 계층은 작업을 **수행**한다. 하지만 가능한 한 중단돼도 기록이 남는 실행 조율 상태는 적게 가진다. 예를 들어 워커가 다음 정보를 유일하게 갖고 있으면 위험하다.

~~~text
현재 Task가 무엇인지
Retry가 몇 번째인지
Human Approval이 필요한지
다음 Dependency가 무엇인지
~~~

이 정보는 워커가 아니라 제어 계층이 가져야 한다. 워커는 다음 정도를 받아 실행하면 된다.

~~~text
Task Input
- goal
- scope
- acceptance
- base revision
- worker profile
- verification profile
~~~

그리고 결과를 반환한다.

~~~text
Task Result
- result revision
- changed files
- verification output
- evidence
- failure / blocker
~~~

이 구조가 되면 워커는 교체 가능해진다.

---

## 7.3 Issue Tracker와 Execution State는 같은 것이 아니다

많은 조직에서 이슈 추적 도구는 이미 작업의 출발점이다. 그래서 다음 흐름은 자연스럽다.

~~~text
Issue
→ Factory Task
→ Worker
~~~

OpenAI Symphony나 WorkOS Horizon처럼 이슈 추적 도구를 작업 관리 화면으로 활용하는 공개 사례도 있다. 다만 Symphony의 공개 명세도 작업 배정·재시도·상태 대조와 조정을 위한 실행 조율기가 기준으로 삼는 실행 상태를 별도로 둔다. “이슈 추적 도구를 제어 계층으로 쓴다”는 표현을 실행 상태까지 모두 이슈에 저장한다는 뜻으로 해석하면 안 된다. 하지만 이슈 추적 도구 하나에 모든 실행 상태를 넣으려 하면 문제가 생긴다. 이슈에는 다음 정보가 잘 맞는다.

- 목표
- 우선순위
- 담당자
- 제품 맥락 정보
- 수용 판단
- 의존 관계

반면 다음은 실행 중 자주 변하는 상태다.

- 현재 시도
- 워커 작업 점유권
- 작업 공간 ID
- 검증 실행
- 재시도 횟수
- 실행 기반 실패
- 정상 동작 확인 신호

이런 정보까지 이슈 의견나 사용자 정의 필드로 표현할 수는 있다. 문제는 그것이 항상 좋은 모델은 아니라는 것이다. 실행 상태는 훨씬 더 자주 바뀐다. 관련 상태를 모두 함께 바꾸거나 모두 바꾸지 않는 원자적 갱신(atomic update)이 필요하고, 실패했을 때 어떤 상태로 복구할지도 정해져 있어야 한다. 그래서 실무에서는 다음처럼 나눌 수 있다.

~~~text
Issue Tracker
= Work Intent / Human Collaboration

Task Store
= Durable Execution State

Worker Runtime
= Temporary Execution
~~~

셋이 같은 제품일 수도 있다. 작은 구현에서는 GitHub 이슈의 라벨과 의견을 사람이 사용하는 조작 화면으로 사용할 수도 있다.

~~~text
ready
→ running
→ review
~~~

이렇게 하면 별도 대시보드 없이도 사람이 현재 흐름을 볼 수 있다. 다만 이 편리함 때문에 다음 두 개를 같은 것으로 보면 안 된다.

~~~text
Human-facing State
≠ Authoritative Runtime State
~~~

이슈 라벨은 사람이 이해하기 좋은 요약 표현일 수 있다. 워커 작업 점유권, 재시도 횟수, 시도 이력 같은 실행 의미까지 같은 표현에 억지로 담을 필요는 없다. 중요한 것은 책임을 구분하는 것이다.

---

## 7.4 Scheduler와 Agent를 구분한다

어떤 작업을 언제 누구에게 줄 것인가. 어떤 구현 전략으로 해결할 것인가. 둘은 다른 문제다. 예를 들어 다음 작업이 있다고 하자.

~~~text
T1
- Java backend
- internal network 필요
- auth module
- medium risk
~~~

어느 워커에 배정할지는 다음 정보로 결정할 수 있다.

- 워커 수행 능력
- 대기열
- 의존 관계
- 위험
- 자원 사용 가능 여부

이것은 작업 배정기의 문제다. 반면 워커 안에 들어간 에이전트는 다음을 판단한다.

- 어떤 유형을 먼저 읽을지
- 어떤 테스트를 실행할지
- 예외 매핑을 어디서 바꿀지
- 어떤 구현이 가장 적절한지

이것은 에이전트의 판단이다. 둘을 섞으면 작업 배정기 판단까지 지시문에 들어가기 쉽다.

~~~text
너는 지금 Queue 상태를 보고
적절한 Task를 선택하고
Retry 횟수도 기억하고
필요하면 다른 Worker를...
~~~

이런 구조는 상태가 대화 기록 안에 숨어 버린다. 이미 알고 있는 작업 배정 규칙은 시스템에 두는 편이 낫다.

---

## 7.5 Worker를 disposable하게 만들려면 무엇을 밖으로 꺼내야 하는가

실행 계층을 쓰고 버릴 수 있게 만들고 싶다면 먼저 물어야 한다.

> 워커를 지금 없애도 다시 이어갈 수 있는가?

필요한 상태가 워커 밖에 있어야 한다. 최소한 다음은 외부화하는 편이 좋다.

### Task State

~~~text
Task Store
- status
- attempt
- retry
- approval
~~~

### Source State

~~~text
Git
- base revision
- commit
- branch
~~~

### Partial Work

~~~text
Checkpoint / Patch / Snapshot
~~~

### Verification

~~~text
Verification Result
- command
- exit
- failed tests
- artifact reference
~~~

### Evidence

~~~text
Artifact Store
- screenshot
- log
- benchmark
~~~

워커는 이 중단돼도 남는 상태를 받아 실행을 수행한다. 이 구조가 있으면 다음이 가능하다.

~~~text
Worker A
→ crash

Control Plane
→ detects loss
→ closes Attempt A1
→ creates Attempt A2

Worker B
→ restores Task state
→ continues
~~~

물론 실제로 "계속 진행"하려면 커밋하지 않은 작업까지 어떻게 보존할지 결정해야 한다. 이 문제는 14~15장에서 더 깊게 다룬다. 여기서 중요한 것은 원칙이다.

**연산 자원은 잃을 수 있어도 작업 상태는 잃지 않는다.**

---

## Human Approval을 기다릴 때 Worker를 계속 잡고 있어야 할까

다음 상황을 생각해보자. 에이전트가 운영 환경 마이그레이션 계획을 만들었다. 검증까지 끝났다. 이제 DBA 승인을 기다려야 한다. 워커를 6시간 동안 계속 실행할 이유가 있을까. 제어 계층이 작업 상태를 중단돼도 기록이 남도록 갖고 있다면 다음처럼 할 수 있다.

~~~text
Task
RUNNING
  ↓
VERIFYING
  ↓
AWAITING_HUMAN

Worker
→ released
~~~

승인이 들어오면 새 워커를 배정할 수 있다.

~~~text
Approval Event
      ↓
Task READY
      ↓
New Worker
~~~

이 구조는 사람의 판단을 오래 기다리는 시간을 실행 자원과 분리한다.

---

## Control Plane과 Execution Plane의 최소 경계

최소 기능 생산 시스템이라면 거대한 실행 조율 플랫폼이 없어도 된다. 다음 정도면 시작할 수 있다.

~~~text
Control Plane
- Task DB
- simple queue
- attempt state
- retry count
- approval state

Execution Plane
- one worker process
- isolated worktree
- coding agent
- build/test
~~~

이 정도만으로도 중요한 효과가 생긴다.

- 워커가 작업의 유일한 상태 담당자가 아니다.
- 재시도 이력을 남길 수 있다.
- 사람의 판단을 기다리는 시간에서 워커를 해제할 수 있다.
- 나중에 워커를 여러 개로 확장할 수 있다.

---

## 다음 질문

제어 계층과 실행 계층을 나눴다. 이제 실행 계층 안을 더 자세히 봐야 한다. 워커는 어떤 파일 시스템을 가져야 하는가. 매번 새로 만들 것인가. 의존 패키지와 브라우저를 작업마다 다시 설치할 것인가. 예열된 상태를 재사용하면 무엇이 위험한가. 다음 장에서는 **워커, 격리 환경, 작업 공간**을 다룬다.

---

## 참고 자료

- OpenAI, *An open-source spec for Codex orchestration: Symphony*  
  https://openai.com/index/open-source-codex-orchestration-symphony/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands*  
  https://www.anthropic.com/engineering/managed-agents
- Microsoft, *Durable Task for AI agents*  
  https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents
- *I Built the Simplest Software Factory*, YouTube video / user-provided transcript  
  https://www.youtube.com/watch?v=AsvzMlLyQ38
