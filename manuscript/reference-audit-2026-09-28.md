# Reference Audit — 2026-09-28

대상:

- `manuscript/references.md`
- 고유 URL 53개

## 결과

**PASS**

- Direct open success: 51
- Direct open tool error: 2
- Independently verified after tool error: 2
- Confirmed dead link: 0

## Direct-open 예외

### 1. ACM DOI

Reference:

`https://doi.org/10.1145/3805760.3814891`

웹 도구의 direct open은 실패했다.

별도 검증:

- AIware 2026 공식 paper page에서 동일 제목과 DOI 확인
- DBLP AIware 2026 proceedings에서 논문 확인

판정:

**VALID — KEEP DOI**

추가 확인된 상태:

- AIware 2026 Main Track conference paper
- pages 43–50

### 2. Google Agent Executor

Reference:

`https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime`

웹 도구의 direct open에서 internal error가 발생했다.

별도 검색 결과:

- Google Cloud Blog의 동일 URL/제목 확인
- 2026-05-20 공개
- Agent Executor 설명 페이지가 현재 검색됨

판정:

**VALID — KEEP URL**

## Current-state 변경 확인

### Factory.ai

기존 `factory.ai/news/factory-signals` URL은 현재 `factory.com/news/factory-signals`로 redirect된다.

기존 URL은 redirect가 정상 동작하므로 책에서는 현재 Reference를 유지할 수 있다.

향후 최종 URL canonicalization 시 `factory.com`으로 교체 가능.

### Other references

다음 도메인의 Reference가 현재 접근 가능함을 확인했다.

- Anthropic
- Backstage
- CNCF
- Cursor
- DORA
- GitHub / GitHub Docs
- Google / Jules
- Kiro
- METR
- Microsoft Research / Security / Learn
- NIST / NCCoE
- OpenAI
- OpenHands GitHub
- arXiv
- SWE-agent
- Temporal
- WorkOS

## Academic Publication Status Notes

2026-09-28 기준:

- Deterministic vs LLM-Controlled Orchestration: AIware 2026 conference paper
- Runtime-Structured Task Decomposition: arXiv + Agentic Software Engineering workshop presentation
- Wink: arXiv
- Building to the Test: Microsoft Research page still labels Preprint
- AgentLens: Microsoft Research lists ArXiv publication
- REAgent: arXiv
- SWE-Explore: arXiv

본문에서는 peer-reviewed 여부를 과장하지 않는다.

## Release Gate

53개 Reference의 link survival check:

**PASS**

출판 형식 metadata 정규화는 별도 bibliography formatting 작업으로 남긴다.
