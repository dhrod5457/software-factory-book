# Manuscript Structural Flow Review

기준일: 2026-09-28

대상:

- `manuscript/book.md`

## 판정

**PASS**

조립본 기준으로 다음을 확인했다.

- Part 7개
- Chapter 24개
- Chapter 번호 중복 없음
- Epilogue 1개
- Book → Part → Chapter → Section heading hierarchy 정리
- 목차 삽입
- 반복되는 `다음 질문` / `이 장에서 남는 질문` 소제목 23개 제거
- 장간 전환 문장은 유지

## 구조

```text
Book
├─ Part I
│  ├─ Chapter 1
│  ├─ Chapter 2
│  └─ Chapter 3
├─ Part II
│  └─ ...
├─ ...
├─ Part VII
│  └─ Chapter 24
└─ Epilogue
```

## Manuscript-level 결정

### 유지

- 각 장 말미의 다음 장 연결 문장
- Chapter별 참고 자료
- Part 단위 구조
- 장별 실제 사례와 반례

### 제거 / 정리

- 반복되는 전환용 소제목
- Part와 Chapter가 같은 heading level이던 조립 흔적

## 다음 Pass

1. 용어 통일
2. Reference 형식 통일
3. Figure 후보 추출
4. Case Study Box 분리
5. Preface / Introduction 검토
6. 장별 분량 균형
