# Phase 7 Full Line Review

기준일: 2026-09-28

대상:

- `chapters/01..24/draft.md`
- `chapters/epilogue/draft.md`

## 최종 판정

**PASS**

24개 본장과 Epilogue에 대해 다음 Review를 완료했다.

- 구조 중복 제거
- 주장 강도 조정
- 연구 조건/한계 표기
- Vendor 사례와 일반 원칙 분리
- Preprint 범위 명시
- 책 자체 synthesis와 외부 표준 분리
- 장간 책임 경계 조정
- 최신성이 중요한 2026 자료 재검증

---

# 1. Review에서 강화한 주장

다음은 서로 다른 산업 사례와 연구에서 반복되어 본문의 핵심 주장으로 유지한다.

1. Model Capability와 Factory Capability는 다르다.
2. Long-running Work의 authoritative state는 Agent Session 밖에 있어야 한다.
3. Worker/Compute와 Task State를 분리하면 retry/reassignment 설계가 쉬워진다.
4. Agent self-report와 completion authority를 분리해야 한다.
5. Test PASS와 User Intent satisfaction은 동일하지 않다.
6. Mandatory Rule은 Prompt만이 아니라 Policy/IAM/Hook/CI 등에서 강제해야 한다.
7. Multi-Agent 효과는 Agent 수보다 Task independence와 coordination cost에 좌우된다.
8. Coding throughput 증가는 Review/CI/Integration 병목을 만들 수 있다.
9. Agent execution authority와 acceptance/merge authority는 분리할 수 있다.
10. Recovery와 observability는 production Agent system의 핵심 capability다.

---

# 2. 책 자체의 Synthesis로 표시한 개념

다음은 업계 표준처럼 쓰지 않는다.

- AI Software Factory의 일곱 핵심 설계 속성
- Evidence Contract
- Failure Fingerprint
- Cost per Accepted Change
- Human Attention per Accepted Change
- First-pass Acceptance Rate를 Factory 후보 Metric으로 사용하는 방식
- M0~M5 Factory Maturity taxonomy
- Reference Factory Acceptance Suite
- Reliability baseline → Recovery + Observability → Scale → Autonomy adoption heuristic

본문에서 처음 사용할 때 책의 제안/후보/taxonomy임을 표시한다.

---

# 3. 범위를 제한한 연구/수치

## Microsoft 2025 Developer RCT

- 4,867 developers
- three field experiments
- completed task +26.08%
- coding-assistant era

2026 asynchronous Factory 일반 수치로 확장하지 않는다.

## METR 2025 OSS RCT

- 16 experienced OSS developers
- 246 tasks
- early-2025 tools
- 19% slower

다른 developer population/model era에 일반화하지 않는다.

## Runtime-Structured Task Decomposition

- two SWE workloads
- 10 runs each

“decomposition 자체보다 failure semantics가 중요할 수 있다”는 반례로만 사용한다.

## AIware 2026 Deterministic vs LLM Orchestration

- structured COBOL modernization workload

모든 coding task에서 deterministic workflow가 우월하다고 해석하지 않는다.

## Microsoft Building to the Test

- 2026 preprint
- two production coding agents
- 18 controlled runs

visible validation과 original intent가 어긋날 수 있다는 사례로 사용한다.

## METR Maintainer Review

- 4 maintainers
- 3 repositories
- 95 issue scope
- single-shot patch review

test pass와 maintainer acceptance의 차이만 사용한다.

## Microsoft AgentLens

- 2,614 trajectories
- analyzed subset 1,815 trajectories / 47 tasks
- 10.7% Lucky Pass in subset

일반 coding-agent pass의 10.7%가 lucky pass라는 식으로 표현하지 않는다.

## Wink

- 2026 preprint
- 10,000+ real-world trajectories
- production-traffic taxonomy
- vendor/research environment

약 30% / 90% 수치는 해당 환경 범위로 제한한다.

## Anthropic Multi-Agent

- controlled multi-agent simulations
- 12-hour software-project scenario 등

실제 enterprise team throughput 수치로 일반화하지 않는다.

## Microsoft Agentic Coding in the Wild

- sampled GitHub Copilot traces from June 2026
- 3.2M users
- 13M sessions
- 761M LLM calls
- 95T tokens
- preprint

agent-native workload 특성을 보여주는 한 production-scale trace로 사용한다.

---

# 4. 현재 상태를 명시한 자료

- NIST Software/AI Agent Identity: 2026-02 Initial Public Draft concept paper, 확정 표준 아님
- GitHub Stacked Pull Requests: 2026-07 public preview 기준
- Google Jules Suggested/Scheduled Tasks: 2025-12 공개 상태 기준
- Google Agent Executor: 2026-05 공개
- Backstage AI Catalog: 현재 docs 기준
- Factory.ai Signals: company implementation, generic proof 아님
- Anthropic self-authored Skills: 2025 글에서 future direction으로 언급된 수준

출간 직전 다시 확인한다.

---

# 5. 구조 중복 조정

- 1장 Metric 상세 → 19장으로 축소
- 3장 Agent-ready Platform 상세 → 21장으로 이동
- 11장 Recovery Ladder 상세 → 14장으로 이동
- 13장 Evidence 최소 필드 반복 제거
- 22장 구축 `Phase` → `Step`으로 변경해 Project Phase / M0~M5와 충돌 제거
- 22장/24장 adoption shorthand 통일
- 24장 self-improvement 자체와 self-modification authority를 분리

---

# 6. Phase 8에서 할 일

Review 단계에서 Architecture와 Claim Boundary는 안정화됐다.

Manuscript 단계에서는 다음에 집중한다.

1. 전체 본문 연결
2. 용어 일괄 통일
3. 제목/소제목 호흡 조정
4. Reference 형식 통일
5. Text Diagram을 출판용 Figure 후보로 정리
6. Case Study Box 위치 선정
7. Preface/Introduction 필요 여부 판단
8. 전체 분량과 장별 균형 조정

Phase 7 결과:

**READY FOR MANUSCRIPT**
