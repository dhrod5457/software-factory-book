# 2장. AI Software Factory란 무엇인가

1장에서 본 문제는 단순했다.

코딩 에이전트가 빨라져도 소프트웨어 전달 전체가 같은 속도로 빨라지는 것은 아니다. 작업이 늘어나면 검토, CI, 통합, 사람의 주의와 노력 같은 다른 단계가 병목이 된다. 그렇다면 어디까지 갖춰야 소프트웨어 생산 시스템이라고 부를 수 있을까. 소프트웨어 생산 시스템은 에이전트를 여러 개 띄우는 시스템과 같은 말이 아니다. 완전 자율 병합이 가능한 시스템만 생산 시스템인 것도 아니다. CI/CD에 LLM 호출을 하나 추가했다고 자동으로 생산 시스템이 되는 것도 아니다. 이 책에서는 다음과 같이 정의한다.

> **AI Software Factory는 실행이 중단돼도 작업 기록이 남도록 관리하고, AI 에이전트에게 실행을 맡기며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.**

이 정의에서 중요한 것은 에이전트 수가 아니라 **중단돼도 기록이 남는 작업(Durable Work), 실행 위임, 독립된 검증, 실패 복구, 지속적인 전달**이다. 에이전트는 중요한 워커지만 생산 시스템 전체는 아니다. 산업 현장에서도 비슷한 경계가 나타난다.

Caylent는 소프트웨어 생산 시스템을 Claude Code 같은 코딩 에이전트 자체가 아니라, 그 주위에 플러그인과 스킬, 후크, 규칙, 실행 순환을 배치해 소프트웨어 개발 과정을 자동화하는 구조로 설명한다. 공개한 DevBench 역시 구조화된 할 일 목록을 구현, 검토, 보안 검토, Git 흐름으로 통과시키는 실행 조율 시스템에 가깝다. 이 사례에서 가져올 원칙은 특정 제품이나 자동화 수준이 아니다.

~~~text
Coding Agent
≠ Software Factory

Agent Capability
+ Harness
+ Work State
+ Verification
+ Delivery Control
→ Factory Capability
~~~

이 책의 정의는 여기서 한 단계 더 넓다. 하네스는 중요한 실행 계층이지만, 지속되는 작업, 복구, 최종 수용 권한, 피드백까지 포함하는 생산 시스템 전체와 동일하지 않다. WorkOS의 Ryan Cooke도 비슷한 경계를 다른 각도에서 설명한다. WorkOS는 격리 환경에 코딩 에이전트를 넣고 지시문으로 PR을 만드는 초기 구조를 운영했지만, 그것만으로는 개발자가 로컬 코딩 에이전트를 직접 사용하는 것과 조직의 소프트웨어 전달 성과 측면에서 뚜렷한 차이를 만들기 어려웠다고 설명한다. 이후 자동화 범위를 코드 생성에서 제품 개발 과정으로 확장했다.

~~~text
Sandbox + Agent + Prompt + PR
= automated coding cell

Work Intake
+ Planning
+ Durable Task
+ Execution
+ Verification
+ Delivery
+ Feedback
= software production system
~~~

여기서 가져올 핵심은 WorkOS의 제품명이 아니다. **제품 개발 과정까지 자동화해야 생산 시스템의 차이가 생긴다**는 경계다. PR 생성은 생산 시스템의 중요한 출력일 수 있지만 생산 시스템 자체와 동일하지 않다.

<!-- CASE C16: WorkOS - PR Factory에서 Product Engineering Factory로 -->

> **Case Study C16 — WorkOS — PR Factory에서 Product Engineering Factory로**
>
> WorkOS는 격리 환경과 코딩 에이전트로 PR을 만드는 초기 구조에서 출발했지만, 조직의 소프트웨어 전달 성과를 바꾸려면 제품 개발 과정 자체를 생산 시스템에 구현해야 한다고 설명한다. 제품 개발 문서 초안, 사람의 작업 범위 조정, 작업 티켓 분해, 의존 관계에 따른 실행, 계획 재평가, MCP Context Engine을 하나의 흐름으로 연결한다.
>
> 이 사례의 핵심은 특정 설계 구조가 아니라 **PR 생성은 생산 시스템의 출력일 수 있지만 생산 시스템 전체는 아니라는 것**이다.
>
> **주의:** 발표 후반의 메모리 계층과 일부 자체 개선 기능은 향후 방향으로 설명됐으며, 에이전트 권한 부여도 아직 해결 중인 문제로 언급된다.

---

## 2.1 왜 다시 Factory라는 표현인가

소프트웨어 생산 시스템이라는 말은 AI 시대에 처음 등장한 것이 아니다. 소프트웨어 공학은 오래전부터 반복 가능한 프로세스, 자동화, 표준화, 재사용 가능한 자산을 통해 생산성을 높이려 해왔다. 최근에는 소프트웨어 생산 시스템과 함께 무인 생산 시스템(Dark Factory) 같은 표현도 등장한다. 하지만 이 책에서는 사람이 보이지 않는가를 기준으로 생산 시스템을 정의하지 않는다.

작업이 중단돼도 기록이 남도록 관리되고, 실행이 통제되며, 결과가 독립적으로 검증되고, 실패 후 복구 가능한가를 더 중요한 경계로 본다. 이 책은 그 역사를 길게 다루지 않는다. 여기서 생산 시스템이라는 표현이 유용한 이유는 하나다.

> 작업을 개인의 순간적인 수행이 아니라 반복 가능한 시스템의 흐름으로 본다.

대화형 에이전트를 개인 도구로 사용할 때는 작업 상태가 개발자의 머릿속과 세션 안에 있어도 된다.

```text
Developer
→ Prompt
→ Agent Session
→ Result
```

하지만 작업이 길어지고 워커가 여러 개가 되고 재시도와 사람의 판단을 기다리는 시간이 생기면 다음 상태를 누군가는 알아야 한다.

- 작업의 목표와 완료 기준
- 어떤 코드 버전에서 시작했는가
- 어떤 시도가 실패했는가
- 누가 작업 중인가
- 어떤 검증이 통과했는가
- 무엇이 아직 남았는가
- 누가 승인해야 하는가

이 상태를 한 에이전트 세션에만 둘 수는 없다. 이때부터 개발은 세션의 연속이 아니라 **작업이 시스템을 통과하는 흐름**에 가까워진다. AI 시대에 생산 시스템이라는 표현이 다시 유용해지는 이유도 여기에 있다.

---

## 2.2 최소 정의를 검증해 보기

정의에 일부러 넣지 않은 것이 있다.

- 에이전트 수
- 특정 모델
- 특정 에이전트 프레임워크
- 완전 자율 병합
- 자동 할 일 목록 선택
- 자체 개선

이 기능들은 강력할 수 있지만 생산 시스템의 필수조건은 아니다. 예를 들어 다음과 같은 구조를 생각해보자.

```text
Human selects Task
      ↓
Durable Task Record
      ↓
One Isolated Worker
      ↓
Coding Agent
      ↓
Deterministic Verification
      ↓
Evidence
      ↓
Human Review
```

에이전트는 하나뿐이고 작업도 사람이 선택하며 병합도 사람이 승인한다. 그래도 대화형 에이전트와 중요한 차이가 있다. 작업 상태가 세션 밖에 남고, 실행환경이 분리되며, 결과가 검증되고, 워커가 실패해도 같은 작업을 재시도하거나 재배정할 수 있다. 반대로 에이전트를 20개 띄워도 모든 세션 상태를 사람이 직접 기억하고, 완료 판단을 에이전트의 “완료했습니다”라는 응답에 의존한다면 생산 시스템은 약하다.

> 생산 시스템의 핵심은 에이전트의 개수가 아니라 작업이 시스템 안에서 어떻게 관리되는가에 있다.

---

## 2.3 일곱 개 핵심 설계 속성

이 책에서는 이후 장에서 반복해서 사용할 설계 속성을 일곱 가지로 정리한다. 모두 첫 구현부터 완비해야 한다는 뜻은 아니다. 22장의 최소 기능 생산 시스템에서는 이 가운데 필요한 일부만으로 시작한다.

### 1. Durable Work

기본 단위는 지시문보다 오래 살아남는 작업이다.

```text
Prompt
= interaction

Task
= durable work item
```

작업에는 목표, 범위, 수용 판단, 상태, 시도, 워커, 검증, 근거 같은 정보가 연결될 수 있다. 핵심 원칙은 단순하다.

> 워커는 잃을 수 있어도 작업은 잃지 않는다.

자세한 상태 모델은 5장에서 다룬다.

### 2. Delegated Execution

에이전트는 답변만 만드는 것이 아니라 실제 실행환경에서 일한다. 저장소를 읽고 수정하며 빌드, 테스트, 브라우저, Git, 외부 도구를 사용한다. 따라서 에이전트에게는 모델뿐 아니라 워커와 실행환경이 필요하다. 이 경계는 7~9장에서 다룬다.

### 3. Controlled Autonomy

모든 결정을 에이전트에게 맡기지 않는다. 작업 상태, 재시도 한도, 권한, 필수 검증처럼 이미 규칙이 있는 것은 시스템이 관리하고, 저장소 탐색, 원인 진단, 구현 전략처럼 사전 규칙화하기 어려운 판단은 에이전트에 맡길 수 있다.

```text
Known Rule
→ System

Uncertain Search / Judgment
→ Agent
```

11장에서 이 경계를 자세히 다룬다.

### 4. Independent Verification

에이전트가 완료했다고 말하는 것과 작업이 실제로 완료된 것은 다르다.

```text
Agent Result
→ Verification
→ Evidence
→ Acceptance
```

컴파일, 테스트, 실행 중 검사, 화면 캡처, 보안 검사, 평가자, 사람의 검토 등 작업 위험에 맞는 검증이 필요하다. 핵심은 에이전트의 자기 보고와 완료 판정을 분리하는 것이다.

### 5. Recoverability

에이전트, 도구, 워커, 네트워크는 실패할 수 있다. 따라서 작업은 재시도, 처음부터 재시작, 중단 지점부터 재개, 다른 워커에 재배정, 사람에게 판단 요청 같은 복구 경로를 가질 수 있어야 한다. 정상 실행 경로보다 실패 후 같은 작업을 일관되게 이어갈 수 있는지가 더 중요하다.

### 6. Acceptance / Governance

실행 권한과 최종 위험을 받아들이는 권한은 다르다.

```text
Work Selection
Planning
Execution
Verification
Acceptance
Merge / Deploy
```

작업 위험에 따라 사람, 에이전트, 정책이 서로 다른 권한을 가질 수 있다. 생산 시스템은 사람의 검토를 없애는 시스템이 아니라 **최종 수용 권한을 명확히 하는 시스템**으로 보는 편이 낫다.

### 7. Feedback

작업 실행에서는 계속 새로운 정보가 나온다.

- 빠진 테스트
- 간헐적으로 실패하는 환경
- 반복되는 검토 의견
- 운영 환경 결함
- 부족한 도구
- 불명확한 요구사항

이 정보는 제품 수정이나 생산 시스템 개선으로 되돌아갈 수 있다. 피드백이 자동이어야 한다는 뜻은 아니다. 중요한 것은 실행 결과가 다음 개선에 사용할 수 있는 상태로 남는다는 것이다.

---

## 2.4 Factory가 아닌 것

정의를 더 명확하게 하려면 무엇과 다른지 봐야 한다.

### Multi-Agent System

여러 에이전트가 있다고 생산 시스템이 되는 것은 아니다. 여러 에이전트를 함께 쓰는 방식은 작업 배정 패턴이나 구현 전략일 수 있다. 최소 기능 생산 시스템은 에이전트 하나로도 성립할 수 있다.

```text
More Agents
≠ More Factory
```

### Agent Framework

에이전트 프레임워크는 모델 순환, 도구, 메모리, 하위 에이전트 같은 실행 기반을 제공할 수 있다. 생산 시스템은 그보다 넓은 소프트웨어 전달 상태를 다룬다.

```text
Requirement
Task
Repository
Commit
Build
Test
Approval
Release
Deployment
```

### Coding Agent Farm

여러 에이전트 세션을 사람이 각각 관리하면 사람의 주의와 노력이 사실상 제어 계층 역할을 한다. 중앙 작업 상태, 검증 규칙, 재시도 정책, 근거가 없다면 에이전트 수가 늘수록 관리 부담도 커질 수 있다.

### CI/CD + LLM

CI/CD는 생산 시스템의 중요한 기반이다.

```text
Source Change
→ Build
→ Test
→ Release
→ Deploy
```

생산 시스템은 여기에 요구사항·작업, 에이전트 작업, 재시도·승인, 피드백까지 연결할 수 있다. 기존 CI/CD를 대체하기보다 사용한다.

### Fully Autonomous Organization

소프트웨어 생산 시스템은 사람이 없는 개발 조직을 뜻하지 않는다. 작업 선택, 설계 구조, 수용 판단, 병합, 배포 권한을 사람이 유지해도 생산 시스템은 성립한다. 완전 자율화는 필수조건이 아니라 운영 정책의 한 선택지다.

---

## 2.5 하나의 Loop로 본다

여기서 생산 시스템을 두 개의 경계로 볼 수 있다. 좁은 의미에서는 이미 정의된 작업을 중단돼도 기록이 남도록 실행하고 검증하고 복구하는 **실행 시스템**이다. 넓은 의미에서는 신호와 의도를 작업으로 변환하는 앞단부터 전달 이후의 관찰과 개선까지 연결하는 **생산 루프**다.

Warp 창업자 Zach Lloyd는 2026년 발표에서 아이디어가 들어오면 에이전트가 문제를 분류하고, 복잡한 작업은 명세로 보내며, 구현·검토·검증·전달·관찰 결과를 다시 위쪽으로 되돌리는 소프트웨어 생산 시스템 순환을 제시했다. 이 책은 그 전망을 그대로 정의로 채택하지는 않지만, 생산 시스템의 경계가 코딩 에이전트 실행보다 넓어질 수 있다는 실제 사례로 사용한다.

지금까지의 요소를 연결하면 책 전체의 참조 순환이 된다.

```text
Intent / Signal
      ↓
Requirement / Specification
      ↓
Task / Acceptance
      ↓
Durable Control Plane
      ↓
Controlled Orchestration
      ↓
Worker / Sandbox
      ↓
Agent + Context + Tools
      ↓
Implementation
      ↓
Independent Verification
      ↓
Evidence
      ↓
Acceptance / Governance
      ↓
Delivery
      ↓
Feedback
      ↺
```

처음부터 모든 요소를 구현할 필요는 없다. 작은 팀은 다음 정도로 시작할 수 있다.

```text
Human selects Task
→ Task Record
→ One Worker
→ Coding Agent
→ Build / Test
→ Evidence
→ Human Review
```

중요한 것은 기능 목록보다 순서다. 신뢰성과 검증을 확인하기 전에 에이전트 수나 결정 권한부터 크게 늘리면 실패 원인을 구분하기 어려워진다. 이후 장에서는 이 순환을 작업 정의, 실행 구조, 검증과 복구, 전체 흐름 운영 순서로 분해한다.

---

소프트웨어 생산 시스템은 기존 소프트웨어 공학을 버리고 새 시스템으로 교체하는 개념이 아니다. 이미 조직에는 Git, 이슈 추적 도구, CI/CD, 테스트, 배포, 운영 감시, 개발자 플랫폼 같은 자산이 있다. 그렇다면 다음 질문이 생긴다.

> AI Software Factory는 기존 CI/CD, DevOps, Platform Engineering, 에이전트 플랫폼과 어디에서 겹치고 어디에서 달라지는가?

먼저 기존 전달 시스템과의 경계를 정리한다.

---

## 참고 자료

- Warp / Zach Lloyd, *Software Engineering Is Becoming Factory Engineering*  
  https://www.youtube.com/watch?v=tUPPVhBBcoM
- OpenAI, *An open-source spec for Codex orchestration: Symphony*  
  https://openai.com/index/open-source-codex-orchestration-symphony/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands*  
  https://www.anthropic.com/engineering/managed-agents
- NIST NCCoE, *Notional Reference Model for DevSecOps*  
  https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
- DORA, *Platform Engineering Capability*  
  https://dora.dev/capabilities/platform-engineering/
- Caylent, *What is a Software Factory*  
  https://www.youtube.com/watch?v=0Q8R_FZbnLk
- Caylent Solutions, *DevBench*  
  https://github.com/caylent-solutions/devbench
