# 2장. AI Software Factory란 무엇인가

1장에서 본 문제는 단순했다.

Coding Agent가 빨라져도 Software Delivery 전체가 같은 속도로 빨라지는 것은 아니다. 작업이 늘어나면 Review, CI, Integration, Human Attention 같은 다른 단계가 병목이 된다.

그렇다면 다음 질문이 남는다.

> Agent를 포함한 Software Production System을 어디까지 갖춰야 Software Factory라고 부를 수 있을까?

이 질문에 답하려면 먼저 몇 가지 오해를 걷어낼 필요가 있다.

Software Factory는 Agent를 여러 개 띄우는 시스템과 같은 말이 아니다.  
완전 자율 Merge가 가능한 시스템만 Factory인 것도 아니다.  
CI/CD에 LLM 호출을 하나 추가했다고 자동으로 Factory가 되는 것도 아니다.

이 책에서는 AI Software Factory를 다음과 같이 정의한다.

> **AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.**

이 정의에서 중요한 단어는 Agent보다 오히려 다른 곳에 있다.

**durable하게 관리되는 Work**,  
**실행 위임**,  
**독립된 검증**,  
**실패 복구**,  
**지속적인 전달**이다.

Agent는 이 시스템의 중요한 Worker다.

하지만 Factory 전체는 아니다.

---

## 2.1 왜 다시 Factory라는 표현인가

Software Factory라는 표현은 AI 시대에 처음 등장한 말이 아니다.

과거에도 Software Engineering은 반복 가능한 개발 프로세스, 자동화 도구, 표준화된 생산 방식, 재사용 가능한 자산을 통해 소프트웨어 생산성을 높이려는 시도를 계속해 왔다.

이 책은 그 역사를 길게 다루지 않는다.

중요한 것은 "Factory"라는 단어가 가진 한 가지 성질이다.

> 작업을 개인의 순간적인 수행이 아니라 반복 가능한 시스템의 흐름으로 본다.

전통적인 개발에서는 한 명의 개발자가 상당한 작업 상태를 머릿속에 가지고 있었다.

무엇을 고치고 있는지, 어디까지 수정했는지, 어떤 테스트가 실패했는지, 다음에 무엇을 할지 개발자 자신이 기억했다.

Coding Agent를 개인 도구로 사용할 때도 처음에는 비슷하다.

```text
Developer
→ Prompt
→ Agent Session
→ Result
```

작업 상태는 대화와 개발자의 머릿속에 있다.

Agent가 하나이고 작업이 짧다면 충분하다.

하지만 작업이 길어지고, Agent가 여러 개가 되고, 사람이 중간에 자리를 비우고, Worker가 죽고, 재시도가 발생하면 이야기가 달라진다.

누군가는 다음 상태를 알아야 한다.

- 이 Task의 목표는 무엇인가
- 어떤 Revision에서 시작했는가
- 누가 작업 중인가
- 어떤 시도가 실패했는가
- 어떤 검증이 통과했는가
- 무엇이 아직 남았는가
- Human Approval이 필요한가
- 다음에 누가 이어받을 수 있는가

이 상태를 한 Agent Session에만 둘 수는 없다.

이때부터 개발은 개인 Session의 연속이 아니라 **Work가 시스템을 통과하는 흐름**에 가까워진다.

AI 시대에 Factory라는 표현이 다시 유용해지는 이유도 여기에 있다.

코드 생성을 자동화해서가 아니라, **작업의 생산과 검증을 반복 가능한 시스템으로 만들 필요가 커졌기 때문**이다.

---

## 2.2 책의 최소 정의

앞에서 제시한 정의를 다시 보자.

> AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템이다.

이 정의는 일부러 몇 가지를 넣지 않았다.

- Agent 수
- 특정 Model
- 특정 Agent Framework
- Fully Autonomous Merge
- Automatic Backlog Selection
- Self-improvement

이 기능들은 강력할 수 있다.

하지만 Factory의 최소 조건은 아니다.

예를 들어 다음과 같은 시스템을 생각해보자.

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

Agent는 하나뿐이다.

Task도 사람이 선택한다.

Merge도 사람이 승인한다.

그럼에도 이 시스템은 단순한 Interactive Agent와 중요한 차이가 있다.

작업 상태가 Session 밖에 남아 있고, 실행환경이 분리되어 있으며, 결과가 검증되고, Evidence를 가지고 사람이 승인한다.

Worker가 실패했을 때 Task 자체는 남아 있다면 재시도나 재배정도 가능하다.

이 책에서는 이런 구조도 충분히 Software Factory의 초기 형태로 본다.

반대로 Agent를 20개 띄워도 다음과 같다면 Factory라고 보기 어렵다.

```text
Human
├─ Agent Session A
├─ Agent Session B
├─ Agent Session C
├─ ...
└─ Agent Session T
```

각 Session의 상태를 사람이 직접 기억한다.

누가 무엇을 하는지 별도의 Task State가 없다.

완료 판단은 Agent의 "완료했습니다"라는 응답에 의존한다.

Worker가 죽으면 어디까지 했는지 알기 어렵다.

Agent 수는 많지만 생산 시스템은 약하다.

이 차이가 중요하다.

> Factory의 핵심은 Agent의 개수가 아니라 Work가 시스템 안에서 어떻게 관리되는가에 있다.

---

## 2.3 일곱 개 핵심 설계 속성

이 책에서는 AI Software Factory를 설명할 때 반복해서 사용할 설계 속성을 일곱 가지로 정리한다.

이 일곱 가지가 모두 첫 구현부터 완비되어야 한다는 뜻은 아니다. 22장의 Minimum Viable Factory는 이 가운데 필요한 일부를 작은 흐름으로 시작한다. 여기서는 이후 장에서 사용할 공통 언어를 먼저 정리한다.

### 1. Durable Work

Factory의 기본 단위는 Prompt가 아니라 Task다.

Prompt는 한 번의 상호작용이다.

Task는 더 오래 살아남는다.

```text
Prompt
= interaction

Task
= durable work item
```

Task에는 다음과 같은 정보가 연결될 수 있다.

- Goal
- Scope
- Acceptance Criteria
- Dependency
- Status
- Attempt
- Worker
- Base Revision
- Result Revision
- Verification
- Evidence
- Approval
- Failure / Retry Reason

모든 필드를 처음부터 가져야 한다는 뜻은 아니다.

핵심은 Agent Session이 사라져도 Task가 남아야 한다는 것이다.

뒤에서 더 자세히 다루겠지만 이 책의 중요한 원칙은 다음 문장으로 요약할 수 있다.

> Worker는 잃을 수 있어도 Task는 잃지 않는다.

---

### 2. Delegated Execution

Factory의 Agent는 답변만 만드는 것이 아니라 실제 실행환경에서 일한다.

예를 들면 다음과 같다.

- Repository checkout
- 파일 수정
- Shell 명령
- Build
- Test
- Browser
- Service 실행
- Git 작업
- 외부 Tool 호출

따라서 Agent에게는 "두뇌"뿐 아니라 "손"이 필요하다.

이 실행환경은 Local Worktree일 수도 있고 Container나 VM일 수도 있다.

중요한 것은 Agent가 실제 작업을 수행하고 결과를 남길 수 있다는 점이다.

---

### 3. Controlled Autonomy

Factory는 모든 결정을 Agent에게 넘기는 시스템이 아니다.

오히려 어떤 결정은 시스템이 강제하고, 어떤 결정만 Agent에게 맡기는 구조가 필요하다.

예를 들어 다음은 deterministic system이 관리하기 좋다.

- Task 상태
- Retry 횟수
- Timeout
- Dependency
- Permission
- Budget
- 필수 검증
- Approval 상태

반대로 다음은 Agent가 강점을 보일 수 있다.

- Repository 탐색
- 원인 진단
- 가설 수립
- 구현 전략
- 디버깅 경로
- 여러 대안 비교

왜 구분해야 할까.

이미 알고 있는 규칙을 매번 LLM에게 다시 판단시키면 비용과 변동성이 늘어난다.

```text
main branch 직접 push 금지
```

같은 규칙은 Prompt에 "하지 마라"고 적어두는 것보다 Branch Protection이나 Permission으로 막는 편이 낫다.

Factory에서 Autonomy는 "Agent에게 다 맡긴다"는 뜻이 아니다.

**불확실한 판단에 Agent를 쓰고, 확정된 규칙은 시스템에 둔다**는 의미에 더 가깝다.

---

### 4. Independent Verification

Agent가 완료했다고 말하는 것과 Task가 실제로 완료된 것은 다르다.

```text
Agent
→ "DONE"

Factory
→ ?
```

중간에 검증이 필요하다.

```text
Agent Result
→ Verification
→ Evidence
→ Acceptance
```

검증은 Task에 따라 다르다.

- Compile
- Lint
- Unit Test
- Integration Test
- E2E
- Browser 확인
- Screenshot
- Security Scan
- Benchmark
- Evaluator Agent
- Human Review

여기서 "Independent"라는 단어가 중요하다.

Agent가 스스로 "테스트를 돌렸고 문제없다"고 말하는 것만으로 끝내지 않는다.

검증 결과가 시스템이나 별도의 검증 주체를 통해 확인 가능해야 한다.

뒤에서 살펴보겠지만 Test PASS조차 User Intent 전체를 보장하지는 않는다.

Factory는 Agent의 자연어 보고와 완료 판정을 분리해야 한다.

---

### 5. Recoverability

Agent는 실패한다.

Tool도 실패한다.

Worker도 죽는다.

Network도 끊긴다.

CI도 flaky할 수 있다.

그래서 Factory 정의에 Recovery가 들어간다.

실패가 발생했을 때 선택지는 하나가 아니다.

```text
Tool Retry
→ Step Retry
→ Agent Nudge
→ Worker Restart
→ Reassignment
→ Human Escalation
```

중요한 것은 "다시 실행" 버튼이 있다는 사실이 아니다.

어디까지 진행했는지 알고, 어떤 상태를 보존해야 하며, 같은 side effect를 중복 실행하지 않도록 하는 구조가 필요하다.

Software Factory Architecture의 품질은 한 번의 happy path보다 **실패 후에도 같은 Task가 일관되게 끝날 수 있는가**에서 더 잘 드러난다.

---

### 6. Acceptance / Governance

Agent가 실행할 수 있다고 해서 최종 승인 권한까지 가져야 하는 것은 아니다.

다음 권한은 서로 다르다.

- Work Selection
- Planning
- Execution
- Verification
- Acceptance
- Merge
- Deploy

예를 들어 Agent가 코드를 작성하고 테스트까지 끝낼 수 있지만 Merge는 사람이 승인할 수 있다.

실제로 공개된 여러 운영 사례에서 이런 형태가 나타난다.

반대로 낮은 위험의 문서 수정이나 deterministic한 maintenance 작업은 Policy에 따라 자동 승인할 수도 있다.

중요한 것은 Human Review가 항상 필요한가 아닌가를 하나의 정답으로 만드는 것이 아니다.

Task 위험에 따라 **누가 최종 위험을 받아들이는지 명확히 하는 것**이다.

---

### 7. Feedback

Factory는 Task 하나를 끝내고 사라지는 시스템이 아니다.

실행 과정에서 계속 새로운 정보가 나온다.

- missing test
- flaky environment
- 느린 build
- 잘못된 instruction
- 반복되는 review comment
- production defect
- 부족한 Tool
- 불명확한 Requirement

이 피드백은 다음 작업으로 돌아갈 수 있다.

```text
Product Failure
→ Regression Test

Repeated Agent Failure
→ Skill / Tool / Context Improvement

Review Rejection
→ Acceptance / Eval Improvement

Production Incident
→ New Task
```

Feedback이 자동이어야 한다는 뜻은 아니다.

중요한 것은 Factory가 작업 결과에서 학습 가능한 구조를 가져야 한다는 것이다.

---

## 2.4 Factory가 아닌 것

정의를 더 명확하게 하려면 무엇이 아닌지도 볼 필요가 있다.

### Multi-Agent System과 같지 않다

Agent가 여러 개 있다고 Factory가 되는 것은 아니다.

Multi-Agent는 하나의 Scheduling Pattern이거나 구현 전략이다.

Task가 독립적일 때 여러 Worker를 병렬 실행하면 효과적일 수 있다.

반대로 같은 Schema나 Core File을 동시에 수정하면 Coordination Cost와 Merge Conflict가 더 커질 수 있다.

즉 다음 등식은 성립하지 않는다.

```text
More Agents
= More Factory
```

Minimum Viable Factory는 Agent 하나로도 만들 수 있다.

---

### Agent Framework와 같지 않다

Agent Framework는 Model Loop, Tool 호출, Memory, Subagent, Context 같은 실행 기반을 제공할 수 있다.

하지만 Software Factory에는 그보다 더 넓은 Software Delivery 상태가 필요하다.

- Requirement
- Task
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

Agent Framework는 Factory의 일부를 구현할 수 있다.

Factory 전체와 같은 것은 아니다.

---

### Coding Agent Farm과 같지 않다

Agent를 여러 개 띄우고 사람이 각각 관리하는 구조를 생각해보자.

```text
Human
→ Agent A
→ Agent B
→ Agent C
→ Agent D
```

각 Agent가 빠르게 일하더라도 중앙의 Task State, 검증 규칙, Retry Policy, Evidence Contract가 없다면 사람의 Attention이 Control Plane 역할을 하게 된다.

규모가 커질수록 이 구조는 관리하기 어려워진다.

Factory는 Agent 수보다 **시스템이 Work를 책임지는 정도**가 중요하다.

---

### CI/CD에 LLM을 붙인 것과 같지 않다

CI/CD는 이미 Software Factory의 중요한 기반이다.

```text
Source Change
→ Build
→ Test
→ Package
→ Release
→ Deploy
```

여기에 Agent를 넣을 수 있다.

```text
CI Failure
→ Agent Analysis
→ Fix
→ CI Retry
```

하지만 이것만으로 Factory 전체가 되는 것은 아니다.

Factory는 CI/CD보다 앞단의 Requirement/Task와 실행 중의 Retry/Approval, 뒤쪽의 Feedback까지 포함할 수 있다.

3장에서 이 경계를 더 자세히 다룬다.

---

### Fully Autonomous Organization과 같지 않다

Software Factory라는 표현을 들으면 사람이 거의 없는 개발 조직을 떠올리기 쉽다.

이 책에서는 그렇게 정의하지 않는다.

사람이 다음 권한을 가지고 있어도 Factory는 성립한다.

- Task 선택
- Requirement 승인
- Architecture 결정
- Risk 승인
- Merge
- Deploy

Agent는 실행 권한만 많이 가질 수도 있다.

완전 자율화는 Factory의 필수조건이 아니라 **운영 정책의 한 선택지**다.

---

## 2.5 Factory를 하나의 Loop로 본다

지금까지의 요소를 하나의 흐름으로 연결하면 다음과 같다.

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

이 그림을 처음 보면 상당히 커 보일 수 있다.

처음부터 모든 요소를 구현해야 한다는 뜻은 아니다.

실제로는 훨씬 작게 시작할 수 있다.

예를 들어 작은 팀이라면 다음만으로 시작할 수 있다.

```text
Human selects Task
      ↓
Task Record
      ↓
One Worker
      ↓
Coding Agent
      ↓
Build / Test
      ↓
Evidence
      ↓
Human Review
```

이 구조가 반복 가능하고, Worker가 실패해도 Task를 복구할 수 있고, 결과를 검증할 수 있다면 이미 중요한 Factory 성질을 갖는다.

그다음 실제 병목과 실패를 관찰하면서 확장한다. Retry/Resume가 먼저 필요할 수도 있고, 반복되는 CI 실패처럼 명확한 Work Source가 있다면 Event Trigger를 먼저 붙일 수도 있다. 중요한 것은 기능 목록의 순서보다 **Reliability와 Verification을 확인하기 전에 Agent 수나 Decision Authority부터 크게 늘리지 않는 것**이다.

이후 장에서는 이 Loop를 Work 정의, 실행 구조, 검증과 복구, 전체 Flow 운영 순서로 분해한다.

---

## 이 장에서 남는 질문

지금까지의 정의만으로도 한 가지는 분명해진다.

Software Factory는 기존 Software Engineering을 버리고 새 시스템으로 교체하는 개념이 아니다.

이미 대부분의 조직에는 다음이 있다.

- CI/CD
- Issue Tracker
- Git
- Test
- Review
- Deployment
- Monitoring
- Developer Platform

그렇다면 다음 질문이 생긴다.

> AI Software Factory는 기존 CI/CD, DevOps, Platform Engineering, Agent Platform과 정확히 어디에서 겹치고 어디에서 달라지는가?

다음 장에서는 이 경계를 정리한다.

---

## 참고 자료

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
