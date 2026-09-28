# Simplest Software Factory: GitHub-native Implementation Case Study

기준일: 2026-09-28

## Source

- *I Built the Simplest Software Factory* (video id: `AsvzMlLyQ38`)
- user-provided transcript
- 약 27분 분량
- 영상 말미에 Upstash sponsorship이 명시되어 있음

## Source Quality

**C급 구현 사례 / tutorial source**

이 자료는 논문, 독립 실증 연구, 표준 문서가 아니다.

따라서 다음 용도로 사용한다.

- Software Factory 개념을 작은 구현으로 설명
- Minimum Viable Factory의 concrete example
- GitHub-native control surface 사례
- worker sandbox / prepared snapshot 사례
- deterministic dispatch와 optional LLM routing 비교
- staged activation / dry-run 사례

다음 주장에는 직접 사용하지 않는다.

- 특정 vendor architecture가 일반적으로 우월하다는 주장
- VPS가 모든 Factory의 최적 Worker 형태라는 주장
- Worker 10개가 적절한 scale이라는 주장
- 특정 Model이 특정 작업 유형에 보편적으로 우월하다는 주장
- 제품의 plan limit, model name, provider capability를 장기 원칙으로 일반화

출판용 인용으로 사용할 경우 원본 영상 URL과 게시일을 publication-time에 다시 확인한다.

---

## 1. 구현의 최소 Loop

영상의 핵심 구현은 다음과 같다.

~~~text
GitHub Issue
→ ready label
→ dispatcher
→ available coding agent
→ implementation / test
→ pull request
→ human review
→ merge
~~~

Agent는 여러 provider를 섞어 사용할 수 있지만, 중요한 것은 Model 조합이 아니다.

이 사례에서 Factory는 Coding Agent 자체가 아니라 다음을 담당하는 wrapper / system으로 설명된다.

- signal 수신
- task triage / dispatch
- worker assignment
- execution 상태 표시
- PR 생성
- human review로 handoff

책의 정의와 연결하면 다음과 같다.

~~~text
Coding Agent
= execution worker

Software Factory
= work flow를 관리하는 production system
~~~

이 자료의 가장 중요한 가치는 "Factory는 Agent가 아니다"라는 경계를 작은 구현으로 보여준다는 데 있다.

---

## 2. LLM 없는 Dispatcher

영상에서는 triage 단계에 LLM을 사용해 bug / feature / documentation 등을 분류할 수도 있다고 설명한다.

하지만 실제 tutorial 구현에서는 반드시 LLM을 넣지 않는다.

~~~text
ready task
→ deterministic code
→ available worker assignment
~~~

이 패턴은 책의 Controlled Autonomy 원칙을 구체화한다.

~~~text
Known Rule
→ code / policy

Uncertain Classification
→ optional model

Engineering Diagnosis
→ coding agent
~~~

Software Factory라고 해서 모든 의사결정 단계에 LLM이 필요한 것은 아니다.

오히려 routing rule이 이미 명확하면 deterministic dispatcher가 더 단순하고 관찰하기 쉽다.

관련 장:

- 11장 Controlled Autonomy
- 7장 Control Plane과 Execution Plane

---

## 3. GitHub를 Human-facing Control Surface로 사용

이 구현은 별도 운영 UI보다 GitHub Issue를 중심으로 동작한다.

예시 상태:

~~~text
ready
→ factory running
→ factory review
~~~

Issue comment에는 다음 정보가 남는다.

- 어떤 Worker가 할당되었는가
- 어떤 Pull Request가 생성되었는가

이 방식의 장점은 개발자가 이미 사용하는 Work Surface에서 Factory 상태를 확인할 수 있다는 점이다.

하지만 이 사례를 다음과 같이 일반화하면 안 된다.

~~~text
GitHub label
= authoritative runtime state
~~~

책의 경계는 그대로 유지한다.

~~~text
Issue Tracker
= Work Intent / Human Collaboration / Control Surface

Task Store
= Durable Execution State

Worker Runtime
= Temporary Execution
~~~

UI와 Source of Truth는 같은 제품에 있을 수도 있지만 개념적으로는 분리해서 본다.

관련 장:

- 7장 Control Plane과 Execution Plane
- 19장 Observability와 Metrics

---

## 4. Worker Sandbox와 Resource Isolation

영상에서는 각 coding agent를 별도 Linux VM 형태의 sandbox에서 실행한다.

제시되는 이유는 두 가지다.

### Security

Issue 같은 외부 입력에는 prompt injection이 포함될 수 있다.

Agent가 host machine의 file, secret, shell authority에 직접 접근하지 않게 sandbox boundary를 둔다.

### Resource Isolation

여러 Worker가 동시에 실행될 때 CPU/RAM을 한 machine에서 경쟁하지 않도록 Worker별 compute allocation을 분리한다.

이 구현 자체를 표준으로 보지는 않는다.

책에서는 격리 범위를 다음 축으로 분해한다.

~~~text
filesystem
process
network
credential
port
database
browser profile
compute resource
~~~

VM은 이 중 여러 축을 강하게 분리하는 한 implementation choice다.

관련 장:

- 8장 Worker, Sandbox, Workspace
- 16장 Security, Identity, Governance

---

## 5. Snapshot은 Reusable Environment다

영상 후반에는 Worker마다 반복 설정하지 않고 reusable snapshot을 만든다.

Snapshot에 포함할 수 있는 예:

- coding agent runtime
- agent skills
- browser-driving tool
- MCP server
- AGENTS.md 같은 repository/agent instruction

새 Worker는 이 snapshot에서 생성된다.

책의 Prepared Environment 개념과 연결하면 다음과 같다.

~~~text
Reusable Worker Image / Snapshot
- runtime
- agent runtime
- tools
- browser
- skills
- MCP integration
- static instructions

Fresh per Task
- source checkout / revision
- task input
- scoped credential
- uncommitted work
- test state
- temporary service data
~~~

핵심은 Snapshot에 무엇을 넣는가보다 **Reusable Environment와 Task-specific State를 섞지 않는 것**이다.

관련 장:

- 8장 Worker, Sandbox, Workspace
- 9장 Harness Engineering

---

## 6. Dry Run 후 Side Effect를 연다

이 구현에서 책에 추가할 가치가 가장 높은 부분 중 하나다.

Project repository와 Factory 연결을 만든 뒤 곧바로 coding agent를 실행하지 않는다.

먼저 다음 Integration만 확인한다.

~~~text
Issue created
→ ready label
→ repository event
→ factory receives signal
~~~

이 단계에서는 실제 코드 수정이 일어나지 않는다.

Dry Run이 통과한 뒤에야 real execution을 활성화한다.

일반화하면 다음과 같은 staged activation pattern이다.

~~~text
Signal Integration
→ Observe-only / Dry Run
→ Agent Execution
→ Repository Write
→ Delivery / Merge Permission
~~~

Autonomy를 한 번에 켜지 않고 Side Effect 범위를 단계적으로 넓히는 방식이다.

이 패턴은 다음 원칙과 잘 맞는다.

~~~text
Reliability
→ Observability
→ Recovery
→ Scale
→ Autonomy
~~~

관련 장:

- 22장 Minimum Viable AI Software Factory
- 20장 Event-driven Factory와 Closed-loop SDLC

---

## 7. Multi-repository Hub-and-Spoke Pattern

영상의 Factory는 여러 Project Repository를 중앙 Factory와 연결한다.

각 Project Repo가 Issue/label signal을 보내고, 중앙 Factory가 Worker를 배정한다.

결과 PR은 원래 Project Repository로 돌아간다.

~~~text
Repo A ─┐
Repo B ─┼→ Factory Ingress
Repo C ─┘       ↓
             Dispatcher
                ↓
            Worker Fleet
                ↓
       PR → Original Repo
~~~

이 구조는 다음 경계를 설명하는 데 유용하다.

- Work Source와 Execution Runtime 분리
- Project Repository와 Factory Repository 분리
- 하나의 Control Plane이 여러 Repository를 관리할 수 있음
- 결과는 원래 ownership boundary로 되돌아감

관련 장:

- 23장 실전 Reference Factory 만들기
- 7장 Control Plane과 Execution Plane

---

## 8. Capability를 주지 않는 것도 Control이다

영상에서는 agent가 특정 destructive infrastructure operation을 수행하지 못하는 제약이 있다.

이 제품 제약 자체를 일반 원칙으로 볼 수는 없다.

하지만 설계 관점에서는 다음 교훈으로 사용할 수 있다.

~~~text
Capability not granted
= enforceable boundary
~~~

예:

~~~text
Agent can
- create worker
- execute task
- create PR

Agent cannot
- delete shared snapshot
- destroy protected infrastructure
~~~

Human Gate는 항상 "승인 버튼"으로 구현되는 것이 아니다.

위험한 Capability 자체를 Worker에 주지 않는 것도 더 강한 Control Boundary가 될 수 있다.

관련 장:

- 16장 Security, Identity, Governance
- 11장 Controlled Autonomy

---

## 9. Observability는 기존 Work Surface에 얹을 수 있다

Issue label과 comment는 정교한 telemetry system은 아니다.

하지만 운영자가 다음 질문에 빠르게 답하게 한다.

- 이 Task가 시작됐는가?
- 현재 실행 중인가?
- 어떤 Worker가 맡았는가?
- Review 단계인가?
- 어떤 PR이 결과인가?

~~~text
ready
→ running
→ review
~~~

이 패턴은 Human-facing observability와 system telemetry를 구분하는 데 유용하다.

~~~text
Human-facing state
- issue label
- comment
- PR link

System telemetry
- attempt
- lease
- tool event
- verification
- cost
- failure
~~~

두 Layer는 서로 보완하지만 동일하지 않다.

관련 장:

- 19장 Observability와 Metrics

---

## 10. 책에 반영할 핵심

이 자료는 새로운 장을 만들 정도의 새 이론은 제공하지 않는다.

대신 기존 내용을 다음처럼 구체화한다.

1. Factory는 Coding Agent 자체가 아니다.
2. Triage / Dispatch에 LLM이 필수는 아니다.
3. GitHub 같은 기존 도구를 Human-facing control surface로 사용할 수 있다.
4. Worker Environment는 snapshot으로 재사용하되 Task State는 fresh하게 유지한다.
5. Event Integration은 Dry Run부터 활성화할 수 있다.
6. 여러 Repository를 하나의 Factory가 관리하는 Hub-and-Spoke 구조가 가능하다.
7. Human Gate는 승인뿐 아니라 Capability omission으로도 구현할 수 있다.
8. Observability UI와 authoritative runtime state를 구분해야 한다.

가장 직접적인 본문 반영 대상은 8장, 11장, 22장, 23장이다.
