# Writing Style Guide

기준일: 2026-09-28

이 문서는 `AI Software Factory` 본문 Draft의 공통 문체 기준이다.

1장 Draft를 기준으로 확정한 첫 번째 버전이며, 이후 Review 과정에서 수정할 수 있다.

---

# 1. 독자

주 독자는 실무 경험이 있는 Software Engineer / Tech Lead / Architect다.

기초 개념을 지나치게 풀어 설명하지 않는다.

하지만 Agentic Software Engineering의 새로운 개념은 기존 Software Engineering 개념과 연결해 설명한다.

---

# 2. 기본 문체

목표:

> 실무 개발자가 동료 개발자에게 설계 판단을 설명하는 문체.

사용:

- 짧고 명확한 문장
- 구체적인 개발 상황
- 작은 수치 예제
- 구조도
- trade-off
- 실패 사례

피함:

- 과도한 미래 예측
- 선언적인 AI 찬양
- 마케팅 문구
- 필요 없는 형용사
- 문단 끝마다 교훈을 붙이는 방식

---

# 3. 한국어와 영어

한국어 문장을 기본으로 한다.

기술적으로 널리 쓰이는 다음 용어는 영문을 허용한다.

- Agent
- Task
- Worker
- Factory
- Harness
- Sandbox
- CI/CD
- Pull Request
- Repository
- Benchmark
- Token
- API
- MCP

한국어가 더 자연스러운 경우 한국어를 우선한다.

예:

- 검증
- 리뷰
- 통합
- 실행환경
- 작업 상태
- 복구
- 승인
- 권한

같은 개념을 한 장 안에서 여러 표기로 바꾸지 않는다.

---

# 4. 주장 순서

가능하면 다음 순서를 사용한다.

```text
문제
→ 실제 예
→ 왜 기존 방식으로 부족한가
→ 설계 원칙
→ 반례 / 한계
→ 다음 단계
```

먼저 원칙을 선언하고 뒤에서 사례를 억지로 붙이지 않는다.

---

# 5. 숫자와 연구

숫자는 장식으로 사용하지 않는다.

항상 다음 맥락을 함께 적는다.

- 시점
- 대상
- Task
- 측정 지표
- 연구 한계

다른 연구의 수치를 직접 비교할 때 실험 조건이 같은지 확인한다.

Vendor 자체 수치는:

> 회사가 공개한 운영 사례

로 표현하고 업계 일반 수치로 확장하지 않는다.

Preprint는 확정된 일반 사실처럼 표현하지 않는다.

---

# 6. 제품 사례

제품 이름이 Chapter의 주어가 되지 않게 한다.

Bad:

> OpenAI는 이렇게 한다. WorkOS는 이렇게 한다. Stripe는 이렇게 한다.

Better:

> Durable Task가 필요한 이유를 설명한 뒤 Symphony와 Horizon을 서로 다른 구현 사례로 사용한다.

제품이 사라져도 본문 논리는 유지되어야 한다.

---

# 7. Blockquote

핵심 주장을 강조할 때만 사용한다.

한 절마다 반복하지 않는다.

장 전체에서 2~4개 정도가 기본이다.

---

# 8. 목록

본문을 목록만으로 채우지 않는다.

목록은 다음에 적합하다.

- 상태
- 비교 기준
- 구성요소
- 체크 항목

논리와 주장은 prose로 설명한다.

---

# 9. 도식

ASCII/Text diagram은 실제 사고 구조가 있을 때 사용한다.

좋은 예:

```text
Task
→ Worker
→ Verification
→ Evidence
```

단순 문장을 화살표로 바꾼 장식용 도식은 피한다.

---

# 10. 반복

같은 결론을:

- 절 끝
- 장 끝
- 핵심 정리

에서 세 번 반복하지 않는다.

장 결론에서는 새로운 주장보다 앞에서 설명한 내용을 짧게 수렴한다.

---

# 11. 용어 도입

새로운 핵심 용어는 처음 등장할 때 정의한다.

예:

> 이 책에서는 Prompt보다 오래 살아남으며 상태·검증·이력을 가진 작업 단위를 Durable Task라고 부른다.

이후에는 반복 정의하지 않는다.

---

# 12. 불확실성 표현

근거가 충분하면 모호하게 쓰지 않는다.

Bad:

> 중요할 수도 있다.

Better:

> 이 연구에서는 X가 관찰됐다.

근거가 약하면 범위를 명확히 제한한다.

> 현재 공개 사례만으로 업계 일반 원칙이라고 단정하기는 어렵다.

---

# 13. 금지에 가까운 표현

가급적 쓰지 않는다.

- 혁명적
- 게임 체인저
- 완전히 새로운 시대
- 압도적
- 반드시 사라진다
- 인간을 대체한다
- 무조건
- 모든 개발 조직

---

# 14. Chapter 시작

가능하면 현실적인 개발 상황이나 질문에서 시작한다.

긴 정의나 역사부터 시작하지 않는다.

---

# 15. Chapter 종료

다음 장에서 필요한 질문을 남긴다.

예:

> 그렇다면 이런 생산 시스템을 어디까지 갖춰야 Software Factory라고 부를 수 있을까?

이 질문이 다음 장 첫 부분과 연결되도록 한다.


---

# 16. 책에서 제안한 개념과 외부 표준을 구분한다

책이 설명을 위해 만든 이름이나 Metric은 처음 등장할 때 성격을 밝힌다.

예:

> 이 책에서는 이 결과 형식을 Evidence Contract라고 부른다.

> Cost per Accepted Change는 업계 표준 Metric이 아니라 Factory 수준의 측정 경계를 설명하기 위한 후보 지표다.

특히 다음은 현재 책 자체의 synthesis / taxonomy다.

- Evidence Contract
- Failure Fingerprint
- Cost per Accepted Change
- Human Attention per Accepted Change
- M0~M5 Factory Maturity
- Reference Factory Acceptance Suite

외부 표준처럼 표현하지 않는다.

---

# 17. Vendor 사례와 일반 원칙 사이에 문장 하나를 둔다

Vendor 내부 데이터는 다음 순서로 쓴다.

```text
관찰된 사실
→ 실험/운영 조건
→ 일반화 한계
→ 책에서 가져올 설계 원칙
```

Bad:

> Agent는 3~5개 이상 관리할 수 없다.

Better:

> OpenAI의 한 내부 사례에서는 3~5개 interactive session 이후 관리 부담이 커졌다고 보고했다. 업계 일반 한계가 아니라 Human Attention이 capacity가 될 수 있음을 보여주는 사례다.

---

# 18. Preprint와 실험 환경을 숨기지 않는다

Preprint는 가능하면 본문에서 바로 표시한다.

- preprint
- controlled simulation
- vendor internal deployment
- sampled production trace
- small workload

같은 범위를 독자가 참고 자료까지 내려가지 않아도 알 수 있게 적는다.

숫자를 쓸 때 특히 중요하다.

---

# 19. 현재 제품 상태와 오래 유지될 원칙을 분리한다

다음은 출간 직전 재검증 대상이다.

- preview / GA 상태
- model 이름
- protocol version
- product limit
- pricing
- current feature name

본문의 핵심 논리는 이 값이 바뀌어도 유지되게 작성한다.

제품 상태를 설명할 때 기준 날짜를 붙인다.
