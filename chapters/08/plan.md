# 08장 설계 - Worker, Sandbox, Workspace

## 장의 목표

Agent가 실제 코드를 바꾸고 명령을 실행하는 환경을 설계한다. Isolation, reproducibility, cold start, persistence, cache 사이의 trade-off를 다룬다.

이 장의 핵심 질문:

> 좋은 Factory Worker는 어떤 상태를 가져야 하는가?

> Ephemeral Worker와 Persistent Worker를 언제 선택할 것인가?

---

## 핵심 주장

> Autonomy가 높아질수록 Worker isolation과 reproducibility가 중요해진다.

> Cache와 durable work state를 혼동하지 말고, 재사용 가능한 환경과 항상 fresh해야 하는 Task state를 분리해야 한다.

---

## 독자가 얻는 것

- Workspace isolation 전략을 비교할 수 있다.
- Ephemeral/Persistent worker trade-off를 설명할 수 있다.
- Prepared environment와 cache를 안전하게 사용할 수 있다.
- Worker profile을 Task capability와 연결할 수 있다.

---

## 반드시 사용할 Research

- `research/02-factory-architecture-patterns.md`
- `research/06-security-isolation-and-permissions.md`
- `research/20-durable-execution-and-workflow-reliability.md`
- `research/21-agent-ready-developer-platform-and-catalog.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- 모든 Agent가 같은 mutable workspace를 공유하는 구조
- 환경 setup을 매 Task Agent가 처음부터 수행하는 구조
- Persistent Worker의 warm state를 authoritative task state로 오해하는 방식

---

# 절 구성

## 08.1 Workspace Isolation

branch/worktree, independent clone, container, VM의 역할을 비교하고 무엇을 격리해야 하는지 설명한다.

## 08.2 Prepared Environment

JDK/Node/browser/build tools와 dependency cache를 미리 준비해 Agent startup을 줄이는 방법을 설명한다.

## 08.3 Fresh State와 Cache

Runtime/tool/cache는 재사용할 수 있지만 source revision, Task, test result, temp data는 fresh해야 한다는 경계를 제시한다.

## 08.4 Ephemeral vs Persistent Worker

clean reproducibility와 warm continuity의 trade-off를 설명하고 task/environment 특성에 따라 선택하도록 한다.

## 08.5 Worker Profile

backend, browser-e2e, GPU, internal-network 등 capability profile을 scheduler와 연결하는 개념을 제시한다.


---

## 필요한 구조 / 그림

1. Worker = Workspace + Runtime + Tools 구조
2. Ephemeral vs Persistent Worker 비교표
3. Prepared Environment + Fresh Task State 분리 그림

---

## 실전 예제 / 실험

- Java backend worker와 Playwright E2E worker profile 비교
- Persistent browser worker에서 stale cache 때문에 잘못된 PASS가 난 상황

---

## 본문에서 의도적으로 다루지 않을 내용

- Docker/Kubernetes 입문
- cloud vendor VM 상품 비교
- container runtime internals

---

## 앞뒤 장 연결

9장에서는 같은 Worker 안에서 Agent가 성공하도록 만드는 Harness Engineering을 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
