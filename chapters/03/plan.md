# 03장 설계 - CI/CD, DevOps, Platform Engineering, Agent Platform과의 경계

## 장의 목표

AI Software Factory가 기존 Software Delivery 체계를 대체하는 새로운 섬이 아니라 그 위에 Agent를 first-class worker로 배치하는 생산 시스템임을 설명한다.

이 장의 핵심 질문:

> Software Factory는 CI/CD와 무엇이 다른가?

> Platform Engineering과 Factory는 경쟁 관계인가?

> Agent Platform과 Software Factory의 경계는 어디인가?

---

## 핵심 주장

> CI/CD는 Factory의 핵심 subsystem이지만 Work 정의·실행·복구 전체를 책임지지 않는다.

> Platform Engineering은 생산 capability를 제공하고 Factory는 그 capability 위에서 실제 Work를 흐르게 한다.

> Agent Platform은 Agent를 실행하고 Software Factory는 Software Work를 완료한다.

---

## 독자가 얻는 것

- CI/CD, DevOps, Platform Engineering, Agent Platform을 Factory와 구분할 수 있다.
- 기존 Internal Developer Platform을 Factory 기반으로 재사용해야 하는 이유를 이해한다.
- Factory를 새 인프라 전체로 오해하지 않을 수 있다.

---

## 반드시 사용할 Research

- `research/19-boundaries-devops-platform-engineering-agent-platform.md`
- `research/21-agent-ready-developer-platform-and-catalog.md`
- `research/22-closed-loop-sdlc-and-production-feedback.md`
- `research/sources.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Factory가 기존 CI/CD를 대체한다는 관점
- 각 Agent가 secret/deploy/observability를 직접 구현하는 구조
- Agent Platform의 generic runtime capability를 Software Delivery domain semantics와 동일시하는 오류

---

# 절 구성

## 03.1 CI/CD는 무엇을 이미 잘하고 있는가

Source Change 이후 Build/Test/Package/Release/Deploy 자동화의 강점을 인정하고, Factory는 앞단의 Work/Agent execution과 실패 수정 loop를 추가한다고 설명한다.

## 03.2 DevOps / DevSecOps와의 관계

small batch, automation, feedback, observability, shared ownership 원칙이 Agent 시대에도 유지되며 NIST DevSecOps reference model과 연결한다.

## 03.3 Platform Engineering과 Factory

Golden Path, self-service, environment, secrets, deployment, catalog를 Platform이 제공하고 Factory가 이 capability를 소비하는 구조를 설명한다.

## 03.4 Agent Platform과 Factory

Runtime, Identity, Gateway, Memory 같은 generic capability와 Repository/PR/Test/Release/Acceptance 같은 Software Delivery domain object를 구분한다.

## 03.5 경계가 주는 설계 이점

Factory가 모든 infrastructure를 재구현하지 않고 existing platform contracts를 활용하면 보안·운영 복잡도가 줄어드는 이유를 설명한다.


---

## 필요한 구조 / 그림

1. CI/CD / Platform / Agent Platform / Software Factory 관계도
2. NIST Plan→Develop→Build→Test→Release→Deploy→Operate loop와 Agent 위치
3. Factory → Platform API → Infrastructure 구조

---

## 실전 예제 / 실험

- 기존 Jenkins/GitHub Actions를 그대로 Verification/Delivery subsystem으로 사용하는 Factory
- Agent가 Kubernetes API를 직접 호출하는 방식과 Platform Golden Path를 호출하는 방식 비교

---

## 본문에서 의도적으로 다루지 않을 내용

- DevOps 입문
- Kubernetes 사용법
- Agent Platform 제품 비교
- Platform Engineering 조직 설계 전체

---

## 앞뒤 장 연결

4장부터는 Factory가 처리할 Work를 어떻게 정의하는지 Intent, Requirement, Acceptance부터 시작한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
