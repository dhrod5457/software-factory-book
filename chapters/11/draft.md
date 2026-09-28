# 11장. Controlled Autonomy: 무엇을 시스템에 두고 무엇을 Agent에게 맡길 것인가

Agentic이라는 말은 자주 “Agent가 더 많은 것을 스스로 결정한다”는 의미로 쓰인다.

하지만 실제 Factory에서 중요한 것은 Autonomy의 양이 아니다.

**어떤 결정을 누구에게 맡길 것인가**다.

예를 들어 다음 두 결정은 성격이 다르다.

~~~text
이 Task는 Retry를 최대 2회만 허용한다.
~~~

~~~text
이 실패의 원인이 SecurityFilter인지 ExceptionMapper인지 조사한다.
~~~

첫 번째는 이미 알고 있는 운영 규칙이다.

두 번째는 탐색과 판단이 필요한 Engineering 문제다.

둘 다 Agent에게 맡길 수는 있다.

하지만 그럴 이유가 있는지는 별개의 문제다.

이 책에서는 다음 원칙을 사용한다.

> 이미 알고 있는 Rule과 State는 시스템이 책임지고, 사전 규칙화하기 어려운 Search와 Judgment에 Agent Autonomy를 사용한다.

---

## 11.1 세 가지 Control Model

Factory의 Control 방식을 단순화하면 세 가지로 볼 수 있다.

### Model A. Deterministic Pipeline

~~~text
Step 1
→ Step 2
→ Step 3
~~~

실행 순서와 분기는 코드가 결정한다.

LLM은 각 Step 안에서 제한된 판단만 한다.

예:

~~~text
checkout
→ build
→ targeted test
→ agent fix
→ test
→ PR
~~~

장점:

- predictable
- debug가 쉽다
- retry boundary가 명확하다
- cost variance가 낮다

단점:

- 예상하지 못한 상황에 유연하지 않을 수 있다.

---

### Model B. Agent-controlled

~~~text
Goal
→ Agent chooses tools
→ Agent decides order
→ Agent decides completion
~~~

Agent가 Workflow 전체를 판단한다.

장점:

- 유연하다
- unknown situation에 대응하기 쉽다
- 새로운 Tool 조합을 찾을 수 있다

단점:

- run variation이 커질 수 있다
- 같은 판단을 반복할 수 있다
- state와 policy가 transcript 안으로 숨어들 수 있다
- 종료 조건이 모호해질 수 있다

---

### Model C. Hybrid Runtime

~~~text
System owns
- state
- policy
- retry
- dependency
- approval

Agent owns
- search
- diagnosis
- implementation
- debugging
~~~

이 책에서는 이 형태를 기본 후보로 본다.

모든 Workflow를 state machine으로 고정하지도 않고, 모든 Control을 Agent에게 넘기지도 않는다.

---

## 11.2 Rule, Heuristic, Judgment를 구분한다

Control Boundary를 설계할 때 모든 결정을 같은 종류로 보면 어렵다.

세 가지로 나눌 수 있다.

### Rule

정확한 조건이 이미 존재한다.

예:

~~~text
main direct push forbidden
~~~

이건 Policy로 강제할 수 있다.

Agent에게 “가능하면 하지 마라”라고 말할 필요가 없다.

---

### Heuristic

정답은 아니지만 좋은 기본 판단이 있다.

예:

~~~text
이 Task는 backend-java Worker가 적합할 가능성이 높다.
~~~

이건 Routing Policy나 Model을 쓸 수 있다.

필요하면 fallback도 둔다.

---

### Judgment

사전에 정확한 규칙을 만들기 어렵다.

예:

~~~text
이 Failure의 Root Cause는 무엇인가?
~~~

~~~text
어떤 구현 전략이 가장 적합한가?
~~~

이런 문제는 Agent가 잘하는 영역이다.

Factory 설계에서 중요한 것은 세 종류를 섞지 않는 것이다.

---

## 11.3 System이 소유해야 할 상태

다음 상태를 Agent Transcript 안에만 두면 위험하다.

- Task Status
- Retry Count
- Timeout
- Dependency
- Worker Lease
- Permission
- Cost Budget
- Required Verification
- Approval State

왜냐하면 Model은 이 상태를 잊거나 잘못 해석할 수 있기 때문이다.

예를 들어 Prompt에 다음과 같이 적었다고 하자.

~~~text
테스트 실패 시 최대 2번까지만 수정하고,
그래도 실패하면 중단해라.
~~~

Agent가 정확히 지킬 수도 있다.

하지만 장시간 실행 중 Context가 압축되거나 Tool Failure가 반복되면 이 규칙이 흐려질 수 있다.

더 안전한 구조는 다음이다.

~~~text
Control Plane
retry_budget = 2

Agent
→ attempt
→ result

System
→ retry allowed?
~~~

Retry Budget은 운영 상태다.

Model의 기억에 맡길 이유가 적다.

같은 원리는 Permission과 Approval에도 적용된다.

---

## 11.4 Agent가 잘하는 영역

반대로 다음은 시스템이 미리 모든 경우를 정의하기 어렵다.

### Repository Exploration

어떤 File과 Symbol이 관련 있는지 찾는다.

### Diagnosis

실패 원인 후보를 만든다.

### Hypothesis

~~~text
JWT expiry exception이 generic error handler로 흘러가는 것 같다.
~~~

### Implementation Strategy

어떤 Layer에서 수정할지 판단한다.

### Debugging Sequence

어떤 Test와 Log를 먼저 볼지 선택한다.

### Alternative Comparison

두 구현의 Trade-off를 비교한다.

이 영역을 모두 deterministic workflow로 만들면 오히려 brittle해질 수 있다.

Agent가 가진 강점은 **정답이 이미 코드로 존재하지 않는 탐색 공간에서 다음 행동을 선택하는 능력**에 있다.

---

## 11.5 왜 “더 Agentic”이 항상 더 좋은 것은 아닌가

연구에서도 비슷한 결과가 나온다.

Agentless는 복잡한 자유 Agent Loop 없이 localization → repair → validation이라는 구조화된 Workflow로 강한 Software Engineering Benchmark 결과를 보여줬다.

또 2026년 COBOL-to-Python modernization 연구에서는 Model, Prompt, Tool을 같게 유지하고 Orchestration Strategy만 비교했다.

Deterministic Orchestration은 LLM-controlled Orchestration과 비슷한 Accuracy를 보이면서도 worst-case robustness와 run variability, Token 사용에서 더 나은 결과를 보고했다.

이 결과를 모든 Task에 일반화할 수는 없다.

하지만 한 가지는 분명하다.

> 구조화 가능한 Process에 Autonomy를 추가한다고 자동으로 품질이 좋아지는 것은 아니다.

Agent Autonomy에도 Cost가 있다.

- 더 많은 Tool Call
- 더 많은 Context
- 더 긴 Trajectory
- 더 큰 Variance
- termination uncertainty

그래서 Autonomy는 기능이 아니라 Trade-off다.

---

## 11.6 DB Migration 예제

다음 작업을 생각해보자.

~~~text
users.status column 추가
API response 변경
migration verification
~~~

모든 것을 Agent에게 자유롭게 맡길 수도 있다.

하지만 일부는 deterministic하게 만들기 쉽다.

~~~text
System
1. migration plan required
2. backward compatibility check required
3. schema test required
4. production apply requires approval
~~~

Agent는 그 안에서 판단한다.

~~~text
Agent
- existing schema 탐색
- migration script 작성
- compatibility issue 진단
- rollback plan 초안
~~~

즉:

~~~text
Deterministic Envelope
        ↓
Agent Judgment
        ↓
Deterministic Gate
~~~

이 구조는 Autonomy를 없애는 것이 아니다.

Autonomy가 유용한 공간을 명확하게 만드는 것이다.

---

## 11.7 LLM 안에 State Machine을 숨기지 않는다

다음 Prompt는 처음에는 편할 수 있다.

~~~text
1. repository를 분석한다.
2. test를 찾는다.
3. 수정한다.
4. 실패하면 다시 분석한다.
5. 최대 두 번 retry한다.
6. security test가 필요하면 실행한다.
7. approval이 필요하면 멈춘다.
~~~

작은 Task에서는 동작할 수 있다.

하지만 Workflow가 커지면 문제가 생긴다.

- 현재 Step이 무엇인지 외부에서 보기 어렵다.
- partial retry가 어렵다.
- timeout과 budget을 통제하기 어렵다.
- approval state를 durable하게 유지하기 어렵다.
- 같은 Step이 중복 실행될 수 있다.

더 나은 구조는 다음과 같다.

~~~text
Executable Workflow
      ↓
LLM Judgment Step
      ↓
Executable Workflow
~~~

LLM은 필요한 판단을 한다.

System은 process state를 관리한다.

---

## 11.8 Recovery도 가장 작은 Scope부터

Agent가 실패했다고 바로 전체 Worker를 재시작할 필요는 없다.

Failure Scope에 따라 대응한다.

~~~text
Tool Retry
→ Step Retry
→ Agent Nudge
→ Subtask Retry
→ Worker Restart
→ Reassignment
→ Human Escalation
~~~

예를 들어 GitHub API가 502를 반환했다.

Code Agent를 새 Worker에서 처음부터 다시 시작할 이유가 없다.

Tool Retry면 충분하다.

반대로 Agent가 계속 같은 잘못된 Architecture를 고집한다면 단순 Tool Retry는 의미가 없다.

Targeted Intervention이나 Reassignment가 필요할 수 있다.

Recovery에도 Control Boundary가 있다.

---

## 11.9 Control Hierarchy

Factory의 Control을 계층으로 보면 다음처럼 정리할 수 있다.

~~~text
Organization Policy
        ↓
Factory Control Plane
        ↓
Workflow / Task Graph
        ↓
Agent Harness
        ↓
Model Decisions
        ↓
Tool Actions
~~~

위쪽으로 갈수록 더 durable하고 authoritative해야 한다.

아래쪽으로 갈수록 더 adaptive하고 probabilistic할 수 있다.

예:

~~~text
Organization Policy
- production secret export 금지

Control Plane
- retry budget = 2

Workflow
- unit → integration → approval

Harness
- available tools

Model
- implementation strategy

Tool
- actual shell command
~~~

이 계층이 있으면 “Agent에게 어디까지 자율성을 줄 것인가”라는 질문을 훨씬 구체적으로 만들 수 있다.

---

## Controlled Autonomy를 설계할 때 묻는 질문

~~~text
1. 이 결정은 이미 정확한 Rule이 있는가?
2. State를 durable하게 기록해야 하는가?
3. 잘못됐을 때 Blast Radius가 큰가?
4. Agent의 탐색 능력이 실제로 필요한가?
5. 같은 판단을 매번 새로 할 이유가 있는가?
6. 결과를 Independent Verification으로 확인할 수 있는가?
~~~

이 질문에 따라 Control 위치를 정한다.

---

## 다음 질문

Agent에게 적절한 Autonomy를 줬다.

그래도 Agent가 만든 결과가 맞는지는 별개의 문제다.

Agent는 자신이 성공했다고 믿을 수 있다.

Test도 통과할 수 있다.

하지만 User Intent를 놓쳤을 수도 있다.

다음 장에서는 **Agent의 완료 보고와 Factory의 완료 판정을 분리하는 Verification 구조**를 다룬다.

---

## 참고 자료

- Agentless  
  https://arxiv.org/abs/2407.01489
- *Deterministic vs. LLM-Controlled Orchestration for COBOL-to-Python Modernization*  
  https://doi.org/10.1145/3805760.3814891
- *Runtime-Structured Task Decomposition for Agentic Coding Systems*  
  https://arxiv.org/abs/2605.15425
- *Wink: Recovering from Misbehaviors in Coding Agents*  
  https://arxiv.org/abs/2602.17037
