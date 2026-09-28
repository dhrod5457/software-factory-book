# Manuscript

이 디렉터리는 Phase 8 원고 조립과 manuscript-level 편집을 위한 공간이다.

## 현재 파일

- `book.md` — 24개 본장 + Epilogue + 들어가며 전체 조립본
- `preface.md` — 들어가며 Source
- `edit-plan.md` — manuscript 단계 편집 순서
- `structural-flow-review.md` — 조립 구조 검토
- `terminology.md` — canonical terminology
- `references.md` — 중복 제거 Reference 53개
- `figures.md` — 출판용 Figure 후보
- `case-studies.md` — Case Study Box 계획
- `case-study-boxes.md` — Case Study Box working copy 14개
- `figure-captions.md` — Figure caption 21개
- `length-balance.md` — 장별 분량 분석

## 조립 상태

검증 완료:

- Part I~VII 모두 존재
- Chapter 1~24 모두 존재
- Chapter 번호 중복 없음
- Epilogue 존재
- 들어가며 존재
- 목차 존재
- Part → Chapter → Section heading hierarchy 정리

## Manuscript 편집 완료 항목

- 반복되는 `다음 질문` 소제목 제거
- 1장 11,025 → 7,228 chars 압축
- 2장 10,563 → 6,808 chars 압축
- 22장 Step A~H를 4개 상위 구조로 grouping
- 23장 Scenario를 Failure/Recovery, Parallel/Conflict로 grouping
- Figure 후보 21개 선정
- Case Study Box 후보 14개 선정

## Source of Truth

Chapter 내용의 원본은 각 `chapters/NN/draft.md`다.

```text
chapters/NN/draft.md
        ↓
manuscript/book.md
```

Manuscript에서 구조 자체를 바꾼 1·2·22·23장은 Chapter Source에 동기화했다.

## 완료된 Phase 8 작업

- 전체 manuscript assembly
- structural flow edit
- Chapter 1·2 압축
- Chapter 22·23 grouping
- 통합 References 53개
- Glossary
- Figure marker 21개
- Case Study marker 14개
- Copyedit Pass
- Markdown integrity check

## 남은 작업

1. 실제 Figure 아트워크 제작
2. Figure / Case Study 최종 삽입·레이아웃
3. 출간 직전 source recheck
4. 최종 release proof

새로운 핵심 주제는 추가하지 않는다.

현재 구조와 핵심 논지는 동결한다.
