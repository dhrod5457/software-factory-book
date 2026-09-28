# Verification, Evidence, and Human Gates

기준일: 2026-09-28

AI Software Factory에서 가장 중요한 질문 중 하나:

> Agent가 "완료했다"고 말하는 것과 실제 완료를 어떻게 구분할 것인가?

이 문서는 검증을 Software Factory의 독립적인 production stage가 아니라 **Agent loop의 일부**로 본다.

## 1. Completion Claim은 Evidence가 아니다

낮은 신뢰:

- "수정했습니다"
- "테스트했습니다"
- "문제가 해결됐습니다"

높은 신뢰:

- commit SHA
- changed files
- exact command
- exit code
- test report
- coverage report
- screenshot
- video
- DOM snapshot
- log
- trace
- benchmark
- deployed URL
- acceptance result

Factory의 output은 자연어 보고서가 아니라 evidence bundle이어야 한다.

## 2. Verification Pyramid

```text
Level 0
Agent self-report

Level 1
Static checks
- compile
- lint
- typecheck
- format

Level 2
Deterministic tests
- unit
- integration
- contract

Level 3
Runtime checks
- service boot
- API call
- DB migration
- E2E

Level 4
Behavioral evidence
- browser
- screenshot
- video
- logs
- metrics

Level 5
Independent evaluator
- separate agent
- security agent
- acceptance agent

Level 6
Human acceptance
```

Task의 위험도에 따라 필요한 Level을 정한다.

## 3. Deterministic Grader를 먼저 사용

Anthropic eval guide:

- string checks
- binary tests
- static analysis
- outcome verification

Coding task는 deterministic verification을 사용하기 좋은 영역이다.

가능하면 LLM judge보다 먼저 사용한다.

출처:

- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

## 4. Generator와 Evaluator 분리

Anthropic long-running app harness:

```text
Planner
→ Generator
→ Evaluator
→ Generator
→ Evaluator
```

배경:

self-evaluation이 지나치게 긍정적인 문제가 있을 수 있다.

별도 evaluator가:

- acceptance criteria 확인
- browser로 실제 app 사용
- 부족한 부분을 generator에 전달

중요:

multi-agent 자체가 목적이 아니라 **독립 평가 관점**을 만드는 것이 목적이다.

출처:

- https://www.anthropic.com/engineering/harness-design-long-running-apps

## 5. Browser / Computer Use Verification

Cursor Cloud Agents:

- browser/desktop 조작
- app 실행
- UI flow 수행
- screenshot/video/log artifact
- PR에 evidence 첨부

Factory Droid Control:

- terminal/browser/desktop
- QA flow
- annotated screenshot
- before/after video

OpenAI Harness Engineering:

- worktree별 app
- DOM
- screenshot
- logs
- metrics
- traces

공통점:

> UI/Runtime 작업은 Diff만으로 완료를 판단하지 않는다.

출처:

- https://cursor.com/docs/cloud-agent/capabilities
- https://docs.factory.ai/software-factory/droid-control
- https://openai.com/index/harness-engineering/

## 6. Demos over Diffs

UI/UX Task에 특히 유용한 패턴:

```text
Before Screenshot
→ Change
→ Build
→ E2E
→ After Screenshot
→ Video
→ Diff Review
```

Demo가 code review를 대체한다는 뜻은 아니다.

목적:

- reviewer의 checkout cost 감소
- behavior drift 빠른 확인
- visual regression 확인

## 7. StrongDM - Scenario-based Validation

StrongDM은 사람 code review 없이 behavior/scenario validation 중심의 더 강한 autonomy model을 제시한다.

중점:

- intent
- scenarios
- constraints
- generated implementation
- iterative validation
- convergence

중요한 비교 질문:

> Source review 없이 behavior validation만으로 production confidence를 얻을 수 있는 범위는 어디까지인가?

이를 보편적 정답으로 취급하지 않는다.

출처:

- https://www.strongdm.com/blog/the-strongdm-software-factory-building-software-with-ai

## 8. Human Review를 유지하는 산업 사례

### Stripe Minions

- unattended implementation
- CI-ready PR
- human review

### WorkOS Horizon

- issue planning human review
- autonomous execution
- human PR merge approval

### OpenAI Symphony

- bulk routine implementation automation
- human review 결과

즉, 현재 공개 사례의 다수는 완전 human-free보다 **Human Gate 위치를 뒤로 이동**시키는 형태다.

## 9. Human Gate 후보 위치

```text
Intent Approval
↓
Task Approval
↓
Plan Approval
↓
Dangerous Action Approval
↓
PR Approval
↓
Deploy Approval
↓
Production Change Approval
```

모든 곳에서 승인하면 autonomy가 사라진다.

어디에도 없으면 blast radius가 커진다.

Risk-based gate가 필요하다.

## 10. Risk-based Verification

예:

### Documentation

- lint
- link check
- preview

### Unit Test 추가

- targeted tests
- full regression

### UI 변경

- build
- browser flow
- screenshot
- accessibility

### DB Migration

- migration dry run
- rollback test
- schema diff
- human approval

### Security/Auth

- tests
- static security
- separate security review
- human approval

## 11. Acceptance Criteria를 Machine-readable하게 만든다

Bad:

```text
로그인 페이지 개선
```

Better:

```text
- invalid password → error message
- locked user → HTTP 423
- successful login → /home
- existing login tests remain green
- mobile 390px layout does not overflow
```

Machine-checkable acceptance가 많을수록 automation depth를 높일 수 있다.

## 12. Evidence Manifest

Task 결과에 다음 형식을 검토할 수 있다.

```text
Task
Result
Commit
Changed Files

Verification
- command
- result
- duration

Behavior
- screenshot
- video
- endpoint result

Observability
- log reference
- trace reference

Known Limitations
Remaining Risk
```

## 13. Evals와 Production Verification을 구분

Evals:

Agent/harness 자체가 좋은가?

Production Task Verification:

이번 코드 변경이 맞는가?

둘은 다르다.

```text
Agent Eval
→ Factory capability 개선

Task Verification
→ 특정 delivery correctness
```

## 14. Feedback Loop

실패를 단순 retry하지 않고 classification한다.

예:

- missing context
- wrong task spec
- missing tool
- environment issue
- model limitation
- flaky test
- permission issue
- dependency conflict
- evaluator weakness

그 결과를:

- skill
- docs
- test
- tool
- sandbox image
- task template
- routing policy

개선으로 연결한다.

## 15. 핵심 후보 메시지

> AI Software Factory에서 검증은 작업이 끝난 뒤 붙이는 QA 단계가 아니라 Agent가 일하는 방식 자체의 일부다.

> Human review를 줄이려면 더 강한 모델보다 더 강한 executable acceptance가 먼저 필요하다.

> 높은 autonomy는 낮은 검증을 의미하지 않는다. 오히려 autonomy가 높을수록 자동 검증과 evidence 요구 수준도 높아져야 한다.
