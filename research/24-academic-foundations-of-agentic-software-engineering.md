# Academic Foundations of Agentic Software Engineering

기준일: 2026-09-28

이 문서는 AI Software Factory의 기반이 되는 Agentic Software Engineering 연구를 제품 문서가 아닌 논문 중심으로 정리한다.

핵심 질문:

> 어떤 연구 결과가 "좋은 모델"을 넘어 "좋은 Software Factory 시스템"의 설계 원칙을 뒷받침하는가?

---

# 1. Software Engineering Agent 연구는 이미 독립 분야로 형성 중

2024~2026 survey들은 Software Engineering에서 LLM-based Agent를 단순 code generation과 구분한다.

반복되는 Agent 특성:

- environment perception
- memory/context
- tool/action
- iterative feedback
- autonomous decision
- human interaction
- multi-agent collaboration

대표 survey:

- From LLMs to LLM-based Agents for Software Engineering
  - https://arxiv.org/abs/2408.02479
- Large Language Model-Based Agents for Software Engineering: A Survey
  - https://arxiv.org/abs/2409.02977
- Agents in Software Engineering: Survey, Landscape, and Vision
  - https://arxiv.org/abs/2409.09030

중요:

survey 자체가 Factory를 정의하지는 않는다.

하지만 Agentic SWE가 다음 SDLC 범위를 포함한다는 근거가 된다.

- requirements
- design
- coding
- test
- maintenance
- autonomous decision

---

# 2. SWE-agent: Model 성능만큼 Interface가 중요하다

SWE-agent의 핵심 연구 가설:

> Agent도 새로운 종류의 computer user이며 Agent에 맞는 interface가 필요하다.

SWE-agent는 Agent-Computer Interface(ACI)를 설계해:

- repository navigation
- code edit
- command execution
- feedback

을 모델이 사용하기 쉽게 만들었다.

연구의 의미:

```text
Agent Capability
=
Model
× Interface
× Environment
```

정확한 곱셈식은 아니지만 시스템 사고 모델로 유용하다.

출처:

- SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
  - NeurIPS 2024
  - https://arxiv.org/abs/2405.15793

Factory 연결:

- Tool UX
- concise output
- edit feedback
- command semantics

는 단순 부가 기능이 아니라 성능 변수다.

---

# 3. Agentless: 더 복잡한 Agent가 항상 좋은 것은 아니다

Agentless 연구는 다음 질문을 제기했다.

> 정말 복잡한 autonomous agent가 항상 필요한가?

Agentless는:

```text
Localization
→ Repair
→ Patch Validation
```

이라는 단순 pipeline을 사용한다.

핵심:

- LLM에게 자유로운 future-action control을 크게 주지 않음
- 복잡한 tool loop를 줄임
- 당시 SWE-bench Lite에서 강한 성능과 낮은 cost를 달성

중요한 연구 메시지:

> Agent autonomy는 목적이 아니다.

구조화 가능한 workflow는 deterministic orchestration이 더 단순하고 효율적일 수 있다.

출처:

- Agentless: Demystifying LLM-based Software Engineering Agents
  - https://arxiv.org/abs/2407.01489

---

# 4. OpenHands: Generalist Software Agent Platform

OpenHands 연구는 software development agent를 위한 platform 요소를 넓게 정의한다.

포함:

- code editing
- command line
- browser
- sandbox
- multi-agent coordination
- benchmark integration

출처:

- OpenHands: An Open Platform for AI Software Developers as Generalist Agents
  - https://arxiv.org/abs/2407.16741

Factory 연결:

OpenHands는 Factory 자체보다 **Worker/Agent Platform** 쪽에 가깝다.

중요한 점은 다음 계층을 실제 연구 구현으로 분리했다는 점이다.

```text
Agent
Tools
Sandbox
User Interface
Evaluation
```

---

# 5. OpenHands Software Agent SDK: Production Agent Runtime 연구

후속 OpenHands SDK 연구는 production-ready software agent에 필요한 요소를 명확히 확장한다.

- custom tools
- memory
- local/remote execution
- REST/WebSocket
- sandbox
- lifecycle control
- multi-model routing
- security analysis
- user interfaces

2026 update에서는 production deployment data를 통해 V1이 이전 architecture보다 system-attributable failures를 줄였다고 보고한다.

출처:

- The OpenHands Software Agent SDK
  - https://arxiv.org/abs/2511.03690

Factory 연결:

> Agent reasoning loop만 잘 만들어서는 production worker가 되지 않는다.

필요:

- lifecycle
- remote execution
- failure handling
- isolation
- API boundary

---

# 6. Requirement 품질이 Agent 성능의 입력 변수다

REAgent 연구는 issue description을 곧바로 implementation prompt로 사용하는 기존 방식의 문제를 지적한다.

문제:

- missing context
- ambiguity
- incomplete requirement

REAgent는 issue-oriented structured requirements를 먼저 만들고 품질을 분석/개선한다.

실험에서는 여러 benchmark/model에서 baseline 대비 resolved issue 수가 평균 17.40% 개선됐다고 보고한다.

출처:

- REAgent: Requirement-Driven LLM Agents for Software Issue Resolution
  - https://arxiv.org/abs/2604.06861

Factory 연결:

```text
Better Coding Agent
만이 아니라
Better Task Specification
```

이 중요하다.

즉 Factory의 front-end requirement pipeline이 worker 성능을 결정한다.

---

# 7. Runtime-Structured Task Decomposition

2026 연구는 monolithic prompt와 static task decomposition을 비교한다.

핵심 발견:

- 단순히 Task를 여러 개로 쪼갠다고 retry cost가 줄지 않음
- static decomposition은 downstream subtask까지 다시 실행해 오히려 비쌀 수 있음
- runtime control logic으로 failed subtask만 다시 실행하면 retry cost 감소

보고된 두 workload에서 runtime-structured 방식은 monolithic/static 대비 retry cost를 크게 줄였다.

출처:

- Runtime-Structured Task Decomposition for Agentic Coding Systems
  - https://arxiv.org/abs/2605.15425

Factory 연결:

> Task decomposition은 prompt-writing 기법이 아니라 execution graph 설계 문제다.

이것은 Durable Task / Retry Scope 설계와 직접 연결된다.

---

# 8. Deterministic vs LLM-Controlled Orchestration

AIware 2026 연구는 COBOL-to-Python modernization에서:

- model
- prompt
- tool
- configuration

을 같게 유지하고 orchestration strategy만 바꿨다.

결과:

- deterministic orchestration이 comparable accuracy
- worst-case robustness 개선
- run variation 감소
- token 사용 최대 3.5x 감소

출처:

- Deterministic vs. LLM-Controlled Orchestration for COBOL-to-Python Modernization
  - AIware 2026
  - https://doi.org/10.1145/3805760.3814891
  - https://arxiv.org/abs/2605.09894

Factory 연결:

```text
Known Process
→ deterministic control

Unknown Search / Diagnosis
→ Agent control
```

이라는 hybrid boundary가 연구 근거를 갖는다.

---

# 9. Resilient Agent는 Misbehavior Recovery가 필요하다

Meta 연구진의 Wink는 production coding-agent traffic에서 misbehavior를 분류했다.

세 범주:

- Specification Drift
- Reasoning Problems
- Tool Call Failures

연구는 약 30%의 trajectory에서 이런 misbehavior가 나타났다고 보고한다.

Wink는 asynchronous observer가 trajectory를 감시해 targeted intervention을 제공한다.

10,000+ real trajectories 평가에서 single intervention이 필요한 misbehavior의 90%를 복구했다고 보고한다.

출처:

- Wink: Recovering from Misbehaviors in Coding Agents
  - https://arxiv.org/abs/2602.17037

Factory 연결:

> Retry는 같은 Agent를 다시 실행하는 것만이 아니다.

더 발전된 형태:

```text
Observe Trajectory
→ Classify Failure
→ Targeted Recovery
→ Continue
```

---

# 10. Repository Exploration은 독립 능력이다

SWE-Explore는 coding task를 단순 resolved/unresolved로 보지 않고 repository exploration을 별도로 측정한다.

평가:

- coverage
- ranking
- context efficiency

848 issues / 10 languages / 203 repositories를 다룬다.

연구는 file-level localization보다 line-level context selection과 ranking이 state-of-the-art agent 간 차이를 만드는 중요한 축이라고 보고한다.

출처:

- SWE-Explore
  - https://arxiv.org/abs/2606.07297

Factory 연결:

Context retrieval은 단순 prompt preprocessing이 아니라 measurable subsystem이다.

---

# 11. Repository-level Reasoning의 Integration Width 문제

RepoReason 연구는 repository-level reasoning을 white-box 방식으로 진단한다.

측정:

- reading load
- simulation depth
- integration width

연구에서는 여러 파일/논리를 통합해야 하는 width가 중요한 bottleneck으로 나타났다고 보고한다.

출처:

- From Laboratory to Real-World Applications: Benchmarking Agentic Code Reasoning at the Repository Level
  - https://arxiv.org/abs/2601.03731

Factory 연결:

Task를 지나치게 크게 만들어 integration width를 늘리면 모델 능력 한계를 직접 건드릴 수 있다.

---

# 12. Research Principle 후보

현재 학술 자료에서 강하게 지지되는 설계 원칙:

### P1. Model 외 시스템 요소가 성능 변수다

- interface
- context
- tool
- environment

### P2. Autonomy는 무조건적인 장점이 아니다

- Agentless
- deterministic orchestration 연구

### P3. Requirement quality가 execution quality의 상한을 만든다

- REAgent

### P4. Decomposition은 execution semantics와 함께 설계해야 한다

- runtime-structured decomposition

### P5. Production Agent에는 Recovery Layer가 필요하다

- Wink
- OpenHands SDK

### P6. Repository understanding을 독립 subsystem으로 봐야 한다

- SWE-Explore
- RepoReason

---

# 13. Factory 관점의 학술적 추상화

```text
Task Quality
      ↓
Context / Repository Understanding
      ↓
Control Strategy
      ↓
Agent Reasoning
      ↓
Tool / Environment Interaction
      ↓
Validation Feedback
      ↓
Recovery
      ↓
Verified Result
```

어느 한 단계만 model scale로 대체할 수 있다는 근거는 현재 없다.

---

# 핵심 후보 메시지

> Agentic Software Engineering 연구는 Software Factory가 단순히 강한 Coding Model을 둘러싼 wrapper가 아니라는 점을 반복해서 보여준다.

> Interface, Task specification, orchestration, context retrieval, validation, recovery를 분리해 설계하고 평가해야 한다.

> "Agentic"한 정도를 최대화하기보다 어떤 결정은 deterministic하게 고정하고 어떤 결정만 모델에게 위임할지 찾는 것이 더 중요한 engineering 문제다.
