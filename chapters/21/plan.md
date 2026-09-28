# 21장 설계 - Developer Platform과 Golden Path를 Factory가 사용하게 만들기

## 장의 목표

Internal Developer Platform을 AI Software Factory의 기반 capability layer로 연결한다. Human-friendly portal뿐 아니라 Agent-friendly machine contract와 catalog가 필요한 이유를 설명한다.

이 장의 핵심 질문:

> Factory가 기존 Platform Engineering 자산을 어떻게 재사용해야 하는가?

> Agent-ready Platform interface는 사람용 portal과 무엇이 다른가?

---

## 핵심 주장

> Platform은 안전하고 표준화된 capability를 제공하고 Factory는 그 capability를 이용해 Work를 완료한다.

> Agent에게 인프라를 임의 생성하게 하기보다 trusted Golden Path를 machine-readable contract로 제공하는 편이 안정적이다.

> Repository뿐 아니라 조직의 Platform도 Agent-readable해야 한다.

---

## 독자가 얻는 것

- Factory와 Developer Platform의 책임을 나눌 수 있다.
- Golden Path를 Agent tool/API로 노출하는 방식을 설계할 수 있다.
- Software Catalog를 context source로 사용할 수 있다.
- Structured error/idempotency/scoped identity가 Agent UX에 중요한 이유를 이해한다.

---

## 반드시 사용할 Research

- `research/19-boundaries-devops-platform-engineering-agent-platform.md`
- `research/21-agent-ready-developer-platform-and-catalog.md`
- `research/03-harness-context-and-agent-legibility.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- 각 Agent가 Terraform/Kubernetes/Secret 처리를 직접 생성
- 사람용 wiki/portal이 있으면 Agent도 충분히 이해할 것이라는 가정
- Catalog를 모든 runtime state의 복제 저장소로 사용하는 오류

---

# 절 구성

## 21.1 Platform이 이미 제공하는 것

environment, CI/CD, secret, deploy, observability, catalog, policy, golden path를 정리한다.

## 21.2 Agent도 Platform Consumer다

Human portal/CLI와 Agent API/MCP/machine contract의 차이를 설명한다.

## 21.3 Golden Path as Tool

provision_database, deploy_staging 같은 trusted operation을 stable contract로 제공하는 방식을 제시한다.

## 21.4 Software Catalog

service owner, dependency, API, lifecycle, skill/MCP metadata를 Agent가 조회하는 context graph로 사용한다.

## 21.5 Agent-friendly Feedback

Deployment failed 같은 텍스트 대신 stage/reason/log_ref/retryable 같은 structured result가 필요한 이유를 설명한다.

## 21.6 Platform Governance

Agent가 Platform API를 통해 infrastructure에 접근하면 naming/policy/audit/cost guardrail을 중앙에서 강제할 수 있음을 보여준다.


---

## 필요한 구조 / 그림

1. Factory→Developer Platform→Infrastructure layered view
2. Human interface vs Agent machine contract
3. Software Catalog lookup flow

---

## 실전 예제 / 실험

- Agent가 Terraform을 직접 쓰는 방식과 provision_database(profile=staging-small) tool 비교
- Catalog에서 service owner와 dependent API를 찾아 review routing

---

## 본문에서 의도적으로 다루지 않을 내용

- Backstage 설치법
- Kubernetes/IDP 구축 튜토리얼
- platform team 조직 설계 전체

---

## 앞뒤 장 연결

22장에서는 앞 장들의 capability를 한꺼번에 만들지 않고 가장 작은 Minimum Viable Factory부터 시작하는 도입 순서를 제시한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
