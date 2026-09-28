# 16장 설계 - Security, Identity, Governance

## 장의 목표

Autonomy와 실행 범위가 커질수록 failure probability보다 blast radius를 줄이는 구조가 중요함을 설명한다. isolation, scoped credential, agent identity, audit, approval을 하나의 governance model로 묶는다.

이 장의 핵심 질문:

> Agent에게 어떤 권한을 어떻게 위임해야 하는가?

> Prompt instruction만으로 위험한 행동을 막을 수 있는가?

---

## 핵심 주장

> AI Software Factory 보안의 목표는 Agent를 완전히 신뢰하는 것이 아니라 덜 신뢰해도 안전하게 운영하는 것이다.

> Mandatory rule은 prompt가 아니라 filesystem/network/IAM/hook/policy에서 강제해야 한다.

> Human identity를 Agent에게 그대로 복제하기보다 Task 범위의 delegated authority를 주는 방향이 적합하다.

---

## 독자가 얻는 것

- Filesystem/network/credential isolation 경계를 설계할 수 있다.
- Agent identity와 initiating human principal을 구분할 수 있다.
- Risk-based approval을 설계할 수 있다.
- Audit와 Provenance에 필요한 event를 정의할 수 있다.

---

## 반드시 사용할 Research
- `research/30-workos-product-engineering-factory.md`

- `research/06-security-isolation-and-permissions.md`
- `research/14-failure-modes-and-antipatterns.md`
- `research/15-governance-provenance-and-agent-identity.md`
- `research/25-human-agent-collaboration-and-responsibility-research.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- Prompt-only Security
- Developer personal token을 Worker에 그대로 전달
- 모든 tool action에 human approval을 요구해 approval fatigue 유발
- Implementer가 test/approval/deploy authority를 모두 가지는 구조

---

# 절 구성

## 16.1 Blast Radius 모델

Agent가 틀릴 수 있다는 전제에서 filesystem, network, credential, branch, environment 경계를 설계한다.

## 16.2 Scoped Credential

repo/branch/environment/task/time 범위로 짧게 발급되는 credential과 broker/proxy pattern을 설명한다.

## 16.3 Agent Identity와 Delegation

Human Principal → Task → Agent Identity → Scoped Capability 관계를 설명한다.

## 16.4 Prompt Injection과 Untrusted Context

Issue/PR/comment 같은 text가 Tool authority와 연결될 때 생기는 risk를 Microsoft 사례로 설명한다.

## 16.5 Risk-based Human Gate

모든 action을 승인받는 대신 auth/payment/migration/production 등 risk class에 따라 gate를 배치한다.

## 16.6 Audit / Provenance

task created, credential issued, external write, policy denied, verification, approval, deploy를 externally observable audit event로 기록한다.


---

## 필요한 구조 / 그림

1. Human Principal→Task→Agent Identity→Capability delegation
2. Layered defense: Model/Environment/Tool/Workflow
3. Risk class vs approval/permission matrix

---

## 실전 예제 / 실험

- Docs task는 repo-write만, production migration task는 read-only planning 후 human approval
- Untrusted PR comment가 shell/tool invocation으로 이어지는 공격 흐름

---

## 본문에서 의도적으로 다루지 않을 내용

- 일반 AI Safety
- enterprise IAM 제품 비교
- cryptographic attestation 상세

---

## 앞뒤 장 연결

17장에서는 안전한 단일 Worker를 여러 개로 늘릴 때 생기는 parallelism과 coordination 문제를 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
