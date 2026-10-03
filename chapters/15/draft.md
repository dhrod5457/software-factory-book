# 15장. Durable Execution: Crash를 넘어 이어지는 Work

에이전트 작업이 몇 초 안에 끝난다면 실행 상태를 크게 고민하지 않아도 된다. 하지만 작업이 수십 분, 수 시간, 며칠까지 길어지면 상황이 달라진다. 그동안 다음 일이 생길 수 있다.

- 워커 프로세스가 죽는다.
- 실행 기반이 재시작된다.
- 네트워크가 끊긴다.
- 외부 API 응답이 유실된다.
- 사람의 승인을 몇 시간 기다린다.
- 같은 도구 호출이 중복 실행된다.

이 순간부터 장시간 실행 에이전트는 단순한 지시문 작성 문제가 아니다. 분산 시스템 문제에 가까워진다.

> 맥락 정보를 저장하는 것과 실행을 복구하는 것은 다른 문제다.

이 장에서는 에이전트가 정보를 기억하는 기능과 구분해, **실행이 중단돼도 상태를 보존하고 이어가는 지속 실행(Durable Execution)**을 다룬다.

---

## 15.1 Memory와 Execution State는 다르다

에이전트 세션을 저장하면 이전 대화를 다시 읽을 수 있다. 하지만 다음 질문에는 답하지 못할 수 있다.

- 어떤 단계가 실제로 완료됐는가
- 어떤 외부 시스템에 남는 변경이 이미 발생했는가
- 어디부터 다시 실행해야 하는가
- 같은 도구 호출을 다시 해도 안전한가
- 어떤 사람 이벤트를 기다리고 있는가

예를 들어 에이전트가 변경 검토 요청을 생성하려고 했다.

~~~text
create_pull_request()
~~~

GitHub에서는 실제로 PR이 만들어졌다. 하지만 네트워크가 끊겨 실행 기반은 응답을 받지 못했다. 다시 시작한 에이전트가 같은 도구를 호출하면 두 번째 PR이 생길 수 있다. 대화 이력을 저장해도 이 문제는 해결되지 않는다. 필요한 것은 **실행 결과와 외부에 남는 변경 이력**이다.

---

## 15.2 Event History

지속 실행에서는 중요한 상태 변화와 외부 행동을 기록한다.

예:

~~~text
TaskStarted
WorkerAssigned
CheckoutCompleted
PatchCreated
UnitTestPassed
PullRequestCreateRequested
PullRequestCreated
ApprovalRequested
~~~

실행 기반이 중간에 죽더라도 이벤트 이력을 보고 이미 완료된 단계를 알 수 있다.

~~~text
Replay
→ completed step skip
→ incomplete step continue
~~~

여기서 실행 기록 재생은 에이전트가 같은 문장을 다시 생성한다는 뜻이 아니다. 작업 흐름 실행 기반이 **어떤 실행이 이미 완료됐는지 재구성**하는 것이다.

---

## 15.3 Checkpoint

모든 이벤트만으로 실제 작업 공간을 복구하기 어려울 수 있다. 그래서 복구 지점을 둔다. 코딩 작업에서는 Git 커밋 자체가 좋은 복구 지점이 될 수 있다.

~~~text
Workspace
→ incremental commit
→ durable Git state
~~~

하지만 Git만으로는 충분하지 않다. Git에 없는 상태가 있기 때문이다.

- 현재 시도
- 승인 상태
- 도구 결과
- 외부 시스템에 남는 변경
- 재시도 횟수
- 대기 중인 타이머

그래서 보통 다음 두 상태가 필요하다.

~~~text
Git State
+
Orchestration State
~~~

필요하면 패치, 파일 시스템 스냅샷, 산출물도 추가할 수 있다. 복구 지점 세부 단위는 작업마다 다를 수 있다. 너무 자주 만들면 추가 부담이 크다. 너무 드물면 비정상 종료 때 잃는 작업이 커진다.

---

## 15.4 Exactly-once를 기대하지 않는다

생산 시스템 실행 기반만으로 임의의 외부 시스템에 남는 변경에 완전한 정확히 한 번 실행하는 보장(Exactly-once)를 보장한다고 가정하면 안 된다. 외부 시스템이 트랜잭션이나 멱등성을 함께 지원하지 않으면 “실행은 성공했지만 응답은 유실된” 상태를 실행 기반 혼자 판별할 수 없기 때문이다. 다음 상황을 보자.

~~~text
Factory
→ deploy(version=abc123)

Deployment Platform
→ success

Network response
→ lost

Factory
→ retry deploy(version=abc123)
~~~

두 번째 호출이 안전한지는 도구 사용 규약에 달려 있다. 그래서 같은 요청을 여러 번 보내도 한 번 실행한 것과 같은 결과를 유지하는 성질인 멱등성(Idempotency)이 중요하다.

예:

~~~text
deploy(
  operation_id="T100-A2-deploy",
  revision="abc123"
)
~~~

같은 operation_id로 재호출하면 플랫폼은 이전 결과를 반환할 수 있다.

~~~text
status: already_completed
deployment_id: dep-882
~~~

이 구조는 다음 작업에도 필요하다.

- 변경 검토 요청 생성
- 이슈 갱신
- 이메일
- DB 변경
- 릴리스
- 결제처럼 중복 실행이 위험한 내부 작업 동작

---

## 15.5 Replay-safe Tool

에이전트 도구도 중단 후 복구할 수 있는 실행 기반을 고려해 설계할 수 있다.

나쁜 예:

~~~text
create_pr(title, body)
~~~

응답이 유실되면 재호출 시 중복 가능성이 있다.

더 나은 예:

~~~text
create_pr(
  operation_id,
  repository,
  head,
  base,
  title
)
~~~

도구는 같은 operation_id를 인식한다.

~~~text
if already executed:
    return previous result
~~~

이 원칙은 에이전트를 위한 플랫폼 인터페이스에서 중요하다. 에이전트가 도구를 자유롭게 호출할수록 실행 기반이 외부 변경이 중복해서 발생하는 것을 막아야 한다.

---

## 15.6 Human Approval은 Async Event다

사람이 판단에 참여하는 방식을 응답을 기다리며 멈춰 있는 동기식 프로세스로 생각하면 자원을 낭비한다.

예:

~~~text
Worker
→ Plan complete
→ waits 8 hours
→ human approve
→ continues
~~~

워커를 8시간 유지할 필요가 없다. 더 좋은 구조는 다음과 같다.

~~~text
Task
→ ApprovalRequested
→ Worker released
→ Task suspended

8 hours later

Human Approval Event
→ Task resumed
→ Worker assigned
~~~

작업 흐름 모델에서는 사람의 승인을 나중에 도착하는 나중에 전달되는 비동기 이벤트나 신호로 표현할 수 있다. 이 구조가 있으면 승인 대기와 연산 자원 점유를 분리할 수 있다.

---

## 15.7 Durable Runtime과 Agent Harness의 책임

둘을 구분해보자.

### Agent Harness

질문:

~~~text
다음에 무엇을 해야 하는가?
~~~

책임:

- 맥락 정보
- 도구 선택
- 에이전트 순환
- 추론
- 구현

### Durable Runtime

질문:

~~~text
이 Work가 현실의 Crash와 Wait를 살아남게 하려면?
~~~

책임:

- 이벤트 이력
- 재시도
- 타이머
- 대기
- 신호
- 취소
- 멱등성
- 중단 지점부터 재개

개념적으로 다음처럼 볼 수 있다.

~~~text
Factory Control Plane
        ↓
Durable Runtime
        ↓
Agent Harness
        ↓
Worker / Sandbox
~~~

구현에 따라 계층이 합쳐질 수 있다. 중요한 것은 책임을 구분하는 것이다.

---

## 15.8 제품이 아니라 책임 분리로 본다

Temporal, Microsoft Durable Task, Google Agent Executor 같은 시스템은 서로 구현과 추상화가 다르다. 특히 여기서 Microsoft Durable Task는 5장에서 정의한 책의 “지속 작업” 작업 단위와 다른 작업 흐름 기술다.

Microsoft는 이를 특정 에이전트 프레임워크에 종속되지 않은 장시간 실행하는 상태를 보존하는 작업 흐름 기반으로 설명하고 있고, Google은 2026년 5월 Agent Executor를 이벤트 기록과 스냅샷으로 서비스 중단나 사람의 개입 이후 실행을 재개하는 오픈소스 실행 기반 표준으로 공개했다.

이 책에서 중요한 것은 특정 제품 API가 아니라 공통적으로 다음 문제를 별도 신뢰성 계층에서 다룬다는 점이다.

- 장시간 실행하는 상태
- 재시도
- 중단 지점부터 재개
- 이벤트
- 사람의 판단을 기다리는 시간
- 비정상 종료 복구

생산 시스템이 직접 모든 것을 구현할 수도 있다. 하지만 작업 점유권, 타이머, 재시도, 이력, 멱등성은 전형적인 분산 시스템 문제다. 규모가 커지기 전에 기존 중단 후 복구할 수 있는 작업 실행 인프라를 검토할 가치가 있다.

---

## 15.9 Crash Test를 Acceptance Scenario로 만든다

생산 시스템 신뢰성을 정상 실행 경로만으로 평가하면 부족하다. 일부러 실패를 주입해볼 수 있다.

~~~text
Worker process kill
VM kill
Network disconnect
Orchestrator restart
Approval delay
Tool timeout
~~~

검증할 항목:

~~~text
Task state preserved?
Retry budget preserved?
Duplicate PR created?
Uncommitted work lost?
Evidence still linked?
Different Worker resume possible?
~~~

이런 시험은 에이전트 성능 평가보다 생산 시스템 신뢰성을 더 직접적으로 보여줄 수 있다.

---

## 15.10 Resume Quality

에이전트 신뢰성을 성공률만으로 보면 부족하다. 장기 작업에서는 다음도 중요하다.

~~~text
Resume Quality
~~~

예를 들어 워커 A가 80%까지 작업하고 죽었다. 워커 B가 처음부터 다시 한다면 작업은 최종적으로 성공할 수 있다. 하지만 연속성은 약하다. 더 강한 기준은 다음이다.

> 다른 워커가 이전 워커의 유효한 작업을 보존하고 이어받을 수 있는가?

이 기준은 5장에서 다룬 지속 작업과 연결된다. 지속 작업 상태가 있어도 작업 공간·복구 지점 상태가 없으면 실제 작업은 다시 시작할 수 있다.

---

## 15.11 Persistent Agent, Persistent Worker, Durable Task를 구분한다

최근 에이전트 제품 중에는 이름과 역할을 가진 에이전트가 여러 세션에 걸쳐 기억, 파일, 브라우저 세션, 선호를 유지하는 형태가 등장하고 있다. Cursor의 Grok Bot도 봇별 맥락 정보를 유지하면서 계정 단위의 계속 유지되는 클라우드 컴퓨터에서 파일과 브라우저 세션을 이어 사용하는 구조를 공개하고 있다. 이런 형태는 긴 작업의 마찰을 크게 줄일 수 있다. 하지만 다음 세 가지 지속성을 같은 것으로 보면 안 된다.

~~~text
Persistent Agent
- role
- learned preference
- memory
- skill

Persistent Worker
- filesystem
- browser session
- process
- cache
- runtime tools

Durable Task
- goal
- status
- attempt
- dependency
- approval
- verification
- evidence
~~~

에이전트가 기억한다고 작업이 중단돼도 기록이 남는 것은 아니다. 워커의 파일이 남아 있다고 실행 조율 상태가 보존된 것도 아니다. 반대로 워커를 잃더라도 작업 저장소와 복구 지점이 살아 있다면 다른 워커에서 작업을 이어갈 수 있다. 따라서 다음 등식을 피한다.

~~~text
Memory
≠ Worker Persistence
≠ Durable Task
≠ Durable Execution
~~~

지속형 에이전트는 작업 경험을 축적하는 UX와 수행 능력 문제다. 지속형 워커는 실행환경의 연속성 문제다. 지속 작업과 지속 실행은 업무 책임과 외부에 남는 변경을 비정상 종료 이후에도 복구하는 시스템 문제다. 이 경계를 분리해야 에이전트 제품의 편리한 지속성을 생산 시스템 신뢰성과 혼동하지 않는다.

## 예: Duplicate PR 방지

시도 A1:

~~~text
operation_id: T100-pr-create
create PR
→ GitHub success
→ response lost
~~~

실행 기반을 처음부터 다시 시작한다. 시도 A2가 다시 요청한다.

~~~text
create_pr(
  operation_id="T100-pr-create"
)
~~~

도구는 기존 결과를 반환한다.

~~~text
status: already_exists
pr: #381
~~~

이것이 지속 실행이 도구 사용 규약에까지 영향을 주는 예다.

---

## 다음 질문

작업이 비정상 종료와 대기를 견딜 수 있게 됐다. 이제 더 오래, 더 많은 권한으로 에이전트를 실행할 수 있다. 그만큼 위험도 커진다. 에이전트가 어떤 인증 정보를 가져야 하는가. 신뢰할 수 없는 이슈 내용이 도구 호출로 이어지면 어떻게 막을 것인가. 다음 장에서는 **보안, 신원, 권한과 책임 관리**를 다룬다.

---

## 참고 자료

- Cursor, *Work with Grok Bot*  
  https://cursor.com/docs/grok-bot/work
- Cursor, *Manage Grok Bot computers*  
  https://cursor.com/docs/grok-bot/computers
- Microsoft, *Durable Task for AI agents*  
  https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents
- Temporal, *AI and Durable Execution*  
  https://docs.temporal.io/ai
- Google Cloud, *Agent Executor: Google’s distributed agent runtime*  
  https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime
- Anthropic, *Effective harnesses for long-running agents*  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
