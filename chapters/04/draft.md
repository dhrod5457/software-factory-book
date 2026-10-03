# 4장. Prompt가 아니라 Requirement와 Acceptance에서 시작한다

AI 코딩 에이전트를 쓰다 보면 가장 먼저 하고 싶은 일은 바로 시키는 것이다.

> 로그인 오류를 고쳐라.

> 출결 화면을 개선해라.

> 이 모듈을 리팩터링해라.

작은 작업에서는 충분할 수 있다. 하지만 작업이 커지면 곧 다른 질문이 생긴다. 어떤 로그인 오류를 고쳐야 하는지, 정상 동작은 무엇인지부터 확인해야 한다. 기존 동작 중 무엇을 유지하고 어디까지 수정해도 되는지, 무엇을 확인하면 완료로 볼 수 있는지도 정해야 한다. 사람끼리 일할 때는 이런 질문을 대화 속에서 자연스럽게 채우기도 한다. 경험이 많은 개발자는 조직의 암묵적 규칙까지 알고 있다. 에이전트에게도 같은 암묵지를 기대하면 문제가 생긴다.

에이전트는 주어진 정보 안에서 가장 그럴듯한 해석을 선택할 수 있다. 하지만 그 해석이 원래 의도와 같다는 보장은 없다. 그래서 생산 시스템에서 첫 번째로 필요한 것은 더 긴 지시문이 아니다.

**무엇을 만들어야 하는지 정하는 요구사항(Requirement)과 무엇을 확인해야 받아들일 수 있는지 정하는 수용 기준(Acceptance)을 만드는 일**이다.

---

## 4.1 Prompt만으로 큰 Work를 관리하기 어려운 이유

지시문은 빠르다. 문제를 설명하고 곧바로 실행할 수 있다. 하지만 지시문에는 보통 목표, 배경, 가정, 제약, 설계에 관한 힌트, 기대하는 결과가 섞여 있다. 이 정보가 한 번의 대화 안에만 남으면 시간이 지나면서 해석이 달라질 수 있다. 예를 들어 다음 이슈를 보자.

~~~text
로그인 오류 수정
~~~

개발자에게는 충분할 수 있다. 이미 장애 상황을 알고 있기 때문이다. 에이전트 입장에서는 다르다.

- 비밀번호 오류인가
- JWT 만료인가
- OAuth 리디렉션 문제인가
- 세션 생성 실패인가
- HTTP 상태가 잘못됐는가

가능한 해석이 많다. 에이전트가 저장소를 읽으며 추측할 수는 있다. 하지만 추측이 맞았는지 확인할 기준이 없다. 그래서 큰 작업에서는 지시문보다 중단 뒤에도 남는 산출물이 필요하다.

~~~text
Conversation
→ ephemeral

Requirement
Acceptance
Design Constraint
Task
→ durable
~~~

이 문서가 거대한 명세서일 필요는 없다. 핵심은 에이전트 세션이 바뀌어도 작업의 의미가 유지되는 것이다.

---

## 4.2 Intent에서 Acceptance까지

생산 시스템 앞단을 다음처럼 볼 수 있다.

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

이 정도만 있어도 에이전트가 탐색해야 하는 범위가 크게 줄어든다. 더 중요한 점은 검증이 가능해진다는 것이다.

~~~text
Requirement
→ Acceptance
→ Test / Runtime Check
~~~

좋은 요구사항은 구현 방법을 세세하게 지시하는 문서가 아니다. 에이전트가 여러 구현 방법 중 선택할 수 있도록 하면서도 완료 여부는 명확하게 판단할 수 있게 해야 한다.

---

### Triage: 모든 Signal을 같은 깊이로 명세하지 않는다

요구사항부터 정하는 방식이라는 말이 모든 이슈에 같은 분량의 문서를 만들라는 뜻은 아니다. 생산 시스템 앞단에는 먼저 **계획의 상세 수준을 정하는 분류와 우선순위 판단**이 필요할 수 있다.

~~~text
Signal / Idea / Issue
        ↓
      Triage
        ↓
  ┌─────┴─────┐
  │           │
Simple      Complex
  │           │
Task      Product Spec
              ↓
         Technical Spec
              ↓
             Task
~~~

Zach Lloyd는 Warp의 생산 시스템 설명에서 단순하고 명확한 이슈는 바로 구현으로 보내고, 복잡한 문제는 명세 에이전트로 보내는 패턴을 제시한다. 이때 제품 명세는 제품에서 항상 지켜야 하는 조건을, 기술 명세는 설계 구조와 코드의 형태를 설명한다고 구분한다. 이 책에서는 이 구조를 그대로 표준으로 삼기보다 다음 질문으로 일반화한다.

~~~text
Product / Requirement
→ 무엇이 참이어야 하는가

Design / Technical Spec
→ 어떤 제약과 구조 안에서 만들 것인가

Task
→ 무엇을 수행할 것인가

Acceptance
→ 무엇이 만족되어야 하는가

Verification
→ 그것을 어떻게 증명할 것인가
~~~

핵심은 문서 종류를 늘리는 데 있지 않다.

**모호성과 위험이 커질수록 실행 전에 의미와 완료 기준을 중단돼도 기록이 더 분명히 남도록 만든다.**

작고 명확한 수정은 곧바로 작업이 될 수 있고, 여러 모듈과 제품 판단이 얽힌 작업은 명세 단계를 거칠 수 있다.

---

## 4.3 Requirements-first와 Design-first

모든 작업이 요구사항부터 시작하는 것은 아니다. 새 기능이라면 다음 흐름이 자연스럽다.

~~~text
Requirement
→ Design
→ Task
~~~

반면 기존 시스템 마이그레이션은 다를 수 있다.

~~~text
Design Constraint
→ Requirement
→ Task
~~~

기존 설계 구조, 배포 제약, 호환성 조건이 먼저 정해질 수 있기 때문이다. 중요한 것은 하나의 계획 수립 과정을 모든 작업에 강요하지 않는 것이다.

2026년 9월 기준 GitHub Spec Kit의 기본 SDD 흐름은 `Specify → Plan → Tasks → Implement → Converge`이고, Kiro도 요구사항·설계·작업을 별도 산출물로 관리한다. 제품별 절차는 다르지만 여기서 가져올 원칙은 문서 형식 자체가 아니라 **의도와 실행 사이에 중단 뒤에도 남는 산출물과 검증 가능한 연결을 둔다는 것**이다.

작은 수정에 20페이지 명세를 만드는 것은 낭비다. 반대로 여러 모듈이 연결된 마이그레이션을 한 줄 지시문으로 처리하는 것도 위험하다. 계획의 상세 수준은 작업의 위험과 복잡도에 맞춰야 한다.

---

## 4.4 산업 사례: Specification과 Architecture가 Backlog로 합쳐진다

Caylent가 공개한 소프트웨어 생산 시스템 설명은 생산 시스템 앞단을 어떻게 준비하는지 보여주는 사례다. 이들의 설명에서는 먼저 범위를 정리하고 Claude를 사용해 시제품 명세를 만든다. 이후 고객에게 반복적으로 새 버전을 보여주며 피드백을 받고, 동시에 운영 환경에 필요한 구조를 설계한다. 두 흐름은 최종적으로 상세 명세와 할 일 목록으로 합쳐지고, 그 결과가 소프트웨어 생산 시스템의 입력이 된다.

~~~text
Scoping
    ↓
Prototype Specification
    ↓
Customer Feedback ───────┐
                         ├→ Detailed Specification
Production Architecture ─┘
                         ↓
                      Backlog
                         ↓
                  Software Factory
~~~

여기서 가져올 원칙은 특정 기간이나 컨설팅 과정이 아니다.

> 생산 시스템의 입력은 정리되지 않은 아이디어가 아니라, 실행 가능한 수준으로 정리된 명세와 설계 구조 제약, 할 일 목록에 가까워질수록 안정적이다.

이는 제품으로 만들 대상을 탐색하는 과정을 모두 자동화해야 한다는 뜻도 아니다. 오히려 의도와 설계 구조를 먼저 정리하고, 에이전트가 실행할 작업과 완료 기준으로 변환하는 경계가 필요하다는 사례다.

---

### WorkOS: 빈 문서를 Agent가 먼저 채우고 사람이 Scope를 결정한다

WorkOS의 제품 개발 과정에는 `Hilltop`이라는 PRD 성격의 산출물이 있다. 프로젝트 목적, 고객의 필요, 경쟁 상황, 초기 설계, 주요 일정 같은 정보를 한곳에 모으고, 에이전트가 짧은 설명에서 첫 초안을 만든 뒤 사람이 검토와 범위 조정을 수행한다. 승인된 산출물은 다시 구현 작업 티켓으로 분해된다.

~~~text
Brief
→ Agent First Draft
→ Human Review / Scope Correction
→ Approved Product Artifact
→ Task Decomposition
→ Execution
~~~

중요한 점은 에이전트가 제품에 담긴 의도의 최종 권한까지 갖는 것이 아니다. 발표에서는 에이전트가 실제 의도보다 범위를 크게 잡는 경우도 있다고 설명한다. 하지만 빈 문서에서 모든 산출물을 사람이 처음부터 만드는 것보다, 에이전트가 맥락 정보를 모아 첫 초안을 만들고 사람이 잘라내고 보정하는 방식이 개발에 드는 주의와 노력을 줄일 수 있다. 따라서 요구사항 작성 자동화는 다음처럼 볼 수 있다.

~~~text
Agent
- research
- context collection
- first draft
- decomposition

Human
- intent
- scope
- trade-off
- acceptance authority
~~~

## 4.5 Requirement Generator와 Acceptance Authority를 분리한다

에이전트가 요구사항 초안을 만드는 것은 유용하다. 오히려 에이전트는 다음 질문을 잘 찾을 수 있다.

- 모호한 표현은 무엇인가
- 충돌하는 조건이 있는가
- 경계 상황이 빠졌는가
- 기존 코드와 맞지 않는 가정이 있는가

하지만 여기서 중요한 경계가 있다.

~~~text
Requirement Generator
≠ Acceptance Authority
~~~

에이전트가 요구사항도 만들고, 테스트도 만들고, 구현도 하고, 완료 판정까지 모두 한다면 같은 오해를 끝까지 유지할 수 있다. 예를 들어 사용자가 원한 것은 재사용 가능한 라이브러리인데 에이전트가 시연용 애플리케이션으로 요구사항을 잘못 해석했다고 하자. 에이전트가 자신의 해석을 기준으로 테스트까지 만들면 테스트는 모두 통과할 수 있다. 하지만 원래 의도는 충족되지 않았다. 그래서 생산 시스템에서는 역할을 분리할 수 있다.

~~~text
Human / Product
→ Intent Authority

Agent
→ Requirement Draft / Clarification

System / Reviewer
→ Acceptance Approval
~~~

작은 유지보수 작업에서는 이 과정이 자동화될 수 있다. 중요한 것은 누가 문서를 작성했느냐보다 **누가 최종 의미를 승인하느냐**다.

---

## 4.6 Requirement에서 Verification까지 연결한다

좋은 생산 시스템은 작업 산출물을 서로 연결한다. Spec Kit의 최신 `converge` 단계처럼 구현 결과를 다시 명세·계획·작업과 대조하는 흐름도 이 연결의 한 사례다.

~~~text
Requirement R1
→ Design D1
→ Task T3
→ Commit C7
→ Verification V2
→ Evidence A4
~~~

이 연결이 있으면 다음 질문에 답하기 쉬워진다.

- 이 요구사항을 구현한 작업은 무엇인가
- 이 작업은 어떤 테스트로 검증됐는가
- 요구사항이 바뀌었는데 테스트가 그대로인 것은 아닌가
- 변경된 코드가 어떤 수용 기준과 연결되는가

추적 가능성을 처음부터 완벽하게 만들 필요는 없다. 최소 기능 생산 시스템이라면 다음 정도만 있어도 충분하다.

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

이 연결이 반복되면 에이전트의 자연어 완료 보고보다 훨씬 강한 완료 기준이 생긴다.

---

## 4.7 Ready Contract

생산 시스템이 고도화되면 모든 할 일 목록 항목을 곧바로 워커에게 보내고 싶어진다. 하지만 대기열에 들어갈 수 있다고 실행 가능한 것은 아니다. 다음 이슈를 생각해 보자.

~~~text
성능 개선
~~~

무엇을 개선해야 하는가. 현재 수치는 얼마인가. 목표는 무엇인가. 어떤 환경에서 측정할 것인가. 이런 정보가 없으면 에이전트가 많은 작업을 해도 완료 여부를 판단하기 어렵다. 그래서 생산 시스템에는 간단한 실행 준비 조건이 필요하다.

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

모든 필드가 항상 필요하지는 않다. 문서 수정은 목표와 수용 판단만으로 충분할 수 있다. 운영 환경 마이그레이션은 훨씬 더 많은 정보가 필요하다.

> 실행 자동화보다 먼저, 어떤 작업이 실행 가능한 상태인지 정의해야 한다.

---

## 예: “로그인 오류 수정”을 Factory Task로 바꾸기

처음 이슈:

~~~text
로그인 오류 수정
~~~

불명확한 내용 확인 이후:

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

이제 에이전트가 무엇을 해야 하는지보다 더 중요한 것이 생겼다.

**무엇을 하면 끝난 것인지 알 수 있게 됐다.**

---

## 다음 질문

요구사항과 수용 판단이 준비됐다고 해도 아직 한 가지 문제가 남는다. 에이전트가 실행 중 중단되면 이 작업은 어디에 남는가. 세션이 닫히면 작업도 사라지는가. 재시도할 때 처음부터 새로운 지시문을 만들어야 하는가. 다음 장에서는 지시문이나 세션보다 오래 살아남는 작업 단위인 **지속 작업**을 정의한다.

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
- Caylent, *What is a Software Factory*  
  https://www.youtube.com/watch?v=0Q8R_FZbnLk
- Warp / Zach Lloyd, *Software Engineering Is Becoming Factory Engineering*  
  https://www.youtube.com/watch?v=tUPPVhBBcoM
