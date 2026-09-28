# Sources

기준일: 2026-09-28

AI 시대 Software Factory 조사에 사용하는 1차 자료 인덱스다.

원칙:

- 공식 engineering blog, specification, documentation, repository, 연구 원문을 우선한다.
- 회사가 공개한 생산성 수치는 해당 조직의 관측 결과로만 기록한다.
- vendor가 제안하는 architecture를 업계 보편 정의로 그대로 사용하지 않는다.
- 제품 기능, benchmark 수치, protocol version은 출판 전에 재검증한다.
- 2차 자료는 키워드 탐색과 교차검증에 사용하고 핵심 주장의 단독 근거로 삼지 않는다.

---

## Cursor / Grok Bot

- Grok Bot
  - https://cursor.com/docs/grok-bot
- Work with Grok Bot
  - https://cursor.com/docs/grok-bot/work
- Get started with Grok Bot
  - https://cursor.com/docs/grok-bot/get-started
- Routines
  - https://prod.cursor.com/help/grok-bot/routines
- Grok Bot for Teams and Enterprise
  - https://cursor.com/docs/grok-bot/teams
- Grok Bot security
  - https://prod.cursor.com/docs/grok-bot/security
- Agent Conf 2026 Agenda
  - https://www.agent.sh/agenda

주요 조사 주제:

- persistent agent identity / context
- persistent cloud computer
- shared computer state and security boundary
- browser / computer use integration
- bot-to-bot coordination and handoff
- reusable skills and templates
- schedule / event routines
- approval / policy / isolation
- operator surface

사용 규칙:

- 발표 자막의 사용자 수, 10x 효과, 비용 절감액 같은 정량 주장은 독립 검증 없이 일반화하지 않는다.
- Persistent Agent/Worker를 Durable Task/Execution과 동일시하지 않는다.
- Bot messaging을 durable orchestration의 대체로 보지 않는다.

## OpenAI

### Agent-first engineering / orchestration

- Harness engineering: leveraging Codex in an agent-first world
  - https://openai.com/index/harness-engineering/
- An open-source spec for Codex orchestration: Symphony
  - https://openai.com/index/open-source-codex-orchestration-symphony/
- Introducing the Agents API
  - https://openai.com/index/introducing-the-agents-api/
- The next evolution of the Agents SDK
  - https://openai.com/index/the-next-evolution-of-the-agents-sdk/

### Agents API documentation

- Overview
  - https://developers.openai.com/api/docs/guides/agents-api/overview
- Sandboxes
  - https://developers.openai.com/api/docs/guides/agents/sandboxes
- Observability
  - https://developers.openai.com/api/docs/guides/agents-api/observability
- Tracing
  - https://developers.openai.com/api/docs/guides/agents-api/tracing
- Sessions
  - https://developers.openai.com/api/docs/guides/agents-api/sessions

### Evaluation

- Separating signal from noise in coding evaluations
  - https://openai.com/index/separating-signal-from-noise-coding-evaluations/

---

## Anthropic

### Long-running agents / harness

- Effective harnesses for long-running agents
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Harness design for long-running application development
  - https://www.anthropic.com/engineering/harness-design-long-running-apps
- Scaling Managed Agents: Decoupling the brain from the hands
  - https://www.anthropic.com/engineering/managed-agents
- Building a C compiler with a team of parallel Claudes
  - https://www.anthropic.com/engineering/building-c-compiler

### Context / tools / skills

- Effective context engineering for AI agents
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Writing effective tools for agents
  - https://www.anthropic.com/engineering/writing-tools-for-agents
- Equipping agents for the real world with Agent Skills
  - https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

### Security / containment

- How we contain Claude across products
  - https://www.anthropic.com/engineering/how-we-contain-claude
- Claude Code sandboxing
  - https://www.anthropic.com/engineering/claude-code-sandboxing
- Claude Code Auto Mode
  - https://www.anthropic.com/engineering/claude-code-auto-mode

### Evaluation

- Demystifying evals for AI agents
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Infrastructure noise in agentic coding evaluations
  - https://www.anthropic.com/engineering/infrastructure-noise

### Industry report

- 2026 Agentic Coding Trends Report
  - https://resources.anthropic.com/2026-agentic-coding-trends-report

---

## WorkOS

- The self-driving codebase: Building Horizon at WorkOS
  - https://workos.com/blog/project-horizon
- What we learned in six months of making AI the default at WorkOS
  - https://workos.com/blog/six-months-of-applied-ai-lessons
- Ryan Cooke, *No, That's Not a Software Factory*
  - conference talk transcript, 사용자 제공 자료
  - 파일: `No, That's Not a Software Factory - Ryan Cooke, WorkOS (HvboD89DyQ8).txt`

주요 조사 주제:

- internal code factory
- Product Engineering Process automation
- output metric vs outcome metric
- Linear/webhook orchestration
- continuous planning / plan re-evaluation
- cloud sandbox
- MCP context engine
- durable control plane
- agent-runtime-independent context
- human approval
- authorization boundary
- dogfooding/self-improvement

---

## Warp

### Software Factory / Factory Engineering

- Zach Lloyd, *Software Engineering Is Becoming Factory Engineering*
  - AI Engineer World's Fair 2026 talk
  - https://www.youtube.com/watch?v=tUPPVhBBcoM
  - 조사 기준: 사용자 제공 English transcript와 원문 video
- Zach Lloyd, *Adopting the software factory model: crawl, walk, run*
  - 2026-09-15
  - https://www.warp.dev/blog/adopting-the-software-factory-model-crawl-walk-run

주요 조사 주제:

- interactive agent에서 automated software factory로의 전환
- idea / issue intake와 triage
- product specification / technical specification
- implementation / review / verification / monitoring을 잇는 closed loop
- computer-use 기반 screenshot / video verification
- control plane / execution environment / data plane
- human time / token time을 포함한 factory efficiency
- observer agent / skill loop 기반 self-improvement
- factory engineer / meta-engineering
- open-source project를 public factory로 운영하는 사례

사용 규칙:

- Lloyd의 보편화 전망은 Warp founder의 전망으로 attribution한다.
- Warp 운영 수치나 제품 주장은 vendor claim으로 취급한다.
- 이 책의 Durable Task, Evidence Contract, Accepted Change, guarded self-improvement 모델과 동일한 업계 표준으로 표현하지 않는다.

## Stripe

- Minions: Stripe’s one-shot, end-to-end coding agents
  - https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
- Minions: Stripe’s one-shot, end-to-end coding agents — Part 2
  - https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
- Stripe Sessions 2026 Developer Keynote
  - https://stripe.com/se/sessions/2026/developer-keynote
- Can AI agents build real Stripe integrations? We built a benchmark to find out
  - https://stripe.com/blog/can-ai-agents-build-real-stripe-integrations

주요 조사 주제:

- unattended implementation
- CI-ready PR
- large monorepo
- human review
- reviewer/CI bottleneck

---

## StrongDM

- The StrongDM Software Factory: Building Software with AI
  - https://www.strongdm.com/blog/the-strongdm-software-factory-building-software-with-ai

주요 조사 주제:

- intent/scenario/constraint
- scenario-based validation
- Digital Twin
- high-autonomy model
- human code review boundary

---

## GitHub

### Copilot agents

- About GitHub Copilot hooks
  - https://docs.github.com/en/copilot/concepts/agents/hooks
- GitHub Copilot hooks reference
  - https://docs.github.com/en/copilot/reference/hooks-reference
- Custom agents
  - https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents
- Fleet
  - https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet

### Spec Kit

- Repository
  - https://github.com/github/spec-kit
- Documentation
  - https://github.com/github/spec-kit/blob/main/docs/index.md
- Agentic Spec-Driven Development
  - https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md
- Project history / principles
  - https://github.com/github/spec-kit/blob/main/docs/history.md

주요 조사 주제:

- specification
- planning
- tasks
- convergence
- durable artifacts
- agent-independent process

---

## Kiro

- Specs
  - https://kiro.dev/docs/specs/
- Feature specs
  - https://kiro.dev/docs/specs/feature-specs/
- Quick Spec
  - https://kiro.dev/docs/specs/quick-plan/
- Analyze requirements
  - https://kiro.dev/docs/specs/analyze-requirements/
- Correctness / property-based verification
  - https://kiro.dev/docs/specs/correctness/
- Web / cloud agent
  - https://kiro.dev/docs/web/

주요 조사 주제:

- requirements → design → tasks
- requirements-first / design-first
- risk-based review gates
- requirement analysis
- executable properties

---

## Factory.ai

### Software Factory architecture

- What is a Software Factory? Architecture
  - https://factory.ai/articles/what-is-a-software-factory-architecture
- Software Factory product
  - https://factory.ai/product/software-factory
- Documentation
  - https://docs.factory.ai/

### Runtime / verification / security

- Factory Desktop / Droid Computers
  - https://factory.ai/news/factory-desktop
- Droid Control
  - https://docs.factory.ai/software-factory/droid-control
- Droid Shield 2.0
  - https://factory.ai/news/droid-shield-2-0

### Routing / self-improvement / large tasks

- Model routing belongs in the harness
  - https://factory.ai/news/model-routing-belongs-in-the-harness
- Factory Signals
  - https://factory.ai/news/factory-signals
- What it takes for coding agents to complete large software tasks
  - https://factory.ai/news/what-it-takes-for-coding-agents-to-complete-large-software-tasks

주의:

Factory.ai가 공개한 성능/비용 수치는 vendor 자체 관측값으로만 사용한다.

---

## Cursor

- Cloud Agents
  - https://cursor.com/docs/cloud-agent
- Cloud Agent capabilities
  - https://cursor.com/docs/cloud-agent/capabilities
- Background Agents
  - https://cursor.com/docs/background-agents
- Self-hosted Cloud Agents
  - https://cursor.com/blog/self-hosted-cloud-agents
- Self-hosted runtime selection
  - https://cursor.com/docs/cloud-agent/self-hosted/choose-runtime

주요 조사 주제:

- isolated VM
- asynchronous/parallel agents
- prepared environment
- browser/full desktop
- screenshot/video/log evidence
- self-hosted execution boundary

---

## Google Jules

- Jules public beta
  - https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/
- Jules API / tools
  - https://blog.google/innovation-and-ai/models-and-research/google-labs/jules-tools-jules-api/
- Proactive / Scheduled / Suggested Tasks
  - https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/

주요 조사 주제:

- asynchronous cloud coding
- secure VM
- parallel tasks
- proactive maintenance
- schedule/trigger

---

## Cognition / Devin

- Devin 2.0
  - https://cognition.com/blog/devin-2

주요 조사 주제:

- multiple parallel agents
- separate cloud IDEs
- human steering/takeover
- interactive planning

---

## OpenHands

- OpenHands repository
  - https://github.com/OpenHands/OpenHands
- Software Agent SDK
  - https://github.com/OpenHands/software-agent-sdk

주요 조사 주제:

- self-hosted agent control center
- local / Docker / VM / cloud workspace
- schedule/webhook automation
- agent runtime abstraction
- run history / sandbox lifecycle

---

## SWE-agent

- Background / Agent-Computer Interface
  - https://swe-agent.com/latest/background/
- ACI design
  - https://swe-agent.com/1.0/background/aci/

주요 조사 주제:

- agent-specific tool interface
- concise output
- edit feedback
- environment interaction design

---

## DORA / Google Cloud

- State of AI-assisted Software Development 2025
  - https://dora.dev/research/2025/dora-report/
- DORA AI Capabilities Model
  - https://dora.dev/ai/capabilities-model/report/
- Balancing AI tensions: Moving from AI adoption to effective SDLC use
  - https://dora.dev/insights/balancing-ai-tensions/
- Platform engineering capability
  - https://dora.dev/capabilities/platform-engineering/

주요 조사 주제:

- AI as amplifier
- system-level delivery
- throughput vs stability
- platform quality
- verification/review bottleneck

---

## METR

- Task-Completion Time Horizons of Frontier AI Models
  - https://metr.org/time-horizons/

주요 조사 주제:

- long-horizon task capability
- human-task-duration-based measurement
- model capability와 factory-level reliability 구분

---

## SWE-bench

- SWE-bench
  - https://www.swebench.com/
- SWE-bench Verified
  - https://www.swebench.com/verified.html
- SWE-Bench Pro Verified preprint
  - https://arxiv.org/abs/2609.08149

주의:

benchmark task quality, contamination, infrastructure effect를 함께 확인한다.

---

## Model Context Protocol

- Official site / specification
  - https://modelcontextprotocol.io/
  - https://modelcontextprotocol.io/specification/
- 2026-07-28 specification release
  - https://blog.modelcontextprotocol.io/posts/2026-07-28/
- MCP roadmap
  - https://blog.modelcontextprotocol.io/posts/mcp-roadmap/
- TypeScript SDK
  - https://ts.sdk.modelcontextprotocol.io/v2/

주요 조사 주제:

- Tools / Resources / Prompts
- stateless protocol core
- authorization
- extensions
- long-running Tasks
- enterprise integration

---

## Agent2Agent Protocol

- Official site
  - https://a2a-protocol.org/
- Specification
  - https://a2a-protocol.org/dev/specification/
- A2A and MCP
  - https://a2a-protocol.org/latest/topics/a2a-and-mcp/
- Agentic AI Foundation announcement
  - https://a2a-protocol.org/latest/blog/2026/08/27/a-new-chapter-for-a2a-joining-the-agentic-ai-foundation/
- Original Google announcement
  - https://developers.googleblog.com/a2a-a-new-era-of-agent-interoperability/

주요 조사 주제:

- capability discovery
- task delegation
- independent agent interoperability
- MCP와 A2A 역할 분리

---

## Agent Client Protocol

- ACP
  - https://zed.dev/acp
- ACP Registry
  - https://zed.dev/blog/acp-registry
- Bring Your Own Agent to Zed
  - https://zed.dev/blog/bring-your-own-agent-to-zed

주요 조사 주제:

- agent ↔ editor/client interoperability
- agent/client decoupling
- reusable developer UI

---

# 본문 사용 규칙

## 회사 내부 수치

다음 표현을 사용한다.

> 회사 X는 내부 운영에서 Y를 보고했다.

다음처럼 일반화하지 않는다.

> AI Software Factory는 Y만큼 생산성을 높인다.

## Vendor architecture

vendor가 정의한 구성요소는 비교 자료로 사용한다.

공통 패턴이 여러 독립 자료에서 반복되는 경우에만 책의 일반 원칙 후보로 승격한다.

## 최신 제품 정보

다음은 변경 가능성이 높다.

- 모델명
- 가격
- concurrency
- context size
- product plan
- exact feature support

본문 핵심 논리와 분리하고 기준일을 기록한다.

## Benchmark

benchmark는 model/agent/harness capability 근거로 사용한다.

조직의 전체 software delivery performance와 동일시하지 않는다.


---

## Additional Failure / Governance / Productivity Sources

### Microsoft Research

- Building to the Test: Coding Agents Deliver What You Check, Not What You Requested
  - June 2026
  - https://www.microsoft.com/en-us/research/publication/building-to-the-test-coding-agents-deliver-what-you-check-not-what-you-requested/
- AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation
  - May 2026
  - https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/
- Agentic Coding in the Wild: Characterizing GitHub Copilot at Production Scale
  - July 2026
  - https://www.microsoft.com/en-us/research/publication/agentic-coding-in-the-wild-characterizing-github-copilot-at-production-scale/
- How Do AI Agents Spend Your Money?
  - April 2026
  - https://www.microsoft.com/en-us/research/publication/how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks/
- The Effects of Generative AI on High-Skilled Work
  - June 2025
  - https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/
- Change2Task: From Repository Changes to Executable Coding Agent Tasks and Environments
  - July 2026
  - https://www.microsoft.com/en-us/research/publication/change2task-from-repository-changes-to-executable-coding-agent-tasks-and-environments/
- RedCodeAgent
  - ICLR 2026
  - https://www.microsoft.com/en-us/research/publication/redcodeagent-automatic-red-teaming-agent-against-diverse-code-agents/

### Microsoft Security

- Securing CI/CD in an agentic world: Claude Code GitHub Action case
  - 2026-06-05
  - https://www.microsoft.com/en-us/security/blog/2026/06/05/securing-ci-cd-in-agentic-world-claude-code-github-action-case/
- When prompts become shells: RCE vulnerabilities in AI agent frameworks
  - 2026-05-07
  - https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/

### METR

- Many SWE-bench-Passing PRs Would Not Be Merged into Main
  - 2026-03-10
  - https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
- Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity
  - 2025-07-10
  - https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- We are Changing our Developer Productivity Experiment Design
  - 2026-02-24
  - https://metr.org/blog/2026-02-24-uplift-update/
- Task Substitution and Uplift
  - 2026-05-08
  - https://metr.org/blog/2026-05-08-task-substitution-and-uplift/
- Measuring the Self-Reported Impact of Early-2026 AI on Technical Worker Productivity
  - 2026-05-11
  - https://metr.org/blog/2026-05-11-ai-usage-survey/
- Frontier Risk Report
  - 2026
  - https://metr.org/frontier-risk-report

### NIST / NCCoE

- AI Agent Standards Initiative
  - 2026-02-17
  - https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure
- Accelerating the Adoption of Software and AI Agent Identity and Authorization
  - 2026-02-05
  - https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd
- Summary Analysis of Responses Regarding Security Considerations for AI Agents
  - 2026-05-18
  - https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai
- Secure Software Development, Security, and Operations (DevSecOps) Practices
  - https://pages.nist.gov/nccoe-devsecops/
- DevSecOps Notional Reference Model
  - https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
- Functional Demonstration Scenarios
  - https://pages.nist.gov/nccoe-devsecops/functional-demonstration-scenarios.html

### GitHub - Review / Governance / Security

- Better tools made Copilot code review worse
  - 2026-07-10
  - https://github.blog/ai-and-ml/github-copilot/better-tools-made-copilot-code-review-worse-heres-how-we-actually-improved-it/
- Turn one giant AI-generated pull request to a reviewable stack
  - 2026-08-04
  - https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/
- Stacked pull requests public preview
  - 2026-07-30
  - https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/
- Security validation for third-party coding agents
  - 2026-06-09
  - https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/
- Enterprise AI Controls & agent control plane
  - 2026-02-26
  - https://github.blog/changelog/2026-02-26-enterprise-ai-controls-agent-control-plane-now-generally-available/
- Audit repository cloud-agent configuration
  - 2026-05-18
  - https://github.blog/changelog/2026-05-18-audit-repository-copilot-cloud-agent-configuration-via-the-rest-api/
- Agent automation controls in GitHub Issues
  - 2026-07-23
  - https://github.blog/changelog/2026-07-23-agent-automation-controls-in-github-issues-in-public-preview/
- How we make AI coding more cost efficient without sacrificing task quality
  - 2026-09-02
  - https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/

### OpenAI - Monitoring / Evaluation Integrity

- How we monitor internal coding agents for misalignment
  - 2026-03-19
  - https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/
- Why SWE-bench Verified no longer measures frontier coding capabilities
  - 2026-02-23
  - https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- Separating signal from noise in coding evaluations
  - 2026-07-08
  - https://openai.com/index/separating-signal-from-noise-coding-evaluations/
- The Hugging Face incident and the road ahead
  - 2026-08-26
  - https://openai.com/index/hugging-face-incident-and-the-road-ahead/

### Anthropic - Multi-agent / Reliability

- Patterns and problems in emerging multiagent systems
  - 2026-08-13
  - https://www.anthropic.com/research/multiagent-systems
- How we built our multi-agent research system
  - https://www.anthropic.com/engineering/multi-agent-research-system

### Recent Research Preprints - Use with Caution

These are useful research signals but should not be treated as settled findings without checking publication status and methodology.

- Where Do AI Coding Agents Fail?
  - https://arxiv.org/abs/2601.15195
- Early-Stage Prediction of Review Effort in AI-Generated Pull Requests
  - https://arxiv.org/abs/2601.00753
- SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents
  - https://arxiv.org/abs/2605.21384
- RewardHackingAgents
  - https://arxiv.org/abs/2603.11337
- Debt Behind the AI Boom
  - https://arxiv.org/abs/2603.28592
- AI-to-AI Code Reviews of GitHub Pull Requests
  - https://arxiv.org/abs/2608.21311


---

## Platform Engineering / DevSecOps / Durable Execution Sources

### NIST / NCCoE - Software Factory / DevSecOps Boundary

- Secure Software Development, Security, and Operations (DevSecOps) Practices
  - https://www.nccoe.nist.gov/projects/secure-software-development-security-and-operations-devsecops-practices
- Notional Reference Model for DevSecOps
  - updated 2026-09
  - https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
- Functional Demonstration Scenarios
  - https://pages.nist.gov/nccoe-devsecops/functional-demonstration-scenarios.html
- New NIST NCCoE Resources on DevSecOps and Agentic AI
  - 2026-09-24
  - https://www.nist.gov/news-events/news/2026/09/new-nist-nccoe-resources-devsecops-and-october-28-webinar-agentic-ai

주요 조사 주제:

- Plan / Develop / Build / Test / Release / Deploy / Operate
- software factory reference model
- control gates
- continuous feedback
- CI/CD
- Zero Trust
- requirement/task generation with AI
- future Agentic AI in develop/build/test
- Agent identity / authorization

### DORA - Platform Engineering

- Platform engineering capability
  - updated 2026-01-12
  - https://dora.dev/capabilities/platform-engineering/

주요 조사 주제:

- Internal Developer Platform
- golden path
- platform as distribution/governance layer for AI
- downstream disorder
- minimum viable platform
- clear task feedback
- balanced scorecard

### CNCF - Platform Engineering

- Platform Engineering Maturity Model
  - https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- Platform engineering for the agentic enterprise
  - 2026-07-21
  - https://www.cncf.io/blog/2026/07/21/platform-engineering-for-the-agentic-enterprise-managing-applications-resources-and-ai-agents/
- Platform engineering maturity: From toolchain to self-service
  - 2026-09-01
  - https://www.cncf.io/blog/2026/09/01/platform-engineering-maturity-from-toolchain-to-self-service/

주요 조사 주제:

- self-service
- platform interfaces
- Agent as first-class platform consumer
- identity / policy / audit
- machine-readable interface

### Backstage

- AI in the Software Catalog
  - https://backstage.io/docs/ai/ai-in-the-catalog/
- Spotify Portal / Software Catalog
  - https://backstage.spotify.com/build-like-spotify

주요 조사 주제:

- AI resource catalog
- skills
- rules
- MCP servers
- ownership
- lifecycle
- Agent-readable organizational context

### Microsoft Durable Task

- Durable Task for AI agents
  - updated 2026-05-05
  - https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents

주요 조사 주제:

- durable execution
- checkpointing
- resume
- retry
- framework-independent runtime
- deterministic vs agent-directed workflows

### Google Agent Executor / Agent Platform

- Agent Executor: Google’s distributed Agent Runtime
  - 2026-05-20
  - https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime
- Gemini Enterprise Agent Runtime
  - https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime
- Choose your agentic AI architecture components
  - https://docs.cloud.google.com/architecture/choose-agentic-ai-architecture-components
- Gemini Enterprise Agent Platform updates
  - 2026-07-29
  - https://cloud.google.com/blog/products/ai-machine-learning/whats-new-in-gemini-enterprise-agent-platform

주요 조사 주제:

- event log / snapshot
- resumption
- distributed deployment
- generic Agent Runtime
- Agent Platform vs Software Factory boundary

### Temporal

- Durable AI
  - https://docs.temporal.io/ai
- Of course you can build dynamic AI agents with Temporal
  - 2025-11-12
  - https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal
- Building AI agents that overcome the complexity cliff
  - 2026-03-10
  - https://temporal.io/blog/building-ai-agents-that-overcome-the-complexity-cliff

주요 조사 주제:

- durable workflow
- event history
- replay
- activities
- long-running agents
- HITL
- idempotent side effects

### Vercel

- Introducing eve
  - 2026-06-17
  - https://vercel.com/blog/introducing-eve
- A new programming model for durable execution
  - 2026-04-16
  - https://vercel.com/blog/a-new-programming-model-for-durable-execution

주요 조사 주제:

- durable execution
- sandboxed compute
- HITL
- subagents
- evals

### AWS AgentCore

- Introducing Amazon Bedrock AgentCore
  - https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-agentcore-securely-deploy-and-operate-ai-agents-at-any-scale/
- AgentCore runtime security best practices
  - https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html
- AgentCore observability
  - https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html

주요 조사 주제:

- generic Agent Platform
- runtime
- identity
- gateway
- memory
- observability
- framework/model independence


---

## Academic Agentic Software Engineering Research

### Surveys

- From LLMs to LLM-based Agents for Software Engineering: A Survey of Current, Challenges and Future
  - https://arxiv.org/abs/2408.02479
- Large Language Model-Based Agents for Software Engineering: A Survey
  - https://arxiv.org/abs/2409.02977
- Agents in Software Engineering: Survey, Landscape, and Vision
  - https://arxiv.org/abs/2409.09030

### Agent Architecture / Interface

- SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
  - NeurIPS 2024
  - https://arxiv.org/abs/2405.15793
- Agentless: Demystifying LLM-based Software Engineering Agents
  - https://arxiv.org/abs/2407.01489
- OpenHands: An Open Platform for AI Software Developers as Generalist Agents
  - https://arxiv.org/abs/2407.16741
- The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents
  - https://arxiv.org/abs/2511.03690

### Requirements / Decomposition / Orchestration

- REAgent: Requirement-Driven LLM Agents for Software Issue Resolution
  - https://arxiv.org/abs/2604.06861
- Runtime-Structured Task Decomposition for Agentic Coding Systems
  - https://arxiv.org/abs/2605.15425
- Deterministic vs. LLM-Controlled Orchestration for COBOL-to-Python Modernization
  - AIware 2026
  - https://doi.org/10.1145/3805760.3814891
  - https://arxiv.org/abs/2605.09894
- Wink: Recovering from Misbehaviors in Coding Agents
  - AIware 2026
  - https://arxiv.org/abs/2602.17037

### Repository Understanding / Context

- SWE-Explore: Benchmarking How Coding Agents Explore Repositories
  - https://arxiv.org/abs/2606.07297
- From Laboratory to Real-World Applications: Benchmarking Agentic Code Reasoning at the Repository Level
  - https://arxiv.org/abs/2601.03731
- Agent READMEs: An Empirical Study of Context Files for Agentic Coding
  - TOSEM 2026
  - https://arxiv.org/abs/2511.12884
- Configuring Agentic AI Coding Tools: An Exploratory Study
  - AIware 2026
  - https://arxiv.org/abs/2602.14690
  - https://doi.org/10.1145/3805760.3814887
- Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?
  - ICLR 2026 MemAgents Workshop
  - https://arxiv.org/abs/2602.11988
- Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories
  - https://arxiv.org/abs/2607.27250
- Operationalizing Ethics for AI Agents: How Developers Encode Values into Repository Context Files
  - AIware 2026
  - https://arxiv.org/abs/2605.05584
  - https://doi.org/10.1145/3805760.3814899

### Human-Agent Collaboration / Responsibility

- When Code Authors Are Agents: A Large-Scale Study of Human-Agent Collaboration in Pull Requests
  - AIware 2026
  - https://doi.org/10.1145/3805760.3814909
- Collaborator or Assistant? How AI Coding Agents Partition Work across Pull Request Lifecycles
  - AIware 2026
  - https://doi.org/10.1145/3805760.3814893
- Humans are Missing from AI Coding Agent Research
  - https://arxiv.org/abs/2608.12355
- Towards AI as a Collaborative Partner: A Taxonomy of AI Agent Behavior in Software Engineering
  - AIware 2026
  - https://doi.org/10.1145/3805760.3814913
- Dialogue SWE-Bench: A Benchmark for Dialogue-Driven Coding Agents
  - https://arxiv.org/abs/2606.13995
- Reliable Vibe Coding: The Human-AI Context Gap in Software Development
  - HHAI 2026
  - https://doi.org/10.3233/FAIA260505
- Preemptive, Buffered, or Guided? Empirical Studies on Human-AI Interaction Strategies for Software Test Case Development
  - ACM TOCHI 2026
  - https://doi.org/10.1145/3817601
- Accountable Agents in Software Engineering: An Analysis of Terms of Service and a Research Roadmap
  - AIware 2026
  - https://arxiv.org/abs/2605.04532
  - https://doi.org/10.1145/3805760.3814889
- Software Engineering in the Agent Era: From Trustworthy Change to Human-Agent Software Organizations
  - theory / position-oriented work; empirical validation still open
  - https://arxiv.org/abs/2609.04630

### Benchmark / Evaluation Science

- SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?
  - ICML 2025
  - https://proceedings.mlr.press/v267/miserendino25a.html
  - https://arxiv.org/abs/2502.12115
- AI Agents That Matter
  - TMLR 2025
  - https://arxiv.org/abs/2407.01502
- SWE-smith: Scaling Data for Software Engineering Agents
  - https://arxiv.org/abs/2504.21798
- SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents
  - https://arxiv.org/abs/2505.20411
- RACE-Bench: A Reasoning-Augmented Benchmark for Repository-Level Code Agents on Feature Addition
  - https://arxiv.org/abs/2603.26337
- RuBench: A Repository-Level Agentic Coding Benchmark with Natively Authored Russian Task Specifications
  - https://arxiv.org/abs/2607.06411
- Are Performance-Optimization Benchmarks Reliably Measuring Coding Agents?
  - https://arxiv.org/abs/2607.01211
- RigorBench: Benchmarking Engineering Process Discipline in Autonomous AI Coding Agents
  - ASE 2026 TRUST
  - https://conf.researchr.org/details/ase-2026/trust-2026-papers/4/

### Verification

- Fixpad++: Automated Bug Fix Verification using LLM Agents
  - AIware 2026
  - https://doi.org/10.1145/3805760.3814915

## Academic-source usage rules

- Peer-reviewed conference/journal papers get priority over vendor claims for general conclusions.
- arXiv/preprints are useful but should be labeled as preprints unless publication is confirmed.
- Position/theory papers should be used for concepts, not presented as empirical fact.
- Small-N ablations are used as counterexamples or hypotheses rather than universal rules.
- Benchmark result numbers should be interpreted together with environment, cost, task selection, and contamination controls.

---

## Implementation Tutorial Sources - Use as Case Studies

### Simplest Software Factory

- *I Built the Simplest Software Factory*
  - YouTube video id: `AsvzMlLyQ38`
  - https://www.youtube.com/watch?v=AsvzMlLyQ38
  - user-provided transcript reviewed 2026-09-28
  - Source Quality: C급 tutorial / implementation case

주요 사용 주제:

- GitHub Issue → Dispatcher → Agent → Pull Request → Human Review
- Software Factory와 Coding Agent의 역할 분리
- deterministic dispatcher와 optional LLM triage
- isolated worker / VM sandbox
- reusable worker snapshot
- GitHub label/comment를 이용한 human-facing state
- dry-run 후 side effect를 단계적으로 활성화하는 패턴
- multi-repository hub-and-spoke orchestration

사용 제한:

- sponsor가 포함된 tutorial이므로 vendor architecture의 우월성 근거로 사용하지 않는다.
- 특정 Worker 수, plan limit, provider/model 선택을 일반 원칙으로 일반화하지 않는다.
- 핵심 설계 원칙은 A급 자료와 기존 연구에서 독립적으로 뒷받침되어야 한다.
