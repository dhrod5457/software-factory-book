# Research Index

기준일: 2026-09-28

이 디렉터리는 **AI 시대 Software Factory** 책을 쓰기 위한 자료 수집 영역이다.

현재는 본문 작성 단계가 아니다.

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

## 읽는 순서

처음 전체 흐름을 볼 때:

1. `00-research-map.md`
2. `01-ai-software-factory-landscape-2026.md`
3. `02-factory-architecture-patterns.md`
4. `10-requirements-specification-and-task-planning.md`
5. `04-orchestration-task-state-and-continuity.md`
6. `03-harness-context-and-agent-legibility.md`
7. `05-verification-evidence-and-human-gates.md`
8. `06-security-isolation-and-permissions.md`
9. `07-observability-metrics-and-economics.md`
10. `08-autonomy-levels-and-self-improvement.md`
11. `09-evals-and-benchmark-limitations.md`
12. `12-engineering-role-and-operating-model.md`
13. `13-protocols-and-interoperability.md`
14. `11-product-and-open-source-landscape.md`
15. `30-workos-product-engineering-factory.md`
16. `sources.md`

## 현재 연구 구조

```text
Intent / Requirement
        ↓
Specification / Acceptance
        ↓
Task Planning / Dependency
        ↓
Durable Control Plane
        ↓
Worker Provisioning / Isolation
        ↓
Agent Harness
        ↓
Tools / Context / MCP
        ↓
Implementation
        ↓
Verification / Evaluator
        ↓
Evidence
        ↓
Policy / Human Gate
        ↓
Merge / Deploy
        ↓
Observability / Feedback
        ↺
```

보조 protocol layer:

```text
Agent ↔ Tools/Data : MCP
Agent ↔ Agent      : A2A
Agent ↔ IDE/Client : ACP
```

## 현재 반복해서 확인되는 패턴

아직 최종 결론은 아니지만 여러 독립 자료에서 반복되는 패턴:

- Agent Session보다 Durable Task가 중요해진다.
- Control Plane과 Execution Plane을 분리한다.
- Worker/Sandbox는 교체 가능해도 Task State는 유지되어야 한다.
- Repository와 실행 중 Application 모두 Agent가 읽을 수 있어야 한다.
- Context Window를 durable storage로 사용하지 않는다.
- deterministic verification을 가능한 한 먼저 사용한다.
- autonomy가 높을수록 isolation, policy, evidence 요구도 강해져야 한다.
- 사람의 역할은 모든 command 실행에서 intent, architecture, acceptance, exception 쪽으로 이동한다.
- Agent throughput이 증가하면 review/CI/verification이 다음 병목이 될 수 있다.
- Factory capability는 model capability와 동일하지 않다.
- requirement와 verification 사이의 traceability가 중요한 자산이 된다.
- self-improvement는 가능하지만 evaluator/policy까지 무제한으로 자기 수정하게 두면 위험하다.
- Sandbox + Coding Agent + PR 생성만으로는 Product Engineering Process 전체를 자동화했다고 보기 어렵다.
- Factory 성과는 PR/LOC 같은 output보다 accepted delivery, cycle time, defect/recovery 같은 outcome과 함께 봐야 한다.
- Task 실행에서 새로 얻은 지식은 현재 Plan과 Task Graph를 다시 평가하는 입력이 될 수 있다.

## Source Quality

### A급

- official engineering blog
- official docs/spec
- project repository
- research paper / benchmark primary source

### B급

- technical book
- independent analysis
- conference report

### C급

- community post
- newsletter
- personal blog

핵심 주장은 가능하면 A급 자료 두 개 이상에서 교차검증한다.

## 다음 Research 작업

자료의 양을 더 늘리는 것보다 다음 검증을 우선한다.

- 회사별 claim과 일반 원칙 분리
- 서로 반대되는 운영 모델 비교
- autonomy boundary 비교
- requirement → task → evidence traceability 구체화
- crash/retry/reassignment failure model 정리
- Factory-level eval scenario 정리
- 개발 조직에서 실제 적용 가능한 최소 Factory 정의 추출

`planning/concept.md`는 위 검증 후 만든다.


## 3차 추가 수집

반례와 운영 한계를 중심으로 다음 문서를 추가했다.

- `14-failure-modes-and-antipatterns.md`
  - test pass와 실제 완료의 차이
  - reward hacking
  - Lucky Pass
  - multi-agent coordination collapse
  - giant PR
  - security boundary failure
- `15-governance-provenance-and-agent-identity.md`
  - Agent identity
  - delegated authority
  - audit
  - artifact provenance
  - enterprise governance
- `16-productivity-evidence-and-measurement.md`
  - RCT / survey / production evidence
  - individual vs factory productivity
  - human attention
  - cost per accepted change
- `17-review-integration-and-throughput-bottlenecks.md`
  - review bottleneck
  - CI / integration capacity
  - stacked PR
  - WIP limit
- `18-research-contradictions-and-open-questions.md`
  - 서로 충돌하는 산업 운영 모델
  - 아직 결론 내리면 안 되는 질문


## 4차 추가 수집 - 경계와 Reliability Layer

이번 수집에서는 AI Software Factory와 인접 discipline의 경계를 집중 조사했다.

추가 문서:

- `19-boundaries-devops-platform-engineering-agent-platform.md`
  - CI/CD / DevOps / DevSecOps
  - Platform Engineering
  - Agent Platform / Runtime
  - Software Factory의 domain boundary
- `20-durable-execution-and-workflow-reliability.md`
  - durable execution
  - checkpoint / replay / retry
  - HITL wait
  - idempotency
  - crash/reassignment reliability
- `21-agent-ready-developer-platform-and-catalog.md`
  - Agent-ready Internal Developer Platform
  - Golden Path as machine contract
  - Software Catalog
  - Agent identity / quota
- `22-closed-loop-sdlc-and-production-feedback.md`
  - production signal
  - diagnosis
  - backlog generation
  - continuous feedback
  - product/factory improvement loop
- `23-minimum-viable-ai-software-factory.md`
  - Minimum Viable Factory
  - reliability before autonomy
  - staged adoption
  - single-worker factory starting point

이번 자료에서 특히 중요한 근거는 NIST NCCoE가 DevSecOps reference model 자체를 software factory 구성 관점으로 설명하고 있다는 점이다. AI Software Factory는 기존 SDLC/DevSecOps/Platform Engineering을 폐기하는 대체재라기보다 이 기반 위에서 AI Agent가 새로운 실행 주체로 들어가는 방향으로 검토한다.


## 5차 추가 수집 - 학술/실증 연구

제품 문서보다 논문과 실증 연구를 중심으로 다음 문서를 추가했다.

- `24-academic-foundations-of-agentic-software-engineering.md`
  - SWE-agent / Agentless / OpenHands
  - Requirement quality
  - runtime decomposition
  - repository exploration
- `25-human-agent-collaboration-and-responsibility-research.md`
  - 실제 PR lifecycle
  - initiative vs approval
  - steerability / verifiability
  - responsibility
- `26-orchestration-science-control-vs-autonomy.md`
  - deterministic vs LLM-controlled orchestration
  - hybrid control
  - recovery hierarchy
- `27-context-files-and-repository-governance-evidence.md`
  - AGENTS.md / CLAUDE.md empirical evidence
  - context file의 효과와 한계
  - repository governance
- `28-benchmark-science-and-evaluation-methodology.md`
  - SWE-Lancer / SWE-smith / SWE-rebench
  - exploration / dialogue / reasoning benchmark
  - process quality / cost
- `29-academic-synthesis-design-principles.md`
  - 지금까지의 산업+학술 자료에서 반복적으로 지지되는 설계 원칙

이번 학술 수집의 핵심은 **복잡한 Agent architecture와 높은 autonomy가 자동으로 더 좋은 결과를 만들지 않는다는 것**이다. Agentless와 deterministic orchestration 연구는 구조화 가능한 단계에서는 단순하고 deterministic한 시스템이 더 효율적일 수 있음을 보여주고, human-agent collaboration 연구는 실행 주도권과 최종 승인 권한을 독립적으로 설계해야 함을 보여준다.

## 6차 추가 수집 - Persistent Agent와 운영 Surface

Agent Conf 2026의 Nick Miller 세션과 Cursor 공식 Grok Bot 문서를 교차검증해 다음 문서를 추가했다.

- `30-persistent-agents-routines-and-factory-boundaries.md`
  - Persistent Agent / Persistent Worker / Durable Task / Durable Execution 분리
  - Context / Capability / Outcome / Guardrail / Evidence Handoff
  - Browser를 Integration Compatibility Layer로 보는 관점
  - Role Separation과 Task Independence 구분
  - Routine Trigger와 Durable Work의 차이
  - Agent Execution Golden Path
  - Learned Skill의 Candidate 승격
  - Operator Surface

이번 자료의 핵심은 Multi-Agent 자체가 아니라, 지속되는 Agent Identity와 Runtime이 등장해도 Factory의 authoritative Task State, Verification, Recovery, Governance는 별도로 필요하다는 점이다.

## 7차 추가 수집 - WorkOS Product Engineering Factory

추가 문서:

- `30-workos-product-engineering-factory.md`
  - PR 생성 자동화와 Software Factory의 경계
  - output metric과 outcome metric
  - Product brief/PRD에서 Task decomposition으로 이어지는 workflow
  - Continuous Planning Loop
  - MCP Context Engine / semantic gateway
  - Agent runtime 독립성
  - session friction 기반 self-improvement
  - authorization open problem

이번 자료의 핵심은 Software Factory의 자동화 단위를 코드 생성에 한정하지 않고 **Product Engineering Process 전체**로 확장한다는 점이다. 특히 Task 완료 후 새 지식을 반영해 Plan을 다시 평가하는 Continuous Planning Loop를 기존 Production Feedback Loop와 구분해 다룬다.

## 구현 사례 추가 - Simplest Software Factory

- `30-simplest-software-factory-case-study.md`
  - GitHub Issue → Dispatcher → Worker → PR → Human Review의 최소 구현
  - LLM 없는 deterministic dispatch
  - GitHub를 Human-facing control surface로 사용하는 패턴
  - Worker snapshot과 fresh task state 분리
  - Event integration의 dry-run / staged activation
  - multi-repository hub-and-spoke Factory
  - C급 tutorial source로 분류하며 일반 원칙의 단독 근거로 사용하지 않음
