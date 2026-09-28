# AI Software Factory와 인접 개념의 경계

기준일: 2026-09-28

이 문서는 AI Software Factory를 다음 인접 개념과 구분하기 위한 연구 노트다.

- CI/CD
- DevOps / DevSecOps
- Platform Engineering
- Internal Developer Platform
- Agent Platform
- Agent Runtime

핵심 목표는 새로운 용어를 만들기 위한 것이 아니라, 책에서 무엇을 Software Factory의 핵심 범위로 볼지 정하는 것이다.

---

# 1. CI/CD와 Software Factory

CI/CD의 핵심 역할:

```text
Source Change
→ Build
→ Test
→ Package
→ Release
→ Deploy
```

CI/CD는 이미 소프트웨어 생산의 자동화 핵심이다.

하지만 일반 CI/CD는 보통 다음을 스스로 결정하지 않는다.

- 어떤 문제를 해결할 것인가
- 어떤 Task를 만들 것인가
- 어떤 변경 전략을 사용할 것인가
- 실패한 코드를 어떻게 수정할 것인가
- 요구사항 ambiguity를 어떻게 해소할 것인가

즉 CI/CD는 **정의된 변경을 검증·전달하는 자동화 파이프라인**에 가깝다.

AI Software Factory는 그 앞단과 중간에 Agent execution을 추가한다.

```text
Intent
→ Requirement
→ Task
→ Agent Work
→ Code Change
→ CI/CD
→ Deploy
→ Feedback
```

따라서:

> CI/CD는 Software Factory의 중요한 실행·검증·전달 subsystem이지만 Factory 전체와 동일하지 않다.

---

# 2. NIST DevSecOps Reference Model

NIST NCCoE의 최신 DevSecOps reference model은 Software Factory를 설명하는 매우 좋은 비-AI 기준점이다.

NIST는 vendor-neutral reference model을 만들면서 실제로 "construct the software factories"라는 표현을 사용한다.

주요 lifecycle:

```text
Plan
→ Develop
→ Build
→ Test
→ Release
→ Deploy
→ Operate
↘
 Continuous Feedback
 ↖
```

횡단 계층:

- Continuous Improvements / Security / Monitoring
- CI/CD
- Zero Trust

핵심 특징:

- 각 phase에 control gate
- downstream feedback이 다시 Plan으로 이동
- build/test에서 independent verification
- provenance / attestation
- ticketing / requirements / risk systems 연결

출처:

- https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html

---

# 3. NIST가 AI를 넣는 방식

2026년 NIST는 현재 human-directed Generative AI를:

- requirement generation
- task decomposition
- ticket creation
- source generation/modification
- infrastructure configuration
- test generation
- security analysis

등에 적용하는 demonstration을 문서화했다.

다음 단계인 Build 3에서는 Agentic AI가:

- develop
- build
- test

코드를 multi-step으로 수행하는 구조를 실증할 예정이다.

또 Agent Identity and Authorization project와 연계한다.

출처:

- https://www.nist.gov/news-events/news/2026/09/new-nist-nccoe-resources-devsecops-and-october-28-webinar-agentic-ai
- https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html

중요한 의미:

> AI Software Factory는 DevSecOps를 버리고 새로 시작하는 개념이라기보다 기존 secure delivery lifecycle 안에서 Agent가 새로운 실행 주체가 되는 방향으로 볼 수 있다.

---

# 4. DevOps / DevSecOps와 Software Factory

DevOps는:

- Dev/Ops collaboration
- automation
- fast feedback
- continuous delivery
- operational ownership

을 포괄하는 **조직·문화·실천 방식**이다.

Software Factory는 그보다 더 구체적인 생산 시스템 관점으로 볼 수 있다.

```text
DevOps
= operating philosophy / practices

Software Factory
= repeatable production system implementing those practices
```

AI 시대에는 Factory에 새로운 actor가 추가된다.

```text
Humans
+ Automation
+ AI Agents
```

따라서 Agent가 들어왔다고 DevOps 원칙이 사라지는 것이 아니다.

오히려:

- feedback
- small batch
- automated test
- observability
- shared ownership

같은 기존 원칙의 중요성이 커진다.

---

# 5. Platform Engineering과 Software Factory

CNCF의 정의:

Platform Engineering은 내부 사용자에게 공통 capability, framework, experience를 제공하는 computing platform을 계획하고 제공하는 discipline이다.

중요 개념:

- internal platform
- self-service
- golden path
- repeatability
- policy
- developer experience

출처:

- https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/

DORA는 internal platform이 AI adoption을 조직 수준의 성과로 전환하는 distribution/governance layer라고 설명한다.

출처:

- https://dora.dev/capabilities/platform-engineering/

---

# 6. 경계 가설

현재 가장 유용한 구분:

```text
Platform Engineering
= 안전하고 표준화된 생산 능력을 제공

Software Factory
= 그 능력을 이용해 실제 Work를 흘려보냄
```

예:

Platform이 제공:

- repository template
- environment
- CI
- secrets
- deployment
- observability
- policy
- sandbox
- API / MCP

Factory가 수행:

- Task selection
- planning
- worker assignment
- implementation
- verification
- retry
- approval
- delivery

즉:

> Platform은 Factory가 사용하는 생산 설비에 가깝고, Factory는 설비를 통해 work item을 결과물로 변환하는 운영 시스템에 가깝다.

단 실제 조직에서는 두 영역이 같은 team/product에 구현될 수 있다.

---

# 7. Agent가 Platform User가 된다

CNCF 2026 논의에서는 기존 Internal Developer Platform의 소비자가 human developer에서 AI agent까지 확대되는 방향이 나타난다.

Agent가 수행할 수 있는 것:

- provision
- deploy
- inspect state
- invoke workflow
- operate resource

따라서 platform에 필요한 것:

- machine-readable interface
- agent identity
- scoped permission
- audit
- common governance

출처:

- https://www.cncf.io/blog/2026/07/21/platform-engineering-for-the-agentic-enterprise-managing-applications-resources-and-ai-agents/

DORA의 golden path가 인간 UI/CLI뿐 아니라 Agent API/MCP surface로 확장되는 방향으로 볼 수 있다.

---

# 8. Software Catalog의 역할

Backstage는 2026년 AI resource를 software catalog에 모델링하는 기능을 제공한다.

예:

- AI Skill
- governance Rule
- MCP Server
- ownership
- lifecycle
- dependency

출처:

- https://backstage.io/docs/ai/ai-in-the-catalog/

Factory 관점:

Catalog는 Agent가 조직의 software estate를 이해하기 위한 구조화된 context source가 될 수 있다.

```text
Repository
+ Software Catalog
+ Runtime State
= richer Agent Context
```

---

# 9. Agent Platform과 Software Factory

Google Gemini Enterprise Agent Platform, AWS AgentCore 같은 시스템은 generic agent infrastructure를 제공한다.

대표 capability:

- runtime
- identity
- gateway/tools
- memory
- observability
- policy
- evaluation

이들은 coding에 국한되지 않는다.

예:

- customer service
- enterprise workflow
- data agent
- operations agent
- coding agent

출처:

- https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime
- https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/

---

# 10. Agent Platform 경계

```text
Agent Platform
= Agent를 실행할 수 있는 범용 기반

Software Factory
= Software Delivery domain에 특화된 Work System
```

Software Factory에 추가로 필요한 domain object:

- Repository
- Branch / Commit
- Requirement
- Issue / Task
- Build
- Test
- PR
- Artifact
- Environment
- Release
- Deployment
- Acceptance

Generic Agent Platform에는 이런 SDLC semantic이 필수가 아니다.

---

# 11. Agent Runtime과 Software Factory

Agent Runtime:

- process/container
- session
- model calls
- tools
- scale
- isolation

Software Factory:

- 여러 Agent Runtime을 생성/관리할 수 있음
- Task 상태를 runtime보다 오래 유지
- verification / delivery lifecycle 관리

따라서:

```text
Agent Runtime
< Agent Platform
< Software Factory? 
```

라고 단순 계층화하면 안 된다.

더 정확한 관계:

```text
Software Factory
uses
- Agent Runtime
- Agent Platform
- Developer Platform
- CI/CD
```

---

# 12. Orchestrator와 Platform Scheduler의 차이

Infrastructure scheduler:

- CPU
- memory
- container
- machine

Factory scheduler:

- Task dependency
- risk
- ownership
- review capacity
- verification capacity
- branch conflict
- worker capability

둘이 연결되지만 목적이 다르다.

---

# 13. Platform Golden Path와 Factory Workflow

Golden Path:

> 이 유형의 서비스를 안전하고 표준적으로 어떻게 만들고 배포하는가?

Factory Workflow:

> 현재 이 Task를 어떤 순서와 actor로 완료할 것인가?

Golden Path가 workflow template 역할을 할 수 있다.

```text
Task
→ select Golden Path
→ instantiate Worker/CI/Deploy
```

---

# 14. Factory가 Platform을 대체하면 안 된다

Anti-pattern:

각 Agent/Factory가 직접:

- secret 관리
- Kubernetes
- deployment
- cloud IAM
- observability

를 제각각 구현.

더 나은 구조:

```text
Factory
→ Platform API / Golden Path
→ Infrastructure
```

이렇게 하면 Agent에게 infrastructure detail을 모두 학습시킬 필요가 줄어든다.

---

# 15. CI/CD 역시 Agent의 Tool이 될 수 있다

기존:

```text
Human push
→ CI
```

AI Factory:

```text
Agent change
→ targeted check
→ CI
→ failure signal
→ Agent fix
→ CI
```

CI가 pipeline 끝이 아니라 Agent feedback loop 안의 tool로 들어간다.

---

# 16. 책에서 사용할 경계 후보

### AI Coding Agent

한 작업을 reasoning/implementation하는 실행자.

### Agent Runtime

Agent가 실행되는 기술 기반.

### Agent Platform

여러 Agent를 안전하게 build/deploy/operate하는 범용 platform.

### Developer Platform

software delivery에 필요한 shared capability/golden path 제공.

### CI/CD

build/test/release/deploy automation.

### AI Software Factory

Intent/Task가 위 시스템들을 통과하며 검증된 software change로 변환되는 전체 work-production system.

---

# 17. 임시 식

```text
AI Software Factory
=
Work Management
+ Agent Orchestration
+ Developer Platform
+ CI/CD
+ Verification
+ Governance
+ Feedback
```

이 식은 최종 정의가 아니다.

하지만 현재 수집된 자료에서는 단순:

```text
Software Factory = Multi-Agent
```

보다 설명력이 훨씬 높다.

---

# 핵심 후보 메시지

> Platform Engineering은 AI Software Factory와 경쟁하는 개념이 아니라 Factory의 기반을 제공한다.

> CI/CD는 Factory의 자동화 spine이지만 Work Selection과 autonomous remediation까지 포함하지는 않는다.

> Agent Platform은 범용 Agent infrastructure이고, Software Factory는 Software Delivery라는 domain workflow를 책임진다.

> AI Software Factory는 DevOps를 대체하기보다 DevOps lifecycle 안에 Agent를 first-class worker로 넣는 진화로 보는 편이 현재 자료와 가장 잘 맞는다.
