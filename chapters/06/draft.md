# 6장. Task 크기, 분해, Dependency

Task를 durable하게 만들면 다음 문제는 크기다.

너무 큰 Task를 Agent에게 주면 오래 실행되고 수정 범위가 넓어진다. 실패했을 때 처음부터 다시 해야 할 가능성도 커진다.

그렇다고 무조건 잘게 나누면 좋은 것도 아니다.

Task가 너무 작으면 Worker 시작, Repository 탐색, Context 전달, Verification 같은 고정 비용이 반복된다.

그래서 좋은 Task 크기는 줄 수나 작업 시간으로 정하기 어렵다.

이 책에서는 다음 기준을 사용한다.

> 좋은 Task는 독립적으로 실행하고, 검증하고, 실패 시 복구할 수 있으며, 사람이 결과를 리뷰할 수 있는 단위다.

Task 분해는 Prompt를 예쁘게 나누는 문제가 아니다.

**실행 그래프를 설계하는 문제**다.

---

## 6.1 Task Size에는 양쪽 비용이 있다

Task가 작아지면 좋은 점이 있다.

- Context가 줄어든다.
- Failure 범위가 작아진다.
- Review가 쉬워진다.
- 병렬 실행 가능성이 커진다.

하지만 너무 작으면 고정 비용이 커진다.

- Worker startup
- Repository checkout
- Context loading
- Scheduling
- Verification
- Result packaging

예를 들어 한 줄 문구 수정 하나를 별도 Worker에 보내는 것이 항상 효율적인 것은 아니다.

반대로 Task가 너무 크면 다른 문제가 생긴다.

- 여러 모듈을 함께 이해해야 한다.
- 변경 파일이 많아진다.
- Retry 시 재작업 범위가 커진다.
- Review가 어려워진다.
- Merge Conflict 가능성이 커진다.
- 완료 조건이 모호해진다.

개념적으로 다음과 같은 균형이 있다.

~~~text
Very Small Task
→ orchestration overhead 증가

Reasonable Task
→ independent execute / verify / review 가능

Very Large Task
→ context / failure / review cost 증가
~~~

절대적인 “30분 이하”나 “파일 3개 이하” 같은 규칙은 두지 않는다.

프로젝트마다 환경 준비 비용과 검증 비용이 다르기 때문이다.

---

## 6.2 독립성은 파일 수보다 중요하다

두 Task가 서로 다른 파일을 수정한다고 해서 독립적인 것은 아니다.

예를 들어 다음 두 작업을 보자.

~~~text
Task A
- user table에 status column 추가

Task B
- User API 응답에 status 추가
~~~

수정 파일은 다를 수 있다.

하지만 B는 A의 Schema와 Domain 의미에 의존한다.

반대로 파일이 일부 겹쳐도 논리적으로 독립적인 경우가 있을 수 있다.

따라서 독립성을 판단할 때는 다음을 본다.

- Scope가 분리되는가
- Acceptance가 독립적인가
- Verification을 따로 실행할 수 있는가
- Shared Schema를 바꾸는가
- 같은 Architecture Decision에 의존하는가
- 동일한 External Resource를 사용해야 하는가
- 한 Task 결과가 다른 Task의 입력인가

독립성이 높을수록 Retry와 Parallelism이 쉬워진다.

---

## 6.3 Task List보다 Dependency Graph가 낫다

Backlog는 보통 List로 보인다.

~~~text
T1
T2
T3
T4
T5
~~~

하지만 실제 실행 순서는 List보다 Graph에 가깝다.

~~~text
T1 ─→ T3 ─→ T5
T2 ───────→ T5
T4 ─→ T6
~~~

T1과 T2는 병렬로 실행할 수 있다.

T5는 둘이 끝나야 Ready가 된다.

T4와 T6은 다른 흐름이다.

Dependency Graph가 있으면 Factory가 다음 질문에 답할 수 있다.

- 지금 Ready인 Task는 무엇인가
- 어떤 Task를 동시에 실행할 수 있는가
- 하나가 실패하면 무엇을 막아야 하는가
- 어떤 결과가 바뀌면 downstream Task를 다시 검증해야 하는가

Task를 자동 선택하려면 Priority보다 먼저 Dependency가 정확해야 한다.

---

## 6.4 Retry Boundary를 같이 설계한다

Task를 나누는 중요한 이유 중 하나는 Retry 범위를 줄이는 것이다.

예를 들어 하나의 큰 workflow가 있다고 하자.

~~~text
Analyze
→ Modify Backend
→ Modify Frontend
→ Run Unit Test
→ Run E2E
→ Build Image
~~~

마지막 E2E에서 실패했다.

Monolithic Task라면 전체 작업을 다시 실행할 수 있다.

Task를 나누면 나아질 것 같지만 반드시 그렇지는 않다.

Static하게 여러 Subtask로 쪼갰어도 orchestration이 실패 상태를 이해하지 못하면 downstream 전체를 다시 실행할 수 있다.

2026년 Runtime-Structured Task Decomposition 연구는 이 차이를 다룬다.

핵심은 분해 자체보다 **dependency와 failure semantics를 runtime이 아는가**다.

~~~text
Failed Subtask
→ affected downstream만 invalidate
→ 필요한 부분만 rerun
~~~

Factory에서 좋은 Task Boundary는 Retry Boundary이기도 하다.

---

## 6.5 Large Task와 Large PR는 다르다

큰 Feature가 하나의 Product Task라고 해서 하나의 거대한 Pull Request로 만들어야 하는 것은 아니다.

예를 들어 인증 시스템 개선을 보자.

Product 수준에서는 하나의 Initiative일 수 있다.

하지만 Delivery는 다음처럼 나눌 수 있다.

~~~text
T1: exception mapping 정리
T2: expired token 처리
T3: refresh token test 보강
T4: metrics 추가
T5: integration regression
~~~

각 Task는 별도의 Reviewable Change를 만들 수 있다.

필요하면 순서를 정한다.

~~~text
T1
 ↓
T2
 ↓
T3
~~~

이렇게 하면 다음 장점이 있다.

- Review scope 감소
- Rollback 범위 감소
- Failure localization 개선
- Merge Conflict 감소

물론 너무 많은 PR chain도 비용이 있다.

Rebase, merge ordering, dependency management가 필요하다.

그래서 Large Task를 무조건 잘게 쪼개는 것이 아니라 **review 가능한 delivery boundary**를 찾는다.

---

## 6.6 병렬화 후보는 Task 구조에서 나온다

여러 Agent를 쓰고 싶어서 Task를 병렬화하면 안 된다.

먼저 Task가 독립적인지 본다.

좋은 병렬 후보:

~~~text
T1: backend unit tests
T2: frontend E2E
T3: documentation
~~~

각 작업의 Scope와 Verification이 분리돼 있다.

나쁜 병렬 후보:

~~~text
T1: UserService 구조 변경
T2: UserService cache 변경
T3: UserService test architecture 변경
~~~

Branch는 달라도 같은 설계 결정을 공유한다.

같은 Schema를 동시에 바꾸는 Task도 비슷하다.

Parallelism은 Agent 수가 아니라 Dependency Graph에서 나온다.

---

## 예: Auth 개선을 분해하기

처음 Work:

~~~text
인증 오류 처리 개선
~~~

먼저 Architecture Decision이 필요하다.

~~~text
D1
- 인증 실패는 공통 error envelope를 사용
- expired / invalid token 모두 401
- OAuth flow는 유지
~~~

그 다음 Task를 만든다.

~~~text
T1
Exception mapping 정리

T2
Expired token 처리

T3
Invalid token regression test

T4
Auth integration test
~~~

Dependency:

~~~text
D1
├→ T1 ─→ T2 ─→ T4
└→ T3 ─────────→ T4
~~~

T1과 T3는 일부 병렬 가능하다.

T4는 앞 작업 결과를 합친 뒤 실행한다.

이 구조가 있으면 Scheduler는 단순 Queue보다 더 나은 결정을 할 수 있다.

---

## Task 분해 체크

Task를 Queue에 넣기 전에 다음 질문을 해볼 수 있다.

~~~text
1. Acceptance를 독립적으로 판단할 수 있는가?
2. 실패하면 이 Task만 Retry할 수 있는가?
3. 예상 변경 범위가 Review 가능한가?
4. 다른 Task의 미완성 결과에 의존하는가?
5. Shared Schema / Core File을 동시에 바꾸는가?
6. 결과를 Commit / Artifact로 전달할 수 있는가?
~~~

이 질문은 점수표가 아니다.

실행과 복구의 경계를 명시적으로 생각하게 만드는 장치다.

---

## 다음 질문

Requirement가 있고, Durable Task가 있고, Dependency Graph까지 만들었다.

이제 실제로 누군가 이 Work를 실행해야 한다.

어떤 Worker를 선택할 것인가.

누가 Task 상태를 바꿀 것인가.

Worker가 죽으면 누가 다시 배정할 것인가.

7장부터는 Factory의 실행 구조로 들어간다.

먼저 **Control Plane과 Execution Plane**을 분리한다.

---

## 참고 자료

- GitHub, *Spec Kit*  
  https://github.com/github/spec-kit
- *Runtime-Structured Task Decomposition for Agentic Coding Systems*  
  https://arxiv.org/abs/2605.15425
- GitHub, *Stacked pull requests are now in public preview*  
  https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/
- GitHub Engineering, *Turn one giant AI-generated pull request to a reviewable stack*  
  https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/
