# 프로젝트 목적

작업 제목:

**AI Software Factory**

AI Coding Agent를 개인 개발 보조도구가 아니라 반복 가능한 소프트웨어 생산 시스템의 Worker로 배치하는 방법을 다루는 Software Engineering 책을 작성한다.

특정 AI 제품의 사용 설명서가 아니다.

## 중심 질문

> AI Agent에게 소프트웨어 작업을 위임하면서도, 작업 상태와 권한과 검증을 통제하고 실패를 복구하며 검증된 변경을 지속적으로 전달하려면 어떤 생산 시스템이 필요한가?

## 핵심 정의

> AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.

## 현재 핵심 모델

```text
Intent / Signal
→ Requirement / Specification
→ Task / Acceptance
→ Durable Control Plane
→ Controlled Orchestration
→ Worker / Sandbox
→ AI Agent + Context + Tools
→ Implementation
→ Independent Verification
→ Evidence
→ Acceptance / Governance
→ Delivery
→ Feedback
↺
```

## 핵심 원칙

1. Model Capability와 Factory Capability를 분리한다.
2. Prompt보다 Durable Task를 중심에 둔다.
3. Requirement와 Acceptance를 구현보다 먼저 명확히 한다.
4. 정형화 가능한 규칙은 시스템이 강제한다.
5. 불확실한 탐색과 판단에 Agent autonomy를 사용한다.
6. Agent self-report와 완료 판정을 분리한다.
7. Verification은 실행 루프 내부에 둔다.
8. Context Window를 durable state로 사용하지 않는다.
9. Worker는 잃을 수 있어도 Task는 잃지 않는다.
10. 병렬화의 대상은 Agent가 아니라 독립 Task다.
11. Execution Authority와 Acceptance Authority를 분리한다.
12. Autonomy가 높을수록 Isolation과 Evidence를 강화한다.
13. Factory의 성능은 Accepted Change 중심으로 본다.
14. Review / CI / Integration 병목도 Factory의 일부로 본다.
15. Factory 자체의 변경도 versioning하고 검증한다.

## 현재 진행 상태

```text
Phase 1 Research
완료에 가까운 상태

Phase 2 Concept
완료
- planning/concept.md

Phase 3 Scope
완료
- planning/scope.md
- planning/future-topics.md

Phase 4 TOC
완료
- planning/toc.md

Phase 5 Chapter Plan
완료
- chapters/01..24/plan.md
- chapters/epilogue/plan.md
- chapters/README.md

Next
Phase 6 Draft
→ chapters/NN/draft.md
```

## Chapter Plan 원칙

각 Plan은 Draft의 Source of Truth다.

필수 항목:

- 장의 목표
- 독자가 답할 질문
- 핵심 주장
- Research 근거
- 반례
- 도식
- 실전 예제
- 포함/제외 경계
- 다음 장 연결

## Source of Truth

현재 우선순위:

1. `planning/concept.md`
2. `planning/scope.md`
3. `planning/toc.md`
4. `chapters/README.md`
5. 각 `chapters/NN/plan.md`
6. `planning/future-topics.md`
7. `research/29-academic-synthesis-design-principles.md`
8. `research/sources.md`

## 작성 방식

`cloud-agent-book`의 작업 흐름을 참고한다.

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

현재는 Chapter Plan을 완료했고 Draft 단계로 넘어간다.
