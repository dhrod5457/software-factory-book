# Case Study Boxes

기준일: 2026-09-28

`manuscript/book.md`의 C01~C14, C16 marker에 대응하는 working box copy다.

제품/연구 사례는 일반 원칙의 예시로 사용하며, 회사 내부 수치나 controlled experiment를 업계 일반 사실로 확장하지 않는다.

---

## C01. OpenAI Symphony — Session보다 Task를 관리한다

OpenAI는 2026년 Symphony를 공개하며 내부 경험상 한 엔지니어가 대화형 코딩 에이전트 세션을 여러 개 직접 관리할 때 작업을 오가며 맥락을 다시 파악하는 일이 빠르게 부담이 된다고 설명했다. 공개 글에서는 대체로 3~5개 세션 이후 관리 부담이 눈에 띄었다고 한다. Symphony가 흥미로운 이유는 숫자 자체가 아니다. 해결 방향이 “더 많은 터미널”이 아니라 이슈와 작업을 중심으로 에이전트 작업을 실행 조율하는 구조였다는 점이다.

**읽을 때 주의:** 3~5라는 숫자는 OpenAI 내부 운영 사례이며 인간이 관리할 수 있는 에이전트 수의 보편적 한계가 아니다.

소스: OpenAI, *An open-source spec for Codex orchestration: Symphony*.

---

## C02. WorkOS Horizon — Durable State와 Disposable Execution

WorkOS의 Horizon은 소프트웨어 작업을 중단돼도 기록이 남는 제어 상태로 관리하고 실제 실행은 격리 환경에서 수행하는 구조를 공개했다. 이 사례가 보여주는 핵심은 “어떤 에이전트를 썼는가”보다 작업 상태와 실행 환경을 분리했다는 점이다. 격리 환경이 사라져도 작업 자체가 사라지지 않아야 재시도와 다른 워커에 재배정이 가능해진다.

**읽을 때 주의:** Horizon의 구체 설계 구조가 모든 생산 시스템의 정답이라는 뜻은 아니다.

소스: WorkOS, *The self-driving codebase: Building Horizon at WorkOS*.

---

## C03. Anthropic Managed Agents — Brain과 Hands를 분리한다

Anthropic은 Managed Agents 설계 구조에서 세션, 하네스, 격리 환경을 분리해 설명한다. 세션은 에이전트 상호작용 상태, 하네스는 모델 순환과 도구·맥락 정보 실행 조율, 격리 환경은 실제 연산 자원과 파일 시스템을 담당한다. 이 구분은 “에이전트”라는 한 단어 안에 모델, 제어 로직, 연산 자원을 모두 넣지 않게 해준다. 각 계층의 실패와 생애주기를 따로 설계할 수 있기 때문이다.

소스: Anthropic, *Scaling Managed Agents: Decoupling the brain from the hands*.

---

## C04. OpenAI Harness Engineering — 거대한 AGENTS.md가 실패한 이유

OpenAI의 하네스 설계 사례에서는 모든 지식을 하나의 거대한 AGENTS.md에 넣는 접근이 잘 작동하지 않았다고 설명한다. 맥락 정보를 많이 차지했고, 모든 규칙이 같은 중요도로 보였으며, 문서가 빠르게 낡아졌다. 해당 팀은 대신 짧은 AGENTS.md를 저장소 지식의 목차처럼 사용하고 상세한 설계 구조와 운영 지식은 구조화된 문서로 분리했다. 교훈은 “맥락 정보를 더 많이 넣어라”가 아니다.

에이전트가 필요한 정보를 필요할 때 찾을 수 있게 저장소를 읽고 이해하기 쉽게 만드는 것이다. 소스: OpenAI, *Harness engineering: leveraging Codex in an agent-first world*.

---

## C05. GitHub Copilot Code Review — 더 좋은 Tool이 처음에는 더 나쁜 결과를 냈다

GitHub는 Copilot Code Review의 코드 탐색 도구를 더 강한 공용 CLI 계열로 교체했지만 초기 오프라인 성능 평가에서 평균 비용이 늘고 유용한 검토 의견이 줄었다고 공개했다. 원인은 도구 자체만이 아니었다. 기존 검토자 지시사항과 탐색 작업 흐름이 새 도구의 사용 방식과 맞지 않았다. GitHub는 도구, 지시사항, 작업 흐름을 함께 다시 조정했고 운영 환경에서 품질을 유지하면서 검토 비용을 낮췄다고 보고했다. 교훈은 단순하다. 하네스의 한 부분을 개선했다고 전체 과정 작업 품질이 자동으로 좋아지는 것은 아니다.

소스: GitHub, *Better tools made Copilot code review worse*.

---

## C06. Microsoft Building to the Test — Test를 통과했지만 요청한 구조는 아니었다

Microsoft Research의 2026년 동료 심사 전 논문은 coding 에이전트에게 강한 observable 테스트 신호를 제공했을 때 에이전트가 요청된 reusable 설계 구조보다 테스트가 직접 확인하는 동작에 맞춘 구현을 만들 수 있음을 통제 실험으로 보여줬다. 공개된 테스트는 통과했다. 하지만 사용자가 원한 설계 의도와는 어긋날 수 있었다. 이 연구는 테스트를 약화시키라는 뜻이 아니다. 테스트가 확인하지 않는 구조적 요구사항까지 검증할 방법이 필요하다는 뜻이다.

**범위:** 실제 운영되는 코딩 에이전트 두 개를 사용한 18회의 조건을 통제한 실행이며 발생 빈도를 일반화할 수 없다.

소스: Microsoft Research, *Building to the Test*.

---

## C07. METR Maintainer Review — Grader PASS와 Merge 판단은 다르다

METR는 SWE-bench Verified 자동화된 채점기를 통과한 패치를 실제 유지보수 담당자에게 검토하게 했다. 4명의 유지보수 담당자가 3개 저장소의 95개 이슈 범위를 살펴본 표본에서, 테스트를 통과한 AI 패치의 상당수가 실제 main에는 병합되지 않았을 것으로 평가됐다. 유지보수 담당자는 테스트 외에도 범위, 유지보수 용이성, 저장소 규칙, unintended 동작을 본다.

**범위:** 에이전트가 검토 피드백을 받고 다시 수정하지 않는 한 번의 실행으로만 평가했다는 제한이 있다.

소스: METR, *Many SWE-bench-Passing PRs Would Not Be Merged into Main*.

---

## C08. Microsoft AgentLens — PASS만 보면 Lucky Pass를 놓친다

AgentLens는 소프트웨어 에이전트의 최종 결과뿐 아니라 작업 실행 경로를 분석한다. 연구진은 2,614개 OpenHands 실행 경로를 분석했고, 과정 비교 기준을 구성할 수 있었던 subset에서 Passing 결과 중 일부가 반복적인 기존 기능의 오류, 원인 확인 없는 재시도, 검증 누락을 포함한 우연한 통과로 분류됐다. 이 사례는 최종 테스트 PASS가 과정 품질을 모두 설명하지 않는다는 점을 보여준다.

**범위:** 보고된 10.7%는 분석 가능한 subset에서 나온 값이며 모든 코딩 에이전트 PASS의 일반 비율이 아니다.

소스: Microsoft Research, *AgentLens*.

---

## C09. Anthropic Multi-Agent Simulation — Agent를 늘리면 Coordination도 늘어난다

Anthropic은 2026년 여러 에이전트가 동일한 소프트웨어 프로젝트를 장시간 공동 개발하는 조건을 통제한 시뮬레이션을 공개했다. 일부 모델에서는 많은 변경 검토 요청을 만들고도 병합 비율이 낮거나 shared-file 충돌 뒤 작업을 포기하는 패턴이 나타났다. 또 다른 experiment에서는 에이전트들이 같은 대기열을 과도하게 polling해 요청량을 폭증시키는 자원 stampede도 관찰됐다. 반면 일부 최신 모델은 파일 담당 관계를 더 명확하게 나누며 충돌을 줄였다.

**범위:** 실제 enterprise 저장소가 아니라 조건을 통제한 시뮬레이션이다.

소스: Anthropic, *Patterns and problems in emerging multiagent systems*.

---

## C10. Microsoft와 METR — “AI 생산성” 숫자가 다른 이유

Microsoft Research의 2025년 field experiment는 4,867명의 개발자에서 AI 코딩 도우미를 사용할 수 있었던 집단의 완료한 작업 증가를 보고했다. METR의 2025년 RCT는 숙련된 오픈소스 개발자 16명이 익숙한 저장소에서 실제 작업을 수행할 때 당시 AI 도구 사용군의 완료 시간이 오히려 늘었다고 보고했다. 두 결과는 모순이라기보다 측정 경계가 다르다는 신호다. 개발자 population, 작업, 도구 generation, 저장소에 익숙한 정도, productivity 지표가 다르면 결과도 달라질 수 있다.

Sources: Microsoft Research, *The Effects of Generative AI on High-Skilled Work*; METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*.

---

## C11. NIST Agent Identity — 사람 계정을 Agent에게 빌려주는 문제

NIST NCCoE는 2026년 2월 소프트웨어 and AI 에이전트 신원 and 권한 부여 개념 문서 초안을 공개했고, 이후 이 논의를 정식 NCCoE 프로젝트로 이어가고 있다. 에이전트 신원 확인, authentication, 권한 부여, 감사, 수행 사실을 부인하지 못하게 하는 장치 같은 문제가 주요 범위다. 이 책의 Task-scoped 에이전트 신원 모델은 이 방향과 맞닿아 있지만 NIST의 확정 표준은 아니다. 핵심 질문은 “에이전트가 누구인가”보다 “누가 어떤 작업에 어떤 실행 권한을 위임했고, 어떤 행동을 했는지 추적할 수 있는가”다.

**상태:** 개념 문서 초안 + ongoing NCCoE 프로젝트.

소스: NIST NCCoE, *Software and AI Agent Identity and Authorization*.

---

## C12. Durable Runtime — Memory보다 Execution History

Microsoft Durable Task와 Google Agent Executor는 구현 방식은 다르지만 장시간 실행하는 에이전트 작업에서 실행 이력, 재시도, 대기, 중단 지점부터 재개를 별도 신뢰성 계층으로 다룬다는 공통점이 있다.

Google은 Agent Executor를 이벤트 기록과 스냅샷을 사용해 서비스 중단나 사람이 판단에 참여하는 방식 이후 실행을 재개하는 실행 기반으로 설명했고, Microsoft는 지속 작업 기반으로 에이전트 작업 흐름을 장시간 유지하는 패턴을 제공한다. 이 사례들의 핵심은 “더 긴 컨텍스트 창”가 아니다. 에이전트 메모리와 실행 durability를 다른 문제로 본다는 점이다.

Sources: Microsoft Durable Task for AI Agents; Google Cloud Agent Executor.

---

## C13. Google Jules — Proactive Work와 Auto-merge는 다르다

Google은 Jules에 Suggested Tasks와 Scheduled Tasks 같은 proactive 작업 기능을 공개했다. Suggested Tasks는 저장소 개선 후보를 찾아 사용자에게 제시하고, deployment-failure 연동에서도 에이전트가 수정을 만든 뒤 변경 검토 요청을 열어 검토할 수 있게 하는 흐름을 보여줬다. 이 사례는 이벤트가 작업을 시작하는 것과 결과를 자동으로 Acceptance/Merge하는 것이 별개의 결정이라는 점을 보여준다. 소스: Google, *Jules proactive updates*.

---

## C14. Runmesh Continuity Gap — Task는 살아남았지만 Work는 재사용되지 않았다

자체 구현 Runmesh의 한 live 연속성 experiment에서는 워커 실행 기반 loss 이후 작업이 사람 개입과 재시도 소비 없이 최종 완료됐다. 지속 작업과 다른 워커에 재배정 자체는 동작했다. 하지만 워커 B는 워커 A가 이미 수행한 유효한 미커밋 변경을 이어받지 못해 처음부터 다시 작업했다. 인계 정보에는 interruption 이유만 남았고 부분 작업 공간 상태가 전달되지 않았다. 이 사례는 지속 작업 상태만으로 연속성이 완성되지 않는다는 점을 보여준다.

> 워커 교체 시 유효한 부분 작업까지 전달하려면 커밋, 패치, 스냅샷 같은 중단 뒤에도 유지되는 작업 공간 복구 지점이 필요하다.

**주의:** 자체 구현 사례 연구이며 일반 산업 통계가 아니다.


---

## C16. WorkOS — PR Factory에서 Product Engineering Factory로

WorkOS의 Ryan Cooke는 격리 환경에 코딩 에이전트를 넣고 지시문으로 변경 검토 요청을 만드는 구조만으로는 조직의 소프트웨어 전달 성과가 크게 달라지지 않을 수 있다고 설명했다. WorkOS는 이후 자동화 범위를 코드 생성에서 제품 개발 과정으로 넓혔다. 예를 들어 제품 간략한 설명에서 PRD 성격의 산출물 초안을 만들고, 사람이 범위를 보정한 뒤 작업으로 분해한다. Linear 작업 티켓이 끝나면 의존 관계에 따라 다음 작업을 진행할 뿐 아니라 현재 계획을 다시 평가해 빠진 작업이 생겼는지도 확인한다.

또한 내부 MCP 연결 관문을 Context Engine으로 사용해 도구만 노출하는 것이 아니라 조직의 데이터 semantics와 자원 discovery guidance를 에이전트에게 제공한다. 이 사례가 보여주는 핵심은 다음과 같다.

> PR 생성은 생산 시스템의 출력일 수 있지만 생산 시스템 전체는 아니다. 제품 개발 과정과 피드백 순환까지 연결될 때 소프트웨어 생산 시스템의 시스템적 차이가 커진다.

**읽을 때 주의:** 발표 후반의 메모리 계층과 일부 자체 개선 기능은 향후 방향으로 설명된 부분이다. 또한 발표자는 에이전트 권한 부여를 아직 충분히 해결하지 못한 문제로 언급한다.

소스: Ryan Cooke, WorkOS, *No, That's Not a Software Factory*, conference talk 대화 기록.
