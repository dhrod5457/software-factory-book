# 12장 설계 - Verification: Agent가 완료했다고 말한 뒤부터가 시작이다

## 장의 목표

Agent self-report와 실제 completion authority를 분리하고, static/deterministic/runtime/behavioral/evaluator/human verification의 계층을 설계한다.

이 장의 핵심 질문:

> Agent가 ‘완료’했다고 했을 때 Factory는 무엇을 확인해야 하는가?

> Test PASS만으로 Task DONE을 선언할 수 있는가?

---

## 핵심 주장

> Agent self-report는 evidence가 아니며 completion authority는 independent verification에 있어야 한다.

> Test PASS는 중요하지만 user intent와 production readiness 전체를 보장하지 않는다.

> Verification은 Agent loop 바깥의 사후 단계가 아니라 실행 중 지속적으로 feedback을 주는 subsystem이다.

---

## 독자가 얻는 것

- Verification pyramid를 구성할 수 있다.
- Task별 최소 required verification을 정의할 수 있다.
- Self-evaluation과 independent evaluation을 구분할 수 있다.
- Building-to-test, reward hacking, lucky pass 위험을 설명할 수 있다.

---

## 반드시 사용할 Research

- `research/05-verification-evidence-and-human-gates.md`
- `research/09-evals-and-benchmark-limitations.md`
- `research/14-failure-modes-and-antipatterns.md`
- `research/28-benchmark-science-and-evaluation-methodology.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Agent가 DONE이라고 말하면 완료 처리
- Visible test를 intent와 동일시
- Agent가 만든 test만으로 자신의 구현을 승인
- Benchmark PASS를 production readiness로 해석

---

# 절 구성

## 12.1 Completion Claim과 Completion Authority

Agent proposes → Verifier checks → Evidence → Policy/Human accepts 구조를 제시한다.

## 12.2 Verification Pyramid

Static → Unit/Integration → Runtime → Behavioral Evidence → Independent Evaluator → Human 순으로 비용과 신뢰 signal을 설명한다.

## 12.3 Executable Acceptance

Requirement/Acceptance를 test/property/runtime scenario에 연결해 Agent iteration feedback으로 사용하는 방식을 설명한다.

## 12.4 Test PASS의 한계

METR maintainer review gap, Microsoft Building to the Test, reward hacking 사례를 통해 validation diversity 필요성을 설명한다.

## 12.5 Independent Evaluator

Generator와 evaluator role 분리의 장점과 같은 model/context의 correlated error 한계를 함께 다룬다.

## 12.6 Verification Policy

Task risk에 따라 required checks를 system policy로 정의하고 Agent가 임의 생략하지 못하게 하는 구조를 제시한다.


---

## 필요한 구조 / 그림

1. Verification pyramid
2. Requirement→Acceptance→Verification traceability
3. Agent self-report vs Verifier authority sequence

---

## 실전 예제 / 실험

- UI Task: typecheck+E2E+screenshot+human visual acceptance
- Backend auth change: unit+integration+security scan+contract test
- Agent가 test를 약화시켜 PASS를 만드는 reward hacking 예

---

## 본문에서 의도적으로 다루지 않을 내용

- Evidence manifest 상세
- Human governance 전체
- benchmark leaderboard 비교

---

## 앞뒤 장 연결

13장에서는 Verification 결과를 사람이 빠르게 판단하고 시스템이 추적할 수 있는 Evidence Contract로 구조화한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
