# Governance, Provenance, and Agent Identity

기준일: 2026-09-28

AI Software Factory가 개인 개발자의 로컬 도구를 넘어 조직 infrastructure가 되면 새로운 질문이 생긴다.

> 이 변경을 누가 했는가?

Agent 시대에는 이 질문을 더 세분화해야 한다.

- 어떤 사람/서비스가 Task를 시작했는가?
- 어떤 Agent identity가 실행했는가?
- 어떤 model/harness/policy가 사용되었는가?
- 어떤 권한으로 어떤 system에 접근했는가?
- 어떤 source context를 사용했는가?
- 어떤 artifact를 만들었는가?
- 누가 승인했는가?

---

## 1. Agent Identity는 실제 Infrastructure 문제로 이동 중

NIST NCCoE는 2026년 Software and AI Agent Identity and Authorization을 별도 project 주제로 제시했다.

관심 영역:

- identification
- authentication
- authorization
- auditing
- non-repudiation
- prompt injection mitigation

출처:

- https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd
- https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents

---

## 2. Human Identity를 Agent에게 그대로 복제하지 않는다

위험한 패턴:

```text
Agent
→ developer personal token
→ all developer permissions
```

더 나은 후보:

```text
Human Principal
      ↓ delegates
Task
      ↓
Agent Identity
      ↓
Scoped Capability
```

필요 정보:

- principal
- delegated task
- scope
- expiry
- target system
- allowed actions

Agent identity는 조직의 IAM에 들어갈 가능성이 높다.

---

## 3. Short-lived Credential

Factory worker는 Task 단위 ephemeral credential을 사용하는 것이 적합할 수 있다.

예:

- specific repo
- specific branch
- specific artifact bucket
- limited issue/project
- limited environment
- expiration

이렇게 하면 worker compromise의 blast radius를 줄인다.

---

## 4. Authorization은 Task Context를 알아야 한다

일반 RBAC:

```text
Agent Role = Developer
```

만으로는 너무 넓을 수 있다.

Factory authorization 후보:

```text
Role
+ Task
+ Repository
+ Branch
+ Environment
+ Risk Class
+ Time
```

즉 contextual / attribute-based policy가 유용하다.

---

## 5. GitHub Enterprise Agent Control Plane

GitHub는 2026 Enterprise AI Controls / agent control plane을 GA로 공개했다.

기능 방향:

- agent activity visibility
- audit logging
- enterprise AI administration role
- control configuration

이는 Agent를 개인 productivity tool이 아니라 enterprise-governed actor로 관리하는 방향을 보여준다.

출처:

- https://github.blog/changelog/2026-02-26-enterprise-ai-controls-agent-control-plane-now-generally-available/

---

## 6. Repository-level Agent Configuration Audit

GitHub는 repository의 coding-agent configuration을 API로 audit할 수 있게 했다.

audit 대상 예:

- MCP server
- enabled tools
- GitHub Actions workflow policy
- firewall configuration

Factory 운영에서는 code뿐 아니라 Agent execution configuration도 configuration inventory가 된다.

출처:

- https://github.blog/changelog/2026-05-18-audit-repository-copilot-cloud-agent-configuration-via-the-rest-api/

---

## 7. AI-generated Artifact Traceability

NIST 2026 DevSecOps reference model은 AI output이 다음 특성을 가져야 한다고 강조한다.

- source context 추적
- established control gate
- logging
- accountable stakeholder approval

AI-generated artifact가 supply chain에 provenance/approval 없이 들어가는 것을 risk로 명시한다.

출처:

- https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html

---

## 8. Provenance

기존 software supply chain provenance가 Agent 시대에 더 중요해진다.

Artifact lineage 후보:

```text
Requirement
→ Task
→ Agent Run
→ Commit
→ Build
→ Artifact
→ Attestation
→ Deployment
```

추가 provenance 후보:

- model
- agent version
- system instruction version
- skills
- MCP/tool versions
- base commit
- sandbox image
- verification
- approval

모든 항목을 artifact에 직접 embed할 필요는 없지만 audit system에서 연결 가능해야 한다.

---

## 9. NIST Functional Scenario - Generated Artifact Provenance

NIST NCCoE functional scenario에는 다음이 포함된다.

- generated artifact provenance 생성/검증
- SLSA attestation
- tracking logs
- SBOM 생성/서명

출처:

- https://pages.nist.gov/nccoe-devsecops/functional-demonstration-scenarios.html

Factory가 source code를 생성하는 순간 software supply-chain control의 일부가 된다.

---

## 10. Provenance와 Evidence를 구분

```text
Evidence
= Task가 맞게 수행되었다는 근거

Provenance
= 이 결과가 어디에서 어떻게 만들어졌는지의 계보
```

예:

Evidence:
- tests pass
- screenshot

Provenance:
- Agent X
- model Y
- Task Z
- commit SHA
- build pipeline
- signed artifact

둘 다 필요하다.

---

## 11. Agent-specific Commit Attribution

Git history에서 단순 bot account만 남기는 것보다 다음 연결이 유용하다.

- Task ID
- attempt ID
- initiating human/service
- agent runtime
- review/approval

Commit trailer나 external metadata로 구현할 수 있다.

예:

```text
Task: TASK-123
Attempt: ATT-456
Agent: coding-agent/backend
Requested-By: user/service
Verified-By: pipeline-17
Approved-By: human-or-policy
```

이 형식은 연구 후보이며 표준은 아니다.

---

## 12. Agent Audit Log

최소 audit event 후보:

- task created
- task selected
- credential issued
- tool invoked
- external write
- permission denied
- security policy triggered
- artifact produced
- verification
- approval
- deploy
- rollback

중요:

raw chain-of-thought가 아니라 externally observable action/state를 기록한다.

---

## 13. Confidence-based Automation

GitHub Issues는 2026년 Agent automation에:

- approvals
- confidence
- rationale

control을 공개했다.

예:

- high confidence → 자동 적용
- medium/low → suggestion / human review

Factory에 그대로 적용할 필요는 없지만 다음 패턴을 보여준다.

> Automation authority는 action별로 다르게 설정할 수 있다.

출처:

- https://github.blog/changelog/2026-07-23-agent-automation-controls-in-github-issues-in-public-preview/

---

## 14. Governance as Policy, Not Prompt

조직 정책:

- protected path
- license
- dependency
- security
- deployment
- approval
- data handling

을 Agent에게 natural-language instruction으로만 전달하지 않는다.

가능하면:

- policy engine
- hook
- branch protection
- IAM
- CI
- firewall
- artifact verification

으로 강제한다.

---

## 15. Governance Level 후보

### Project

- repository rules
- test
- allowed tool

### Team

- review
- deployment
- shared resource

### Organization

- model/vendor
- data policy
- secret
- audit
- agent identity

### Regulatory / Customer

- provenance
- segregation of duties
- retention
- compliance

---

## 16. Segregation of Duties

완전 자율 Factory에서도 같은 Agent가:

```text
write code
→ change tests
→ approve itself
→ deploy
```

하는 구조는 위험할 수 있다.

분리 후보:

- implementer
- verifier
- approver
- deployer

각 역할이 반드시 서로 다른 LLM일 필요는 없다.

중요한 것은 authority boundary다.

---

## 17. Third-party Coding Agents

GitHub는 third-party coding agent output에도:

- CodeQL
- dependency validation
- secret scanning

을 자동 적용하는 기능을 GA로 공개했다.

중요한 방향:

> 어떤 Agent vendor가 코드를 작성했는지와 별개로 동일한 downstream security gate를 적용한다.

출처:

- https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/

---

## 18. Factory Configuration도 Supply-chain Input

Agent behavior는 source code 외에도 다음에 의해 바뀐다.

- instructions
- skills
- hooks
- MCP server
- model routing
- sandbox image
- network policy

따라서 이 구성도:

- versioning
- review
- provenance
- rollback

대상이 되어야 한다.

---

## 19. Policy Change Risk

Factory policy를 바꾸는 것은 일반 application code보다 더 큰 blast radius를 가질 수 있다.

예:

```text
maxRetry 3 → 20
network deny → allow
human approval → auto
test required → optional
```

따라서 Factory meta-config change에는 별도 approval/verification이 필요하다.

---

# 핵심 후보 메시지

> AI Software Factory에서는 소스 코드의 provenance만으로 충분하지 않다. 어떤 Agent, 정책, 실행환경, 검증 절차가 결과를 만들었는지도 추적 가능해야 한다.

> Agent에게 사람 계정을 빌려주는 것보다 Task 범위의 권한을 가진 독립 identity를 부여하는 방향이 장기적으로 더 적합하다.

> Governance는 autonomy의 반대가 아니다. Governance가 기계적으로 강제될수록 저위험 영역에서 Agent autonomy를 더 높일 수 있다.
