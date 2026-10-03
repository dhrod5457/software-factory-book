# 6장. Task 크기, 분해, Dependency

작업 기록이 중단 뒤에도 남도록 만들면 다음 문제는 크기다. 너무 큰 작업을 에이전트에게 주면 오래 실행되고 수정 범위가 넓어진다. 실패했을 때 처음부터 다시 해야 할 가능성도 커진다. 그렇다고 무조건 잘게 나누면 좋은 것도 아니다. 작업이 너무 작으면 워커 시작, 저장소 탐색, 맥락 정보 전달, 검증 같은 고정 비용이 반복된다. 그래서 좋은 작업 크기는 줄 수나 작업 시간으로 정하기 어렵다. 이 책에서는 다음 기준을 사용한다.

> 좋은 작업은 독립적으로 실행하고, 검증하고, 실패 시 복구할 수 있으며, 필요한 승인 주체가 결과를 판단할 수 있는 단위다.

작업을 나눈다는 것은 지시문을 보기 좋게 나누는 데 그치지 않는다. **어떤 작업을 먼저 하고 어떤 작업을 함께 할 수 있는지, 그 관계를 설계하는 일**이다.

---

## 6.1 Task Size에는 양쪽 비용이 있다

작업이 작아지면 좋은 점이 있다.

- 맥락 정보가 줄어든다.
- 실패 범위가 작아진다.
- 검토가 쉬워진다.
- 병렬 실행 가능성이 커진다.

하지만 너무 작으면 고정 비용이 커진다.

- 워커 시작
- 저장소 코드 가져오기
- 맥락 정보 불러오기
- 작업 배정
- 검증
- 결과 정리

예를 들어 한 줄 문구 수정 하나를 별도 워커에 보내는 것이 항상 효율적인 것은 아니다. 반대로 작업이 너무 크면 다른 문제가 생긴다.

- 여러 모듈을 함께 이해해야 한다.
- 변경 파일이 많아진다.
- 재시도 시 재작업 범위가 커진다.
- 검토가 어려워진다.
- 병합 충돌 가능성이 커진다.
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

절대적인 “30분 이하”나 “파일 3개 이하” 같은 규칙은 두지 않는다. 프로젝트마다 환경 준비 비용과 검증 비용이 다르기 때문이다.

---

## 6.2 독립성은 파일 수보다 중요하다

두 작업이 서로 다른 파일을 수정한다고 해서 독립적인 것은 아니다. 예를 들어 다음 두 작업을 보자.

~~~text
Task A
- user table에 status column 추가

Task B
- User API 응답에 status 추가
~~~

수정 파일은 다를 수 있다. 하지만 B는 A의 스키마와 업무 영역 의미에 의존한다. 반대로 파일이 일부 겹쳐도 논리적으로 독립적인 경우가 있을 수 있다. 따라서 독립성을 판단할 때는 다음을 본다.

- 범위가 분리되는가
- 수용 판단이 독립적인가
- 검증을 따로 실행할 수 있는가
- 공유 스키마를 바꾸는가
- 같은 설계 구조 결정에 의존하는가
- 동일한 외부 자원을 사용해야 하는가
- 한 작업 결과가 다른 작업의 입력인가

독립성이 높을수록 재시도와 병렬 실행이 쉬워진다.

---

## 6.3 Task List보다 Dependency Graph가 낫다

할 일 목록은 보통 목록으로 보인다.

~~~text
T1
T2
T3
T4
T5
~~~

하지만 실제 실행 순서는 목록보다 그래프에 가깝다.

~~~text
T1 ─→ T3 ─→ T5
T2 ───────→ T5
T4 ─→ T6
~~~

T1과 T2는 병렬로 실행할 수 있다. T5는 둘이 끝나야 실행 준비가 된 상태가 된다. T4와 T6은 다른 흐름이다. 의존 관계 그래프가 있으면 생산 시스템이 다음 질문에 답할 수 있다.

- 지금 실행 준비가 된 상태인 작업은 무엇인가
- 어떤 작업을 동시에 실행할 수 있는가
- 하나가 실패하면 무엇을 막아야 하는가
- 어떤 결과가 바뀌면 후속 단계 작업을 다시 검증해야 하는가

작업을 자동 선택하려면 우선순위보다 먼저 의존 관계가 정확해야 한다.

---

## 6.4 Retry Boundary를 같이 설계한다

작업을 나누는 중요한 이유 중 하나는 재시도 범위를 줄이는 것이다. 예를 들어 하나의 큰 작업 흐름이 있다고 하자.

~~~text
Analyze
→ Modify Backend
→ Modify Frontend
→ Run Unit Test
→ Run E2E
→ Build Image
~~~

마지막 E2E에서 실패했다. 하나로 묶인 작업이라면 전체 작업을 다시 실행할 수 있다. 작업을 나누면 나아질 것 같지만 반드시 그렇지는 않다. 미리 고정해 여러 하위 작업으로 쪼갰어도 실행 조율이 실패 상태를 이해하지 못하면 후속 단계 전체를 다시 실행할 수 있다.

2026년 `Runtime-Structured Task Decomposition` 연구는 두 소프트웨어 공학 작업 유형을 각각 10회씩 비교한 소규모 실험에서 이 차이를 다뤘다. 미리 고정한 작업 분해는 경우에 따라 하나로 묶어 실행하는 방식보다 재시도 비용이 더 커졌고, 의존 관계와 실패를 실행 중 제어 로직이 관리한 방식은 실패한 하위 작업만 다시 실행해 재시도 비용을 낮췄다. 아직 제한된 작업 유형의 연구이므로 일반 법칙으로 볼 수는 없지만, 적어도 “잘게 나누기만 하면 복구 비용이 줄어든다”는 가정에는 반례가 된다.

핵심은 나누는 행위 자체보다 **실행 시스템이 작업 간 의존 관계와 실패가 다른 작업에 미치는 영향을 이해하는가**에 있다.

~~~text
Failed Subtask
→ affected downstream만 invalidate
→ 필요한 부분만 rerun
~~~

생산 시스템에서 좋은 작업 경계는 재시도 범위기도 하다.

---

## 6.5 Large Task와 Large PR는 다르다

큰 기능이 하나의 제품 작업이라고 해서 하나의 거대한 변경 검토 요청으로 만들어야 하는 것은 아니다. 예를 들어 인증 시스템 개선을 보자. 제품 수준에서는 하나의 추진 과제일 수 있다. 하지만 전달은 다음처럼 나눌 수 있다.

~~~text
T1: exception mapping 정리
T2: expired token 처리
T3: refresh token test 보강
T4: metrics 추가
T5: integration regression
~~~

각 작업은 별도의 검토 가능한 변경을 만들 수 있다. 필요하면 순서를 정한다.

~~~text
T1
 ↓
T2
 ↓
T3
~~~

이렇게 하면 다음 장점이 있다.

- 검토 범위 감소
- 이전 상태로 복구 범위 감소
- 실패 문제 위치 파악 개선
- 병합 충돌 감소

물론 너무 많은 연속된 변경 검토 요청도 비용이 있다. 기준 브랜치 갱신, 병합 순서 관리, 의존 관계 관리가 필요하다. 그래서 큰 작업을 무조건 잘게 쪼개는 것이 아니라 **검토 가능한 전달 단위**를 찾는다.

---

## 6.6 병렬화 후보는 Task 구조에서 나온다

여러 에이전트를 쓰고 싶어서 작업을 병렬화하면 안 된다. 먼저 작업이 독립적인지 본다.

좋은 병렬 후보:

~~~text
T1: backend unit tests
T2: frontend E2E
T3: documentation
~~~

각 작업의 범위와 검증이 분리돼 있다.

나쁜 병렬 후보:

~~~text
T1: UserService 구조 변경
T2: UserService cache 변경
T3: UserService test architecture 변경
~~~

브랜치는 달라도 같은 설계 결정을 공유한다. 같은 스키마를 동시에 바꾸는 작업도 비슷하다. 병렬 실행은 에이전트 수가 아니라 의존 관계 그래프에서 나온다.

---

## 예: Auth 개선을 분해하기

처음 작업:

~~~text
인증 오류 처리 개선
~~~

먼저 설계 구조 결정이 필요하다.

~~~text
D1
- 인증 실패는 공통 error envelope를 사용
- expired / invalid token 모두 401
- OAuth flow는 유지
~~~

그 다음 작업을 만든다.

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

의존 관계:

~~~text
D1
├→ T1 ─→ T2 ─→ T4
└→ T3 ─────────→ T4
~~~

T1과 T3는 일부 병렬 가능하다. T4는 앞 작업 결과를 합친 뒤 실행한다. 이 구조가 있으면 작업 배정기는 단순 대기열보다 더 나은 결정을 할 수 있다.

---

## Task 분해 체크

작업을 대기열에 넣기 전에 다음 질문을 해볼 수 있다.

~~~text
1. Acceptance를 독립적으로 판단할 수 있는가?
2. 실패하면 이 Task만 Retry할 수 있는가?
3. 예상 변경 범위가 Review 가능한가?
4. 다른 Task의 미완성 결과에 의존하는가?
5. Shared Schema / Core File을 동시에 바꾸는가?
6. 결과를 Commit / Artifact로 전달할 수 있는가?
~~~

이 질문은 점수표가 아니다. 실행과 복구의 경계를 명시적으로 생각하게 만드는 장치다.

---

## 다음 질문

요구사항이 있고, 지속 작업이 있고, 의존 관계 그래프까지 만들었다. 이제 실제로 누군가 이 작업을 실행해야 한다. 어떤 워커를 선택할 것인가. 누가 작업 상태를 바꿀 것인가. 워커가 죽으면 누가 다시 배정할 것인가.

7장부터는 생산 시스템의 실행 구조로 들어간다.

먼저 **제어 계층과 실행 계층**을 분리한다.

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
