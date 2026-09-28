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

Phase 3 Scope
완료

Phase 4 TOC
완료

Phase 5 Chapter Plan
완료

Phase 6 Draft
완료
- chapters/01..24/draft.md
- chapters/epilogue/draft.md

Current
Phase 7 Review
- review/part-01..07-draft-review.md
- review/full-draft-structural-review.md

Next
Phase 8 Manuscript
```

## Draft Completion

확인 완료:

- 24개 본장 Draft
- Epilogue Draft
- Writing Style Guide
- Part별 Draft Review
- Full Draft Structural Review

## Review 기준

- 중복 제거
- 장간 역할 분리
- 연구 주장 강도 조정
- 최신 출처 재검증
- Vendor 사례와 일반 원칙 구분
- 용어 통일
- 도식 보강
- 문체 Line Edit

## Source of Truth

1. `planning/concept.md`
2. `planning/scope.md`
3. `planning/toc.md`
4. 각 `chapters/NN/plan.md`
5. 각 `chapters/NN/draft.md`
6. `chapters/epilogue/draft.md`
7. `planning/writing-style.md`
8. `review/full-draft-structural-review.md`
9. `research/sources.md`

## 작성 방식

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

현재는 Draft를 완료했고 Review 단계다.
