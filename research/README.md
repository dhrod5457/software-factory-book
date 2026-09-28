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
15. `sources.md`

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
