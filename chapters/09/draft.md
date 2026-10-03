# 9장. Harness Engineering: Agent가 일할 수 있는 환경 만들기

같은 모델을 쓰는데 팀마다 결과가 크게 다를 수 있다. 한쪽에서는 저장소를 잘 탐색하고 필요한 테스트를 찾아 안정적으로 수정한다. 다른 쪽에서는 파일을 헤매고, 불필요한 명령을 반복하고, 긴 로그를 맥락 정보에 가득 넣은 뒤 방향을 잃는다. 차이는 모델만으로 설명하기 어렵다. 에이전트가 실제로 일하는 방식은 모델 주변 환경에 크게 영향을 받는다. 이 책에서는 모델이 실제 작업을 수행할 수 있도록 지시, 도구, 필요한 정보와 실행 순서를 연결하는 조정 계층을 **하네스(Harness)**라고 부른다.

~~~text
Harness
=
Instructions
+ Context
+ Tool Interface
+ Feedback
+ Verification Hooks
+ Execution Loop / Gates
~~~

하네스의 정확한 경계는 구현마다 다르다. 예를 들어 Anthropic Managed Agents는 세션, 하네스, 격리 환경을 별도 인터페이스로 분리한다. 여기서 하네스는 연산 자원 자체가 아니라 모델 순환과 맥락 정보·도구 선택 규칙을 연결하는 계층을 뜻한다. 하네스 설계는 지시문을 더 잘 쓰는 기술보다 넓다. 에이전트가 저장소와 도구를 어떻게 보고, 어떤 결과를 받고, 어떤 규칙이 강제되는지를 설계하는 일이다.

---

## 9.1 Harness란 무엇인가

모델은 혼자 저장소를 수정하지 않는다. 다음과 같은 계층이 필요하다.

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

하네스는 모델과 실제 소프트웨어 환경 사이의 인터페이스다. 예를 들어 에이전트가 테스트 실패를 분석해야 한다고 하자. 모델이 보는 것은 실제 10MB 로그 전체일 수도 있고, 하네스가 정리한 실패 목록일 수도 있다.

~~~text
Option A
→ raw test log 10MB

Option B
→ failed tests: 3
→ top stack trace
→ artifact URI
→ detail tool
~~~

두 경우 같은 모델을 사용해도 행동은 달라진다. 하네스가 에이전트의 탐색 비용과 오류 가능성을 바꾼다.

### Harness가 Tool 묶음보다 넓어지는 지점

스킬과 도구를 많이 제공한다고 처음부터 최종 전달까지의 전체 과정이 자동으로 만들어지는 것은 아니다. Caylent의 소프트웨어 생산 시스템 설명은 이 경계를 분명하게 보여준다. 이들은 플러그인이 스킬, 후크, 규칙을 통해 에이전트의 지식과 행동 규칙을 제공할 수 있지만, 명세에서 운영에 사용할 수준의 소프트웨어까지 신뢰성 있게 전달하려면 그 위에서 에이전트 순환을 실행하는 하네스가 필요하다고 설명한다. 그 하네스는 단순히 도구를 노출하는 데서 끝나지 않는다.

~~~text
Specification
      ↓
Detailed Plan
      ↓
Execution
      ↓
Review Gates
- functional
- architecture conformance
- security
- scope conformance
      ↓
Feedback / Correction
      ↺
~~~

즉 운영 환경 하네스는 다음 질문까지 책임질 수 있다.

- 다음 실행 단계는 무엇인가
- 어떤 검토를 언제 실행할 것인가
- 실패한 검토 피드백을 어떻게 다음 시도에 전달할 것인가
- 실제 변경이 계획된 범위를 벗어나지 않았는가
- 보안과 설계 구조 제약을 지켰는가

Caylent의 공개 DevBench 구현에서도 구조화된 할 일 목록을 실행 담당자가 구현한 뒤 코드, 테스트, 문서, 변경 목록 평가자와 별도 보안 검토를 통과시키는 순환이 확인된다. 모든 생산 시스템이 같은 검토 구성을 가져야 한다는 뜻은 아니다. 중요한 것은 **에이전트의 수행 능력을 반복 가능한 실행 순서와 강제 가능한 통과 조건으로 묶는 것**이다. 이 경계를 다음처럼 구분할 수 있다.

~~~text
Skill / Tool
= Agent가 사용할 Capability

Harness
= Capability를 사용해 Agent Work Loop를 실행하는 구조

Software Factory
= Harness를 Durable Work, Control, Recovery, Acceptance, Delivery와 연결한 생산 시스템
~~~

따라서 다음 등식도 피한다.

~~~text
Skill
≠ Harness

Harness
≠ Software Factory
~~~

---

## 9.2 Agent-Computer Interface

사람에게 좋은 CLI가 에이전트에게도 항상 좋은 것은 아니다. SWE-agent는 이 문제를 Agent-Computer Interface, ACI라는 관점으로 다뤘다. 핵심은 도구의 존재 여부뿐 아니라 **에이전트가 도구를 어떻게 사용하게 되는가**다. 예를 들어 사람은 다음 명령을 실행하고 긴 출력에서 필요한 부분을 찾을 수 있다.

~~~text
cat huge_file.log
~~~

에이전트에게 같은 방식으로 5만 줄을 반환하면 맥락 정보를 낭비할 수 있다. 대신 다음처럼 만들 수 있다.

~~~text
log_summary()
failed_tests()
failure_detail(test_id)
~~~

파일 보기 도구도 마찬가지다. 사람은 IDE에서 자유롭게 스크롤할 수 있다. 에이전트에게는 다음 정보가 더 중요할 수 있다.

- 줄 번호
- 코드 이름과 기호 경계
- 출력이 잘렸다는 표시
- 다음 범위
- 탐색 결과 우선순위

수정 도구도 단순 파일쓰기보다 다음 피드백을 주면 유리하다.

~~~text
edit applied
lint: failed
line 42: incompatible type
~~~

도구가 에이전트에게 즉시 구조화된 피드백을 주면 잘못된 수정이 다음 단계까지 퍼지는 것을 줄일 수 있다.

---

## 9.3 Instruction, Skill, Tool, MCP의 역할을 나눈다

에이전트 맞춤 설정 기능이 늘어나면 모든 것을 한 파일에 넣고 싶어진다. 하지만 역할을 분리하는 편이 유지보수하기 쉽다. 이 책에서는 다음처럼 구분한다.

### Instruction

지속적으로 알아야 하는 지침이다.

예:

~~~text
- Java 21 사용
- 기존 API response envelope 유지
- 테스트 없는 behavior change 금지
~~~

### Skill

반복해서 사용하는 절차다.

예:

~~~text
DB migration verification
release-note generation
UI screenshot validation
~~~

스킬은 필요할 때 불러오는 것이 좋다. 모든 작업에 항상 넣을 필요는 없다.

### Tool

에이전트가 외부 행동을 수행하는 인터페이스다.

예:

~~~text
run_test()
search_log()
deploy_staging()
get_issue()
~~~

### MCP

외부 시스템의 도구와 데이터를 에이전트에 노출하는 연결 규약 화면으로 볼 수 있다.

예:

- 이슈
- CI
- 문서
- 로그
- 운영 감시
- 내부 API

중요한 점은 MCP가 지속 작업 상태 자체는 아니라는 것이다.

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

지시사항에 적어둘 수 있다. 하지만 반드시 지켜야 한다면 브랜치 보호 기능으로 막는 편이 낫다. 다른 예도 같다.

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

하네스 설계에서 중요한 경계는 다음이다.

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

에이전트가 규칙을 이해하도록 하는 것과 시스템이 규칙을 강제하는 것은 다른 문제다.

---

## 9.5 Tool은 Agent를 위한 API다

사람용 API와 에이전트 도구는 목적이 조금 다르다. 사람은 문서를 읽고 매개변수를 이해할 수 있다. 에이전트는 도구 이름, 스키마, 결과를 보고 행동 전략을 세운다. 그래서 좋은 도구는 보통 다음 특성을 가진다.

- 책임이 좁고 명확하다.
- 이름으로 행동을 추측할 수 있다.
- 결과가 구조화되어 있다.
- 너무 많은 데이터를 한 번에 반환하지 않는다.
- 실패 이유를 시스템이 읽을 수 있다.
- 다음 행동을 선택할 단서가 있다.

예를 들어 이런 도구가 있다고 하자.

~~~text
get_everything()
~~~

이슈, 로그, 테스트, 배포 상태를 한 번에 반환한다. 처음에는 편해 보인다. 하지만 출력이 커지고 에이전트가 어떤 데이터가 최신인지 판단하기 어려워진다. 다음처럼 분리하는 편이 낫다.

~~~text
test_summary()
failed_tests()
test_failure_detail(id)
artifact_get(id)
log_search(query)
~~~

에이전트가 필요할 때 점진적으로 조회한다. 이것이 필요한 정보를 단계적으로 조회하는 방식(Progressive Retrieval)이다.

---

## 9.6 Result Gateway

도구 출력이 큰 시스템에서는 모델 앞에 결과 연결 관문을 둘 수 있다.

~~~text
Tool / Runtime
      ↓
Result Gateway
      ↓
Summary + Index + Artifact Ref
      ↓
Agent
~~~

예를 들어 전체 회귀 검사가 수천 개 테스트를 실행했다고 하자. 에이전트에게 필요한 것은 보통 전체 PASS 로그가 아니다.

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

에이전트는 실패한 세 개만 자세히 볼 수 있다. 이 구조는 토큰 절약만을 위한 것이 아니다. 불필요한 정보에 묻히지 않고 중요한 단서를 쉽게 찾게 하는 것이 목적이다. 너무 짧게 요약해 중요한 정보를 없애도 문제가 된다. 그래서 요약과 상세 정보 조회를 함께 제공해야 한다.

---

## 9.7 Tool을 늘리면 항상 좋아지는가

도구가 많으면 에이전트가 할 수 있는 일이 늘어난다. 하지만 선택 공간도 커진다. 비슷한 도구가 여러 개 있으면 잘못 선택할 수 있다. 권한 범위도 넓어진다. 맥락 정보에 도구 스키마가 많이 들어가면 비용도 증가할 수 있다. 따라서 도구 모음도 작업별로 조절할 수 있다.

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

모든 워커에 모든 도구를 주는 것보다 수행 능력을 좁히는 편이 보안과 신뢰성 모두에 도움이 될 수 있다.

---

## 9.8 Harness도 Regression이 생긴다

도구를 업그레이드하면 성능이 좋아질 것이라고 생각하기 쉽다. 하지만 도구 인터페이스가 바뀌면 기존 지시사항과 에이전트 행동 전략이 더 이상 맞지 않을 수 있다. GitHub는 2026년 Copilot Code Review의 코드 탐색 도구를 공용 CLI 계열로 교체했을 때 초기 오프라인 성능 평가에서 평균 비용이 늘고 유용한 검토 의견이 줄었다고 공개했다.

도구 자체보다 검토자에 맞지 않는 지시사항과 탐색 작업 흐름이 문제였고, 이를 다시 설계한 뒤 운영 환경에서는 기존 품질을 유지하면서 평균 검토 비용을 약 20% 낮췄다고 보고했다. 이는 GitHub의 제품 내부 사례이지 모든 에이전트에 그대로 적용되는 수치는 아니다.

이 사례의 교훈은 단순하다.

> 하네스도 소프트웨어다.

하네스를 바꿀 때도 다음을 해야 한다.

- 버전 관리
- 테스트
- 평가
- 단계적 적용
- 비교
- 이전 상태로 복구

모델 평가만 하고 하네스 변경은 검증하지 않는다면 실제 생산 시스템 성능 변화를 설명하기 어렵다.

---

## 9.9 Prepared Harness

워커 구성이 실행 기반을 준비한다면 미리 준비된 하네스는 작업 유형에 맞는 에이전트 환경을 준비한다. 예를 들어 백엔드 수정 구성은 다음처럼 구성할 수 있다.

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

UI 작업은 다르다.

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

이렇게 하면 에이전트가 작업마다 자신의 도구 모음을 처음부터 조립할 필요가 없다.

---

## 9.10 Context, Capability, Outcome, Guardrail, Evidence

미리 준비된 하네스를 실제 작업에 적용할 때는 에이전트에게 무엇을 줄지 다시 한 번 단순한 질문으로 정리할 수 있다. Cursor의 Grok Bot 문서는 좋은 작업 인계를 설명하면서 작업, 관련 맥락 정보, 필요한 도구 접근, 완료 상태를 함께 주는 방식을 제시한다. 제품별 UI는 달라질 수 있지만, 이 구조는 에이전트 작업 설계의 실용적인 출발점이 된다. 이 책에서는 이를 다음 다섯 요소로 확장한다.

~~~text
Context
- 무엇을 알아야 하는가

Capability
- 어디에서 읽고
- 어디에 행동할 수 있는가

Outcome
- 무엇이 끝난 상태인가

Guardrail
- 무엇을 하면 안 되는가
- 어디에서 멈춰야 하는가

Evidence
- 완료를 무엇으로 증명하는가
~~~

수행 능력은 도구, MCP, API, 브라우저, 셸 같은 실행 수단을 포함한다. 성과는 단순한 자연어 목표보다 구체적이어야 한다.

~~~text
Goal
- 로그인 실패 메시지 개선

Outcome
- 잘못된 자격증명 입력 시 새 메시지 표시
- 기존 성공 로그인 동작 유지

Guardrail
- 인증 정책 변경 금지
- production 직접 변경 금지

Evidence
- targeted test
- browser screenshot
- changed revision
~~~

이 구조는 지시문 서식을 만들기 위한 것이 아니다. 작업이 에이전트에게 전달되기 전에 정보, 권한, 완료 조건, 통제, 증거가 서로 분리되어 있는지 확인하는 작업 규약에 가깝다. 특히 성과와 근거를 분리하는 것이 중요하다.

~~~text
Outcome
= 무엇이 참이어야 하는가

Evidence
= 그것이 참임을 무엇으로 확인했는가
~~~

에이전트가 "완료했다"고 말하는 것은 성과도 근거도 아니다. 이 구분은 뒤의 검증과 증거 계약으로 이어진다.

## Model 문제인가 Harness 문제인가

에이전트가 실패했을 때 바로 모델을 바꾸기 전에 확인할 수 있다.

~~~text
Task가 모호했는가?
필요한 Context를 찾을 수 있었는가?
Tool Output이 너무 컸는가?
Edit Feedback이 부족했는가?
환경이 재현 가능했는가?
필수 검증이 Harness에 있었는가?
~~~

이 질문에 문제가 있다면 더 큰 모델이 근본 해결책이 아닐 수 있다. 소프트웨어 생산 시스템의 강점은 모델을 교체하는 것 외에도 개선할 수 있는 시스템 계층이 많다는 데 있다.

---

## 다음 질문

하네스를 준비했다고 해도 맥락 정보를 무한정 넣을 수는 없다. 저장소 문서, 설계 구조, 이슈, 로그, 추적 기록, 목록까지 모두 맥락 정보에 넣으면 오히려 에이전트가 중요한 정보를 찾기 어려워질 수 있다. 다음 장에서는 **얼마나 많은 맥락 정보를 줄 것인가가 아니라, 필요한 맥락 정보를 어떻게 찾게 할 것인가**를 다룬다.

---

## 참고 자료

- Cursor, *Grok Bot*  
  https://cursor.com/docs/grok-bot
- Cursor, *Get started with Grok Bot*  
  https://cursor.com/docs/grok-bot/get-started
- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  https://openai.com/index/harness-engineering/
- SWE-agent, *Agent-Computer Interface*  
  https://swe-agent.com/1.0/background/aci/
- Anthropic, *Writing tools for agents*  
  https://www.anthropic.com/engineering/writing-tools-for-agents
- GitHub, *Better tools made Copilot code review worse*  
  https://github.blog/ai-and-ml/github-copilot/better-tools-made-copilot-code-review-worse-heres-how-we-actually-improved-it/
- Caylent, *What is a Software Factory*  
  https://www.youtube.com/watch?v=0Q8R_FZbnLk
- Caylent Solutions, *DevBench Architecture*  
  https://github.com/caylent-solutions/devbench/blob/main/docs/architecture.md
- Caylent Solutions, *DevBench Execution Modes*  
  https://github.com/caylent-solutions/devbench/blob/main/docs/execution-modes.md
