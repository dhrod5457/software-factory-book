# Human-Agent Collaboration and Responsibility Research

기준일: 2026-09-28

AI Software Factory가 실제 조직에서 동작하려면 Agent task success만으로는 부족하다.

사람과 Agent 사이에서 다음이 어떻게 배분되는지가 중요하다.

- initiative
- steering
- verification
- approval
- responsibility
- communication

이 문서는 2026년 empirical / human-centered research를 중심으로 정리한다.

---

# 1. Agent가 PR을 만들면 협업 구조 자체가 달라진다

AIware 2026 연구:

- 40,214 pull requests
- 2,807 GitHub repositories
- 33,596 agent-authored PR
- 6,618 human-authored PR

관찰:

- agent-authored PR이 더 빠르게 integration되는 경향
- 그러나 전체 merge rate는 낮음
- documentation task에서는 agent가 상대적으로 강함
- behavior-changing contribution에서는 상대적으로 약함
- review communication도 더 analytic / bot-oriented하게 변함

출처:

- When Code Authors Are Agents
  - AIware 2026
  - https://doi.org/10.1145/3805760.3814909

Factory 연결:

> Agent output이 늘어나면 repository의 사회적 workflow도 바뀐다.

따라서 review queue와 collaboration quality를 metric에 넣어야 한다.

---

# 2. Operational Agency와 Merge Authority는 분리된다

다른 AIware 2026 연구는 29,585 PR lifecycle을 분석해:

```text
Initiator
×
Approver
```

taxonomy를 사용했다.

분석 대상 5개 tool:

- OpenAI
- GitHub Copilot
- Devin
- Cursor
- Claude Code

핵심:

- 일부 tool은 agent가 PR lifecycle을 적극 시작
- 그러나 terminal merge authority는 거의 항상 human에 남음

논문의 표현으로:

> Agency와 Governance는 decouple될 수 있다.

출처:

- Collaborator or Assistant? How AI Coding Agents Partition Work across Pull Request Lifecycles
  - AIware 2026
  - https://doi.org/10.1145/3805760.3814893

Factory 연결:

Autonomy를 단일 축으로 측정하면 부족하다.

최소 분리:

```text
Work Initiation Authority
Execution Authority
Verification Authority
Acceptance Authority
Merge/Deploy Authority
```

---

# 3. "Humans Are Missing" 비판

2026 position paper는 기존 coding-agent research가 autonomous task completion에 과도하게 집중한다고 지적한다.

제안하는 human-agent quality dimension:

- Task Alignment
- Verifiability
- Steerability
- Adaptability

출처:

- Humans are Missing from AI Coding Agent Research
  - https://arxiv.org/abs/2608.12355

Factory 연결:

완전 자동화율 외에 다음을 측정해야 한다.

- 사람이 잘못된 방향을 얼마나 쉽게 고칠 수 있는가
- Agent 결과를 얼마나 빠르게 검증할 수 있는가
- requirement 변화에 얼마나 잘 적응하는가

---

# 4. Collaborative Agent Behavior Taxonomy

Google 연구진의 AIware 2026 연구는:

- 91 sets of developer-defined rules
- 15 experienced professional developer interviews

를 바탕으로 desirable SWE Agent behavior taxonomy를 만들었다.

네 범주:

1. Adhere to Standards and Processes
2. Ensure Code Quality and Reliability
3. Solve Problems Effectively
4. Collaborate with the Developer

출처:

- Towards AI as a Collaborative Partner
  - AIware 2026
  - https://doi.org/10.1145/3805760.3814913

Factory 연결:

Correctness-only acceptance는 enterprise Agent quality의 일부만 측정한다.

---

# 5. Human-AI Context Gap

HHAI 2026 qualitative study는 수개월간 Claude Code와 실제 system을 만들고 debugging한 163 interaction episodes를 분석했다.

식별한 breakdown theme:

- Human-AI context gap
- Asymmetrical / unsynchronized learning
- Trust-erosion spiral
- Error-expanding spiral

출처:

- Reliable Vibe Coding: The Human-AI Context Gap in Software Development
  - HHAI 2026
  - https://doi.org/10.3233/FAIA260505

Factory 연결:

사람과 Agent가 같은 Task를 보고 있어도 mental model이 같다는 보장은 없다.

Durable specification / evidence / task state가 collaboration artifact로 필요한 이유가 된다.

---

# 6. Dialogue Ability는 Coding Ability와 별개일 수 있다

Dialogue SWE-Bench는 기존 autonomous benchmark와 달리 user dialogue를 포함한다.

연구 결과:

> 더 좋은 coding model이 항상 더 좋은 dialogue model은 아니다.

출처:

- Dialogue SWE-Bench
  - https://arxiv.org/abs/2606.13995

Factory 연결:

Human-in-the-loop task에서는:

- clarification
- question quality
- uncertainty communication

도 별도 capability다.

---

# 7. Software Testing에서도 Human-AI Interaction Design이 중요

2026 ACM TOCHI 연구는 software test case development에서 human-AI interaction strategy를 실증적으로 연구한다.

연구 배경은 autonomous system만 강조하면 실제 workflow에서 존재하는:

- prior design
- post-review

의 human involvement를 놓친다는 점이다.

출처:

- Preemptive, Buffered, or Guided? Empirical Studies on Human–AI Interaction Strategies for Software Test Case Development
  - ACM TOCHI 2026
  - https://doi.org/10.1145/3817601

Factory 연결:

Human Gate의 위치만 아니라 **interaction pattern**도 결과 quality에 영향을 줄 수 있다.

---

# 8. Responsibility는 아직 Human 중심이다

AIware 2026 accountability 연구는 9개 provider의 14 policy document를 분석했다.

주요 결과:

- output rights는 user에게 주는 경우가 많음
- correctness / safety / legal compliance 책임은 user에게 남기는 경향
- indemnification / data governance / liability structure는 provider별 차이

출처:

- Accountable Agents in Software Engineering
  - https://arxiv.org/abs/2605.04532
  - https://doi.org/10.1145/3805760.3814889

Factory 연결:

> Technical autonomy가 커져도 organizational/legal responsibility가 자동으로 Agent에게 이동하는 것은 아니다.

---

# 9. Trustworthy Change / Responsibility Topology

2026년 9월 이론 논문은 Agent 시대의 Software Engineering을 다음 개념으로 설명한다.

### Trustworthy Change

Intent부터:

- delegated execution
- verification
- integration
- acceptance
- operation

까지 이동하는 engineering object.

### Human-Agent Cell

Agent execution은 candidate/evidence를 만들지만 final residual-risk acceptance authority는 자동으로 갖지 않는다.

출처:

- Software Engineering in the Agent Era: From Trustworthy Change to Human-Agent Software Organizations
  - https://arxiv.org/abs/2609.04630

주의:

이 논문은 theory construction이며 저자도 empirical validity가 아직 open이라고 명시한다.

책에서 "검증된 사실"보다 유용한 conceptual model로 사용한다.

---

# 10. Human Agent Role Matrix 후보

```text
                Human      Agent      System/Policy
---------------------------------------------------
Intent            A/R        C
Requirement       A/R        R/C
Plan              A/C        R
Implementation     C          R
Verification       C          R         R
Acceptance         A          C
Merge/Deploy       A/R        C         Gate
Recovery           C          R         R
```

A = Accountable
R = Responsible
C = Consulted

이 표는 연구용 초안이며 task risk에 따라 달라져야 한다.

---

# 11. Factory에서 Human은 "Exception Handler"만은 아니다

지나치게 단순한 미래상:

```text
Agent does everything
Human handles exceptions
```

실제 연구는 사람의 지속 역할을 더 넓게 보여준다.

- intent
- semantic commitment
- quality norm
- organization rule
- acceptance
- residual risk
- social coordination

---

# 12. Human Attention은 Capacity Constraint

Agent execution은 elastic하게 늘릴 수 있다.

하지만:

- review
- architecture decision
- risk acceptance
- product intent

은 동일하게 확장되지 않는다.

Factory scheduler는 worker capacity만 아니라 human attention capacity도 고려해야 한다.

---

# 13. Factory UX 연구가 필요하다

향후 연구 질문:

- 언제 interrupt할 것인가
- 무엇을 evidence로 보여줄 것인가
- confidence를 어떻게 전달할 것인가
- 사람에게 얼마나 자주 질문할 것인가
- takeover가 쉬운가
- suspended Task를 어떻게 이해할 것인가

Factory dashboard/TUI도 단순 monitoring UI가 아니라 collaboration surface가 된다.

---

# 핵심 후보 메시지

> Agent에게 실행권을 주는 것과 최종 승인권을 주는 것은 다른 문제다.

> AI Software Factory의 Human-in-the-loop는 "중간마다 허락받기"가 아니라 intent, verification, acceptance, responsibility를 적절히 배치하는 governance design 문제다.

> 실제 Software Engineering에서 Agent 품질은 correctness뿐 아니라 alignment, verifiability, steerability, collaboration으로 평가해야 한다.
