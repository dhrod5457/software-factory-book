# 04장 설계 - Prompt가 아니라 Requirement와 Acceptance에서 시작한다

## 장의 목표

Coding Agent에게 곧바로 Issue 문장을 던지는 대신 Intent를 실행 가능한 Requirement와 Acceptance Criteria로 바꾸는 이유와 방법을 다룬다.

이 장의 핵심 질문:

> Agent에게 일을 맡기기 전에 무엇이 명확해야 하는가?

> Requirement 작성 권한과 Acceptance 권한을 어떻게 분리할 것인가?

---

## 핵심 주장

> Requirement 품질은 Agent execution quality의 입력 변수이자 상한이다.

> 좋은 Factory는 Requirement와 Verification 사이의 traceability를 만든다.

> Agent가 Requirement를 작성할 수 있어도 Product Intent와 Acceptance Authority까지 자동으로 갖는 것은 아니다.

---

## 독자가 얻는 것

- Prompt와 durable specification의 차이를 설명할 수 있다.
- Acceptance Criteria를 Task 실행 전 contract로 사용할 수 있다.
- Requirements-first와 Design-first를 상황에 맞게 선택할 수 있다.
- Requirement → Task → Verification traceability를 설계할 수 있다.

---

## 반드시 사용할 Research
- `research/30-workos-product-engineering-factory.md`

- `research/10-requirements-specification-and-task-planning.md`
- `research/24-academic-foundations-of-agentic-software-engineering.md`
- `research/25-human-agent-collaboration-and-responsibility-research.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Issue 문장 하나를 곧바로 구현 prompt로 사용하는 패턴
- Agent가 Requirement와 Test를 동시에 만들어 같은 오해를 공유하는 위험
- 모든 작은 Task에 무거운 spec process를 강제하는 과잉 절차

---

# 절 구성

## 04.1 Prompt만으로 큰 Work를 관리하기 어려운 이유

hidden assumption, acceptance ambiguity, session-local decision, drift 문제를 설명한다.

## 04.2 Intent에서 Acceptance까지

Intent → Requirement → Clarification → Acceptance → Design Constraint 흐름과 각 artifact의 책임을 정의한다.

## 04.3 Requirements-first와 Design-first

신규 기능과 brownfield/migration에서 시작점이 달라질 수 있음을 Kiro 사례로 설명한다.

## 04.4 Requirement Generator와 Evaluator 분리

Agent가 draft를 만들더라도 ambiguity/conflict/missing edge case를 별도로 검토해야 하는 이유를 다룬다.

## 04.5 Traceability

Requirement R1 → Task T3 → Commit → Test V2 → Evidence 구조를 통해 누락과 drift를 추적하는 방식을 제시한다.

## 04.6 Ready Contract

Factory Queue에 들어가기 전에 Goal, Scope, Acceptance, Dependency, Risk가 충분히 정의되었는지 확인하는 최소 조건을 제안한다.


---

## 필요한 구조 / 그림

1. Intent→Requirement→Acceptance→Task→Verification traceability chain
2. Requirement Author / Evaluator / Acceptance Authority 역할 분리
3. Ready Contract 체크 흐름

---

## 실전 예제 / 실험

- ‘로그인 오류 수정’ Issue를 expired-token 401 acceptance로 구체화하는 예
- DB migration에서 Design-first로 시작한 뒤 Requirement/Task를 만드는 예

---

## 본문에서 의도적으로 다루지 않을 내용

- Product Strategy 자동화
- 시장 조사 Agent
- formal specification 상세
- Spec Kit/Kiro 제품 사용법

---

## 앞뒤 장 연결

5장에서는 이렇게 정의된 Work를 Agent Session과 독립적으로 살아남는 Durable Task로 모델링한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
