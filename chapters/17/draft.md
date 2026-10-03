# 17장. Parallel Worker와 Multi-Agent: 언제 병렬화할 것인가

워커 하나가 안정적으로 동작하면 다음 생각이 자연스럽게 든다.

> 워커를 10개로 늘리면 처리량도 10배가 되지 않을까?

항상 그렇지는 않다. 병렬화의 효과는 에이전트 수보다 **작업들이 서로 어떤 관계를 맺는지**에 달려 있다. 독립성이 낮은 작업을 동시에 실행하면 다음 비용이 생긴다.

- 같은 파일 충돌
- 같은 스키마 수정
- 중복 탐색
- 중복 구현
- 병합 충돌
- 검토 과부하
- 공유 자원 경쟁

그래서 이 책에서는 다음 원칙을 사용한다.

> 병렬화의 대상은 에이전트가 아니라 독립 작업이다.

---

## 17.1 Useful Parallelism의 조건

병렬화가 유리하려면 다음 조건이 많을수록 좋다.

- 범위가 독립적이다.
- 파일 중복이 적다.
- 공유 스키마를 건드리지 않는다.
- 수용 판단을 독립적으로 검증할 수 있다.
- 한 작업의 결과가 다른 작업의 입력이 아니다.
- 같은 외부 자원을 두고 경쟁하지 않는다.

예:

~~~text
T1 backend unit test 추가
T2 frontend E2E 보강
T3 documentation 업데이트
~~~

세 작업은 비교적 독립적이다. 반면 다음은 병렬화하기 어렵다.

~~~text
T1 UserService 구조 변경
T2 UserService cache 변경
T3 UserService test architecture 변경
~~~

브랜치가 달라도 실제로는 같은 설계 결정을 공유한다.

---

## 17.2 Task DAG에서 Parallelism이 나온다

6장에서 의존 관계 그래프를 만들었다.

병렬 실행은 이 그래프에서 자연스럽게 나온다.

예:

~~~text
T1 ─→ T3 ─→ T5
T2 ───────→ T5
T4 ─→ T6
~~~

동시에 실행 가능한 후보:

~~~text
T1
T2
T4
~~~

T5는 T1, T2가 모두 끝나야 한다. 이 구조에서는 에이전트 수를 먼저 정하지 않는다. 실행 준비가 된 작업 수와 의존 관계를 보고 필요한 워커 수를 정한다.

---

## 17.3 Fan-out / Fan-in

병렬 워커는 보통 다음 구조를 가진다.

~~~text
          ┌→ Worker A → Result A
Task Set ─┼→ Worker B → Result B
          └→ Worker C → Result C
                    ↓
              Integration
                    ↓
              Verification
~~~

작업을 여러 갈래로 나누는 단계가 팬아웃(Fan-out)이고, 결과를 다시 모으는 단계가 팬인(Fan-in)이다. 문제는 결과를 다시 합칠 때 드러난다. 각 작업이 독립적으로 PASS해도 합친 결과가 실패할 수 있다.

예:

~~~text
Worker A
→ API field rename

Worker B
→ client code old field 사용

둘 다 local test PASS

Integration
→ FAIL
~~~

따라서 병렬 실행에는 통합 통과 조건이 필요하다.

---

## 17.4 Ownership은 Scheduling Signal이다

생산 시스템 작업 배정기는 CPU와 메모리만 보는 것이 아니다. 소프트웨어 충돌 가능성도 볼 수 있다.

예:

~~~text
Task A
touches:
- auth/schema.sql
- AuthService.java

Task B
touches:
- auth/schema.sql
- LoginController.java
~~~

두 작업은 같은 스키마를 수정할 가능성이 높다. 작업 배정기는 병렬 제약을 줄 수 있다.

~~~text
shared_schema = true
→ serialize or coordinate
~~~

완벽하게 예측할 수는 없다. 에이전트가 실제로 어떤 파일을 수정할지 사전에 모를 수도 있다. 그래서 두 단계가 필요하다.

~~~text
Pre-scheduling prediction
+
Runtime conflict detection
~~~

---

## 17.5 More Agents가 More Throughput이 아닌 이유

Anthropic이 2026년 8월 공개한 연구는 이런 조율 실패를 통제된 시뮬레이션에서 보여준다. 여러 모델 세대와 에이전트 수를 바꿔 동일한 오픈월드 게임 프로젝트를 12시간 동안 공동 개발하게 했을 때, 일부 모델에서는 많은 PR을 열고도 병합 비율이 낮았고 공유 파일 충돌 뒤 PR을 포기하는 패턴이 나타났다. 더 최신 모델 중 일부는 오히려 파일 담당 관계를 강하게 나눠 충돌을 줄였다.

저자들 스스로 결과물의 품질이 전반적으로 낮았다고 밝힌 실험이며 실제 조직의 운영 환경 저장소를 그대로 재현한 것은 아니다. 따라서 이 결과를 여러 에이전트를 사용하는 모든 시스템에 일반화할 수는 없다.

하지만 한 가지는 분명하다.

~~~text
More Agents
≠ More Useful Parallelism
~~~

유용한 병렬성은 다음에 더 가깝다.

~~~text
Useful Parallelism
=
Parallel Completed Work
- Conflict
- Duplicate Work
- Reconciliation
- Review Overload
~~~

---

## 17.6 Same-model Committee의 함정

여러 에이전트에게 같은 질문을 하고 다수결을 하면 더 안전할 것처럼 보인다. 하지만 같은 모델, 같은 맥락 정보, 같은 도구를 사용하면 비슷한 오류를 반복할 수 있다. 같은 연구에서는 에이전트들이 동일하거나 유사한 모델·맥락 정보·실행 보조 구조를 가질 때 행동 다양성이 낮아지는 현상도 관찰됐다. 한 초기 게임 실험에서는 30개 에이전트 중 18개가 우연히 동일한 `mvp-game-loop` 브랜치 이름을 선택했다.

즉:

~~~text
N Agents
≠ N Independent Opinions
~~~

평가자를 분리할 때도 마찬가지다. 독립성을 높이려면 다음을 고려할 수 있다.

- 다른 맥락 정보
- 다른 역할
- 다른 모델
- 비공개 테스트
- 규칙 기반 검증기
- 사람의 검토

목표는 에이전트 수가 아니라 **오류의 연관성을 줄이는 것**이다.

---

## 17.7 Parent/Subagent와 Task Worker는 다르다

한 에이전트가 내부적으로 하위 에이전트를 쓰는 구조와 생산 시스템이 여러 지속 작업을 병렬 실행하는 구조는 다르다.

### Parent / Subagent

~~~text
One Task
→ Parent Agent
  ├→ research subagent
  ├→ test subagent
  └→ reviewer subagent
~~~

작업 상태는 하나다.

### Parallel Task Workers

~~~text
Task A → Worker A
Task B → Worker B
Task C → Worker C
~~~

각 작업은 독립 상태, 시도, 근거를 가진다. 둘 다 여러 에이전트를 함께 쓰는 방식처럼 보이지만 제어 경계가 다르다.

---

## 17.8 Shared Resource Stampede

여러 에이전트가 같은 외부 자원을 동시에 주기적으로 조회하면 문제가 생길 수 있다. Anthropic의 별도 대기열 관리 실험에서는 조율 수단이 부족한 에이전트들이 초당 30회 조회하는 백그라운드 프로그램을 만들었고, 한 실행에서 240만 건의 요청 중 실제 수용된 작업은 117건이었다. 이 역시 실험 환경의 극단적 사례지만 에이전트 속도가 자원 경쟁을 증폭할 수 있다는 점을 보여준다.

예:

~~~text
10 Workers
→ same CI API polling every second
~~~

또는:

~~~text
20 Workers
→ same test environment
→ same database
→ same rate-limited API
~~~

에이전트는 사람보다 훨씬 빠르게 반복 호출할 수 있다. 따라서 다음이 필요하다.

- 대기열
- 작업 점유권
- 재시도 간격 늘리기
- 호출 빈도 제한
- 동시 실행 수 제한
- 공정한 작업 배정

병렬 실행은 연산 자원만 늘리는 문제가 아니다. 공유 자원의 권한과 책임 관리가 필요하다.

---

## 17.9 Concurrency Budget

워커 수만 보지 않는다. 실제 병렬 처리 능력은 다음 중 가장 작은 값에 제한될 수 있다.

~~~text
Ready Task
Worker
CI
Review
Integration
Shared API
Budget
~~~

예:

~~~text
Workers: 20
Ready Tasks: 12
CI slots: 4
Review capacity: 3
~~~

이 경우 20개 워커를 모두 실행하는 것이 좋은 선택은 아닐 수 있다. 생산 시스템 작업 배정기는 후속 단계 처리 능력까지 고려할 수 있다.

---

## 17.10 Role Separation은 Task Independence가 아니다

실제 에이전트 제품에서는 프런트엔드, QA, 문서, 연구처럼 이름과 역할이 다른 에이전트를 만들고 서로 메시지를 주고받거나 작업을 넘기는 형태를 제공하기 시작했다. Cursor의 Grok Bot도 여러 봇의 병렬 실행, 메시지 교환, 작업 담당 관계 인계를 제품 기능으로 제공한다. 이 구조는 사람 조직과 비슷해 보여 이해하기 쉽다. 하지만 이름이 다르다고 작업이 독립적인 것은 아니다.

~~~text
Frontend Bot
Backend Bot
QA Bot
Documentation Bot
~~~

네 에이전트가 모두 같은 API 스키마 변경에 의존한다면 실제 작업 관계 그래프는 여전히 강하게 결합되어 있다. 따라서 다음을 구분한다.

~~~text
Role Separation
= 누가 어떤 종류의 판단과 행동을 주로 하는가

Task Independence
= 결과를 독립적으로 실행·검증·통합할 수 있는가
~~~

생산 시스템 작업 배정기가 병렬화를 결정할 때 더 중요한 것은 두 번째다. 에이전트 간 통신도 마찬가지다.

~~~text
Agent delegation
≠ durable orchestration
~~~

봇끼리 대화하고 일을 넘기는 것은 조율 수행 능력이다. 의존 관계, 시간 초과, 재시도, 담당 관계, 완료, 근거를 판단의 기준이 되도록 관리하는 것은 제어 계층의 책임이다. 여러 에이전트를 함께 쓰는 방식 UI가 좋아질수록 이 경계를 더 명확히 해야 한다.

## 예: 독립 Task 3개와 충돌 Task 3개

### Good

~~~text
T1 backend unit tests
T2 frontend E2E
T3 docs
~~~

병렬 실행 후 각 결과를 독립적으로 검증할 수 있다.

### Bad

~~~text
T4 auth schema
T5 auth service refactor
T6 auth API contract
~~~

같은 업무 영역 모델을 공유한다. 순차 실행이나 명시적인 조율이 더 나을 수 있다.

---

## 병렬화 전에 묻는 질문

~~~text
1. Acceptance를 독립적으로 검증할 수 있는가?
2. File/Schema overlap이 낮은가?
3. 한 Task 결과가 다른 Task 입력인가?
4. Shared Resource를 경쟁하는가?
5. Fan-in 이후 Integration Verification이 있는가?
6. Review Capacity가 병렬 결과를 감당할 수 있는가?
~~~

이 질문이 워커 수보다 먼저다.

---

## 다음 질문

병렬 워커로 구현 처리량을 높였다. 이제 더 많은 변경 검토 요청과 검증 작업이 나온다. 그 결과 검토 대기열과 CI 대기열이 길어질 수 있다. 다음 장에서는 코딩 다음 단계에서 생기는 **검토, CI, 통합 병목**을 다룬다.

---

## 참고 자료

- Cursor, *Grok Bot*  
  https://cursor.com/docs/grok-bot
- Anthropic, *Patterns and problems in emerging multiagent systems*  
  https://www.anthropic.com/research/multiagent-systems
- Anthropic, *Building a C compiler with a team of parallel Claudes*  
  https://www.anthropic.com/engineering/building-c-compiler
- GitHub, *Copilot CLI Fleet*  
  https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet
