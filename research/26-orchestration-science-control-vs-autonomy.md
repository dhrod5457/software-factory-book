# Orchestration Science: Control vs Autonomy

기준일: 2026-09-28

AI Software Factory의 중요한 설계 문제:

> Workflow control을 어디까지 Agent에게 넘길 것인가?

현재 연구는 "더 Agentic할수록 좋다"는 단순한 결론을 지지하지 않는다.

---

# 1. 세 가지 Control Model

## Model A - Deterministic Pipeline

```text
Step 1
→ Step 2
→ Step 3
```

Code/System이 execution order를 결정.

LLM은 각 step의 bounded judgment 수행.

## Model B - Agent-controlled

```text
Goal
→ Agent chooses tools/order
→ Agent decides completion
```

## Model C - Hybrid Runtime

```text
System owns:
- state
- policy
- retry
- dependency

Agent owns:
- search
- diagnosis
- implementation strategy
```

현재 자료에서는 Model C가 가장 일반화 가능한 후보로 보인다.

---

# 2. Agentless의 교훈

Agentless는 자유로운 agent loop 대신:

- localization
- repair
- validation

이라는 고정 workflow를 사용했다.

복잡한 Agent architecture 없이도 당시 강한 benchmark 결과를 냈다.

출처:

- https://arxiv.org/abs/2407.01489

의미:

> Search space가 구조화 가능한 Task에 full autonomy를 넣는 것은 overhead일 수 있다.

---

# 3. Deterministic Orchestration Controlled Study

AIware 2026 modernization 연구:

- orchestration만 experimental variable로 분리
- deterministic vs LLM-controlled 비교

결과:

- accuracy comparable
- deterministic worst-case robustness 우수
- variability 낮음
- token 최대 3.5x 감소

출처:

- https://doi.org/10.1145/3805760.3814891

이것은 Software Factory에 매우 직접적인 결과다.

---

# 4. Static Decomposition도 항상 좋지 않다

Runtime-Structured Task Decomposition 연구:

### Monolithic

한 workflow 전체 재실행.

### Static Decomposition

subtask는 나누지만 failure 후 downstream 재실행 비용 존재.

### Runtime-Structured

control logic이 dependency/failure를 관리해 failed subtask만 rerun.

출처:

- https://arxiv.org/abs/2605.15425

핵심:

> Decomposition 자체보다 failure semantics가 중요하다.

---

# 5. Workflow Engine과 Prompt를 분리

Bad:

```text
Prompt:
1. inspect
2. analyze
3. test
4. if fail ...
5. if condition ...
...
```

문제:

- state가 implicit
- branch debug 어려움
- partial retry 어려움

Better:

```text
Executable Workflow
  ↓
LLM Judgment Step
```

Agent에게 process control을 자연어로만 맡기지 않는다.

---

# 6. Wink: Agent 자체를 수정하지 않고 Recovery Layer 추가

Wink는 Agent trajectory를 external observer가 감시한다.

```text
Primary Agent
      ↓ events
Observer
      ↓
Targeted Intervention
```

중요:

- primary model 교체 없이 system reliability 개선
- Agent failure를 runtime에서 감지/복구

출처:

- https://arxiv.org/abs/2602.17037

Factory 연결:

Supervisor/Monitor Agent가 항상 일을 대신할 필요는 없다.

필요할 때만 intervention하는 구조가 가능하다.

---

# 7. Control Plane은 Model 밖에 있어야 하는가

강한 후보:

다음 상태는 model transcript 안이 아니라 external durable system이 authoritative해야 한다.

- Task status
- retry count
- approval
- dependency
- worker lease
- cost budget
- verification result

이유:

model은:

- hallucinate
- forget
- redefine state

할 수 있다.

---

# 8. Agent가 잘하는 Control

Agent에게 유리한 영역:

- unknown code exploration
- hypothesis generation
- debugging sequence
- implementation alternative
- tool choice among safe tools
- ambiguity identification

사전에 state machine으로 모두 모델링하기 어렵다.

---

# 9. System이 잘하는 Control

deterministic system에 유리:

- retry count
- timeout
- permission
- dependency
- budget
- required test
- deployment order
- approval state

정확한 rule이 이미 존재한다면 LLM에게 재판단시킬 이유가 적다.

---

# 10. Rule / Heuristic / Judgment 구분

### Rule

```text
main direct push forbidden
```

→ deterministic.

### Heuristic

```text
이 Task는 backend worker가 적합할 확률 높음
```

→ policy/model routing 가능.

### Judgment

```text
어떤 구현 전략이 가장 적합한가?
```

→ Agent.

Factory 설계에서 세 가지를 섞지 않는다.

---

# 11. Orchestration Cost

Orchestration layer 자체도 cost가 있다.

- Agent handoff
- context duplication
- scheduling delay
- subagent calls
- reconciliation

따라서:

```text
More Structured
≠ Always Cheaper

More Agentic
≠ Always Better
```

실제 workload로 비교해야 한다.

---

# 12. Multi-Agent Orchestration

Multi-agent를 사용할 경우 추가 control:

- ownership
- dependency
- shared state
- merge conflict
- budget
- termination

Anthropic multi-agent 연구에서 coordination failure가 관찰된 이유와 연결된다.

---

# 13. Control Hierarchy 후보

```text
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
```

위 계층일수록:

- 더 deterministic
- 더 durable
- 더 authoritative

아래로 갈수록:

- 더 adaptive
- 더 probabilistic

하게 설계하는 것이 후보 원칙이다.

---

# 14. Recovery Hierarchy

실패 시 바로 full restart하지 않는다.

```text
Tool Retry
→ Step Retry
→ Agent Nudge
→ Subtask Retry
→ Worker Restart
→ Reassignment
→ Human Escalation
```

각 failure class에 가장 작은 recovery scope를 선택한다.

---

# 15. Orchestration Evals

평가 항목:

- same failure repeated?
- correct step rerun?
- retry budget obeyed?
- duplicate external action?
- stuck loop?
- unnecessary subagent?
- human escalation timing?

Outcome correctness만으로 orchestration quality를 평가하지 않는다.

---

# 핵심 후보 메시지

> Software Factory는 모든 결정을 Agent에게 주는 시스템이 아니라 deterministic control과 probabilistic judgment의 경계를 설계하는 시스템이다.

> 이미 알고 있는 workflow rule을 LLM에게 다시 추론시키면 variability와 cost가 증가할 수 있다.

> Agent autonomy는 search와 adaptation에 쓰고, state·policy·budget·dependency는 가능한 한 system이 책임지는 구조가 현재 연구와 가장 잘 맞는다.
