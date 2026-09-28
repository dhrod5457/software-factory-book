# Academic Synthesis: AI Software Factory Design Principles

기준일: 2026-09-28

이 문서는 지금까지 수집한 논문/실증 연구에서 **반복적으로 지지되는 설계 원칙**을 추출한다.

아직 `planning/concept.md`가 아니다.

연구 증거의 강도를 확인하기 위한 중간 synthesis다.

---

# Principle 1. Model 성능과 System 성능을 분리한다

근거:

- SWE-agent: ACI 영향
- OpenHands SDK: runtime/lifecycle/sandbox
- AI Agents That Matter: cost/reproducibility
- RuBench: deployed product가 평가 단위일 수 있음

따라서:

```text
Factory Capability
≠ Model Capability
```

Factory 평가에는:

- context
- harness
- tools
- runtime
- verification
- policy

가 포함되어야 한다.

증거 강도: 강함.

---

# Principle 2. Autonomous Control은 선택적으로 사용한다

근거:

- Agentless
- deterministic vs LLM-controlled orchestration
- runtime-structured decomposition

구조화 가능한 단계는 code-driven control이 더 안정적/저렴할 수 있다.

Agent는:

- search
- diagnosis
- open-ended judgment

에 집중.

증거 강도: 강함.

---

# Principle 3. Task Specification은 Worker보다 앞선다

근거:

- REAgent
- Spec Kit / Kiro industry evidence
- Human-AI context gap
- building-to-test 문제

모호한 input에 강한 Agent를 붙이는 것보다:

- clarification
- structured requirement
- acceptance

가 중요하다.

증거 강도: 중간~강함.

---

# Principle 4. Context는 많을수록 좋지 않다

근거:

- SWE-agent ACI
- SWE-Explore
- AGENTS.md evaluation
- context file ablation

Context file이:

- exploration 증가
- cost 증가

를 만들지만 task success는 개선하지 않을 수 있다.

따라서:

> Progressive, Relevant, Minimal Context.

증거 강도: 강함.

---

# Principle 5. Verification은 독립 Authority를 가져야 한다

근거:

- METR maintainer review gap
- Building to the Test
- reward hacking
- Fixpad++
- separate evaluator research

Agent self-report를 final truth로 두면 안 된다.

```text
Agent proposes
Verifier decides evidence
Policy/Human accepts
```

증거 강도: 매우 강함.

---

# Principle 6. Recovery는 Production Agent의 핵심 기능이다

근거:

- Wink production trajectory
- Anthropic long-running harness
- OpenHands SDK
- Durable execution systems

Agent가 한번에 성공하는 것보다:

- drift 감지
- targeted intervention
- retry
- resume

가 실제 reliability를 결정한다.

증거 강도: 강함.

---

# Principle 7. Execution Authority와 Acceptance Authority를 분리한다

근거:

- AIware PR lifecycle study
- human-agent collaboration study
- accountability research
- NIST governance

실제 공개 workflow에서 Agent가 실행을 주도해도 merge/acceptance는 사람에게 남는 경우가 많다.

증거 강도: 강함.

---

# Principle 8. Multi-Agent는 Task Structure가 허용할 때만 사용한다

근거:

- Anthropic multiagent research
- GitHub Fleet industry evidence
- Agentless/simple baseline research

Agent 수가 늘면:

- conflict
- duplicated context
- coordination
- correlated error

가 증가할 수 있다.

증거 강도: 강함.

---

# Principle 9. Trajectory도 Outcome만큼 중요하다

근거:

- AgentLens Lucky Pass
- RigorBench
- Wink
- reward hacking research

PASS라도:

- blind retry
- unsafe path
- test manipulation

이면 production confidence가 낮다.

증거 강도: 중간~강함.

---

# Principle 10. Human Collaboration은 독립 품질 축이다

근거:

- Humans are Missing position paper
- AIware human-agent studies
- Dialogue SWE-Bench
- HHAI context-gap study

측정 후보:

- alignment
- steerability
- verifiability
- adaptability

증거 강도: 중간.

분야 자체가 아직 성장 중이다.

---

# Principle 11. Factory는 Socio-Technical System이다

근거:

- human-agent PR study
- accountability
- DORA
- NIST
- trustworthy-change theory

Factory가 바꾸는 것은 code generation만이 아니다.

- review pattern
- responsibility
- communication
- approval
- team flow

도 바뀐다.

증거 강도: 강함.

---

# Principle 12. Benchmark 하나로 Autonomy를 판단하지 않는다

근거:

- SWE-bench contamination
- SWE-Lancer
- SWE-rebench
- AI Agents That Matter
- performance benchmark audit

필요:

- multiple task types
- fresh tasks
- human evaluation
- cost
- environment reporting

증거 강도: 매우 강함.

---

# Principle 13. Durable External State는 Long-Horizon의 전제다

근거:

- Anthropic long-running agent
- OpenHands SDK
- Durable Task / Temporal / Agent Executor industry/runtime evidence

Context window만으로:

- long task
- crash
- reassignment

을 안정적으로 처리하기 어렵다.

증거 강도: 강함.

---

# Principle 14. Repository Configuration도 Software다

근거:

- Agent README empirical study
- Agent configuration study
- context file governance 연구

AGENTS.md, Skills, Hooks, MCP config 등이 future Agent behavior를 바꾼다.

따라서:

- version
- review
- owner
- eval

이 필요하다.

증거 강도: 중간~강함.

---

# Principle 15. Factory의 최적화 단위는 "Accepted Change"다

학술 + 산업 자료를 합친 후보.

단순:

- tokens
- PR count
- Agent runs

보다:

- accepted
- verified
- integrated
- low rework

변경이 중요하다.

직접적인 단일 논문의 확립된 metric은 아니므로 책의 synthesis로 표시해야 한다.

증거 강도: 중간.

---

# 설계 원칙을 Architecture로 변환

```text
Intent
  ↓
Structured Task / Acceptance
  ↓
Durable Control Plane
  ↓
Hybrid Orchestration
  ├─ Deterministic Rules
  └─ Agent Judgment
  ↓
Relevant Context Assembly
  ↓
Isolated Agent Runtime
  ↓
Implementation
  ↓
Independent Verification
  ↓
Evidence
  ↓
Acceptance Authority
  ↓
Delivery
  ↓
Production Feedback
  ↓
Eval / Factory Improvement
```

---

# Concept 정의에 가까워진 부분

현재 자료를 종합하면 AI Software Factory의 핵심에는 최소 다음이 반복적으로 나타난다.

### 1. Durable Work

Prompt/session보다 오래가는 Task.

### 2. Delegated Execution

Agent가 actual environment에서 실행.

### 3. Controlled Autonomy

deterministic rule과 model judgment 분리.

### 4. Independent Verification

self-report와 completion 분리.

### 5. Recoverability

retry / resume / reassignment.

### 6. Acceptance / Governance

누가 최종 risk를 받아들이는지 명확.

### 7. Feedback

실패와 운영 결과가 다음 work/system improvement로 돌아감.

---

# 아직 약한 부분

다음은 concept 정의의 필수 요소로 확정하기 전에 더 조심해야 한다.

### Automatic Work Selection

proactive examples는 있지만 보편적 requirement는 아님.

### Multi-Agent

Factory에 필수 아님.

### Self-Improvement

고급 capability이지 최소 정의일 가능성 낮음.

### Fully Autonomous Merge

현재 empirical workflow에서는 human approval이 여전히 강함.

### Requirement Generation

Agent가 작성할 수 있지만 authoritative requirement owner와는 별개.

---

# 현재 가장 강한 최소 정의 후보

아직 최종 문구 아님:

> AI Software Factory는 소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 생산 시스템이다.

이 정의의 장점:

- Multi-Agent를 필수로 만들지 않음
- Fully Autonomous를 필수로 만들지 않음
- CI/CD와 구분 가능
- Agent Platform과 구분 가능
- Human Gate의 위치를 policy로 열어둠

---

# Research 단계 종료 판단 기준

다음이 충족되면 `planning/concept.md`로 이동 가능하다.

- 최소 정의의 각 핵심 요소에 독립된 2개 이상의 근거
- 반례 문서화
- 인접 개념 경계 정리
- 산업 사례 + 학술 연구 모두 확보
- human role / governance 포함
- benchmark 한계 포함

현재는 이 조건에 상당 부분 도달했다.
