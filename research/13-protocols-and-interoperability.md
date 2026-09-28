# Protocols and Interoperability in AI Software Factories

기준일: 2026-09-28

AI Software Factory가 여러 모델, Agent, IDE, Tool, 사내 시스템을 조합하게 되면서 제품별 독점 API만으로 모든 연결을 유지하기 어려워지고 있다.

현재 중요한 프로토콜 계층은 최소 세 가지로 나눠 볼 수 있다.

```text
Agent ↔ Tools / Data
        MCP

Agent ↔ Agent
        A2A

Agent ↔ IDE / Client
        ACP
```

이 구분은 완전히 고정된 업계 표준 taxonomy는 아니지만, 2026년 공개 프로토콜의 역할을 설명하는 데 유용하다.

## 1. MCP - Agent와 Tool/Data

Model Context Protocol은 AI application이 외부 시스템의 data와 tools에 연결되는 open standard다.

MCP server가 노출할 수 있는 기본 primitive:

- Tools
- Resources
- Prompts

Factory 관점에서 MCP는 다음을 공통 interface로 만들 수 있다.

- GitHub / GitLab
- CI
- issue tracker
- observability
- DB
- internal API
- artifact store
- deployment
- documentation

출처:

- https://modelcontextprotocol.io/
- https://modelcontextprotocol.io/specification/

## 2. MCP 2026-07-28

2026-07-28 specification은 production-scale agent workflow를 더 직접적으로 겨냥한다.

주요 변화:

- stateless protocol core
- multi round-trip requests
- header-based routing
- cacheable list results
- authorization hardening
- extensions framework
- long-running work를 위한 Tasks extension

Factory 관점에서 중요한 것은 MCP가 단순 local tool adapter에서 장기 실행/enterprise integration까지 확장되고 있다는 점이다.

출처:

- https://blog.modelcontextprotocol.io/posts/2026-07-28/

## 3. MCP와 Durable Task는 같은 것이 아니다

MCP에 Tasks extension이 들어와도 Software Factory 전체의 Task State와 동일시하면 안 된다.

Factory Task에는 보통:

- business/work intent
- dependency
- ownership
- attempts
- workspace
- verification
- approval
- delivery state

가 필요하다.

MCP Task는 protocol-level long-running operation을 표현하는 수단으로 볼 수 있다.

따라서:

```text
Factory Task State
> MCP transport/protocol task
```

가 될 수 있다.

## 4. A2A - Agent와 Agent

Agent2Agent(A2A) Protocol은 서로 다른 framework/vendor로 만들어진 독립 agent system이 협업할 수 있도록 하는 open standard다.

공식 specification에서 목표로 제시하는 기능:

- capability discovery
- interaction modality negotiation
- collaborative task management
- information exchange
- 상대 agent의 internal memory/tool을 직접 공유하지 않고 협업

출처:

- https://a2a-protocol.org/

## 5. A2A의 핵심: Agent는 Tool과 다르다

A2A는 Agent를 단순 RPC function으로 보지 않는다.

Agent는:

- own policy
- own context
- own execution
- own long-running task state

를 가질 수 있다.

따라서 Factory 내부에서 다음 구조가 가능하다.

```text
Factory Orchestrator
      ↓
Planning Agent
      ↓ A2A
Implementation Agent
      ↓ A2A
Verification Agent
```

다만 내부 동일 runtime 안의 subagent까지 반드시 A2A로 연결해야 한다는 뜻은 아니다.

## 6. MCP와 A2A 역할 구분

A2A 공식 문서도 두 protocol을 상호보완적으로 설명한다.

### MCP

Agent가 tool/resource를 사용.

```text
Agent → Tool / Database / API
```

### A2A

독립 agent가 다른 agent와 협업.

```text
Agent → Agent
```

이 구분은 Software Factory architecture를 설명할 때 유용하다.

출처:

- https://a2a-protocol.org/latest/topics/a2a-and-mcp/

## 7. A2A 1.0

2026년 현재 A2A specification 1.0 계열이 공개되어 있다.

A2A는 Google에서 시작되어 Linux Foundation으로 기증되었고, 2026년 8월 Agentic AI Foundation의 Growth Stage project로 편입됐다고 공식 프로젝트가 발표했다.

Factory 책에서 중요한 것은 governance 자체보다 **vendor-independent agent delegation layer가 실제 표준화 대상으로 등장했다는 사실**이다.

출처:

- https://a2a-protocol.org/v1.0.0/
- https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/

## 8. ACP - Agent와 Development Client

Agent Client Protocol(ACP)은 agent와 editor/client 사이의 interoperability를 목표로 한다.

Zed가 시작했으며 다음과 같은 agent/client 분리를 지향한다.

```text
Coding Agent
      ↕ ACP
Editor / IDE
```

의미:

- agent 구현자가 각 IDE별 UI integration을 새로 만들지 않아도 됨
- editor는 agent-agnostic UI 제공 가능
- agent 교체와 client 교체의 coupling 감소

출처:

- https://zed.dev/acp

## 9. ACP 생태계

2026년 ACP Registry에는 여러 agent가 등록되어 있다.

공식 Zed 자료에서 예로 드는 agent:

- Claude Agent
- Codex CLI
- GitHub Copilot CLI
- Gemini CLI
- OpenCode

그리고 client 쪽도 Zed 외에 VS Code/JetBrains/Neovim 등으로 확장되는 방향을 보인다.

제품 목록은 빠르게 변하므로 출판 시점 재검증이 필요하다.

출처:

- https://zed.dev/blog/acp-registry
- https://zed.dev/acp

## 10. Protocol Layer와 Factory Layer

중요한 구분:

```text
Protocol
= 어떻게 연결하고 통신하는가

Factory
= 어떤 Task를 언제 누구에게 주고
  어떤 권한/검증/복구 정책으로 완료시키는가
```

MCP/A2A/ACP가 있어도 다음은 자동으로 해결되지 않는다.

- priority
- dependency
- retry
- approval
- cost budget
- risk
- completion criteria
- merge authority
- incident handling

즉 protocol은 Factory infrastructure의 일부이지 Factory 자체는 아니다.

## 11. Interoperability가 중요한 이유

### Vendor Independence

특정 coding agent와 tool integration의 결합도를 줄인다.

### Replaceability

Agent/model/tool을 교체 가능하게 만든다.

### Specialization

서로 다른 강점을 가진 agent를 조합할 수 있다.

### Organizational Boundary

다른 team/company의 agent를 internal state 공개 없이 연결할 가능성을 만든다.

### Long-term Architecture

모델과 제품의 변화 속도가 빠르므로 stable integration boundary가 중요하다.

## 12. Protocol이 늘어날수록 생기는 새로운 문제

표준화가 모든 complexity를 없애지는 않는다.

추가 문제:

- identity
- authorization
- trust
- capability discovery
- version negotiation
- audit
- task ownership
- cross-agent prompt injection
- delegation loop
- cost attribution
- timeout
- partial failure

Factory control plane이 여전히 필요하다.

## 13. Security Boundary

외부 agent/tool과 연결될수록 trust boundary가 명확해야 한다.

후보:

```text
Untrusted Input
      ↓
Agent
      ↓
Policy
      ↓
MCP Tool / A2A Agent
      ↓
Scoped Capability
```

프로토콜 compatibility가 상대 system의 신뢰성을 의미하지 않는다.

## 14. Factory Reference Stack 후보

```text
Human / Product Systems
        ↓
Requirement / Task System
        ↓
Factory Control Plane
        ↓
Agent Runtime / Harness
   ├── MCP → Tools / Data
   ├── A2A → External/Specialized Agents
   └── ACP → Developer Client / IDE
        ↓
Sandbox / Compute
        ↓
Verification / Evidence
```

ACP는 developer-facing workflow에서만 필요할 수 있으며 headless Factory에는 필수가 아니다.

## 15. 핵심 후보 메시지

> AI Software Factory는 하나의 거대한 Agent보다 교체 가능한 Agent, Tool, Runtime을 stable boundary로 조립하는 방향으로 갈 가능성이 높다.

> MCP, A2A, ACP는 각각 연결 문제를 줄이지만 Task ownership과 orchestration 문제를 대신 해결하지 않는다.

> Protocol interoperability가 높아질수록 Factory의 경쟁력은 특정 모델 integration보다 specification, policy, verification, organizational knowledge에 더 많이 남을 수 있다.
