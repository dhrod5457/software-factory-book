# 21장. Developer Platform과 Golden Path를 Factory가 사용하게 만들기

소프트웨어 생산 시스템을 만든다고 모든 인프라 수행 능력을 새로 만들 필요는 없다. 조직마다 성숙도는 다르지만, 소프트웨어 생산 시스템을 도입하려는 팀은 대개 다음 기능 중 일부를 이미 사용하고 있다.

- CI/CD
- 환경 자원 준비
- 비밀 정보 관리
- 배포
- 관측 가능성
- 소프트웨어 목록
- 표준 개발 경로

생산 시스템이 해야 할 일은 조직이 이미 갖춘 기능을 에이전트도 안전하게 사용할 수 있도록 연결하는 것이다.

> 플랫폼은 생산 기능을 제공하고, 생산 시스템은 그 기능을 이용해 작업을 완료한다.

---

## 21.1 Platform이 이미 제공하는 것

내부 개발자 플랫폼은 보통 다음 문제를 해결한다.

~~~text
어떻게 Service를 만든다?
어떻게 DB를 만든다?
어떻게 배포한다?
어떻게 Secret을 쓴다?
어떻게 Observability를 붙인다?
~~~

이것은 사람 개발자에게도 어려운 반복 작업이다. 에이전트에게도 똑같다. 생산 시스템이 각각의 인프라 세부사항을 직접 다루게 하면 다음 문제가 생긴다.

- 정책 실제 상태와의 차이
- 보안 위험
- 비용 편차
- 중복 로직

그래서 기존 플랫폼 기능을 재사용하는 편이 낫다.

---

## 21.2 Agent도 Platform Consumer다

사람용 플랫폼 인터페이스는 보통 다음과 같다.

- 포털
- CLI
- 문서
- 대시보드

에이전트에는 사람용 포털과는 다른 인터페이스가 더 적합할 수 있다. 2026년 CNCF의 업계 논의에서도 AI 에이전트를 사람과 함께 플랫폼 기능을 소비하는 사람 이외의 사용자로 보고, 구별되는 신원과 범위가 제한된 권한, 감사가 필요한 방향을 제시한다. 이는 CNCF 표준 정의라기보다 현재 Platform Engineering의 확장 논의로 보는 편이 맞다.

- API
- MCP
- 구조화된 스키마
- 안정적인 식별자
- 시스템이 읽을 수 있는 오류

예를 들어 사람에게는 버튼 하나가 편하다. 에이전트에게는 다음 도구 사용 규약이 더 편하다.

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

기존 표준 개발 경로:

> 회사에서 Spring Boot 서비스를 만드는 표준 방법

에이전트 시대에는 이를 실행 가능한 규약으로 만들 수 있다.

~~~text
create_service()
provision_database()
deploy_staging()
setup_observability()
run_security_scan()
~~~

중요한 점은 에이전트가 Kubernetes/Terraform 세부사항을 매번 생성하지 않는다는 것이다. 신뢰할 수 있는 플랫폼이 표준 구현을 제공한다.

---

## 21.4 직접 Infra를 만들게 하는 방식과 비교

작업:

~~~text
staging DB를 만들어라.
~~~

에이전트가 직접 Terraform을 생성:

위험:

- 크기 선택이 달라짐
- 이름 지정 불일치
- 보안 그룹 오류
- 비용 증가
- 정책 실제 상태와의 차이

표준 개발 경로:

~~~text
provision_database(
  profile="staging-small"
)
~~~

플랫폼이 다음을 보장할 수 있다.

- 허용된 자원 배치 구조
- 이름 지정
- 암호화
- 백업
- 감사
- 비용 한도

이는 에이전트의 자유도를 줄이는 데 목적이 있는 것이 아니다. 인프라를 다룰 때 이미 알고 있는 규칙을 다시 활용하는 것이다.

---

## 21.5 Software Catalog

에이전트가 저장소만 보고 조직 전체를 이해하기는 어렵다. 목록이 충분히 관리되고 있다면 다음 정보를 찾을 수 있다. Backstage의 현재 문서도 스킬, 권한과 책임 관리 규칙, MCP 서버 같은 AI 자원을 담당 관계·생애주기·관계와 함께 소프트웨어 목록에 모델링하는 기능을 제공한다.

- 서비스 담당자
- 의존 관계
- API
- 생애주기
- 환경
- 문서
- 검토 규칙

흐름:

~~~text
Task
→ Catalog Lookup
→ Owner / Dependency / API
→ Focused Context
~~~

예를 들어 에이전트가 auth-service를 바꾼다. 목록에서 의존하는 서비스를 찾고 통합 검증 범위를 결정할 수 있다.

---

## 21.6 Catalog는 모든 것의 Source of Truth가 아니다

모든 실행 상태를 목록에 복제하면 오래된 데이터가 생긴다. 책임을 나눈다.

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

목록은 조직 맥락 정보 그래프에 가깝다.

---

## 21.7 Agent-friendly Feedback

사람에게는 다음 메시지도 충분할 수 있다.

~~~text
Deployment failed.
~~~

에이전트에게는 부족하다.

더 좋은 결과:

~~~text
status: failed
stage: readiness
reason: health_check_timeout
retryable: true
logs: artifact://deploy/1234
~~~

에이전트는 다음 행동을 판단할 수 있다.

- 재시도
- 로그 확인
- 코드 수정
- 사람에게 판단 요청

구조화된 피드백은 에이전트가 다음 행동을 고르기 쉽게 한다. DORA의 2025 Platform Engineering 연구는 사람 개발자에게도 “작업 결과에 대한 명확한 피드백”이 플랫폼 경험과 강하게 연결된다고 보고한다. 이를 에이전트 인터페이스에 적용하는 것은 이 책의 설계 확장이다.

---

## 21.8 Idempotency도 Platform Contract에 포함한다

지속 실행과 연결하면 플랫폼 도구에는 작업 동작 식별 정보가 필요할 수 있다.

~~~text
deploy_staging(
  operation_id,
  service,
  revision
)
~~~

같은 operation_id로 재호출해도 중복 배포를 막는다. 에이전트가 사용할 수 있는 플랫폼은 단순 API 노출을 넘어 **반복 실행해도 안전한 시스템 간 사용 규약**을 고려할 수 있다. 모든 플랫폼 API에 반드시 operation_id가 필요한 것은 아니지만, 재시도 시 외부 변경이 중복해서 발생하는 것이 위험한 작업에는 중요한 조건이다.

---

## 21.9 Platform Governance

에이전트가 플랫폼 API를 통해 인프라에 접근하면 권한과 책임 관리를 중앙화할 수 있다.

~~~text
Agent
→ Platform Contract
→ Policy
→ Infrastructure
~~~

정책:

- 허용된 지역
- 최대 DB 크기
- 네트워크
- 인증 정보
- 승인
- 감사

각 에이전트가 인프라 정책을 직접 해석할 필요가 줄어든다.

---

## 21.10 Human-friendly와 Agent-friendly를 함께 유지한다

에이전트가 사용할 수 있는 플랫폼이라고 사람용 포털을 없앨 필요는 없다. 같은 기능을 여러 인터페이스로 제공할 수 있다.

~~~text
Human
→ Portal / CLI

Agent
→ API / MCP

Both
→ Same Platform Capability
~~~

이 구조가 중요하다. 사람과 에이전트가 서로 다른 인프라를 사용하면 운영이 분리된다.

---

## 21.11 Agent Execution Golden Path

표준 개발 경로는 인프라 자원 준비에만 적용되는 개념이 아니다. 조직에서 반복되는 에이전트 작업에도 표준 실행 구성을 만들 수 있다.

예:

~~~text
backend-fix
security-review
db-migration
ui-verification
release-check
incident-diagnosis
~~~

각 구성은 단순 지시문 서식이 아니라 다음 묶음이 될 수 있다.

~~~text
Agent Execution Profile
=
Instruction
+ Skills
+ Tool / Connector Set
+ Worker Profile
+ Verification Profile
+ Permission Policy
+ Evidence Contract
~~~

최근 제품에서 봇 서식이나 공유 가능한 에이전트 설정을 제공하는 흐름은 이런 가능성을 보여준다. 중요한 것은 특정 공유 장터가 아니라 검증된 에이전트 작업 패턴을 조직 자산으로 재사용할 수 있다는 점이다. 예를 들어 db-migration 구성은 다음을 포함할 수 있다.

~~~text
Instruction
- migration convention

Skills
- schema-diff
- backward-compatibility-check

Worker
- database client
- isolated test database

Permission
- production write denied

Verification
- migration up/down
- compatibility test

Evidence
- schema diff
- test result
- migration revision
~~~

이렇게 하면 팀마다 에이전트에게 같은 운영 규칙을 다시 설명하는 비용을 줄일 수 있다. 하지만 서식 공유가 곧 신뢰 전파를 의미해서는 안 된다. 새로운 스킬, 도구, 권한 정책이 포함된 구성은 소프트웨어처럼 버전 관리, 검토, 평가, 단계적 적용할 수 있어야 한다. 즉 에이전트 시대의 표준 개발 경로는 다음까지 확장될 수 있다.

~~~text
Infrastructure Golden Path
+
Agent Execution Golden Path
~~~

플랫폼은 에이전트가 자유롭게 모든 방법을 발명하게 만드는 대신, 조직에서 이미 검증한 실행 능력과 안전한 경로를 제공한다.

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

지금까지 책에서는 상당히 많은 수행 능력을 다뤘다. 하지만 처음 생산 시스템을 만들 때 이 모든 것을 구현해야 할까. 다음 장에서는 **Minimum Viable AI Software Factory**로 범위를 다시 줄인다.

---

## 참고 자료

- Cursor, *Work with Grok Bot*  
  https://cursor.com/docs/grok-bot/work
- Cursor, *Grok Bot for Teams and Enterprise*  
  https://cursor.com/docs/grok-bot/teams
- DORA, *Platform Engineering Capability*  
  https://dora.dev/capabilities/platform-engineering/
- CNCF, *Platform Engineering Maturity Model*  
  https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- CNCF, *Platform Engineering for the Agentic Enterprise*  
  https://www.cncf.io/blog/2026/07/21/platform-engineering-for-the-agentic-enterprise-managing-applications-resources-and-ai-agents/
- Backstage, *AI in the Software Catalog*  
  https://backstage.io/docs/ai/ai-in-the-catalog/
