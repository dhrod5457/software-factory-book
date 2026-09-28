# Source Validation Snapshot

기준일: 2026-09-28

이 문서는 Phase 7에서 최신성 또는 Claim Strength가 중요한 자료를 다시 확인한 기록이다.

## Current / primary sources rechecked

### OpenAI
- Harness Engineering
- Symphony
- internal coding-agent misalignment monitoring

확인 용도:
- harness / agent legibility
- human attention / orchestration
- reward hacking context

### Microsoft Research / Security
- developer field experiments
- Building to the Test
- AgentLens
- Agentic Coding in the Wild
- Semantic Kernel agent-framework vulnerabilities
- Claude Code GitHub Action case
- Durable Task for AI Agents

확인 용도:
- productivity
- verification failure
- trajectory quality
- production-scale workload
- tool security boundary
- durable execution

### METR
- experienced OSS developer RCT
- maintainer review of SWE-bench-passing patches

확인 용도:
- productivity measurement
- automated grader vs maintainer acceptance

### Anthropic
- Managed Agents
- emerging multiagent systems
- Agent Skills

확인 용도:
- session/harness/sandbox boundary
- coordination / conformity / resource contention
- skill/self-improvement direction

### NIST NCCoE
- DevSecOps live reference model
- Software and AI Agent Identity and Authorization concept paper

확인 용도:
- existing SDLC boundary
- identity / authorization / auditing direction

### GitHub
- Spec Kit
- Copilot Code Review tool regression
- Stacked Pull Requests
- giant AI PR → reviewable stack
- coding agent efficiency

확인 용도:
- specification workflow
- harness regression
- reviewability
- token vs task efficiency

### Caylent / DevBench
- What is a Software Factory
- DevBench public architecture
- DevBench execution modes

확인 용도:
- software factory / harness framing
- specification + architecture → backlog → factory input
- execution loop and review gates
- changes-manifest scope conformance
- security review

주의:
- 영상 자막은 자동 전사 오류 가능성이 있어 고유명사와 구현 세부는 공개 DevBench 저장소로 교차 확인
- "completely automated" 같은 표현은 Caylent의 사례 설명으로만 사용하고 책의 일반 정의로 승격하지 않음

### Google
- Jules proactive updates
- Agent Executor

확인 용도:
- event-driven work source
- durable execution runtime

### Warp / Zach Lloyd
- *Software Engineering Is Becoming Factory Engineering* — AI Engineer World's Fair 2026 talk
- *Adopting the software factory model: crawl, walk, run* — Warp, 2026-09-15

확인 용도:
- idea / issue intake와 triage
- product specification / technical specification
- implementation / review / verification / monitoring loop
- computer-use 기반 behavioral evidence
- human time / token time을 포함한 factory efficiency
- observer / skill improvement loop
- factory engineer / meta-engineering framing

Claim strength:
- 발표의 구조와 용어는 Zach Lloyd / Warp의 thesis와 운영 사례로 attribution한다.
- “모든 프로젝트가 Software Factory를 갖게 된다” 같은 미래 전망은 일반 사실로 쓰지 않는다.
- Warp 운영 수치와 제품 효과는 vendor claim으로 취급한다.
- 이 책의 Evidence Contract, Accepted Change, guarded self-improvement는 Warp가 정의한 업계 표준이 아니라 책의 synthesis로 유지한다.

### DORA / CNCF / Backstage
- 2025 DORA report and platform capability
- CNCF agentic platform discussion
- Backstage AI Catalog

확인 용도:
- system-level delivery
- platform boundary
- agent as platform consumer
- software/AI catalog

## Publication-time recheck list

다음은 최종 출판 직전에 반드시 다시 확인한다.

- preview → GA 여부
- Model 이름
- protocol version
- product feature name
- current API limitation
- company-reported operational metrics
- preprint의 peer-reviewed publication 여부
- NIST draft → final/project outcome 변화

책의 핵심 원칙은 이 정보가 바뀌어도 유지되도록 작성한다.
