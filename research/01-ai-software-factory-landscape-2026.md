# AI Software Factory Landscape - 2026

기준일: 2026-09-28

이 문서는 AI 시대 Software Factory를 실제로 운영하거나 그에 가까운 시스템을 공개한 사례를 비교하기 위한 1차 자료 노트다.

## 먼저 보이는 공통점

현재 사례들을 비교하면 Software Factory는 단순한 "coding agent"보다 넓다.

반복해서 등장하는 구성은 다음과 같다.

```text
Work Source
→ Planning
→ Orchestration
→ Isolated Execution
→ Agent + Context + Tools
→ Verification
→ Evidence
→ Human/Automated Gate
→ Merge / Next Task
```

특히 모델 자체보다 다음 인프라가 반복적으로 중요하게 등장한다.

- agent-friendly repository
- cloud sandbox / worktree
- durable task state
- issue tracker / webhook control plane
- MCP / tools / repository-local knowledge
- automated test
- browser/runtime verification
- independent evaluator
- evidence artifact
- human approval boundary
- logs / metrics / traces
- retry / continuation

---

# 1. OpenAI - Harness Engineering

자료:

- OpenAI, `Harness engineering: leveraging Codex in an agent-first world`, 2026-02-11
- https://openai.com/index/harness-engineering/

공개 사례:

- 내부 제품을 수동 작성 코드 없이 Codex로 구축
- 3명의 엔지니어가 약 5개월 동안 약 1,500 PR을 merge했다고 보고
- repository의 코드뿐 아니라 tests, CI, docs, observability, internal tooling도 agent가 생성
- 인간의 역할을 코드 작성보다 환경, 의도, feedback loop 설계 쪽으로 이동

중요한 패턴:

### Repository knowledge as system of record

거대한 단일 instruction file보다 agent가 탐색할 수 있는 구조화된 repository knowledge를 강조한다.

핵심 문제:

- agent가 접근할 수 없는 Slack/문서/사람 머릿속 정보는 실행 중 사실상 존재하지 않는다.
- context를 많이 넣는 것이 아니라 필요한 지식을 discoverable하게 만드는 것이 중요하다.

### Application legibility

Agent가 실제 application을 검증할 수 있도록 다음을 노출했다.

- worktree별 app instance
- DOM
- screenshots
- navigation
- logs
- metrics
- traces

즉, "코드를 읽을 수 있음"에서 "실행 결과를 읽을 수 있음"으로 확장한다.

### Agent-to-agent review

사람 review를 완전히 없앤다고 정의하지 않지만, review workload를 agent-to-agent 쪽으로 크게 이동한다.

### Factory 관점의 의미

Agent 성능보다 **agent가 일할 수 있는 repository/harness를 만드는 일**이 독립된 engineering discipline이 될 수 있다는 강한 사례다.

---

# 2. OpenAI - Symphony

자료:

- OpenAI, `An open-source spec for Codex orchestration: Symphony`, 2026-04-27
- https://openai.com/index/open-source-codex-orchestration-symphony/

핵심 변화:

```text
Before
Human
→ agent session 관리
→ PR
→ 다음 session 시작

Symphony
Task Tracker
→ open task 감지
→ dedicated workspace
→ agent loop
→ task 상태
→ review
```

OpenAI가 명시적으로 제시하는 전환:

- coding session 중심이 아니라 deliverable/task 중심
- Linear 같은 project-management board를 control plane으로 사용
- open task마다 dedicated agent workspace
- active task에 agent가 지속적으로 붙어 있도록 supervisor/orchestrator가 관리

Factory 관점의 의미:

> Software Factory의 핵심 추상화가 "Agent Session"에서 "Durable Task"로 이동한다.

이 주제는 책의 핵심 후보다.

---

# 3. WorkOS - Horizon

자료:

- WorkOS, `The self-driving codebase: Building Horizon at WorkOS`, 2026-05-06
- https://workos.com/blog/project-horizon

WorkOS가 직접 사용하는 표현:

- internal code factory
- event-driven AI software development
- self-driving codebase

## End-to-end 흐름

공개된 흐름을 단순화하면:

```text
Human requirements
→ Linear project
→ PM agent decomposes issues
→ Human reviews issues
→ issue In Progress
→ webhook
→ orchestrator
→ cloud sandbox
→ implementation agent
→ validation
→ PR
→ Human approval
→ merge webhook
→ dependency re-evaluation
→ next eligible task
```

## 세 개의 핵심 infrastructure

WorkOS는 구조를 거의 명시적으로 세 층으로 설명한다.

### Execution engine

Cloud sandbox.

요구사항:

- isolation
- reproducibility
- independent verification
- security
- egress control
- fast boot
- cache
- pause/resume
- concurrent execution

### Context engine

Custom MCP server.

목적:

- logs
- Sentry errors
- Slack conversations
- internal conventions
- shared tools

Agent마다 거대한 prompt를 들고 다니는 대신 공통 context/tool surface를 제공한다.

### Work orchestrator

Sandbox 밖의 control plane.

역할:

- webhook 정규화
- work item
- sandbox lifecycle
- routing
- permission
- state
- artifact
- Slack/Linear/GitHub/UI handoff

중요한 설계:

> Sandbox는 disposable execution primitive이고, orchestrator는 durable control plane이다.

## Verification

현재:

- lint
- build
- automated test

확장 방향:

- headless browser
- screenshots
- DOM snapshots
- separate verification sandbox
- security testing agent

## Human gate

WorkOS는 PR merge 전에 명시적 human approval을 유지한다.

따라서 autonomy를 높여도 human control plane을 없애지 않는 사례다.

## Self-improvement

Horizon이 실제 작업을 하면서 드러내는 문제:

- missing script
- flaky test
- unclear convention
- slow environment
- poor MCP pattern

이런 friction을 다시 factory 개선 Task로 넣는다.

Factory가 product code뿐 아니라 **자기 생산 시스템도 개선하는 compounding loop**를 갖는 사례다.

---

# 4. Stripe - Minions

자료:

- Stripe, `Minions: Stripe’s one-shot, end-to-end coding agents`, 2026-02-09
- https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
- Stripe, Part 2, 2026-02-19
- https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
- Stripe Sessions 2026 Developer Keynote
- https://stripe.com/se/sessions/2026/developer-keynote

Stripe가 공개한 모델:

- one-shot
- end-to-end
- unattended implementation
- human-reviewed output

대표 흐름:

```text
Slack / Task
→ Minion
→ repository search
→ implementation
→ test / CI
→ PR
→ human review / approve
```

Stripe는 2026 Sessions에서 Minions가 주당 1,000개 이상의 PR을 production으로 보낸다고 밝혔다.

주의:

이 수치는 Stripe 자체 운영 발표다. 업계 일반 생산성 수치로 일반화하지 않는다.

Factory 관점의 핵심:

- 개발자의 scarce resource를 attention으로 본다.
- agent가 중간 질문을 반복하기보다 unattended하게 task를 끝까지 처리한다.
- 최종 review는 사람에게 남긴다.

WorkOS와 함께 **implementation autonomy + human merge authority** 패턴을 설명하기 좋다.

---

# 5. StrongDM - Software Factory

자료:

- StrongDM, `The StrongDM Software Factory: Building Software with AI`, 2026-02-19
- https://www.strongdm.com/blog/the-strongdm-software-factory-building-software-with-ai

StrongDM의 공개 설명은 다른 사례보다 자율성이 강하다.

흐름:

```text
Human
→ intent
→ scenarios
→ constraints

Agents
→ generate
→ validate against behavior
→ iterate until convergence
```

핵심 요소:

- scenario-based validation
- Digital Twin Universe
- end-to-end agent execution
- human code review 없이 validation 중심으로 운영

Factory 관점에서 중요한 질문:

> 충분히 강한 behavioral validation이 있다면 source code review의 역할은 어디까지 줄어들 수 있는가?

이것을 책의 결론으로 바로 채택하지 않는다.

Stripe/WorkOS의 human review 모델과 대비해 **Autonomy Boundary** 사례로 사용한다.

---

# 6. Anthropic - Long-running Agent Harness

자료:

- Anthropic, `Effective harnesses for long-running agents`, 2025-11-26
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

핵심 문제:

- context window가 끝나면 이전 session의 실제 상태를 잃을 수 있음
- agent가 큰 작업을 one-shot하려다 중간에 끊김
- 새 agent가 이전 작업을 이해하는 데 비용 발생
- 일부 구현 후 전체 완료로 오판

해결 패턴:

- initializer
- feature list
- progress artifact
- git history
- incremental work
- clean handoff

Factory 관점의 의미:

> Long-running autonomy에는 LLM memory보다 durable external state가 중요하다.

이 주제는 Task State / Session Continuity 장의 핵심 근거 후보다.

---

# 7. Anthropic - Planner / Generator / Evaluator

자료:

- Anthropic, `Harness design for long-running application development`, 2026-03-24
- https://www.anthropic.com/engineering/harness-design-long-running-apps

구조:

```text
Planner
→ Generator
→ Evaluator
→ Generator
→ Evaluator
...
```

주요 발견:

- self-evaluation은 지나치게 긍정적일 수 있음
- 생성 agent와 평가 agent를 분리하면 개선 여지가 있음
- evaluator는 Playwright로 실제 application을 사용
- acceptance criteria를 구체화할수록 평가 가능성이 높아짐
- harness는 품질을 높일 수 있지만 비용/시간도 크게 증가함
- 모델이 좋아지면 필요한 harness의 경계도 이동함

Factory 관점의 의미:

> 모든 Task에 multi-agent가 필요한 것이 아니라, 현재 모델의 reliable boundary 밖에 있는 Task에 추가 evaluator/harness가 비용을 정당화하는지 판단해야 한다.

---

# 8. Anthropic - Parallel Agent Teams

자료:

- Anthropic, `Building a C compiler with a team of parallel Claudes`, 2026-02-05
- https://www.anthropic.com/engineering/building-c-compiler

공개 실험:

- 16 agents
- shared codebase
- 장기간 병렬 작업
- test harness를 중심으로 autonomous progress

핵심 조사 질문:

- 병렬 agent가 같은 파일/상태에 접근할 때 충돌을 어떻게 제어했는가?
- coordinator 없이 가능한 범위는 어디인가?
- test가 work allocation과 convergence에 어떤 역할을 하는가?
- token/compute 비용이 어느 시점부터 비효율적이 되는가?

---

# 9. DORA - AI는 Delivery System을 증폭한다

자료:

- https://dora.dev/research/2025/dora-report/
- https://dora.dev/insights/balancing-ai-tensions/

DORA 2025의 핵심 관점:

- AI adoption은 기존 조직의 강점과 약점을 증폭하는 성격을 보임
- 생성 속도 향상만으로 전체 SDLC가 자동 개선되지 않음
- saved time이 auditing/verification으로 이동할 수 있음
- 높은 AI adoption은 throughput 증가와 함께 instability 증가와도 연관됨

Factory 관점의 의미:

> Software Factory의 성능을 코드 생성량으로만 측정하면 안 된다.

---

# 10. METR - Long-horizon capability

자료:

- METR, `Task-Completion Time Horizons of Frontier AI Models`
- https://metr.org/time-horizons/

METR는 human expert가 걸리는 작업 시간 기준으로 agent의 task-completion horizon을 측정한다.

Factory 관점의 의미:

- 모델 자체의 long-task reliability와
- factory가 decomposition/retry/state/verification으로 만든 시스템-level reliability를 구분할 수 있다.

---

# 첫 비교표

| 사례 | Task 시작 | Orchestration | Execution | Verification | Human Gate |
|---|---|---|---|---|---|
| OpenAI Harness | Human task | Prompt/PR loop | Worktree | tests + app/log/metrics + agent review | 선택적 |
| OpenAI Symphony | Issue tracker | Supervisor | dedicated workspace | repo workflow | review |
| WorkOS Horizon | Webhook/Linear | durable orchestrator | cloud sandbox | lint/build/test, browser 확대 예정 | PR merge approval |
| Stripe Minions | Slack/task | unattended one-shot | internal agent runtime | CI | PR review |
| StrongDM | intent/scenario | factory loop | agent runtime | scenario/Digital Twin | code review 없음 |
| Anthropic Harness | spec/task list | harness loop | agent session | feature/test/browser evaluator | 실험별 다름 |

이 표는 1차 버전이다. 이후 각 시스템의 정확한 세부 구조를 공식 자료로 보강한다.

---

# 현재 가장 중요한 연구 가설

## 가설 1

AI Software Factory의 핵심은 더 좋은 code generation이 아니라 **durable work orchestration**이다.

## 가설 2

Task는 prompt보다 중요한 추상화가 된다.

```text
Prompt
= 한 번의 interaction

Task
= 상태, dependency, evidence, retry, ownership을 가진 durable work item
```

## 가설 3

Factory에서 agent의 실행환경은 IDE보다 worker runtime에 가깝다.

## 가설 4

Verification은 post-process가 아니라 agent loop 내부에 들어간다.

## 가설 5

Human의 역할은 code author에서 다음 방향으로 이동한다.

- intent
- specification
- architecture
- acceptance
- risk decision
- exception handling
- system improvement

단, 어느 단계까지 이동하는지는 조직마다 다르다.

## 가설 6

완전 자율보다 **명확한 autonomy boundary**가 더 일반적인 산업 패턴일 가능성이 있다.

현재 사례:

- StrongDM: 높은 autonomy
- Stripe: implementation autonomous, review human
- WorkOS: planning/review human, execution autonomous
- OpenAI: human steering + increasing agent review

## 가설 7

Factory의 가장 중요한 자산은 모델보다 시간이 지나며 축적되는 다음 요소일 수 있다.

- executable validation
- repository knowledge
- agent tools
- sandbox image
- skills
- task history
- failure taxonomy
- verification artifacts
- routing/approval policy

이 가설은 후속 자료로 검증한다.
