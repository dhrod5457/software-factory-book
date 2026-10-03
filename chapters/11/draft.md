# 11장. Controlled Autonomy: 무엇을 시스템에 두고 무엇을 Agent에게 맡길 것인가

에이전트 중심이라는 말은 자주 “에이전트가 더 많은 것을 스스로 결정한다”는 의미로 쓰인다. 하지만 실제 생산 시스템에서 중요한 것은 자율성의 양이 아니다.

**어떤 결정을 누구에게 맡길 것인가**다.

예를 들어 다음 두 결정은 성격이 다르다.

~~~text
이 Task는 Retry를 최대 2회만 허용한다.
~~~

~~~text
이 실패의 원인이 SecurityFilter인지 ExceptionMapper인지 조사한다.
~~~

첫 번째는 이미 알고 있는 운영 규칙이다. 두 번째는 탐색과 판단이 필요한 공학 문제다. 둘 다 에이전트에게 맡길 수는 있다. 하지만 그럴 이유가 있는지는 별개의 문제다. 이 책에서는 다음 원칙을 사용한다.

> 이미 알고 있는 규칙과 상태는 시스템이 책임지고, 사전 규칙화하기 어려운 탐색과 판단에 에이전트 자율성을 사용한다.

---

## 11.1 세 가지 Control Model

생산 시스템의 제어 방식을 단순화하면 세 가지로 볼 수 있다.

### Model A. Deterministic Pipeline

~~~text
Step 1
→ Step 2
→ Step 3
~~~

실행 순서와 분기는 코드가 결정한다. LLM은 각 단계 안에서 제한된 판단만 한다.

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

- 예측 가능
- 오류 분석이 쉽다
- 재시도 경계가 명확하다
- 비용 편차가 낮다

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

에이전트가 작업 흐름 전체를 판단한다.

장점:

- 유연하다
- 예상하지 못한 상황에 대응하기 쉽다
- 새로운 도구 조합을 찾을 수 있다

단점:

- 실행 변동이 커질 수 있다
- 같은 판단을 반복할 수 있다
- 상태와 정책이 대화 기록 안으로 숨어들 수 있다
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

이 책에서는 이 형태를 기본 후보로 본다. 모든 작업 흐름을 정해진 상태 전이로 고정하지도 않고, 모든 진행 결정을 에이전트에게 넘기지도 않는다.

---

## 11.2 Rule, Heuristic, Judgment를 구분한다

제어 경계를 설계할 때 모든 결정을 같은 종류로 보면 어렵다. 세 가지로 나눌 수 있다.

### Rule

정확한 조건이 이미 존재한다.

예:

~~~text
main direct push forbidden
~~~

이건 정책으로 강제할 수 있다. 에이전트에게 “가능하면 하지 마라”라고 말할 필요가 없다.

---

### Heuristic

정답은 아니지만 좋은 기본 판단이 있다.

예:

~~~text
이 Task는 backend-java Worker가 적합할 가능성이 높다.
~~~

이건 경로 선택 정책이나 모델을 쓸 수 있다. 필요하면 대안 경로도 둔다.

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

이런 문제는 에이전트가 잘하는 영역이다. 생산 시스템 설계에서 중요한 것은 세 종류를 섞지 않는 것이다.

---

### 모든 Triage에 LLM이 필요한 것은 아니다

소프트웨어 생산 시스템을 만들기 시작하면 분류와 우선순위 판단, 경로 선택, 배정까지 모두 모델에 맡기고 싶어질 수 있다. 하지만 조건이 이미 명확하면 그럴 이유가 없다. 예를 들어 공개된 한 작은 GitHub 기능을 활용하는 생산 시스템 구현은 이슈에 `ready` 상태가 들어오면 단순 작업 배정기가 가용 워커를 선택한다. 필요하면 LLM으로 버그 / 기능 / 문서 같은 분류를 추가할 수 있지만, 기본 배정 자체에는 LLM이 필수가 아니다.

~~~text
ready task
→ deterministic dispatcher
→ available worker
~~~

반대로 입력의 의미를 해석해야 한다면 모델을 넣을 수 있다.

~~~text
known routing rule
→ code

ambiguous classification
→ optional model

root-cause diagnosis
→ coding agent
~~~

이 사례는 규칙, 경험에 따른 판단 기준, 판단을 나누는 이유를 잘 보여준다.

> **에이전트 중심 시스템의 수준은 LLM 호출 횟수로 결정되지 않는다. 이미 아는 결정을 코드로 남기는 것도 좋은 실행 조율이다.**

---

## 11.3 System이 소유해야 할 상태

다음 상태를 에이전트 대화 기록 안에만 두면 위험하다.

- 작업 상태
- 재시도 횟수
- 시간 초과
- 의존 관계
- 워커 작업 점유권
- 권한
- 비용 한도
- 필수 검증
- 승인 상태

왜냐하면 모델은 이 상태를 잊거나 잘못 해석할 수 있기 때문이다. 예를 들어 지시문에 다음과 같이 적었다고 하자.

~~~text
테스트 실패 시 최대 2번까지만 수정하고,
그래도 실패하면 중단해라.
~~~

에이전트가 정확히 지킬 수도 있다. 하지만 장시간 실행 중 맥락 정보가 압축되거나 도구 실패가 반복되면 이 규칙이 흐려질 수 있다. 더 안전한 구조는 다음이다.

~~~text
Control Plane
retry_budget = 2

Agent
→ attempt
→ result

System
→ retry allowed?
~~~

재시도 한도는 운영 상태다. 모델의 기억에 맡길 이유가 적다. 같은 원리는 권한과 승인에도 적용된다.

---

## 11.4 Agent가 잘하는 영역

반대로 다음은 시스템이 미리 모든 경우를 정의하기 어렵다.

### Repository Exploration

어떤 파일과 코드의 이름과 기호가 관련 있는지 찾는다.

### Diagnosis

실패 원인 후보를 만든다.

### Hypothesis

~~~text
JWT expiry exception이 generic error handler로 흘러가는 것 같다.
~~~

### Implementation Strategy

어떤 계층에서 수정할지 판단한다.

### Debugging Sequence

어떤 테스트와 로그를 먼저 볼지 선택한다.

### Alternative Comparison

두 구현의 장단점을 비교한다. 이 영역까지 모두 정해진 규칙에 따라 실행하도록 만들면, 예상하지 못한 상황에 오히려 쉽게 실패할 수 있다. 에이전트가 가진 강점은 **정답이 이미 코드로 존재하지 않는 탐색 공간에서 다음 행동을 선택하는 능력**에 있다.

---

## 11.5 왜 “더 Agentic”이 항상 더 좋은 것은 아닌가

연구에서도 비슷한 결과가 나온다. Agentless는 2024년 당시 복잡한 자유 에이전트 순환 없이 문제 위치 파악 → 수정 → 검증이라는 구조화된 작업 흐름만으로 경쟁력 있는 SWE-bench 결과를 보여줬다. 현재 최고 성능을 말하는 근거라기보다, 에이전트 설계 구조의 복잡성이 성능의 필수조건은 아니라는 역사적 반례로 보는 편이 적절하다.

2026년 AIware에 발표된 COBOL-to-Python 현대화 연구는 모델, 지시문, 도구, 원본 프로그램을 고정하고 실행 조율 전략만 바꿔 비교했다. 이 실험에서 규칙 기반 실행 조율은 LLM이 제어하는 방식과 비슷한 기능의 정확성을 보이면서 최악의 상황에서의 안정성과 실행 결과의 편차를 개선했고, 토큰 사용은 조건에 따라 최대 3.5배 낮았다.

다만 이 결과는 구조화된 기존 시스템 현대화 작업 유형에 대한 연구다. 모든 코딩 작업에 정해진 규칙에 따른 흐름이 더 낫다고 일반화할 수는 없다. 하지만 한 가지는 분명하다.

> 구조화 가능한 과정에 자율성을 추가한다고 자동으로 품질이 좋아지는 것은 아니다.

에이전트 자율성은 상황에 따라 추가 비용을 만들 수 있다.

- 더 많은 도구 호출
- 더 많은 맥락 정보
- 더 긴 실행 경로
- 더 큰 편차
- 종료 시점의 불확실성

그래서 자율성은 기능 하나를 추가하는 문제가 아니라 장점과 비용을 함께 따져야 하는 선택이다.

---

## 11.6 DB Migration 예제

다음 작업을 생각해보자.

~~~text
users.status column 추가
API response 변경
migration verification
~~~

모든 것을 에이전트에게 자유롭게 맡길 수도 있다. 하지만 일부는 정해진 규칙에 따라 만들기 쉽다.

~~~text
System
1. migration plan required
2. backward compatibility check required
3. schema test required
4. production apply requires approval
~~~

에이전트는 그 안에서 판단한다.

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

이 구조는 자율성을 없애는 것이 아니다. 자율성이 유용한 공간을 명확하게 만드는 것이다.

---

## 11.7 LLM 안에 State Machine을 숨기지 않는다

다음 지시문은 처음에는 편할 수 있다.

~~~text
1. repository를 분석한다.
2. test를 찾는다.
3. 수정한다.
4. 실패하면 다시 분석한다.
5. 최대 두 번 retry한다.
6. security test가 필요하면 실행한다.
7. approval이 필요하면 멈춘다.
~~~

작은 작업에서는 동작할 수 있다. 하지만 작업 흐름이 커지면 문제가 생긴다.

- 현재 단계가 무엇인지 외부에서 보기 어렵다.
- 부분 재시도가 어렵다.
- 시간 초과와 한도를 통제하기 어렵다.
- 승인 상태를 중단돼도 기록이 남도록 유지하기 어렵다.
- 같은 단계가 중복 실행될 수 있다.

더 나은 구조는 다음과 같다.

~~~text
Executable Workflow
      ↓
LLM Judgment Step
      ↓
Executable Workflow
~~~

LLM은 필요한 판단을 한다. 시스템은 프로세스 상태를 관리한다.

---

## 11.8 Recovery Policy도 Agent 밖에 둔다

실패가 발생했을 때 어디까지 되돌릴지 결정하는 것도 제어 문제다. 일시적인 도구 오류와 반복되는 구현 실패를 같은 재시도로 처리하면 비용과 변동성이 커진다. 따라서 복구 한도와 판단 요청 조건은 제어 계층이 소유하고, 에이전트는 필요한 진단과 수정에 집중하는 편이 좋다. 도구 재시도부터 다른 워커에 재배정, 사람에게 판단 요청까지의 구체적인 복구 단계는 14장에서 다룬다.

---

## 11.9 Control Hierarchy

생산 시스템의 제어를 계층으로 보면 다음처럼 정리할 수 있다.

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

위쪽 계층일수록 상태가 오래 보존되고 판단의 기준이 되어야 한다. 아래쪽 계층은 상황에 맞게 적응하거나 확률에 따라 판단할 수 있다.

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

이 계층이 있으면 “에이전트에게 어디까지 자율성을 줄 것인가”라는 질문을 훨씬 구체적으로 만들 수 있다.

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

이 질문에 따라 제어 위치를 정한다.

---

## 다음 질문

에이전트에게 적절한 자율성을 줬다. 그래도 에이전트가 만든 결과가 맞는지는 별개의 문제다. 에이전트는 자신이 성공했다고 믿을 수 있다. 테스트도 통과할 수 있다. 하지만 사용자의 의도를 놓쳤을 수도 있다. 다음 장에서는 **에이전트의 완료 보고와 생산 시스템의 완료 판정을 분리하는 검증 구조**를 다룬다.

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
- *I Built the Simplest Software Factory*, YouTube video / user-provided transcript  
  https://www.youtube.com/watch?v=AsvzMlLyQ38
