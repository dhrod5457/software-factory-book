# 01장 설계 - Coding Agent가 좋아진 뒤 무엇이 병목이 되는가

## 장의 목표

이 장은 책의 출발점이다. Coding Agent의 코드 생성 능력이 향상된 뒤에도 전체 Software Delivery가 자동으로 빨라지지 않는 이유를 보여준다. 문제를 모델 성능이 아니라 시스템의 흐름, Human Attention, Review/CI/Integration 병목으로 확장한다.

이 장의 핵심 질문:

> Agent가 코드를 잘 쓰는데 왜 별도의 Software Factory가 필요한가?

> 개인 Agent 생산성과 조직 Delivery 생산성은 왜 다른가?

---

## 핵심 주장

> Coding speed의 개선은 Delivery System의 병목을 다음 단계로 이동시킬 수 있다.

> Factory의 목적은 Agent를 많이 실행하는 것이 아니라 검증된 변경이 사용자에게 도달하는 전체 흐름을 개선하는 것이다.

---

## 독자가 얻는 것

- Model Capability와 Factory Capability를 구분할 수 있다.
- Agent execution time, developer blocking time, cycle time을 구분할 수 있다.
- Review/CI/Integration이 새로운 병목이 될 수 있음을 설명할 수 있다.
- AI 생산성 연구의 상반된 결과를 동일한 숫자로 일반화하지 않을 수 있다.

---

## 반드시 사용할 Research

- `research/01-ai-software-factory-landscape-2026.md`
- `research/07-observability-metrics-and-economics.md`
- `research/16-productivity-evidence-and-measurement.md`
- `research/17-review-integration-and-throughput-bottlenecks.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- METR 2025 숙련 OSS 개발자 RCT의 slowdown 결과
- Microsoft field experiment의 task completion 증가 결과
- Agent throughput 증가가 review queue를 키울 수 있다는 반례
- Benchmark score를 실제 조직 생산성과 동일시하는 오류

---

# 절 구성

## 01.1 Coding Assistant에서 Coding Agent로

응답 생성에서 Repository를 탐색하고 Tool을 실행해 실제 변경을 만드는 주체로 역할이 바뀐 과정을 짧게 설명한다. 특정 제품의 역사를 나열하지 않는다.

## 01.2 코드 생성 속도와 Delivery 속도는 다르다

Implementation만 빨라져도 Review, CI, Integration, Deployment가 그대로면 end-to-end throughput이 제한된다는 흐름을 설명한다.

## 01.3 Human Attention이 새로운 Capacity가 된다

개발자가 여러 Agent session을 직접 관리하면 context switching과 review attention이 병목이 될 수 있음을 설명한다.

## 01.4 생산성 연구가 서로 다른 이유

Task 유형, 개발자 숙련도, 도구 세대, 측정 boundary가 다르면 상반된 결과가 나올 수 있음을 Microsoft/METR/DORA 자료로 보여준다.

## 01.5 최적화 단위를 바꾼다

Token, Agent count, LOC, PR count보다 Accepted Change, cycle time, human intervention을 더 중요한 후보 지표로 제시한다.


---

## 필요한 구조 / 그림

1. Coding throughput 증가 후 병목이 Review → CI → Integration으로 이동하는 흐름
2. Model Capability → Agent Capability → Factory Capability의 계층
3. Agent Execution Time / Human Blocking Time / End-to-End Cycle Time 비교

---

## 실전 예제 / 실험

- 하나의 Agent가 PR 1개를 만들던 팀이 10개 Agent로 하루 PR 30개를 만들지만 reviewer는 2명인 상황
- Build 5분, Agent 수정 3분, Review 대기 2일인 Task의 병목 분석

---

## 본문에서 의도적으로 다루지 않을 내용

- Factory architecture 세부 구조
- Durable Task 스키마
- 특정 모델/제품 benchmark 순위
- AI가 개발자를 대체하는 미래 예측

---

## 앞뒤 장 연결

2장에서는 이 문제를 해결하기 위해 책에서 말하는 AI Software Factory가 무엇인지 최소 정의와 경계를 제시한다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
