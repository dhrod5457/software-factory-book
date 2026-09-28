# 24장 설계 - Factory Maturity와 Autonomy를 어떻게 올릴 것인가

## 장의 목표

책 전체를 하나의 단계적 도입 모델로 정리한다. Factory의 infrastructure maturity와 Agent decision authority를 같은 축으로 섞지 않고 별도로 관리한다.

이 장의 핵심 질문:

> 언제 Parallel/Event-driven/Adaptive Factory로 확장해야 하는가?

> Autonomy를 올려도 되는 조건은 무엇인가?

---

## 핵심 주장

> Maturity와 Autonomy는 다른 축이다.

> 높은 Autonomy는 목표가 아니라 충분한 reliability, observability, verification, governance 위에서 선택하는 운영 정책이다.

> Work Selection, Execution, Acceptance, Merge 권한을 각각 독립적으로 높일 수 있다.

---

## 독자가 얻는 것

- M0~M5 maturity model을 research taxonomy로 사용할 수 있다.
- Autonomy authority matrix를 설계할 수 있다.
- 현재 조직이 다음 capability를 추가할 준비가 됐는지 판단할 수 있다.
- Self-improvement를 마지막 고급 단계로 배치할 수 있다.

---

## 반드시 사용할 Research

- `research/08-autonomy-levels-and-self-improvement.md`
- `research/23-minimum-viable-ai-software-factory.md`
- `research/25-human-agent-collaboration-and-responsibility-research.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Autonomy를 0~100 하나의 숫자로 평가
- Agent 수/Worker 수를 maturity와 동일시
- Human review가 있다는 이유로 낮은 maturity라고 판단
- Self-improvement를 reliability 이전에 도입

---

# 절 구성

## 24.1 Maturity와 Autonomy 분리

Factory infrastructure capability와 decision authority를 두 축으로 설명한다.

## 24.2 M0~M5 후보

Interactive Agent, Repeatable Worker, Durable Factory, Parallel Factory, Event-driven Factory, Adaptive Factory를 책 자체 taxonomy로 제시하되 업계 표준이 아님을 명시한다.

## 24.3 Autonomy Authority Matrix

Work Selection, Planning, Execution, Verification, Acceptance, Merge/Deploy 권한을 Human/Agent/System에 배분한다.

## 24.4 승급 조건

다음 단계로 갈 때 success rate보다 evidence, recovery, downstream capacity, security, human attention을 함께 확인한다.

## 24.5 Risk-based Autonomy

docs와 auth/payment/production migration이 같은 autonomy policy를 가질 필요가 없음을 설명한다.

## 24.6 Self-improvement의 위치

docs/skill/tool/eval 개선은 가능하지만 evaluator/security policy 자체 변경에는 shadow/canary/approval/rollback이 필요함을 설명한다.

## 24.7 조직별 Roadmap

small team, platform team, regulated enterprise가 서로 다른 maturity 목표를 가질 수 있음을 제시한다.


---

## 필요한 구조 / 그림

1. Maturity axis × Autonomy axis matrix
2. M0→M5 staged roadmap
3. Authority matrix by decision type

---

## 실전 예제 / 실험

- M2 Durable Factory에서 execution은 autonomous지만 merge는 human인 조직
- Low-risk docs는 auto-merge, auth code는 human approval인 risk-based policy
- M3로 가기 전 review queue capacity 측정

---

## 본문에서 의도적으로 다루지 않을 내용

- 업계 표준 인증 모델처럼 제시
- 미래 예측 순위
- AI 조직 전체의 인사/고용 설계

---

## 앞뒤 장 연결

Epilogue에서는 24장의 roadmap을 넘어 개발자의 역할과 Software Engineering이 Software Production System 설계로 확장되는 의미를 정리한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
