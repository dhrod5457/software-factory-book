# 10장. Context Engineering과 Agent Legibility

에이전트가 실패하면 맥락 정보가 부족했다고 생각하기 쉽다. 그래서 더 많은 문서를 넣고, 더 긴 지시사항을 만들고, 로그를 통째로 붙인다. 하지만 맥락 정보는 많을수록 좋은 자원이 아니다. 정보가 늘어나면 중요한 단서가 묻힐 수 있다. 오래된 문서가 최신 코드와 맞지 않을 수도 있고, 긴 로그가 추론에 사용할 공간을 차지할 수도 있다. 그래서 Context Engineering의 질문은 다음에 가깝다.

> 얼마나 많이 넣을 것인가가 아니라, 필요한 정보를 에이전트가 얼마나 쉽게 찾을 수 있게 만들 것인가?

이 책에서는 이를 **에이전트가 구조와 상태를 읽고 이해하기 쉬운 정도(Agent Legibility)**와 연결해 본다. 저장소와 애플리케이션이 사람에게만 읽기 쉬운 것이 아니라 에이전트도 구조와 상태를 탐색할 수 있어야 한다.

---

## 10.1 Context Window는 Storage가 아니다

컨텍스트 창은 에이전트가 현재 작업을 이해하고 판단하는 작업 공간이다. 지속적인 지식 저장소가 아니다. 그 안에 다음 정보를 모두 넣는다고 해보자.

- 전체 설계 구조 문서
- 과거 장애
- 모든 코딩 규칙
- 모든 API 문서
- 수천 줄 로그
- 서비스 담당 관계
- 배포 운영 절차서

처음에는 안전해 보인다. 하지만 실제로는 다음 문제가 생긴다.

- 중요한 정보가 묻힌다.
- 오래된 문서가 섞인다.
- 같은 내용을 반복해서 읽는다.
- 비용이 증가한다.
- 작업과 무관한 정보가 판단을 방해한다.

그래서 맥락 정보는 세 가지 속성을 갖는 편이 좋다.

~~~text
Relevant
Minimal
Progressive
~~~

작업 시작 시 필요한 최소 정보만 주고, 추가 정보는 탐색을 통해 가져오게 한다.

---

## 10.2 Repository Legibility

에이전트가 저장소를 읽을 수 있다고 해서 저장소를 이해할 수 있는 것은 아니다. 다음 저장소를 생각해보자.

~~~text
README
- 실행 방법 없음

scripts/
- 오래된 shell script 여러 개

docs/
- architecture 문서가 실제 코드와 다름

test/
- 어떤 test가 빠른지 알 수 없음

service/
- owner 정보 없음
~~~

사람도 어렵지만 에이전트에게는 더 어렵다. 에이전트가 작업하기 쉽게 준비된 저장소라면 최소한 다음 질문에 답하기 쉬워야 한다.

- 어디서 시작해야 하는가
- 빌드 명령은 무엇인가
- 빠른 테스트는 무엇인가
- 설계 구조 경계는 어디인가
- 어떤 파일은 자동 생성되는가
- 어떤 영역은 변경하면 안 되는가
- 누가 담당자인가

저장소를 읽고 이해하기 쉽게 만드는 일은 문서량을 늘리는 일이 아니다. 탐색 경로를 만드는 일이다.

예:

~~~text
README
→ quick orientation

AGENTS.md
→ agent rules / entry points

docs/architecture/
→ module boundaries

scripts/
→ canonical commands

CODEOWNERS / catalog
→ ownership
~~~

에이전트가 처음부터 모든 문서를 읽지 않아도 되는 구조가 중요하다.

---

## 10.3 AGENTS.md는 지식 저장소가 아니라 Entry Point다

맥락 정보 파일은 유용하다. 하지만 여기에 모든 조직 지식을 넣으면 다시 문제가 생긴다. 예를 들어 AGENTS.md가 2만 줄이 됐다고 하자.

- 빌드 규칙
- API 문서
- 보안 정책
- 모든 서비스 설명
- 과거 장애
- 코딩 방식
- 릴리스 절차

에이전트는 매 작업마다 이 전체를 읽어야 할 수 있다. OpenAI의 2026년 하네스 설계 사례도 “거대한 하나의 AGENTS.md” 방식을 실패한 접근으로 설명한다. 맥락 정보를 과도하게 차지하고, 모든 규칙이 중요해 보여 우선순위가 흐려지며, 문서가 빠르게 낡아졌다는 것이다. 해당 팀은 대신 약 100줄 규모의 AGENTS.md를 목차처럼 사용하고 상세 지식은 구조화된 문서로 분리했다. 이는 한 조직의 사례이지만 맥락 정보 파일을 지식 저장소보다 출발점으로 보는 데 유용한 근거다. 그래서 맥락 정보 파일은 출발점에 가깝게 사용하는 편이 낫다.

~~~text
AGENTS.md

- build: ./gradlew build
- fast test: ./gradlew test
- architecture: docs/architecture/README.md
- auth rules: docs/architecture/auth.md
- UI rules: docs/frontend/ui.md
- release: skills/release/
~~~

에이전트는 작업에 필요한 문서만 추가로 읽는다. 다음과 같은 구조다.

~~~text
Entry
→ Map
→ Relevant Doc
→ Skill
→ Tool Result
~~~

이것이 필요한 정보를 단계적으로 보여주는 방식(Progressive Disclosure)다.

---

## 10.4 조직 지식은 Repository 밖에도 있다

저장소만 읽어서는 알 수 없는 정보도 많다.

예:

- 이 서비스의 담당자는 누구인가
- 어떤 API가 이 서비스에 의존하는가
- 운영 환경 이름은 무엇인가
- 어떤 팀이 승인해야 하는가
- 내부 MCP 서버는 무엇인가
- 어떤 워커 구성을 써야 하는가

이런 정보는 소프트웨어 목록이나 개발자 플랫폼에서 가져올 수 있다.

~~~text
Task
→ Catalog Lookup
→ Owner / Dependency / API / Environment
→ Focused Context
~~~

목록이 모든 상태의 기준 원본이 될 필요는 없다. 각 데이터는 원래 시스템에 남을 수 있다.

~~~text
Code
→ Git

Deployment State
→ Runtime Platform

Logs
→ Observability

Task
→ Task Store

Ownership / Dependency Index
→ Catalog
~~~

목록의 역할은 모든 것을 복제하는 것이 아니라 **에이전트가 어디서 무엇을 찾아야 하는지 연결하는 것**이다.

---

### MCP Gateway를 Context Engine으로 만든다

외부 시스템을 MCP로 연결했다고 Context Engineering이 끝나는 것은 아니다. WorkOS는 내부 MCP 연결 관문을 `Context Engine`처럼 사용한다고 설명한다. Snowflake와 내부 시스템을 연결하는 것뿐 아니라, 어떤 테이블에 어떤 의미의 데이터가 있고 어떤 질문에서 어떤 소스를 찾아야 하는지까지 도구 설명과 맥락 정보로 제공한다. 이 차이는 다음처럼 볼 수 있다.

~~~text
Raw Tool Gateway
→ API를 Agent에게 노출

Semantic Tool Gateway
→ Tool + Schema + Usage Guidance

Organizational Context Gateway
→ Tool
 + Data Semantics
 + Organization Convention
 + Resource Discovery
~~~

에이전트에게 `query()`라는 도구 하나를 주는 것과, 조직의 데이터 구조를 이해하고 올바른 소스를 선택할 수 있게 만드는 것은 다른 문제다. 또한 이런 맥락 정보 계층이 특정 코딩 에이전트의 세션 안에만 있지 않으면 여러 실행 기반이 같은 조직 지식을 재사용할 수 있다.

~~~text
Durable Task / Context / Policy
          ↓
     MCP Context Layer
      ↙    ↓     ↘
 Agent A Agent B Agent C
~~~

따라서 에이전트 공급업체를 교체해도 작업 상태와 조직 맥락 정보가 유지되는 구조가 장기적으로 더 유연하다.

## 10.5 Application Legibility

에이전트에게 코드만 보이게 해서는 충분하지 않은 작업이 많다. UI 작업을 생각해보자. 코드 변경 내역이 맞아 보여도 실제 화면에서는 다음 문제가 생길 수 있다.

- 버튼이 가려진다.
- 모달 창이 화면 밖으로 나간다.
- CSS가 깨진다.
- 오류 메시지가 보이지 않는다.

백엔드도 마찬가지다. 코드만 읽어서는 실제 실행 중 상태를 알 수 없다. 그래서 에이전트가 볼 수 있는 대상은 다음처럼 확장된다.

~~~text
Source Code
+ DOM
+ Browser
+ Screenshot
+ Logs
+ Metrics
+ Traces
+ Deployment State
~~~

OpenAI의 하네스 설계 사례가 강조하는 에이전트가 읽고 이해하기 쉬운 정도도 이 방향과 연결된다. 애플리케이션이 에이전트에게 읽히려면 실행 중 확인한 근거가 접근 가능해야 한다. 예를 들어 API 오류 작업이라면 다음 흐름이 가능하다.

~~~text
Task
→ service log search
→ trace lookup
→ relevant code
→ test
→ runtime verify
~~~

이런 구조에서는 관측 가능성도 에이전트 맥락 정보의 일부가 된다.

---

## 10.6 Raw Log를 Context에 그대로 넣지 않는다

운영 환경 로그 50MB를 에이전트에게 통째로 주면 어떻게 될까. 필요한 오류는 한 줄일 수 있다. 더 좋은 방식은 탐색 인터페이스를 제공하는 것이다.

~~~text
log_search(
  service="auth",
  error="TokenExpiredException",
  since="30m"
)
~~~

결과:

~~~text
matches: 12
top_trace: trace-8421
sample:
- 14:02:11 TokenExpiredException
- 14:02:12 mapped to 500
~~~

필요하면 세부 추적 기록을 조회한다.

~~~text
trace_get("trace-8421")
~~~

이 방식은 맥락 정보를 줄이는 것보다 **정보 접근을 단계화하는 것**이 목적이다.

---

## 10.7 예: Auth Bug의 Progressive Context

작업:

~~~text
expired JWT 요청이 500을 반환한다.
401로 수정하라.
~~~

처음 맥락 정보:

~~~text
- Task goal
- acceptance
- repo map
- auth module location
~~~

에이전트가 설계 구조 문서를 찾는다.

~~~text
docs/architecture/auth.md
~~~

그다음 관련 테스트를 찾는다.

~~~text
AuthServiceTest
SecurityFilterTest
~~~

실패 로그가 필요하면 도구로 조회한다.

~~~text
log_search(TokenExpiredException)
~~~

즉 다음 순서다.

~~~text
Task
→ Repository Map
→ Auth Architecture
→ Target Test
→ Runtime Log
~~~

처음부터 저장소 전체와 모든 로그를 맥락 정보에 넣지 않는다.

---

## 10.8 Agent가 읽을 수 없는 정보는 운영상 없는 것과 비슷하다

중요한 설계 구조 규칙이 팀 Slack 대화에만 있다고 하자. 사람들은 알고 있다. 에이전트는 모른다. 에이전트가 해당 저장소를 수정할 때는 그 규칙을 안정적으로 사용할 수 없다. OpenAI의 사례에서는 이를 “에이전트가 실행 중 접근할 수 없는 정보는 사실상 존재하지 않는 것과 같다”는 식으로 설명했다. 같은 문제는 다음에서도 발생한다.

- 사람 머릿속의 운영 절차서
- 오래된 위키
- 구두 합의
- 화면 캡처로만 존재하는 대시보드
- 특정 개발자만 아는 테스트 명령

생산 시스템을 도입하면 이런 암묵지가 더 잘 드러난다. 에이전트가 자주 같은 실수를 한다면 모델 문제일 수도 있지만, 조직 지식이 시스템에서 접근할 수 없는 문제일 수도 있다. 저장소, 목록, 실행 기반을 에이전트가 읽을 수 있게 만드는 작업은 결국 사람에게도 도움이 된다.

---

## Context를 더 넣기 전에 묻는 질문

~~~text
1. 이 정보는 현재 Task와 직접 관련 있는가?
2. 최신 정보인가?
3. Agent가 필요할 때 찾을 수 있는가?
4. 원문 전체가 필요한가, index/summary로 충분한가?
5. 반드시 지켜야 하는 규칙인가?
6. 그렇다면 Context가 아니라 Policy로 강제해야 하지 않는가?
~~~

특히 마지막 질문이 중요하다. 맥락 정보 파일은 에이전트에게 설명하는 수단이다. 반드시 지켜야 하는 규칙을 보장하는 수단은 아니다.

---

## 다음 질문

맥락 정보를 잘 준비해도 한 가지 결정은 남는다. 어떤 것은 에이전트가 자유롭게 판단하게 하고, 어떤 것은 시스템이 고정해야 하는가. 재시도 횟수도 에이전트가 정해야 할까. 권한도 에이전트에게 판단시킬까. DB 마이그레이션 순서도 매번 새로 계획하게 할까. 다음 장에서는 **통제된 자율성**, 즉 정해진 규칙에 따른 제어와 에이전트 판단의 경계를 다룬다.

---

## 참고 자료

- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  https://openai.com/index/harness-engineering/
- SWE-agent, *Agent-Computer Interface*  
  https://swe-agent.com/1.0/background/aci/
- Backstage, *AI in the Software Catalog*  
  https://backstage.io/docs/ai/ai-in-the-catalog/
- SWE-Explore  
  https://arxiv.org/abs/2606.07297
