# Part IV Draft Review

기준일: 2026-09-28

대상:

- `chapters/13/draft.md`
- `chapters/14/draft.md`
- `chapters/15/draft.md`
- `chapters/16/draft.md`

## 판정

**PASS WITH MINOR FOLLOW-UP**

Part IV의 역할은 명확하다.

~~~text
13장
Verification 결과를 Evidence Package로 표준화

14장
Failure를 분류하고 적절한 Recovery 선택

15장
Crash / Wait / Duplicate Side Effect를 Durable Execution으로 처리

16장
Autonomy를 Security / Identity / Governance 경계 안에 둠
~~~

Part V로 넘어가도 된다.

---

## 13장 역할

핵심:

- Result Contract
- Evidence minimum fields
- Behavioral Evidence
- Evidence vs Provenance
- Machine-readable Manifest
- Review Startup Cost

후속 line edit:

- result.json 예시는 final manuscript에서 schema box로 정리
- Provenance 상세는 16장과 중복되지 않게 현재 수준 유지

상태:

**READY FOR PART V**

---

## 14장 역할

핵심:

- Failure Taxonomy
- Recovery Ladder
- Retry Budget
- Failure Fingerprint
- Restart / Resume / Reassign
- Carryover
- Human Escalation

좋은 점:

- 모든 Failure를 Agent 실패로 보지 않음
- Infra Failure와 Code Failure를 분리
- Human Escalation을 정상 상태로 봄

후속 line edit:

- Wink 수치/표현은 final citation pass에서 원문 재검증
- 15장의 durable runtime internals를 선행하지 않도록 현재 수준 유지

상태:

**READY FOR PART V**

---

## 15장 역할

핵심:

- Memory != Execution State
- Event History
- Checkpoint
- Idempotency
- Replay-safe Tool
- Async Human Wait
- Crash Test

좋은 점:

- Context 저장과 execution recovery를 명확히 분리
- Git checkpoint와 orchestration state를 같이 봄
- Different-worker resume를 강한 continuity 기준으로 제시

후속 line edit:

- Temporal / Durable Task / Agent Executor는 책임 분리 사례로만 유지
- distributed systems 상세 구현은 제외 유지

상태:

**READY FOR PART V**

---

## 16장 역할

핵심:

- Blast Radius
- Prompt-only Security 비판
- Scoped Credential
- Agent Identity
- Untrusted Context
- Risk-based Human Gate
- Audit / Provenance

좋은 점:

- Security를 Model Trust 문제가 아니라 capability boundary 문제로 설명
- Execution Authority와 Acceptance Authority 분리
- Chain-of-Thought를 audit requirement로 두지 않음

후속 line edit:

- NIST/GitHub/Microsoft의 최신 정책·제품 세부는 출간 전 재검증
- Enterprise IAM 표준 세부는 scope 밖 유지

상태:

**READY FOR PART V**

---

# Part IV 전체 결론

Part IV의 한 줄 요약:

> Agent 결과를 신뢰하려면 결과 Evidence, 실패 복구, 실행 지속성, 권한 경계를 모두 시스템 차원에서 관리해야 한다.

다음 Part V에서는 안전한 단일 Worker를 여러 개로 늘렸을 때 생기는:

- Parallelism
- Review / CI / Integration Bottleneck
- Observability / Metrics

를 다룬다.
