# 19장. Observability와 Metrics: 무엇을 측정할 것인가

생산 시스템을 운영하기 시작하면 곧 숫자가 쌓인다.

- 에이전트 실행시간
- 토큰
- 도구 호출
- 워커 사용률
- 테스트 결과
- 변경 검토 요청 수

하지만 숫자를 많이 모았다고 해서 생산 시스템의 상태를 이해할 수 있는 것은 아니다. 예를 들어 에이전트 실행시간이 절반으로 줄었다. 좋은 변화처럼 보인다. 그런데 검토 대기열이 두 배로 늘고 변경 되돌리기가 증가했다면 전체 전달은 좋아지지 않았을 수 있다. 생산 시스템의 관측 가능성(Observability)은 기록과 지표를 통해 실제로 무슨 일이 일어나는지 파악하는 능력이다. 그 목적은 에이전트 자체를 감시하는 데 있지 않다.

> 작업이 어디에서 멈추고, 어떤 비용과 실패를 거쳐, 얼마나 많은 사람의 주의와 노력을 사용해 수용된 변경이 되는지 보는 것이다.

여기서 `Accepted Change`와 뒤에서 사용하는 `Cost per Accepted Change`는 업계 표준 지표가 아니라 이 책이 생산 시스템 수준의 측정 경계를 설명하기 위해 사용하는 개념 정리다. Zach Lloyd도 소프트웨어 생산 시스템을 설명하면서 얼마나 많은 소프트웨어를 전달했는지뿐 아니라 사람의 작업 시간과 토큰 처리 시간을 함께 측정하고 개선해야 한다고 주장한다. 이 책은 그 측정 경계를 한 단계 더 좁힌다. 생성량이나 완료 보고보다 **검증과 수용 판단을 통과한 변경**을 중심으로 시간·비용·사람의 주의와 노력을 본다.

~~~text
Generated Output
→ Candidate
→ Verified Change
→ Accepted Change

Accepted Change
───────────────
Human Attention
Cycle Time
Compute / Token Cost
Retry / Rework
~~~

---

## 19.1 무엇을 관찰할 것인가

생산 시스템 관측 가능성은 여러 계층을 가진다.

### Task

~~~text
created
ready
assigned
running
verifying
awaiting_human
done
failed
~~~

### Attempt

~~~text
attempt_id
worker
model
start/end
retry_reason
failure_class
~~~

### Worker

~~~text
active
idle
lost
resource
profile
~~~

### Agent / Harness

~~~text
turns
tool_calls
context_compaction
model_switch
~~~

이 계층을 따로 보는 이유는 실제 에이전트가 수행하는 작업이 일반 대화와 다르기 때문이다. Microsoft Research가 2026년 6월 GitHub Copilot 실제 운영 기록을 표본 분석한 동료 심사 전 논문은 320만 사용자, 1,300만 세션, 7억6,100만 LLM 호출, 95조 토큰 규모에서 사용자의 한 차례 요청 안에 LLM 호출과 도구 실행이 반복되고 사용량이 긴 꼬리 분포, 즉 일부 사용량이 유난히 큰 분포를 보이는 특성을 보고했다.

이는 한 제품의 표본으로 추출한 실행 기록이지만 에이전트 실행 기반 비용을 단순 대화 요청 수로만 보기 어렵다는 근거가 된다.

### Execution

~~~text
commands
exit_code
wall_time
cpu
memory
~~~

### Verification

~~~text
checks
pass/fail
duration
artifact
~~~

### Human

~~~text
steering
review
approval
rejection
takeover
~~~

### Cost

~~~text
model
compute
sandbox
CI
storage
review
rework
~~~

이 계층들을 구분하면 실패가 어디에서 생겼는지 더 정확히 볼 수 있다.

### Human-facing Observability와 Telemetry는 다르다

운영자가 항상 추적 기록 보기 도구를 열어야 하는 것은 아니다. 작은 생산 시스템에서는 기존 작업 화면에 단순한 상태를 보여주는 것만으로도 유용하다.

예:

~~~text
Issue label
ready → running → review

Issue comment
worker: W3
result: PR #52
~~~

이 정도 정보만으로도 사람은 "시작됐는가, 누가 맡았는가, 검토할 결과가 나왔는가"를 빠르게 판단할 수 있다. 하지만 이것이 시스템 운영 계측 정보 전체를 대체하지는 않는다.

~~~text
Human-facing state
- label
- comment
- PR link

System telemetry
- attempt
- lease
- tool event
- verification
- cost
- failure
~~~

좋은 관측 가능성은 두 계층을 모두 가질 수 있다. 사람에게는 간단한 상태를 보여주고, 장애 분석에는 더 세밀한 이벤트와 지표를 남긴다.

---

## 19.2 Raw Chain-of-Thought가 Observability의 중심은 아니다

생산 시스템을 관찰한다고 에이전트의 내부 추론 전체를 저장해야 하는 것은 아니다. 운영에 더 중요한 것은 외부에서 확인할 수 있는 이벤트다.

예:

~~~text
TaskAssigned
ToolInvoked
VerificationFailed
RetryScheduled
ApprovalRequested
WorkerLost
TaskDone
~~~

이 이벤트만으로도 많은 질문에 답할 수 있다.

- 왜 작업이 늦었는가
- 어떤 도구가 반복 실패했는가
- 사람의 판단을 기다리는 시간이 얼마나 길었는가
- 같은 실패가 몇 번 반복됐는가

내부 추론 대화 기록을 감사 기준 원본으로 삼지 않는다.

---

## 19.3 Task Timeline을 쪼개서 본다

작업이 10시간 걸렸다고 하자. 이 숫자만으로는 원인을 알 수 없다. 다음처럼 나눌 수 있다.

~~~text
READY              30m
RUNNING             12m
VERIFYING            8m
AWAITING_HUMAN       8h
RETRY               20m
DONE
~~~

전체 처리 시간은 길지만 에이전트 실행은 짧다. 이 경우 병목은 모델이 아니다. 사람의 판단을 기다리는 시간이다. 다른 작업은 반대일 수 있다.

~~~text
READY                1m
RUNNING              4h
VERIFYING            5m
DONE
~~~

여기서는 에이전트·하네스·작업 크기를 봐야 한다. 따라서 다음 시간을 분리한다.

~~~text
Queue Time
Execution Time
Verification Time
Human Wait
Retry / Rework
Total Cycle Time
~~~

---

## 19.4 Agent Metric과 Factory Metric을 구분한다

에이전트 수준 지표:

- 작업 성공
- 토큰
- 대화 횟수
- 도구 호출
- 평가 점수

생산 시스템 수준 지표:

- 전체 처리 시간
- 첫 시도 수용
- 재시도
- 검토 대기 시간
- 변경 되돌리기
- 배포 후 발견된 결함
- 개입
- Cost per Accepted Change

사업 수준 지표:

- 기능 사용 정도
- 신뢰성
- 지원 요청량
- 매출 / 비용

계층을 섞지 않는다.

~~~text
Agent Efficiency
        ↓
Team Flow
        ↓
Delivery Performance
        ↓
Business Outcome
~~~

한 단계 개선이 다음 단계 개선을 보장하지 않는다.

---

### Activity → Output → Flow → Outcome

생산 시스템 지표를 한 층으로 놓으면 숫자가 쉽게 왜곡된다. WorkOS는 AI가 만든 PR 비율, PR 개수, 운영 환경에 들어간 AI 코드 비율 같은 지표가 실제 고객이 얻는 성과를 가릴 수 있다고 지적한다. PR이 늘어도 기능 전달이 빨라졌는지, 결함이 늘지 않았는지는 별도 문제다. 이 책에서는 측정 경계를 다음 네 층으로 나눈다.

~~~text
Activity
- Agent Runs
- Tokens
- Tool Calls

Output
- Commits
- LOC
- Pull Requests

Flow
- Cycle Time
- Review Time
- Human Blocking Time
- First-pass Acceptance

Outcome
- Feature Delivery
- Accepted Change
- Escaped Defect
- Revert
- MTTR
- Customer Impact
~~~

이 계층은 하위 지표를 버리자는 뜻이 아니다. 에이전트 실행과 PR 수는 처리 능력과 비용을 설명하는 데 필요하다. 다만 **출력이 늘었다는 사실을 성과가 좋아졌다는 결론으로 바로 연결하지 않는다.**

WorkOS가 생산 시스템의 목표를 코드 생산량보다 기능 전달과 고객에게 미친 영향에 두고, 동시에 결함 비율과 복구 시간을 보려는 이유도 여기에 있다.

## 19.5 First-pass Acceptance

에이전트가 후보를 많이 만드는 것보다 실제로 얼마나 적은 수정으로 받아들여지는지가 중요할 수 있다.

예:

~~~text
100 Proposed Changes

60 accepted without edit
20 accepted after human edit
10 rejected
10 abandoned
~~~

이 데이터는 단순 PR 수보다 더 많은 정보를 준다. 이 책에서는 이런 차이를 보기 위한 후보 지표로 `First-pass Acceptance Rate`를 사용한다. 표준 지표는 아니지만 재시도와 사람 수정이 많은 시스템을 단순 출력 개수와 구분하는 데 유용하다.

---

## 19.6 Human Attention

에이전트가 비동기로 일할수록 사람의 작업 시간을 따로 봐야 한다.

후보:

- 방향을 바로잡는 데 든 시간
- 검토 소요 시간
- 승인 대기
- 개입 횟수
- 직접 인수 횟수

개념적으로 다음 지표를 생각할 수 있다.

~~~text
Human Attention
----------------
Accepted Change
~~~

표준 지표는 아니다. 하지만 생산 시스템이 실제로 사람의 반복적인 주의와 노력을 줄이고 있는지 보는 데 도움이 된다.

---

## 19.7 Token을 비용과 생산성의 대리변수로 쓰지 않는다

에이전트 A:

~~~text
tokens: low
retries: 4
human fix: 30 min
~~~

에이전트 B:

~~~text
tokens: high
retries: 0
human fix: 2 min
~~~

토큰만 보면 A가 더 싸다. 하지만 GitHub가 2026년 공개한 에이전트 효율 사례도 개별 도구 응답의 토큰을 지나치게 줄이면 필요한 맥락 정보가 사라져 추가 호출과 전체 작업량이 늘 수 있다고 지적한다. 목표는 각 상호작용의 토큰 최소화가 아니라 작업 성과 대비 전체 비용을 줄이는 것이다. 따라서 전체 비용은 다를 수 있다.

~~~text
Total Cost
=
Model
+ Compute
+ Sandbox
+ CI
+ Review
+ Retry
+ Rework
~~~

그래서 하나의 후보로 다음을 사용할 수 있다.

~~~text
Cost per Accepted Change
~~~

완벽한 지표는 아니다. 작업 가치와 위험이 다르기 때문이다. 하지만 토큰당 비용이나 시도당 비용보다 생산 시스템 수준에 가깝다.

---

## 19.8 Benchmark와 Production Metric을 분리한다

SWE-bench 같은 성능 평가는 중요하다. 모델·하네스의 수행 능력을 비교하고 기존 기능의 오류를 찾을 수 있다. 하지만 실제 생산 시스템에는 성능 평가에 없는 요소가 있다.

- 조직의 저장소
- 실제 의존 관계
- 사람의 검토
- CI 대기열
- 권한
- 보안 통과 조건
- 운영 환경 실패
- 비용

그래서 다음 등식은 성립하지 않는다.

~~~text
Benchmark Score
=
Production Capability
~~~

성능 평가는 신호다. 운영 환경 지표는 실제 작업 분포를 보여준다. 둘 다 필요하다.

---

## 19.9 Production Failure를 Eval로 되돌린다

관측 가능성의 가장 큰 가치는 대시보드가 아니라 학습의 순환에 있다.

예:

~~~text
Production Failure
→ Failure Class
→ Eval Case
→ Harness / Tool Fix
→ Regression Test
→ Deploy
~~~

같은 문제가 반복되면 생산 시스템 자체를 개선할 수 있다.

예:

- 특정 맥락 정보가 항상 누락된다.
- 브라우저 워커가 오래된 상태를 남긴다.
- 에이전트가 같은 테스트를 반복한다.
- 검토자가 같은 의견을 남긴다.

이 정보는 스킬, 도구, 문서, 정책 개선으로 이어질 수 있다.

---

## 19.10 Minimum Viable Dashboard

처음부터 거대한 관측 가능성 플랫폼이 필요하지는 않다. 최소 대시보드는 다음 질문에 답하면 된다.

### Flow

~~~text
Backlog
Ready
Running
Blocked
Awaiting Human
Done
Failed
~~~

### Worker

~~~text
Active
Idle
Lost
~~~

### Quality

~~~text
Verification Pass
Retry
Reject
Revert
~~~

### Human Load

~~~text
Review Queue
Approval Wait
Intervention
~~~

### Cost

~~~text
Task Cost
Accepted-change Cost
~~~

이 정도만 있어도 운영 개선을 시작할 수 있다.

---

## 예: 10분 실행, 8시간 Review Wait

작업 A:

~~~text
Agent execution: 10m
Verification: 5m
Review wait: 8h
Review: 10m
~~~

모델을 20% 빠르게 바꿔도 전체 과정 개선은 거의 없다. 오히려 검토 대기열을 줄이는 것이 더 효과적일 수 있다.

작업 B:

~~~text
Agent execution: 2h
Retry: 3
Review wait: 5m
~~~

여기서는 작업 명세, 하네스, 모델, 실패 복구를 봐야 한다. 관측 가능성이 있어야 두 문제를 구분할 수 있다.

---

## 19.11 Factory Metric Set

초기에는 다음 정도면 충분하다.

~~~text
Flow
- cycle_time
- queue_time
- execution_time
- verification_time
- human_wait

Quality
- first_pass_acceptance
- retry
- reject
- revert

Human
- intervention_count
- review_minutes

Cost
- task_cost
- accepted_change_cost
~~~

생산 시스템이 커지면 더 추가한다. 지표는 측정 가능한 것을 많이 모으기 위해 만드는 것이 아니다.

**운영 결정을 바꾸기 위해 만든다.**

---

## 다음 질문

생산 시스템이 충분히 관찰되기 시작하면 새로운 가능성이 생긴다. 사람이 매번 작업을 직접 만들지 않아도 CI 실패, 취약점, 운영 환경 신호가 작업 소스가 될 수 있다. 하지만 알림을 곧바로 에이전트 행동으로 연결하면 위험하다. 다음 장에서는 **이벤트 기반 생산 시스템과 운영 결과를 개발로 되돌리는 순환 구조**를 다룬다.

---

## 참고 자료

- DORA, *2025 DORA Report*  
  https://dora.dev/research/2025/dora-report/
- Microsoft Research, *Agentic Coding in the Wild*  
  https://www.microsoft.com/en-us/research/publication/agentic-coding-in-the-wild-characterizing-github-copilot-at-production-scale/
- GitHub, *How we make AI coding more cost-efficient without sacrificing task quality*  
  https://github.blog/ai-and-ml/github-copilot/how-we-make-ai-coding-more-cost-efficient-without-sacrificing-task-quality/
- Anthropic, *Demystifying evals for AI agents*  
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Warp / Zach Lloyd, *Software Engineering Is Becoming Factory Engineering*  
  https://www.youtube.com/watch?v=tUPPVhBBcoM
- *I Built the Simplest Software Factory*, YouTube video / user-provided transcript  
  https://www.youtube.com/watch?v=AsvzMlLyQ38
