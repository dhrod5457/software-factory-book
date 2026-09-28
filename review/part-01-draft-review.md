# Part I Draft Review

기준일: 2026-09-28

대상:

- `chapters/01/draft.md`
- `chapters/02/draft.md`
- `chapters/03/draft.md`

## 판정

**PASS WITH MINOR FOLLOW-UP**

Part I의 역할 분담은 명확하다.

```text
1장
왜 Coding Agent만으로는 부족한가

2장
그렇다면 AI Software Factory란 무엇인가

3장
기존 CI/CD / DevOps / Platform / Agent Platform과 어디가 다른가
```

초고 단계에서 Part II로 넘어가도 된다.

---

## 1장 역할

핵심:

- 병목 이동
- Human Attention
- 생산성 측정 경계
- Model / Agent / Factory Capability 분리

2장 architecture 정의를 선행하지 않고 문제를 충분히 만든다.

1차 Review 후 반복을 줄이고 Microsoft/METR 연구 조건을 명확히 수정했다.

현재 상태:

**READY FOR LATER LINE EDIT**

---

## 2장 역할

핵심:

- 최소 정의
- 7개 구성요소
- Factory가 아닌 것
- Broad Loop

좋은 점:

- Multi-Agent를 필수조건에서 제거
- Fully Autonomous Merge를 필수조건에서 제거
- Minimum Viable Factory 예제로 정의를 검증
- Recoverability를 핵심 정의에 포함

후속 line edit 후보:

- 7개 구성요소 구간이 목록처럼 느껴지지 않도록 Draft Review 단계에서 장면/예시를 조금 더 연결할 수 있음
- CI/CD 경계 설명은 3장과 겹치므로 최종 편집 시 현재보다 더 축약 가능

현재 상태:

**READY FOR PART II**

---

## 3장 역할

핵심:

- 기존 Delivery System과의 경계
- Build vs Buy 경계
- Platform을 Factory의 기반으로 사용
- Agent Platform과 Software Delivery Domain 구분

좋은 점:

- 기존 시스템을 폐기한다는 서사를 피함
- Platform API / Golden Path를 Agent가 사용하는 그림이 명확함
- Agent Runtime과 Factory를 단순 포함관계로 만들지 않음

후속 line edit 후보:

- 21장 Platform Engineering 심화 내용과 겹치지 않도록 3장은 경계까지만 유지
- Software Catalog 상세는 21장으로 넘김

현재 상태:

**READY FOR PART II**

---

# Part I 전체에서 유지할 문장 역할

## 1장

> Agent가 빨라질수록 전체 Delivery System을 봐야 한다.

## 2장

> Factory의 핵심은 Agent 수가 아니라 Durable Work와 검증 가능한 흐름이다.

## 3장

> Factory는 기존 CI/CD와 Platform을 대체하지 않고 사용한다.

세 문장이 서로 다른 역할을 하므로 이후 Draft에서도 이 경계를 유지한다.

---

# Part II 진입 조건

충족:

- 문제 정의 완료
- 핵심 Definition 완료
- 인접 개념 Boundary 완료
- Writing Style 확정
- Research source 충분

다음:

`4장 Requirement / Acceptance`
→ `5장 Durable Task`
→ `6장 Task Decomposition / Dependency`
