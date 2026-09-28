# 21장. Developer Platform과 Golden Path를 Factory가 사용하게 만들기

Software Factory를 만든다고 모든 Infrastructure Capability를 새로 만들 필요는 없다.

대부분의 조직에는 이미 다음이 있다.

- CI/CD
- Environment Provisioning
- Secret Management
- Deployment
- Observability
- Software Catalog
- Golden Path

Factory가 해야 할 일은 이 Capability를 Agent도 안전하게 사용할 수 있게 연결하는 것이다.

> Platform은 생산 Capability를 제공하고, Factory는 그 Capability를 이용해 Work를 완료한다.

---

## 21.1 Platform이 이미 제공하는 것

Internal Developer Platform은 보통 다음 문제를 해결한다.

~~~text
어떻게 Service를 만든다?
어떻게 DB를 만든다?
어떻게 배포한다?
어떻게 Secret을 쓴다?
어떻게 Observability를 붙인다?
~~~

이것은 사람 개발자에게도 어려운 반복 작업이다.

Agent에게도 똑같다.

Factory가 각각의 Infra Detail을 직접 다루게 하면 다음 문제가 생긴다.

- Policy Drift
- Security Risk
- Cost Variation
- Duplicated Logic

그래서 기존 Platform Capability를 재사용하는 편이 낫다.

---

## 21.2 Agent도 Platform Consumer다

사람용 Platform Interface는 보통 다음과 같다.

- Portal
- CLI
- Documentation
- Dashboard

Agent는 다른 Interface를 선호할 수 있다.

- API
- MCP
- Structured Schema
- Stable Identifier
- Machine-readable Error

예를 들어 사람에게는 버튼 하나가 편하다.

Agent에게는 다음 Tool Contract가 더 편하다.

~~~text
deploy_staging(
  service,
  revision
)
~~~

결과:

~~~text
deployment_id
status
url
log_ref
~~~

---

## 21.3 Golden Path를 Tool로 만든다

기존 Golden Path:

> 회사에서 Spring Boot Service를 만드는 표준 방법

Agent 시대에는 이를 실행 가능한 Contract로 만들 수 있다.

~~~text
create_service()
provision_database()
deploy_staging()
setup_observability()
run_security_scan()
~~~

중요한 점은 Agent가 Kubernetes/Terraform 세부사항을 매번 생성하지 않는다는 것이다.

Trusted Platform이 표준 구현을 제공한다.

---

## 21.4 직접 Infra를 만들게 하는 방식과 비교

Task:

~~~text
staging DB를 만들어라.
~~~

Agent가 직접 Terraform을 생성:

위험:

- Size 선택이 달라짐
- Naming 불일치
- Security Group 오류
- Cost 증가
- Policy Drift

Golden Path:

~~~text
provision_database(
  profile="staging-small"
)
~~~

Platform이 다음을 보장할 수 있다.

- allowed topology
- naming
- encryption
- backup
- audit
- cost limit

Agent의 자유도를 줄이는 것이 아니라 Infrastructure Domain에서는 이미 알고 있는 Rule을 재사용하는 것이다.

---

## 21.5 Software Catalog

Agent가 Repository만 보고 조직 전체를 이해하기는 어렵다.

Catalog에서 다음을 찾을 수 있다.

- Service Owner
- Dependency
- API
- Lifecycle
- Environment
- Documentation
- Review Rule

흐름:

~~~text
Task
→ Catalog Lookup
→ Owner / Dependency / API
→ Focused Context
~~~

예를 들어 Agent가 auth-service를 바꾼다.

Catalog에서 dependent service를 찾고 Integration Verification 범위를 결정할 수 있다.

---

## 21.6 Catalog는 모든 것의 Source of Truth가 아니다

모든 Runtime State를 Catalog에 복제하면 stale data가 생긴다.

책임을 나눈다.

~~~text
Code
→ Git

Task
→ Task Store

Deployment
→ Runtime Platform

Logs
→ Observability

Ownership / Dependency Index
→ Catalog
~~~

Catalog는 조직 Context Graph에 가깝다.

---

## 21.7 Agent-friendly Feedback

사람에게는 다음 메시지도 충분할 수 있다.

~~~text
Deployment failed.
~~~

Agent에게는 부족하다.

더 좋은 결과:

~~~text
status: failed
stage: readiness
reason: health_check_timeout
retryable: true
logs: artifact://deploy/1234
~~~

Agent는 다음 행동을 판단할 수 있다.

- retry
- log inspect
- code fix
- escalation

Structured Feedback은 Agent UX의 핵심이다.

---

## 21.8 Idempotency도 Platform Contract에 포함한다

Durable Execution과 연결하면 Platform Tool에는 operation identity가 필요할 수 있다.

~~~text
deploy_staging(
  operation_id,
  service,
  revision
)
~~~

같은 operation_id로 재호출해도 duplicate deploy를 막는다.

Agent-ready Platform은 단순 API 노출이 아니라 **replay-safe machine contract**까지 고려해야 한다.

---

## 21.9 Platform Governance

Agent가 Platform API를 통해 Infrastructure에 접근하면 Governance를 중앙화할 수 있다.

~~~text
Agent
→ Platform Contract
→ Policy
→ Infrastructure
~~~

Policy:

- allowed region
- max DB size
- network
- credential
- approval
- audit

각 Agent가 Infrastructure Policy를 직접 해석할 필요가 줄어든다.

---

## 21.10 Human-friendly와 Agent-friendly를 함께 유지한다

Agent-ready Platform이라고 사람용 Portal을 없앨 필요는 없다.

같은 Capability를 여러 Interface로 제공할 수 있다.

~~~text
Human
→ Portal / CLI

Agent
→ API / MCP

Both
→ Same Platform Capability
~~~

이 구조가 중요하다.

Human과 Agent가 서로 다른 Infrastructure를 사용하면 운영이 분리된다.

---

## Platform을 Agent-ready하게 만들 때 묻는 질문

~~~text
1. Capability가 stable machine contract로 노출되는가?
2. Output이 structured한가?
3. Error가 retryable 여부를 알려주는가?
4. Idempotent한가?
5. Scoped Identity를 지원하는가?
6. Audit 가능한가?
7. Catalog에서 ownership/dependency를 찾을 수 있는가?
~~~

---

## 다음 질문

지금까지 책에서는 상당히 많은 Capability를 다뤘다.

하지만 처음 Factory를 만들 때 이 모든 것을 구현해야 할까.

다음 장에서는 **Minimum Viable AI Software Factory**로 범위를 다시 줄인다.

---

## 참고 자료

- DORA, *Platform Engineering Capability*  
  https://dora.dev/capabilities/platform-engineering/
- CNCF, *Platform Engineering Maturity Model*  
  https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- CNCF, *Platform Engineering for the Agentic Enterprise*  
  https://www.cncf.io/blog/2026/07/21/platform-engineering-for-the-agentic-enterprise-managing-applications-resources-and-ai-agents/
- Backstage, *AI in the Software Catalog*  
  https://backstage.io/docs/ai/ai-in-the-catalog/
