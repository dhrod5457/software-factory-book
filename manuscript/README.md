# Manuscript

이 디렉터리는 Phase 8 원고 조립과 manuscript-level 편집을 위한 공간이다.

## 현재 파일

- `book.md` — 24개 본장 + Epilogue 전체 조립본
- `edit-plan.md` — manuscript 단계 편집 순서와 완료 기준

## 조립 상태

검증 완료:

- Part I~VII 모두 존재
- Chapter 1~24 모두 존재
- Chapter 번호 중복 없음
- Epilogue 존재
- 상단 목차 추가

## Source of Truth

현재 원본 본문은 각 Chapter Draft다.

```text
chapters/NN/draft.md
        ↓
manuscript/book.md
```

Manuscript 단계에서 구조적 편집이 발생하면 최종적으로 Chapter Source와 동기화한다.

## Phase 8 원칙

Manuscript 단계에서는 새로운 핵심 주제를 추가하지 않는다.

우선순위:

1. 장간 연결
2. 중복 제거
3. 용어 통일
4. 제목/소제목 호흡
5. Reference 형식
6. Figure/Box 위치
7. 전체 분량 균형
8. Front matter
9. Publication-time source recheck

새로운 연구가 꼭 필요하면 `research/`에 먼저 기록한다.
