# WorkOS: PR Factory에서 Product Engineering Factory로

기준일: 2026-09-28

## Source

- Ryan Cooke, WorkOS, *No, That's Not a Software Factory* conference talk transcript
- 사용자 제공 transcript: `No, That's Not a Software Factory - Ryan Cooke, WorkOS (HvboD89DyQ8).txt`
- 보조 공개 자료: WorkOS, *The self-driving codebase: Building Horizon at WorkOS*

이 문서는 발표 내용을 그대로 재현하지 않고, 책의 설계 원칙에 필요한 주장과 사례를 요약한다.

---

# 1. 핵심 문제 제기

발표가 비판하는 전형적인 Software Factory 이미지는 다음과 같다.

```text
Sandbox
→ Coding Agent
→ Prompt
→ Pull Request
→ Merge
```

WorkOS는 초기 구현에서 이 구조만으로는 개발자가 로컬 Coding Agent를 직접 사용하는 것과 조직 전체 outcome 측면에서 뚜렷하게 다른 결과를 만들지 못했다고 설명한다.

따라서 Factory의 자동화 대상을 코드 생성 자체에서 **Product Engineering Process**로 확장한다.

핵심 후보 문장:

> Agent가 PR을 만드는 것은 Factory의 실행 셀일 수 있지만 Software Factory 전체는 아니다.

> AI Software Factory의 자동화 단위는 코드 생성이 아니라 Software Engineering Process다.

---

# 2. Output Metric과 Outcome Metric을 구분한다

발표는 다음과 같은 수치를 Factory 성공 지표로만 사용할 때의 한계를 지적한다.

- AI가 만든 Pull Request 비율
- Pull Request 개수
- AI가 생성한 코드량
- Production에 들어간 AI 코드량

이들은 대부분 output 또는 activity를 측정한다.

반면 WorkOS가 보고자 하는 것은 다음과 같은 조직 outcome이다.

- Feature delivery가 빨라졌는가
- 복잡한 기능의 Cycle Time이 줄었는가
- Customer Value가 더 빨리 전달되는가
- Defect Rate가 악화되지 않는가
- Recovery Time이 나빠지지 않는가

책의 Metric 계층 후보:

```text
Activity
- agent runs
- tokens
- tool calls

Output
- commits
- LOC
- pull requests

Flow
- cycle time
- review time
- human blocking time
- first-pass acceptance

Outcome
- feature delivery
- accepted change
- escaped defect
- revert
- MTTR
- customer impact
```

핵심 원칙:

> Factory가 많이 만들었는지보다 검증된 가치가 더 빨리 전달됐는지를 측정한다.

---

# 3. TARS와 Horizon: Product Process와 Execution Infrastructure를 분리한다

발표에서 WorkOS는 두 계층을 설명한다.

### TARS

사용자가 Coding Agent와 상호작용하고 Product Engineering workflow를 연결하는 계층.

연결 예:

- Slack
- Linear
- GitHub
- Webhook

역할:

- 프로젝트 진행 상태 추적
- Product artifact 생성
- Task dependency 관찰
- 다음 단계 시작
- Human feedback 반영

### Horizon

Execution infrastructure orchestration 계층.

역할:

- Sandbox
- Workload execution
- Agent runtime
- MCP gateway 앞의 infrastructure orchestration

일반화 가능한 경계:

```text
Product / Work Orchestration
≠
Execution Infrastructure
```

Factory는 둘을 연결하지만 둘을 하나의 컴포넌트로 만들 필요는 없다.

---

# 4. 기존 Product Engineering Ritual을 Factory에 Encode한다

WorkOS는 Hilltop이라는 PRD 성격의 문서를 사용한다.

이 artifact에는 다음이 들어간다.

- Project purpose
- Customer need
- Competitive context
- Early design
- Major milestone

Agent는 짧은 brief에서 첫 초안을 만들고, 사람이 scope와 방향을 보정한 뒤 구현 Task로 분해한다.

```text
Brief
→ Agent-generated first draft
→ Human review / scope correction
→ Approved product artifact
→ Task decomposition
→ Execution
```

여기서 중요한 점은 Agent에게 Product Intent의 최종 권한을 넘기는 것이 아니다.

Agent는 blank-page cost를 낮추고 context 수집과 초안을 맡는다.
Human은 Intent, Scope, Trade-off, Acceptance Authority를 유지할 수 있다.

---

# 5. Continuous Planning Loop

발표에서 특히 중요한 패턴은 Task dependency 자동 실행보다 그 다음이다.

Task가 끝나면 Agent가 현재 project plan을 다시 보고 빠진 Task가 생겼는지 재평가한다.

구현 중 새 정보가 생기기 때문이다.

```text
Plan
→ Task
→ Execution
→ New Knowledge
→ Plan Re-evaluation
→ Task Graph Update
```

이를 Production Feedback Loop와 구분할 필요가 있다.

### Execution Learning Loop

Task 실행에서 얻은 지식이 현재 Plan을 수정한다.

### Product Feedback Loop

Production/User signal이 새로운 Requirement를 만든다.

### Factory Improvement Loop

Agent 실행 friction이 Skill/Tool/Context/Policy 개선을 만든다.

이 세 Loop를 분리하면 Closed-loop Factory를 더 정확히 설명할 수 있다.

---

# 6. MCP Gateway를 Context Engine으로 사용한다

WorkOS는 내부 MCP gateway를 단순 Tool proxy보다 넓게 사용한다.

연결 대상 예:

- Snowflake
- Product utilization data
- Customer conversation data
- Linear
- Internal systems

중요한 부분은 API 노출만이 아니다.

Agent에게 다음도 함께 제공한다.

- 어떤 데이터가 어디에 있는가
- Table이 어떤 의미를 갖는가
- 어떤 질문에 어떤 source를 사용해야 하는가
- 조직이 Tool과 Data를 어떻게 구성했는가

이를 다음처럼 구분할 수 있다.

```text
Raw Tool Gateway
→ API 노출

Semantic Tool Gateway
→ Tool + schema + usage guidance

Organizational Context Gateway
→ Tool + data semantics + conventions + discovery guidance
```

핵심 원칙:

> MCP를 연결하는 것과 Context Engineering을 끝내는 것은 같은 일이 아니다.

---

# 7. Factory State는 특정 Coding Agent와 분리할 수 있다

발표에서는 같은 Ticket과 Documentation을 WorkOS 내부 Coding Agent뿐 아니라 다른 Agent에도 제공할 수 있다고 설명한다.

일반화하면:

```text
Factory
- Task
- Context
- Policy
- Verification
- Evidence
       ↓
Agent Runtime A / B / C
```

따라서 Durable Work와 Organization Context를 특정 Agent Vendor의 session state 안에 가두지 않는 것이 중요하다.

---

# 8. Self-improvement는 Session 관찰에서 시작할 수 있다

WorkOS가 설명한 다음 방향에는 자체 sandbox infrastructure와 memory layer가 포함된다.

또한 Agent session을 관찰해 다음을 찾는 방향을 제시한다.

- Agent가 반복해서 틀리는 지점
- 새 Skill이 필요한 지점
- 오래되어 무효가 된 Skill
- Context/Tool friction
- Infrastructure bottleneck

```text
Factory Execution
→ Friction Signal
→ Improvement Candidate
→ Skill / Tool / Context / Infrastructure Change
→ Evaluation
→ Better Factory
```

주의:

발표 후반의 일부는 현재 완성된 capability가 아니라 향후 구축 방향이다.
본문에서는 구현 완료 사실로 일반화하지 않는다.

---

# 9. Authorization은 남아 있는 핵심 난제다

발표자는 마지막에 Agent authorization 문제를 아직 충분히 해결하지 못한 영역으로 언급한다.

이는 MCP나 Tool 연결이 늘어날수록 더 중요하다.

```text
Human Principal
→ Delegation
→ Agent Identity
→ Authorization
→ MCP Gateway
→ Internal Systems
```

질문:

- Agent는 누구의 권한으로 실행되는가
- Task마다 어떤 Capability를 위임받았는가
- Read와 Write 권한을 어떻게 분리하는가
- Approval은 어느 action에 필요한가
- Side effect를 누구에게 귀속하는가
- Audit와 Revocation은 가능한가

이 사례는 Agent-ready Context Layer와 Authorization Layer를 동시에 설계해야 함을 보여준다.

---

# 10. 책에 반영할 설계 원칙

1. **PR 생성기를 Software Factory 전체로 부르지 않는다.**
2. **Factory의 자동화 범위를 Coding에서 Product Engineering Process로 확장한다.**
3. **Output Metric과 Outcome Metric을 분리한다.**
4. **Planning artifact를 실행 중 다시 평가할 수 있게 한다.**
5. **MCP를 Tool 연결뿐 아니라 Semantic Context Layer로 본다.**
6. **Durable Factory State를 Agent Vendor와 분리한다.**
7. **Self-improvement는 실제 session friction에서 시작한다.**
8. **Authorization을 완성되지 않은 핵심 운영 문제로 다룬다.**

---

# 11. Chapter 반영 지도

| Chapter | 반영 내용 |
|---|---|
| 2장 | Sandbox + Agent + PR만으로는 Factory 전체가 아니라는 경계 |
| 4장 | Product brief → Agent draft → Human review → Task decomposition |
| 10장 | MCP Context Engine / Semantic Tool Gateway |
| 16장 | Agent authorization을 아직 어려운 운영 문제로 제시 |
| 19장 | Output Metric vs Outcome Metric |
| 20장 | Continuous Planning Loop / Task completion 후 plan re-evaluation |
| 24장 | Session friction → Skill/Tool/Context improvement |

---

# 12. Claim Boundary

- WorkOS의 architecture와 workflow를 업계 표준으로 표현하지 않는다.
- WorkOS 내부 효과를 보편적인 productivity improvement 수치로 일반화하지 않는다.
- 발표에서 향후 계획으로 설명한 memory/self-improvement capability를 현재 production capability처럼 쓰지 않는다.
- Authorization 미해결 언급은 WorkOS 자체 상태를 보여주는 사례이지 모든 Factory가 동일 수준이라는 뜻은 아니다.
