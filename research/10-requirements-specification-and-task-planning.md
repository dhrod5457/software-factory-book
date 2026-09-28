# Requirements, Specification, and Task Planning

기준일: 2026-09-28

AI Software Factory가 단순 "코딩 자동화"를 넘어서는 지점은 **무엇을 만들지 정의하고, 실행 가능한 Task로 변환하는 단계**다.

이 문서는 Requirement → Specification → Design → Task → Implementation 흐름을 조사한다.

## 1. 왜 Prompt만으로 부족한가

한 번의 prompt는 빠르지만 다음 문제가 있다.

- 요구사항 누락
- hidden assumption
- acceptance ambiguity
- 설계 결정이 conversation 안에만 남음
- session 변경 시 context 소실
- 구현 완료 여부를 machine-check하기 어려움

따라서 큰 Task일수록 **durable planning artifact**가 중요해진다.

## 2. GitHub Spec Kit

GitHub Spec Kit은 2026년 기준 다음 core flow를 제공한다.

```text
Specify
→ Plan
→ Tasks
→ Implement
→ Converge
```

확장 quality gate:

```text
Constitution
→ Specify
→ Clarify
→ Plan
→ Checklist
→ Tasks
→ Analyze
→ Implement
→ Converge
```

중요한 철학:

- intent를 implementation보다 먼저 고정
- spec/plan/tasks를 durable artifact로 유지
- 특정 coding agent에 종속되지 않음
- workflow 자체를 reusable process로 취급

출처:

- https://github.com/github/spec-kit
- https://github.com/github/spec-kit/blob/main/docs/index.md
- https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md

## 3. Durable Artifact

Spec Kit history는 다음 theme을 명시한다.

- Intent comes before implementation
- Artifacts should be durable
- Process should be agent-independent
- Method should adapt to work

Factory 관점에서 중요:

```text
Conversation
→ ephemeral

spec.md
plan.md
tasks.md
→ durable
```

이 구조는 session continuity와도 연결된다.

출처:

- https://github.com/github/spec-kit/blob/main/docs/history.md

## 4. Kiro Specs

Kiro는 feature work를 기본적으로:

```text
Requirements
→ Design
→ Tasks
→ Implementation
```

으로 구조화한다.

Artifact:

- requirements.md
- design.md
- tasks.md

Requirements에는 user story / acceptance criteria를 넣고, design에는 architecture와 implementation approach, tasks에는 discrete execution unit을 만든다.

출처:

- https://kiro.dev/docs/specs/
- https://kiro.dev/docs/getting-started/first-project/

## 5. Requirements-first와 Design-first

실제 brownfield에서는 항상 요구사항부터 시작하지 않는다.

Kiro는 두 workflow를 분리한다.

### Requirements-first

```text
Requirements
→ Design
→ Tasks
```

적합:

- product behavior가 중심
- architecture 자유도 높음

### Design-first

```text
Design
→ Requirements
→ Tasks
```

적합:

- 기존 architecture
- migration
- performance constraint
- compliance
- technical feasibility

Factory가 하나의 planning process만 강요하면 실제 업무를 제대로 반영하지 못할 수 있다.

출처:

- https://kiro.dev/docs/specs/feature-specs/

## 6. Quick Spec와 Review Gate

모든 Task에 동일한 governance를 적용할 필요는 없다.

Kiro Quick Spec:

- clarifying question
- requirements/design/tasks 자동 생성
- phase별 approval 생략

대신 complex/high-risk task는 standard spec의 explicit review gate를 권장한다.

중요한 패턴:

> Planning depth도 Task risk에 따라 조절한다.

출처:

- https://kiro.dev/docs/specs/quick-plan/

## 7. Requirement Analysis

Kiro는 requirements에서 다음을 검사하는 별도 단계를 제공한다.

- logical inconsistency
- ambiguity
- conflicting constraint
- unstated assumption
- missing edge case

이것은 AI Software Factory에서 중요한 역할 분리를 보여준다.

```text
Requirement Generator
≠ Requirement Evaluator
```

특히 code를 만들기 전에 requirement defect를 잡는 것이 더 싸다.

출처:

- https://kiro.dev/docs/specs/analyze-requirements/
- https://kiro.dev/blog/deep-spec-analysis/

## 8. Requirement에서 Test Property 생성

Kiro correctness 기능은 specification에서 testable property를 추출하고 property-based test를 생성하는 방향을 보여준다.

즉:

```text
Requirement
→ Formal/Testable Property
→ Generated Test
→ Implementation
→ Verification
```

Software Factory에서 가장 강력한 연결은 **Intent가 Verification까지 이어지는 것**이다.

출처:

- https://kiro.dev/docs/specs/correctness/
- https://kiro.dev/blog/property-based-testing/

## 9. Specification Traceability

이상적인 Factory에서는 다음 연결이 추적 가능해야 한다.

```text
Requirement R1
→ Design D3
→ Task T7
→ Commit C
→ Test V4
→ Artifact A
```

이렇게 되면:

- 누락 확인
- 변경 영향 분석
- 요구사항 drift 감지
- verification completeness

가 가능해진다.

## 10. Task Decomposition

Task 분해가 필요한 이유:

- context 축소
- parallelism
- independent verification
- retry scope 제한
- ownership
- review

하지만 지나치게 작은 Task:

- startup overhead
- repeated context
- orchestration cost

지나치게 큰 Task:

- failure blast radius
- context pollution
- review 어려움
- recovery 어려움

따라서 적절한 Task size는 실제 측정 대상이다.

## 11. Task Graph

Task list보다 graph가 현실에 가깝다.

```text
Requirement
  ↓
Design
  ↓
T1 ─→ T3 ─→ T5
T2 ───────→ T5
T4 ─→ T6
```

Task dependency가 명확해야 safe parallelism이 가능하다.

## 12. Task Selection

AI Software Factory가 고도화되면 backlog에서 다음 Task를 자동 선택할 수 있다.

하지만 selection에는 policy가 필요하다.

후보 입력:

- priority
- dependency
- risk
- owner
- environment availability
- worker capability
- cost
- branch conflict
- due date

```text
Ready Task Set
→ Policy
→ Scheduler
→ Worker Assignment
```

## 13. Idea Assessment도 Factory 앞단에 들어갈 수 있다

GitHub Spec Kit은 구현 workflow와 별개로 idea assessment를 제공한다.

Outcome:

- go
- clarify
- stop

중요:

> 아이디어를 분석했다고 자동으로 implementation을 시작하지 않는다.

이는 Product Decision과 Execution 권한을 분리하는 좋은 패턴이다.

출처:

- https://github.com/github/spec-kit/blob/main/docs/index.md

## 14. Requirement Ownership

Agent가 specification을 작성할 수 있어도 product intent의 authoritative owner가 누구인지는 별도다.

가능한 모델:

### Human authoritative

Agent는 명세 draft.

### Human + Agent collaborative

Agent가 ambiguity/question을 제기하고 사람 결정 반영.

### Policy-constrained autonomous

low-risk maintenance에서 Agent가 requirement/task 생성까지.

Factory에서 "누가 문서를 썼는가"보다 **누가 승인 권한을 갖는가**가 중요하다.

## 15. Drift

긴 프로젝트에서 발생:

```text
Requirements change
but
Tasks / Tests / Code stay old
```

따라서 spec sync가 필요하다.

Kiro는 requirements/design 수정 이후 tasks sync workflow를 제공한다.

Spec Kit은 artifact consistency / converge step을 둔다.

Factory는 spec/code/test drift를 지속적으로 탐지하는 구조로 확장할 수 있다.

## 16. Factory 앞단 Reference Flow 후보

```text
Signal / Human Intent
      ↓
Idea Assessment
      ↓
Requirement Draft
      ↓
Clarification
      ↓
Acceptance Criteria
      ↓
Architecture / Design
      ↓
Task Graph
      ↓
Risk / Dependency / Routing
      ↓
Execution Queue
```

## 17. 핵심 후보 메시지

> AI Software Factory가 coding agent farm과 다른 이유는 코드 작성 이전의 intent와 작업 구조도 durable artifact로 관리하기 때문이다.

> 요구사항 자동 생성보다 중요한 것은 요구사항과 verification 사이의 traceability다.

> Task를 자동 실행하기 전에 어떤 Task가 실행 가능한 상태인지 정의하는 Ready Contract가 필요하다.
