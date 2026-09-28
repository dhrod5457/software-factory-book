# Part V Draft Review

기준일: 2026-09-28

대상:

- `chapters/17/draft.md`
- `chapters/18/draft.md`
- `chapters/19/draft.md`

## 판정

**PASS WITH MINOR FOLLOW-UP**

Part V의 역할 분담:

~~~text
17장
어떤 Work가 실제로 병렬화 가능한가

18장
병렬 결과가 만드는 Review / CI / Integration 병목을 어떻게 관리할 것인가

19장
전체 Flow를 무엇으로 관찰하고 측정할 것인가
~~~

Part VI로 넘어가도 된다.

---

## 17장 역할

핵심:

- Task independence
- Fan-out / Fan-in
- Ownership / Conflict
- Correlated Error
- Parent/Subagent vs Task Worker
- Concurrency Budget

좋은 점:

- Multi-Agent를 architecture 자체가 아니라 scheduling pattern으로 설명
- Same-model Committee를 독립 의견으로 보지 않음
- Shared Resource Stampede 포함

후속 line edit:

- Anthropic multi-agent 연구의 구체 관찰 수치는 final citation pass에서 재검증
- Multi-Agent framework 비교는 scope 밖 유지

상태:

**READY FOR PART VI**

---

## 18장 역할

핵심:

- Bottleneck Migration
- Reviewability
- Giant PR
- Verification Queue
- CI Capacity
- WIP Limit
- Integration Acceptance

좋은 점:

- Correct but unreviewable을 품질 문제로 봄
- Worker Utilization보다 Flow를 우선
- AI Reviewer를 보조 capacity로 다룸

후속 line edit:

- 1장의 throughput 가상 예와 숫자 중복은 final manuscript에서 조정
- Lean/Kanban 일반론으로 확장하지 않음

상태:

**READY FOR PART VI**

---

## 19장 역할

핵심:

- Task / Attempt / Worker / Human Observability
- Task Timeline
- Factory vs Agent Metric
- Human Attention
- Cost per Accepted Change
- Benchmark vs Production
- Production Failure → Eval

좋은 점:

- raw Chain-of-Thought를 observability 핵심으로 두지 않음
- Agent runtime speed와 end-to-end flow를 분리
- Minimum Viable Dashboard 제시

후속 line edit:

- Microsoft production-scale workload 수치 등 최신 값은 출간 직전 재검증
- 기업 KPI 일반론으로 확대하지 않음

상태:

**READY FOR PART VI**

---

# Part V 전체 결론

> Parallelism은 Worker 수의 문제가 아니라 independent work와 downstream capacity의 문제이며, 실제 개선은 전체 Flow를 관찰할 때만 판단할 수 있다.

다음 Part VI에서는 Observability에서 들어오는 신호를 다시 Work로 변환하고, 기존 Developer Platform을 Factory의 capability layer로 사용하는 구조를 다룬다.
