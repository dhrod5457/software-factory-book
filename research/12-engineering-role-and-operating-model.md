# Engineering Role and Operating Model

기준일: 2026-09-28

AI Software Factory의 변화는 기술 아키텍처만이 아니다.

개발자가 직접 수행하던 작업 중 일부가 Agent/Factory로 이동하면서 **사람의 병목과 역할도 이동**한다.

## 1. "Humans steer. Agents execute."

OpenAI Harness Engineering의 대표적인 표현이다.

그 실험에서 인간 엔지니어의 업무는 직접 code typing보다:

- environment design
- capability gap 발견
- specification
- feedback loop
- architecture
- guardrails

쪽으로 이동했다.

출처:

- https://openai.com/index/harness-engineering/

## 2. Human Attention이 Scarce Resource

Symphony가 해결하려 한 문제는 model speed가 아니었다.

여러 agent session을 사람이 직접:

- 시작
- 기억
- 확인
- steer
- retry

하면서 context switching이 병목이 되었다.

OpenAI는 대략 3~5개 interactive session 수준부터 관리 부담이 커졌다고 설명한다.

따라서 Orchestrator는 compute scheduler만이 아니라 **human attention scheduler**이기도 하다.

출처:

- https://openai.com/index/open-source-codex-orchestration-symphony/

## 3. Implementation보다 Specification/Review가 병목으로 이동

Factory.ai의 architecture framing:

agents가 execution을 자동화하면 bottleneck이:

```text
Writing Change
→ Defining Intent
→ Reviewing / Policy
```

로 이동한다.

출처:

- https://factory.ai/articles/what-is-a-software-factory-architecture

## 4. DORA의 경고

AI가 local coding productivity를 높여도:

- testing
- review
- security
- deployment

이 느리면 전체 성과가 개선되지 않는다.

즉 individual developer productivity를 최적화하는 것과 organizational delivery를 최적화하는 것은 다르다.

출처:

- https://dora.dev/research/2025/dora-report/
- https://dora.dev/capabilities/platform-engineering/

## 5. Engineer의 새 업무 후보

### Intent Engineering

무엇을 만들지 명확히 정의.

### Spec Engineering

Acceptance와 constraint를 실행 가능하게 만들기.

### Harness Engineering

Agent가 성공 가능한 environment/tool/context 구성.

### Eval Engineering

Agent/factory capability regression 측정.

### Verification Engineering

Task outcome을 자동 판단 가능한 형태로 만들기.

### Platform Engineering

재현 가능한 execution path 제공.

### Policy Engineering

어떤 action을 어디까지 자동 허용할지 설계.

### Exception Handling

Factory가 불확실한 Task를 사람에게 올렸을 때 판단.

## 6. Coding Skill이 사라지는가

현재 자료는 그렇게 단정하기 어렵다.

오히려 다음 능력이 필요하다.

- architecture understanding
- debugging
- test design
- security
- system boundary
- performance
- production judgment

Agent 결과를 판단하고 Factory 자체를 개선하려면 deep technical knowledge가 여전히 필요하다.

DORA는 AI가 expertise 형성의 productive struggle를 줄일 수 있다는 tension도 제기한다.

출처:

- https://dora.dev/insights/balancing-ai-tensions/

## 7. Junior/Senior 역할 변화 가설

검증이 더 필요한 가설:

### Junior

기존 반복 구현 업무 일부가 자동화될 수 있음.

대신:

- acceptance 작성
- eval/test
- agent run analysis
- narrow task ownership

이 training surface가 될 수 있음.

### Senior

- task decomposition
- architecture
- risk
- policy
- harness
- multi-agent workflow
- technical review

비중 증가 가능.

하지만 실제 labor data 없이 강하게 단정하지 않는다.

## 8. PM / Product 역할과 Factory

WorkOS Horizon의 PM agent는 requirement를 issue로 분해한다.

Spec Kit은 idea assessment와 specification을 implementation과 분리한다.

따라서 Software Factory가 engineering team 내부만의 시스템에서 점점:

```text
Product Intent
→ Requirement
→ Task
→ Engineering
```

전반을 연결할 가능성이 있다.

그러나 product priority 결정까지 autonomous하게 넘기는 것은 별도 governance 문제다.

## 9. Reviewer Bottleneck

Agent가 10배 많은 PR을 만들면 사람 reviewer가 10배 빨라지지 않는다.

해결 방향:

- smaller changes
- stronger automated verification
- evidence
- agent pre-review
- risk-based review
- batching/queue policy

OpenAI Harness Engineering은 agent-to-agent review 비중을 늘린 사례를 공개했다.

## 10. Ownership

Agent가 작업했다고 code ownership이 사라지는 것은 아니다.

필요한 질문:

- 누가 requirement owner인가
- 누가 component owner인가
- 누가 agent result를 accept할 수 있는가
- 누가 production incident 책임을 갖는가
- 누가 policy를 변경할 수 있는가

Factory는 responsibility를 machine에 "넘긴다"기보다 execution authority를 위임한다.

## 11. Team Topology 변화

가능한 운영 모델:

### Individual + Agents

한 개발자가 여러 asynchronous agent 사용.

### Team Factory

공용 queue + workers + policies.

### Platform Factory

중앙 platform team이 factory infrastructure 제공, product teams가 task/spec/policy 사용.

### Domain Factory

각 domain마다 dedicated tools/context/evals.

어떤 형태가 유리한지는 조직 규모와 coupling에 따라 달라진다.

## 12. On-call / Incident

Agent가 incident investigation까지 수행할 수 있지만 production action은 별도 authority가 필요하다.

가능한 흐름:

```text
Alert
→ Agent investigation
→ evidence
→ mitigation proposal
→ approval
→ controlled action
```

고위험 환경에서는 완전 자동 action보다 이 구조가 현실적일 수 있다.

## 13. New Management Problem

사람이 Agent를 직접 일일이 관리하면 manager-to-agent ratio 문제가 생긴다.

Symphony식 전환:

```text
Human manages sessions
→ System manages agents
→ Human manages objectives/policy
```

이것이 Software Factory의 조직적 의미 중 하나다.

## 14. 핵심 후보 메시지

> AI Software Factory는 개발자를 없애는 자동화가 아니라 개발자의 scarce attention을 구현에서 intent, architecture, verification, exception으로 재배치하는 시스템이다.

> Agent가 많아질수록 사람에게 더 많은 terminal window를 주는 방식은 확장되지 않는다. Agent management 자체를 software로 만들어야 한다.

> 조직 생산성은 coding speed가 아니라 전체 delivery system이 새로운 throughput을 흡수할 수 있는지에 달려 있다.
