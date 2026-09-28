# Security, Isolation, and Permissions

기준일: 2026-09-28

AI Software Factory는 Agent의 능력이 커질수록 보안 문제도 커진다.

핵심 질문은 단순히 "Agent가 실수할 확률"이 아니다.

> Agent가 실수하거나 공격당했을 때 어디까지 피해를 줄 수 있는가?

즉, probability뿐 아니라 **blast radius**를 설계해야 한다.

## 1. Human Approval만으로는 충분하지 않다

Anthropic은 Claude Code telemetry에서 permission prompt의 약 93%가 승인된다고 공개했다.

문제:

- approval fatigue
- 반복 승인으로 주의력 저하
- multi-agent에서는 모든 action을 사람이 추적하기 어려움
- prompt injection은 benign-looking action으로 이어질 수 있음

따라서 autonomy와 safety의 trade-off를 approval dialog만으로 해결하기 어렵다.

출처:

- https://www.anthropic.com/engineering/claude-code-auto-mode
- https://www.anthropic.com/engineering/how-we-contain-claude

## 2. Permission 대신 Capability Boundary

보다 강한 방식:

```text
Agent can only:
- read allowed paths
- write workspace
- access approved hosts
- push session branch
- use scoped credentials
- call approved tools
```

즉, "하면 안 된다"를 prompt로 설명하기보다 **할 수 없는 환경**을 만든다.

## 3. Filesystem Isolation + Network Isolation

Anthropic Claude Code sandboxing은 두 경계를 함께 강조한다.

### Filesystem

- workspace write 허용
- sensitive system path 제한

### Network

- approved domain만 접근
- proxy를 통한 outbound control

한쪽만 막는 것은 충분하지 않다.

- filesystem만 격리하고 network open → secret exfiltration 위험
- network만 막고 filesystem unrestricted → host credential/system 변경 위험

출처:

- https://www.anthropic.com/engineering/claude-code-sandboxing

## 4. Credential을 Sandbox 안에 직접 넣지 않는다

Claude Code on the web 사례:

- git credential/signing key를 sandbox 안에 직접 노출하지 않음
- custom proxy가 git operation을 중계
- scoped credential
- branch/repository destination 검증
- proxy가 실제 auth token을 attach

중요한 패턴:

```text
Agent
→ constrained operation request
→ trusted broker/proxy
→ policy check
→ privileged system
```

이 구조는 Git 외에도 적용 가능하다.

- cloud deployment
- DB migration
- artifact upload
- ticket update
- production action

## 5. Sandbox Credential과 Service Credential 분리

Factory 후보 구조:

```text
Orchestrator Credential
- task system
- worker lifecycle

Worker Credential
- repo branch
- artifact bucket
- test system

Production Credential
- 직접 제공하지 않음
- broker/approval 통과
```

Least privilege가 핵심이다.

## 6. Prompt Injection은 External Context에서 온다

Anthropic은 외부 content를 별도 attack surface로 본다.

예:

- poisoned README
- issue text
- web page
- MCP result
- Slack
- third-party docs

MCP server가 안전해도 MCP가 가져오는 data가 안전하다는 뜻은 아니다.

즉:

```text
Trusted Connector
≠ Trusted Content
```

출처:

- https://www.anthropic.com/engineering/how-we-contain-claude

## 7. Model Layer + Environment Layer + Tool Layer

방어를 겹친다.

### Model layer

- system instruction
- prompt injection detection
- action classifier
- safety training

### Environment layer

- VM/container
- filesystem
- network
- process
- resource limit

### Tool layer

- scoped API
- allowlist
- read-only
- broker
- server-side validation

### Workflow layer

- approval
- protected branches
- CI
- deploy policy

한 layer에만 의존하지 않는다.

## 8. Auto Mode의 Action Classifier

Anthropic Auto Mode는:

- safe tool allowlist
- project file edits 자동 허용
- 위험 가능 action은 transcript classifier
- prompt injection probe
- repeated denial 시 escalation

중요한 설계:

classifier는 agent의 설명보다 **실제 action payload와 user intent**를 평가한다.

이것은 Factory의 approval automation에 참고할 수 있다.

출처:

- https://www.anthropic.com/engineering/claude-code-auto-mode

## 9. Deny-and-Continue

위험 action을 차단했다고 session을 무조건 종료할 필요는 없다.

```text
Action denied
→ reason returned
→ agent finds safer path
→ continue
```

장점:

- false positive가 전체 task failure로 이어지지 않음
- autonomy 유지

단 반복 denial은 escalation한다.

이것은 Security Gate를 failure가 아니라 **normal feedback**로 만드는 패턴이다.

## 10. Protected Branch와 Agent Branch

Agent가 자유롭게 write할 수 있는 영역을 분리한다.

```text
Agent:
- own branch write
- force push limited
- main direct push forbidden

Human/Delivery Service:
- merge
- protected environment deployment
```

Agent에게 repo write permission이 있어도 organization 전체 permission을 줄 필요가 없다.

## 11. Secret Detection

Factory.ai Droid Shield:

- autonomous commit/push 전에 secret detection
- suspicious secret 발견 시 block

Agent 생산량이 커질수록 human reviewer가 모든 diff를 보지 못할 수 있으므로 deterministic scanning의 중요성이 커진다.

출처:

- https://factory.ai/news/droid-shield-2-0

## 12. Hooks as Policy Enforcement

GitHub Copilot Hooks:

- tool execution approve/deny
- secret scanning
- custom validation
- audit logging
- failure alert

중요:

Prompt instruction이 아니라 lifecycle event에서 deterministic enforcement가 가능하다.

출처:

- https://docs.github.com/en/copilot/concepts/agents/hooks

## 13. Self-hosted Execution

Cursor는 self-hosted cloud agents를 지원한다.

목적:

- repository checkout이 perimeter 밖으로 나가면 안 되는 조직
- internal dependency/network 필요
- compliance
- local caches
- proprietary services

하지만 agent loop와 inference까지 반드시 on-prem이라는 뜻은 아니다.

어디에서 무엇이 실행되는지 정확히 분해해야 한다.

출처:

- https://cursor.com/blog/self-hosted-cloud-agents
- https://cursor.com/docs/cloud-agent/self-hosted/choose-runtime

## 14. Resource Isolation

보안뿐 아니라 reliability와 cost에도 필요하다.

Worker별:

- CPU
- memory
- disk
- process count
- execution time
- network
- artifact quota

단 너무 tight한 resource limit은 agent 성능 평가 자체를 왜곡할 수 있다.

Anthropic은 Terminal-Bench 실험에서 resource configuration만으로 success rate가 크게 변할 수 있음을 공개했다.

출처:

- https://www.anthropic.com/engineering/infrastructure-noise

## 15. Task Risk Class

Factory에 risk class를 도입할 수 있다.

### R0 - Read only

- research
- code reading
- documentation analysis

### R1 - Isolated source change

- branch change
- test
- no external write

### R2 - Shared development system write

- issue
- PR
- artifact
- dev database

### R3 - Staging action

- deploy
- migration rehearsal
- integration credentials

### R4 - Production / destructive

- production deploy
- schema mutation
- delete
- external customer impact

Risk별:

- worker profile
- model mode
- approval
- verification
- credential
- retry

를 다르게 한다.

## 16. 핵심 후보 메시지

> AI Software Factory의 보안은 Agent를 믿을 수 있게 만드는 문제보다 Agent를 덜 믿어도 운영 가능한 경계를 만드는 문제다.

> autonomy를 늘리고 싶다면 approval prompt를 없애는 것이 아니라 sandbox, scoped capability, deterministic policy를 먼저 강화해야 한다.

> Agent의 권한은 사람 개발자의 계정을 그대로 복제하는 방식보다 Task에 필요한 capability를 임시로 위임하는 방식이 바람직하다.
