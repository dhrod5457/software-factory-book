# Manuscript Quality Check

기준일: 2026-09-28

대상:

- `manuscript/book.md`

## 판정

**WORKING MANUSCRIPT COMPLETE**

## 구조 검증

- Part: 7
- Chapter: 24
- Missing Chapter: 0
- Duplicate Chapter: 0
- Preface / 들어가며: 1
- Epilogue: 1
- Glossary: 1
- References: 1
- Unique Reference Entries: 53
- Figure Markers: 21
- Case Study Markers: 14

## 분량

- 약 170,000 characters
- 약 26,000 whitespace-delimited word-like tokens
- 약 11,000 lines

정확한 출판 페이지 수는 편집/도식/폰트/판형에 따라 달라지므로 여기서는 추정하지 않는다.

## 완료된 Manuscript Pass

1. Chapter Draft 전체 조립
2. Part / Chapter heading hierarchy 정리
3. 반복 Transition Heading 제거
4. Preface 추가
5. 1·2장 압축
6. 22·23장 section grouping
7. 53개 Reference 통합
8. Glossary 추가
9. Figure 21개 배치 지점 지정
10. Case Study 14개 배치 지점 지정
11. 장별 분량 분석
12. Chapter Source 동기화가 필요한 구조 변경 반영

## 출판 전 남은 작업

### Copyedit

- 한국어/영문 띄어쓰기
- 문장 호흡
- 표기 통일
- 오탈자
- 코드/도식 caption

### Figure Production

- `manuscript/figures.md`의 21개 후보 중 실제 제작 수 확정
- 중복 Figure 통합 가능성 검토
- 출판용 Caption 작성

### Case Study Box

- `manuscript/case-studies.md`의 14개 후보 중 실제 삽입 수 확정
- Vendor/Research condition을 Box 내부에 유지

### Publication-time Source Recheck

- Preview → GA
- Product/Feature 이름
- Protocol version
- Model 이름
- Vendor operational metric
- Preprint publication status
- NIST draft/final state

## Source of Truth

- 내용: `chapters/NN/draft.md`
- 조립/출판 편집: `manuscript/book.md`
- 용어: `manuscript/glossary.md`, `manuscript/terminology.md`
- References: `manuscript/references.md`
- Figure: `manuscript/figures.md`
- Case Study: `manuscript/case-studies.md`

## 다음 상태

책의 구조와 논지는 더 이상 확장하지 않는다.

이후 변경은 다음 세 종류만 허용한다.

1. 오류 수정
2. 근거/현재성 수정
3. 출판 편집
