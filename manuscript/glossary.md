# Glossary

이 Glossary는 책에서 반복해서 사용하는 핵심 용어의 의미를 고정한다.

영문 기술어를 모두 한국어로 번역하는 것이 목적이 아니다. 같은 단어가 장마다 다른 의미로 쓰이지 않도록 하는 것이 목적이다.

## AI Software Factory

소프트웨어 작업을 durable하게 관리하고, AI Agent에게 실행을 위임하며, 독립된 검증과 통제 아래 실패를 복구하고 검증된 변경을 지속적으로 전달하는 소프트웨어 생산 시스템.

이 책의 working definition이다.

## Agent

Model을 중심으로 Context, Tool, 실행 루프를 결합해 목표 지향적인 작업을 수행하는 실행 주체.

Model 자체와 구분한다.

## Task

완료까지 추적되는 Work Item.

Prompt보다 오래 살아남으며 Goal, Scope, Acceptance, State, Attempt, Verification 같은 정보를 가질 수 있다.

## Durable Task

Agent Session이나 Worker보다 오래 살아남는 Task.

이 책의 개념어다.

Microsoft Durable Task 제품/기술명과 구분한다.

## Attempt

하나의 Task를 완료하기 위한 개별 실행 시도.

Task 하나에 여러 Attempt가 존재할 수 있다.

## Worker

Task를 실제로 실행하는 Compute/Runtime 단위.

Workspace, Runtime, Tool, Network, Temporary State를 포함할 수 있다.

## Control Plane

Task State, Assignment, Retry, Dependency, Approval, Policy처럼 Work의 흐름을 관리하는 계층.

## Execution Plane

Worker와 Workspace에서 실제 코드 수정, Build, Test, Browser 실행 등이 일어나는 계층.

## Harness

Model이 실제 Work를 수행하도록 Context, Tool Interface, Instruction, Feedback, Verification Hook을 연결하는 조정 계층.

Sandbox/Compute 자체와 구분한다.

## Sandbox

Agent 실행을 다른 Task나 Production 환경에서 격리하는 실행 경계.

Filesystem, Process, Network, Credential 등의 격리를 포함할 수 있다.

## Context

Agent가 현재 판단과 작업에 사용하는 정보.

Context Window는 durable storage가 아니다.

## Agent Legibility

Repository, Runtime, Platform 상태를 Agent가 탐색하고 이해할 수 있는 정도.

문서량보다 discoverability와 machine-readable feedback을 중시한다.

## Acceptance Criteria

Task가 어떤 상태가 되면 완료로 판단할 수 있는지 정의한 기준.

가능하면 Verification으로 연결될 수 있어야 한다.

## Acceptance Authority

Residual Risk를 받아들이고 최종 완료/승인을 결정할 권한.

Implementer와 같은 주체일 필요는 없다.

## Verification

Agent의 Completion Claim을 독립적으로 확인하는 과정 또는 subsystem.

Compile, Test, Runtime Check, Security Scan, Evaluator, Human Review 등을 포함할 수 있다.

## Evidence

완료 판단을 뒷받침하는 관찰 가능한 근거.

예:

- Test Result
- Screenshot
- Log
- Benchmark
- Runtime Response

## Evidence Contract

Task Result와 Verification/Evidence를 일정한 구조로 반환하기 위한 이 책의 설계 패턴.

업계 표준 명칭이 아니다.

## Evidence Manifest

Evidence Contract를 machine-readable artifact로 표현한 결과물.

## Provenance

Result가 어떤 Requirement, Task, Agent, Revision, Policy, Approval을 거쳐 만들어졌는지 나타내는 Lineage.

Evidence와 구분한다.

## Retry

동일하거나 유사한 실행 범위를 다시 수행하는 복구 방식.

## Restart

Worker 또는 실행을 처음 상태에 가깝게 다시 시작하는 것.

## Resume

Checkpoint나 durable state를 사용해 이미 완료된 Work를 보존하고 이어서 실행하는 것.

## Reassignment

같은 Task를 다른 Worker에 배정하는 것.

Resume와 항상 같은 의미는 아니다.

## Recovery

실패 후 Task를 일관된 상태로 되돌리거나 계속 진행하게 만드는 전체 복구 과정.

## Durable Execution

Crash, Retry, Wait, External Event를 넘어 Workflow 실행 상태를 보존하고 재개하는 실행 모델.

Agent Memory와 구분한다.

## Human Gate

특정 Risk를 받아들이기 전에 사람의 판단이나 승인을 요구하는 Policy Point.

모든 Task에 필요한 것은 아니다.

## Controlled Autonomy

이미 알고 있는 Rule과 durable state는 System이 관리하고, 사전 규칙화하기 어려운 Search/Judgment에 Agent의 자율성을 사용하는 설계 원칙.

## Useful Parallelism

동시에 실행된 Agent/Worker 수가 아니라 Conflict, Duplicate Work, Reconciliation Cost를 제외하고 실제로 증가한 유효한 병렬 Work.

이 책에서 사용하는 설명 개념이다.

## Observability

Task, Attempt, Worker, Verification, Human Wait, Cost 등 externally observable state와 event를 통해 Factory의 실제 Flow를 이해하는 능력.

Raw Chain-of-Thought 수집과 같은 뜻이 아니다.

## Accepted Change

필요한 Verification과 Acceptance를 거쳐 조직이 받아들인 Software Change.

이 책의 Factory-level measurement boundary를 설명하기 위한 개념이며 업계 표준 Metric은 아니다.

## Cost per Accepted Change

Accepted Change 하나를 만드는 데 들어간 Model, Compute, CI, Review, Retry, Rework 등의 비용을 함께 보려는 후보 지표.

이 책의 synthesis다.

## Closed-loop SDLC

Operate/Observe에서 나온 Signal이 다시 Diagnosis, Requirement, Test, Task, Delivery로 돌아가는 Software Delivery Loop.

이 책에서는 기존 Continuous Feedback을 Agent Work Intake까지 확장해 사용한다.

## Golden Path

조직이 반복적으로 사용하는 검증되고 표준화된 Platform Capability/Workflow.

Agent에게는 API/MCP/Tool 형태의 machine contract로 노출할 수 있다.

## Maturity

Factory가 갖춘 운영 Capability의 범위.

이 책의 M0~M5는 비규범적 설명 taxonomy이며 조직 점수가 아니다.

## Autonomy

Work Selection, Planning, Execution, Verification, Acceptance, Merge/Deploy 같은 Decision Authority를 Agent/System에 얼마나 위임했는지 나타내는 축.

Maturity와 같은 축이 아니다.
