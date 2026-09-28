# 20장 설계 - Event-driven Factory와 Closed-loop SDLC

## 장의 목표

사람의 명시적 Prompt 외에 CI 실패, vulnerability, incident, schedule 같은 signal이 Factory work source가 되는 구조를 설명한다. 단, signal을 곧바로 Agent action에 연결하지 않고 diagnosis/risk/task 단계로 변환한다.

이 장의 핵심 질문:

> 어떤 이벤트가 자동으로 Task를 만들 수 있는가?

> Production signal을 안전하게 Agent work로 연결하려면 어떤 중간 단계가 필요한가?

---

## 핵심 주장

> Alert는 Task가 아니며 signal을 diagnose/scope/acceptance가 있는 work item으로 변환해야 한다.

> Closed-loop Factory는 Delivery 이후의 production evidence를 다음 Requirement/Test/Task로 되돌린다.

> Event-driven과 Fully Autonomous는 같은 말이 아니다.

---

## 독자가 얻는 것

- Issue/CI/Review/Incident trigger를 Task source로 설계할 수 있다.
- Signal→Diagnosis→Task pipeline을 만들 수 있다.
- Production failure를 regression test/eval로 환류시킬 수 있다.
- Noise amplification과 unsafe self-healing 위험을 이해한다.

---

## 반드시 사용할 Research

- `research/22-closed-loop-sdlc-and-production-feedback.md`
- `research/08-autonomy-levels-and-self-improvement.md`
- `research/14-failure-modes-and-antipatterns.md`
- `research/19-boundaries-devops-platform-engineering-agent-platform.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Alert→Agent→Production Action 직결
- 모든 telemetry anomaly를 backlog로 생성
- Self-healing loop가 config를 반복 변경하며 oscillation
- Production incident를 acceptance 없이 auto-deploy

---

# 절 구성

## 20.1 Task Source의 확장

Human request 외에 Issue, CI Failure, Review, Vulnerability, Scheduled maintenance, Production signal을 work intake로 본다.

## 20.2 Alert ≠ Task

CPU high 같은 signal을 재현 가능하고 검증 가능한 Task로 바꾸려면 diagnosis/scope/acceptance가 필요함을 설명한다.

## 20.3 Event-driven Trigger

event가 자동 실행을 시작할 수 있지만 risk/task readiness policy를 통과하도록 한다.

## 20.4 Closed-loop SDLC

Operate → Observe → Learn → Plan → Task → Deliver 흐름을 NIST Continuous Feedback과 연결한다.

## 20.5 Product Loop와 Factory Loop

production defect가 product fix가 되는 loop와 repeated friction이 skill/tool/docs 개선으로 이어지는 loop를 구분한다.

## 20.6 Noise / Oscillation Control

deduplication, cooldown, change budget, human escalation을 통해 feedback loop 폭주를 막는다.


---

## 필요한 구조 / 그림

1. Signal→Diagnose→Scope→Risk→Task→Execute pipeline
2. Closed-loop SDLC
3. Product Loop vs Factory Improvement Loop

---

## 실전 예제 / 실험

- Nightly test fail→Task 생성→fix→regression test 고정
- Production latency alert를 바로 코드 수정하지 않고 trace 기반 diagnosis task로 변환

---

## 본문에서 의도적으로 다루지 않을 내용

- AIOps 일반론
- 완전 자동 incident response
- product roadmap automation

---

## 앞뒤 장 연결

21장에서는 이런 Factory가 cloud/CI/secret/deploy를 직접 구현하지 않고 Developer Platform의 Golden Path를 활용하는 구조를 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
