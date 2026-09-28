# AI Software Factory

> Manuscript working copy  
> 기준일: 2026-09-28  
> Source: reviewed chapter drafts

이 파일은 Review가 완료된 Chapter Draft를 출판 원고 흐름으로 조립한 working manuscript다.

원본 Source of Truth는 각 `chapters/NN/draft.md`이며, Manuscript 단계의 편집은 이후 이 파일과 Chapter Source에 동기화한다.

---

# Part I. Coding Agent에서 Software Factory로

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

---

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

---

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

NIST NCCoE가 2026년 9월 갱신한 DevSecOps live reference model을 보면 Software Delivery를 다음과 같은 연속된 흐름으로 본다.

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

중요한 점은 AI가 이 구조를 없애는 것이 아니라는 것이다. 2026년 9월 기준 NIST의 현재 공개 구현은 human-directed Generative AI를 Plan·Develop·Continuous Feedback에 넣고 있으며, 다음 Build 3에서 Agentic AI가 Develop·Build·Test를 수행하는 구조를 검토하고 있다. NIST 역시 AI를 별도 SDLC로 떼어내기보다 기존 DevSecOps lifecycle 안에 통제된 실행 주체로 넣는 방향을 취한다.

이 관점에서 Factory는 사람, 기존 자동화, Agent를 하나의 Work Flow 안에서 연결한다.

```text
Human / Product
      ↓
Plan / Requirement
      ↓
Human + Automation + Agent
      ↓
Build / Test / Release / Deploy
      ↓
Operate / Feedback
```

DevOps가 사라지는 것이 아니라 실행 주체가 늘어나는 것이다.

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

Agent가 Platform의 소비자가 되면 Portal과 문서만으로는 부족할 수 있다. Stable API, structured result, scoped permission처럼 machine-readable한 interface가 중요해진다.

다만 이 장에서는 경계만 확인한다. Golden Path를 Agent Tool로 만드는 방법과 Software Catalog, structured error, idempotency 같은 구체적인 Platform 설계는 21장에서 다룬다.

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

이 구조에서는 Factory가 모든 기능을 직접 구현하지 않는다. Factory는 Work 상태, Worker 선택, 검증, 복구, 승인 같은 Software Delivery의 흐름을 책임지고, Platform과 CI/CD는 환경·Credential·Build·Test·Deploy 같은 기존 Capability를 제공한다. Agent Runtime은 실제 Agent 실행을 담당한다.

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

---

# Part II. Work를 정의하는 시스템

# 4장. Prompt가 아니라 Requirement와 Acceptance에서 시작한다

AI Coding Agent를 쓰다 보면 가장 먼저 하고 싶은 일은 바로 시키는 것이다.

> 로그인 오류를 고쳐라.

> 출결 화면을 개선해라.

> 이 모듈을 리팩터링해라.

작은 작업에서는 충분할 수 있다. 하지만 작업이 커지면 곧 다른 질문이 생긴다.

로그인 오류는 어떤 오류인가. 정상 동작은 무엇인가. 기존 동작 중 무엇을 유지해야 하는가. 어디까지 수정해도 되는가. 무엇을 확인하면 완료라고 볼 수 있는가.

사람끼리 일할 때는 이런 질문을 대화 속에서 자연스럽게 채우기도 한다. 경험이 많은 개발자는 조직의 암묵적 규칙까지 알고 있다.

Agent에게도 같은 암묵지를 기대하면 문제가 생긴다.

Agent는 주어진 정보 안에서 가장 그럴듯한 해석을 선택할 수 있다. 하지만 그 해석이 원래 Intent와 같다는 보장은 없다.

그래서 Factory에서 첫 번째로 필요한 것은 더 긴 Prompt가 아니다.

**실행 가능한 Requirement와 Acceptance를 만드는 일**이다.

---

## 4.1 Prompt만으로 큰 Work를 관리하기 어려운 이유

Prompt는 빠르다. 문제를 설명하고 곧바로 실행할 수 있다.

하지만 Prompt에는 보통 Goal, Background, Assumption, Constraint, Design Hint, Expected Result가 섞여 있다. 이 정보가 한 번의 Conversation 안에만 있으면 시간이 지나면서 해석이 흔들릴 수 있다.

예를 들어 다음 Issue를 보자.

~~~text
로그인 오류 수정
~~~

개발자에게는 충분할 수 있다. 이미 장애 상황을 알고 있기 때문이다.

Agent 입장에서는 다르다.

- 비밀번호 오류인가
- JWT 만료인가
- OAuth redirect 문제인가
- 세션 생성 실패인가
- HTTP status가 잘못됐는가

가능한 해석이 많다.

Agent가 Repository를 읽으며 추측할 수는 있다. 하지만 추측이 맞았는지 확인할 기준이 없다.

그래서 큰 Work에서는 Prompt보다 durable artifact가 필요하다.

~~~text
Conversation
→ ephemeral

Requirement
Acceptance
Design Constraint
Task
→ durable
~~~

이 문서가 거대한 명세서일 필요는 없다. 핵심은 Agent Session이 바뀌어도 Work의 의미가 유지되는 것이다.

---

## 4.2 Intent에서 Acceptance까지

Factory 앞단을 다음처럼 볼 수 있다.

~~~text
Intent
→ Requirement
→ Clarification
→ Acceptance Criteria
→ Design Constraint
→ Task
~~~

각 단계는 다른 질문에 답한다.

### Intent

왜 이 일을 하는가.

~~~text
만료된 JWT 때문에 사용자가 500 오류 화면을 본다.
인증 실패로 처리해야 한다.
~~~

### Requirement

시스템이 어떻게 동작해야 하는가.

~~~text
만료된 JWT 요청은 HTTP 401을 반환해야 한다.
~~~

### Acceptance Criteria

무엇을 확인하면 완료라고 볼 것인가.

~~~text
Given expired JWT
When protected endpoint is requested
Then response status is 401
And internal server error is not logged
~~~

### Design Constraint

무엇을 바꾸지 않아야 하는가.

~~~text
DB schema 변경 없음
OAuth flow 변경 없음
공통 error envelope 유지
~~~

이 정도만 있어도 Agent가 탐색해야 하는 범위가 크게 줄어든다.

더 중요한 점은 검증이 가능해진다는 것이다.

~~~text
Requirement
→ Acceptance
→ Test / Runtime Check
~~~

좋은 Requirement는 구현 방법을 세세하게 지시하는 문서가 아니다. Agent가 여러 구현 방법 중 선택할 수 있도록 하면서도 완료 여부는 명확하게 판단할 수 있게 해야 한다.

---

## 4.3 Requirements-first와 Design-first

모든 작업이 Requirement부터 시작하는 것은 아니다.

새 기능이라면 다음 흐름이 자연스럽다.

~~~text
Requirement
→ Design
→ Task
~~~

반면 기존 시스템 Migration은 다를 수 있다.

~~~text
Design Constraint
→ Requirement
→ Task
~~~

기존 Architecture, 배포 제약, 호환성 조건이 먼저 정해질 수 있기 때문이다.

중요한 것은 하나의 Planning Process를 모든 작업에 강요하지 않는 것이다.

2026년 9월 기준 GitHub Spec Kit의 기본 SDD 흐름은 `Specify → Plan → Tasks → Implement → Converge`이고, Kiro도 Requirement·Design·Task를 별도 artifact로 관리한다. 제품별 절차는 다르지만 여기서 가져올 원칙은 문서 형식 자체가 아니라 **Intent와 실행 사이에 durable artifact와 검증 가능한 연결을 둔다는 것**이다.

작은 수정에 20페이지 Spec을 만드는 것은 낭비다. 반대로 여러 모듈이 연결된 Migration을 한 줄 Prompt로 처리하는 것도 위험하다.

Planning Depth는 Task의 Risk와 Complexity에 맞춰야 한다.

---

## 4.4 Requirement Generator와 Acceptance Authority를 분리한다

Agent가 Requirement 초안을 만드는 것은 유용하다.

오히려 Agent는 다음 질문을 잘 찾을 수 있다.

- 모호한 표현은 무엇인가
- 충돌하는 조건이 있는가
- Edge Case가 빠졌는가
- 기존 코드와 맞지 않는 가정이 있는가

하지만 여기서 중요한 경계가 있다.

~~~text
Requirement Generator
≠ Acceptance Authority
~~~

Agent가 Requirement도 만들고, Test도 만들고, 구현도 하고, 완료 판정까지 모두 한다면 같은 오해를 끝까지 유지할 수 있다.

예를 들어 사용자가 원한 것은 reusable library인데 Agent가 demo application으로 Requirement를 잘못 해석했다고 하자. Agent가 자신의 해석을 기준으로 Test까지 만들면 Test는 모두 통과할 수 있다. 하지만 원래 Intent는 충족되지 않았다.

그래서 Factory에서는 역할을 분리할 수 있다.

~~~text
Human / Product
→ Intent Authority

Agent
→ Requirement Draft / Clarification

System / Reviewer
→ Acceptance Approval
~~~

작은 maintenance Task에서는 이 과정이 자동화될 수 있다.

중요한 것은 누가 문서를 작성했느냐보다 **누가 최종 의미를 승인하느냐**다.

---

## 4.5 Requirement에서 Verification까지 연결한다

좋은 Factory는 Work Artifact를 서로 연결한다. Spec Kit의 최신 `converge` 단계처럼 구현 결과를 다시 specification·plan·task와 대조하는 흐름도 이 연결의 한 사례다.

~~~text
Requirement R1
→ Design D1
→ Task T3
→ Commit C7
→ Verification V2
→ Evidence A4
~~~

이 연결이 있으면 다음 질문에 답하기 쉬워진다.

- 이 Requirement를 구현한 Task는 무엇인가
- 이 Task는 어떤 Test로 검증됐는가
- Requirement가 바뀌었는데 Test가 그대로인 것은 아닌가
- 변경된 코드가 어떤 Acceptance Criteria와 연결되는가

Traceability를 처음부터 완벽하게 만들 필요는 없다.

Minimum Viable Factory라면 다음 정도만 있어도 충분하다.

~~~text
Task
→ Acceptance
→ Verification Command
→ Result
~~~

예:

~~~text
Task:
expired JWT handling

Acceptance:
expired token → 401

Verification:
./gradlew test --tests AuthServiceTest.expiredToken

Result:
PASS
~~~

이 연결이 반복되면 Agent의 자연어 완료 보고보다 훨씬 강한 완료 기준이 생긴다.

---

## 4.6 Ready Contract

Factory가 고도화되면 모든 Backlog Item을 곧바로 Worker에게 보내고 싶어진다.

하지만 Queue에 들어갈 수 있다고 실행 가능한 것은 아니다.

다음 Issue를 생각해 보자.

~~~text
성능 개선
~~~

무엇을 개선해야 하는가. 현재 수치는 얼마인가. 목표는 무엇인가. 어떤 환경에서 측정할 것인가.

이런 정보가 없으면 Agent가 많은 작업을 해도 완료 여부를 판단하기 어렵다.

그래서 Factory에는 간단한 Ready Contract가 필요하다.

~~~text
Goal
- 무엇을 바꿀 것인가

Scope
- 어디까지 수정 가능한가

Acceptance
- 무엇으로 완료를 확인할 것인가

Dependency
- 선행 작업이 있는가

Risk
- 특별한 승인이나 제한이 필요한가
~~~

모든 필드가 항상 필요하지는 않다.

Docs 수정은 Goal과 Acceptance만으로 충분할 수 있다. Production Migration은 훨씬 더 많은 정보가 필요하다.

> 실행 자동화보다 먼저, 어떤 Work가 실행 가능한 상태인지 정의해야 한다.

---

## 예: “로그인 오류 수정”을 Factory Task로 바꾸기

처음 Issue:

~~~text
로그인 오류 수정
~~~

Clarification 이후:

~~~text
Goal
- expired JWT 요청을 인증 실패로 처리

Scope
- auth module

Acceptance
- expired JWT → HTTP 401
- server error log 미발생
- valid JWT behavior 유지

Do Not Change
- DB schema
- OAuth flow

Verification
- AuthServiceTest.expiredToken
- auth integration test
~~~

이제 Agent가 무엇을 해야 하는지보다 더 중요한 것이 생겼다.

**무엇을 하면 끝난 것인지 알 수 있게 됐다.**

---

## 다음 질문

Requirement와 Acceptance가 준비됐다고 해도 아직 한 가지 문제가 남는다.

Agent가 실행 중 중단되면 이 Work는 어디에 남는가. Session이 닫히면 Task도 사라지는가. Retry할 때 처음부터 새로운 Prompt를 만들어야 하는가.

다음 장에서는 Prompt나 Session보다 오래 살아남는 작업 단위인 **Durable Task**를 정의한다.

---

## 참고 자료

- GitHub, *Spec Kit*  
  https://github.com/github/spec-kit
- Kiro, *Specs*  
  https://kiro.dev/docs/specs/
- Kiro, *Analyze Requirements*  
  https://kiro.dev/docs/specs/analyze-requirements/
- REAgent, *Requirement-Driven LLM Agents for Software Issue Resolution*  
  https://arxiv.org/abs/2604.06861

---

# 5장. Durable Task: Session보다 오래 살아남는 작업 단위

Agent에게 일을 맡겼다.

20분 동안 Repository를 탐색했고 파일 세 개를 수정했다.

테스트 하나가 아직 실패한다.

그 순간 Worker가 죽었다.

다시 시작했을 때 가장 먼저 필요한 것은 무엇일까.

더 좋은 Model이 아니다.

**어디까지 했는지 알 수 있는 작업 상태**다.

Interactive Agent에서는 Session이 작업의 중심이 되기 쉽다.

Software Factory에서는 충분하지 않다.

이 책에서는 Prompt와 Session보다 오래 살아남으며 상태, 시도, 검증, 결과를 가진 작업 단위를 **Durable Task**라고 부른다.

여기서 Durable Task는 이 책의 개념어다. Microsoft의 `Durable Task`라는 workflow runtime/product와 이름이 겹치지만 같은 뜻은 아니다. Microsoft Durable Task는 15장에서 durable execution의 구현 사례로 따로 다룬다.

---

## 5.1 Prompt, Session, Task

세 가지는 비슷해 보이지만 lifetime이 다르다.

~~~text
Prompt
= 한 번의 interaction

Session
= Agent가 일하는 execution context

Task
= 완료까지 추적되는 durable work item
~~~

Prompt는 사라져도 된다.

Session도 종료될 수 있다.

Task는 완료되거나 명시적으로 종료될 때까지 남아야 한다.

예를 들어 다음 요청을 생각해 보자.

~~~text
expired JWT를 401로 처리
~~~

Prompt에는 이 문장이 들어갈 수 있다.

Session에는 Repository 탐색, Tool Call, 실패 로그, 수정 결과가 쌓인다.

Task에는 더 오래 남아야 할 정보가 있다.

- Goal
- Scope
- Acceptance
- Status
- Attempt
- Worker
- Base Revision
- Verification
- Evidence
- Approval
- Failure Reason

Session이 새로 만들어져도 이 정보는 유지돼야 한다.

---

## 5.2 Task 최소 스키마

Durable Task를 처음부터 거대한 schema로 만들 필요는 없다.

다만 다음 범주는 구분하는 편이 좋다.

### Identity

~~~text
task_id
project_id
~~~

### Intent

~~~text
goal
scope
acceptance
~~~

### Scheduling

~~~text
priority
dependency
risk
required_capability
~~~

### Execution

~~~text
status
attempt_id
worker_id
workspace
base_revision
current_revision
~~~

### Verification

~~~text
verification_profile
verification_result
evidence
~~~

### Governance

~~~text
approval_state
approved_by
~~~

### Recovery

~~~text
failure_class
retry_count
carryover
~~~

모든 조직이 같은 필드를 가질 필요는 없다.

중요한 것은 이 정보가 Agent transcript 안에만 존재하지 않는 것이다.

---

## 5.3 Task와 Attempt를 분리한다

Task를 운영 단위로 만들려면 Attempt를 별도로 봐야 한다.

다음 상황을 생각해 보자.

~~~text
Task T-100
Goal: expired JWT → 401
~~~

첫 번째 Worker가 작업했지만 Verification에 실패했다.

~~~text
Attempt A1
Worker: W1
Result: failed
Reason: integration test failed
~~~

두 번째 Attempt에서 같은 Task를 다시 수행할 수 있다.

~~~text
Attempt A2
Worker: W2
Result: passed
~~~

Task는 하나다.

시도는 둘이다.

~~~text
Task T-100
├─ Attempt A1 → FAILED
└─ Attempt A2 → PASSED
~~~

이 구조가 필요한 이유는 단순하다.

실패한 Attempt도 정보이기 때문이다.

- 어떤 Worker에서 실패했는가
- 어떤 Command가 실패했는가
- 몇 번 Retry했는가
- 같은 Failure가 반복되는가
- 어떤 변경이 이미 만들어졌는가

Retry할 때 Task 자체를 새로 만들면 이 history가 끊긴다.

그러면 시스템은 같은 실패를 처음 보는 것처럼 반복할 수 있다.

---

## 5.4 Task 상태 전이

Factory에서는 Task 상태를 Agent의 자연어 설명과 분리하는 편이 좋다.

예를 들어 다음 정도의 상태가 있을 수 있다.

~~~text
READY
  ↓
RUNNING
  ↓
VERIFYING
  ↓
AWAITING_HUMAN
  ↓
DONE
~~~

실패 경로도 필요하다.

~~~text
RUNNING
  ├→ BLOCKED
  ├→ RETRY
  └→ FAILED
~~~

각 상태는 의미가 달라야 한다.

### READY

실행 조건이 충족됐다.

### RUNNING

현재 Attempt가 실행 중이다.

### VERIFYING

구현은 끝났고 required verification을 수행 중이다.

### AWAITING_HUMAN

Agent가 할 수 있는 일은 끝났고 승인이나 판단을 기다린다.

### BLOCKED

Dependency나 외부 조건 때문에 진행할 수 없다.

### RETRY

현재 Attempt는 종료됐고 새 Attempt가 필요하다. 실제 구현에서는 `RETRY_SCHEDULED`처럼 대기 상태와 실행 가능 상태를 더 세분화할 수 있다.

### DONE

Acceptance와 required gate를 모두 통과했다.

Agent가 "완료"라고 말해도 바로 DONE으로 가지 않는다.

상태 전이는 System Policy가 결정해야 한다.

---

## 5.5 Task가 Worker보다 오래 살아야 한다

Worker는 여러 이유로 사라질 수 있다.

- process crash
- VM restart
- timeout
- deploy
- network loss
- preemption
- manual stop

이때 Task state가 Worker 안에만 있다면 Work도 같이 사라진다.

좋은 구조는 반대다.

~~~text
Task State
= durable

Worker
= replaceable
~~~

Worker가 죽으면 Control Plane은 다음을 확인할 수 있어야 한다.

- Task는 RUNNING이었는가
- Attempt는 어디까지 갔는가
- Commit이 남아 있는가
- uncommitted change가 있는가
- 마지막 Verification은 무엇인가
- Retry 가능한 Failure인가

그리고 필요하면 새 Worker를 배정한다.

~~~text
Worker A lost
      ↓
Task remains
      ↓
Worker B assigned
~~~

이 구조가 가능하려면 Task state와 execution state를 분리해야 한다.

---

## 5.6 Context Window를 Task Database로 쓰지 않는다

Agent Session에는 많은 정보가 있다.

- 탐색한 파일
- 실패 로그
- 수정 이유
- 다음 행동

그래서 transcript 자체를 작업 저장소처럼 사용하고 싶어진다.

하지만 문제가 있다.

Context는 길이 제한이 있다.

Compaction이 발생할 수 있다.

Session이 교체될 수 있다.

다른 Worker가 같은 형식으로 이어받는다는 보장도 없다.

따라서 중요한 상태는 외부 durable artifact로 꺼내야 한다.

예:

~~~text
Task Store
Git
Artifact Store
Verification Result
~~~

Context Window는 reasoning을 위한 공간이다.

Durable Task State는 운영을 위한 기록이다.

둘을 섞지 않는다.

---

## 5.7 Carryover: 다른 Worker가 이어받을 수 있는가

단순히 다음 정보만 남겨서는 충분하지 않을 수 있다.

~~~text
Worker lost.
~~~

새 Worker가 실제로 이어받으려면 더 많은 정보가 필요하다.

~~~text
Goal
- expired JWT → 401

Completed
- AuthService 수정
- target unit test PASS

Remaining
- integration test failure

Changed Files
- AuthService.java
- AuthServiceTest.java

Current Revision
- abc123

Uncommitted Changes
- patch artifact://task-100/a1.patch

Latest Failure
- AuthIntegrationTest.expiredToken

Next Action
- inspect exception mapping
~~~

이것이 Carryover다.

Carryover의 품질을 평가하는 가장 좋은 질문은 간단하다.

> 다른 Worker가 이전 Worker의 도움 없이 이어갈 수 있는가?

이 질문에 답할 수 없다면 Task state가 충분히 durable하지 않은 것이다.

---

## 예: Verification 실패 후 새 Attempt

~~~text
Task T-100
Status: VERIFYING

Attempt A1
Worker: W1
Verification: FAIL
Reason: integration test
~~~

System은 A1을 닫는다.

~~~text
Task T-100
Status: RETRY
retry_count: 1
~~~

다음 Worker에게는 원래 Goal과 함께 실패 Evidence가 전달된다.

~~~text
Attempt A2
Worker: W2
Input:
- original acceptance
- A1 changes
- failed test
- failure summary
~~~

A2가 통과하면 Task는 VERIFYING을 거쳐 DONE으로 이동한다.

Task는 처음부터 새로 만들어지지 않는다.

---

## 다음 질문

Durable Task를 만들었다고 끝은 아니다.

Task가 너무 크면 Context와 Retry 비용이 커진다.

너무 작으면 Worker 시작과 Context 전달 비용이 더 커진다.

Task끼리 Dependency가 있으면 아무 순서로나 실행할 수도 없다.

다음 장에서는 **어떤 크기로 Task를 나누고 어떤 Dependency를 표현해야 하는가**를 다룬다.

---

## 참고 자료

- OpenAI, *An open-source spec for Codex orchestration: Symphony*  
  https://openai.com/index/open-source-codex-orchestration-symphony/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Anthropic, *Effective harnesses for long-running agents*  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Microsoft, *Durable Task for AI agents*  
  https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents

---

# 6장. Task 크기, 분해, Dependency

Task를 durable하게 만들면 다음 문제는 크기다.

너무 큰 Task를 Agent에게 주면 오래 실행되고 수정 범위가 넓어진다. 실패했을 때 처음부터 다시 해야 할 가능성도 커진다.

그렇다고 무조건 잘게 나누면 좋은 것도 아니다.

Task가 너무 작으면 Worker 시작, Repository 탐색, Context 전달, Verification 같은 고정 비용이 반복된다.

그래서 좋은 Task 크기는 줄 수나 작업 시간으로 정하기 어렵다.

이 책에서는 다음 기준을 사용한다.

> 좋은 Task는 독립적으로 실행하고, 검증하고, 실패 시 복구할 수 있으며, 필요한 승인 주체가 결과를 판단할 수 있는 단위다.

Task 분해는 Prompt를 예쁘게 나누는 문제가 아니다.

**실행 그래프를 설계하는 문제**다.

---

## 6.1 Task Size에는 양쪽 비용이 있다

Task가 작아지면 좋은 점이 있다.

- Context가 줄어든다.
- Failure 범위가 작아진다.
- Review가 쉬워진다.
- 병렬 실행 가능성이 커진다.

하지만 너무 작으면 고정 비용이 커진다.

- Worker startup
- Repository checkout
- Context loading
- Scheduling
- Verification
- Result packaging

예를 들어 한 줄 문구 수정 하나를 별도 Worker에 보내는 것이 항상 효율적인 것은 아니다.

반대로 Task가 너무 크면 다른 문제가 생긴다.

- 여러 모듈을 함께 이해해야 한다.
- 변경 파일이 많아진다.
- Retry 시 재작업 범위가 커진다.
- Review가 어려워진다.
- Merge Conflict 가능성이 커진다.
- 완료 조건이 모호해진다.

개념적으로 다음과 같은 균형이 있다.

~~~text
Very Small Task
→ orchestration overhead 증가

Reasonable Task
→ independent execute / verify / review 가능

Very Large Task
→ context / failure / review cost 증가
~~~

절대적인 “30분 이하”나 “파일 3개 이하” 같은 규칙은 두지 않는다.

프로젝트마다 환경 준비 비용과 검증 비용이 다르기 때문이다.

---

## 6.2 독립성은 파일 수보다 중요하다

두 Task가 서로 다른 파일을 수정한다고 해서 독립적인 것은 아니다.

예를 들어 다음 두 작업을 보자.

~~~text
Task A
- user table에 status column 추가

Task B
- User API 응답에 status 추가
~~~

수정 파일은 다를 수 있다.

하지만 B는 A의 Schema와 Domain 의미에 의존한다.

반대로 파일이 일부 겹쳐도 논리적으로 독립적인 경우가 있을 수 있다.

따라서 독립성을 판단할 때는 다음을 본다.

- Scope가 분리되는가
- Acceptance가 독립적인가
- Verification을 따로 실행할 수 있는가
- Shared Schema를 바꾸는가
- 같은 Architecture Decision에 의존하는가
- 동일한 External Resource를 사용해야 하는가
- 한 Task 결과가 다른 Task의 입력인가

독립성이 높을수록 Retry와 Parallelism이 쉬워진다.

---

## 6.3 Task List보다 Dependency Graph가 낫다

Backlog는 보통 List로 보인다.

~~~text
T1
T2
T3
T4
T5
~~~

하지만 실제 실행 순서는 List보다 Graph에 가깝다.

~~~text
T1 ─→ T3 ─→ T5
T2 ───────→ T5
T4 ─→ T6
~~~

T1과 T2는 병렬로 실행할 수 있다.

T5는 둘이 끝나야 Ready가 된다.

T4와 T6은 다른 흐름이다.

Dependency Graph가 있으면 Factory가 다음 질문에 답할 수 있다.

- 지금 Ready인 Task는 무엇인가
- 어떤 Task를 동시에 실행할 수 있는가
- 하나가 실패하면 무엇을 막아야 하는가
- 어떤 결과가 바뀌면 downstream Task를 다시 검증해야 하는가

Task를 자동 선택하려면 Priority보다 먼저 Dependency가 정확해야 한다.

---

## 6.4 Retry Boundary를 같이 설계한다

Task를 나누는 중요한 이유 중 하나는 Retry 범위를 줄이는 것이다.

예를 들어 하나의 큰 workflow가 있다고 하자.

~~~text
Analyze
→ Modify Backend
→ Modify Frontend
→ Run Unit Test
→ Run E2E
→ Build Image
~~~

마지막 E2E에서 실패했다.

Monolithic Task라면 전체 작업을 다시 실행할 수 있다.

Task를 나누면 나아질 것 같지만 반드시 그렇지는 않다.

Static하게 여러 Subtask로 쪼갰어도 orchestration이 실패 상태를 이해하지 못하면 downstream 전체를 다시 실행할 수 있다.

2026년 `Runtime-Structured Task Decomposition` 연구는 두 Software Engineering workload를 각각 10회씩 비교한 소규모 실험에서 이 차이를 다뤘다. Static Decomposition은 경우에 따라 monolithic 실행보다 retry 비용이 더 커졌고, dependency와 failure를 runtime control logic이 관리한 방식은 실패한 subtask만 다시 실행해 retry 비용을 낮췄다. 아직 제한된 workload의 연구이므로 일반 법칙으로 볼 수는 없지만, 적어도 “잘게 나누기만 하면 복구 비용이 줄어든다”는 가정에는 반례가 된다.

핵심은 분해 자체보다 **dependency와 failure semantics를 runtime이 아는가**다.

~~~text
Failed Subtask
→ affected downstream만 invalidate
→ 필요한 부분만 rerun
~~~

Factory에서 좋은 Task Boundary는 Retry Boundary이기도 하다.

---

## 6.5 Large Task와 Large PR는 다르다

큰 Feature가 하나의 Product Task라고 해서 하나의 거대한 Pull Request로 만들어야 하는 것은 아니다.

예를 들어 인증 시스템 개선을 보자.

Product 수준에서는 하나의 Initiative일 수 있다.

하지만 Delivery는 다음처럼 나눌 수 있다.

~~~text
T1: exception mapping 정리
T2: expired token 처리
T3: refresh token test 보강
T4: metrics 추가
T5: integration regression
~~~

각 Task는 별도의 Reviewable Change를 만들 수 있다.

필요하면 순서를 정한다.

~~~text
T1
 ↓
T2
 ↓
T3
~~~

이렇게 하면 다음 장점이 있다.

- Review scope 감소
- Rollback 범위 감소
- Failure localization 개선
- Merge Conflict 감소

물론 너무 많은 PR chain도 비용이 있다.

Rebase, merge ordering, dependency management가 필요하다.

그래서 Large Task를 무조건 잘게 쪼개는 것이 아니라 **review 가능한 delivery boundary**를 찾는다.

---

## 6.6 병렬화 후보는 Task 구조에서 나온다

여러 Agent를 쓰고 싶어서 Task를 병렬화하면 안 된다.

먼저 Task가 독립적인지 본다.

좋은 병렬 후보:

~~~text
T1: backend unit tests
T2: frontend E2E
T3: documentation
~~~

각 작업의 Scope와 Verification이 분리돼 있다.

나쁜 병렬 후보:

~~~text
T1: UserService 구조 변경
T2: UserService cache 변경
T3: UserService test architecture 변경
~~~

Branch는 달라도 같은 설계 결정을 공유한다.

같은 Schema를 동시에 바꾸는 Task도 비슷하다.

Parallelism은 Agent 수가 아니라 Dependency Graph에서 나온다.

---

## 예: Auth 개선을 분해하기

처음 Work:

~~~text
인증 오류 처리 개선
~~~

먼저 Architecture Decision이 필요하다.

~~~text
D1
- 인증 실패는 공통 error envelope를 사용
- expired / invalid token 모두 401
- OAuth flow는 유지
~~~

그 다음 Task를 만든다.

~~~text
T1
Exception mapping 정리

T2
Expired token 처리

T3
Invalid token regression test

T4
Auth integration test
~~~

Dependency:

~~~text
D1
├→ T1 ─→ T2 ─→ T4
└→ T3 ─────────→ T4
~~~

T1과 T3는 일부 병렬 가능하다.

T4는 앞 작업 결과를 합친 뒤 실행한다.

이 구조가 있으면 Scheduler는 단순 Queue보다 더 나은 결정을 할 수 있다.

---

## Task 분해 체크

Task를 Queue에 넣기 전에 다음 질문을 해볼 수 있다.

~~~text
1. Acceptance를 독립적으로 판단할 수 있는가?
2. 실패하면 이 Task만 Retry할 수 있는가?
3. 예상 변경 범위가 Review 가능한가?
4. 다른 Task의 미완성 결과에 의존하는가?
5. Shared Schema / Core File을 동시에 바꾸는가?
6. 결과를 Commit / Artifact로 전달할 수 있는가?
~~~

이 질문은 점수표가 아니다.

실행과 복구의 경계를 명시적으로 생각하게 만드는 장치다.

---

## 다음 질문

Requirement가 있고, Durable Task가 있고, Dependency Graph까지 만들었다.

이제 실제로 누군가 이 Work를 실행해야 한다.

어떤 Worker를 선택할 것인가.

누가 Task 상태를 바꿀 것인가.

Worker가 죽으면 누가 다시 배정할 것인가.

7장부터는 Factory의 실행 구조로 들어간다.

먼저 **Control Plane과 Execution Plane**을 분리한다.

---

## 참고 자료

- GitHub, *Spec Kit*  
  https://github.com/github/spec-kit
- *Runtime-Structured Task Decomposition for Agentic Coding Systems*  
  https://arxiv.org/abs/2605.15425
- GitHub, *Stacked pull requests are now in public preview*  
  https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/
- GitHub Engineering, *Turn one giant AI-generated pull request to a reviewable stack*  
  https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/
