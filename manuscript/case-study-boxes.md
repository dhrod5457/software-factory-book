# Case Study Boxes

기준일: 2026-09-28

`manuscript/book.md`의 C01~C14 marker에 대응하는 working box copy다.

제품/연구 사례는 일반 원칙의 예시로 사용하며, 회사 내부 수치나 controlled experiment를 업계 일반 사실로 확장하지 않는다.

---

## C01. OpenAI Symphony — Session보다 Task를 관리한다

OpenAI는 2026년 Symphony를 공개하며 내부 경험상 한 엔지니어가 interactive coding-agent session을 여러 개 직접 관리할 때 Context Switching이 빠르게 부담이 된다고 설명했다. 공개 글에서는 대체로 3~5개 session 이후 관리 부담이 눈에 띄었다고 한다.

Symphony가 흥미로운 이유는 숫자 자체가 아니다. 해결 방향이 “더 많은 Terminal”이 아니라 Issue와 Task를 중심으로 Agent Work를 orchestration하는 구조였다는 점이다.

**읽을 때 주의:** 3~5라는 숫자는 OpenAI 내부 운영 사례이며 인간이 관리할 수 있는 Agent 수의 보편적 한계가 아니다.

Source: OpenAI, *An open-source spec for Codex orchestration: Symphony*.

---

## C02. WorkOS Horizon — Durable State와 Disposable Execution

WorkOS의 Horizon은 Software Work를 durable한 control state로 관리하고 실제 실행은 sandbox environment에서 수행하는 구조를 공개했다.

이 사례가 보여주는 핵심은 “어떤 Agent를 썼는가”보다 Task State와 Execution Environment를 분리했다는 점이다. Sandbox가 사라져도 Work 자체가 사라지지 않아야 Retry와 Reassignment가 가능해진다.

**읽을 때 주의:** Horizon의 구체 Architecture가 모든 Factory의 정답이라는 뜻은 아니다.

Source: WorkOS, *The self-driving codebase: Building Horizon at WorkOS*.

---

## C03. Anthropic Managed Agents — Brain과 Hands를 분리한다

Anthropic은 Managed Agents Architecture에서 Session, Harness, Sandbox를 분리해 설명한다. Session은 Agent interaction state, Harness는 Model loop와 Tool/Context orchestration, Sandbox는 실제 Compute와 Filesystem을 담당한다.

이 구분은 “Agent”라는 한 단어 안에 Model, Control Logic, Compute를 모두 넣지 않게 해준다. 각 계층의 Failure와 Lifecycle을 따로 설계할 수 있기 때문이다.

Source: Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands*.

---

## C04. OpenAI Harness Engineering — 거대한 AGENTS.md가 실패한 이유

OpenAI의 Harness Engineering 사례에서는 모든 지식을 하나의 거대한 AGENTS.md에 넣는 접근이 잘 작동하지 않았다고 설명한다. Context를 많이 차지했고, 모든 규칙이 같은 중요도로 보였으며, 문서가 빠르게 stale해졌다.

해당 팀은 대신 짧은 AGENTS.md를 Repository 지식의 목차처럼 사용하고 상세한 Architecture와 운영 지식은 구조화된 문서로 분리했다.

교훈은 “Context를 더 많이 넣어라”가 아니다. Agent가 필요한 정보를 필요할 때 찾을 수 있게 Repository를 legible하게 만드는 것이다.

Source: OpenAI, *Harness engineering: leveraging Codex in an agent-first world*.

---

## C05. GitHub Copilot Code Review — 더 좋은 Tool이 처음에는 더 나쁜 결과를 냈다

GitHub는 Copilot Code Review의 code exploration tool을 더 강한 공용 CLI 계열로 교체했지만 초기 offline benchmark에서 평균 비용이 늘고 유용한 review comment가 줄었다고 공개했다.

원인은 Tool 자체만이 아니었다. 기존 reviewer instruction과 탐색 workflow가 새 Tool의 사용 방식과 맞지 않았다. GitHub는 Tool, Instruction, Workflow를 함께 다시 조정했고 production에서 품질을 유지하면서 review cost를 낮췄다고 보고했다.

교훈은 단순하다. Harness의 한 부분을 개선했다고 end-to-end task quality가 자동으로 좋아지는 것은 아니다.

Source: GitHub, *Better tools made Copilot code review worse*.

---

## C06. Microsoft Building to the Test — Test를 통과했지만 요청한 구조는 아니었다

Microsoft Research의 2026년 preprint는 coding agent에게 강한 observable test signal을 제공했을 때 Agent가 요청된 reusable architecture보다 test가 직접 확인하는 behavior에 맞춘 구현을 만들 수 있음을 통제 실험으로 보여줬다.

Visible Test는 통과했다. 하지만 사용자가 원한 설계 Intent와는 어긋날 수 있었다.

이 연구는 Test를 약화시키라는 뜻이 아니다. Test가 확인하지 않는 구조적 Requirement까지 검증할 방법이 필요하다는 뜻이다.

**범위:** 두 production coding agent를 사용한 18회의 controlled run이며 prevalence를 일반화할 수 없다.

Source: Microsoft Research, *Building to the Test*.

---

## C07. METR Maintainer Review — Grader PASS와 Merge 판단은 다르다

METR는 SWE-bench Verified automated grader를 통과한 Patch를 실제 Maintainer에게 검토하게 했다. 4명의 Maintainer가 3개 Repository의 95개 Issue 범위를 살펴본 표본에서, Test를 통과한 AI Patch의 상당수가 실제 main에는 Merge되지 않았을 것으로 평가됐다.

Maintainer는 Test 외에도 Scope, Maintainability, Repository Convention, unintended behavior를 본다.

**범위:** Agent가 Review Feedback을 받고 다시 수정하지 않는 single-shot 평가라는 제한이 있다.

Source: METR, *Many SWE-bench-Passing PRs Would Not Be Merged into Main*.

---

## C08. Microsoft AgentLens — PASS만 보면 Lucky Pass를 놓친다

AgentLens는 Software Agent의 최종 결과뿐 아니라 작업 Trajectory를 분석한다. 연구진은 2,614개 OpenHands trajectory를 분석했고, process reference를 구성할 수 있었던 subset에서 Passing 결과 중 일부가 반복 Regression, Blind Retry, 검증 누락을 포함한 Lucky Pass로 분류됐다.

이 사례는 최종 Test PASS가 Process Quality를 모두 설명하지 않는다는 점을 보여준다.

**범위:** 보고된 10.7%는 분석 가능한 subset에서 나온 값이며 모든 coding-agent PASS의 일반 비율이 아니다.

Source: Microsoft Research, *AgentLens*.

---

## C09. Anthropic Multi-Agent Simulation — Agent를 늘리면 Coordination도 늘어난다

Anthropic은 2026년 여러 Agent가 동일한 software project를 장시간 공동 개발하는 controlled simulation을 공개했다. 일부 Model에서는 많은 Pull Request를 만들고도 Merge 비율이 낮거나 shared-file conflict 뒤 Work를 포기하는 패턴이 나타났다.

또 다른 experiment에서는 Agent들이 같은 queue를 과도하게 polling해 요청량을 폭증시키는 resource stampede도 관찰됐다.

반면 일부 최신 Model은 file ownership을 더 명확하게 나누며 충돌을 줄였다.

**범위:** 실제 enterprise Repository가 아니라 controlled simulation이다.

Source: Anthropic, *Patterns and problems in emerging multiagent systems*.

---

## C10. Microsoft와 METR — “AI 생산성” 숫자가 다른 이유

Microsoft Research의 2025년 field experiment는 4,867명의 개발자에서 AI Coding Assistant 접근군의 completed task 증가를 보고했다.

METR의 2025년 RCT는 숙련된 오픈소스 개발자 16명이 익숙한 Repository에서 실제 Task를 수행할 때 당시 AI 도구 사용군의 완료 시간이 오히려 늘었다고 보고했다.

두 결과는 모순이라기보다 measurement boundary가 다르다는 신호다.

Developer population, Task, Tool generation, Repository familiarity, productivity metric이 다르면 결과도 달라질 수 있다.

Sources: Microsoft Research, *The Effects of Generative AI on High-Skilled Work*; METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*.

---

## C11. NIST Agent Identity — 사람 계정을 Agent에게 빌려주는 문제

NIST NCCoE는 2026년 Software and AI Agent Identity and Authorization concept paper를 공개하며 Agent identification, authentication, authorization, auditing, non-repudiation 같은 문제를 공식적으로 다루기 시작했다.

이 책의 Task-scoped Agent Identity 모델은 이 방향과 맞닿아 있지만 NIST의 확정 표준은 아니다.

핵심 질문은 “Agent가 누구인가”보다 “누가 어떤 Task에 어떤 Capability를 위임했고, 어떤 행동을 했는지 추적할 수 있는가”다.

**상태:** Initial Public Draft / ongoing project.

Source: NIST NCCoE, *Software and AI Agent Identity and Authorization*.

---

## C12. Durable Runtime — Memory보다 Execution History

Microsoft Durable Task와 Google Agent Executor는 구현 방식은 다르지만 long-running Agent Work에서 execution history, retry, wait, resume를 별도 reliability layer로 다룬다는 공통점이 있다.

Google은 Agent Executor를 event log와 snapshot을 사용해 outage나 Human-in-the-loop 이후 execution을 재개하는 runtime으로 설명했고, Microsoft는 Durable Task 기반으로 Agent workflow를 장시간 유지하는 패턴을 제공한다.

이 사례들의 핵심은 “더 긴 Context Window”가 아니다. Agent Memory와 execution durability를 다른 문제로 본다는 점이다.

Sources: Microsoft Durable Task for AI Agents; Google Cloud Agent Executor.

---

## C13. Google Jules — Proactive Work와 Auto-merge는 다르다

Google은 Jules에 Suggested Tasks와 Scheduled Tasks 같은 proactive work 기능을 공개했다. Suggested Tasks는 Repository 개선 후보를 찾아 사용자에게 제시하고, deployment-failure 연동에서도 Agent가 Fix를 만든 뒤 Pull Request를 열어 Review할 수 있게 하는 흐름을 보여줬다.

이 사례는 Event가 Work를 시작하는 것과 결과를 자동으로 Acceptance/Merge하는 것이 별개의 Decision이라는 점을 보여준다.

Source: Google, *Jules proactive updates*.

---

## C14. Runmesh Continuity Gap — Task는 살아남았지만 Work는 재사용되지 않았다

자체 구현 Runmesh의 한 live continuity experiment에서는 Worker runtime loss 이후 Task가 사람 개입과 retry 소비 없이 최종 완료됐다. Durable Task와 Reassignment 자체는 동작했다.

하지만 Worker B는 Worker A가 이미 수행한 유효한 미commit 변경을 이어받지 못해 처음부터 다시 작업했다. Carryover에는 interruption reason만 남았고 partial workspace state가 전달되지 않았다.

이 사례는 Durable Task State만으로 Continuity가 완성되지 않는다는 점을 보여준다.

> Worker 교체 시 유효한 partial work까지 전달하려면 Commit, Patch, Snapshot 같은 durable workspace checkpoint가 필요하다.

**주의:** 자체 구현 Case Study이며 일반 산업 통계가 아니다.
