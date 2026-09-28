# 10장. Context Engineering과 Agent Legibility

Agent가 실패하면 Context가 부족했다고 생각하기 쉽다.

그래서 더 많은 문서를 넣고, 더 긴 Instruction을 만들고, 로그를 통째로 붙인다.

하지만 Context는 많을수록 좋은 자원이 아니다.

필요한 정보가 늘어나면 중요한 Signal이 묻힐 수 있다. 오래된 문서와 최신 코드가 충돌할 수도 있고, 긴 로그가 Reasoning 공간을 잡아먹을 수도 있다.

그래서 Context Engineering의 질문은 다음에 가깝다.

> 얼마나 많이 넣을 것인가가 아니라, 필요한 정보를 Agent가 얼마나 쉽게 찾을 수 있게 만들 것인가?

이 책에서는 이를 **Agent Legibility**와 연결해 본다.

Repository와 Application이 사람에게만 읽기 쉬운 것이 아니라 Agent도 구조와 상태를 탐색할 수 있어야 한다.

---

## 10.1 Context Window는 Storage가 아니다

Context Window는 Agent가 현재 Task를 이해하고 판단하는 작업 공간이다.

Durable Knowledge Store가 아니다.

그 안에 다음 정보를 모두 넣는다고 해보자.

- 전체 Architecture 문서
- 과거 Incident
- 모든 Coding Convention
- 모든 API 문서
- 수천 줄 Log
- Service Ownership
- Deployment Runbook

처음에는 안전해 보인다.

하지만 실제로는 다음 문제가 생긴다.

- 중요한 정보가 묻힌다.
- 오래된 문서가 섞인다.
- 같은 내용을 반복해서 읽는다.
- 비용이 증가한다.
- Task와 무관한 정보가 판단을 방해한다.

그래서 Context는 세 가지 속성을 갖는 편이 좋다.

~~~text
Relevant
Minimal
Progressive
~~~

Task 시작 시 필요한 최소 정보만 주고, 추가 정보는 탐색을 통해 가져오게 한다.

---

## 10.2 Repository Legibility

Agent가 Repository를 읽을 수 있다고 해서 Repository를 이해할 수 있는 것은 아니다.

다음 Repository를 생각해보자.

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

사람도 어렵지만 Agent에게는 더 어렵다.

Agent-ready Repository라면 최소한 다음 질문에 답하기 쉬워야 한다.

- 어디서 시작해야 하는가
- Build 명령은 무엇인가
- 빠른 Test는 무엇인가
- Architecture boundary는 어디인가
- 어떤 파일은 자동 생성되는가
- 어떤 영역은 변경하면 안 되는가
- 누가 Owner인가

Repository Legibility는 문서량을 늘리는 일이 아니다.

탐색 경로를 만드는 일이다.

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

Agent가 처음부터 모든 문서를 읽지 않아도 되는 구조가 중요하다.

---

## 10.3 AGENTS.md는 지식 저장소가 아니라 Entry Point다

Context File은 유용하다.

하지만 여기에 모든 조직 지식을 넣으면 다시 문제가 생긴다.

예를 들어 AGENTS.md가 2만 줄이 됐다고 하자.

- Build 규칙
- API 문서
- Security 정책
- 모든 서비스 설명
- 과거 Incident
- Coding Style
- Release Procedure

Agent는 매 Task마다 이 전체를 읽어야 할 수 있다.

최근 Context File 관련 연구들도 긴 Instruction이나 Repository-level Context File이 항상 Task success를 높이는 것은 아니며 exploration과 cost를 늘릴 수 있음을 보여준다.

그래서 Context File은 Entry Point에 가깝게 사용하는 편이 낫다.

~~~text
AGENTS.md

- build: ./gradlew build
- fast test: ./gradlew test
- architecture: docs/architecture/README.md
- auth rules: docs/architecture/auth.md
- UI rules: docs/frontend/ui.md
- release: skills/release/
~~~

Agent는 Task에 필요한 문서만 추가로 읽는다.

다음과 같은 구조다.

~~~text
Entry
→ Map
→ Relevant Doc
→ Skill
→ Tool Result
~~~

이것이 Progressive Disclosure다.

---

## 10.4 조직 지식은 Repository 밖에도 있다

Repository만 읽어서는 알 수 없는 정보도 많다.

예:

- 이 Service의 Owner는 누구인가
- 어떤 API가 이 Service에 의존하는가
- Production Environment 이름은 무엇인가
- 어떤 팀이 승인해야 하는가
- 내부 MCP Server는 무엇인가
- 어떤 Worker Profile을 써야 하는가

이런 정보는 Software Catalog나 Developer Platform에서 가져올 수 있다.

~~~text
Task
→ Catalog Lookup
→ Owner / Dependency / API / Environment
→ Focused Context
~~~

Catalog가 모든 상태의 Source of Truth가 될 필요는 없다.

각 데이터는 원래 시스템에 남을 수 있다.

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

Catalog의 역할은 모든 것을 복제하는 것이 아니라 **Agent가 어디서 무엇을 찾아야 하는지 연결하는 것**이다.

---

## 10.5 Application Legibility

Agent에게 Code만 보이게 해서는 충분하지 않은 Task가 많다.

UI 작업을 생각해보자.

Source Diff가 맞아 보여도 실제 화면에서는 다음 문제가 생길 수 있다.

- 버튼이 가려진다.
- Modal이 화면 밖으로 나간다.
- CSS가 깨진다.
- Error Message가 보이지 않는다.

Backend도 마찬가지다.

Code만 읽어서는 실제 Runtime 상태를 알 수 없다.

그래서 Agent가 볼 수 있는 대상은 다음처럼 확장된다.

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

OpenAI의 Harness Engineering 사례가 강조하는 Agent Legibility도 이 방향과 연결된다.

Application이 Agent에게 읽히려면 Runtime Evidence가 접근 가능해야 한다.

예를 들어 API 오류 Task라면 다음 흐름이 가능하다.

~~~text
Task
→ service log search
→ trace lookup
→ relevant code
→ test
→ runtime verify
~~~

이런 구조에서는 Observability도 Agent Context의 일부가 된다.

---

## 10.6 Raw Log를 Context에 그대로 넣지 않는다

Production Log 50MB를 Agent에게 통째로 주면 어떻게 될까.

필요한 Error는 한 줄일 수 있다.

더 좋은 방식은 탐색 Interface를 제공하는 것이다.

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

필요하면 세부 Trace를 조회한다.

~~~text
trace_get("trace-8421")
~~~

이 방식은 Context를 줄이는 것보다 **정보 접근을 단계화하는 것**이 목적이다.

---

## 10.7 예: Auth Bug의 Progressive Context

Task:

~~~text
expired JWT 요청이 500을 반환한다.
401로 수정하라.
~~~

처음 Context:

~~~text
- Task goal
- acceptance
- repo map
- auth module location
~~~

Agent가 Architecture 문서를 찾는다.

~~~text
docs/architecture/auth.md
~~~

그다음 관련 Test를 찾는다.

~~~text
AuthServiceTest
SecurityFilterTest
~~~

실패 로그가 필요하면 Tool로 조회한다.

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

처음부터 Repository 전체와 모든 Log를 Context에 넣지 않는다.

---

## 10.8 Agent가 읽을 수 없는 정보는 운영상 없는 것과 비슷하다

중요한 Architecture Rule이 팀 Slack 대화에만 있다고 하자.

사람들은 알고 있다.

Agent는 모른다.

Agent가 해당 Repository를 수정할 때는 그 규칙이 사실상 존재하지 않는 것과 비슷하다.

같은 문제는 다음에서도 발생한다.

- 사람 머릿속의 Runbook
- 오래된 Wiki
- 구두 합의
- Screenshot으로만 존재하는 Dashboard
- 특정 개발자만 아는 Test Command

Factory를 도입하면 이런 암묵지가 더 잘 드러난다.

Agent가 자주 같은 실수를 한다면 Model 문제일 수도 있지만, 조직 지식이 machine-accessible하지 않은 문제일 수도 있다.

Repository, Catalog, Runtime을 Agent-readable하게 만드는 작업은 결국 사람에게도 도움이 된다.

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

특히 마지막 질문이 중요하다.

Context File은 Agent에게 설명하는 수단이다.

Mandatory Rule을 보장하는 수단은 아니다.

---

## 다음 질문

Context를 잘 준비해도 한 가지 결정은 남는다.

어떤 것은 Agent가 자유롭게 판단하게 하고, 어떤 것은 시스템이 고정해야 하는가.

Retry 횟수도 Agent가 정해야 할까.

Permission도 Agent에게 판단시킬까.

DB Migration 순서도 매번 새로 계획하게 할까.

다음 장에서는 **Controlled Autonomy**, 즉 deterministic control과 Agent judgment의 경계를 다룬다.

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
