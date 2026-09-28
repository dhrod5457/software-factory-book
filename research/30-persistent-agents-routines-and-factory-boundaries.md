# Persistent Agents, Shared Computers, Routines, and Software Factory Boundaries

기준일: 2026-09-28

## 조사 대상

- Agent Conf 2026, Nick Miller, *Building a Software Factory with Cursor, xAI, and Grok Bot*
- 사용자 제공 발표 자막: `Building a Software Factory with Cursor, xAI, and Grok Bot - Nick Miller (iHmBg0N7EOA).txt`
- Cursor 공식 Grok Bot 문서
- Agent Conf 공식 Agenda

이 문서는 제품 소개를 본문에 그대로 옮기기 위한 자료가 아니다.

목적은 발표에서 드러난 Agent 운영 패턴을 현재 책의 Software Factory 경계와 비교해 재사용 가능한 설계 원칙으로 추상화하는 것이다.

---

## 1. Source Quality

### A급: 공식 제품 문서

- Cursor, Grok Bot
  - https://cursor.com/docs/grok-bot
- Cursor, Work with Grok Bot
  - https://cursor.com/docs/grok-bot/work
- Cursor, Routines
  - https://prod.cursor.com/help/grok-bot/routines
- Cursor, Grok Bot for Teams and Enterprise
  - https://cursor.com/docs/grok-bot/teams
- Cursor, Grok Bot Security
  - https://prod.cursor.com/docs/grok-bot/security

확인 가능한 내용:

- persistent cloud computer
- browser / filesystem / terminal
- 여러 Bot의 shared computer
- Bot별 context accumulation
- Bot 간 coordination과 task handoff
- schedule / event based routines
- workflow demonstration → skill
- approval / policy / isolation

### A급: 공식 행사 Agenda

- Agent Conf 2026 Agenda
  - https://www.agent.sh/agenda

확인 가능한 내용:

- 2026-09-17
- Nick Miller
- *Building a Software Factory with Cursor, xAI, and Grok Bot*
- Orchestration & Multi-Agent Systems 세션

### B급: 발표 자막

사용자 제공 TXT는 세션 내용의 구조와 사례를 파악하는 데 유용하다.

다만 자동자막에는 제품명이 Grokbot/Grockbot/Grabbot/Rockbot 등으로 흔들리고 일부 고유명사도 오인식 가능성이 있다.

따라서 다음은 공식 자료 재확인 없이 사실 근거로 사용하지 않는다.

- 제품명 세부 표기
- 조직/소속
- 출시일
- 사용자 수
- 생산성 배수
- 계약 절감액 등 정량 주장

---

## 2. 발표에서 반복되는 운영 모델

발표의 Bot 설계 설명은 크게 다음 세 요소로 요약된다.

~~~text
Context
Connectors
Outcomes
~~~

이 프레임은 이해하기 쉽지만 Software Factory에서는 통제와 검증을 추가해야 한다.

~~~text
Context
Capability / Connectors
Outcome
Guardrail
Evidence
~~~

### Context

Agent가 Work를 수행하기 위해 알아야 하는 정보.

- role
- project context
- preferences
- repository knowledge

### Capability / Connectors

Agent가 읽고 행동할 수 있는 Surface.

- API
- MCP
- Plugin
- Browser
- Shell
- filesystem

### Outcome

완료 상태.

단순 Activity가 아니라 무엇이 실제로 달성되어야 하는지 정의한다.

### Guardrail

금지된 행동과 Human Gate.

### Evidence

Outcome이 충족됐음을 검증하는 Artifact.

이 다섯 요소는 9장의 Prepared Harness와 12~13장의 Verification/Evidence를 연결하는 실전 Handoff Contract로 사용할 수 있다.

---

## 3. Persistence는 네 종류로 분리한다

Cursor 공식 문서는 Bot의 기억과 역할이 Session을 넘어 유지되고, Bot들이 persistent cloud computer의 file/browser state를 공유한다고 설명한다.

이를 Factory 관점에서 분해하면 다음과 같다.

~~~text
Persistent Agent
- memory
- role
- preference
- skill

Persistent Worker
- filesystem
- browser session
- installed tool
- cache

Durable Task
- status
- attempt
- approval
- verification
- evidence

Durable Execution
- event history
- checkpoint
- replay
- idempotent side effect
~~~

핵심:

> Persistent Agent나 Persistent Worker가 있다고 Durable Task와 Durable Execution이 자동으로 생기지 않는다.

이 구분은 15장의 기존 `Memory ≠ Durable Execution`을 확장한다.

---

## 4. Browser는 Integration Compatibility Layer다

공식 문서는 Plugin이 없더라도 Browser/Computer Use를 통해 Website를 사용할 수 있다고 설명한다.

Software Factory에서는 다음 우선순위가 적합하다.

~~~text
Structured API / MCP / Tool
        ↓
CLI
        ↓
Browser / Computer Use
        ↓
Human Handoff
~~~

Browser는 API가 없는 Legacy System까지 접근할 수 있는 범용 Surface다.

하지만 다음 특성이 있다.

- DOM/UI 변경
- session expiry
- automation blocking
- human-only step
- prompt injection surface
- 낮은 determinism

따라서 Browser는 stable machine contract의 대체가 아니라 마지막 Integration Gap을 메우는 Compatibility Layer로 보는 편이 안전하다.

---

## 5. Specialized Bot은 Task Independence를 보장하지 않는다

발표에서는 Frontend, QA, Documentation, Research 등 역할이 다른 Bot Team을 예로 든다.

공식 문서도 Bot 간 parallel work, message, handoff를 지원한다.

하지만 Factory 관점에서는 다음을 구분한다.

~~~text
Role Separation
≠
Task Independence
~~~

Role은 Agent가 잘하는 일이나 책임을 표현한다.

Parallel Scheduling의 조건은 Task의 dependency, file/schema overlap, independent acceptance다.

따라서 "Bot Team"을 그대로 Multi-Agent Factory의 근거로 사용하지 않는다.

17장의 기존 원칙인 "병렬화의 대상은 Agent가 아니라 독립 Task다"를 유지한다.

---

## 6. Agent Delegation과 Orchestration은 다르다

Bot A가 Bot B에 일을 부탁할 수 있는 것은 Coordination Capability다.

Factory의 Control Plane은 다음을 durable하게 관리해야 한다.

- dependency
- assignment
- timeout
- retry
- completion
- approval
- evidence

따라서:

~~~text
Agent-to-Agent Communication
≠ Durable Orchestration
~~~

A2A나 Bot messaging이 발전해도 Task State의 authoritative ownership 문제는 별도로 남는다.

---

## 7. Routine은 Trigger Layer다

Cursor Routines는 Schedule과 여러 외부 Event를 Trigger로 사용할 수 있다.

이 기능은 20장의 Event-driven Factory 사례로 적합하다.

하지만:

~~~text
Routine Trigger
≠ Durable Task
~~~

Factory 연결 시 추가로 필요하다.

- deduplication
- cooldown
- active-run conflict handling
- retry policy
- replay-safe side effect
- diagnosis vs fix classification
- acceptance policy

Event-driven은 Work 시작 방법이고 Autonomy는 Decision Authority의 범위다.

두 축을 합치지 않는다.

---

## 8. Agent Template을 조직 자산으로 본다

공유 가능한 Bot/Template/Skill 흐름에서 가져올 수 있는 일반 원칙은 Marketplace 자체가 아니다.

~~~text
Reusable Agent Configuration
=
Organizational Asset
~~~

Factory에서는 이를 Agent Execution Profile로 확장할 수 있다.

~~~text
Instruction
+ Skills
+ Tool / Connector Set
+ Worker Profile
+ Verification Profile
+ Permission Policy
+ Evidence Contract
~~~

이 Profile은 Platform Engineering의 Golden Path와 연결된다.

~~~text
Infrastructure Golden Path
+
Agent Execution Golden Path
~~~

---

## 9. Learned Skill은 Self-improvement Candidate다

Workflow Demonstration이나 Agent-generated Skill은 반복 Work를 줄일 수 있다.

하지만 Production Configuration 변경은 별도 승격 흐름이 필요하다.

~~~text
Observed Workflow
→ Candidate Skill
→ Eval
→ Review
→ Version
→ Shadow / Canary
→ Production
~~~

특히 Evaluator, Security Policy, Permission, Approval 변경은 일반 Skill보다 강한 Gate가 필요하다.

---

## 10. Operator Surface

발표와 제품에서 주목할 또 하나의 패턴은 복잡한 Runtime을 Message 중심 Surface 뒤에 숨긴다는 점이다.

Factory도 내부 Complexity를 사용자에게 그대로 노출할 필요는 없다.

Operator의 핵심 행동은 다음으로 줄일 수 있다.

~~~text
Create
Observe
Approve
Intervene
Inspect Evidence
~~~

단순한 UI는 상태를 숨기는 것이 아니라 다음 행동을 빠르게 결정할 수 있게 해야 한다.

- 무엇이 Running인가
- 무엇이 Blocked인가
- 무엇이 Human을 기다리는가
- 무엇이 변경됐는가
- 무엇으로 검증됐는가

Reference Factory의 UI/TUI/Dashboard 설계에 반영할 수 있다.

---

## 11. 본문에 사용하지 않을 주장

발표에는 제품 채택률, "10x" 효과, 개인 생산성·삶의 질 개선, 계약 절감액 등의 주장이 등장한다.

이 수치는 발표자의 제품/조직 경험이며 독립적으로 검증된 Software Factory 생산성 근거가 아니다.

따라서 19장의 Metric 원칙을 유지한다.

~~~text
Agent Activity
≠ Factory Throughput
≠ Business Outcome
~~~

본문에서는 다음을 우선한다.

- cycle time
- first-pass acceptance
- retry/rework
- human attention
- revert/escaped defect
- cost per accepted change

---

## 12. 반영 위치

- 9장: Context / Capability / Outcome / Guardrail / Evidence
- 15장: Persistent Agent / Worker / Task / Execution 분리
- 17장: Role Separation ≠ Task Independence
- 20장: Routine Trigger ≠ Durable Task
- 21장: Agent Execution Golden Path
- 23장: Operator Surface
- 24장: Candidate Skill promotion
- 19장: 홍보성 생산성 수치를 근거로 사용하지 않는 기존 원칙 유지

---

## 13. 최종 판단

이 사례의 가장 중요한 의미는 Multi-Agent의 존재가 아니다.

더 중요한 변화는 Agent가 일회성 Session에서 벗어나 지속되는 Identity와 Runtime을 갖고, 실제 업무 System과 연결되고, 반복 Workflow를 Skill과 Routine으로 축적한다는 점이다.

Software Factory는 이 Capability를 그대로 신뢰하는 시스템이 아니다.

~~~text
Persistent Agents
        +
Durable Work
        +
Controlled Capability
        +
Independent Verification
        +
Recoverable Execution
        =
Operational Software Production System
~~~

제품의 Convenience Layer와 Factory의 Reliability Layer를 구분하는 것이 이 사례에서 얻을 수 있는 가장 중요한 설계 교훈이다.
