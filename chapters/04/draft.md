# 4장. Prompt가 아니라 Requirement와 Acceptance에서 시작한다

AI Coding Agent를 쓰다 보면 가장 먼저 하고 싶은 일은 바로 시키는 것이다.

> 로그인 오류를 고쳐라.

> 출결 화면을 개선해라.

> 이 모듈을 리팩터링해라.

작은 작업에서는 충분할 수 있다. 하지만 작업이 커지면 곧 다른 질문이 생긴다.

로그인 오류는 어떤 오류인가. 정상 동작은 무엇인가. 기존 동작 중 무엇을 유지해야 하는가. 어디까지 수정해도 되는가. 무엇을 확인하면 완료라고 볼 수 있는가.

사람끼리 일할 때는 이런 질문을 대화 속에서 자연스럽게 채우기도 한다. 경험이 많은 개발자는 조직의 암묵적 규칙까지 알고 있다.

Agent에게도 같은 암묵지를 기대하면 문제가 생긴다.

Agent는 주어진 정보 안에서 가장 그럴듯한 해석을 선택할 수 있다. 하지만 그 해석이 원래 Intent와 같다는 보장은 없다.

그래서 Factory에서 첫 번째로 필요한 것은 더 긴 Prompt가 아니다.

**실행 가능한 Requirement와 Acceptance를 만드는 일**이다.

---

## 4.1 Prompt만으로 큰 Work를 관리하기 어려운 이유

Prompt는 빠르다. 문제를 설명하고 곧바로 실행할 수 있다.

하지만 Prompt에는 보통 Goal, Background, Assumption, Constraint, Design Hint, Expected Result가 섞여 있다. 이 정보가 한 번의 Conversation 안에만 있으면 시간이 지나면서 해석이 흔들릴 수 있다.

예를 들어 다음 Issue를 보자.

~~~text
로그인 오류 수정
~~~

개발자에게는 충분할 수 있다. 이미 장애 상황을 알고 있기 때문이다.

Agent 입장에서는 다르다.

- 비밀번호 오류인가
- JWT 만료인가
- OAuth redirect 문제인가
- 세션 생성 실패인가
- HTTP status가 잘못됐는가

가능한 해석이 많다.

Agent가 Repository를 읽으며 추측할 수는 있다. 하지만 추측이 맞았는지 확인할 기준이 없다.

그래서 큰 Work에서는 Prompt보다 durable artifact가 필요하다.

~~~text
Conversation
→ ephemeral

Requirement
Acceptance
Design Constraint
Task
→ durable
~~~

이 문서가 거대한 명세서일 필요는 없다. 핵심은 Agent Session이 바뀌어도 Work의 의미가 유지되는 것이다.

---

## 4.2 Intent에서 Acceptance까지

Factory 앞단을 다음처럼 볼 수 있다.

~~~text
Intent
→ Requirement
→ Clarification
→ Acceptance Criteria
→ Design Constraint
→ Task
~~~

각 단계는 다른 질문에 답한다.

### Intent

왜 이 일을 하는가.

~~~text
만료된 JWT 때문에 사용자가 500 오류 화면을 본다.
인증 실패로 처리해야 한다.
~~~

### Requirement

시스템이 어떻게 동작해야 하는가.

~~~text
만료된 JWT 요청은 HTTP 401을 반환해야 한다.
~~~

### Acceptance Criteria

무엇을 확인하면 완료라고 볼 것인가.

~~~text
Given expired JWT
When protected endpoint is requested
Then response status is 401
And internal server error is not logged
~~~

### Design Constraint

무엇을 바꾸지 않아야 하는가.

~~~text
DB schema 변경 없음
OAuth flow 변경 없음
공통 error envelope 유지
~~~

이 정도만 있어도 Agent가 탐색해야 하는 범위가 크게 줄어든다.

더 중요한 점은 검증이 가능해진다는 것이다.

~~~text
Requirement
→ Acceptance
→ Test / Runtime Check
~~~

좋은 Requirement는 구현 방법을 세세하게 지시하는 문서가 아니다. Agent가 여러 구현 방법 중 선택할 수 있도록 하면서도 완료 여부는 명확하게 판단할 수 있게 해야 한다.

---

## 4.3 Requirements-first와 Design-first

모든 작업이 Requirement부터 시작하는 것은 아니다.

새 기능이라면 다음 흐름이 자연스럽다.

~~~text
Requirement
→ Design
→ Task
~~~

반면 기존 시스템 Migration은 다를 수 있다.

~~~text
Design Constraint
→ Requirement
→ Task
~~~

기존 Architecture, 배포 제약, 호환성 조건이 먼저 정해질 수 있기 때문이다.

중요한 것은 하나의 Planning Process를 모든 작업에 강요하지 않는 것이다.

Kiro나 Spec Kit 같은 specification-driven workflow에서도 핵심은 문서 형식 자체보다 **Intent와 실행 사이에 durable artifact를 둔다는 것**에 있다.

작은 수정에 20페이지 Spec을 만드는 것은 낭비다. 반대로 여러 모듈이 연결된 Migration을 한 줄 Prompt로 처리하는 것도 위험하다.

Planning Depth는 Task의 Risk와 Complexity에 맞춰야 한다.

---

## 4.4 Requirement Generator와 Acceptance Authority를 분리한다

Agent가 Requirement 초안을 만드는 것은 유용하다.

오히려 Agent는 다음 질문을 잘 찾을 수 있다.

- 모호한 표현은 무엇인가
- 충돌하는 조건이 있는가
- Edge Case가 빠졌는가
- 기존 코드와 맞지 않는 가정이 있는가

하지만 여기서 중요한 경계가 있다.

~~~text
Requirement Generator
≠ Acceptance Authority
~~~

Agent가 Requirement도 만들고, Test도 만들고, 구현도 하고, 완료 판정까지 모두 한다면 같은 오해를 끝까지 유지할 수 있다.

예를 들어 사용자가 원한 것은 reusable library인데 Agent가 demo application으로 Requirement를 잘못 해석했다고 하자. Agent가 자신의 해석을 기준으로 Test까지 만들면 Test는 모두 통과할 수 있다. 하지만 원래 Intent는 충족되지 않았다.

그래서 Factory에서는 역할을 분리할 수 있다.

~~~text
Human / Product
→ Intent Authority

Agent
→ Requirement Draft / Clarification

System / Reviewer
→ Acceptance Approval
~~~

작은 maintenance Task에서는 이 과정이 자동화될 수 있다.

중요한 것은 누가 문서를 작성했느냐보다 **누가 최종 의미를 승인하느냐**다.

---

## 4.5 Requirement에서 Verification까지 연결한다

좋은 Factory는 Work Artifact를 서로 연결한다.

~~~text
Requirement R1
→ Design D1
→ Task T3
→ Commit C7
→ Verification V2
→ Evidence A4
~~~

이 연결이 있으면 다음 질문에 답하기 쉬워진다.

- 이 Requirement를 구현한 Task는 무엇인가
- 이 Task는 어떤 Test로 검증됐는가
- Requirement가 바뀌었는데 Test가 그대로인 것은 아닌가
- 변경된 코드가 어떤 Acceptance Criteria와 연결되는가

Traceability를 처음부터 완벽하게 만들 필요는 없다.

Minimum Viable Factory라면 다음 정도만 있어도 충분하다.

~~~text
Task
→ Acceptance
→ Verification Command
→ Result
~~~

예:

~~~text
Task:
expired JWT handling

Acceptance:
expired token → 401

Verification:
./gradlew test --tests AuthServiceTest.expiredToken

Result:
PASS
~~~

이 연결이 반복되면 Agent의 자연어 완료 보고보다 훨씬 강한 완료 기준이 생긴다.

---

## 4.6 Ready Contract

Factory가 고도화되면 모든 Backlog Item을 곧바로 Worker에게 보내고 싶어진다.

하지만 Queue에 들어갈 수 있다고 실행 가능한 것은 아니다.

다음 Issue를 생각해 보자.

~~~text
성능 개선
~~~

무엇을 개선해야 하는가. 현재 수치는 얼마인가. 목표는 무엇인가. 어떤 환경에서 측정할 것인가.

이런 정보가 없으면 Agent가 많은 작업을 해도 완료 여부를 판단하기 어렵다.

그래서 Factory에는 간단한 Ready Contract가 필요하다.

~~~text
Goal
- 무엇을 바꿀 것인가

Scope
- 어디까지 수정 가능한가

Acceptance
- 무엇으로 완료를 확인할 것인가

Dependency
- 선행 작업이 있는가

Risk
- 특별한 승인이나 제한이 필요한가
~~~

모든 필드가 항상 필요하지는 않다.

Docs 수정은 Goal과 Acceptance만으로 충분할 수 있다. Production Migration은 훨씬 더 많은 정보가 필요하다.

> 실행 자동화보다 먼저, 어떤 Work가 실행 가능한 상태인지 정의해야 한다.

---

## 예: “로그인 오류 수정”을 Factory Task로 바꾸기

처음 Issue:

~~~text
로그인 오류 수정
~~~

Clarification 이후:

~~~text
Goal
- expired JWT 요청을 인증 실패로 처리

Scope
- auth module

Acceptance
- expired JWT → HTTP 401
- server error log 미발생
- valid JWT behavior 유지

Do Not Change
- DB schema
- OAuth flow

Verification
- AuthServiceTest.expiredToken
- auth integration test
~~~

이제 Agent가 무엇을 해야 하는지보다 더 중요한 것이 생겼다.

**무엇을 하면 끝난 것인지 알 수 있게 됐다.**

---

## 다음 질문

Requirement와 Acceptance가 준비됐다고 해도 아직 한 가지 문제가 남는다.

Agent가 실행 중 중단되면 이 Work는 어디에 남는가. Session이 닫히면 Task도 사라지는가. Retry할 때 처음부터 새로운 Prompt를 만들어야 하는가.

다음 장에서는 Prompt나 Session보다 오래 살아남는 작업 단위인 **Durable Task**를 정의한다.

---

## 참고 자료

- GitHub, *Spec Kit*  
  https://github.com/github/spec-kit
- Kiro, *Specs*  
  https://kiro.dev/docs/specs/
- Kiro, *Analyze Requirements*  
  https://kiro.dev/docs/specs/analyze-requirements/
- REAgent, *Requirement-Driven LLM Agents for Software Issue Resolution*  
  https://arxiv.org/abs/2604.06861
