# 1장. Coding Agent가 좋아진 뒤 무엇이 병목이 되는가

몇 년 전까지 AI 코딩 도구의 가치는 비교적 설명하기 쉬웠다. 개발자가 코드를 작성하는 동안 다음 줄을 추천하고, 반복 코드를 만들고, 모르는 API 사용법을 빠르게 알려주는 도구였다.

질문도 자연스럽게 개인 개발자의 속도에 맞춰졌다.

> 이 도구를 쓰면 코드를 얼마나 더 빨리 작성할 수 있는가?

Coding Agent가 등장하면서 이 질문만으로는 부족해졌다.

지금의 Agent는 코드 조각만 제안하지 않는다. Repository를 탐색하고 파일을 수정하고 Shell 명령을 실행한다. 테스트가 실패하면 원인을 찾고 다시 수정한다. 경우에 따라 브라우저를 열어 실제 화면까지 확인한다.

문제는 Agent가 더 많은 코드를 더 빨리 만들기 시작한 다음부터다.

코드는 빨리 만들어졌는데 Pull Request가 쌓인다.  
Pull Request는 늘었는데 CI가 밀린다.  
CI는 통과했는데 리뷰가 대기한다.  
각 변경은 맞는데 통합 과정에서 시스템이 깨진다.

병목이 사라진 것이 아니라 이동한 것이다.

이 책이 AI Software Factory를 이야기하는 출발점은 여기다.

> Agent가 코드를 얼마나 잘 쓰는가보다, Agent가 만든 Work를 Software Delivery System이 얼마나 잘 흡수하는가를 함께 봐야 한다.

---

## 1.1 Coding Assistant에서 Coding Agent로

Coding Assistant와 Coding Agent를 제품 이름으로 나누기는 어렵다. 같은 제품도 사용 방식에 따라 Assistant처럼 동작할 수도 있고 Agent처럼 동작할 수도 있다.

이 책에서는 작업 방식으로 구분한다.

Coding Assistant의 흐름은 대체로 다음과 같다.

```text
Developer
→ 질문 / 코드 작성
→ AI 응답
→ Developer 판단
→ 다음 행동
```

작업의 주도권과 상태는 대부분 개발자에게 있다.

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

예를 들어 다음 작업을 생각해 보자.

> 만료된 JWT가 들어오면 500이 아니라 401을 반환하도록 수정하고 관련 테스트를 통과시켜라.

Assistant 방식에서는 개발자가 관련 파일을 찾고 AI의 도움을 받아 수정하고, 직접 테스트를 실행해 실패 로그를 다시 전달한다.

Agent 방식에서는 Repository와 Shell에 접근할 수 있는 Agent가 관련 코드를 찾고, 테스트하고, 수정하고, 다시 검증한다.

사람이 하던 여러 번의 왕복이 하나의 작업 실행으로 묶인다.

이 차이를 설명하려면 Model만 봐서는 부족하다.

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

Benchmark가 높은 Model을 도입했다고 팀 생산성이 같은 비율로 좋아지는 것은 아니다. Repository 구조, 테스트, Tool, 실행환경이 약하면 강한 Model도 불안정할 수 있다.

> 좋은 Model이 좋은 Factory를 자동으로 만들지는 않는다.

---

## 1.2 코드 생성 속도와 Delivery 속도는 다르다

소프트웨어 변경이 사용자에게 도달하기까지는 여러 단계가 있다.

```text
Requirement
→ Implementation
→ Review
→ Verification
→ Integration
→ Release
→ Production
```

Coding Agent는 Implementation을 빠르게 만들 수 있다. 하지만 나머지 단계의 처리 능력은 그대로일 수 있다.

가상의 예를 들어보자.

Agent들이 하루에 30개의 Pull Request를 만들 수 있는데 리뷰 Capacity가 8개라면 매일 22개가 대기열에 추가된다. Worker를 더 늘려도 이 병목은 해결되지 않는다.

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

DORA의 AI 연구도 비슷한 시스템 관점을 취한다. AI가 초기 코드 생성을 빠르게 해도 테스트, 리뷰, 배포 같은 downstream capability가 받쳐주지 않으면 개인 수준의 개선이 전체 Delivery 성능으로 이어지지 않을 수 있다.

작업 시간을 보는 방식도 달라진다.

Agent가 Bug를 3분 만에 고치고 Test까지 8분 안에 통과했더라도 Pull Request가 다음 날 리뷰된다면 Task의 End-to-End Cycle Time은 하루가 넘는다.

따라서 최소한 다음은 구분해야 한다.

```text
Agent Execution Time
Verification Time
Queue / Review Wait
Human Review Time
Total Task Cycle Time
```

Agent가 빨라졌다는 사실과 변경이 빨리 전달됐다는 사실은 다르다.

---

## 1.3 Human Attention이 새로운 Capacity가 된다

Agent가 한두 개일 때는 사람이 직접 관리해도 된다.

여러 Agent를 동시에 사용하기 시작하면 개발자는 곧 다른 일을 하게 된다.

- 어떤 Agent가 무엇을 하는지 확인한다.
- 중간 질문에 답한다.
- 완료 결과를 읽는다.
- 실패한 작업을 다시 시작한다.
- Pull Request를 검토한다.
- 충돌을 조정한다.

OpenAI가 2026년 4월 Symphony를 공개하며 설명한 내부 경험에서도 한 엔지니어가 interactive coding-agent session을 대체로 3~5개 정도까지는 편하게 관리했지만, 그 이상에서는 Context Switching 부담이 커졌다고 한다. 업계 일반 한계가 아니라 한 조직의 운영 사례다.

중요한 것은 session 수가 늘수록 **Human Attention 자체가 Capacity Constraint가 될 수 있다는 점**이다.

Software Factory의 목표는 사람을 없애는 것이 아니다.

사람의 Attention을 반복적인 실행 관리에서 다음과 같은 판단으로 옮기는 데 가깝다.

- 무엇을 만들어야 하는가
- 어떤 Architecture가 적절한가
- 어떤 위험을 허용할 것인가
- 무엇을 완료라고 판단할 것인가
- 어떤 변경을 Production에 넣을 것인가

반면 환경 준비, 반복 테스트, 상태 추적, 로그 수집 같은 작업은 시스템으로 이동할 수 있다.

그래서 이 책에서는 다음과 같은 질문을 사용한다.

> 검증된 변경 하나를 받아들이기 위해 사람이 얼마나 많은 Attention을 사용했는가?

```text
Human Attention
----------------
Accepted Change
```

표준 지표는 아니다. Agent 실행량과 사람의 실제 부담을 구분하기 위한 사고 도구다.

---

## 1.4 생산성 연구가 서로 다른 이유

AI 코딩 도구의 생산성 효과를 이야기하면 서로 반대처럼 보이는 수치가 나온다.

2025년 Microsoft Research는 Microsoft, Accenture, 익명의 Fortune 100 기업에서 수행된 세 Randomized Field Experiment를 통합해 4,867명의 개발자를 분석했다. AI Coding Assistant 접근군에서는 completed task가 26.08% 증가했다. 다만 이 연구는 주로 당시 코드 완성형 Assistant Workflow를 다뤘다.

같은 해 METR는 숙련된 오픈소스 개발자 16명이 자신이 잘 아는 Repository에서 246개의 실제 Task를 수행하는 RCT를 진행했다. 2025년 2~6월 수준의 AI 도구를 사용한 Task는 평균 완료 시간이 19% 늘었다. 참여자들은 실제 측정과 달리 자신들이 약 20% 빨라졌다고 추정했다.

`+26%`와 `-19%`를 같은 생산성 축에서 직접 비교하면 안 된다.

두 연구는 개발자 집단, Task, Repository familiarity, 도구 세대, 측정 지표가 다르다.

핵심은 어느 숫자가 “진짜 AI 생산성”인지 고르는 것이 아니다.

> 생산성 결과는 Task, 개발자, Workflow, 측정 경계에 따라 달라진다.

Agentic Workflow가 발전하면 측정 자체도 어려워진다.

한 개발자가 Agent A와 B를 동시에 실행하면서 직접 Task C를 처리한다고 해보자. Task A의 인간 작업 시간은 처음 지시한 3분인가, 중간 리뷰 8분까지인가, Agent가 잘못 수정해 사람이 고친 시간도 포함해야 하는가.

AI가 있기 때문에 예전에는 생략했던 Test, Documentation, Dependency Update, 반복 QA를 새로 수행하게 될 수도 있다.

따라서 이 책은 “AI는 개발자를 몇 % 빠르게 만든다”는 하나의 숫자를 제시하지 않는다.

대신 다음을 묻는다.

> 어떤 Task에서, 어떤 Workflow와 품질·리뷰·재작업 비용을 포함했을 때 end-to-end value가 증가했는가?

---

## 1.5 최적화 단위를 바꾼다

AI Coding Agent를 도입하면 측정하기 쉬운 숫자부터 보게 된다.

- Token
- Agent Run
- 생성 코드량
- Pull Request 수
- Benchmark 점수
- Agent 실행시간

이 숫자들은 운영에 필요하지만 최종 목표가 되면 왜곡이 생길 수 있다.

Agent A는 Token을 적게 쓰지만 네 번 재시도하고 Reviewer가 크게 수정한다. Agent B는 Token을 더 쓰지만 첫 시도에서 검증을 통과하고 거의 수정 없이 Merge된다.

Token만 보면 A가 효율적이지만 조직의 전체 비용은 다를 수 있다.

```text
Total Cost
=
Model
+ Compute
+ Sandbox
+ CI
+ Review
+ Retry
+ Rework
```

그래서 이 책에서는 `Cost per Accepted Change` 같은 지표를 후보로 사용한다. 업계 표준은 아니다. 핵심은 특정 지표가 아니라 **측정 범위를 Agent에서 Delivery System으로 넓히는 것**이다.

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

한 단계의 개선이 다음 단계 개선을 보장하지 않는다.

구체적인 Factory 지표는 19장에서 다룬다. 여기서는 한 가지만 기억하면 된다.

> Agent가 빨라졌는지가 아니라 검증된 변경이 실제로 더 잘 흐르는지를 본다.

---

Software Factory가 모든 병목을 없애는 것은 아니다.

요구사항은 바뀌고, Test는 불완전하고, Production 환경은 예상과 다르며, Agent도 실패한다.

필요한 것은 실패와 대기를 숨기는 것이 아니라 어디에서 Work가 멈췄고 왜 멈췄는지 알 수 있는 구조다.

문제는 이제 “좋은 Coding Agent를 어떻게 쓰는가”에서 다음 질문으로 바뀐다.

> Agent를 포함한 Software Production System은 어떤 구조를 가져야 하는가?

다음 장에서는 이 시스템을 이 책에서 **AI Software Factory**라고 부르는 이유와 최소 정의를 정리한다.

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
