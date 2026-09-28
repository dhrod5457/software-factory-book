# Manuscript Copyedit Pass

기준일: 2026-09-28

대상:

- `manuscript/book.md`

## 판정

**PASS**

## 수행한 편집

### 구조

- Part 7개 / Chapter 24개 / Epilogue 유지
- Book → Part → Chapter → Section heading hierarchy 정리
- 22장 Step A~H를 Baseline / Reliability / Scale / Autonomy 흐름으로 grouping
- 23장 Scenario를 Failure/Recovery, Parallel/Conflict 묶음으로 grouping

### 초반 밀도

- 1장: 11,025 → 약 7,200 chars
- 2장: 10,563 → 약 6,800 chars

삭제보다 중복 축소와 후속 장 cross-reference를 우선했다.

### 문체

- 반복 Transition heading 23개 제거
- `다음 장에서는` 형태의 동일 전환 문장 22개를 문맥형 전환으로 수정
- `중요한 것은`, `이 책에서는` 등 반복되는 문장 버릇 32곳 축소
- 정의 문장에 필요한 “이 책에서는”은 유지

### References

- Chapter별 참고자료는 원본 `chapters/*/draft.md`에 유지
- `manuscript/book.md`에서는 Chapter별 참고자료 제거
- 53개 고유 Reference를 단일 `# References`로 통합
- `manuscript/references.md` 별도 유지

### 용어

- `manuscript/terminology.md` 작성
- `manuscript/glossary.md` 작성 및 book 삽입
- 단순 전역 번역 대신 기술 용어의 의미 경계를 고정

### Layout

- Figure marker: 21
- Case Study marker: 14
- Figure plan: `manuscript/figures.md`
- Case Study plan: `manuscript/case-studies.md`

### Markdown Integrity

- Unclosed fence: 0
- Cross-type fence error: 0
- Chapter별 참고자료 섹션: 0
- `다음 장에서는` 잔여: 0
- Missing Chapter: 0

## 최종 상태

구조와 핵심 논지는 동결한다.

이후 허용 변경:

1. 오탈자 / 문장 교정
2. 출처 현재성 / 사실 오류 수정
3. Figure / Case Study / Caption 편집
4. 출판 형식 편집
