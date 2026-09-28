# 1장 1차 Draft Review

기준일: 2026-09-28

대상:

- `chapters/01/plan.md`
- `chapters/01/draft.md`

## 판정

**REVISE MINOR**

Plan의 핵심 질문과 주장에는 잘 맞는다.

특히 다음은 유지한다.

- Coding Assistant → Coding Agent 전환을 제품 기능이 아니라 작업 방식으로 설명
- Model / Agent / Factory Capability 분리
- Review / CI / Integration으로 병목이 이동한다는 흐름
- Human Attention을 capacity로 보는 관점
- Microsoft와 METR의 상반된 생산성 연구를 함께 제시
- Accepted Change 중심의 metric 방향

다만 Draft 단계에서 다음을 수정한다.

---

## 1. 반복 축소

후반부의 다음 메시지가 여러 차례 반복된다.

- Agent가 빨라도 전체 Delivery가 빨라지는 것은 아니다.
- 병목은 downstream으로 이동한다.
- Agent보다 System을 봐야 한다.

핵심 메시지는 유지하되 결론부를 압축한다.

특히:

- `1.2`
- `1.5`
- `병목을 없애는 것이 아니라 관리한다`
- `이 장의 핵심 정리`

사이의 중복을 줄인다.

---

## 2. 연구 수치의 비교 범위 명확화

Microsoft 2025와 METR 2025는 서로 다른 조건이다.

본문에서 이미 이를 설명하고 있지만 다음을 더 명확히 한다.

Microsoft:

- 기업 환경 field experiment
- 4,867 developers
- 주로 당시 Coding Assistant workflow
- completed tasks 중심

METR:

- experienced OSS developers 16명
- familiar mature repositories
- early-2025 tools
- task completion time 중심

따라서:

> +26%와 -19%를 같은 productivity axis의 정반대 결과처럼 단순 비교하지 않는다.

두 자료의 목적은 AI가 빠른지 느린지 결론내리는 것이 아니라 **measurement boundary에 따라 결과가 달라진다는 점**을 보여주는 것이다.

---

## 3. Hypothetical Example 명시

`30 PR/day vs 8 review/day`는 설명을 위한 가상 예제다.

실제 산업 데이터처럼 읽히지 않도록 처음에:

> 단순한 가상 예를 들어보자.

라고 명시한다.

---

## 4. 영어 혼용 정리

다음처럼 한국어 문장 흐름을 우선한다.

권장:

- 리뷰(Review)
- 검증(Verification)
- 통합(Integration)
- 작업 주기(Cycle Time)

단, 다음 기술 용어는 영문을 유지해도 된다.

- Agent
- Task
- Worker
- Factory
- CI/CD
- Pull Request
- Repository
- Benchmark
- Token

같은 개념을 문단마다 한국어/영어로 번갈아 쓰지 않는다.

---

## 5. AI 문체 제거

다음 형태를 과도하게 반복하지 않는다.

- "중요한 점은"
- "이 차이는 생각보다 크다"
- "한 문장으로 줄이면"
- 문단마다 별도의 교훈 blockquote

Blockquote는 각 장의 정말 중요한 주장 2~4개 정도로 제한한다.

---

## 6. Chapter 1에서 Architecture를 앞당기지 않는다

현재 Draft는 Control Plane, Durable Task 스키마 등 뒤 장의 내용을 깊게 선행하지 않아 적절하다.

유지한다.

1장은 문제를 만들고 2장으로 넘기는 역할만 한다.

---

## 7. 참고 자료 형식

현재 말미의 참고 자료 목록은 유지 가능하다.

최종 원고 단계에서는 전체 책의 citation style을 통일한다.

Draft 단계에서는:

- 연구명
- 기관/저자
- 링크

정도로 충분하다.

---

# 수정 후 완료 기준

- 1장 Plan의 5개 절을 그대로 유지
- 전체 길이는 현재 대비 약 10~15% 축소 가능
- Microsoft/METR 연구 조건을 더 직접적으로 대비
- hypothetical throughput 예제를 명확히 표시
- 결론 반복 축소
- 2장으로 자연스럽게 연결
