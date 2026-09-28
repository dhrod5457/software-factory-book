# Part IV Phase 7 Review

기준일: 2026-09-28

대상:
- chapters/13/draft.md
- chapters/14/draft.md
- chapters/15/draft.md
- chapters/16/draft.md

판정: **PASS**

## 주요 수정

### 13장
- Evidence Contract를 업계 표준이 아니라 이 책의 설계 패턴으로 명시
- Demos over Diffs를 실무적 접근으로 한정하고 source/security review 대체가 아님을 유지
- 13.2와 13.9의 최소 필드 반복을 제거
- 핵심을 Result Revision ↔ Verification ↔ Artifact 연결 일관성으로 수렴

### 14장
- Failure Fingerprint를 책의 설계 패턴으로 명시
- Wink를 2026 arXiv preprint로 표시
- 10,000+ real-world trajectories, 약 30% taxonomy occurrence, single-intervention 대상의 90% 해결이라는 연구 범위를 명시
- 해당 수치를 일반적인 coding-agent 실패율로 해석하지 않도록 제한

### 15장
- arbitrary external side effect에 대한 exactly-once를 runtime이 단독 보장할 수 없다는 표현으로 정밀화
- Human Approval을 workflow 상 asynchronous event/signal로 표현
- 책의 Durable Task와 Microsoft Durable Task technology를 다시 분리
- Google Agent Executor의 2026-05 event log/snapshot 기반 resume 사례를 현재 자료로 반영

### 16장
- NIST Agent Identity 자료를 2026-02 Initial Public Draft concept paper / ongoing project로 명시
- Task-scoped identity를 NIST 표준이 아닌 이 책의 architecture proposal로 제한
- Microsoft Claude Code GitHub Action / Semantic Kernel 사례를 특정 취약 버전·구성의 수정된 vulnerability로 contextualize
- “LLM은 security boundary가 아니다”는 tool authority 설계 원칙으로 수렴

### 중복 정리
- 11장의 Recovery Ladder 상세를 14장으로 이동하고 11장에는 Control Plane이 recovery policy를 소유한다는 연결만 남김

## 현재성 검증

확인:
- Wink, arXiv 2602.17037, 2026-02
- Microsoft Durable Task for AI Agents, updated 2026-05-05
- Google Agent Executor, 2026-05-20
- NIST Software/AI Agent Identity and Authorization, Initial Public Draft 2026-02-05
- Microsoft Security Claude Code GitHub Action case, 2026-06-05
- Microsoft Security Semantic Kernel RCE cases, 2026-05-07

## 남은 후속

- Evidence Manifest의 실제 JSON Schema는 Reference Factory 구현 시 별도 관리
- Identity 표준은 출간 직전 NIST 프로젝트 상태 재확인
- Security vendor vulnerability는 출간 시점 patched/current context 재확인
