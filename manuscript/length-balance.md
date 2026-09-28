# Chapter Length Balance

기준일: 2026-09-28

대상:

- `manuscript/book.md`

## 전체

24개 본장 평균:

- 약 6,696 characters / chapter

1·2장 압축 편집 후 재측정한 값이다.

분량 자체를 동일하게 맞추는 것이 목표는 아니다.

다음 기준으로 본다.

- 장의 역할에 비해 지나치게 긴가
- 짧지만 지나치게 많은 소절로 잘게 끊기는가
- 사례/연구가 본문 핵심보다 더 큰 비중을 차지하는가
- Diagram으로 바꾸면 줄일 수 있는 설명이 많은가

---

## 압축 완료

### 1장 — 7,228 chars

기존 11,025자에서 약 34% 축소.

수정:

- Agent/Factory 차이를 핵심 구조로 압축
- 30 PR/day와 cycle-time 예제 중복 축소
- Microsoft/METR 연구 조건은 유지하되 반복 설명 정리
- Metric 상세를 19장으로 이동

현재 분량:

- 평균 대비 약 +8%
- 추가 구조 축소 불필요

### 2장 — 6,808 chars

기존 10,563자에서 약 36% 축소.

수정:

- 7개 설계 속성을 개념 요약 + 후속 장 cross-reference 구조로 압축
- “Factory가 아닌 것” 사례 설명 축약
- 전체 Loop 설명 중복 제거

현재 분량:

- 평균과 거의 동일
- 추가 압축 불필요

---

## 현재 긴 장

### 12장 — 9,101 chars

긴 이유가 비교적 명확하다.

- Verification Pyramid
- Building to the Test
- Maintainer Acceptance
- Reward Hacking
- Lucky Pass

편집 방향:

- C06/C07/C08 Research Box로 사례 분리
- 본문 논리는 유지

삭제보다 layout 개선 대상.

---

### 16장 — 8,664 chars

Security / Identity / Governance를 한 장에 묶었기 때문에 자연스럽게 길다.

분할은 권장하지 않는다.

대신:

- C11 NIST Identity Box
- Microsoft Security 사례 Box
- F13 Delegation Figure

로 본문 호흡을 줄인다.

---

## 짧은 장

### 20장 — 4,928 chars

가장 짧다.

하지만 핵심 역할은 명확하다.

- Signal != Task
- event-driven != full autonomy
- closed-loop
- noise / oscillation

현재로도 독립 장 역할은 성립한다.

무리한 확장 불필요.

필요 시 F17과 C13으로 시각 밀도를 보강한다.

---

### 21장 — 5,546 chars

Platform boundary는 3장에서 이미 설명했다.

따라서 짧은 것이 오히려 적절하다.

Golden Path / Catalog / structured interface에만 집중 유지.

---

### 22장 — 5,521 chars / 15 sections

분량보다 **fragmentation**이 문제다.

Step A~H를 모두 H3로 두어 호흡이 너무 잘게 끊긴다.

편집 후보:

```text
1. Baseline
   - Repository
   - Worker
   - Evidence

2. Reliability
   - Durable State
   - Retry/Resume

3. Scale
   - Event Trigger
   - Parallel Worker

4. Autonomy
   - Risk-based Automation
```

즉 8개 Step은 유지하되 4개 상위 묶음으로 보이게 한다.

---

### 23장 — 5,624 chars / 14 sections

Scenario마다 별도 절이라 Reference Manual처럼 보일 수 있다.

편집 후보:

- Architecture / Data Model
- Failure Scenarios
- Parallel/Conflict Scenarios
- Acceptance Matrix

로 묶는다.

F20 Scenario Matrix와 함께 사용하면 본문을 더 자연스럽게 만들 수 있다.

---

## Code Block Density

특히 많은 장:

- 19장: 29 code fences
- 12장: 27
- 16장: 25
- 5장: 23
- 23장: 23
- 11장: 22
- 15장: 22

모든 text diagram을 코드블록으로 유지하지 않는다.

Figure로 승격할 항목은 `manuscript/figures.md` 기준으로 치환한다.

단순 1~2줄 표현은 prose 또는 표로 바꿀 수 있다.

---

## 결론

현재 장별 분량은 구조 변경이 필요할 정도로 불균형하지 않다.

완료:

1. 1장 압축
2. 2장 압축
3. 22장 section grouping
4. 23장 scenario grouping

남은 편집 대상:

1. 12장 Research Box / Figure 분리
2. 16장 Security Case Study Box 분리
3. 19장 text diagram 일부를 Figure로 대체
4. 20~21장의 짧은 분량은 현재 유지

내용 추가보다 **layout과 정보 계층 조정**을 우선한다.
