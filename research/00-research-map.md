# Software Factory Book - Research Map

기준일: 2026-09-28

이 저장소는 현재 **자료 수집 단계**다.

참고 프로젝트 `cloud-agent-book`의 작업 방식을 따라, 본문을 먼저 쓰지 않고 다음 순서로 진행한다.

```text
research
→ concept
→ scope
→ toc
→ chapter plan
→ draft
→ review
→ manuscript
```

현재 단계에서는 Software Factory의 정의를 하나로 고정하지 않는다. 역사적 Software Factory와 2025~2026년의 agent-native Software Factory를 분리해서 근거를 수집한 뒤, 공통점과 차이를 비교해 책의 정의를 만든다.

## 조사 축

### A. 역사와 원형

확인할 질문:

- Software Factory라는 표현은 언제 등장했는가?
- 1960~1990년대 Software Factory는 무엇을 자동화하려 했는가?
- Hitachi, SDC, Toshiba, NEC, Fujitsu 사례의 공통점은 무엇인가?
- 표준화, 재사용, 프로세스, 품질관리, 도구화가 어떤 역할을 했는가?
- 제조업 비유가 실제 소프트웨어 개발에서 어디까지 유효했는가?

우선 자료:

- Michael A. Cusumano, *Japan's Software Factories: A Challenge to U.S. Management* (1991)
- Michael A. Cusumano, *The Software Factory: A Historical Interpretation* (IEEE Software, 1989)
- Yoshihiro Matsumoto, *Notes on the Next Generation Software Factory* (1992)
- Hitachi corporate history / annual report
- Harvey Bratman, Terry Court, *The Software Factory* (IEEE Computer, 1975)

### B. 2000년대 Software Factories

확인할 질문:

- Software Product Line, DSL, Model Driven Development, code generation은 Software Factory 개념을 어떻게 바꾸었는가?
- 2004년 Microsoft/Wiley 계열의 Software Factories 방법론은 일본식 factory와 무엇이 같고 다른가?

우선 자료:

- Jack Greenfield, Keith Short, Steve Cook, Stuart Kent, *Software Factories: Assembling Applications with Patterns, Models, Frameworks, and Tools* (2004)

### C. DevOps / Continuous Delivery / Platform Engineering

확인할 질문:

- CI/CD, Infrastructure as Code, self-service, paved road, Internal Developer Platform은 현대 Software Factory의 어떤 기반을 제공하는가?
- 개발자 개인의 생산성보다 시스템 수준의 flow를 어떻게 측정해야 하는가?
- 자동화가 많아질수록 품질·거버넌스·관측성은 어떻게 포함되어야 하는가?

우선 자료:

- DORA research
- CNCF Platform Engineering / Platform Maturity Model
- Continuous Delivery / Accelerate 계열 연구와 실무 자료

### D. Coding Agent에서 Agentic Software Factory로

확인할 질문:

- 단일 coding agent와 software factory의 경계는 무엇인가?
- Task queue, orchestrator, workspace isolation, sandbox, retries, approvals, evidence가 왜 필요한가?
- 사람이 코드를 쓰지 않는 것과 사람이 검증을 포기하는 것은 같은 말인가?
- interactive agent에서 background / event-driven / fleet model로 넘어갈 때 병목은 무엇인가?

우선 사례:

- StrongDM Software Factory
- Stripe Minions
- WorkOS Horizon
- OpenAI Symphony / Codex orchestration
- OpenHands

### E. Harness / Context / Verification

확인할 질문:

- 모델 성능보다 harness가 중요한 구간은 어디인가?
- Repository instructions, skills, tools, MCP, sandbox, environment preparation은 어떤 역할을 하는가?
- deterministic check와 LLM judge를 어떻게 나누는가?
- retry loop는 언제 도움이 되고 언제 오류를 증폭하는가?
- 사람이 개입해야 하는 approval boundary는 어디인가?

### F. 평가와 한계

확인할 질문:

- SWE-bench류 benchmark가 실제 Software Factory 성능을 얼마나 설명하는가?
- benchmark contamination과 saturation 문제는 무엇인가?
- long-horizon task capability를 어떻게 측정할 것인가?
- PR 수, token 사용량, cycle time, acceptance rate, escaped defect 중 무엇을 봐야 하는가?
- 공장 전체의 성능과 단일 모델 성능을 어떻게 분리해서 측정할 것인가?

우선 자료:

- SWE-bench / SWE-bench Pro
- METR time horizon research
- DORA AI-assisted software development research

## 출처 등급

### A - 1차 자료

가장 우선한다.

- 논문 원문
- 공식 기술 문서
- 실제 운영팀의 engineering blog
- 공식 specification
- 프로젝트 공식 repository

### B - 2차 분석

1차 자료를 해석하거나 비교할 때 사용한다.

- 신뢰할 수 있는 연구자/엔지니어의 분석
- 기술 서적
- 학회/산업 보고서

### C - 탐색 자료

새로운 사례나 키워드를 찾는 용도다.

- 개인 블로그
- 뉴스레터
- 커뮤니티 글
- curated list

C 등급만으로 본문 핵심 주장을 만들지 않는다.

## 현재 작성 원칙

- 최신 AI 제품의 가격, 모델명, 사용량 제한은 책의 핵심 정의와 분리한다.
- 회사가 주장하는 생산성 수치는 해당 회사의 관측값으로만 기록한다.
- benchmark 점수와 실제 조직 생산성을 동일시하지 않는다.
- "완전 자율", "dark factory", "human review 유지"를 서로 다른 운영 모델로 구분한다.
- 특정 제품 사용 설명서가 아니라 재사용 가능한 시스템 원리를 찾는다.
- 기존 Software Factory의 역사와 2026년 agent-native 의미가 연속적인지, 단지 이름만 재사용한 것인지도 검증 대상으로 남긴다.

## Research 파일

- `research/01-history-and-classic-software-factories.md`
- `research/02-platform-and-delivery-foundations.md`
- `research/03-agentic-software-factories-2026.md`
- `research/04-orchestration-verification-and-evaluation.md`

