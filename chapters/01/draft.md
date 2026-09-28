# 1장. Coding Agent가 좋아진 뒤 무엇이 병목이 되는가

몇 년 전까지만 해도 AI 코딩 도구의 가치는 비교적 설명하기 쉬웠다. 개발자가 코드를 작성하는 동안 다음 줄을 추천하고, 반복적인 코드를 대신 만들고, 모르는 API 사용법을 빠르게 알려주는 도구였다. 생산성에 대한 질문도 자연스럽게 개인 개발자의 작업 속도에 맞춰졌다.

> 이 도구를 쓰면 코드를 몇 퍼센트 더 빨리 작성할 수 있는가?

Coding Agent가 등장하면서 이 질문은 충분하지 않게 됐다.

지금의 Agent는 코드 조각만 제안하지 않는다. Repository를 탐색하고, 파일을 수정하고, Shell 명령을 실행하고, 테스트가 실패하면 다시 코드를 바꾸고, 경우에 따라 브라우저를 열어 실제 화면까지 확인한다. 작업을 잘 정의해 주면 개발자가 다른 일을 하는 동안 상당한 시간 동안 혼자 실행될 수도 있다.

이 변화는 단순히 “자동완성이 더 똑똑해졌다”는 수준이 아니다.

작업의 실행 주체가 달라지고 있다.

그런데 Agent가 더 많은 코드를 더 빨리 만들기 시작하면 이상한 일이 생긴다. 처음에는 병목이 줄어드는 것처럼 보이지만, 잠시 지나면 다른 곳에서 줄이 길어진다.

코드는 빨리 만들어졌는데 Pull Request가 쌓인다.  
Pull Request는 빨리 만들어졌는데 CI가 밀린다.  
CI는 통과했는데 Reviewer가 보지 못한다.  
Review는 끝났는데 Integration 과정에서 충돌이 난다.  
각각의 변경은 맞는데 합쳐 놓으니 시스템이 깨진다.

즉, 병목이 사라진 것이 아니라 이동한다.

이 책이 AI Software Factory를 이야기하는 출발점은 바로 여기다.

Agent가 코드를 얼마나 잘 쓰는지보다, **Agent가 만든 작업을 조직의 Software Delivery System이 얼마나 잘 흡수할 수 있는가**가 더 중요한 문제가 되기 시작한다.

---

## 1.1 Coding Assistant에서 Coding Agent로

Coding Assistant와 Coding Agent의 경계는 제품 이름으로 나누기 어렵다. 같은 제품도 어떤 방식으로 사용하느냐에 따라 Assistant처럼 동작할 수도 있고 Agent처럼 동작할 수도 있다.

그래서 이 책에서는 기능 목록보다 작업 방식으로 구분한다.

Coding Assistant의 기본 흐름은 대체로 다음과 같다.

```text
Developer
→ 질문 / 코드 작성
→ AI 응답
→ Developer 판단
→ 다음 행동
```

주도권과 작업 상태는 대부분 개발자에게 있다. AI는 한 번의 interaction 안에서 도움을 준다.

Coding Agent는 다르다.

```text
Task
→ Repository 탐색
→ 파일 수정
→ 명령 실행
→ Build / Test
→ 실패 분석
→ 수정
→ 재검증
→ Result
```

중간의 여러 단계를 Agent가 스스로 수행한다.

이 차이는 생각보다 크다.

예를 들어 개발자가 다음과 같이 요청한다고 해보자.

> 만료된 JWT가 들어오면 500이 아니라 401을 반환하도록 수정하고 관련 테스트를 통과시켜라.

Assistant 방식에서는 개발자가 관련 파일을 찾고, AI에게 코드를 물어보고, 수정 내용을 붙여 넣고, 직접 테스트를 실행하고, 실패 로그를 다시 AI에게 전달한다.

Agent 방식에서는 Repository를 읽을 수 있고 Shell을 실행할 수 있는 Agent가 관련 코드를 찾고, 테스트를 실행하고, 실패를 확인하고, 수정한 뒤 다시 테스트한다.

사람이 하던 여러 차례의 왕복이 하나의 작업 실행으로 묶인다.

여기서 중요한 점은 Agent의 가치가 단순히 코드를 생성하는 능력에만 있지 않다는 것이다.

Agent가 실제 Software Engineering 작업을 수행하려면 최소한 다음과 같은 요소가 함께 필요하다.

- Repository에 접근할 수 있어야 한다.
- 파일을 읽고 수정할 수 있어야 한다.
- Build와 Test를 실행할 수 있어야 한다.
- 실패 결과를 읽을 수 있어야 한다.
- 작업 중간의 상태를 유지할 수 있어야 한다.
- 완료 여부를 판단할 수 있는 피드백을 받아야 한다.

따라서 실제 Agent의 능력은 Model 하나로 설명하기 어렵다.

개념적으로 다음처럼 볼 수 있다.

```text
Model Capability
      ↓
Agent Capability
      ↓
Factory Capability
```

Model Capability는 코드를 이해하고 추론하고 생성하는 능력이다.

Agent Capability에는 여기에 Repository 접근, Tool 사용, Context, 실행환경, Feedback Loop가 더해진다.

Factory Capability는 한 단계 더 넓다. 여러 Task의 상태를 관리하고, 실패를 복구하고, 검증하고, Review와 Delivery까지 연결하는 시스템의 능력이다.

이 세 가지를 섞으면 문제가 생긴다.

Benchmark에서 높은 점수를 받은 Model을 도입했는데 실제 팀 생산성이 기대만큼 오르지 않을 수 있다. 반대로 가장 비싼 Model을 사용하지 않더라도 Repository 구조, 테스트, Tool, 실행환경이 잘 준비된 시스템에서는 훨씬 안정적인 결과를 낼 수 있다.

이 책에서는 이 차이를 계속 유지한다.

> 좋은 Model이 좋은 Factory를 자동으로 만들지는 않는다.

---

## 1.2 코드 생성 속도와 Delivery 속도는 다르다

소프트웨어 변경이 사용자에게 도달하기까지는 코드 작성 외에도 여러 단계가 있다.

단순화하면 다음과 같다.

```text
Requirement
→ Implementation
→ Review
→ Verification
→ Integration
→ Release
→ Production
```

기존에는 Implementation이 큰 비중을 차지하는 경우가 많았다. 개발자가 직접 코드를 작성하고, 오류를 고치고, 테스트를 추가하는 데 시간이 걸렸다.

Coding Agent는 이 구간을 빠르게 만들 수 있다.

문제는 나머지 단계의 처리 능력이 그대로일 수 있다는 것이다.

가령 어떤 팀에서 개발자 한 명이 하루에 Review 가능한 Pull Request를 평균 1개 만든다고 해보자. Reviewer 두 명이 하루에 합쳐 8개의 PR을 안정적으로 검토할 수 있다면 큰 문제가 없다.

이제 여러 Agent를 활용하면서 하루에 30개의 PR을 만들 수 있게 됐다고 하자.

코드 생성량은 크게 증가했다.

하지만 Reviewer가 처리할 수 있는 양이 여전히 8개라면 어떻게 될까.

```text
Agent Output:        30 PR / day
Review Capacity:      8 PR / day
--------------------------------
Review Queue:       +22 PR / day
```

첫날에는 생산성이 폭발적으로 좋아진 것처럼 보일 수 있다.

며칠이 지나면 stale PR이 늘어나고, base branch가 바뀌면서 conflict가 늘어나고, Reviewer는 더 많은 Context Switching을 겪게 된다. 오래 대기한 PR은 원래 작성 시점의 전제와 달라질 수도 있다.

Agent를 더 추가하면 이 문제는 해결되지 않는다.

오히려 더 빨리 악화될 수 있다.

이것은 전형적인 시스템 병목 문제다.

개념적으로 Factory의 처리량은 가장 느린 단계보다 빨라질 수 없다.

```text
Factory Throughput
≈ min(
  Ready Work,
  Worker Capacity,
  Verification Capacity,
  Review Capacity,
  Integration Capacity,
  Deployment Capacity
)
```

정확한 수학식이라기보다 사고 모델이다.

Worker를 2개에서 20개로 늘려도 Review Capacity가 그대로라면 전체 Delivery Throughput은 그만큼 늘지 않는다.

DORA의 AI 관련 연구가 중요한 이유도 여기에 있다. DORA는 AI를 고립된 개인 생산성 도구로 보기보다 기존 Delivery System의 강점과 약점을 증폭할 수 있는 요소로 본다. 코드 생성이 빨라졌을 때 테스트, Review, Security, Deployment가 충분히 받쳐주지 않으면 개선 효과가 downstream에서 흡수될 수 있다.

이를 한 문장으로 줄이면 다음과 같다.

> Agent가 빨라질수록 시스템의 느린 부분이 더 잘 보인다.

---

### 3분 수정, 2일 대기

조금 더 현실적인 Task 하나를 보자.

Agent가 작은 Bug를 수정하는 데 3분이 걸렸다.

Build와 Target Test에 5분이 걸렸다.

여기까지만 보면 8분짜리 작업이다.

하지만 실제 흐름은 다음과 같을 수 있다.

```text
09:00 Task 시작
09:03 Agent 수정 완료
09:08 Build / Test PASS
09:10 PR 생성
다음 날 15:00 Review 시작
15:30 수정 요청
15:35 Agent 재수정
15:40 Verification PASS
17:00 Merge
```

Agent Execution Time은 몇 분이다.

그러나 End-to-End Cycle Time은 하루가 넘는다.

여기서 “Agent가 3분 만에 고쳤다”는 말은 사실이지만 전체 생산성을 설명하지 못한다.

적어도 다음 시간을 분리해서 봐야 한다.

```text
Agent Execution Time
Human Blocking Time
Human Review Time
Verification Time
Queue Time
Total Task Cycle Time
```

비동기 Agent가 40분 동안 작업했다고 해서 개발자가 40분 동안 기다린 것도 아니다. 반대로 Agent가 3분 만에 끝냈다고 해서 조직이 3분 만에 변경을 전달한 것도 아니다.

Software Factory 관점에서는 이 차이가 중요하다.

---

## 1.3 Human Attention이 새로운 Capacity가 된다

Agent가 한두 개일 때는 사람이 직접 관리해도 된다.

작업을 하나 맡기고, 결과를 확인하고, 다음 작업을 맡긴다.

하지만 동시에 여러 Agent를 사용하기 시작하면 개발자는 곧 다른 종류의 일을 하게 된다.

- 어떤 Agent가 무슨 작업을 하고 있는지 확인한다.
- 중간 질문에 답한다.
- 완료됐다는 결과를 읽는다.
- 실패한 Agent를 다시 시작한다.
- Pull Request를 검토한다.
- 서로 충돌하는 변경을 조정한다.
- 어떤 작업을 다음에 맡길지 결정한다.

처음에는 “Agent가 나 대신 일한다”고 느꼈지만, 어느 순간 “내가 Agent들을 관리하고 있다”는 상태가 된다.

OpenAI가 Symphony를 공개하며 설명한 변화도 이 문제와 맞닿아 있다. 여러 interactive coding-agent session을 사람이 직접 관리하면 Context Switching과 Attention이 병목이 된다. 그래서 session 중심이 아니라 Task/Deliverable 중심으로 orchestration하는 방향이 등장한다.

여기서 한 가지 오해를 피해야 한다.

Software Factory의 목적이 사람을 없애는 것은 아니다.

오히려 사람의 Attention이 어디에 쓰이는지를 바꾸는 문제에 가깝다.

사람이 계속 해야 할 가능성이 높은 일은 다음과 같다.

- 무엇을 만들어야 하는가
- 요구사항의 의미가 무엇인가
- 어떤 Architecture가 적절한가
- 어떤 위험을 허용할 것인가
- 무엇을 완료라고 판단할 것인가
- 어떤 변경을 Production에 넣을 것인가

반면 반복적인 실행과 확인은 시스템으로 이동할 수 있다.

- Repository checkout
- 환경 준비
- 반복적인 테스트 실행
- 이미 정의된 Validation
- 실패 로그 수집
- Artifact 정리
- 상태 추적

따라서 좋은 Factory의 목표는 단순히 Human Intervention을 0으로 만드는 것이 아니다.

위험한 작업에서는 적절한 Human Gate가 반드시 필요할 수 있다.

더 적절한 질문은 이것이다.

> 사람이 한 개의 검증된 변경을 받아들이기 위해 얼마나 많은 Attention을 사용했는가?

개념적인 지표로 다음을 생각할 수 있다.

```text
Human Attention
----------------
Accepted Change
```

정확한 표준 Metric은 아니다. 하지만 Agent 시대의 생산성을 생각하는 데 유용한 방향을 준다.

Agent가 수십 개의 PR을 만들었지만 사람이 그것을 이해하고 수정하고 충돌을 해결하는 데 더 많은 시간을 쓰고 있다면 성공적인 Factory라고 보기 어렵다.

반대로 Agent 실행시간 자체는 길어도 사람이 일을 맡긴 뒤 다른 중요한 작업을 할 수 있고, 결과를 Evidence와 함께 짧게 Review할 수 있다면 가치가 있을 수 있다.

즉, Agent 시대에는 Latency뿐 아니라 **Attention과 Throughput**을 함께 봐야 한다.

---

## 1.4 생산성 연구가 서로 다른 이유

AI 코딩 도구의 생산성 효과를 이야기하면 서로 정반대처럼 보이는 수치가 자주 등장한다.

2025년 Microsoft Research가 세 개 회사의 Randomized Field Experiment를 통합 분석한 연구에서는 총 4,867명의 개발자를 대상으로 AI Coding Assistant 접근 효과를 분석했다. 이 연구에서는 AI 도구 사용군에서 completed task가 평균적으로 약 26% 더 많이 관찰됐다. 특히 경험이 적은 개발자에서 adoption과 gain이 더 큰 경향이 보고됐다.

반면 METR가 2025년에 진행한 연구에서는 전혀 다른 결과가 나왔다.

숙련된 오픈소스 개발자 16명이 자신이 잘 아는 성숙한 Repository에서 실제 Issue를 해결하게 했을 때, 당시 AI 도구를 사용한 경우 평균 작업 시간이 약 19% 늘어났다.

더 흥미로운 부분은 개발자의 인식이었다.

실제 측정 결과는 느려졌지만 참여 개발자들은 AI가 자신을 대략 20% 정도 빠르게 만들었다고 예상했다.

어느 연구가 맞을까.

둘 다 자신의 조건 안에서는 의미가 있다.

다만 두 결과를 같은 질문의 답처럼 비교하면 안 된다.

연구 조건이 다르기 때문이다.

- 사용한 AI 도구의 세대가 다르다.
- Task 종류가 다르다.
- Repository familiarity가 다르다.
- 개발자 숙련도가 다르다.
- 작업 시간이 다르다.
- 생산성의 정의가 다르다.

Microsoft 연구는 기업 환경에서 completed task 수를 중심으로 봤다.

METR 연구는 숙련 개발자가 자신이 잘 아는 Repository에서 특정 Task를 끝내는 실제 시간을 측정했다.

더구나 Agentic Workflow가 발전하면서 측정 자체가 어려워지고 있다.

METR는 2026년 후속 실험을 진행하며 새로운 문제를 보고했다. AI 없이 작업하기를 원하지 않는 개발자가 연구 참여를 거부하면서 selection bias가 생기고, 한 개발자가 여러 Agent를 동시에 운영하면 “이 Task에 사람이 정확히 몇 분을 썼는가”를 재기 어려워진다는 것이다.

예전의 생산성 측정은 다음과 같은 그림을 가정하기 쉬웠다.

```text
Developer
→ Task A
→ 완료
→ Task B
→ 완료
```

Agentic Workflow에서는 다음처럼 될 수 있다.

```text
Developer
├─ Agent A → Task A
├─ Agent B → Task B
└─ 직접    → Task C

40분 뒤
├─ A Review
├─ B Retry
└─ C 계속 진행
```

어느 시간을 Task A의 생산성으로 계산해야 할까.

Agent가 실행된 40분인가.

개발자가 처음 지시한 3분인가.

Review한 8분까지 더해야 하는가.

중간에 Agent가 잘못 수정해서 사람이 20분간 고쳤다면 그것도 포함해야 하는가.

이 때문에 AI 시대의 생산성은 “개발자가 코딩에 쓴 시간” 하나로 설명하기 어려워진다.

METR는 productivity uplift를 생각할 때 기존 작업을 얼마나 빨리 하는지뿐 아니라, AI가 있기 때문에 새롭게 수행하게 된 작업과 전체 value 변화도 구분할 필요가 있다고 제안한다.

이 구분은 Software Factory에서 특히 중요하다.

예전에는 비용이 아까워 생략했던 일을 Agent가 수행할 수 있기 때문이다.

- 테스트 추가
- Documentation 보강
- Dependency Update
- Screenshot QA
- Accessibility Check
- Migration Validation
- 로그 조사
- 반복적인 Refactoring

기존 Task 하나를 30% 빨리 끝내는 것만이 가치가 아니다.

Task Mix 자체가 달라질 수 있다.

따라서 이 책에서는 “AI는 개발자를 몇 % 빠르게 만든다”는 하나의 숫자를 제시하지 않는다.

대신 다음 질문을 사용한다.

> 어떤 Task에서, 어떤 개발자가, 어떤 Workflow로, 어떤 품질과 Review 비용을 포함했을 때 실제 end-to-end value가 증가했는가?

---

## 1.5 최적화 단위를 바꾼다

AI Coding Agent를 처음 도입하면 눈에 잘 보이는 숫자를 측정하기 쉽다.

- 사용한 Token 수
- Agent 실행 횟수
- 생성한 코드 줄 수
- 만든 Pull Request 수
- Benchmark 점수
- Agent가 Task를 끝낸 시간

이 숫자들이 쓸모없다는 뜻은 아니다.

문제는 이것을 최종 목표로 사용할 때 생긴다.

예를 들어 Agent A와 Agent B를 비교해 보자.

Agent A는 Token을 적게 쓴다. 하지만 네 번 Retry한 뒤 PR을 만들고, Reviewer가 크게 수정해야 한다.

Agent B는 Token을 두 배 사용한다. 하지만 첫 시도에서 Test를 통과하고 Reviewer가 거의 수정하지 않고 Merge한다.

Token 기준으로는 A가 효율적이다.

조직 비용 기준으로는 B가 더 나을 수 있다.

이를 조금 더 넓게 보면 Factory의 비용은 다음 요소를 포함한다.

```text
Total Cost
=
Model
+ Compute
+ Sandbox
+ CI
+ Storage
+ Review
+ Retry
+ Failure / Rework
```

따라서 유용한 후보 지표 중 하나는 다음과 같다.

```text
Cost per Accepted Change
```

물론 이것도 완벽한 지표는 아니다.

문서 수정 한 건과 결제 시스템 변경 한 건은 가치와 위험이 다르다. 코드 변경을 작은 조각으로 쪼개면 Accepted Change 수 자체를 인위적으로 늘릴 수도 있다.

중요한 것은 숫자 하나를 표준으로 선언하는 것이 아니라 **측정 boundary를 Agent에서 Delivery System으로 넓히는 것**이다.

다음과 같이 계층을 분리할 수 있다.

```text
Agent Efficiency
      ↓
Developer Productivity
      ↓
Team Flow
      ↓
Delivery Performance
      ↓
Business Value
```

한 단계의 개선이 다음 단계의 개선을 보장하지 않는다.

Agent의 Benchmark Score가 올랐다고 Team Flow가 개선되는 것은 아니다.

Developer가 코드를 더 빨리 작성했다고 Production Incident가 줄어드는 것도 아니다.

PR 수가 늘었다고 사용자에게 더 많은 가치가 전달된 것도 아니다.

이 책에서 Factory를 이야기할 때 계속 확인해야 할 기준은 그래서 단순하다.

> 검증된 변경이 실제로 더 잘 흐르고 있는가?

이를 보기 위한 Factory-level 지표는 다음과 같은 것들이 될 수 있다.

- Task Cycle Time
- Queue Time
- Verification Time
- Human Blocking Time
- Review Time
- First-pass Acceptance Rate
- Retry Rate
- Rejection Rate
- Revert
- Escaped Defect
- Human Intervention
- Cost per Accepted Change

이 지표들이 모두 항상 필요한 것은 아니다.

Minimum Viable Factory에서는 몇 개만 기록해도 된다.

예를 들어 처음에는 다음 정도로 시작할 수 있다.

```text
Task
- created_at
- started_at
- verified_at
- done_at

Human
- intervention_count
- review_minutes

Quality
- verification_pass
- retry_count
- accepted
```

이 정도만 있어도 중요한 질문에 답할 수 있다.

Agent를 추가한 뒤 Task Cycle Time이 실제로 줄었는가.

Retry는 늘었는가.

Review Queue는 길어졌는가.

사람이 중간에 개입하는 횟수는 줄었는가.

Agent는 더 빨라졌는데 Accepted Change까지 걸리는 시간은 그대로인 것은 아닌가.

이 질문을 하기 시작하면 관점이 바뀐다.

관심의 중심이 Model에서 System으로 이동한다.

---

## 병목을 없애는 것이 아니라 관리한다

Software Factory라는 표현은 자칫 모든 것이 끊김 없이 자동으로 흘러가는 완벽한 생산라인을 떠올리게 한다.

실제 소프트웨어 개발은 그렇게 단순하지 않다.

요구사항은 바뀌고, 테스트는 불완전하고, Production 환경은 예상과 다르며, Agent도 실패한다.

Factory의 목적은 이런 불확실성을 없애는 것이 아니다.

어디에서 Work가 멈췄는지 알고, 왜 멈췄는지 확인하고, 다음 행동을 결정할 수 있는 시스템을 만드는 것이다.

Coding Agent의 능력이 좋아질수록 이 문제가 더 중요해진다.

Agent가 느릴 때는 한 번에 몇 개의 작업만 들어오므로 사람이 직접 관리해도 된다.

Agent가 빨라지고 여러 개를 동시에 실행할 수 있게 되면 더 이상 사람의 머릿속과 여러 터미널 창만으로는 충분하지 않다.

작업 상태가 필요하다.

검증 기준이 필요하다.

실패를 처리할 방법이 필요하다.

Review Capacity를 알아야 한다.

어떤 Task를 시작하면 안 되는지도 알아야 한다.

이때부터 문제는 “좋은 Coding Agent를 어떻게 쓰는가”에서 “Agent를 포함한 Software Production System을 어떻게 설계하는가”로 바뀐다.

다음 장에서는 이 시스템을 이 책에서 **AI Software Factory**라고 부르는 이유와, Factory라고 부르기 위한 최소 구성요소가 무엇인지 정의한다.

---

## 이 장의 핵심 정리

Coding Agent가 좋아졌다고 Software Delivery 전체가 자동으로 좋아지는 것은 아니다.

```text
Implementation이 빨라지면
→ Review가 병목이 될 수 있다.

Review가 빨라지면
→ Verification이 병목이 될 수 있다.

Verification이 빨라지면
→ Integration이나 Deployment가 병목이 될 수 있다.
```

따라서 Factory는 특정 단계의 속도가 아니라 전체 흐름을 본다.

그리고 다음 세 가지를 구분한다.

```text
Model Capability
Agent Capability
Factory Capability
```

AI 생산성 역시 하나의 숫자로 설명하지 않는다.

Task, 개발자, Workflow, 품질, Review, Retry, Rework를 함께 봐야 한다.

이 책에서 앞으로 반복해서 사용할 기준은 다음이다.

> AI Software Factory가 최적화해야 할 것은 Agent 수나 코드 생성량이 아니라, 사람이 감당 가능한 Attention 안에서 검증된 소프트웨어 변경이 지속적으로 전달되는 전체 흐름이다.

---

## 참고 자료

- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  https://openai.com/index/harness-engineering/
- OpenAI, *An open-source spec for Codex orchestration: Symphony*  
  https://openai.com/index/open-source-codex-orchestration-symphony/
- DORA, *2025 DORA Report*  
  https://dora.dev/research/2025/dora-report/
- DORA, *Balancing AI tensions*  
  https://dora.dev/insights/balancing-ai-tensions/
- Microsoft Research, *The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers*  
  https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/
- METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*  
  https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- METR, *We are Changing our Developer Productivity Experiment Design*  
  https://metr.org/blog/2026-02-24-uplift-update/
- METR, *Task Substitution and Uplift*  
  https://metr.org/blog/2026-05-08-task-substitution-and-uplift/
