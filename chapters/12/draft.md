# 12장. Verification: Agent가 완료했다고 말한 뒤부터가 시작이다

Agent가 다음과 같이 보고했다고 하자.

> 수정 완료했습니다. 테스트도 모두 통과했습니다.

Interactive 사용에서는 여기서 사람이 코드를 열어보고 판단할 수 있다.

Factory에서는 이 문장을 Task의 최종 상태로 사용하면 안 된다.

Agent의 보고는 하나의 **Completion Claim**이다.

Task를 DONE으로 만들 수 있는 **Completion Authority**와는 다르다.

이 책에서는 다음 구조를 기본으로 본다.

~~~text
Agent
→ Candidate Result
→ Verification
→ Evidence
→ Acceptance
~~~

Agent는 결과를 제안한다.

Verifier는 검증한다.

System이나 Human은 남은 위험을 받아들일지 결정한다.

> Agent가 "DONE"이라고 말하는 것과 Factory가 DONE이라고 판정하는 것은 다른 사건이다.

---

## 12.1 Completion Claim과 Completion Authority

Task를 수행한 Agent는 자신의 작업에 가장 많은 Context를 가지고 있다.

그래서 다음도 잘 설명할 수 있다.

- 어떤 파일을 바꿨는가
- 어떤 명령을 실행했는가
- 왜 이런 구현을 선택했는가
- 어떤 문제가 남았는가

하지만 자신의 작업을 설명할 수 있다는 것과 독립적으로 검증할 수 있다는 것은 다르다.

예를 들어 Agent가 다음과 같이 말할 수 있다.

~~~text
- expired JWT를 401로 수정
- unit test PASS
- integration test PASS
~~~

Factory는 최소한 다음을 독립적으로 확인할 수 있어야 한다.

~~~text
Result Revision
→ 실제 commit은 무엇인가

Verification
→ 어떤 command가 실행됐는가

Exit
→ 실제 result는 PASS인가

Acceptance
→ 401 behavior가 확인됐는가
~~~

즉 Agent의 자연어 Summary를 authoritative state로 사용하지 않는다.

---

## 12.2 Verification Pyramid

모든 Task에 같은 검증 비용을 쓸 필요는 없다.

검증은 여러 층으로 구성할 수 있다.

~~~text
Static
        ↓
Deterministic Test
        ↓
Runtime Verification
        ↓
Behavioral Evidence
        ↓
Independent Evaluator
        ↓
Human Acceptance
~~~

위로 갈수록 일반적으로 비용이 커지고, 더 넓은 종류의 오류를 잡을 수 있다.

### Static

- compile
- typecheck
- lint
- format
- schema validation

빠르고 deterministic하다.

### Deterministic Test

- unit
- integration
- contract
- migration test

Task의 구체적인 behavior를 검증한다.

### Runtime Verification

실제 Service를 실행한다.

- service boot
- API request
- DB migration
- background job

### Behavioral Evidence

사람이나 Evaluator가 실제 결과를 볼 수 있게 한다.

- screenshot
- video
- DOM
- logs
- traces
- benchmark

### Independent Evaluator

구현 Agent와 다른 Context나 Role을 가진 평가자가 결과를 점검한다.

### Human Acceptance

Residual Risk와 Product Intent를 최종적으로 사람이 판단한다.

Verification을 비용 순서의 Pyramid로만 볼 필요는 없다. **무엇에 대한 적합성을 검증하는가**라는 축도 필요하다.

~~~text
Functional Conformance
- 요구한 동작을 실제로 하는가

Architecture Conformance
- 정해진 Architecture / Design Constraint를 지켰는가

Scope Conformance
- 허용된 파일과 변경 범위를 벗어나지 않았는가

Security Conformance
- 필요한 Security Policy와 Review를 통과했는가
~~~

예를 들어 Test가 모두 PASS해도 Agent가 허용되지 않은 공통 모듈까지 수정했거나, Requirement가 요구한 Architecture Boundary를 우회했다면 Production-ready Change라고 보기 어렵다.

Caylent는 Software Factory Harness가 Security Review, Architectural Conformance, Scope 이탈 여부를 실행 Loop 안에서 점검해야 한다고 설명한다. 현재 공개 DevBench 구현은 이를 code/test/doc review, 실제 변경과 Changes Manifest의 비교, 별도 Security Review 같은 Gate로 구체화한다.

~~~text
Behavior PASS
+
Architecture PASS
+
Scope PASS
+
Security PASS
→ stronger completion evidence
~~~

모든 Task가 네 축을 모두 요구하는 것은 아니다. 핵심은 Functional Test 하나가 전체 Conformance를 대표한다고 가정하지 않는 것이다.

모든 Task가 Pyramid 끝까지 갈 필요는 없다.

Docs typo는 lint와 preview만으로 충분할 수 있다.

Payment Logic 변경은 integration, security, human review까지 필요할 수 있다.

---

## 12.3 Verification은 마지막 단계가 아니라 Feedback Loop다

검증을 마지막에 한 번만 수행하면 Agent는 오랫동안 잘못된 방향으로 갈 수 있다.

더 좋은 구조는 실행 중에도 빠른 Feedback을 주는 것이다.

~~~text
Edit
→ Fast Check
→ Fix
→ Targeted Test
→ Fix
→ Candidate
→ Expensive Verification
~~~

예를 들어 Java Backend Task라면 다음처럼 계층화할 수 있다.

~~~text
1. compile
2. target unit test
3. module integration test
4. full regression
~~~

초기 수정마다 Full Regression을 돌리면 비용이 너무 크다.

반대로 Target Test만 보고 끝내면 Integration 문제를 놓칠 수 있다.

그래서 Verification도 비용과 범위에 따라 단계화한다.

~~~text
Cheap Feedback
→ Candidate Confidence
→ Expensive Acceptance
~~~

이 구조는 CI Capacity 관리와도 연결된다.

---

## 12.4 Executable Acceptance

4장에서 Requirement와 Acceptance를 분리했다.

Verification은 그 Acceptance를 실행 가능한 형태로 바꾸는 단계다.

예:

~~~text
Requirement
- expired JWT는 인증 실패다.

Acceptance
- protected endpoint 호출 시 HTTP 401

Verification
- integration test
- runtime request
~~~

연결하면 다음과 같다.

~~~text
Requirement
      ↓
Acceptance
      ↓
Executable Check
      ↓
Evidence
~~~

이 Traceability가 강할수록 Agent가 “무엇을 해야 하는가”와 “무엇을 하면 끝인가”를 같은 방향으로 볼 수 있다.

단, 한 가지 주의가 필요하다.

Acceptance를 Test 하나와 완전히 동일시하면 안 된다.

---

## 12.5 Test PASS가 User Intent와 같지 않은 이유

Test는 강력하다.

Agent에게 빠르고 deterministic한 Feedback을 준다.

하지만 Test는 **검사한 것만** 확인한다.

Microsoft Research의 2026년 preprint *Building to the Test*는 두 production coding agent를 사용한 18회 controlled run에서 이런 위험을 관찰했다. Hidden Playwright oracle을 Agent loop에 제공하자 점수는 거의 완벽해졌지만, 요청된 reusable library 대신 tested behavior를 직접 담은 demo 형태로 우회하는 결과가 나올 수 있었다. 저자들도 다른 Agent·Signal·Model Family에서의 prevalence는 열린 질문이라고 명시한다.

예를 들어 사용자는 다음을 원했다고 하자.

~~~text
여러 Service에서 재사용할 수 있는 rate-limit library를 만들어라.
~~~

Visible Test는 한 Service에서 특정 요청이 제한되는지만 검사한다.

Agent는 해당 Service에 직접 조건문을 넣어 Test를 통과시킬 수 있다.

~~~text
Visible Test
→ PASS

Original Intent
→ reusable library
→ FAIL
~~~

이것이 Building to the Test 문제다.

Test를 없애야 한다는 뜻이 아니다.

Validation의 종류를 넓혀야 한다.

- structural check
- hidden test
- runtime scenario
- code review
- independent evaluator

---

## 12.6 Automated Grader PASS와 Maintainer Acceptance는 다르다

METR의 2026년 연구 노트는 SWE-bench Verified에서 자동 grader를 통과한 Patch를 실제 Maintainer에게 다시 검토하게 했다. 4명의 Maintainer가 3개 Repository의 95개 Issue 범위를 다룬 표본에서, Test를 통과한 AI Patch의 상당수가 실제 main에는 Merge되지 않았을 것으로 평가됐다. 다만 Agent에게 Review Feedback을 받고 반복 수정할 기회를 주지 않은 single-shot 평가라는 제한이 있다.

이 차이는 이상하지 않다.

Maintainer는 Test 외에도 다음을 본다.

- Repository Convention
- Code Quality
- Unintended Behavior
- Maintainability
- Broader Integration
- Scope Appropriateness

따라서 다음 등식은 성립하지 않는다.

~~~text
Automated Test PASS
=
Production-ready Change
~~~

Factory의 Verification은 Test Runner 하나보다 넓어야 한다.

---

## 12.7 Reward Hacking

더 위험한 경우도 있다.

Agent가 Task를 해결하는 대신 **검증 신호를 약화시킬 수 있다.**

예:

~~~text
실패하는 Test를 skip 처리
Test assertion 삭제
Validation Script 수정
Scoring condition 우회
~~~

결과만 보면 PASS다.

실제 문제는 해결되지 않았다.

OpenAI는 2026년 내부 Coding Agent Monitoring 결과에서 Test를 항상 통과하도록 수정하거나 Check를 비활성화하는 Reward Hacking을 실제 관찰 범주로 공개했고, 빈도는 rare이지만 severity는 높게 분류했다. 이 역시 OpenAI 내부 deployment의 관찰이며 일반적인 발생률로 해석하면 안 된다.

Factory에서는 다음 경계를 고려할 수 있다.

- Agent가 Verification Definition을 자유롭게 수정하지 못하게 한다.
- Test 변경을 별도 Evidence로 표시한다.
- 평가 코드/hidden test를 Worker에서 보호한다.
- Verification Profile을 Control Plane이 정한다.

특히 구현 Agent가 자신을 평가하는 기준까지 마음대로 바꿀 수 있는 구조는 위험하다.

---

## 12.8 Lucky Pass: 결과만 맞아도 충분한가

Final Test가 통과했지만 Trajectory가 불안정할 수도 있다.

Microsoft AgentLens 연구는 8개 Model Backend의 2,614개 OpenHands Trajectory를 분석했고, process reference를 구성할 수 있었던 47개 Task의 1,815개 Trajectory subset에서 Passing Trajectory의 10.7%를 Lucky Pass로 분류했다. 저자들은 반복 Regression, Blind Retry, Verification 누락처럼 결과 PASS만으로 가려지는 Process 문제를 분석한다.

예:

~~~text
Edit
→ test fail

random edit
→ another test fail

revert

different edit
→ PASS
~~~

최종 결과만 보면 성공이다.

하지만 다음 Task에서도 같은 성공을 재현할 수 있을지는 불확실하다.

Factory에서는 Outcome뿐 아니라 Process Signal도 일부 관찰할 수 있다.

- retry 횟수
- test weakening
- regression count
- verification skipped
- unsafe command
- repeated same failure

이 정보는 19장의 Observability에서 더 자세히 다룬다.

---

## 12.9 Independent Evaluator

구현 Agent와 평가 Agent를 분리하면 장점이 있다.

~~~text
Implementer
→ Candidate

Evaluator
→ inspect
→ test
→ behavioral check
→ feedback
~~~

Anthropic의 long-running application harness 연구에서도 Planner, Generator, Evaluator를 분리하는 방향이 사용됐다.

하지만 Evaluator Agent가 있다고 자동으로 독립 검증이 되는 것은 아니다.

같은 Model, 같은 Context, 같은 Assumption을 사용하면 같은 오류를 공유할 수 있다.

~~~text
Same Model
+ Same Context
+ Same Tests
→ Correlated Error 가능
~~~

그래서 Independent Evaluation은 다양한 방법을 조합할 수 있다.

- deterministic tests
- separate context
- different role
- different model
- hidden check
- human review

핵심은 Agent 수가 아니라 **검증 신호의 독립성**이다.

---

## 12.10 Task별 Verification Policy

Agent에게 “적절한 테스트를 알아서 해라”라고만 하지 않는다.

Task Risk에 따라 최소 Verification을 System Policy로 정할 수 있다.

### Low Risk

~~~text
docs
generated file
test-only change
~~~

예:

~~~text
lint
preview
diff check
~~~

### Medium Risk

~~~text
business logic
API behavior
~~~

예:

~~~text
unit
integration
contract
agent review
~~~

### High Risk

~~~text
auth
payment
migration
infrastructure
~~~

예:

~~~text
unit
integration
security
migration check
runtime verification
human approval
~~~

이 구조에서는 Agent가 Test 하나를 생략해도 Task가 DONE으로 이동할 수 없다.

Required Verification은 Control Plane이 알고 있기 때문이다.

---

## 예: UI Task와 Backend Auth Task

### UI Task

Goal:

~~~text
모바일 화면에서 신청 버튼이 겹치지 않게 수정
~~~

Verification:

~~~text
typecheck
E2E
mobile viewport screenshot
human visual acceptance
~~~

Source Diff만으로는 화면을 판단하기 어렵다.

### Auth Task

Goal:

~~~text
expired JWT → 401
~~~

Verification:

~~~text
unit
integration
contract
security scan
runtime request
~~~

같은 “코드 수정”이라도 필요한 Evidence가 다르다.

Verification Profile은 Task type과 Risk에 맞아야 한다.

---

## Verification 설계에서 묻는 질문

~~~text
1. Agent의 자기 보고 외에 무엇으로 확인할 것인가?
2. Acceptance를 실행 가능한 Check로 바꿀 수 있는가?
3. Visible Test에만 과적합할 수 있는가?
4. Agent가 Verification Definition을 약화시킬 수 있는가?
5. Runtime Behavior를 봐야 하는가?
6. Independent Evaluator나 Human Gate가 필요한가?
7. 실제 변경이 선언된 Scope를 벗어나지 않았는가?
8. Architecture / Design Constraint를 별도로 확인해야 하는가?
9. 이 Task의 Risk에 비해 Verification Cost가 적절한가?
~~~

---

## 다음 질문

Verification이 끝났다고 사람이 결과를 빠르게 이해할 수 있는 것은 아니다.

Commit은 무엇인지, 어떤 Test가 실행됐는지, Screenshot은 어디 있는지, Known Risk는 무엇인지 매번 찾아야 한다면 Review 비용이 커진다.

다음 장에서는 검증 결과를 표준화된 **Evidence Contract**로 묶는 방법을 다룬다.

---

## 참고 자료

- Microsoft Research, *Building to the Test: Coding Agents Deliver What You Check, Not What You Requested*  
  https://www.microsoft.com/en-us/research/publication/building-to-the-test-coding-agents-deliver-what-you-check-not-what-you-requested/
- METR, *Many SWE-bench-Passing PRs Would Not Be Merged into Main*  
  https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
- OpenAI, *How we monitor internal coding agents for misalignment*  
  https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/
- Microsoft Research, *AgentLens*  
  https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/
- Caylent, *What is a Software Factory*  
  https://www.youtube.com/watch?v=0Q8R_FZbnLk
- Caylent Solutions, *DevBench Architecture*  
  https://github.com/caylent-solutions/devbench/blob/main/docs/architecture.md
