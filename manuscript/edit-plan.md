# Manuscript Edit Plan

기준일: 2026-09-28

## 목표

Review가 완료된 25개 Draft를 한 권의 연속된 원고로 다듬는다.

현재 `manuscript/book.md`는 구조적 조립이 완료된 working copy다.

---

## Pass 1. Structural Flow

확인:

- Part 시작 문장
- Chapter 마지막 질문과 다음 Chapter 첫 문장 연결
- 같은 개념 반복
- 같은 예제 반복
- 같은 Diagram 반복

특히 중복 후보:

- Human Attention
- Accepted Change
- Review bottleneck
- Worker loss
- Reliability / Recovery / Observability / Autonomy
- CI/CD / Platform boundary

---

## Pass 2. Terminology

통일 후보:

- 리뷰 / Review
- 검증 / Verification
- 통합 / Integration
- 실행환경 / Runtime / Environment
- 증거 / Evidence
- 작업 / Work / Task
- 승인 / Acceptance / Approval

핵심 기술 용어는 영문 유지 가능:

- Agent
- Task
- Worker
- Factory
- Harness
- Sandbox
- Control Plane
- Evidence Contract
- Durable Execution

---

## Pass 3. Figures

Text Diagram 중 정식 Figure 후보를 추린다.

우선 후보:

1. AI Software Factory 전체 Loop
2. Model → Agent → Factory Capability
3. Control Plane / Execution Plane
4. Task / Attempt / Worker 관계
5. Verification Pyramid
6. Evidence / Provenance
7. Recovery Ladder
8. Parallel Fan-out / Fan-in
9. Factory Throughput Bottleneck
10. Maturity × Autonomy Matrix

---

## Pass 4. Case Study Boxes

일반 원칙과 분리해서 Box 처리할 후보:

- OpenAI Symphony
- WorkOS Horizon
- Anthropic Managed Agents
- GitHub Copilot Code Review regression
- Microsoft AgentLens
- METR maintainer review
- Anthropic multi-agent coordination
- Runmesh continuity gap

---

## Pass 5. References

Chapter별 참고자료를 최종적으로 통일한다.

후보 형식:

```text
기관/저자, 제목, 연도.
URL
```

출간 직전 다시 확인:

- preview / GA
- product name
- protocol version
- model name
- preprint publication status
- vendor operational metrics

---

## Pass 6. Front Matter

검토할 항목:

- Preface
- 이 책이 다루는 것 / 다루지 않는 것
- 독자
- 용어 사용 원칙
- 책 읽는 순서

필요한 것만 추가한다.

---

## 완료 기준

- 24개 장과 Epilogue가 한 권의 연속된 흐름으로 읽힌다.
- 동일 핵심 주장을 여러 장에서 반복 설명하지 않는다.
- 책 자체 개념과 업계 표준이 구분된다.
- Vendor / Preprint 수치의 범위가 본문에서 드러난다.
- Figure와 Case Study 위치가 결정된다.
- Reference 형식이 통일된다.
- publication-time source recheck 목록이 남아 있다.
