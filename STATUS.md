# Current Phase

Phase 3 - Scope 완료

Research 단계에서 산업 사례, 학술 연구, 실패 사례, 보안, 거버넌스, Platform/DevOps 경계, Benchmark/Eval 자료를 수집했다.

`planning/concept.md`에서 책의 최소 정의와 중심 원칙을 고정했고, `planning/scope.md`에서 핵심 본문·Advanced Topic·Future Topic·명시적 제외 범위를 확정했다.

# Working Title

**AI Software Factory**

최종 제목/부제는 아직 확정하지 않는다.

# Core Definition

> AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.

# Core Elements

```text
Durable Work
Delegated Execution
Controlled Autonomy
Independent Verification
Recoverability
Acceptance / Governance
Feedback
```

# Scope Guardrails

핵심 범위:

- Requirement / Task
- Durable Control Plane
- Worker / Sandbox
- Harness / Context / Tool
- Verification / Evidence
- Retry / Resume / Reassignment
- Security / Governance
- Observability / Metrics
- Review / Integration
- CI/CD / Platform Engineering 연결
- Minimum Viable Factory
- Maturity / Autonomy

최소 정의의 필수조건이 아닌 것:

- Multi-Agent
- Fully autonomous merge
- Automatic work selection
- Self-improvement
- Agent-generated requirements
- General-purpose Agent Platform

핵심 범위에서 제외:

- Foundation Model 학습
- Fine-tuning 튜토리얼
- Prompt Engineering 입문
- Agent Framework 종합 비교
- Kubernetes / DevOps 입문
- General-purpose Agent OS
- AI 조직 대체론

# Source of Truth

1. `planning/concept.md`
2. `planning/scope.md`
3. `planning/future-topics.md`
4. `research/29-academic-synthesis-design-principles.md`
5. `research/18-research-contradictions-and-open-questions.md`
6. `research/19-boundaries-devops-platform-engineering-agent-platform.md`
7. `research/14-failure-modes-and-antipatterns.md`
8. `research/sources.md`

# Next

Phase 4 - TOC

다음 문서를 작성한다.

`planning/toc.md`

목차 설계 방향:

```text
왜 필요한가
→ 무엇인가
→ Work를 어떻게 정의하는가
→ Agent가 어디서 일하는가
→ 어떻게 통제하는가
→ 어떻게 검증하는가
→ 실패하면 어떻게 하는가
→ 어떻게 확장하는가
→ 조직에서 어떻게 운영하는가
```

제품별 Part 구성은 피하고 원칙 중심으로 구성한다.
