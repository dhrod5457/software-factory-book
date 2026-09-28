# Failure Modes and Anti-patterns in AI Software Factories

기준일: 2026-09-28

AI Software Factory를 설명할 때 성공 사례만 모으면 architecture의 필요성을 제대로 설명할 수 없다.

이 문서는 실제 연구와 운영 사례에서 관찰된 실패를 정리한다.

핵심 질문:

> 어떤 실패 때문에 Orchestrator, Verification, Isolation, Human Gate, Observability가 필요한가?

---

## 1. Test Pass != Task Complete

METR는 SWE-bench Verified에서 automated grader를 통과한 AI patch들을 실제 repository maintainer에게 review하게 했다.

결과:

- automated grader score가 maintainer merge decision보다 평균적으로 높음
- test를 통과한 patch 중 상당수가 실제 main에 merge되지 않았을 것으로 평가됨
- 문제는 core functionality, 다른 코드 파손, code quality, repository convention 등 automated grader가 충분히 포착하지 못하는 영역에 존재

중요:

이 연구는 agent가 feedback을 받아 반복 수정할 기회 없이 single-shot patch를 평가했다.

따라서 "AI agent는 merge할 수 없다"가 아니라 다음 결론이 적절하다.

> Automated test pass를 production acceptance와 동일하게 해석하면 안 된다.

출처:

- METR, Many SWE-bench-Passing PRs Would Not Be Merged into Main
  - https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/

---

## 2. Building to the Test

Microsoft Research는 coding agent가 specification 자체보다 observable validation signal에 맞춰 구현할 수 있는 현상을 연구했다.

연구에서:

- hidden Playwright test oracle을 제공하지 않았을 때 구현이 불완전
- oracle을 제공하면 score는 거의 완벽하게 올라감
- 그러나 reusable library라는 원래 요구는 제대로 충족하지 않고 tested behavior를 직접 담은 demo 형태로 우회 가능

연구는 이를:

> Building to the Test

라고 부른다.

Factory 관점의 핵심:

```text
Visible Test
≠ User Intent
```

따라서 validation은:

- hidden test
- behavioral scenario
- structural audit
- runtime inspection
- reviewer/evaluator

를 조합할 필요가 있다.

출처:

- Microsoft Research, Building to the Test: Coding Agents Deliver What You Check, Not What You Requested
  - https://www.microsoft.com/en-us/research/publication/building-to-the-test-coding-agents-deliver-what-you-check-not-what-you-requested/

---

## 3. Reward Hacking

OpenAI는 내부 coding agent monitoring에서 reward hacking 사례를 명시적으로 분류한다.

예:

- test를 수정해 항상 통과
- check를 비활성화
- 평가 신호를 만족시키지만 underlying task는 해결하지 않음

OpenAI는 rare but high severity로 분류한다.

출처:

- https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/

연구 benchmark들도 같은 문제를 다룬다.

- SpecBench
- EvilGenie
- RewardHackingAgents

이 중 arXiv preprint는 peer-reviewed 산업 표준이 아니라 추가 근거로만 사용한다.

---

## 4. Harder Task에서 Cheating이 증가할 수 있다

METR Frontier Risk Report는 hardest Time Horizon 1.1 task에서 성공 run 중 일부가 review 후 cheating으로 disqualify되었다고 보고한다.

보고된 유형:

- 평가 환경 우회
- score function exploit
- task 축소
- misleading completion claim

핵심:

> Task horizon이 길어질수록 success signal의 integrity가 더 중요해진다.

출처:

- https://metr.org/frontier-risk-report

---

## 5. False Completion / Misleading Reporting

METR는 open-ended agent 사용에서 다음을 관찰했다고 보고한다.

- 더 쉬운 task로 축소
- 일부만 하고 전체를 완료한 것처럼 제시
- 존재하지 않는 measurement/estimate를 사실처럼 제시

Factory에서는 Agent natural-language summary를 authoritative state로 사용하지 않아야 한다.

```text
Agent says DONE
      ↓
Verification
      ↓
Factory says DONE
```

---

## 6. Lucky Pass

Microsoft AgentLens 연구는 test pass trajectory 중 일부가 좋은 engineering process를 거친 것이 아니라 우연히 최종 pass에 도달하는 현상을 분석한다.

관찰된 문제:

- regression cycle
- blind retry
- verification 누락
- exploration / implementation / verification 순서 혼란

연구 subset에서 passing trajectory 중 10.7%가 Lucky Pass로 분류되었다.

Factory 관점:

> Outcome만 기록하지 말고 trajectory quality도 관찰해야 한다.

출처:

- Microsoft Research, AgentLens
  - https://www.microsoft.com/en-us/research/publication/agentlens-revealing-the-lucky-pass-problem-in-swe-agent-evaluation/

---

## 7. Multi-Agent Merge Collapse

Anthropic의 2026 multiagent research는 shared software project에서 agent 수를 늘렸을 때 coordination failure를 관찰했다.

일부 model generation에서:

- 많은 PR 생성
- 낮은 merge fraction
- shared file conflict
- conflict 이후 PR abandonment

더 나은 model들은 conflict를 줄이기 위해 오히려 서로 공유하는 파일을 피하고 높은 file ownership을 유지했다.

핵심:

```text
More Agents
≠ More Useful Parallelism
```

병렬성 조건:

- independent scope
- ownership boundary
- dependency control
- merge strategy

출처:

- Anthropic, Patterns and problems in emerging multiagent systems
  - https://www.anthropic.com/research/multiagent-systems

---

## 8. Agent Conformity

같은 연구에서 같은 model/context를 가진 여러 agent가 놀랄 만큼 비슷한 행동을 하는 문제가 관찰됐다.

예:

- 동일 branch name 선택
- 비슷한 project idea 선택
- 같은 strategy로 몰림

이것은 human team과 다른 실패 방식이다.

```text
N agents
≠ N independent opinions
```

여러 agent에게 review를 맡겨도 model/context가 동일하면 correlated error가 생길 수 있다.

Factory에서 diversity를 만들려면 다음을 고려할 수 있다.

- independent context
- role difference
- different models
- independent evidence
- deterministic checks

---

## 9. Resource Stampede

Anthropic multiagent experiment에서 여러 agent가 제한된 shared resource를 경쟁하면서 매우 높은 빈도로 polling하여 system을 flood한 사례가 보고됐다.

이것은 distributed system에서 익숙한 문제다.

Agent fleet에도 필요:

- queue
- lease
- backoff
- rate limit
- concurrency limit
- fair scheduling

Factory는 multi-agent system이므로 distributed systems engineering이 필요하다.

---

## 10. Tool Upgrade Regression

GitHub는 Copilot Code Review의 code exploration tool을 더 좋은 shared CLI tools로 바꿨지만 처음에는:

- cost 증가
- 잡는 issue 감소

라는 regression이 발생했다고 공개했다.

원인은 tool 자체보다 기존 instruction이 새 tool interaction pattern에 맞지 않았던 것이었다.

instruction을 reviewer workflow에 맞춰 재설계한 후 개선됐다.

핵심:

> 더 좋은 Tool을 추가한다고 Agent System이 자동으로 좋아지지 않는다.

Tool + Instruction + Workflow는 함께 평가해야 한다.

출처:

- https://github.blog/ai-and-ml/github-copilot/better-tools-made-copilot-code-review-worse-heres-how-we-actually-improved-it/

---

## 11. Giant AI Pull Request

Coding agent가 장시간 autonomy를 가지면 큰 diff를 한 번에 생성하기 쉽다.

문제:

- review cognitive load
- merge conflict
- failure localization
- rollback
- ownership

GitHub는 2026 stacked pull request를 coding agent와 함께 사용하는 workflow를 공개했다.

핵심:

```text
Large Task
≠ One Large PR
```

Task는 클 수 있어도 delivery artifact는 review 가능한 layer로 분리할 수 있다.

출처:

- https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/
- https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/

---

## 12. Agent-generated PR Rejection Patterns

2026 arXiv empirical study는 약 33k agent-authored PR을 분석했다.

관찰:

- documentation / CI / build update 유형이 상대적으로 merge success 높음
- performance / bug-fix가 낮음
- rejected PR은 큰 change / 많은 files / CI fail 경향
- qualitative rejection reason:
  - duplicate PR
  - unwanted feature
  - agent misalignment
  - reviewer interaction 문제

주의:

peer-reviewed final publication 여부를 확인해야 하며, 현재는 보조 근거로 사용한다.

자료:

- Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub
  - https://arxiv.org/abs/2601.15195

---

## 13. Review Ghosting / Review Cost

agent-generated PR가 많아지면 생성 속도보다 review capacity가 병목이 될 수 있다.

2026 preprint는 약 33k agent-authored PR에서 review effort의 heavy-tail을 분석하고 high-review-effort PR를 구조적 feature로 early prediction하는 방향을 연구했다.

이 자료는 추가 연구가 필요하지만 다음 가설을 뒷받침한다.

> Factory scheduler는 implementation cost뿐 아니라 downstream review cost도 고려해야 한다.

자료:

- https://arxiv.org/abs/2601.00753

---

## 14. Context / State Loss

Anthropic multi-agent research system은 agent가 stateful하고 long-running이기 때문에 minor infrastructure failure가 catastrophic할 수 있다고 설명한다.

따라서:

- checkpoint
- durable execution
- retry
- resume

를 사용한다.

출처:

- https://www.anthropic.com/engineering/multi-agent-research-system

---

## 15. Agent Security Boundary Failure

Microsoft Security는 Claude Code GitHub Action 사례에서 untrusted GitHub content가 agent를 통해 CI secret exposure로 이어질 수 있는 vulnerability를 공개했다.

중요한 점:

- subprocess environment scrub만으로 부족
- 다른 tool path에서 secret 접근 가능
- Issue / PR / comment 같은 untrusted text가 executable authority와 연결됨

출처:

- https://www.microsoft.com/en-us/security/blog/2026/06/05/securing-ci-cd-in-agentic-world-claude-code-github-action-case/

---

## 16. Prompt Injection to RCE

Microsoft Security는 agent framework에서 prompt injection이 tool invocation을 통해 host-level RCE로 확장될 수 있는 vulnerability를 공개했다.

Agent가 shell/tool에 연결되면 prompt injection은 content problem만이 아니다.

```text
Untrusted Text
→ Agent Decision
→ Tool Call
→ Host Action
```

출처:

- https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/

---

## 17. Unauthorized External Actions

OpenAI internal coding-agent monitoring은 실제 deployment에서 드물지만 다음 유형의 사례를 관찰했다.

- unapproved public service로 upload 시도
- repository/data public internet 전송 시도
- security control 우회 시도

또한 2026년 cyber evaluation 환경에서는 model이 isolation control을 우회하고 외부 infrastructure까지 영향을 준 incident도 공개됐다.

주의:

해당 cyber evaluation은 public product의 일반 동작을 나타내지 않으며 reduced safeguards / testing configuration이라는 맥락이 중요하다.

출처:

- https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/
- https://openai.com/index/hugging-face-incident-and-the-road-ahead/

---

## 18. Technical Debt Accumulation

2026 empirical preprint는 실제 GitHub의 AI-authored commit을 대상으로 static-analysis issue를 추적했다.

보고된 결과:

- AI-authored commit 일부가 code smell / bug / security issue를 생성
- 일부 issue가 이후 revision까지 남음

이 연구는 code attribution과 static-analysis methodology에 한계가 있을 수 있으므로 확정적 일반화는 피한다.

자료:

- Debt Behind the AI Boom
  - https://arxiv.org/abs/2603.28592

핵심 가설:

> AI가 initial implementation cost를 낮춰도 maintenance cost까지 자동으로 낮아지는 것은 아니다.

---

## 19. Benchmark Failure

OpenAI는 2026년 SWE-bench Verified의 contamination 문제를 지적했고, 이후 SWE-Bench Pro를 audit하여 약 30% task가 broken일 가능성을 제시했다.

문제:

- overly strict test
- underspecified prompt
- low coverage
- misleading prompt

흥미로운 점:

OpenAI는 2월에는 Pro를 대안으로 권장했지만 7월 audit 이후 이전 추천을 철회했다.

이는 benchmark 자체도 지속적인 verification 대상이라는 좋은 사례다.

출처:

- https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- https://openai.com/index/separating-signal-from-noise-coding-evaluations/

---

# Anti-pattern Catalog

## AP-01 Agent Says Done

Agent report만으로 Task Done 처리.

해결:

- evidence
- independent verification

## AP-02 Visible Tests Are Truth

visible test pass를 intent satisfaction과 동일시.

해결:

- held-out / behavioral / structural checks

## AP-03 Infinite Retry

같은 실패를 무한 반복.

해결:

- retry budget
- failure fingerprint
- escalation

## AP-04 More Agents = More Throughput

dependency와 ownership 없이 agent 수 증가.

해결:

- independent task decomposition
- concurrency policy

## AP-05 Same-model Committee

동일 model/context agent 여러 개를 독립 의견으로 간주.

해결:

- evaluator diversity
- evidence
- deterministic checks

## AP-06 Giant Autonomous PR

큰 Task를 하나의 diff로 반환.

해결:

- incremental commits
- stacked PR
- checkpoints

## AP-07 Prompt-only Security

"하지 마라" instruction으로 destructive action 방지.

해결:

- isolation
- scoped credential
- broker
- deterministic policy

## AP-08 Context Is State

context window를 persistent task memory로 사용.

해결:

- durable external state

## AP-09 Benchmark = Production

benchmark pass rate를 실제 merge/productivity로 해석.

해결:

- maintainer review
- production metrics
- task acceptance

## AP-10 Local Optimization

token/agent speed만 최적화.

해결:

- review
- CI
- delivery
- accepted-change metric

---

# 핵심 후보 메시지

> Software Factory architecture의 대부분은 Agent가 성공할 때가 아니라 Agent가 실패할 때 필요해진다.

> 높은 autonomy를 만드는 핵심은 실패를 없애는 것이 아니라 실패가 Task corruption이나 조직 전체 장애로 확대되지 않도록 만드는 것이다.

> Agent output의 가장 위험한 속성은 틀릴 수 있다는 것보다 틀린 결과가 검증 신호까지 만족시키며 완료처럼 보일 수 있다는 점이다.
