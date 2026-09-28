# 1장. Coding Agent가 좋아진 뒤 무엇이 병목이 되는가

몇 년 전까지 AI 코딩 도구의 가치는 비교적 설명하기 쉬웠다. 개발자가 코드를 작성하는 동안 다음 줄을 추천하고, 반복 코드를 만들고, 모르는 API 사용법을 빠르게 알려주는 도구였다. 생산성 질문도 자연스럽게 개인 개발자의 작업 속도에 맞춰졌다.

> 이 도구를 쓰면 코드를 얼마나 더 빨리 작성할 수 있는가?

Coding Agent가 등장하면서 이 질문만으로는 부족해졌다.

지금의 Agent는 코드 조각만 제안하지 않는다. Repository를 탐색하고, 파일을 수정하고, Shell 명령을 실행한다. 테스트가 실패하면 원인을 찾고 코드를 다시 바꾼다. 경우에 따라 브라우저를 열어 실제 화면까지 확인한다. 작업이 충분히 명확하면 개발자가 다른 일을 하는 동안 비동기적으로 실행될 수도 있다.

문제는 Agent가 더 많은 코드를 더 빨리 만들기 시작한 다음부터다.

코드는 빨리 만들어졌는데 Pull Request가 쌓인다.  
Pull Request는 늘었는데 CI가 밀린다.  
CI는 통과했는데 리뷰가 대기한다.  
리뷰가 끝났는데 통합 과정에서 충돌한다.  
각각의 변경은 맞는데 합쳐 놓으니 시스템이 깨진다.

병목이 없어진 것이 아니라 다른 단계로 이동한 것이다.

이 책이 AI Software Factory를 이야기하는 출발점은 여기다.

Agent가 코드를 얼마나 잘 쓰는지뿐 아니라, **Agent가 만든 작업을 Software Delivery System이 얼마나 잘 흡수할 수 있는가**를 함께 봐야 한다.

---

## 1.1 Coding Assistant에서 Coding Agent로

Coding Assistant와 Coding Agent를 제품 이름으로 구분하기는 어렵다. 같은 제품도 어떤 방식으로 사용하느냐에 따라 Assistant처럼 동작할 수도 있고 Agent처럼 동작할 수도 있다.

이 책에서는 기능 목록보다 작업 방식으로 구분한다.

Coding Assistant의 기본 흐름은 다음과 비슷하다.

```text
Developer
→ 질문 / 코드 작성
→ AI 응답
→ Developer 판단
→ 다음 행동
```

작업의 주도권과 상태는 대부분 개발자에게 있다. AI는 한 번의 상호작용 안에서 도움을 준다.

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

중간 단계의 상당 부분을 Agent가 직접 수행한다.

예를 들어 다음 작업을 생각해 보자.

> 만료된 JWT가 들어오면 500이 아니라 401을 반환하도록 수정하고 관련 테스트를 통과시켜라.

Assistant 방식에서는 개발자가 관련 파일을 찾고, AI에게 코드를 묻고, 수정 내용을 적용하고, 직접 테스트를 실행한다. 실패 로그가 나오면 다시 AI에게 전달한다.

Agent 방식에서는 Repository와 Shell에 접근할 수 있는 Agent가 관련 코드를 찾고, 테스트를 실행하고, 실패를 확인하고, 수정한 뒤 다시 검증한다.

사람이 하던 여러 차례의 왕복이 하나의 작업 실행으로 묶인다.

이때 Agent의 능력은 Model 하나로 설명하기 어렵다. 실제 Software Engineering 작업을 수행하려면 다음 요소가 함께 필요하다.

- Repository 접근
- 파일 읽기와 수정
- Build / Test 실행
- 실패 결과 해석
- 작업 중 상태 유지
- 완료 여부를 판단할 피드백

그래서 이 책에서는 다음 세 수준을 구분한다.

```text
Model Capability
      ↓
Agent Capability
      ↓
Factory Capability
```

**Model Capability**는 코드를 이해하고 추론하고 생성하는 능력이다.

**Agent Capability**에는 Repository 접근, Tool 사용, Context, 실행환경, 피드백 루프가 추가된다.

**Factory Capability**는 더 넓다. 여러 Task의 상태를 관리하고, 실패를 복구하고, 검증하고, 리뷰와 전달까지 연결하는 시스템의 능력이다.

Benchmark가 높은 Model을 도입했다고 팀 생산성이 같은 비율로 좋아지는 것은 아니다. 반대로 가장 비싼 Model을 사용하지 않아도 Repository 구조, 테스트, Tool, 실행환경이 잘 준비돼 있으면 더 안정적인 결과를 낼 수 있다.

> 좋은 Model이 좋은 Factory를 자동으로 만들지는 않는다.

---

## 1.2 코드 생성 속도와 Delivery 속도는 다르다

소프트웨어 변경이 사용자에게 도달하기까지는 코드 작성 외에도 여러 단계가 있다.

```text
Requirement
→ Implementation
→ Review
→ Verification
→ Integration
→ Release
→ Production
```

Coding Agent는 Implementation 구간을 빠르게 만들 수 있다. 하지만 나머지 단계의 처리 능력은 그대로일 수 있다.

단순한 가상 예를 들어보자.

여러 Agent를 활용해 하루에 30개의 Pull Request를 만들 수 있게 됐다고 하자. 그런데 Reviewer가 안정적으로 처리할 수 있는 양이 하루 8개라면 어떻게 될까.

```text
Agent Output:        30 PR / day
Review Capacity:      8 PR / day
--------------------------------
Review Queue:       +22 PR / day
```

처음에는 생산성이 크게 좋아진 것처럼 보인다.

하지만 며칠이 지나면 리뷰 대기열이 늘고, 오래 대기한 PR은 base branch 변화 때문에 충돌 가능성이 커진다. Reviewer는 더 많은 Context Switching을 겪는다.

여기에 Agent를 더 추가해도 해결되지 않는다.

개념적으로 Factory의 처리량은 가장 느린 단계에 제한된다.

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

정확한 수학식이라기보다 병목을 찾기 위한 사고 모델이다.

Worker를 2개에서 20개로 늘려도 Review Capacity가 그대로라면 전체 Delivery Throughput은 그만큼 증가하지 않는다.

DORA의 AI 연구에서도 비슷한 시스템 관점이 나타난다. AI가 초기 코드 생성을 빠르게 하더라도 테스트, 리뷰, 보안, 배포가 받쳐주지 않으면 개인 수준의 개선이 downstream 병목에 흡수될 수 있다.

### 3분 수정, 하루 이상 대기

작은 Bug 하나를 Agent가 3분 만에 고쳤다고 해보자.

Build와 Target Test에 5분이 걸렸다.

여기까지만 보면 8분짜리 작업이다.

실제 흐름은 다음과 같을 수 있다.

```text
09:00 Task 시작
09:03 Agent 수정 완료
09:08 Build / Test PASS
09:10 PR 생성

다음 날
15:00 Review 시작
15:30 수정 요청
15:35 Agent 재수정
15:40 Verification PASS
17:00 Merge
```

Agent Execution Time은 몇 분이다.

하지만 Task의 End-to-End Cycle Time은 하루가 넘는다.

“Agent가 3분 만에 고쳤다”는 말은 사실이지만 전체 생산성을 설명하지 못한다.

최소한 다음 시간은 구분해야 한다.

```text
Agent Execution Time
Human Blocking Time
Human Review Time
Verification Time
Queue Time
Total Task Cycle Time
```

비동기 Agent가 40분 동안 실행돼도 개발자가 40분을 기다린 것은 아닐 수 있다. 반대로 Agent가 3분 만에 작업을 끝냈어도 조직이 3분 만에 변경을 전달한 것은 아니다.

Software Factory는 이 차이를 관리해야 한다.

---

## 1.3 Human Attention이 새로운 Capacity가 된다

Agent가 한두 개일 때는 사람이 직접 관리해도 된다.

작업을 맡기고 결과를 확인한 뒤 다음 작업을 시작한다.

하지만 여러 Agent를 동시에 사용하면 개발자는 곧 다른 종류의 일을 하게 된다.

- 어떤 Agent가 무슨 작업을 하고 있는지 확인한다.
- 중간 질문에 답한다.
- 완료 결과를 읽는다.
- 실패한 작업을 다시 시작한다.
- Pull Request를 검토한다.
- 충돌하는 변경을 조정한다.
- 다음에 어떤 작업을 시작할지 결정한다.

처음에는 “Agent가 나 대신 일한다”고 느꼈지만 어느 순간 “내가 Agent들을 관리하고 있다”는 상태가 된다.

OpenAI가 2026년 4월 Symphony를 공개하며 설명한 문제도 이 지점과 닿아 있다. OpenAI는 내부 경험에서 한 엔지니어가 interactive coding-agent session을 대체로 3~5개 정도까지는 편하게 관리했지만, 그 이상에서는 Context Switching이 눈에 띄게 부담이 됐다고 설명한다. 이 수치는 업계 일반 한계가 아니라 한 조직의 운영 사례다. 중요한 점은 session 수가 늘수록 사람의 Attention이 새로운 Capacity Constraint가 될 수 있다는 것이다. Symphony는 이 문제를 session보다 Task와 Deliverable 중심으로 orchestration하는 방식으로 풀었다.

Software Factory의 목표는 사람을 없애는 것이 아니다.

사람의 Attention을 반복적인 실행 관리에서 더 가치 있는 판단으로 옮기는 데 가깝다.

사람이 계속 책임져야 할 가능성이 높은 영역은 다음과 같다.

- 무엇을 만들어야 하는가
- 요구사항의 의미가 무엇인가
- 어떤 Architecture가 적절한가
- 어떤 위험을 허용할 것인가
- 무엇을 완료라고 판단할 것인가
- 어떤 변경을 Production에 넣을 것인가

반면 반복적인 실행은 시스템으로 이동할 수 있다.

- Repository checkout
- 환경 준비
- 반복 테스트
- 정의된 Validation
- 실패 로그 수집
- Artifact 정리
- 상태 추적

따라서 Human Intervention이 낮다는 이유만으로 좋은 Factory라고 할 수는 없다. 위험한 작업에는 의도적인 Human Gate가 필요할 수 있다.

더 유용한 질문은 다음에 가깝다.

> 검증된 변경 하나를 받아들이기 위해 사람이 얼마나 많은 Attention을 사용했는가?

개념적인 지표로 표현하면 다음과 같다.

```text
Human Attention
----------------
Accepted Change
```

표준 Metric은 아니다. 하지만 Agent 시대의 생산성을 바라보는 방향을 잘 보여준다.

Agent가 수십 개의 PR을 만들었지만 사람이 그것을 이해하고 수정하고 충돌을 해결하는 데 더 많은 시간을 쓴다면 좋은 결과라고 보기 어렵다.

반대로 Agent 실행시간이 길더라도 사람이 다른 작업을 할 수 있고, 완료된 결과를 Evidence와 함께 짧게 검토할 수 있다면 가치가 있다.

---

## 1.4 생산성 연구가 서로 다른 이유

AI 코딩 도구의 생산성 효과를 이야기할 때 서로 반대처럼 보이는 수치가 자주 등장한다.

2025년 6월 Microsoft Research가 Microsoft, Accenture, 익명의 Fortune 100 기업에서 수행된 세 Randomized Field Experiment를 통합 분석한 연구에서는 총 4,867명의 개발자를 대상으로 AI 기반 Coding Assistant 접근 효과를 분석했다. 세 실험을 합친 추정치에서는 completed task가 26.08% 증가했고, 경험이 적은 개발자에서 adoption과 gain이 더 큰 경향이 보고됐다. 다만 이 연구가 평가한 것은 주로 코드 완성을 제안하는 Coding Assistant Workflow이며, 이 책에서 다루는 2026년 비동기 Coding Agent Factory와 같은 작업 방식은 아니다.

같은 해 METR는 다른 조건에서 다른 결과를 보고했다.

METR는 숙련된 오픈소스 개발자 16명이 자신이 잘 아는 성숙한 Repository에서 246개의 실제 Task를 수행하는 RCT를 진행했다. 2025년 2~6월 수준의 AI 도구 사용이 허용된 Task에서는 완료 시간이 평균 19% 늘었다. 참여자들은 실험이 끝난 뒤에도 AI가 자신을 약 20% 빠르게 만들었다고 추정했다. 이 결과 역시 해당 시점의 도구, 숙련 개발자, 성숙한 Repository라는 조건에 묶여 있다.

이 두 수치를 `+26%`와 `-19%`라는 하나의 생산성 축에서 직접 비교하면 안 된다.

실험 조건과 측정 대상이 다르기 때문이다.

Microsoft 연구:

- 기업 환경
- 4,867명
- 당시 Coding Assistant 중심 Workflow
- completed task 수 중심

METR 연구:

- 숙련 OSS 개발자 16명
- 자신이 잘 아는 성숙한 Repository
- early-2025 도구
- 실제 Task completion time 중심

두 연구의 의미는 “AI가 빠르다” 또는 “AI가 느리다” 중 하나를 고르는 데 있지 않다.

**생산성 결과는 Task, 개발자, Workflow, 측정 경계에 따라 달라진다**는 점이 중요하다.

Agentic Workflow가 발전하면서 측정 자체도 더 어려워지고 있다.

METR는 2026년 후속 실험 설계를 검토하면서 두 가지 문제를 보고했다. AI 없이 작업하기 싫어하는 개발자가 연구 참여를 꺼리면서 selection bias가 생겼고, 한 개발자가 여러 Agent를 동시에 운영하면 Task별 인간 작업 시간을 단순 stopwatch 방식으로 재기 어려워졌다.

예전에는 다음과 같은 흐름을 가정하기 쉬웠다.

```text
Developer
→ Task A
→ 완료
→ Task B
→ 완료
```

Agentic Workflow에서는 다음처럼 겹칠 수 있다.

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

Task A의 생산성을 무엇으로 계산해야 할까.

Agent가 실행된 40분인가.  
개발자가 처음 지시한 3분인가.  
Review한 8분도 포함해야 하는가.  
Agent가 잘못 수정해 사람이 다시 고친 시간은 어떻게 계산할 것인가.

그래서 AI 시대의 생산성을 “개발자가 코딩에 쓴 시간” 하나로 설명하기 어렵다.

METR는 기존 작업을 얼마나 빨리 하는지뿐 아니라, AI가 있기 때문에 새롭게 수행하게 된 작업과 전체 value 변화도 구분할 필요가 있다고 제안한다.

예전에는 비용 때문에 생략했던 작업을 Agent가 수행할 수도 있다.

- 테스트 추가
- Documentation 보강
- Dependency Update
- Screenshot QA
- Accessibility Check
- Migration Validation
- 로그 조사
- 반복 Refactoring

AI의 효과가 기존 Task를 빠르게 하는 데만 있는 것은 아니다. Task Mix 자체가 바뀔 수 있다.

따라서 이 책에서는 “AI는 개발자를 몇 % 빠르게 만든다”는 하나의 숫자를 제시하지 않는다.

대신 다음을 묻는다.

> 어떤 Task에서, 어떤 개발자가, 어떤 Workflow로, 어떤 품질·리뷰·재작업 비용을 포함했을 때 실제 end-to-end value가 증가했는가?

---

## 1.5 최적화 단위를 바꾼다

AI Coding Agent를 도입하면 눈에 잘 보이는 숫자부터 측정하기 쉽다.

- Token 사용량
- Agent 실행 횟수
- 생성 코드량
- Pull Request 수
- Benchmark 점수
- Agent 실행시간

이 숫자들은 운영에 필요하다.

다만 최종 목표로 쓰면 왜곡이 생길 수 있다.

예를 들어 Agent A는 Token을 적게 쓰지만 네 번 Retry한 뒤 PR을 만들고, Reviewer가 크게 수정해야 한다고 하자.

Agent B는 Token을 두 배 쓰지만 첫 시도에서 검증을 통과하고 거의 수정 없이 Merge된다.

Token만 보면 A가 효율적이다.

조직의 전체 비용을 보면 B가 더 나을 수 있다.

Factory 비용에는 적어도 다음 요소가 들어간다.

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

그래서 이 책에서는 `Cost per Accepted Change` 같은 지표를 하나의 후보로 본다.

완벽한 지표는 아니다. 문서 수정 한 건과 결제 시스템 변경 한 건은 가치와 위험이 다르고, 변경을 잘게 쪼개면 Accepted Change 수를 인위적으로 늘릴 수도 있다.

핵심은 특정 지표를 표준으로 선언하는 것이 아니라 **측정 범위를 Agent에서 Delivery System으로 넓히는 것**이다.

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

Benchmark Score가 올랐다고 Team Flow가 좋아지는 것은 아니다.  
PR 수가 늘었다고 사용자에게 전달된 가치가 같은 비율로 늘어나는 것도 아니다.

Factory 수준에서는 Agent 실행량보다 Task Cycle Time, Queue/Review 대기, First-pass Acceptance, Retry/Rework, Human Intervention 같은 흐름 지표가 더 중요할 수 있다. 구체적인 Metric 설계는 19장에서 다룬다.

처음부터 많은 지표를 수집할 필요는 없다. Task의 생성·시작·검증·완료 시각과 Retry, Review 정도만 있어도 중요한 질문을 시작할 수 있다.

Agent를 추가한 뒤 Task Cycle Time이 실제로 줄었는가.  
Retry는 늘었는가.  
Review Queue는 길어졌는가.  
사람의 개입 횟수는 줄었는가.  
Agent는 빨라졌지만 Accepted Change까지 걸리는 시간은 그대로인가.

관심의 중심이 Model에서 System으로 이동하는 순간이다.

---

## 이 장에서 남는 질문

Software Factory가 모든 병목을 없애 주는 것은 아니다.

요구사항은 바뀌고, 테스트는 불완전하고, Production 환경은 예상과 다르며, Agent도 실패한다.

필요한 것은 실패와 대기를 숨기는 것이 아니라 어디에서 Work가 멈췄고 왜 멈췄는지 알 수 있는 구조다.

Coding Agent가 느릴 때는 사람이 몇 개의 Session을 직접 관리해도 된다.

Agent가 빨라지고 여러 작업을 동시에 실행할 수 있게 되면 사람의 머릿속과 여러 터미널 창만으로는 충분하지 않다.

작업 상태, 검증 기준, 실패 처리, 리뷰 용량을 시스템으로 관리해야 한다.

문제는 이제 “좋은 Coding Agent를 어떻게 쓰는가”에서 다음 질문으로 바뀐다.

> Agent를 포함한 Software Production System은 어떤 구조를 가져야 하는가?

다음 장에서는 이 시스템을 이 책에서 **AI Software Factory**라고 부르는 이유와, Factory라고 부르기 위한 최소 구성요소를 정의한다.

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
