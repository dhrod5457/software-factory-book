# Figure Captions

기준일: 2026-09-28

`manuscript/book.md`의 F01~F21 marker에 대응하는 working caption이다.

## F01. Model → Agent → Factory Capability

Model 성능은 Agent와 Factory 성능의 한 구성요소일 뿐이다. Repository, Tool, Context, 실행환경, 상태 관리, 검증을 포함한 시스템 계층이 실제 Delivery Capability를 결정한다.

## F02. AI Software Factory Reference Loop

Intent가 Requirement와 Durable Task로 변환되고, Control Plane과 Worker를 거쳐 검증·Evidence·Governance·Delivery로 이어진 뒤 운영 Feedback이 다시 다음 Work로 돌아오는 전체 Loop.

## F03. Work Artifact Traceability

Requirement에서 Design, Task, Commit, Verification, Evidence까지 연결하면 “무엇을 왜 바꿨고 무엇으로 완료를 판정했는가”를 추적할 수 있다.

## F04. Task / Attempt / Worker State Model

Task는 여러 Attempt를 가질 수 있고 각 Attempt는 서로 다른 Worker에서 실행될 수 있다. Worker가 교체되어도 Task와 Attempt History는 남는다.

## F05. Control Plane vs Execution Plane

Control Plane은 Task State, Assignment, Retry, Approval을 관리하고 Execution Plane은 실제 Repository 수정과 Build/Test를 수행한다. Work State와 Compute를 분리하는 것이 핵심이다.

## F06. Worker Isolation Boundary

Workspace Isolation은 Git Branch만의 문제가 아니다. Filesystem, Process, Network, Credential, Runtime State, External Resource를 각각 어떤 경계로 분리할지 결정해야 한다.

## F07. Harness / Context / Runtime

Harness는 Model과 실제 Software Environment 사이에서 Instruction, Context, Tool Interface, Feedback을 연결한다. Sandbox와 Runtime은 실행 공간이고 Harness는 그 실행을 조정하는 계층이다.

## F08. Controlled Autonomy Stack

상위 계층은 Policy와 Durable State를 소유하고, 아래로 갈수록 Agent의 adaptive judgment가 커진다. 이미 알고 있는 Rule과 불확실한 Search/Judgment를 같은 방식으로 처리하지 않는다.

## F09. Verification Pyramid

Static Check에서 Human Acceptance까지 검증의 범위와 비용이 달라진다. 모든 Task가 가장 높은 단계까지 갈 필요는 없으며 Risk에 맞는 검증 조합을 선택한다.

## F10. Evidence vs Provenance

Evidence는 결과가 맞다는 근거이고 Provenance는 결과가 어떤 Task, Agent, Revision, Policy, Approval을 거쳐 만들어졌는지 나타내는 Lineage다.

## F11. Recovery Ladder

일시적인 Tool 오류에서 Human Escalation까지 Failure Scope에 맞춰 복구 범위를 키운다. 가능한 한 가장 작은 범위부터 복구하는 것이 비용과 재작업을 줄인다.

## F12. Durable Execution Timeline

Side Effect 이후 Crash가 발생해도 Event History, Checkpoint, Idempotency를 통해 이미 완료된 실행을 재구성하고 안전하게 Resume할 수 있어야 한다.

## F13. Agent Security Delegation

Human Principal의 권한 전체를 빌려주는 대신 Task와 Agent Identity에 필요한 Capability만 위임한다. Identity, Authorization, Approval, Audit를 하나의 Delegation Chain으로 본다.

## F14. Parallel Fan-out / Fan-in

Task Independence가 확보된 Work만 여러 Worker에 Fan-out하고, Fan-in 이후에는 Integration Verification을 수행한다. Parallelism의 단위는 Agent 수가 아니라 독립 Task다.

## F15. Factory Throughput Bottleneck

전체 Factory 처리량은 Worker 수 하나가 아니라 Ready Work, Verification, Review, Integration, Deployment 등 가장 느린 단계에 제한된다.

## F16. Task Timeline / Observability

Task Cycle Time을 Queue, Execution, Verification, Human Wait로 분해하면 병목이 Model인지 Review인지 구분할 수 있다.

## F17. Signal → Task Conversion

Production Alert나 CI Failure를 바로 Agent Action으로 연결하지 않는다. Diagnose, Scope, Risk, Acceptance를 거쳐 실행 가능한 Task로 변환한다.

## F18. Factory ↔ Developer Platform

Factory는 기존 Developer Platform의 Golden Path, CI/CD, Secret, Deploy, Observability Capability를 재사용한다. 사람과 Agent가 같은 Platform Capability를 서로 다른 Interface로 소비한다.

## F19. Minimum Viable Factory

첫 Factory는 Single Worker와 Human Review로도 충분하다. 중요한 것은 Durable Task, Isolation, Verification, Evidence가 반복 가능한 흐름으로 연결되는가다.

## F20. Reference Factory Acceptance Scenarios

Happy Path뿐 아니라 Verification Failure, Worker Kill, Reassignment, Human Wait, Parallel Execution, Conflict를 acceptance scenario로 만들어 Factory Reliability를 검증한다.

## F21. Maturity × Autonomy Matrix

Factory Capability의 성숙도와 Agent Decision Authority는 서로 다른 축이다. 운영 Capability가 높아도 Risk가 큰 Decision은 Human Authority를 유지할 수 있다.
