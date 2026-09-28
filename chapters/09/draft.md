# 9장. Harness Engineering: Agent가 일할 수 있는 환경 만들기

같은 Model을 쓰는데 팀마다 결과가 크게 다를 수 있다.

한쪽에서는 Repository를 잘 탐색하고 필요한 Test를 찾아 안정적으로 수정한다.

다른 쪽에서는 파일을 헤매고, 불필요한 명령을 반복하고, 긴 로그를 Context에 가득 넣은 뒤 방향을 잃는다.

차이는 Model만으로 설명하기 어렵다.

Agent가 실제로 일하는 방식은 Model 주변 환경에 크게 영향을 받는다.

이 책에서는 이 환경을 **Harness**라고 부른다.

~~~text
Harness
=
Instructions
+ Context
+ Tools
+ Execution
+ Feedback
+ Verification
~~~

Harness Engineering은 Prompt를 더 잘 쓰는 기술보다 넓다.

Agent가 Repository와 Tool을 어떻게 보고, 어떤 결과를 받고, 어떤 규칙이 강제되는지를 설계하는 일이다.

---

## 9.1 Harness란 무엇인가

Model은 혼자 Repository를 수정하지 않는다.

다음과 같은 계층이 필요하다.

~~~text
Task
      ↓
Harness
  - instructions
  - context
  - tools
  - skills
  - search
  - browser
  - result filtering
      ↓
Model
      ↓
Tool Actions
      ↓
Repository / Runtime
~~~

Harness는 Model과 실제 Software Environment 사이의 인터페이스다.

예를 들어 Agent가 Test 실패를 분석해야 한다고 하자.

Model이 보는 것은 실제 10MB 로그 전체일 수도 있고, Harness가 정리한 실패 목록일 수도 있다.

~~~text
Option A
→ raw test log 10MB

Option B
→ failed tests: 3
→ top stack trace
→ artifact URI
→ detail tool
~~~

두 경우 같은 Model을 사용해도 행동은 달라진다.

Harness가 Agent의 탐색 비용과 오류 가능성을 바꾼다.

---

## 9.2 Agent-Computer Interface

사람에게 좋은 CLI가 Agent에게도 항상 좋은 것은 아니다.

SWE-agent는 이 문제를 Agent-Computer Interface, ACI라는 관점으로 다뤘다.

핵심은 Tool의 존재 여부뿐 아니라 **Agent가 Tool을 어떻게 사용하게 되는가**다.

예를 들어 사람은 다음 명령을 실행하고 긴 출력에서 필요한 부분을 찾을 수 있다.

~~~text
cat huge_file.log
~~~

Agent에게 같은 방식으로 5만 줄을 반환하면 Context를 낭비할 수 있다.

대신 다음처럼 만들 수 있다.

~~~text
log_summary()
failed_tests()
failure_detail(test_id)
~~~

File Viewer도 마찬가지다.

사람은 IDE에서 자유롭게 스크롤할 수 있다.

Agent에게는 다음 정보가 더 중요할 수 있다.

- line number
- symbol boundary
- truncated indicator
- next range
- search result ranking

Edit Tool도 단순 파일쓰기보다 다음 Feedback을 주면 유리하다.

~~~text
edit applied
lint: failed
line 42: incompatible type
~~~

Tool이 Agent에게 즉시 구조화된 Feedback을 주면 잘못된 수정이 다음 단계까지 퍼지는 것을 줄일 수 있다.

---

## 9.3 Instruction, Skill, Tool, MCP의 역할을 나눈다

Agent customization 기능이 늘어나면 모든 것을 한 파일에 넣고 싶어진다.

하지만 역할을 분리하는 편이 유지보수하기 쉽다.

이 책에서는 다음처럼 구분한다.

### Instruction

지속적으로 알아야 하는 Guideline이다.

예:

~~~text
- Java 21 사용
- 기존 API response envelope 유지
- 테스트 없는 behavior change 금지
~~~

### Skill

반복해서 사용하는 Procedure다.

예:

~~~text
DB migration verification
release-note generation
UI screenshot validation
~~~

Skill은 필요할 때 불러오는 것이 좋다.

모든 Task에 항상 넣을 필요는 없다.

### Tool

Agent가 외부 행동을 수행하는 Interface다.

예:

~~~text
run_test()
search_log()
deploy_staging()
get_issue()
~~~

### MCP

외부 System의 Tool과 Data를 Agent에 노출하는 Protocol Surface로 볼 수 있다.

예:

- Issue
- CI
- Documentation
- Logs
- Monitoring
- Internal API

중요한 점은 MCP가 Durable Task State 자체는 아니라는 것이다.

~~~text
MCP
= capability / context access

Task Store
= orchestration state
~~~

둘을 섞지 않는다.

---

## 9.4 반드시 지켜야 할 규칙은 Prompt에만 두지 않는다

다음 규칙을 생각해보자.

~~~text
main branch에 직접 push하지 마라.
~~~

Instruction에 적어둘 수 있다.

하지만 반드시 지켜야 한다면 Branch Protection으로 막는 편이 낫다.

다른 예도 같다.

~~~text
secret commit 금지
→ secret scanner / hook

required test pass
→ verification gate

forbidden path 변경 금지
→ policy / hook

production deploy 승인 필요
→ permission / approval
~~~

Harness Engineering에서 중요한 경계는 다음이다.

~~~text
Explain
→ Instruction

Reusable Procedure
→ Skill

Action
→ Tool

Must Enforce
→ Policy / Hook
~~~

Agent가 규칙을 이해하도록 하는 것과 시스템이 규칙을 강제하는 것은 다른 문제다.

---

## 9.5 Tool은 Agent를 위한 API다

사람용 API와 Agent Tool은 목적이 조금 다르다.

사람은 Documentation을 읽고 parameter를 이해할 수 있다.

Agent는 Tool 이름, schema, result를 보고 행동 전략을 세운다.

그래서 좋은 Tool은 보통 다음 특성을 가진다.

- 책임이 좁고 명확하다.
- 이름으로 행동을 추측할 수 있다.
- 결과가 구조화되어 있다.
- 너무 많은 데이터를 한 번에 반환하지 않는다.
- 실패 이유가 machine-readable하다.
- 다음 행동을 선택할 단서가 있다.

예를 들어 이런 Tool이 있다고 하자.

~~~text
get_everything()
~~~

Issue, Log, Test, Deployment 상태를 한 번에 반환한다.

처음에는 편해 보인다.

하지만 Output이 커지고 Agent가 어떤 데이터가 최신인지 판단하기 어려워진다.

다음처럼 분리하는 편이 낫다.

~~~text
test_summary()
failed_tests()
test_failure_detail(id)
artifact_get(id)
log_search(query)
~~~

Agent가 필요할 때 점진적으로 조회한다.

이것이 Progressive Retrieval이다.

---

## 9.6 Result Gateway

Tool Output이 큰 시스템에서는 Model 앞에 Result Gateway를 둘 수 있다.

~~~text
Tool / Runtime
      ↓
Result Gateway
      ↓
Summary + Index + Artifact Ref
      ↓
Agent
~~~

예를 들어 Full Regression이 수천 개 Test를 실행했다고 하자.

Agent에게 필요한 것은 보통 전체 PASS 로그가 아니다.

~~~text
tests: 1370
passed: 1367
failed: 3

failures:
- AuthServiceTest.expiredToken
- LoginControllerTest.invalidSession
- SecurityFilterTest.missingHeader

full_log:
artifact://verify/932/log.txt
~~~

Agent는 실패한 세 개만 자세히 볼 수 있다.

이 구조는 Token 절약만을 위한 것이 아니다.

Signal-to-noise ratio를 높이는 것이 목적이다.

너무 짧게 요약해 중요한 정보를 없애도 문제가 된다.

그래서 Summary와 Detail Retrieval을 함께 제공해야 한다.

---

## 9.7 Tool을 늘리면 항상 좋아지는가

Tool이 많으면 Agent가 할 수 있는 일이 늘어난다.

하지만 선택 공간도 커진다.

비슷한 Tool이 여러 개 있으면 잘못 선택할 수 있다.

권한 범위도 넓어진다.

Context에 Tool schema가 많이 들어가면 비용도 증가할 수 있다.

따라서 Tool Set도 Task별로 조절할 수 있다.

예:

~~~text
docs-worker
- repo read/write
- markdown lint
- docs preview

backend-worker
- repo
- shell
- test
- internal API

release-worker
- repo read
- build artifact
- release tool
- approval gate
~~~

모든 Worker에 모든 Tool을 주는 것보다 capability를 좁히는 편이 보안과 reliability 모두에 도움이 될 수 있다.

---

## 9.8 Harness도 Regression이 생긴다

Tool을 업그레이드하면 성능이 좋아질 것이라고 생각하기 쉽다.

하지만 Tool Interface가 바뀌면 기존 Instruction과 Agent 행동 전략이 더 이상 맞지 않을 수 있다.

GitHub는 Copilot Code Review 개선 과정에서 더 좋은 Tool을 추가했지만 초기에는 오히려 비용이 늘고 이슈 검출이 악화된 사례를 공개했다. 이후 Instruction과 Workflow를 함께 조정해야 했다.

이 사례의 교훈은 단순하다.

> Harness도 Software다.

Harness를 바꿀 때도 다음을 해야 한다.

- version
- test
- eval
- rollout
- compare
- rollback

Model 평가만 하고 Harness 변경은 검증하지 않는다면 실제 Factory 성능 변화를 설명하기 어렵다.

---

## 9.9 Prepared Harness

Worker Profile이 Runtime을 준비한다면 Prepared Harness는 Task 유형에 맞는 Agent 환경을 준비한다.

예를 들어 Backend Fix Profile은 다음처럼 구성할 수 있다.

~~~text
Runtime
- JDK 21
- Gradle

Instructions
- backend conventions

Skills
- targeted-test
- api-contract-check

Tools
- repo search
- shell
- test
- log search

Verification
- unit
- integration
~~~

UI Task는 다르다.

~~~text
Runtime
- Node
- Browser

Skills
- browser-check
- screenshot-compare

Tools
- DOM
- screenshot
- console log

Verification
- E2E
- visual evidence
~~~

이렇게 하면 Agent가 Task마다 자신의 Toolchain을 처음부터 조립할 필요가 없다.

---

## Model 문제인가 Harness 문제인가

Agent가 실패했을 때 바로 Model을 바꾸기 전에 확인할 수 있다.

~~~text
Task가 모호했는가?
필요한 Context를 찾을 수 있었는가?
Tool Output이 너무 컸는가?
Edit Feedback이 부족했는가?
환경이 재현 가능했는가?
필수 검증이 Harness에 있었는가?
~~~

이 질문에 문제가 있다면 더 큰 Model이 근본 해결책이 아닐 수 있다.

Software Factory의 강점은 Model을 교체하는 것 외에도 개선할 수 있는 System Layer가 많다는 데 있다.

---

## 다음 질문

Harness를 준비했다고 해도 Context를 무한정 넣을 수는 없다.

Repository 문서, Architecture, Issue, Log, Trace, Catalog까지 모두 Context에 넣으면 오히려 Agent가 중요한 정보를 찾기 어려워질 수 있다.

다음 장에서는 **얼마나 많은 Context를 줄 것인가가 아니라, 필요한 Context를 어떻게 찾게 할 것인가**를 다룬다.

---

## 참고 자료

- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  https://openai.com/index/harness-engineering/
- SWE-agent, *Agent-Computer Interface*  
  https://swe-agent.com/1.0/background/aci/
- Anthropic, *Writing tools for agents*  
  https://www.anthropic.com/engineering/writing-tools-for-agents
- GitHub, *Better tools made Copilot code review worse*  
  https://github.blog/ai-and-ml/github-copilot/better-tools-made-copilot-code-review-worse-heres-how-we-actually-improved-it/
