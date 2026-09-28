# Publication Source Recheck — 2026-09-28

출판 직전 변경 가능성이 높은 항목을 2026-09-28 기준으로 다시 확인한 기록이다.

## 판정

**PASS WITH CURRENT-STATE NOTES**

책의 핵심 논리를 바꿔야 할 변경은 발견되지 않았다.

---

## 1. GitHub Stacked Pull Requests

현재 상태:

**Public Preview 유지**

확인:

- 2026-07-30 GitHub Changelog의 public preview 상태가 현재도 유효하다.
- 2026-09 GitHub의 Pull Requests UI 업데이트에서도 stack indicator가 preview UI에 포함되어 있다.

원고 조치:

- 18장의 “2026년 7월 public preview” 표현 유지.
- GA라고 쓰지 않는다.

---

## 2. NIST Software and AI Agent Identity and Authorization

현재 상태:

- 2026-02 concept paper는 여전히 **Draft**로 표시된다.
- NIST AI Agent Standards Initiative 페이지도 해당 문서를 Draft Concept Paper로 표시한다.
- 2026-08 NIST 후속 글에서는 이 작업이 NCCoE의 Software and AI Agent Identity and Authorization project로 이어지고 있음을 확인할 수 있다.

원고 조치:

- “확정 표준”이라고 표현하지 않는다.
- “Draft concept paper + ongoing NCCoE project”로 설명한다.
- Task-scoped Agent Identity는 NIST 규격이 아니라 책의 architecture proposal이라는 기존 문구 유지.

---

## 3. Model Context Protocol

현재 최신 정식 Specification:

**2026-07-28**

현재 official specification page가 2026-07-28을 latest version으로 표시한다.

확인된 주요 성질:

- stateless protocol core
- request-level protocol version
- Multi Round-Trip Requests
- extensions framework
- authorization updates

MCP Tasks는 별도 extension으로 존재한다.

원고 조치:

- 2026-07-28 이후 버전이 나온 것으로 쓰지 않는다.
- MCP Task와 Factory의 Durable Task를 동일시하지 않는다.

---

## 4. Building to the Test

현재 상태:

**ArXiv Preprint 유지**

- June 2026
- arXiv 2606.28430
- Microsoft Research page도 Preprint로 표시

원고 조치:

- 12장의 “2026년 preprint” 표현 유지.
- 18 controlled runs와 prevalence open question이라는 범위 유지.

---

## 5. AgentLens

현재 상태:

- Microsoft Research publication page에 2026년 5월 ArXiv publication으로 등록
- 별도 peer-reviewed venue 확인은 하지 못함

원고 조치:

- “연구” 또는 “ArXiv 연구” 수준으로 표현.
- peer-reviewed paper라고 쓰지 않는다.

---

## 6. Wink

현재 상태:

**ArXiv paper**

- arXiv 2602.17037
- production traffic 기반 taxonomy
- 10,000+ trajectories evaluation

원고 조치:

- 약 30% misbehavior occurrence와 90% single-intervention resolution은 해당 deployment/research environment 범위로 유지.
- 일반적인 coding-agent failure rate로 표현하지 않는다.

---

## 7. Runtime-Structured Task Decomposition

현재 상태:

**ArXiv paper**

- arXiv 2605.15425
- two software-engineering workloads
- three configurations
- 10 runs each

원고 조치:

- 제한된 workload의 연구라는 기존 caveat 유지.
- decomposition 일반 법칙으로 확장하지 않는다.

---

## 8. Google Jules Proactive Work

현재 상태:

- Suggested Tasks는 현재 docs에서도 **experimental feature**
- repository별 Proactivity opt-in
- Suggested Tasks는 review 대상
- Scheduled Tasks는 2026-01부터 Edit/Pause/Resume 지원

원고 조치:

- Event-driven Work Intake와 autonomous acceptance를 구분하는 사례로 유지.
- Suggested Tasks가 완전 autonomous remediation이라고 쓰지 않는다.

---

## 9. Google Agent Executor

현재 상태:

- 2026-05-20 공개
- open-source runtime standard
- event log + snapshot
- outage / HITL interruption 이후 resume 지원

원고 조치:

- Durable Execution 사례로 유지.
- Agent framework 전체와 동일시하지 않는다.

---

## 10. Backstage AI Catalog

현재 docs:

- `AiResource`로 Skill / Governance Rule 모델링
- MCP server를 catalog API entity로 모델링
- ownership / lifecycle / relationship tracking
- MCP Actions Backend 제공

원고 조치:

- 21장의 Agent-ready Catalog 사례 유지.
- “모든 조직이 이렇게 해야 한다”는 normative claim으로 쓰지 않는다.

---

# Publication Gate Result

다음 current-state 항목은 2026-09-28 기준 검증 완료:

- GitHub Stacked PR preview status
- NIST Agent Identity project status
- MCP latest specification
- Building to the Test publication status
- AgentLens publication type
- Wink publication status
- Runtime-Structured Task Decomposition status
- Jules proactive feature status
- Google Agent Executor status
- Backstage AI catalog status

최종 PDF/출판 생성 시점이 크게 뒤로 밀리면 이 문서의 항목만 다시 검사한다.
