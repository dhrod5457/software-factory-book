# Context Files and Repository Governance: Empirical Evidence

기준일: 2026-09-28

AGENTS.md, CLAUDE.md 같은 context file은 Agent-ready repository의 대표적인 실무 패턴이 되었다.

하지만 연구 결과는 단순하지 않다.

> Context file이 존재한다고 task success가 자동으로 증가하지 않는다.

이 문서는 실제 empirical evidence를 비교한다.

---

# 1. Agent README는 새로운 Software Artifact

대규모 empirical study:

- 2,303 agent context files
- 1,925 repositories

분석된 파일:

- CLAUDE.md
- AGENTS.md
- copilot-instructions.md

연구는 이 파일들이 static documentation이 아니라:

- 자주 수정되고
- configuration처럼 진화하며
- project-specific rule을 저장

하는 artifact라고 본다.

출처:

- Agent READMEs: An Empirical Study of Context Files for Agentic Coding
  - https://arxiv.org/abs/2511.12884

---

# 2. 무엇을 주로 적는가

연구에서 많이 나타난 정보:

- implementation detail
- architecture
- build/run/test 절차

반대로 낮은 비중:

- security
- performance

대략 14~15% 수준으로 보고되었다.

Factory 연결:

> Context file을 작성했다고 Governance가 완성되는 것이 아니다.

Functional success guide가 중심이고 non-functional guardrail은 부족할 수 있다.

---

# 3. Configuration Mechanism은 Context File보다 넓다

AIware 2026 empirical study는 5개 coding tool의 repository-level configuration을 분석했다.

식별된 8개 mechanism:

- Context Files
- Skills
- Subagents
- Commands
- Rules
- Settings
- Hooks
- MCP Servers

2,000개 이상 repository를 분석한 결과:

- Context File이 가장 지배적
- AGENTS.md가 interoperable convention으로 부상
- Skills/Subagents는 아직 shallow adoption

출처:

- Configuring Agentic AI Coding Tools: An Exploratory Study
  - AIware 2026
  - https://arxiv.org/abs/2602.14690
  - https://doi.org/10.1145/3805760.3814887

Factory 연결:

Repository customization은 점점 versioned infrastructure가 되고 있다.

---

# 4. 그런데 AGENTS.md가 성능을 낮출 수도 있다

ICLR 2026 workshop 연구는 coding agent task success를 context file 유무로 비교했다.

결과:

- task success improvement 없음
- 일부 조건에서 감소
- inference cost 20% 이상 증가
- broader exploration/test를 유도
- agent가 instruction은 잘 따름

연구 결론:

> 불필요한 requirement가 Task를 어렵게 할 수 있으므로 context file은 최소 요구사항 중심이어야 한다.

출처:

- Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?
  - https://arxiv.org/abs/2602.11988
  - https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd

---

# 5. 다른 2026 Ablation도 Correctness Effect를 찾지 못함

두 frontier agent를 이용한 소규모 controlled ablation에서는:

- context strategy가 task correctness를 유의미하게 바꾸지 않음
- failure 원인이 repository knowledge보다 implementation skill인 경우가 많음

출처:

- Do Context Files Help Coding Agents?
  - https://arxiv.org/abs/2607.27250

주의:

17 real tasks / 3 repositories의 작은 연구이므로 일반화에 제한이 있다.

---

# 6. Context File은 "More Context"가 목적이 아니다

현재 연구를 합치면:

Bad:

```text
AGENTS.md
= 모든 project knowledge를 한 파일에 넣기
```

Better:

```text
AGENTS.md
= 최소 invariant / navigation entry point
```

나머지:

- architecture docs
- skills
- tool
- catalog
- test
- policy

로 분리하는 편이 후보 원칙이다.

---

# 7. Instruction과 Enforcement를 분리

Context file에:

> 절대로 secret을 commit하지 마라.

라고 쓰는 것보다:

- secret scanner
- hook
- permission
- protected path

가 더 강한 enforcement다.

즉:

```text
Instruction
= Agent decision guidance

Enforcement
= System guarantee
```

---

# 8. Context File의 좋은 내용 후보

연구와 실무를 합친 최소 내용:

- project purpose
- relevant architecture map
- build/test entry point
- important conventions
- change boundary
- where to find deeper docs

불필요하게:

- 매우 상세한 tutorial
- 모든 edge case
- duplicate documentation

을 넣지 않는다.

---

# 9. Agent Context는 Versioned Governance Artifact

Context file이 Agent behavior에 실제 영향을 주기 때문에:

- code review
- owner
- change history
- test/eval

대상이 될 수 있다.

특히 global instruction 변경은 많은 future Agent run에 영향을 준다.

---

# 10. Values / Ethics도 Context에 들어가기 시작

AIware 2026 vision paper는 repository context file에:

- fairness
- accessibility
- sustainability
- tone
- privacy

같은 지침이 포함되는 사례를 조사한다.

출처:

- Operationalizing Ethics for AI Agents
  - https://arxiv.org/abs/2605.05584
  - https://doi.org/10.1145/3805760.3814899

이것은 자연어 context가 governance layer 역할을 시작했음을 보여준다.

하지만 adherence는 별도 검증이 필요하다.

---

# 11. Context Freshness

Agent README 연구는 파일이 지속적으로 진화하는 artifact임을 보여준다.

문제:

- architecture changed
- instruction stale
- test command changed
- deleted subsystem still mentioned

따라서 context file도 drift detection 대상이다.

---

# 12. Progressive Disclosure

후보 구조:

```text
AGENTS.md
→ Architecture Index
→ Relevant Module Doc
→ Skill
→ Tool Result
```

현재 Task에 필요한 context만 단계적으로 가져온다.

SWE-Explore의 context-efficiency 연구와도 연결된다.

---

# 13. Context Quality Metric 후보

- relevance
- freshness
- contradiction
- duplication
- token cost
- instruction compliance
- task success impact

"파일이 있는가?"보다 quality가 중요하다.

---

# 14. Factory 연결

Factory는 Task마다:

- relevant instruction
- skill
- policy
- catalog
- environment

를 조립해 Context Package를 만들 수 있다.

Repository 전체 context를 항상 동일하게 전달할 필요가 없다.

---

# 핵심 후보 메시지

> Agent context file은 중요한 새로운 engineering artifact지만 만능 성능 향상 장치는 아니다.

> 더 많은 context보다 더 적고 정확한 context가 유리할 수 있다.

> Context와 Policy를 구분하고, 반드시 지켜야 하는 규칙은 deterministic enforcement로 내려야 한다.

> AI Software Factory는 context file을 읽는 수준을 넘어 Task별로 적절한 knowledge, skill, tool, policy를 조립하는 Context System이 필요하다.
