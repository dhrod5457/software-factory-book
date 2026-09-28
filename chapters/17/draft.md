# 17장. Parallel Worker와 Multi-Agent: 언제 병렬화할 것인가

Worker 하나가 안정적으로 동작하면 다음 생각이 자연스럽게 든다.

> Worker를 10개로 늘리면 처리량도 10배가 되지 않을까?

항상 그렇지는 않다.

병렬화는 Agent 수의 문제가 아니라 **Task Structure의 문제**다.

독립성이 낮은 Task를 동시에 실행하면 다음 비용이 생긴다.

- 같은 파일 충돌
- 같은 Schema 수정
- 중복 탐색
- 중복 구현
- Merge Conflict
- Review overload
- Shared Resource 경쟁

그래서 이 책에서는 다음 원칙을 사용한다.

> 병렬화의 대상은 Agent가 아니라 독립 Task다.

---

## 17.1 Useful Parallelism의 조건

병렬화가 유리하려면 다음 조건이 많을수록 좋다.

- Scope가 독립적이다.
- File overlap이 적다.
- Shared Schema를 건드리지 않는다.
- Acceptance를 독립적으로 검증할 수 있다.
- 한 Task의 결과가 다른 Task의 입력이 아니다.
- 같은 외부 Resource를 두고 경쟁하지 않는다.

예:

~~~text
T1 backend unit test 추가
T2 frontend E2E 보강
T3 documentation 업데이트
~~~

세 Task는 비교적 독립적이다.

반면 다음은 병렬화하기 어렵다.

~~~text
T1 UserService 구조 변경
T2 UserService cache 변경
T3 UserService test architecture 변경
~~~

Branch가 달라도 실제로는 같은 설계 결정을 공유한다.

---

## 17.2 Task DAG에서 Parallelism이 나온다

6장에서 Dependency Graph를 만들었다.

Parallelism은 이 Graph에서 자연스럽게 나온다.

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

T5는 T1, T2가 모두 끝나야 한다.

이 구조에서는 Agent 수를 먼저 정하지 않는다.

Ready Task 수와 Dependency를 보고 필요한 Worker 수를 정한다.

---

## 17.3 Fan-out / Fan-in

Parallel Worker는 보통 다음 구조를 가진다.

~~~text
          ┌→ Worker A → Result A
Task Set ─┼→ Worker B → Result B
          └→ Worker C → Result C
                    ↓
              Integration
                    ↓
              Verification
~~~

Fan-out에서 여러 Work를 분산한다.

Fan-in에서 결과를 다시 합친다.

문제는 Fan-in에서 드러난다.

각 Task가 독립적으로 PASS해도 합친 결과가 실패할 수 있다.

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

따라서 Parallel Execution에는 Integration Gate가 필요하다.

---

## 17.4 Ownership은 Scheduling Signal이다

Factory Scheduler는 CPU와 Memory만 보는 것이 아니다.

Software Conflict 가능성도 볼 수 있다.

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

두 Task는 같은 Schema를 수정할 가능성이 높다.

Scheduler는 Parallel Penalty를 줄 수 있다.

~~~text
shared_schema = true
→ serialize or coordinate
~~~

완벽하게 예측할 수는 없다.

Agent가 실제로 어떤 File을 수정할지 사전에 모를 수도 있다.

그래서 두 단계가 필요하다.

~~~text
Pre-scheduling prediction
+
Runtime conflict detection
~~~

---

## 17.5 More Agents가 More Throughput이 아닌 이유

Anthropic이 2026년 8월 공개한 연구는 이런 Coordination Failure를 통제된 simulation에서 보여준다. 여러 Model Generation과 Agent 수를 바꿔 동일한 open-world game project를 12시간 동안 공동 개발하게 했을 때, 일부 Model에서는 많은 PR을 열고도 Merge 비율이 낮았고 shared file conflict 뒤 PR을 포기하는 패턴이 나타났다. 더 최신 Model 중 일부는 오히려 file ownership을 강하게 나눠 충돌을 줄였다.

저자들 스스로 결과물의 품질이 전반적으로 낮았다고 밝힌 실험이며 실제 조직의 Production Repository를 그대로 재현한 것은 아니다. 따라서 이 결과를 모든 Multi-Agent 시스템에 일반화할 수는 없다.

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

여러 Agent에게 같은 질문을 하고 다수결을 하면 더 안전할 것처럼 보인다.

하지만 같은 Model, 같은 Context, 같은 Tool을 사용하면 비슷한 오류를 반복할 수 있다.

같은 연구에서는 Agent들이 동일하거나 유사한 Model·Context·Scaffolding을 가질 때 행동 다양성이 낮아지는 현상도 관찰됐다. 한 초기 game experiment에서는 30개 Agent 중 18개가 우연히 동일한 `mvp-game-loop` branch name을 선택했다.

즉:

~~~text
N Agents
≠ N Independent Opinions
~~~

Evaluator를 분리할 때도 마찬가지다.

독립성을 높이려면 다음을 고려할 수 있다.

- 다른 Context
- 다른 Role
- 다른 Model
- hidden test
- deterministic verifier
- human review

목표는 Agent 수가 아니라 **Error Correlation을 줄이는 것**이다.

---

## 17.7 Parent/Subagent와 Task Worker는 다르다

한 Agent가 내부적으로 Subagent를 쓰는 구조와 Factory가 여러 Durable Task를 병렬 실행하는 구조는 다르다.

### Parent / Subagent

~~~text
One Task
→ Parent Agent
  ├→ research subagent
  ├→ test subagent
  └→ reviewer subagent
~~~

Task State는 하나다.

### Parallel Task Workers

~~~text
Task A → Worker A
Task B → Worker B
Task C → Worker C
~~~

각 Task는 독립 State, Attempt, Evidence를 가진다.

둘 다 Multi-Agent처럼 보이지만 Control Boundary가 다르다.

---

## 17.8 Shared Resource Stampede

여러 Agent가 같은 External Resource를 동시에 Polling하면 문제가 생길 수 있다. Anthropic의 별도 queue-management experiment에서는 coordination 수단이 부족한 Agent들이 초당 30회 polling daemon을 만들었고, 한 run에서 240만 건의 요청 중 실제 accepted job은 117건이었다. 이 역시 실험 환경의 극단적 사례지만 Agent speed가 resource contention을 증폭할 수 있다는 점을 보여준다.

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

Agent는 사람보다 훨씬 빠르게 반복 호출할 수 있다.

따라서 다음이 필요하다.

- queue
- lease
- backoff
- rate limit
- concurrency limit
- fair scheduling

Parallelism은 Compute만 늘리는 문제가 아니다.

Shared Resource Governance가 필요하다.

---

## 17.9 Concurrency Budget

Worker Count만 보지 않는다.

실제 Parallel Capacity는 다음 중 가장 작은 값에 제한될 수 있다.

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

이 경우 20개 Worker를 모두 실행하는 것이 좋은 선택은 아닐 수 있다.

Factory Scheduler는 downstream capacity까지 고려할 수 있다.

---

## 17.10 Role Separation은 Task Independence가 아니다

실제 Agent 제품에서는 Frontend, QA, Documentation, Research처럼 이름과 역할이 다른 Agent를 만들고 서로 메시지를 주고받거나 Task를 넘기는 형태를 제공하기 시작했다. Cursor의 Grok Bot도 여러 Bot의 병렬 실행, 메시지 교환, Task ownership handoff를 제품 기능으로 제공한다.

이 구조는 사람 조직과 비슷해 보여 이해하기 쉽다.

하지만 이름이 다르다고 Work가 독립적인 것은 아니다.

~~~text
Frontend Bot
Backend Bot
QA Bot
Documentation Bot
~~~

네 Agent가 모두 같은 API Schema 변경에 의존한다면 실제 Task Graph는 여전히 강하게 결합되어 있다.

따라서 다음을 구분한다.

~~~text
Role Separation
= 누가 어떤 종류의 판단과 행동을 주로 하는가

Task Independence
= 결과를 독립적으로 실행·검증·통합할 수 있는가
~~~

Factory Scheduler가 병렬화를 결정할 때 더 중요한 것은 두 번째다.

Agent-to-Agent Communication도 마찬가지다.

~~~text
Agent delegation
≠ durable orchestration
~~~

Bot끼리 대화하고 일을 넘기는 것은 Coordination Capability다.

Dependency, timeout, retry, ownership, completion, evidence를 authoritative하게 관리하는 것은 Control Plane의 책임이다.

Multi-Agent UI가 좋아질수록 이 경계를 더 명확히 해야 한다.

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

같은 Domain Model을 공유한다.

순차 실행이나 explicit coordination이 더 나을 수 있다.

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

이 질문이 Worker 수보다 먼저다.

---

## 다음 질문

Parallel Worker로 Implementation Throughput을 높였다.

이제 더 많은 Pull Request와 Verification Job이 나온다.

그 결과 Review Queue와 CI Queue가 길어질 수 있다.

다음 장에서는 Coding 다음 단계에서 생기는 **Review, CI, Integration Bottleneck**을 다룬다.

---

## 참고 자료

- Anthropic, *Patterns and problems in emerging multiagent systems*  
  https://www.anthropic.com/research/multiagent-systems
- Anthropic, *Building a C compiler with a team of parallel Claudes*  
  https://www.anthropic.com/engineering/building-c-compiler
- GitHub, *Copilot CLI Fleet*  
  https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet
