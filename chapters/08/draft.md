# 8장. Worker, Sandbox, Workspace

Control Plane이 Task를 관리한다면 Execution Plane은 Task를 실제로 수행한다.

그 중심에 Worker가 있다.

Worker를 단순히 “Agent가 실행되는 컴퓨터”라고 보면 설계가 부족해진다.

Factory에서 Worker는 다음 요소가 묶인 실행 단위에 가깝다.

~~~text
Worker
=
Workspace
+ Runtime
+ Tools
+ Network
+ Temporary State
~~~

좋은 Worker는 빠르기만 해서는 안 된다.

다시 만들 수 있어야 하고, 다른 Task의 흔적에 오염되지 않아야 하며, 필요한 경우 장시간 상태를 유지할 수도 있어야 한다.

이 장의 핵심은 하나다.

> 재사용해야 하는 환경과 항상 새로 시작해야 하는 Work State를 구분한다.

---

## 8.1 무엇을 격리해야 하는가

Agent가 파일을 수정하고 Shell 명령을 실행하려면 독립된 Workspace가 필요하다.

먼저 Branch는 source history를 분리하지만 실행환경을 격리하지는 않는다.

~~~text
shared filesystem
├─ branch A
└─ branch B
~~~

같은 working directory를 공유한다면 독립 Workspace라고 보기 어렵다. Worktree나 독립 Clone부터 filesystem 수준의 작업 공간을 나눌 수 있다.

~~~text
repo/
├─ worktree-task-a/
└─ worktree-task-b/
~~~

파일 변경 충돌을 줄일 수 있다.

하지만 process, port, environment variable, cache는 여전히 공유될 수 있다.

Container나 VM을 사용하면 격리 범위가 더 커진다.

~~~text
Task
→ isolated filesystem
→ isolated process
→ controlled network
→ scoped credential
~~~

어떤 방식을 써야 하는지는 Task 위험과 환경 복잡도에 따라 달라진다.

중요한 것은 “무엇을 격리해야 하는가”를 명확히 하는 것이다.

예를 들어 다음은 서로 다른 경계다.

- source file
- process
- network
- credential
- port
- database
- browser profile
- temporary cache

코드만 분리하고 Browser Session은 공유하면 한 Agent의 Login 상태가 다른 Agent 테스트에 영향을 줄 수 있다.

Workspace Isolation은 Git 문제만이 아니다.

---

## 8.2 Prepared Environment

완전히 깨끗한 환경은 안전하지만 느릴 수 있다.

매 Task마다 다음을 처음부터 설치한다고 해보자.

- JDK
- Node
- Browser
- Playwright
- Gradle dependency
- npm package
- system package

Agent가 실제 수정에 5분을 쓰는데 환경 준비에 20분이 걸릴 수 있다.

그래서 Worker에는 미리 준비된 Environment가 필요하다.

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

Browser Task는 다른 Profile을 가질 수 있다.

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

이렇게 하면 Agent가 Task마다 환경 설치 방법부터 추론할 필요가 줄어든다.

---

### Prepared Snapshot과 Fresh Task State

Prepared Environment를 실제 운영 형태로 만들 때는 Image나 Snapshot을 사용할 수 있다.

한 공개 tutorial 구현에서는 Coding Agent Runtime, Skill, Browser Tool, MCP Server, `AGENTS.md` 같은 정적 실행 자산을 reusable snapshot에 넣고 새 Worker를 그 환경에서 생성한다. 특정 Vendor 방식이 표준이라는 뜻은 아니다. 중요한 것은 **환경의 재사용 단위와 Task의 fresh state를 분리했다는 점**이다.

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

이 구분이 무너지면 Snapshot은 빠른 bootstrap 수단이 아니라 오래된 Work State를 복제하는 수단이 된다.

따라서 Prepared Environment의 목표는 "항상 같은 Worker를 유지하는 것"이 아니라 다음에 가깝다.

> **같은 실행 능력은 재현하고, Task의 작업 상태는 새로 시작한다.**

---

## 8.3 Fresh State와 Cache를 구분한다

환경을 재사용하기 시작하면 새로운 위험이 생긴다.

Cache와 Work State가 섞이는 것이다.

다음은 재사용하기 좋다.

- package download cache
- container image
- installed compiler
- browser binary
- build tool

반면 다음은 주의가 필요하다.

- source checkout
- uncommitted changes
- generated files
- local database data
- browser session
- test result
- temp file
- runtime process

예를 들어 이전 Task가 local Redis에 값을 남겼다고 하자.

다음 Task의 테스트가 같은 Redis를 사용한다.

테스트는 PASS했다.

하지만 clean environment에서는 실패할 수 있다.

이런 상태 오염은 Agent에게 더 위험하다.

Agent는 환경이 오염됐는지 모르고 코드가 맞다고 판단할 수 있기 때문이다.

그래서 다음 경계를 유지하는 편이 좋다.

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

물론 실제 시스템에서는 일부 runtime state를 의도적으로 유지할 수도 있다.

그 경우에도 그것이 authoritative Task State가 되어서는 안 된다.

---

## 8.4 Ephemeral Worker와 Persistent Worker

Worker 운영에는 두 방향이 있다.

### Ephemeral Worker

Task마다 새로 만든다.

~~~text
Task
→ provision
→ execute
→ collect result
→ destroy
~~~

장점:

- clean state
- reproducibility
- isolation
- 낮은 cross-task contamination

적합한 경우:

- 독립적인 Bug Fix
- CI-like Task
- 보안 민감 작업
- 짧은 Task

단점:

- cold start
- dependency restore
- 큰 Repository checkout 비용
- 복잡한 runtime setup

### Persistent Worker

Worker를 유지하고 여러 Task를 처리한다.

~~~text
Worker
→ Task A
→ Task B
→ Task C
~~~

장점:

- warm cache
- running service 유지
- 복잡한 environment reuse
- 긴 프로젝트 continuity

단점:

- stale dependency
- state contamination
- credential accumulation
- 재현성 저하

둘 중 하나가 항상 정답은 아니다. 공개된 Agent 시스템에서도 persistent environment와 disposable sandbox가 모두 사용된다. 선택 기준은 제품 유행이 아니라 Task의 setup cost, contamination risk, security boundary, reproducibility다.

예를 들어 Android Build처럼 초기 환경 준비가 매우 비싸다면 Persistent Worker가 유리할 수 있다.

반대로 untrusted external PR를 분석한다면 Ephemeral Worker가 더 적합할 수 있다.

---

## 8.5 Persistent Worker를 쓸 때 가장 조심할 것

Persistent Worker의 편리함 때문에 다음 상태까지 Worker에 맡기기 쉽다.

~~~text
현재 Task
진행 상황
승인 상태
다음 행동
~~~

이렇게 되면 Worker가 다시 Control Plane이 된다.

Persistent Worker는 **warm environment**를 제공할 수 있다.

하지만 Task State의 authoritative source가 되어서는 안 된다.

구분하면 다음과 같다.

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

Worker가 오래 살아도 Work State는 외부에 남는다.

---

## 8.6 Worker Profile

모든 Task가 같은 Worker를 필요로 하지는 않는다.

예를 들어 다음 네 Task를 생각해보자.

~~~text
T1 Java API fix
T2 React browser E2E
T3 Android build
T4 GPU model benchmark
~~~

같은 Worker Image로 모두 처리하려고 하면 환경이 거대해진다.

대신 capability profile을 정의할 수 있다.

~~~text
backend-java
browser-e2e
android
gpu
internal-network
~~~

Task는 필요한 capability를 선언한다.

~~~text
Task T1
requires:
- backend-java
- internal-network
~~~

Scheduler는 맞는 Worker를 찾는다.

이렇게 하면 “Backend Agent”, “Frontend Agent”처럼 역할만 자연어로 나누는 것보다 실행환경까지 명확하게 연결할 수 있다.

---

## 예: Java Backend Worker와 Browser Worker

Backend Task:

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

Browser Task:

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

두 Task는 Model이 같아도 필요한 Runtime과 Tool이 다르다.

Factory에서 Worker Selection은 Agent Personality가 아니라 **실행 capability**를 기준으로 볼 수 있다.

---

## Stale Browser State가 만든 잘못된 PASS

Persistent Browser Worker에서 이전 Task의 로그인 Session이 남았다고 하자.

새 Task는 로그인하지 않은 사용자의 Error Page를 검증해야 한다.

하지만 Browser Cookie가 남아 있어서 인증된 화면이 열린다.

Agent는 DOM과 Screenshot을 보고 정상으로 판단할 수 있다.

이 문제는 Model 성능이 아니다.

Worker State 문제다.

해결 방법은 다음처럼 다양하다.

- Task마다 Browser Profile reset
- cookie/storage clear
- clean test account
- Ephemeral Browser Worker
- runtime state checksum

중요한 것은 Failure Class를 구분하는 것이다.

코드가 틀렸는지, 환경이 오염됐는지 분리하지 않으면 Agent는 잘못된 방향으로 수정할 수 있다.

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

이 질문에 답하면 Worker가 단순한 “원격 개발 머신”에서 Factory의 execution unit으로 바뀐다.

---

## 다음 질문

좋은 Worker를 만들었다고 Agent가 자동으로 잘 일하는 것은 아니다.

같은 Model과 같은 Repository를 사용해도 Tool의 형태, Instruction, Search 결과, Error Feedback에 따라 행동이 달라진다.

다음 장에서는 Model 주변에서 Agent의 실제 작업 능력을 만드는 **Harness Engineering**을 다룬다.

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
