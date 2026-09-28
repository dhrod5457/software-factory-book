# AI Software Factory Book - Research Map

기준일: 2026-09-28

이 책의 주제는 **AI 시대의 Software Factory**다.

과거 Software Factory의 역사는 용어 배경을 설명하기 위한 최소 범위로만 다룬다. 핵심은 2025~2026년에 실제 조직들이 coding agent를 단순 보조 도구가 아니라 **지속적으로 소프트웨어 변경을 생산하는 시스템** 안에 배치하기 시작한 변화다.

참고 프로젝트 `cloud-agent-book`의 작성 방식을 따라 다음 순서로 진행한다.

```text
research
→ concept
→ scope
→ toc
→ chapter plan
→ draft
→ review
→ manuscript
```

현재는 **research 단계**다. 목차와 결론을 먼저 고정하지 않는다.

## 책이 조사할 중심 질문

> AI coding agent가 좋아진 뒤, 소프트웨어 개발 조직은 어떻게 "개발자가 agent를 사용하는 방식"에서 "software factory가 지속적으로 작업을 처리하는 방식"으로 이동하는가?

이를 다음 질문으로 나눈다.

- 단일 coding agent와 Software Factory의 경계는 무엇인가?
- 요구사항과 제품 의도를 누가 명세 가능한 Task로 바꾸는가?
- 어떤 Task를 자동으로 선택하고 어떤 Task는 사람이 승인해야 하는가?
- 여러 Worker/Agent를 어떻게 격리하고 병렬 실행하는가?
- Session이 끊겨도 작업 상태와 미완료 맥락을 어떻게 이어가는가?
- Repository, 문서, 도구, MCP, Skills를 어떻게 agent가 읽기 쉬운 환경으로 만드는가?
- Build/Test/Browser/Observability를 어떻게 agent 검증 루프에 넣는가?
- Agent가 "완료했다"고 말하는 것과 실제 완료를 어떻게 분리하는가?
- Code Review, Acceptance Test, Scenario Validation 중 어디까지 자동화할 수 있는가?
- Retry, reassignment, human approval, escalation은 누가 관리하는가?
- Agent의 권한과 blast radius는 어떻게 제한하는가?
- PR 수나 Token이 아니라 Factory 전체 생산성을 무엇으로 측정하는가?
- Software Factory가 스스로 자신의 harness와 workflow를 개선할 수 있는가?

## 작업 정의 - 아직 최종 정의가 아님

현재 자료 수집을 위한 임시 모델:

```text
Intent / Requirement
        ↓
Specification / Acceptance Criteria
        ↓
Task Planning / Dependency
        ↓
Orchestrator / Queue
        ↓
Isolated Worker / Sandbox
        ↓
Coding Agent + Tools + Context
        ↓
Build / Test / Browser / Runtime Verification
        ↓
Evidence / Artifact
        ↓
Review / Approval / Merge
        ↓
Observation / Feedback
        ↺
```

Software Factory인지 판단할 때 단순히 "AI가 코드를 작성한다"는 사실만 보지 않는다.

반복 가능한 생산 시스템으로서 최소한 다음 축을 조사한다.

1. Intent
2. Work selection / planning
3. Orchestration
4. Isolation / execution
5. Context / harness
6. Verification
7. Evidence
8. Human control
9. Recovery / continuity
10. Security / permissions
11. Observability
12. Feedback / self-improvement
13. Metrics / economics

## 1차 조사 대상

### OpenAI - Harness Engineering / Symphony

중점:

- Humans steer, agents execute
- agent-friendly repository
- repository knowledge as system of record
- worktree별 실행환경과 observability
- agent-to-agent review
- task tracker를 control plane으로 사용하는 orchestration
- coding session보다 deliverable/task 중심 운영

자료:

- https://openai.com/index/harness-engineering/
- https://openai.com/index/open-source-codex-orchestration-symphony/

### WorkOS - Horizon

중점:

- event-driven code factory
- Linear issue decomposition
- webhook-driven orchestration
- cloud sandbox
- shared MCP context surface
- orchestrator/control plane과 disposable sandbox 분리
- verification sandbox
- human review gate
- dogfooding을 통한 factory 자체 개선

자료:

- https://workos.com/blog/project-horizon
- https://workos.com/blog/six-months-of-applied-ai-lessons

### Stripe - Minions

중점:

- one-shot end-to-end unattended coding agent
- Slack/task에서 시작해 CI-ready PR까지 진행
- 사람의 중간 개입 없이 실행
- 최종 human review/approval 유지
- 대규모 monorepo에서 context search와 CI integration
- 높은 Agent throughput 이후 review/CI가 병목이 되는 문제

자료:

- https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
- https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
- https://stripe.com/se/sessions/2026/developer-keynote

### StrongDM - Software Factory

중점:

- humans define intent
- agents generate/validate/iterate
- scenario-based validation
- Digital Twin Universe
- human code review 없이 validation으로 convergence를 판단하는 강한 자율 모델

자료:

- https://www.strongdm.com/blog/the-strongdm-software-factory-building-software-with-ai

주의:

StrongDM 모델을 AI Software Factory의 유일한 정의로 사용하지 않는다. human review를 유지하는 WorkOS/Stripe/OpenAI 사례와 비교한다.

### Anthropic - Long-running Harness / Agent Teams

중점:

- long-horizon 작업의 session continuity
- progress artifact와 git history
- feature/task decomposition
- planner / generator / evaluator 분리
- self-evaluation 한계
- evaluator agent
- parallel agents와 shared codebase
- harness complexity와 비용

자료:

- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.anthropic.com/engineering/harness-design-long-running-apps
- https://www.anthropic.com/engineering/building-c-compiler
- https://www.anthropic.com/engineering/how-we-contain-claude

## 기반 연구

### DORA

목적:

AI가 기존 delivery system의 강점과 약점을 증폭한다는 관점, throughput과 stability의 trade-off, 조직/플랫폼 수준 측정.

- https://dora.dev/research/2025/dora-report/
- https://dora.dev/ai/capabilities-model/report/
- https://dora.dev/insights/balancing-ai-tensions/

### METR

목적:

Agent가 장시간 작업을 얼마나 안정적으로 수행할 수 있는지, long-horizon capability를 모델 성능과 factory 구조에서 분리해 이해.

- https://metr.org/time-horizons/

### GitHub Copilot Agent Platform

목적:

- custom agents
- sub-agent orchestration
- hooks
- deterministic policy enforcement
- MCP
- cloud execution

자료:

- https://docs.github.com/en/copilot/concepts/agents/hooks
- https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents

## 핵심 비교 축

사례를 다음 표준 축으로 기록한다.

| 축 | 확인 내용 |
|---|---|
| Work Source | Human prompt, Issue, Slack, CI failure, webhook, backlog |
| Planning | Human, PM agent, planner agent, 없음 |
| Orchestration | Session 직접 실행, queue, task tracker, event-driven |
| Worker | Local, cloud, VM, container, sandbox |
| Isolation | Branch, worktree, container, VM |
| Context | repo docs, AGENTS.md, MCP, logs, issue, chat |
| Continuity | session resume, progress file, durable task state |
| Verification | lint, build, unit, integration, E2E, browser, scenario |
| Evaluator | same agent, separate agent, deterministic runner, human |
| Output | diff, commit, PR, screenshot, log, artifact |
| Human Gate | none, task approval, PR review, merge approval |
| Recovery | retry, reassignment, resume, rollback |
| Security | permission, egress, secret handling, sandbox |
| Observability | task/event/log/trace/worker state |
| Feedback | manual improvement, automated diagnosis, self-improvement |
| Metric | task success, merge, cycle time, quality, cost |

## 중요한 대립 가설

자료를 수집하면서 다음을 일부러 한쪽으로 결론 내리지 않는다.

### Human review

- StrongDM: scenario validation이 code review를 대체하는 방향
- Stripe: unattended implementation + human review
- WorkOS: review-first, explicit human approval
- OpenAI: human review가 필수는 아니며 agent-to-agent review 비중 확대

### Single agent vs multi-agent

- 강한 단일 agent + 좋은 harness로 충분한 영역
- planner/generator/evaluator 분리가 도움이 되는 영역
- parallel agents가 유리한 영역
- coordination cost가 성능 이득을 넘는 영역

### Model capability vs system capability

분리해서 기록한다.

```text
Model Capability
≠
Software Factory Capability
```

Factory 성능에는 모델 외에도 다음이 포함된다.

- Task quality
- Environment
- Context
- Tools
- Verification
- Orchestration
- State
- Security
- Human decisions

## 역사 자료의 위치

과거 Software Factory는 다음 질문에 답하는 정도로만 조사한다.

> 왜 AI 시대에 다시 "factory"라는 표현이 등장했는가?

본문의 주제가 되지 않는다.

필요하다면 서론에서 다음 정도만 비교한다.

```text
과거
표준화 + 자동화 + 재사용 + 품질관리

AI 시대
위 기반
+ autonomous coding agents
+ orchestration
+ isolated execution
+ machine-readable context
+ autonomous verification
+ durable task state
+ continuous feedback
```

## Research 파일 현황

현재 수집된 연구 문서:

- `research/00-research-map.md` - 전체 조사 지도
- `research/01-ai-software-factory-landscape-2026.md` - 2026 실제 운영 사례
- `research/02-factory-architecture-patterns.md` - 공통 아키텍처 패턴
- `research/03-harness-context-and-agent-legibility.md` - Harness / Context / Agent Legibility
- `research/04-orchestration-task-state-and-continuity.md` - Orchestration / Durable Task / Continuity
- `research/05-verification-evidence-and-human-gates.md` - Verification / Evidence / Human Gate
- `research/06-security-isolation-and-permissions.md` - Security / Isolation / Permission
- `research/07-observability-metrics-and-economics.md` - Observability / Metrics / Economics
- `research/08-autonomy-levels-and-self-improvement.md` - Autonomy / Self-improvement
- `research/09-evals-and-benchmark-limitations.md` - Evals / Benchmark
- `research/10-requirements-specification-and-task-planning.md` - Requirement / Specification / Task Planning
- `research/11-product-and-open-source-landscape.md` - Product / Open-source Landscape
- `research/12-engineering-role-and-operating-model.md` - Human Role / Operating Model
- `research/13-protocols-and-interoperability.md` - MCP / A2A / ACP / Interoperability

- `research/14-failure-modes-and-antipatterns.md` - Failure Modes / Anti-patterns
- `research/15-governance-provenance-and-agent-identity.md` - Governance / Provenance / Agent Identity
- `research/16-productivity-evidence-and-measurement.md` - Productivity Evidence / Measurement
- `research/17-review-integration-and-throughput-bottlenecks.md` - Review / Integration / Throughput Bottlenecks
- `research/18-research-contradictions-and-open-questions.md` - Contradictions / Open Questions

- `research/19-boundaries-devops-platform-engineering-agent-platform.md` - CI/CD / DevOps / Platform / Agent Platform 경계
- `research/20-durable-execution-and-workflow-reliability.md` - Durable Execution / Workflow Reliability
- `research/21-agent-ready-developer-platform-and-catalog.md` - Agent-ready Platform / Catalog
- `research/22-closed-loop-sdlc-and-production-feedback.md` - Closed-loop SDLC / Production Feedback
- `research/23-minimum-viable-ai-software-factory.md` - Minimum Viable Factory / Adoption
- `research/sources.md` - 공식 1차 출처 인덱스

다음 단계에서는 새 주제를 무작정 늘리기보다 각 문서의 주장과 출처를 다시 교차검증하고, 서로 반복되는 원칙을 `planning/concept.md` 후보로 추출한다.

## 아직 최종 정의하지 않을 것

현재 research 단계에서는 다음을 확정하지 않는다.

- 최종 책 제목
- 최종 목차
- Software Factory의 한 문장 정의
- 자율성 단계의 업계 표준화된 명칭
- 특정 vendor architecture를 정답으로 채택하는 것

충분한 독립 근거가 반복되는 패턴만 concept 단계로 승격한다.
