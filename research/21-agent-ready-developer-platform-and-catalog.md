# Agent-ready Developer Platform and Software Catalog

기준일: 2026-09-28

AI Software Factory가 조직 전체에서 동작하려면 Agent가 각 repository와 infrastructure를 매번 처음부터 추론하게 만들 수 없다.

기존 Platform Engineering이 만든:

- Golden Path
- Internal Developer Platform
- Software Catalog
- Self-service API
- Policy

가 Agent 시대에 새로운 의미를 갖는다.

---

# 1. 기존 Internal Developer Platform

CNCF / DORA 관점의 Platform Engineering:

- common capabilities
- self-service
- repeatability
- developer experience
- policy
- secure delivery

목적:

개발자가 infrastructure detail을 직접 다루는 cognitive load를 줄이는 것.

출처:

- https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- https://dora.dev/capabilities/platform-engineering/

---

# 2. Agent도 Platform User다

2026년 CNCF 논의에서는 AI Agent를 developer/SRE와 함께 platform의 first-class consumer로 본다.

Human:

- portal
- CLI
- GitOps

Agent:

- API
- MCP
- machine contract

공통 governance:

- identity
- permission
- policy
- observability

출처:

- https://www.cncf.io/blog/2026/07/21/platform-engineering-for-the-agentic-enterprise-managing-applications-resources-and-ai-agents/

---

# 3. Human-friendly와 Agent-friendly Interface는 다르다

Human-friendly:

- wiki
- portal
- dashboard
- tutorial

Agent-friendly:

- structured metadata
- deterministic API
- machine-readable schemas
- concise tool output
- stable identifiers
- query interface

문서를 Agent가 읽을 수 있다고 Agent-ready platform이 되는 것은 아니다.

---

# 4. Golden Path가 Agent Skill이 될 수 있다

기존 Golden Path:

> 회사에서 Spring Boot 서비스를 만드는 표준 방법.

Agent 시대:

```text
Golden Path
→ machine-readable workflow
→ Agent invokes
```

예:

- create-service
- provision-db
- deploy-staging
- setup-observability
- run-security-scan

Agent에게 Kubernetes/Terraform detail을 모두 생성시키기보다 trusted platform workflow를 호출하게 한다.

---

# 5. Software Catalog

Catalog가 관리하는 것:

- service
- owner
- dependency
- API
- lifecycle
- documentation
- environment

Agent에게 필요한 이유:

"이 서비스가 무엇인가?"를 코드만 읽어 추론할 필요 감소.

```text
Task
→ Catalog Lookup
→ Owner / Dependencies / APIs / Runtime
→ Focused Context
```

---

# 6. Backstage의 AI Resource Modeling

Backstage는 AI-related entity를 catalog에 넣는 방향을 제공한다.

예:

- Skill
- Rule
- MCP Server

Rule 예시에는 Agent가 지켜야 하는 security/quality constraint와 rationale을 구조화한다.

출처:

- https://backstage.io/docs/ai/ai-in-the-catalog/

중요:

Factory 자체의 metadata도 catalog 대상이 될 수 있다.

---

# 7. Agent Asset Catalog 후보

Software Factory에서는 다음을 catalog할 수 있다.

### Software

- repo
- service
- API
- database
- owner

### Agent

- role
- model
- capabilities
- allowed tools
- risk class

### Skill

- purpose
- version
- owner
- eval

### Tool / MCP

- capability
- permission
- endpoint
- owner

### Worker Profile

- environment
- runtime
- cache
- network

### Verification Profile

- commands
- acceptance
- evaluator

---

# 8. Catalog != Source of Truth for Everything

예:

- service ownership → catalog
- actual deployment state → runtime platform
- code → Git
- task → task system
- logs → observability

Catalog는 link/index 역할을 한다.

모든 데이터를 복제하면 stale state 문제가 생긴다.

---

# 9. Platform Contract

Agent가 platform capability를 사용할 때 입력/출력이 명확해야 한다.

예:

```text
deploy_staging(
  service,
  revision,
  environment
)

Returns:
- deployment_id
- url
- status
- log_ref
```

이런 contract는 natural-language runbook보다 Agent reliability를 높일 수 있다.

---

# 10. Feedback Quality

DORA는 platform quality에서 task outcome에 대한 clear feedback을 중요하게 본다.

Agent에게도 똑같이 중요하다.

Bad:

```text
Deployment failed.
```

Better:

```text
status: failed
stage: readiness
reason: health_check_timeout
logs: artifact://...
retryable: true
```

Machine-actionable feedback이 Agent loop를 개선한다.

---

# 11. Platform as Governance Layer

Agent가 직접 infra API에 접근하지 않고 Platform API를 거치면:

- allowed topology
- naming
- policy
- audit
- security
- cost limit

을 중앙에서 강제할 수 있다.

```text
Agent
→ Platform Contract
→ Policy
→ Infrastructure
```

---

# 12. Agent-specific Identity

Platform은 Agent를 shared human credential로 처리하면 안 된다.

필요:

- workload identity
- scoped permission
- audit
- resource quota

AWS AgentCore와 Google Agent Platform도 generic agent infrastructure에서 identity를 first-class capability로 제공하는 방향이다.

출처:

- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/
- https://cloud.google.com/blog/products/ai-machine-learning/whats-new-in-gemini-enterprise-agent-platform

---

# 13. Agent Quota

Agent는 Human보다 훨씬 빠르게 API를 반복 호출할 수 있다.

필요:

- request quota
- compute quota
- cost budget
- concurrency
- rate limit

기존 human-oriented platform limit을 그대로 쓰면 부족할 수 있다.

---

# 14. Agent-ready Documentation

문서 후보 구조:

```text
README
→ quick orientation

AGENTS.md / instruction
→ agent rules

Architecture docs
→ boundaries

Catalog
→ ownership/dependency

Skills
→ procedures

Tools/MCP
→ actions
```

각각 책임을 나눈다.

---

# 15. Machine-readable Ownership

Agent가 변경 전 다음 질문에 답할 수 있어야 한다.

- 이 파일/서비스 owner는 누구인가?
- review requirement는?
- high-risk path인가?
- dependent system은?

CODEOWNERS만으로 일부 가능하지만 richer catalog가 필요할 수 있다.

---

# 16. Environment Catalog

Task에 맞는 Worker를 선택하기 위해:

- Java backend
- browser E2E
- Android
- GPU
- internal network

같은 execution profile을 catalog할 수 있다.

Factory scheduler와 platform provisioning 연결점이다.

---

# 17. Agent Legibility + Platform Engineering

OpenAI의 Agent Legibility와 Platform Engineering을 결합하면:

```text
Agent-ready Organization
=
Readable Repository
+ Machine-readable Platform
+ Observable Runtime
```

코드만 잘 정리하는 것으로 충분하지 않다.

---

# 18. Anti-pattern: Agent에게 Infrastructure를 생성하게만 하기

Task:

> staging DB를 만들어라.

Agent가 매번 Terraform을 임의 생성한다면:

- policy drift
- cost variation
- security risk

Golden Path 호출:

> provision_database(profile=staging-small)

이 더 안정적일 수 있다.

---

# 19. Platform Team의 역할 변화

기존:

- developer golden path

확장:

- human + agent golden path

즉 platform interface design에도 Agent UX가 들어간다.

Agent UX 후보:

- schema clarity
- error semantics
- idempotency
- asynchronous operation
- artifact reference

---

# 핵심 후보 메시지

> AI Software Factory를 조직 규모로 확장하려면 Repository뿐 아니라 Internal Developer Platform도 Agent-readable해야 한다.

> Golden Path는 문서화된 권장 방식에서 Agent가 안전하게 호출할 수 있는 machine contract로 진화할 수 있다.

> Software Catalog는 사람용 검색 포털을 넘어 Agent가 ownership, dependency, policy를 찾는 조직 context graph 역할을 할 수 있다.
