# Part III Draft Review

기준일: 2026-09-28

대상:

- `chapters/07/draft.md`
- `chapters/08/draft.md`
- `chapters/09/draft.md`
- `chapters/10/draft.md`
- `chapters/11/draft.md`
- `chapters/12/draft.md`

## 판정

**PASS WITH MINOR FOLLOW-UP**

Part III의 역할 분담은 다음처럼 명확하다.

~~~text
7장
누가 Work State를 책임지는가
→ Control Plane / Execution Plane

8장
Agent는 어디서 실행되는가
→ Worker / Sandbox / Workspace

9장
Model 주변의 실행 Interface는 무엇인가
→ Harness

10장
Agent가 필요한 정보를 어떻게 찾는가
→ Context / Legibility

11장
어떤 Decision을 System과 Agent가 각각 소유하는가
→ Controlled Autonomy

12장
Agent 결과를 누가 무엇으로 판정하는가
→ Verification
~~~

Part IV로 넘어가도 된다.

---

## 7장 역할

핵심:

- Control Plane / Execution Plane 책임 분리
- Task completion responsibility
- Issue Tracker / Task Store / Worker Runtime 경계
- Human Wait와 Worker release

후속 line edit 후보:

- 15장 Durable Execution과의 중복을 피하기 위해 crash/replay internals는 현재 수준 유지
- Control Plane 상태 그림을 manuscript 단계에서 추가

상태:

**READY FOR PART IV**

---

## 8장 역할

핵심:

- Workspace Isolation
- Prepared Environment
- Fresh State / Cache
- Ephemeral / Persistent Worker
- Worker Profile

좋은 점:

- Persistent Worker를 정답으로 만들지 않음
- Worker warm state와 authoritative Task State를 구분
- stale browser state 반례 포함

후속 line edit 후보:

- VM/container 비교는 표로 정리 가능
- Security 상세는 16장으로 넘긴 현재 경계 유지

상태:

**READY FOR PART IV**

---

## 9장 역할

핵심:

- Harness 정의
- Agent-Computer Interface
- Instruction / Skill / Tool / MCP
- Tool Output / Result Gateway
- Harness Regression

좋은 점:

- Tool 수 증가를 capability 증가와 동일시하지 않음
- Mandatory Rule을 Policy/Hook으로 분리
- Harness 자체를 version/eval 대상 Software로 봄

후속 line edit 후보:

- MCP 설명은 13장 protocol research가 아니라 현재처럼 capability surface 수준에서 제한
- Prepared Harness와 8장 Worker Profile의 표기만 manuscript 단계에서 통일

상태:

**READY FOR PART IV**

---

## 10장 역할

핵심:

- Context Window != Storage
- Repository Legibility
- AGENTS.md as entry point
- Catalog / Runtime Context
- Progressive Disclosure

좋은 점:

- More Context = Better Agent를 명시적으로 거부
- Repository / Catalog / Runtime을 서로 다른 source로 구분
- Context와 Mandatory Policy를 분리

후속 line edit 후보:

- Context File empirical study의 구체 수치는 final citation review에서 보강
- 21장 Developer Platform과 겹치는 Catalog 상세는 현재 수준 유지

상태:

**READY FOR PART IV**

---

## 11장 역할

핵심:

- Deterministic / Agent-controlled / Hybrid
- Rule / Heuristic / Judgment
- System-owned State
- Agent-owned Judgment
- Recovery Scope

좋은 점:

- 책의 핵심 철학을 구체적인 control placement 문제로 설명
- “더 Agentic = 더 좋음”을 전제로 하지 않음
- LLM transcript 안에 workflow state를 숨기는 anti-pattern 포함

후속 line edit 후보:

- AIware 2026 deterministic orchestration 연구 수치는 final source review에서 원문 재검증
- Maturity/Autonomy taxonomy는 24장으로 유지

상태:

**READY FOR PART IV**

---

## 12장 역할

핵심:

- Completion Claim / Completion Authority
- Verification Pyramid
- Executable Acceptance
- Building to the Test
- Reward Hacking
- Lucky Pass
- Verification Policy

좋은 점:

- Test를 약화시키지 않고 Test의 한계를 설명
- Agent self-report와 Factory DONE을 분리
- Task Risk에 따라 Verification Profile을 다르게 설정

후속 line edit 후보:

- Independent Evaluator가 같은 Model/Context일 때 correlated error가 있다는 내용을 17장과 중복되지 않게 유지
- Evidence Manifest 상세는 13장으로 이동한 현재 경계 유지

상태:

**READY FOR PART IV**

---

# Part III 전체 결론

Part III의 한 줄 요약:

> Durable Task를 안전하게 실행하려면 Work State, Compute, Agent Interface, Context, Decision Authority, Completion Authority를 서로 분리해야 한다.

다음 Part IV에서는 이 실행 결과를 실제 조직에서 신뢰할 수 있게 만드는:

- Evidence
- Failure / Recovery
- Durable Execution
- Security / Identity / Governance

로 이동한다.
