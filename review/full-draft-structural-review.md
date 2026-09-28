# Full Draft Structural Review

기준일: 2026-09-28

대상:

- `chapters/01..24/draft.md`
- `chapters/epilogue/draft.md`

## 결과

**25 / 25 Draft 파일 존재 확인**

구조:

~~~text
Part I
Why / Definition / Boundary

Part II
Requirement / Durable Task / Decomposition

Part III
Control Plane / Worker / Harness / Context / Autonomy / Verification

Part IV
Evidence / Recovery / Durable Execution / Security

Part V
Parallelism / Review-CI-Integration / Observability

Part VI
Closed-loop / Developer Platform

Part VII
Minimum Viable Factory / Reference Factory / Maturity

Epilogue
Software Engineering → Software Production
~~~

## 전체 논리 판정

**STRUCTURE PASS**

책의 중심 논리가 처음부터 끝까지 유지된다.

~~~text
Intent
→ Structured Work
→ Durable Task
→ Controlled Execution
→ Independent Verification
→ Evidence
→ Recovery
→ Governance
→ Delivery Flow
→ Feedback
~~~

## Review Phase에서 우선 확인할 항목

### 1. 중복 제거

특히 반복 가능성이 높은 주제:

- Human Attention
- Accepted Change
- Review Bottleneck
- Worker Loss
- Reliability → Autonomy
- CI/CD / Platform boundary

장별 역할은 유지하되 같은 예와 문장을 반복하지 않게 편집한다.

### 2. 용어 통일

후보:

- Review → 리뷰
- Verification → 검증
- Integration → 통합
- Evidence는 핵심 용어로 영문 유지 여부 결정
- Durable Task / Control Plane / Worker / Harness는 핵심 영문 용어 유지

### 3. Source Validation

출간 전 반드시 재검증:

- 2026 Vendor 제품/기능
- 2026 논문/preprint publication status
- 회사 자체 생산성 수치
- 최신 Benchmark 상태
- Protocol version

### 4. Claim Strength

강한 주장:

- durable external state
- independent verification
- recovery
- task independence before parallelism
- model capability != factory capability

조심할 주장:

- Maturity taxonomy
- Accepted Change metric
- future role changes
- self-improvement
- autonomous merge boundary

### 5. 도식 추가

Plan에 정의했지만 Draft에는 text diagram만 있는 항목을 manuscript 단계에서 시각화한다.

### 6. 실제 사례 Box

제품 이름이 본문 논리를 지배하지 않도록:

- 원칙
- 사례
- 반례

순서를 유지한다.

## Draft Phase 완료 조건

충족:

- 24개 본장 Draft 작성
- Epilogue Draft 작성
- Part별 Review 작성
- Writing Style Guide 존재
- Scope / TOC / Plan과 구조 일치

따라서 다음 단계:

**Phase 7 - Review**
