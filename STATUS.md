# Current Phase

Phase 4 - TOC 완료

Research, Concept, Scope를 바탕으로 `planning/toc.md`를 작성했다.

목차는 제품별 구성이 아니라 AI Software Factory를 설계하는 사고 흐름을 따른다.

```text
왜 필요한가
→ 무엇인가
→ Work를 어떻게 정의하는가
→ Agent가 어디서 일하는가
→ 어떻게 통제하는가
→ 어떻게 검증하는가
→ 실패하면 어떻게 복구하는가
→ 여러 Worker를 어떻게 관리하는가
→ 기존 Delivery System과 어떻게 연결하는가
→ 작은 Factory부터 어떻게 확장하는가
```

# Working Title

**AI Software Factory**

최종 제목/부제는 아직 확정하지 않는다.

# TOC Structure

7 Parts + 24 Chapters + Epilogue

```text
Part I   Coding Agent에서 Software Factory로
Part II  Work를 정의하는 시스템
Part III Factory의 실행 구조
Part IV  결과를 믿을 수 있게 만드는 시스템
Part V   여러 Worker와 전체 Flow 관리
Part VI  조직의 Software Delivery System으로 확장
Part VII Minimum Viable Factory에서 Adaptive Factory까지
```

# Core Definition

> AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.

# Source of Truth

1. `planning/concept.md`
2. `planning/scope.md`
3. `planning/toc.md`
4. `planning/future-topics.md`
5. `research/29-academic-synthesis-design-principles.md`
6. `research/18-research-contradictions-and-open-questions.md`
7. `research/sources.md`

# Next

Phase 5 - Chapter Plan

각 장마다:

`chapters/NN/plan.md`

를 작성한다.

각 plan에 최소 포함:

- 장의 목적
- 독자가 답할 질문
- 핵심 주장
- 반드시 사용할 research source
- 반례
- 도식
- 실전 예제
- 포함/제외 경계
- 다음 장으로 연결

Draft는 Chapter Plan 이후 작성한다.
