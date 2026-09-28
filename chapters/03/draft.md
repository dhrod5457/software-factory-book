# 3장. CI/CD, DevOps, Platform Engineering, Agent Platform과의 경계

2장에서 AI Software Factory의 최소 정의를 정했다.

하지만 실제 조직에는 이미 많은 시스템이 있다.

- Git
- Issue Tracker
- CI/CD
- Internal Developer Platform
- Monitoring
- Deployment Platform
- Secret Management
- Agent Runtime

그래서 새로운 이름을 붙이는 것보다 더 중요한 질문이 생긴다.

> AI Software Factory는 기존 시스템과 정확히 무엇이 다른가?

이 경계를 잘못 잡으면 두 가지 문제가 생긴다.

하나는 기존에 잘 동작하던 CI/CD와 Platform을 무시하고 모든 것을 다시 만드는 것이다.

다른 하나는 반대로 기존 파이프라인에 Agent 호출 하나를 추가하고 그것을 Software Factory라고 부르는 것이다.

둘 다 피해야 한다.

이 장에서는 AI Software Factory를 기존 Software Delivery System 위에 놓고 경계를 정리한다.

---

## 3.1 CI/CD는 무엇을 이미 잘하고 있는가

CI/CD는 이미 소프트웨어 생산 자동화의 핵심이다.

일반적인 흐름은 다음과 같다.

```text
Source Change
→ Build
→ Test
→ Package
→ Release
→ Deploy
```

이 구조는 매우 강력하다.

사람이 매번 수동으로 Build와 Test를 실행하지 않아도 된다.

같은 Revision에 대해 반복 가능한 검증을 수행할 수 있다.

Release와 Deployment를 정책에 따라 자동화할 수도 있다.

Software Factory는 이 기반을 버리지 않는다.

오히려 적극적으로 사용한다.

차이는 CI/CD가 보통 **정의된 변경 이후**를 잘 다룬다는 데 있다.

예를 들어 CI는 다음 질문에 답한다.

- 이 Commit이 Build되는가?
- Test가 통과하는가?
- Artifact를 만들 수 있는가?
- Deployment가 성공하는가?

하지만 일반적인 CI/CD는 다음 질문까지 스스로 책임지지 않는다.

- 어떤 문제를 해결해야 하는가?
- 어떤 Task를 지금 시작해야 하는가?
- 어떤 파일을 수정해야 하는가?
- 실패한 Test를 어떻게 고칠 것인가?
- 같은 Task를 다른 Worker에게 재배정해야 하는가?
- Human Approval을 기다려야 하는가?

AI Software Factory는 이 앞단과 중간을 확장한다.

```text
Intent
→ Requirement
→ Task
→ Agent Work
→ Code Change
→ CI/CD
→ Delivery
→ Feedback
```

이 관점에서는 CI/CD가 사라지는 것이 아니다.

Factory의 중요한 검증·전달 subsystem이 된다.

특히 Agent 시대에는 CI가 파이프라인의 끝에만 있는 것도 아니다.

```text
Agent Change
→ Targeted Test
→ CI
→ Failure
→ Agent Fix
→ CI
```

CI 결과가 Agent에게 다시 피드백되어 수정 루프 안으로 들어올 수 있다.

즉, Factory가 CI/CD를 대체하는 것이 아니라 CI/CD를 더 자주 호출하고 더 중요한 feedback source로 사용한다.

---

## 3.2 DevOps와 DevSecOps를 대체하지 않는다

AI Software Factory를 새로운 개발 방법론으로 오해할 필요도 없다.

DevOps와 DevSecOps가 강조해 온 원칙은 Agent 시대에도 그대로 중요하다.

- 작은 변경
- 빠른 피드백
- 자동화된 검증
- 운영 가시성
- 개발과 운영의 연결
- 보안의 조기 통합

오히려 Agent가 더 많은 변경을 더 빠르게 만들수록 이런 원칙은 더 중요해질 수 있다.

NIST NCCoE의 DevSecOps reference model을 보면 Software Delivery를 다음과 같은 연속된 흐름으로 본다.

```text
Plan
→ Develop
→ Build
→ Test
→ Release
→ Deploy
→ Operate
        ↘
     Feedback
        ↖
```

여기에 CI/CD, Security, Monitoring, Control Gate가 횡단으로 들어간다.

중요한 점은 AI가 이 구조를 없애는 것이 아니라는 것이다.

Agent는 이 lifecycle 안에 새로운 실행 주체로 들어간다.

예를 들어 다음과 같이 볼 수 있다.

```text
Human / Product Signal
        ↓
Plan / Requirement
        ↓
Agent
→ Develop
→ Build
→ Test
        ↓
Existing Release / Deploy System
        ↓
Operate
        ↓
Feedback
```

이 구조에서는 DevOps가 사라지지 않는다.

기존 DevOps가 사람과 자동화 중심으로 설계됐다면, 이제 Agent가 새로운 actor로 추가된다.

```text
Human
+ Automation
+ AI Agent
```

Factory는 이 셋을 하나의 Work Flow로 묶는 쪽에 가깝다.

---

## 3.3 Platform Engineering과 Factory는 경쟁 관계가 아니다

Platform Engineering과 Software Factory는 자주 겹쳐 보인다.

둘 다 다음을 이야기하기 때문이다.

- 표준화
- 자동화
- Self-service
- Golden Path
- Policy
- Developer Experience

하지만 책임의 중심이 다르다.

Platform Engineering은 조직에 **공통 생산 capability**를 제공한다.

예를 들면 다음과 같다.

- 표준 Repository Template
- Build Environment
- CI
- Secret Management
- Deployment
- Observability
- Database Provisioning
- Software Catalog
- Policy

Developer는 이 capability를 사용해 제품을 만든다.

AI Software Factory도 똑같이 이 capability를 사용할 수 있다.

경계를 단순화하면 다음과 같다.

```text
Platform Engineering
= 안전하고 표준화된 생산 능력을 제공

Software Factory
= 그 능력을 사용해 실제 Work를 완료
```

예를 들어 Task가 "staging database를 준비하라"라고 하자.

Agent에게 Terraform과 Kubernetes 설정을 매번 새로 생성하게 할 수도 있다.

하지만 조직에 이미 Golden Path가 있다면 다음처럼 만드는 편이 낫다.

```text
provision_database(
  profile = "staging-small"
)
```

Agent는 구현 세부사항을 직접 만들지 않는다.

Platform이 검증된 방식으로 Resource를 준비한다.

이 구조의 장점은 명확하다.

- Policy가 중앙에서 적용된다.
- Naming과 Resource Size가 표준화된다.
- Audit가 쉬워진다.
- Agent에게 과도한 Infra 권한을 주지 않아도 된다.
- 팀마다 다른 Terraform을 생성하는 drift를 줄일 수 있다.

즉, Factory가 Platform을 대체하려고 하면 안 된다.

다음 구조가 더 자연스럽다.

```text
Factory
→ Platform API / Golden Path
→ Infrastructure
```

---

### Agent도 Platform User가 된다

기존 Internal Developer Platform은 사람을 주요 사용자로 생각했다.

그래서 다음 interface가 중요했다.

- Portal
- CLI
- Documentation
- Dashboard

Agent가 사용자가 되면 요구사항이 조금 달라진다.

Agent-friendly interface에는 다음이 더 중요하다.

- Structured Schema
- Stable Identifier
- Deterministic API
- Machine-readable Error
- Idempotency
- Scoped Permission
- Artifact Reference

사람에게는 다음 메시지도 충분할 수 있다.

```text
Deployment failed.
```

사람은 로그를 찾아보고 원인을 추적할 수 있다.

Agent에게는 다음 형태가 더 유용하다.

```text
status: failed
stage: readiness
reason: health_check_timeout
retryable: true
logs: artifact://deploy/1234
```

Agent 시대에는 Platform UX도 사람만을 위한 것이 아니게 된다.

---

## 3.4 Agent Platform과 Software Factory

Agent Platform과 Software Factory는 더 쉽게 혼동된다.

Agent Platform은 보통 Agent를 만들고 운영하는 범용 기반을 제공한다.

예를 들면 다음 capability다.

- Runtime
- Model Access
- Tool Gateway
- Identity
- Memory
- Observability
- Policy
- Evaluation

이 기능은 Coding Agent뿐 아니라 다른 Agent에도 사용할 수 있다.

- Customer Support Agent
- Data Agent
- Sales Agent
- Operations Agent
- Research Agent

Software Factory는 이보다 Domain이 좁다.

Software Delivery에 특화된 object와 상태를 다룬다.

- Requirement
- Repository
- Branch
- Commit
- Build
- Test
- Pull Request
- Artifact
- Approval
- Release
- Deployment
- Acceptance

그래서 다음처럼 구분하는 편이 유용하다.

```text
Agent Platform
= Agent를 실행할 수 있는 범용 기반

AI Software Factory
= Software Work를 완료하는 Domain System
```

Agent Platform이 충분히 좋아도 다음을 자동으로 제공하지는 않는다.

- 어떤 Task가 Ready인가
- 이 Task의 Dependency는 무엇인가
- 어떤 Verification이 필수인가
- 이 Pull Request를 Merge해도 되는가
- Worker가 죽었을 때 같은 Task를 어떻게 이어받는가
- 같은 Schema를 수정하는 Task를 동시에 시작해도 되는가

이것은 Software Factory가 알아야 하는 Domain State다.

---

### Runtime과 Factory도 구분한다

Agent Runtime은 실행 기반이다.

```text
Agent Runtime
- process
- container
- model call
- tool call
- filesystem
- isolation
```

Factory는 Runtime을 사용할 수 있다.

하지만 Factory의 Task는 Runtime보다 오래 살아야 한다.

Runtime이 죽어도 다음은 남아야 한다.

- Task
- Attempt History
- Verification
- Evidence
- Approval
- Retry State

그래서 단순하게 다음과 같이 계층화하면 오해가 생긴다.

```text
Agent Runtime
< Agent Platform
< Software Factory
```

항상 포함 관계는 아니다.

더 정확한 표현은 다음에 가깝다.

```text
Software Factory
uses
- Agent Runtime
- Agent Platform
- Developer Platform
- CI/CD
```

Factory는 이 기반 위에서 Software Delivery domain의 Work를 관리한다.

---

## 3.5 경계를 나누면 무엇이 좋아지는가

경계를 나누는 이유는 용어 정리를 하기 위해서만은 아니다.

실제 Architecture가 단순해진다.

예를 들어 Factory를 만든다고 다음 기능을 모두 직접 구현한다고 해보자.

- Secret Manager
- CI Runner
- Container Scheduler
- Deployment System
- Logging
- Metrics
- Artifact Storage
- Agent Runtime

거대한 프로젝트가 된다.

실제로 필요한 것은 기존 Capability를 연결하는 것일 수 있다.

```text
Task
      ↓
Factory Control Plane
      ↓
Agent Runtime
      ↓
Developer Platform
      ↓
CI/CD / Deploy / Observability
```

이 구조에서는 Factory가 직접 모든 일을 하지 않는다.

Factory는 다음을 책임진다.

- Work 상태
- 어떤 Worker가 필요한가
- 어떤 Capability를 호출해야 하는가
- 어떤 Verification이 필요한가
- 실패하면 어떻게 복구할 것인가
- 언제 사람의 승인이 필요한가

Platform은 다음을 책임진다.

- 환경 생성
- Credential
- Build Infrastructure
- Deployment
- Monitoring
- 공통 Policy

CI/CD는 다음을 책임진다.

- deterministic build
- test
- artifact
- release/deployment pipeline

Agent Runtime은 실제 Agent execution을 담당한다.

각 시스템이 잘하는 일을 그대로 사용한다.

이렇게 하면 Factory Architecture를 새 인프라 전체로 만들지 않아도 된다.

---

## Software Factory는 새로운 섬이 아니다

이 책에서 AI Software Factory를 기존 Software Engineering과 분리된 새로운 세계로 보지 않는 이유가 있다.

실제 조직에서 가장 현실적인 Factory는 기존 자산을 재사용할 가능성이 높다.

```text
Git
+ Issue Tracker
+ CI/CD
+ Internal Developer Platform
+ Agent Runtime
+ Task Orchestration
+ Verification
+ Governance
```

이 조합이 조직마다 다를 뿐이다.

새롭게 필요한 것은 모든 도구를 다시 만드는 것이 아니라 **Agent가 이 시스템 안에서 Work를 수행할 수 있도록 상태와 권한과 피드백을 연결하는 것**이다.

그래서 Factory를 설계할 때 첫 질문은 다음이 아니다.

> 어떤 Agent Platform을 도입할까?

먼저 물어야 할 것은 이것이다.

> 우리 조직에 이미 어떤 Software Delivery Capability가 있고, 그중 Agent가 안전하게 사용할 수 없는 부분은 어디인가?

이 질문을 하면 구축 범위가 줄어든다.

그리고 무엇을 새로 만들어야 하는지도 선명해진다.

---

## 다음 질문

지금까지는 Factory의 외곽 경계를 정리했다.

이제부터는 내부로 들어간다.

Agent에게 Task를 주기 전에 먼저 결정해야 할 것이 있다.

Agent가 무엇을 구현해야 하는지 어떻게 정의할 것인가.

어떤 상태가 되어야 "작업할 준비가 됐다"고 볼 것인가.

다음 장에서는 Prompt를 바로 Agent에게 던지는 대신 **Intent를 Requirement와 Acceptance로 바꾸는 과정**부터 시작한다.

---

## 참고 자료

- NIST NCCoE, *Notional Reference Model for DevSecOps*  
  https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
- DORA, *Platform Engineering Capability*  
  https://dora.dev/capabilities/platform-engineering/
- CNCF, *Platform Engineering Maturity Model*  
  https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- CNCF, *Platform Engineering for the Agentic Enterprise*  
  https://www.cncf.io/blog/2026/07/21/platform-engineering-for-the-agentic-enterprise-managing-applications-resources-and-ai-agents/
- Backstage, *AI in the Software Catalog*  
  https://backstage.io/docs/ai/ai-in-the-catalog/
