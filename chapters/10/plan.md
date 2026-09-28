# 10장 설계 - Context Engineering과 Agent Legibility

## 장의 목표

Agent에게 많은 정보를 한 번에 넣는 대신 필요한 정보를 찾을 수 있는 Repository, Documentation, Catalog, Runtime 구조를 만든다.

이 장의 핵심 질문:

> Agent에게 얼마만큼의 Context를 줘야 하는가?

> Repository와 Application을 Agent-readable하게 만든다는 것은 무엇인가?

---

## 핵심 주장

> More Context는 Better Agent와 같지 않으며 relevant/minimal/progressive context가 중요하다.

> Agent가 읽을 수 없는 조직 지식과 runtime state는 사실상 존재하지 않는 것과 비슷하다.

> Context file은 중요한 artifact지만 mandatory policy enforcement를 대체하지 못한다.

---

## 독자가 얻는 것

- Progressive Context 구조를 설계할 수 있다.
- Repository map, architecture docs, software catalog의 역할을 구분할 수 있다.
- AGENTS.md를 최소 entry point로 설계할 수 있다.
- Runtime logs/metrics/traces를 Agent-readable하게 만드는 이유를 이해한다.

---

## 반드시 사용할 Research
- `research/30-workos-product-engineering-factory.md`

- `research/03-harness-context-and-agent-legibility.md`
- `research/21-agent-ready-developer-platform-and-catalog.md`
- `research/24-academic-foundations-of-agentic-software-engineering.md`
- `research/27-context-files-and-repository-governance-evidence.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- AGENTS.md에 모든 조직 지식을 넣는 방식
- Context file이 있으면 correctness가 자동 개선된다는 주장
- 외부 wiki/Slack에만 중요한 지식을 두는 구조
- Raw logs를 context window에 통째로 넣는 방식

---

# 절 구성

## 10.1 Context Window는 Storage가 아니다

일시적인 reasoning space와 durable organizational knowledge를 분리한다.

## 10.2 Repository Legibility

build/test entry point, architecture map, ownership, conventions을 Agent가 탐색 가능한 형태로 만든다.

## 10.3 Context File의 효과와 한계

Agent README empirical studies를 소개하고 과도한 instruction이 cost를 늘릴 수 있음을 설명한다.

## 10.4 Software Catalog와 Organization Context

service ownership, dependency, API, MCP/Skill metadata를 catalog에서 조회하는 구조를 다룬다.

## 10.5 Application Legibility

DOM, browser, logs, metrics, traces, deployment state도 code와 같은 context source임을 설명한다.

## 10.6 Progressive Disclosure

Entry → Map → Relevant Doc → Skill → Tool Result 순으로 Task-specific context package를 만드는 방식을 제시한다.


---

## 필요한 구조 / 그림

1. Progressive Context ladder
2. Repository / Catalog / Runtime three-source context model
3. AGENTS.md as entry point, not knowledge dump

---

## 실전 예제 / 실험

- Auth bug task에서 auth architecture doc와 target test만 단계적으로 조회
- service owner와 dependent API를 catalog lookup으로 찾는 예

---

## 본문에서 의도적으로 다루지 않을 내용

- RAG/vector DB 일반론
- Agent memory taxonomy
- 문서 작성법 전체

---

## 앞뒤 장 연결

11장에서는 Context가 충분히 준비된 뒤 어떤 decision을 system과 Agent가 각각 가져야 하는지 Controlled Autonomy를 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
