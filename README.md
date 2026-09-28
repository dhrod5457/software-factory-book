# AI Software Factory

AI Coding Agent를 실제 소프트웨어 생산 시스템 안에서 어떻게 배치하고 운영할지 다루는 Software Engineering 책 프로젝트입니다.

현재 작업 제목은 **AI Software Factory**이며 최종 제목과 부제는 아직 확정하지 않았습니다.

## 중심 질문

> AI Agent에게 소프트웨어 작업을 위임하면서도, 작업 상태와 권한과 검증을 통제하고 실패를 복구하며 검증된 변경을 지속적으로 전달하려면 어떤 생산 시스템이 필요한가?

## 현재 정의

> AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.

## 현재 작업 단계

```text
Phase 1 Research       완료에 가까움
Phase 2 Concept        완료
Phase 3 Scope          완료
Phase 4 TOC            완료
Phase 5 Chapter Plan   완료
Phase 6 Draft          다음
Phase 7 Review
Phase 8 Manuscript
```

## 현재 Source of Truth

- `planning/concept.md`
- `planning/scope.md`
- `planning/toc.md`
- `chapters/README.md`
- `chapters/01..24/plan.md`
- `chapters/epilogue/plan.md`
- `PROJECT.md`
- `STATUS.md`

Research:

- `research/README.md`
- `research/00-research-map.md`
- `research/sources.md`

범위 밖 후속 주제:

- `planning/future-topics.md`

## 책의 구조

```text
Part I   Coding Agent에서 Software Factory로
Part II  Work를 정의하는 시스템
Part III Factory의 실행 구조
Part IV  결과를 믿을 수 있게 만드는 시스템
Part V   여러 Worker와 전체 Flow 관리
Part VI  조직의 Software Delivery System으로 확장
Part VII Minimum Viable Factory에서 Adaptive Factory까지
Epilogue Software Engineering에서 Software Production으로
```

총 24장 + Epilogue입니다.

## Draft 규칙

각 장은 해당 `plan.md`를 기준으로 `draft.md`를 작성합니다.

새로운 내용이 생기더라도 바로 범위를 넓히지 않고 먼저 `planning/scope.md`와 비교합니다.

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

다음 작업은 1장부터 Draft를 작성하는 것입니다.
