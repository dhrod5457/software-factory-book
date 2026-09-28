# Autonomy Levels and Self-Improvement

기준일: 2026-09-28

AI Software Factory의 자율성은 YES/NO가 아니다.

다음 질문을 분리해야 한다.

- 누가 Task를 발견하는가?
- 누가 Task를 선택하는가?
- 누가 계획하는가?
- 누가 구현하는가?
- 누가 검증하는가?
- 누가 merge/deploy를 승인하는가?
- 누가 Factory 자체를 개선하는가?

## 1. 임시 Autonomy Matrix

| 단계 | Work Selection | Planning | Execution | Verification | Merge |
|---|---|---|---|---|---|
| A0 | Human | Human | Human | Human | Human |
| A1 | Human | Human/Agent | Agent assisted | Human | Human |
| A2 | Human | Agent | Agent | Auto + Human | Human |
| A3 | Human/System | Agent | Agent | Auto | Human |
| A4 | System | Agent | Agent | Auto + Agent evaluator | Policy/Human by risk |
| A5 | System | Agent | Agent | Auto | Auto by policy |

이 표는 업계 표준이 아니라 책의 연구용 taxonomy다.

## 2. 공개 사례 배치

### Stripe Minions

대략:

- human task
- unattended execution
- CI
- human PR review

→ A2/A3 영역.

출처:

- https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents

### WorkOS Horizon

- human requirement
- PM agent decomposition
- human issue review
- event-driven autonomous implementation
- automated validation
- human merge approval

→ planning까지 일부 agent화된 A3에 가까움.

출처:

- https://workos.com/blog/project-horizon

### OpenAI Symphony

- issue tracker open task
- supervisor assigns continuous agent
- autonomous routine implementation
- humans review result

→ Task execution orchestration이 더 자동화된 A3.

출처:

- https://openai.com/index/open-source-codex-orchestration-symphony/

### StrongDM

- humans define intent/scenario/constraints
- agents implement/validate/iterate
- human code review 제거 방향

→ A4/A5에 가까운 강한 autonomy model.

출처:

- https://www.strongdm.com/blog/the-strongdm-software-factory-building-software-with-ai

## 3. Work Selection Autonomy

실행 자율성과 선택 자율성은 다르다.

낮은 위험:

- dependency update
- docs drift
- lint
- missing tests
- flaky test investigation

높은 위험:

- feature priority
- architecture redesign
- breaking API
- product behavior change

Google Jules는 Suggested Tasks / Scheduled Tasks로 proactive work direction을 보여준다.

하지만 proactive discovery와 auto-merge는 별개다.

출처:

- https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/

## 4. Self-Improvement에는 두 종류가 있다

### Product Self-Improvement

Factory가 개발 대상 software를 개선한다.

### Factory Self-Improvement

Factory가 자기 harness를 개선한다.

예:

- missing tool 추가
- skill 수정
- flaky test 제거
- environment image 개선
- task template 수정
- routing policy 변경
- evaluator 강화

둘을 구분한다.

## 5. OpenAI Harness Engineering의 Compounding Loop

OpenAI 사례에서 실패할 때 인간이 직접 patch하는 대신:

> agent가 다음에는 성공할 수 있도록 어떤 capability가 부족한가?

를 묻는 방식으로 개선했다.

결과적으로:

- docs
- tests
- guardrails
- app legibility
- Chrome DevTools
- smoke test
- skills

등 harness가 축적된다.

이것은 Factory learning의 한 형태다.

출처:

- https://openai.com/index/harness-engineering/

## 6. WorkOS Horizon Dogfooding

Horizon이 실제 codebase를 작업하면서 발견한 friction:

- missing script
- flaky test
- unclear convention
- slow sandbox
- poor MCP tool

을 다시 Horizon platform 개선으로 되돌리는 loop를 설명한다.

```text
Factory Work
→ Friction
→ Factory Improvement Task
→ Better Factory
→ More Work
```

출처:

- https://workos.com/blog/project-horizon

## 7. Factory.ai Signals

Factory.ai는 Signals라는 closed-loop self-improvement 구조를 공개했다.

개념:

- session 분석
- friction/delight signal
- threshold
- Droid가 개선 issue/fix 수행

중요:

Factory.ai 자체 주장/구현 사례다.

"self-improving"이라는 표현을 일반적 사실로 확대하지 않는다.

출처:

- https://factory.ai/news/factory-signals

## 8. Skills를 Agent가 다시 작성하는 방향

Anthropic Agent Skills 글은 장기적으로 agent가:

- skill create
- skill edit
- skill evaluate

를 스스로 할 가능성을 명시한다.

Factory 관점:

반복 실패를 procedural knowledge로 codify하는 loop.

```text
Failure
→ New Procedure
→ Skill
→ Eval
→ Reuse
```

출처:

- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

## 9. Self-Improvement의 위험

자동 개선은 쉽게 reward hacking으로 이어질 수 있다.

예:

- test를 약하게 수정
- evaluator를 통과하도록 behavior 왜곡
- metric 자체를 최적화
- safety rule 우회
- benchmark leakage 활용

따라서 Factory self-modification은 일반 product change보다 더 강한 gate가 필요할 수 있다.

## 10. Meta-change 분리

Factory 구성 변경:

- system instruction
- skill
- tool
- policy
- evaluator
- routing
- sandbox image

는 별도 change class로 관리할 수 있다.

요구:

- evaluation
- shadow run
- canary
- rollback
- human approval

## 11. Shadow Mode

새 policy/agent/harness를 바로 production decision에 쓰지 않고:

```text
Production Factory
→ real task

Candidate Factory
→ same/sampled task
→ no authoritative action

Compare
→ quality / cost / safety
```

후 승격.

이 패턴은 self-improvement의 안전 장치 후보다.

## 12. Autonomy Boundary는 Task별로 달라진다

한 조직 안에서도:

### Docs

A5 가능할 수 있음.

### Unit Tests

A4 가능.

### Feature Code

A3.

### DB Migration

A2.

### Production Incident

Action별 A1~A4 혼합.

따라서 조직 전체에 단일 autonomy level을 붙이는 것은 부정확하다.

## 13. Escalation이 있어야 Autonomy가 가능하다

Autonomous system은 막히지 않는 시스템이 아니다.

잘 설계된 autonomous system은:

- uncertainty
- policy conflict
- repeated failure
- unknown risk

에서 정확히 멈출 수 있어야 한다.

```text
Autonomy
= Execute Independently
+ Know When To Escalate
```

## 14. Human Role의 이동

자료에서 반복되는 방향:

기존:

- 직접 구현
- command 실행
- test 실행

이동:

- intent
- specification
- acceptance
- architecture
- policy
- exception
- review
- factory design

OpenAI는 "Humans steer. Agents execute."라고 요약한다.

하지만 이 역할 이동의 정도는 team/task마다 다르다.

## 15. 핵심 후보 메시지

> AI Software Factory의 목표는 사람을 제거하는 것이 아니라 사람이 개입해야 하는 지점을 더 가치 있는 결정으로 이동시키는 것이다.

> 높은 자율성은 Task 선택, 실행, 검증, merge 권한을 한 번에 넘기는 것이 아니라 각각의 경계를 독립적으로 설계하는 문제다.

> Self-improvement는 Factory의 강력한 특성이 될 수 있지만, Factory가 자기 평가 기준까지 자유롭게 바꾸게 두면 검증 자체가 무너질 수 있다.
