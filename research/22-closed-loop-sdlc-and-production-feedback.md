# Closed-loop SDLC and Production Feedback

기준일: 2026-09-28

Software Factory가 단순 implementation pipeline을 넘어가면 production에서 발생한 signal이 다시 planning으로 돌아오는 closed loop가 중요해진다.

```text
Plan
→ Develop
→ Deliver
→ Operate
→ Observe
→ Learn
→ New Work
→ Plan
```

---

# 1. NIST Continuous Feedback

NIST DevSecOps reference model에서 Continuous Feedback은 별도 핵심 dimension이다.

후기 단계의:

- defect
- vulnerability
- operation event
- policy deviation
- external threat

이 Plan 단계의 requirement/task를 다시 만든다.

출처:

- https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html

---

# 2. Plan은 한 번만 하지 않는다

NIST는 Plan phase 요구사항이 downstream feedback을 통해 계속 refine된다고 설명한다.

즉:

```text
Requirement v1
→ Delivery
→ Evidence
→ Requirement v2
```

AI Software Factory에서도 planning artifact를 immutable contract 하나로 보면 안 된다.

---

# 3. AI가 Feedback을 Backlog로 변환

NIST Functional Scenario H-7.2:

AI component가:

- historical incidents 분석
- improvement theme 추출
- actionable backlog item 생성

하는 시나리오를 정의한다.

출처:

- https://pages.nist.gov/nccoe-devsecops/functional-demonstration-scenarios.html

이것은 Work Selection Autonomy의 현실적인 초기 형태다.

---

# 4. Signal Sources

Factory input은 사람의 prompt만이 아니다.

Production signal 후보:

- error rate
- incident
- Sentry
- security vulnerability
- performance regression
- customer support
- failed deployment
- flaky test
- dependency advisory
- cost anomaly

---

# 5. Signal → Task 변환

직접 자동 실행 전에 중간 단계가 필요하다.

```text
Signal
→ Diagnose
→ Correlate
→ Proposed Work Item
→ Risk/Priority
→ Approval/Policy
→ Task
```

모든 alert를 coding agent에 바로 연결하면 noise가 work explosion으로 바뀐다.

---

# 6. Alert != Task

Alert:

> CPU high.

Task:

> image-processing service memory leak 재현 및 수정. Acceptance: load test X에서 RSS < threshold.

중간에:

- diagnosis
- scope
- acceptance

가 필요하다.

---

# 7. Production Context

Agent가 issue를 수정하려면 source code만으로 부족할 수 있다.

필요:

- logs
- metrics
- traces
- release revision
- feature flag
- deployment history
- config

OpenAI Harness Engineering이 application observability를 Agent-readable하게 만든 이유와 연결된다.

---

# 8. Reproduction First

Production bug workflow 후보:

```text
Incident
→ Reproduction
→ Failing Test
→ Fix
→ Test Pass
→ Deploy
→ Production Signal Recovery
```

가장 강한 evidence는 문제를 재현한 executable case일 수 있다.

---

# 9. Feedback을 테스트로 고정

반복 가능한 failure:

```text
Production Failure
→ Regression Test
→ Permanent Verification Asset
```

Factory가 작업할수록 test suite/eval suite가 축적된다.

---

# 10. Factory Learning

같은 유형의 실패가 반복될 경우:

- missing test
- missing skill
- bad template
- unclear policy
- weak observability

로 분류한다.

결과:

```text
Task Fix
+
Factory Fix
```

둘을 만들 수 있다.

---

# 11. WorkOS Dogfooding과 연결

WorkOS Horizon은 자기 codebase를 작업하면서 발견되는 friction을 factory improvement로 되돌리는 형태를 설명한다.

Closed loop에는 두 종류가 있다.

### Product Loop

Production feedback → product change

### Factory Loop

Factory execution feedback → factory capability improvement

---

# 12. Autonomous Remediation

낮은 위험에서는:

```text
Known Failure
→ Known Fix Pattern
→ Automated Verification
→ Auto Remediation
```

가능.

예:

- dependency lock regeneration
- formatting
- docs drift
- known config mismatch

고위험 production incident를 같은 방식으로 다루면 안 된다.

---

# 13. Risk-based Loop Closure

### Level 1

Signal → Human Task

### Level 2

Signal → Agent diagnosis → Human Task approval

### Level 3

Signal → Agent patch → Human merge

### Level 4

Signal → Agent patch → auto verify → policy merge

### Level 5

Signal → autonomous remediation/deploy

Task별로 다르게 적용한다.

---

# 14. Operation에서 Plan으로 돌아가는 연결

Software Factory가 implementation-only라면:

```text
Issue → PR
```

Closed-loop Factory:

```text
Operate
→ Signal
→ Plan
→ Task
→ Change
→ Deploy
→ Verify Production
```

이 차이는 책의 broad definition 근거가 된다.

---

# 15. Deployment Verification

CI pass로 끝내지 않고 production/staging observation까지 Task completion에 포함할 수 있다.

예:

- error rate
- latency
- health
- business KPI

단 false correlation을 피하기 위해 acceptance window/policy가 필요하다.

---

# 16. Rollback도 Task Outcome

Task 상태 후보:

- Delivered
- VerifiedInProduction
- RolledBack
- Degraded
- NeedsFollowup

Merge/DONE을 동일시하지 않는다.

---

# 17. Closed-loop의 위험

자동 feedback loop는 잘못 설계하면 oscillation을 만든다.

예:

```text
Agent adjusts config
→ metric moves
→ Agent reverses
→ metric moves
→ repeated churn
```

필요:

- cooldown
- change budget
- causal confidence
- human escalation
- rollback

---

# 18. Noise Amplification

모든 telemetry anomaly를 backlog로 만들면:

```text
Observability Noise
→ Backlog Noise
→ Agent Work Noise
```

따라서 triage/evaluation이 필요하다.

---

# 19. Feedback Provenance

새 Task가 왜 만들어졌는지 추적한다.

```text
Task T100
origin:
- incident INC-12
- trace ...
- alert ...
```

이렇게 해야 이후 Agent가 원래 evidence를 다시 확인할 수 있다.

---

# 20. Core Closed-loop Model

```text
Business / User Intent
        ↓
Plan
        ↓
Task
        ↓
Build / Change
        ↓
Verify
        ↓
Release / Deploy
        ↓
Operate
        ↓
Signals / Evidence
        ↓
Triage / Learn
        └──────────→ Plan
```

Agent는 이 loop의 여러 단계에 들어갈 수 있지만 loop 자체가 Agent와 동일한 것은 아니다.

---

# 핵심 후보 메시지

> AI Software Factory의 최종 형태를 Issue-to-PR 자동화로만 보면 범위가 너무 좁다.

> Production Feedback을 새로운 Requirement와 Task로 변환하는 loop가 연결될 때 Factory는 지속적인 생산 시스템에 가까워진다.

> 자율성이 높아질수록 Signal을 곧바로 Action으로 연결하지 말고 diagnosis, risk, acceptance를 중간에 두는 것이 중요하다.
