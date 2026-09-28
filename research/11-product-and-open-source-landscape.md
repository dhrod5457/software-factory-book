# Product and Open-source Landscape

기준일: 2026-09-28

이 문서는 특정 제품 비교/추천을 위한 표가 아니다.

AI Software Factory를 구성하는 기능이 실제 시장과 오픈소스에서 어떤 형태로 구현되고 있는지 관찰하기 위한 landscape다.

## 1. OpenAI

### Codex / Harness Engineering

관심 영역:

- agent-friendly repo
- tests/guardrails
- application legibility
- repository knowledge
- agent review

자료:

- https://openai.com/index/harness-engineering/

### Symphony

관심 영역:

- issue tracker control plane
- durable task
- dedicated workspace
- supervisor
- agent loop
- review workflow

자료:

- https://openai.com/index/open-source-codex-orchestration-symphony/

### Agents API

관심 영역:

- managed session
- long-running agent
- context compaction
- subagents
- hosted/self-hosted sandbox
- observability

자료:

- https://openai.com/index/introducing-the-agents-api/
- https://developers.openai.com/api/docs/guides/agents-api/overview

## 2. Anthropic

### Claude Code / Agent SDK

관심:

- long-running harness
- session continuity
- evaluator pattern
- context engineering
- skills
- security

### Managed Agents

관심:

- session/harness/sandbox separation
- brain/hands
- durable state
- many brains / many hands

자료:

- https://www.anthropic.com/engineering/managed-agents

## 3. GitHub Copilot

관심:

- cloud agent
- subagents
- custom agents
- hooks
- fleet
- SDK

Fleet:

- plan decomposition
- parallel subagent
- parent orchestration

Hooks:

- deterministic policy

Spec Kit:

- specification
- planning
- tasks
- convergence

자료:

- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet
- https://docs.github.com/en/copilot/concepts/agents/hooks
- https://github.com/github/spec-kit

## 4. WorkOS Horizon

관심:

- code factory
- Linear/webhook
- cloud sandbox
- MCP context engine
- durable orchestrator
- human review
- compounding self-improvement

자료:

- https://workos.com/blog/project-horizon

## 5. Stripe Minions

관심:

- one-shot
- end-to-end
- unattended
- large monorepo
- CI
- human review

자료:

- https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
- https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2

## 6. StrongDM

관심:

- explicit Software Factory framing
- scenario-based validation
- Digital Twin
- high autonomy
- review boundary shift

자료:

- https://www.strongdm.com/blog/the-strongdm-software-factory-building-software-with-ai

## 7. Factory.ai

가장 직접적으로 "Software Factory" 제품 개념을 전개한다.

2026 reference architecture:

1. Intent intake
2. Context
3. Planning
4. Execution
5. Review/policy
6. Delivery
7. Observability

추가 관심:

- Droids
- model routing
- automations
- Missions
- Droid Computers
- Shield
- Signals
- Droid Control
- OTEL

자료:

- https://factory.ai/articles/what-is-a-software-factory-architecture
- https://factory.ai/product/software-factory
- https://docs.factory.ai/

주의:

Factory.ai가 정의하는 architecture는 vendor의 product framing이다.

중요한 참고 모델이지만 책의 보편 정의로 그대로 채택하지 않는다.

## 8. Cursor

### Cloud Agents

- isolated VM
- background/asynchronous
- parallel
- browser/full desktop
- MCP
- multi-repo
- screenshots/videos/log artifact

### Self-hosted

- organization perimeter
- internal resources
- team pool

자료:

- https://cursor.com/docs/cloud-agent
- https://cursor.com/docs/cloud-agent/capabilities
- https://cursor.com/blog/self-hosted-cloud-agents

## 9. Google Jules

관심:

- asynchronous coding
- secure VM
- GitHub
- parallel tasks
- API
- scheduled task
- suggested task
- proactive maintenance

자료:

- https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/
- https://blog.google/innovation-and-ai/models-and-research/google-labs/jules-tools-jules-api/
- https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/

## 10. Kiro

관심:

- requirements
- design
- tasks
- review gates
- autonomous web mode
- sandbox
- automations
- property-based verification

자료:

- https://kiro.dev/docs/specs/
- https://kiro.dev/docs/web/
- https://kiro.dev/docs/specs/correctness/

## 11. Devin

Devin 2.0:

- multiple parallel Devins
- each own cloud IDE
- human can steer/take over
- interactive planning
- search
- wiki

관심:

- parallel developer agent UX
- cloud environment
- human steering model

자료:

- https://cognition.com/blog/devin-2

## 12. OpenHands

2026 OpenHands Agent Canvas:

- self-hosted control center
- OpenHands/Claude/Codex/Gemini/ACP agent backend
- local/remote/cloud
- schedule/webhook automation
- Slack/GitHub/Linear integration

SDK:

- local or ephemeral workspace
- Docker/Kubernetes
- multi-agent major tasks

Repository boundaries:

- Agent Canvas
- Agent SDK/Server
- automation
- extensions

이 구조는 오픈소스로 control plane/runtime 분리를 관찰하기 좋다.

자료:

- https://github.com/OpenHands/OpenHands
- https://github.com/OpenHands/software-agent-sdk

## 13. SWE-agent / mini-SWE-agent

연구 가치:

- Agent-Computer Interface
- tool design
- coding benchmark harness

Software Factory 전체는 아니지만 worker/harness 연구에 중요하다.

자료:

- https://swe-agent.com/latest/background/
- https://swe-agent.com/1.0/background/aci/

## 14. 기능 Matrix

| 시스템 | Spec/Plan | Queue/Orchestrator | Isolated Runtime | Parallel | Verification | Evidence | Human Gate | Automation |
|---|---|---|---|---|---|---|---|---|
| OpenAI Symphony | Issue | Yes | Workspace | Yes | Repo-specific | Video/PR | Review | Always-on |
| WorkOS Horizon | PM Agent | Yes | Cloud sandbox | Yes | Test/browser roadmap | PR | Merge | Event |
| GitHub Copilot | Plan | Session/Fleet | Cloud/local | Yes | Tools/CI | Result | Configurable | CLI/cloud |
| Factory.ai | Yes | Missions/Automation | Local/cloud | Yes | QA/Droid Control | Video/log | Adjustable | Schedule/event |
| Cursor | Task | Cloud Agent control | VM | Yes | Browser/test | Video/screenshot/log | Review | Automation |
| Jules | Task | Service | Cloud VM | Yes | Agent test | Diff/plan | Review | Schedule/proactive |
| Kiro | Requirements/Design/Tasks | Session/Automation | Sandbox | Some | PBT/test | Spec/PR | Configurable | Cron |
| OpenHands | Agent/task | Automation server | Docker/VM/cloud | Yes | Tools | Run history | Configurable | Schedule/webhook |

이 표는 기능 존재 여부를 대략적으로 비교하는 연구용 초안이다.

제품 기능은 빠르게 변하므로 출판 전에 다시 검증해야 한다.

## 15. Landscape에서 보이는 공통 방향

### 방향 A

Local interactive coding → Remote asynchronous work.

### 방향 B

Single session → Parallel agents.

### 방향 C

Prompt → Durable specification/task.

### 방향 D

Manual start → Event/schedule/proactive start.

### 방향 E

Source-only → Browser/runtime evidence.

### 방향 F

Human permission each action → Sandbox/policy boundary.

### 방향 G

Agent-specific UX → Agent-independent orchestration/runtime abstraction.

## 16. 책에서 제품을 사용하는 원칙

제품은 chapter의 주인공이 아니다.

각 제품은 pattern의 concrete example로 사용한다.

예:

```text
Durable Task
→ Symphony / Horizon

Sandbox Boundary
→ Anthropic / Cursor / OpenAI

Spec-driven
→ Spec Kit / Kiro

Parallel Fleet
→ GitHub / Anthropic

Evidence
→ Cursor / Factory

Self-improvement
→ WorkOS / Factory.ai
```

제품명이 사라져도 원칙이 남도록 작성한다.
