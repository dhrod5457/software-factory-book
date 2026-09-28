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

### Google
- Jules proactive updates
- Agent Executor

확인 용도:
- event-driven work source
- durable execution runtime

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
