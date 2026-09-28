# Epilogue 설계 - Software Engineering에서 Software Production으로

## 장의 목표

이 책에서 구축한 AI Software Factory의 기술적 원칙을 개발자 역할과 Software Engineering의 장기적 변화에 연결한다.

미래를 단정하거나 "개발자가 사라진다"는 결론으로 가지 않는다.

핵심 질문:

> Agent가 더 많은 구현을 수행하게 될 때 사람의 Software Engineering 역할은 어디로 이동하는가?

> 좋은 개발자는 더 많은 코드를 직접 쓰는 사람인가, 더 많은 검증된 변화를 안전하게 생산할 수 있는 시스템을 만드는 사람인가?

---

## 핵심 주장

> AI Software Factory는 개발자를 제거하는 구조가 아니라 개발자의 scarce attention을 Intent, Architecture, Verification, Risk, Exception에 다시 배분하는 구조로 볼 수 있다.

> Agent가 늘어날수록 Orchestration, Verification, Governance 자체가 새로운 Software Engineering 대상이 된다.

> Software Engineering의 결과 단위가 코드 작성에서 Trustworthy / Accepted Change의 생산으로 넓어질 수 있다.

---

## 독자가 얻는 것

- 책 전체의 Durable Task, Verification, Recovery, Governance 원칙을 하나의 운영 철학으로 연결한다.
- "Humans steer, Agents execute"를 지나치게 단순하게 받아들이지 않는다.
- 직접 구현 능력과 Factory 설계 능력이 경쟁 관계가 아니라 서로 보완될 수 있음을 이해한다.
- AI Software Factory 도입의 목표를 Zero-human이 아니라 안전하고 검증 가능한 delegated execution으로 정의할 수 있다.

---

## 반드시 사용할 Research

- `research/12-engineering-role-and-operating-model.md`
- `research/16-productivity-evidence-and-measurement.md`
- `research/25-human-agent-collaboration-and-responsibility-research.md`
- `research/29-academic-synthesis-design-principles.md`

---

## 반드시 다룰 반례 / 주의점

- "개발자는 이제 코드를 읽을 필요가 없다"는 과도한 주장
- Agent 실행 속도 향상을 곧 조직 생산성 향상으로 보는 오류
- Human을 Exception Handler 하나로만 축소하는 관점
- Junior/Senior 역할 변화를 실증 근거 없이 단정하는 서술
- Self-improving Factory를 필연적인 종착점으로 표현하는 방식

---

# 절 구성

## E.1 구현에서 의도와 검증으로 이동하는 Attention

사람의 시간이 반복 명령과 기계적 구현에서 줄어들 수 있지만 다음 판단은 계속 중요하다.

- 무엇을 만들어야 하는가
- 어떤 architecture를 선택할 것인가
- 어떤 위험을 허용할 것인가
- 무엇을 완료라고 볼 것인가
- 실패를 어떻게 처리할 것인가

## E.2 Coding Skill은 사라지는가

Architecture, debugging, test, security, performance, production reasoning에는 여전히 코드 이해 능력이 필요하다.

따라서 "코드를 쓰는 시간 감소"와 "코드 역량의 불필요"를 구분한다.

## E.3 Agent Management도 Software가 된다

Agent 수가 늘어나면 사람이 각 Agent를 직접 관리하기보다:

- Queue
- Policy
- Verification
- Dashboard
- Evidence
- Recovery

를 Software로 만든다.

Factory 자체가 새로운 engineering artifact가 된다.

## E.4 Human-Agent Organization

사람과 Agent의 역할을 작성자/보조자 같은 단순 구분이 아니라 Authority 관점으로 다시 본다.

- Intent
- Planning
- Execution
- Verification
- Acceptance
- Merge/Deploy

각 권한은 다른 주체가 가질 수 있다.

## E.5 생산성의 정의를 다시 묻는다

"몇 줄 코드를 썼는가" 대신:

- 검증된 변경
- 사람의 blocking time
- review/rework
- escaped defect
- cost

로 생산성을 본다.

## E.6 Factory도 계속 개선되는 Software다

실패에서:

- Test
- Skill
- Tool
- Documentation
- Policy
- Environment

를 개선할 수 있다.

하지만 evaluator와 security boundary까지 무제한 self-modification하는 것은 별도 risk라는 점을 남긴다.

## E.7 마지막 질문

책의 결론을 하나의 미래 예측으로 닫지 않는다.

독자가 자신의 조직에서 다음을 답하도록 한다.

> 우리는 어떤 일을 Agent에게 위임할 것인가?

> 그 Agent가 실패해도 안전한가?

> 완료를 누가 무엇으로 판단하는가?

> Agent가 늘어날수록 사람의 Attention은 실제로 더 가치 있는 판단에 쓰이고 있는가?

---

## 필요한 구조 / 그림

1. Code Authoring 중심 역할 → Intent / Verification / Factory Engineering으로 Attention 이동
2. Human / Agent / System Authority Matrix 재등장
3. 책 전체 reference loop 최종 그림

---

## 본문에서 의도적으로 다루지 않을 내용

- AGI 전망
- 개발자 고용 규모 예측
- 직군별 승자/패자 예측
- AI 조직론 전체
- 미래 연도별 기술 예측

---

## Draft 완료 기준

- 책의 기술적 결론을 사람/조직 문제와 연결하되 과장하지 않는다.
- 최소 두 개 이상의 실증/연구 근거를 사용한다.
- 미래 예측보다 현재 설계 원칙을 중심으로 마무리한다.
- 마지막 문장은 독자에게 판단권을 남긴다.
