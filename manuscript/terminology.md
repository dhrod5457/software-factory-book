# Terminology Guide

기준일: 2026-09-28

Manuscript 단계에서 사용할 canonical terminology다.

목표는 모든 영문을 번역하는 것이 아니라 **같은 개념을 장마다 다른 표현으로 쓰지 않는 것**이다.

## 핵심 용어: 영문 유지

다음은 책의 architecture vocabulary로 영문 표기를 유지한다.

- AI Software Factory
- Agent
- Task
- Worker
- Factory
- Harness
- Sandbox
- Control Plane
- Execution Plane
- Durable Task
- Durable Execution
- Evidence Contract
- Context
- Runtime
- Tool
- MCP
- CI/CD
- Pull Request
- Repository
- Benchmark
- Token

## 한국어 우선

본문 prose에서는 다음 표기를 기본으로 한다.

| 혼용 후보 | Canonical |
| --- | --- |
| Review | 리뷰 |
| Reviewer | 리뷰어 |
| Verification | 검증 |
| Integration | 통합 |
| Approval | 승인 |
| Permission | 권한 |
| Environment | 환경 / 실행환경 |
| Failure | 실패 |
| Recovery | 복구 |
| Dependency | 의존성 |
| Requirement | 요구사항 |
| Specification | 명세 |
| Metric | 지표 |

단, 다음 경우 원문 영문을 유지한다.

- 제품/논문 제목
- API/상태/필드 이름
- 코드 예제
- 고유한 architecture term을 처음 정의하는 문장

## 의미 구분이 필요한 용어

### Acceptance

두 의미를 구분한다.

- Acceptance Criteria → 완료 기준 / Acceptance Criteria
- Acceptance Authority → 완료 승인 권한 / Acceptance Authority

단순히 모두 “승인”으로 번역하지 않는다.

### Evidence

일반 문장에서는 “근거”라고 쓸 수 있지만, 책의 구조적 개념인 `Evidence`, `Evidence Contract`, `Evidence Manifest`는 영문을 유지한다.

### State / Status

- State → 시스템 상태 모델
- Status → 특정 Task/Attempt의 현재 상태 값

구현 예제에서는 원문 필드명을 유지한다.

### Runtime / Environment

- Runtime → 실행 중인 compute/process/tool context
- Environment → 실행에 필요한 OS/runtime/dependency/config 환경

서로 같은 말로 치환하지 않는다.

## 출처

외부 논문·제품·문서 제목은 번역하거나 용어를 치환하지 않고 원문을 유지한다.

## 적용 순서

1. Chapter title은 마지막에 일괄 검토
2. 본문 prose의 Review/Verification/Integration부터 통일
3. 코드/diagram/source title은 제외
4. 의미가 달라질 수 있는 Acceptance/Evidence/Runtime은 수동 검토
