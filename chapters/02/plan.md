# 02장 설계 - AI Software Factory란 무엇인가

## 장의 목표

책 전체에서 사용할 정의와 최소 구성요소를 확정한다. Multi-Agent, 완전 자율화, CI/CD+LLM 같은 좁은 정의를 배제하고 Durable Work, Delegated Execution, Verification, Recovery, Governance, Feedback을 중심에 둔다.

이 장의 핵심 질문:

> AI Software Factory를 Coding Agent Farm과 무엇으로 구분할 것인가?

> Factory라고 부르기 위한 최소 구성요소는 무엇인가?

---

## 핵심 주장

> AI Software Factory의 핵심은 Agent 수가 아니라 Durable Work와 검증 가능한 생산 흐름이다.

> Multi-Agent, 자동 Task 선택, 완전 자율 Merge, Self-improvement는 최소 정의의 필수조건이 아니다.

---

## 독자가 얻는 것

- 책에서 사용할 AI Software Factory 정의를 설명할 수 있다.
- 최소 7개 구성요소를 설명할 수 있다.
- Coding Agent Farm, CI/CD, Agent Platform과 개념적으로 구분할 수 있다.
- 왜 실패와 복구가 Factory 정의에 포함되는지 이해한다.

---

## 반드시 사용할 Research
- `research/30-workos-product-engineering-factory.md`

- `research/00-research-map.md`
- `research/02-factory-architecture-patterns.md`
- `research/18-research-contradictions-and-open-questions.md`
- `research/19-boundaries-devops-platform-engineering-agent-platform.md`
- `research/23-minimum-viable-ai-software-factory.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Software Factory = Multi-Agent라는 정의
- Software Factory = CI/CD에 LLM을 붙인 것이라는 정의
- Fully Autonomous Organization을 최소 조건으로 보는 주장
- 특정 vendor architecture를 일반 정의로 채택하는 오류

---

# 절 구성

## 02.1 왜 다시 Factory라는 표현인가

Traditional Software Factory 역사는 짧게만 언급하고, 반복 가능하고 표준화된 생산 시스템이라는 의미가 AI Agent 시대에 왜 다시 중요해졌는지 연결한다.

## 02.2 책의 최소 정의

planning/concept.md의 정의를 제시하고 durable하게 관리되는 Work, delegated execution, independent verification이 왜 들어가는지 설명한다.

## 02.3 일곱 개 핵심 구성요소

Durable Work, Delegated Execution, Controlled Autonomy, Independent Verification, Recoverability, Acceptance/Governance, Feedback을 각각 한 단락으로 소개한다.

## 02.4 Factory가 아닌 것

Multi-Agent System, Agent Framework, Coding Agent Farm, CI/CD with LLM을 비교해 경계를 선명하게 한다.

## 02.5 Broad Loop

Intent → Requirement → Task → Execute → Verify → Deliver → Feedback 전체를 보여주되 각 요소는 뒤 장에서 깊게 다룬다고 안내한다.


---

## 필요한 구조 / 그림

1. AI Software Factory reference loop
2. 최소 7개 구성요소 원형 또는 계층도
3. Agent / Harness / Runtime / Factory의 포함·사용 관계

---

## 실전 예제 / 실험

- Human이 Task를 선택하고 단일 Worker가 실행하며 deterministic verification과 human review로 끝나는 Minimum Viable Factory
- 여러 Agent를 띄웠지만 Task state와 verification이 없는 Coding Agent Farm 비교

---

## 본문에서 의도적으로 다루지 않을 내용

- 각 구성요소의 구현 상세
- 자율성 maturity 세부 taxonomy
- 장기 역사 서술

---

## 앞뒤 장 연결

3장에서는 정의를 기존 CI/CD, DevOps, Platform Engineering, Agent Platform과 비교해 개념적 경계를 확정한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
