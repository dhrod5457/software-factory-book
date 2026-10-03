# 8장. Worker, Sandbox, Workspace

제어 계층이 작업을 관리한다면 실행 계층은 작업을 실제로 수행한다. 그 중심에 워커가 있다. 워커를 단순히 “에이전트가 실행되는 컴퓨터”라고 보면 설계가 부족해진다. 생산 시스템에서 워커는 다음 요소가 묶인 실행 단위에 가깝다.

~~~text
Worker
=
Workspace
+ Runtime
+ Tools
+ Network
+ Temporary State
~~~

좋은 워커는 빠를 뿐 아니라 같은 환경으로 다시 만들 수 있어야 한다. 다른 작업이 남긴 흔적에 영향을 받지 않아야 하고, 필요할 때는 상태를 오랫동안 유지할 수도 있어야 한다. 이 장의 핵심은 하나다.

> 재사용해야 하는 환경과 항상 새로 시작해야 하는 작업 상태를 구분한다.

---

## 8.1 무엇을 격리해야 하는가

에이전트가 파일을 수정하고 셸 명령을 실행하려면 독립된 작업 공간이 필요하다. 먼저 브랜치는 소스 이력을 분리하지만 실행환경을 격리하지는 않는다.

~~~text
shared filesystem
├─ branch A
└─ branch B
~~~

같은 작업 디렉터리를 공유한다면 독립 작업 공간이라고 보기 어렵다. Worktree나 독립 복제본부터 파일 시스템 수준의 작업 공간을 나눌 수 있다.

~~~text
repo/
├─ worktree-task-a/
└─ worktree-task-b/
~~~

파일 변경 충돌을 줄일 수 있다. 하지만 프로세스, 포트, 환경 변수, 캐시는 여전히 공유될 수 있다. 컨테이너나 VM을 사용하면 격리 범위가 더 커진다.

~~~text
Task
→ isolated filesystem
→ isolated process
→ controlled network
→ scoped credential
~~~

어떤 방식을 써야 하는지는 작업 위험과 환경 복잡도에 따라 달라진다. 중요한 것은 “무엇을 격리해야 하는가”를 명확히 하는 것이다. 예를 들어 다음은 서로 다른 경계다.

- 소스 파일
- 프로세스
- 네트워크
- 인증 정보
- 포트
- 데이터베이스
- 브라우저 구성
- 임시 캐시

코드만 분리하고 브라우저 세션은 공유하면 한 에이전트의 로그인 상태가 다른 에이전트 테스트에 영향을 줄 수 있다. 작업 공간 격리는 Git 문제만이 아니다.

---

## 8.2 Prepared Environment

완전히 깨끗한 환경은 안전하지만 느릴 수 있다. 매 작업마다 다음을 처음부터 설치한다고 해보자.

- JDK
- Node
- 브라우저
- Playwright
- Gradle 의존 패키지
- npm 묶음
- 시스템 묶음

에이전트가 실제 수정에 5분을 쓰는데 환경 준비에 20분이 걸릴 수 있다. 그래서 워커에는 미리 준비된 환경이 필요하다.

예:

~~~text
Worker Profile: backend-java

Runtime
- JDK 21
- Gradle
- PostgreSQL client

Cache
- Gradle dependency

Tools
- git
- rg
- curl

Network
- artifact registry
- staging API
~~~

브라우저 작업은 다른 구성을 가질 수 있다.

~~~text
Worker Profile: browser-e2e

Runtime
- Node
- Chromium
- Playwright

Tools
- screenshot
- trace viewer

Network
- staging frontend
~~~

이렇게 하면 에이전트가 작업마다 환경 설치 방법부터 추론할 필요가 줄어든다.

---

### Prepared Snapshot과 Fresh Task State

미리 준비된 환경을 실제 운영 형태로 만들 때는 이미지나 스냅샷을 사용할 수 있다. 한 공개 구현 예제에서는 코딩 에이전트 실행 기반, 스킬, 브라우저 도구, MCP 서버, `AGENTS.md` 같은 정적 실행 자산을 재사용 가능한 스냅샷에 넣고 새 워커를 그 환경에서 생성한다. 특정 공급업체 방식이 표준이라는 뜻은 아니다. 중요한 것은 **환경의 재사용 단위와 작업의 새로운 상태를 분리했다는 점**이다.

~~~text
Reusable Worker Image / Snapshot
- runtime
- coding agent runtime
- tools
- browser
- skills
- MCP integration
- static instructions

Fresh per Task
- source revision
- workspace
- task input
- scoped credential
- uncommitted work
- test state
- temporary service data
~~~

이 구분이 무너지면 스냅샷은 빠른 초기 준비 수단이 아니라 오래된 작업 상태를 복제하는 수단이 된다. 따라서 미리 준비된 환경의 목표는 "항상 같은 워커를 유지하는 것"이 아니라 다음에 가깝다.

> **같은 실행 능력은 재현하고, 작업 상태는 새로 시작한다.**

---

## 8.3 Fresh State와 Cache를 구분한다

환경을 재사용하기 시작하면 새로운 위험이 생긴다. 캐시와 작업 상태가 섞이는 것이다. 다음은 재사용하기 좋다.

- 묶음 내려받기 캐시
- 컨테이너 이미지
- 설치된 컴파일러
- 브라우저 실행 파일
- 빌드 도구

반면 다음은 주의가 필요하다.

- 가져온 소스
- 커밋하지 않은 변경
- 생성 파일
- 로컬 데이터베이스 데이터
- 브라우저 세션
- 테스트 결과
- 임시 파일
- 실행 중인 프로세스

예를 들어 이전 작업이 로컬 Redis에 값을 남겼다고 하자. 다음 작업의 테스트가 같은 Redis를 사용한다. 테스트는 PASS했다. 하지만 깨끗한 환경에서는 실패할 수 있다. 이런 상태 오염은 에이전트에게 더 위험하다. 에이전트는 환경이 오염됐는지 모르고 코드가 맞다고 판단할 수 있기 때문이다. 그래서 다음 경계를 유지하는 편이 좋다.

~~~text
Reusable
- runtime
- tool
- dependency cache

Fresh per Task
- source revision
- workspace
- task input
- test state
- temporary service data
~~~

물론 실제 시스템에서는 일부 실행 상태를 의도적으로 유지할 수도 있다. 그 경우에도 그것이 판단의 기준이 되는 작업 상태가 되어서는 안 된다.

---

## 8.4 Ephemeral Worker와 Persistent Worker

워커 운영에는 두 방향이 있다.

### Ephemeral Worker

작업마다 새로 만든다.

~~~text
Task
→ provision
→ execute
→ collect result
→ destroy
~~~

장점:

- 깨끗한 상태
- 재현성
- 격리
- 낮은 작업 간 상태 오염

적합한 경우:

- 독립적인 버그 수정
- CI와 비슷한 작업
- 보안 민감 작업
- 짧은 작업

단점:

- 처음부터 시작하는 비용
- 의존 패키지 복원
- 큰 저장소 코드 가져오기 비용
- 복잡한 실행환경 준비

### Persistent Worker

워커를 유지하고 여러 작업을 처리한다.

~~~text
Worker
→ Task A
→ Task B
→ Task C
~~~

장점:

- 예열된 캐시
- 실행 중인 서비스 유지
- 복잡한 환경 재사용
- 긴 프로젝트 연속성

단점:

- 오래된 의존 패키지
- 상태 오염
- 인증 정보 누적
- 재현성 저하

둘 중 하나가 항상 정답은 아니다. 공개된 에이전트 시스템에서도 계속 유지하는 환경과 쓰고 버리는 격리 환경이 모두 사용된다. 제품의 유행보다 작업 환경을 준비하는 비용, 이전 작업의 흔적이 남을 위험, 보안을 위해 분리해야 할 범위, 같은 환경을 다시 만들 수 있는지를 기준으로 선택해야 한다. 예를 들어 Android 빌드처럼 초기 환경 준비가 매우 비싸다면 지속형 워커가 유리할 수 있다. 반대로 신뢰할 수 없는 외부 변경 검토 요청을 분석한다면 일회성 워커가 더 적합할 수 있다.

---

## 8.5 Persistent Worker를 쓸 때 가장 조심할 것

지속형 워커의 편리함 때문에 다음 상태까지 워커에 맡기기 쉽다.

~~~text
현재 Task
진행 상황
승인 상태
다음 행동
~~~

이렇게 되면 워커가 다시 제어 계층이 된다. 지속형 워커는 **예열된 환경**을 제공할 수 있다. 하지만 작업 상태의 기준 원본이 되어서는 안 된다. 구분하면 다음과 같다.

~~~text
Worker may keep
- compiler
- dependency cache
- browser binary
- local repo mirror

Control Plane keeps
- task status
- attempt
- acceptance
- approval
- retry
- evidence reference
~~~

워커가 오래 살아도 작업 상태는 외부에 남는다.

---

## 8.6 Worker Profile

모든 작업이 같은 워커를 필요로 하지는 않는다. 예를 들어 다음 네 작업을 생각해보자.

~~~text
T1 Java API fix
T2 React browser E2E
T3 Android build
T4 GPU model benchmark
~~~

같은 워커 이미지로 모두 처리하려고 하면 환경이 거대해진다. 대신 수행 능력 구성을 정의할 수 있다.

~~~text
backend-java
browser-e2e
android
gpu
internal-network
~~~

작업은 필요한 수행 능력을 선언한다.

~~~text
Task T1
requires:
- backend-java
- internal-network
~~~

작업 배정기는 맞는 워커를 찾는다. 이렇게 하면 “백엔드 에이전트”, “프런트엔드 에이전트”처럼 역할만 자연어로 나누는 것보다 실행환경까지 명확하게 연결할 수 있다.

---

## 예: Java Backend Worker와 Browser Worker

백엔드 작업:

~~~text
Goal
- expired JWT → 401

Worker Profile
- JDK 21
- Gradle
- PostgreSQL
- internal artifact registry

Verification
- unit
- integration
~~~

브라우저 작업:

~~~text
Goal
- login error message 확인

Worker Profile
- Node
- Chromium
- Playwright

Verification
- E2E
- screenshot
~~~

두 작업은 모델이 같아도 필요한 실행 기반과 도구가 다르다. 생산 시스템에서 워커 선택은 에이전트의 성격이 아니라 **실행 능력**을 기준으로 볼 수 있다.

---

## Stale Browser State가 만든 잘못된 PASS

지속형 브라우저 워커에서 이전 작업의 로그인 세션이 남았다고 하자. 새 작업은 로그인하지 않은 사용자의 오류 화면을 검증해야 한다. 하지만 브라우저 쿠키가 남아 있어서 인증된 화면이 열린다. 에이전트는 DOM과 화면 캡처를 보고 정상으로 판단할 수 있다. 이 문제는 모델 성능이 아니다. 워커 상태 문제다. 해결 방법은 다음처럼 다양하다.

- 작업마다 브라우저 구성 초기화
- cookie/storage clear
- 깨끗한 테스트 계정
- 일회성 브라우저 워커
- 실행 상태 검사 합계

중요한 것은 실패 유형을 구분하는 것이다. 코드가 틀렸는지, 환경이 오염됐는지 분리하지 않으면 에이전트는 잘못된 방향으로 수정할 수 있다.

---

## Worker를 설계할 때 묻는 질문

다음 질문으로 시작할 수 있다.

~~~text
1. 어떤 filesystem state가 Task마다 fresh해야 하는가?
2. 어떤 cache는 재사용해도 되는가?
3. 어떤 credential을 Worker가 가져야 하는가?
4. Network access는 어디까지 필요한가?
5. Worker를 죽였을 때 다시 만들 수 있는가?
6. 동일 Task를 다른 Worker에서도 재현할 수 있는가?
7. 어떤 capability profile이 필요한가?
~~~

이 질문에 답하면 워커가 단순한 “원격 개발 머신”에서 생산 시스템의 실행 단위로 바뀐다.

---

## 다음 질문

좋은 워커를 만들었다고 에이전트가 자동으로 잘 일하는 것은 아니다. 같은 모델과 같은 저장소를 사용해도 도구의 형태, 지시사항, 탐색 결과, 오류 피드백에 따라 행동이 달라진다. 다음 장에서는 모델 주변에서 에이전트의 실제 작업 능력을 만드는 **하네스 설계**를 다룬다.

---

## 참고 자료

- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands*  
  https://www.anthropic.com/engineering/managed-agents
- Cursor, *Cloud Agents*  
  https://cursor.com/docs/cloud-agent
- OpenHands, *Software Agent SDK*  
  https://github.com/OpenHands/software-agent-sdk
- *I Built the Simplest Software Factory*, YouTube video / user-provided transcript  
  https://www.youtube.com/watch?v=AsvzMlLyQ38
