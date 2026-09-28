# 13장 설계 - Evidence Contract: 완료를 설명하지 말고 증명한다

## 장의 목표

Verification 결과를 사람이 빠르게 판단하고 시스템이 추적할 수 있는 표준 결과물로 만드는 방법을 정의한다. 자연어 완료 보고를 Commit, Test Result, Screenshot, Log/Trace, Risk 같은 Evidence 묶음으로 바꾼다.

이 장의 핵심 질문:

> Agent 결과를 어떤 형식으로 받아야 빠르게 Review할 수 있는가?

> Evidence와 Provenance는 어떻게 다른가?

---

## 핵심 주장

> Agent의 자연어 완료 보고보다 재현 가능하고 검증 가능한 Artifact가 우선되어야 한다.

> Evidence Contract를 표준화하면 Review startup cost와 자동화된 acceptance 판단을 줄일 수 있다.

> Evidence는 ‘맞다’의 근거이고 Provenance는 ‘어떻게 만들어졌는가’의 계보다.

---

## 독자가 얻는 것

- Task Result Contract를 설계할 수 있다.
- Commit/Test/Screenshot/Log를 하나의 Evidence Package로 묶을 수 있다.
- Evidence와 Provenance를 구분할 수 있다.
- UI/Runtime 작업에서 Demos over Diffs를 적절히 사용할 수 있다.

---

## 반드시 사용할 Research

- `research/05-verification-evidence-and-human-gates.md`
- `research/15-governance-provenance-and-agent-identity.md`
- `research/17-review-integration-and-throughput-bottlenecks.md`
- `research/29-academic-synthesis-design-principles.md`

연구 자료는 제품/논문 소개 자체가 아니라 이 장의 설계 판단을 뒷받침하거나 반례를 제시하는 용도로 사용한다.

---

## 반드시 다룰 반례 / 주의점

- ‘완료했습니다’ 같은 자연어 summary만 반환하는 방식
- Evidence artifact가 다른 commit SHA를 가리키는 inconsistency
- Screenshot만 보고 코드/보안 검증을 생략하는 과잉 Demos over Diffs

---

# 절 구성

## 13.1 Result Contract가 필요한 이유

Agent마다 결과 보고 형식이 다르면 review와 downstream automation이 어려워지는 문제를 설명한다.

## 13.2 Evidence 최소 필드

Task ID, base/result revision, changed files, exact commands, verification result, artifact reference, known limitation, remaining risk를 제안한다.

## 13.3 Behavioral Evidence

UI screenshot/video, API response, service boot, runtime logs처럼 diff만으로 알 수 없는 결과를 포함하는 이유를 설명한다.

## 13.4 Evidence와 Provenance

Test PASS와 artifact lineage를 구분하고 model/harness/sandbox/approval metadata를 어디까지 추적할지 설명한다.

## 13.5 Evidence Manifest

machine-readable result.json 형태를 예시로 제시하고 human-readable summary와 연결한다.

## 13.6 Review Startup Cost 줄이기

Reviewer가 처음부터 repository를 재현하지 않고도 scope/risk/result를 판단할 수 있게 Evidence Package를 구성한다.


---

## 필요한 구조 / 그림

1. Task→Verification→Evidence Package→Review sequence
2. Evidence vs Provenance 비교
3. result.json + artifact tree 예시

---

## 실전 예제 / 실험

- UI 변경에 before/after screenshot+E2E trace+commit을 반환
- Performance fix에 benchmark before/after와 environment metadata를 포함

---

## 본문에서 의도적으로 다루지 않을 내용

- Artifact storage product 비교
- SBOM/attestation 표준 상세
- Human approval policy 전체

---

## 앞뒤 장 연결

14장에서는 Evidence가 실패를 보여주었을 때 Task를 어떻게 retry/resume/reassign할지 다룬다.

---

## Draft 완료 기준

- 장의 첫 질문에 본문이 명확히 답한다.
- 최소 2개 이상의 독립된 Research 근거를 사용한다.
- 성공 사례뿐 아니라 실패/반례를 포함한다.
- 제품 기능 설명보다 오래 유지되는 설계 원칙을 먼저 제시한다.
- 다음 장에서 다시 설명할 내용을 중복해서 깊게 다루지 않는다.
