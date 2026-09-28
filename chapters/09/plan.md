# 09장 설계 - Harness Engineering: Agent가 일할 수 있는 환경 만들기

## 장의 목표

Model 성능과 별개로 Agent의 행동을 결정하는 instructions, tools, skills, search, browser, result filtering 같은 Harness를 하나의 engineering layer로 설명한다.

이 장의 핵심 질문:

> 같은 모델인데 왜 Harness에 따라 결과가 크게 달라지는가?

> Agent에게 Tool을 많이 주는 것이 항상 좋은가?

---

## 핵심 주장

> Model을 바꾸지 않고도 Harness 개선으로 Agent 성능과 reliability를 높일 수 있다.

> Tool은 사람용 UI가 아니라 Agent가 호출하는 API이므로 output shape와 feedback semantics가 중요하다.

---

## 독자가 얻는 것

- Harness의 구성요소를 설명할 수 있다.
- Instruction, Skill, Tool, MCP의 역할을 구분할 수 있다.
- Tool output과 feedback을 Agent-friendly하게 설계할 수 있다.
- Model 문제와 Harness 문제를 분리해 진단할 수 있다.

---

## 반드시 사용할 Research

- `research/03-harness-context-and-agent-legibility.md`
- `research/24-academic-foundations-of-agentic-software-engineering.md`
- `research/27-context-files-and-repository-governance-evidence.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- 더 좋은 모델이면 Harness가 필요 없다는 주장
- 모든 기능을 하나의 거대한 prompt에 넣는 방식
- Tool 수를 늘리면 자동으로 능력이 늘어난다는 가정
- Tool upgrade 후 오히려 성능이 악화된 GitHub 사례

---

# 절 구성

## 09.1 Harness란 무엇인가

Model 주변의 instruction, context, tools, execution, feedback, verification 구조로 정의한다.

## 09.2 Agent-Computer Interface

SWE-agent ACI 연구를 통해 file viewer, edit feedback, command output가 성능 변수임을 설명한다.

## 09.3 Instruction / Skill / Tool / MCP

Guidance, reusable procedure, external capability의 책임을 나누고 deterministic enforcement와 구분한다.

## 09.4 Tool Output Design

긴 raw output보다 summary/index/artifact reference/progressive retrieval이 유리한 이유를 설명한다.

## 09.5 Harness Regression

Tool 변경이 기존 instruction/workflow와 맞지 않으면 성능이 떨어질 수 있으므로 harness 자체를 eval해야 함을 설명한다.

## 09.6 Prepared Harness

Task type에 맞는 worker profile, tool set, skill set을 미리 조립하는 방식을 소개한다.


---

## 필요한 구조 / 그림

1. Model surrounded by Harness components
2. Instruction/Skill/Tool/Policy responsibility map
3. Raw output vs Result Gateway pattern

---

## 실전 예제 / 실험

- 10MB test log 대신 failed-test index와 artifact URI만 Agent에게 전달
- 동일 모델에 다른 file-edit interface를 제공했을 때 작업 경로가 달라지는 예

---

## 본문에서 의도적으로 다루지 않을 내용

- MCP protocol 세부 사양
- Agent framework 비교
- Prompt engineering 입문

---

## 앞뒤 장 연결

10장에서는 Harness에 들어가는 Context를 얼마나, 어떤 순서로 제공해야 하는지 깊게 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
