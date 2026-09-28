# Harness, Context, and Agent Legibility

기준일: 2026-09-28

AI Software Factory에서 모델은 중요한 구성요소지만 모델만으로 생산 시스템이 되지 않는다.

여러 1차 자료에서 반복해서 등장하는 개념은 **agent가 작업을 잘할 수 있도록 repository, tools, environment, context를 설계하는 harness engineering**이다.

## 1. Harness는 무엇인가

임시 정의:

> Harness는 모델이 실제 작업을 수행할 수 있도록 context, tools, execution environment, feedback, verification을 연결하는 실행 구조다.

Harness에 포함될 수 있는 것:

- system / project instruction
- repository map
- skills
- MCP
- shell
- file editor
- search
- browser
- sandbox
- test runner
- tool output filtering
- context compaction
- subagent delegation
- policy/approval hooks
- progress state

## 2. OpenAI - Repository를 System of Record로 만든다

OpenAI Harness Engineering 사례에서 중요한 원칙:

- agent가 접근할 수 없는 정보는 사실상 존재하지 않는 것과 같다.
- Slack/사람의 머릿속/외부 문서에만 규칙을 두지 않는다.
- repository 안에서 discoverable한 문서와 구조로 만든다.
- 거대한 한 파일보다 탐색 가능한 계층형 지식을 만든다.
- code뿐 아니라 test, CI, observability, tooling까지 agent-readable하게 만든다.

핵심 표현:

> agent legibility

사람에게 readable한 repository만으로 충분하지 않고 agent가 다음을 찾아낼 수 있어야 한다.

- 어디를 수정하는가
- 어떤 명령을 실행하는가
- 무엇이 완료 기준인가
- 실패 원인을 어디서 찾는가
- architecture rule은 무엇인가

출처:

- https://openai.com/index/harness-engineering/

## 3. ACI - Agent Computer Interface

SWE-agent는 Agent-Computer Interface(ACI)라는 관점을 제시했다.

실험에서 단순 shell/file access보다 agent에 맞는 interaction interface가 성능에 영향을 준다.

대표 예:

- edit 후 linter
- 너무 긴 파일 출력을 피하는 file viewer
- concise search result
- empty command output도 명시적으로 성공 상태 전달

중요한 메시지:

> 인간 개발자에게 좋은 CLI가 곧 Agent에게 좋은 CLI라는 보장은 없다.

Tool output의 크기, structure, feedback timing이 agent 성능에 영향을 준다.

출처:

- https://swe-agent.com/1.0/background/aci/
- https://swe-agent.com/latest/background/

## 4. Tool은 Agent를 위한 API다

Anthropic의 tool engineering 자료는 일반 API와 Agent Tool의 차이를 강조한다.

좋은 tool의 특징:

- 명확한 이름
- 좁은 responsibility
- 의미 있는 context 반환
- token-efficient output
- namespace
- agent가 성공 전략을 선택할 수 있는 충분한 flexibility
- eval을 통한 실제 agent performance 측정

출처:

- https://www.anthropic.com/engineering/writing-tools-for-agents

Factory에 적용:

```text
Bad
get_everything()

Better
test_summary()
failed_tests()
test_failure_detail(id)
artifact_get(id)
log_search(query)
```

대규모 raw output을 바로 model context에 넣기보다 progressive retrieval이 유리할 수 있다.

## 5. MCP는 Context Surface이지 Memory 자체가 아니다

MCP가 제공할 수 있는 것:

- issue
- docs
- logs
- monitoring
- database
- deployment
- Slack
- CI
- artifact
- internal API

WorkOS Horizon에서는 custom MCP server를 context engine으로 사용한다.

중요한 distinction:

```text
MCP
= external capability/context access protocol

Durable Task State
= orchestration state

Agent Memory
= 별도 문제
```

세 가지를 같은 것으로 취급하지 않는다.

출처:

- https://workos.com/blog/project-horizon

## 6. Skills / Instructions / Hooks / MCP의 역할 분리

GitHub Copilot 문서에서 customisation surface가 잘 구분된다.

### Instruction

지속적인 project rule.

### Skill

필요할 때 로드하는 reusable instruction/script/resource package.

### Custom Agent

특정 역할의 prompt + scoped tools.

### Hook

agent lifecycle 특정 시점에 deterministic shell logic 실행.

용도:

- allow/deny
- security scanning
- audit
- validation
- event capture

### MCP

외부 system/tool/data 연결.

이 구분은 Software Factory에서도 유용하다.

```text
Rule / Knowledge
→ Instructions

Reusable Procedure
→ Skill

Specialized Reasoner
→ Agent

Must Always Enforce
→ Hook / Policy

External Capability
→ MCP / Tool
```

출처:

- https://docs.github.com/en/copilot/reference/customization-cheat-sheet
- https://docs.github.com/en/copilot/concepts/agents/hooks

## 7. Deterministic Rule을 Agent Prompt에 넣지 않는다

반드시 지켜야 하는 규칙이 deterministic하게 검사 가능하다면 prompt보다 enforcement layer가 적합하다.

예:

- secret commit 차단
- protected branch push 차단
- forbidden path 변경 차단
- test pass requirement
- generated file consistency
- license header
- migration safety check

GitHub Hooks와 Factory Droid Shield는 이런 방향의 사례다.

출처:

- https://docs.github.com/en/copilot/concepts/agents/hooks
- https://factory.ai/news/droid-shield-2-0

## 8. Environment as Agent Context

Agent의 context는 text만이 아니다.

```text
Context
= Text
+ Repository
+ Filesystem
+ Runtime
+ Installed Tools
+ Running Services
+ Browser State
+ External Systems
```

Cursor Cloud Agents는 isolated VM 안에:

- repo
- dependencies
- secrets
- startup command
- browser
- desktop
- network

를 제공한다.

환경이 준비되지 않으면 agent가 setup에 token/time을 소비하거나 잘못된 환경에서 검증할 수 있다.

출처:

- https://cursor.com/docs/cloud-agent
- https://cursor.com/docs/cloud-agent/capabilities

## 9. Prepared Environment

Cursor의 `.cursor/environment.json`은 대표적인 환경 코드화 사례다.

포함 가능:

- install command
- startup command
- terminals
- snapshot

장점:

- reproducibility
- cold start 감소
- agent가 환경 설치를 추론할 필요 감소

Software Factory에서는 이런 개념을 제품 비종속적으로 추상화할 수 있다.

```text
Worker Profile
- runtime
- build tools
- browsers
- caches
- environment variables
- network policy
- startup services
```

## 10. Application Legibility

OpenAI Harness Engineering과 Cursor/Factory의 browser evidence 사례는 중요한 확장을 보여준다.

기존:

```text
Agent sees source code
```

확장:

```text
Agent sees:
- DOM
- browser
- screenshot
- logs
- metrics
- traces
- runtime behavior
```

즉, application도 agent가 읽을 수 있게 만들어야 한다.

UI 작업에서 source diff만으로 correctness를 판단하기 어렵다.

## 11. Context Window를 Storage로 쓰지 않는다

장시간 작업에서는 context window가 durable state가 될 수 없다.

대신:

- task state
- commit history
- progress artifact
- feature checklist
- test status
- decision log

를 외부화한다.

Anthropic long-running harness는 session 간 handoff artifact의 필요성을 실험적으로 보여준다.

출처:

- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

## 12. Model Routing도 Harness 문제

Factory.ai는 2026년 model routing을 Software Factory layer에 둔다.

핵심 아이디어:

- Task 종류에 따라 모델 선택
- 비용/성능 trade-off
- cache/context 특성을 함께 고려
- 모델을 workflow에 hard-code하지 않음

중요한 연구 질문:

> Routing이 agent 내부 판단이어야 하는가, orchestration/harness policy여야 하는가?

출처:

- https://factory.ai/product/software-factory
- https://factory.ai/news

## 13. Agent Readiness

AI Software Factory를 만들기 전에 repository가 agent-ready인지 평가할 필요가 있다.

후보 항목:

### Build

- clean checkout에서 build 가능한가
- single command가 있는가
- dependency가 reproducible한가

### Test

- 빠른 targeted test가 있는가
- 전체 test와 부분 test가 분리되는가
- flaky test가 추적되는가

### Documentation

- architecture
- module ownership
- convention
- command
- constraint

### Runtime

- local/cloud에서 실행 가능한가
- browser validation 가능한가
- test fixture가 있는가

### Observability

- log search
- error lookup
- metric lookup
- trace lookup

### Safety

- destructive operation boundary
- secrets
- network
- protected resources

## 14. 책의 핵심 후보 메시지

> AI Software Factory의 생산성은 모델에게 더 많은 context를 넣는 데서 나오지 않는다. 필요한 정보와 행동 경로를 agent가 스스로 찾을 수 있게 만드는 데서 나온다.

> Agent에게 설명해야 하는 규칙과 시스템이 강제로 보장해야 하는 규칙을 분리해야 한다.

> Repository, runtime, tools, observability가 모두 Agent Interface의 일부가 된다.
