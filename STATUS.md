# Current Phase

Phase 8 - Manuscript

상태: **RELEASE CANDIDATE RC2 — CONTENT REFRESH / RE-PROOF REQUIRED**

24개 본장과 Epilogue의 Draft 및 Phase 7 Review를 완료했다.

확인:

- `chapters/01..24/draft.md`
- `chapters/epilogue/draft.md`
- Part I~VII structural review
- Part I~VII line review
- Full Draft Structural Review
- Full Line Review
- 2026-09-28 Source Validation Snapshot
- Writing Style Guide Phase 7 규칙 반영

# Title

**AI Software Factory**

부제:

**코딩 에이전트를 소프트웨어 생산 시스템으로 운영하는 설계 원칙**

# Current Structure

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

24 Chapters + Epilogue.

# Phase 7 Result

판정:

**READY FOR MANUSCRIPT**

Review에서 완료한 항목:

1. 구조 중복 제거
2. 장간 책임 경계 정리
3. 주장 강도 조정
4. 최신 Source 재검증
5. Vendor 수치/기능의 범위 명시
6. Preprint / simulation / internal deployment 범위 명시
7. 책 자체 synthesis와 업계 표준 구분
8. Case Study와 일반 원칙 분리
9. 문체 Line Edit
10. Maturity / Autonomy / Self-improvement 과장 방지

상세:

- `review/full-line-review.md`
- `review/source-validation-2026-09-28.md`

# Source of Truth

1. `planning/concept.md`
2. `planning/scope.md`
3. `planning/toc.md`
4. `planning/writing-style.md`
5. 각 `chapters/NN/plan.md`
6. 각 `chapters/NN/draft.md`
7. `chapters/epilogue/draft.md`
8. `review/full-line-review.md`
9. `review/source-validation-2026-09-28.md`
10. `research/sources.md`

# Manuscript Progress

완료:

- `manuscript/book.md` 전체 조립
- Part 7개 / Chapter 24개 / Epilogue 검증
- `들어가며` 추가
- 목차 추가
- Heading hierarchy 정리
- Chapter transition heading 반복 제거
- 1·2장 압축 및 원본 Chapter 동기화
- 22·23장 section grouping 및 원본 Chapter 동기화
- `manuscript/references.md` — 55개 고유 Reference
- `manuscript/terminology.md`
- `manuscript/figures.md` — Figure 후보 21개
- `manuscript/case-studies.md` — Case Study Box 후보 15개
- `manuscript/length-balance.md`
- `manuscript/structural-flow-review.md`

완료 추가:

- Copyedit Pass 완료
- Markdown integrity check PASS
- Glossary 추가
- Chapter별 Reference 제거 → 55개 통합 References
- Figure marker 21개 실제 배치
- Case Study marker 15개 실제 배치
- Manuscript quality check PASS

완료 추가:

- Figure caption 21개 작성
- Case Study Box 15개 최종 working copy 작성
- 기계적 proof scan PASS

완료 추가:

- F01~F21 Mermaid Figure source 작성
- 21개 Figure를 book.md에 실제 삽입
- C01~C15 Case Study Box를 book.md에 실제 삽입
- Publication source recheck 완료
- Release Proof PASS — Warp content refresh 이전 snapshot
- RC1 snapshot 기록

완료 추가:

- 최종 RC 제목 / 부제 결정
- 기존 53개 Reference link audit PASS
- Warp 신규 Reference 2개 source URL 확인
- 기존 audit 기준 dead link 0

남은 Release Gate:

1. Warp content refresh 이후 manuscript proof / link check 재실행
2. SVG/PDF용 Figure export 및 흑백/축소 가독성
3. Reference publication metadata/style 최종화
4. 사람 기준 최종 교정
5. 최종 출판 산출물 build

# Next

```text
RC2
→ figure export / final proof / bibliography pass
→ publication build
→ release manuscript
```

구조와 핵심 논지는 더 이상 확장하지 않는다.
