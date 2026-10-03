# 13장. Evidence Contract: 완료를 설명하지 말고 증명한다

검증이 끝났다고 검토가 자동으로 쉬워지는 것은 아니다. 검토자가 매번 다음을 직접 찾아야 한다고 해보자.

- 어떤 커밋이 결과인가
- 어떤 파일이 바뀌었는가
- 어떤 테스트가 실행됐는가
- 화면 캡처는 어디 있는가
- 실패했던 시도가 있었는가
- 남은 위험은 무엇인가

에이전트가 말로 길게 설명할 수도 있다. 하지만 설명만으로는 같은 결과를 다시 확인하거나 결과가 나온 과정을 추적하기 어렵다. 이 책에서는 결과와 검증 근거를 일정한 형식으로 함께 남기는 약속을 **증거 계약(Evidence Contract)**이라고 부른다. 업계의 정식 표준 이름이 아니라, 이후 설계를 설명하기 위해 이 책에서 사용하는 패턴이다.

> 완료를 설명하는 것보다, 무엇으로 완료를 판단했는지 남긴다.

---

## 13.1 Result Contract가 필요한 이유

에이전트마다 결과 보고 형식이 다르면 후속 단계가 복잡해진다.

에이전트 A:

~~~text
수정 완료했습니다.
테스트도 정상입니다.
~~~

에이전트 B:

~~~text
Changed 4 files.
Unit test passed.
~~~

에이전트 C:

~~~text
PR created.
Screenshot attached.
~~~

사람은 의미를 해석할 수 있다. 하지만 자동 시스템은 다음을 알기 어렵다.

- 어떤 코드 버전인가
- 어떤 검증이 필수였는가
- 실제 종료 코드는 무엇인가
- 산출물이 해당 코드 버전에서 만들어졌는가
- 위험이 남았는가

그래서 생산 시스템 결과는 일정한 구조를 갖는 편이 좋다.

~~~text
Task
→ Result
→ Verification
→ Evidence
→ Review / Acceptance
~~~

---

## 13.2 Evidence 최소 필드

모든 작업에 같은 근거가 필요한 것은 아니다. 그래도 공통 골격은 만들 수 있다.

예:

~~~text
task_id
base_revision
result_revision
declared_scope
changed_files
verification
artifacts
known_limitations
remaining_risk
~~~

검증에는 실제 실행 정보가 들어간다.

~~~text
verification:
  - command: ./gradlew test --tests AuthServiceTest
    exit_code: 0
    duration_ms: 8421
~~~

산출물은 별도 저장소를 참조할 수 있다.

~~~text
artifacts:
  - type: screenshot
    ref: artifact://task-100/mobile-after.png
  - type: log
    ref: artifact://task-100/integration.log
~~~

중요한 것은 에이전트가 “테스트했다”고 말하는 것이 아니라 **무엇을 어떻게 실행했고 결과가 무엇인지** 확인할 수 있다는 것이다. 범위가 중요한 작업이라면 `declared_scope`와 `changed_files`를 함께 남긴다.

~~~text
declared_scope
- src/auth/**
- tests/auth/**

changed_files
- src/auth/AuthService.java
- tests/auth/AuthServiceTest.java
~~~

이 둘을 비교하면 “테스트는 통과했지만 계획하지 않은 영역까지 수정한 변경”을 별도의 근거로 드러낼 수 있다. 검증도 이름만 나열하기보다 어떤 요구 조건 준수를 확인했는지 구분할 수 있다.

~~~text
verification
- functional: PASS
- architecture: PASS
- scope: PASS
- security: PASS
~~~

작업에 적용되지 않는 항목은 생략하거나 명시적으로 N/A 처리할 수 있다.

---

## 13.3 Commit과 Evidence를 연결한다

근거가 있어도 어떤 코드 기준인지 모르면 의미가 약해진다. 예를 들어 화면 캡처가 있다. 그런데 화면 캡처를 찍은 뒤 코드가 또 바뀌었다. 현재 커밋과 화면 캡처의 관계를 알 수 없다. 그래서 최소한 다음 연결이 필요하다.

~~~text
Task
→ Result Revision
→ Verification
→ Artifact
~~~

예:

~~~text
result_revision: abc123
screenshot_revision: abc123
test_revision: abc123
~~~

이 연결이 있어야 검토자가 현재 결과와 근거가 같은 상태를 가리키는지 알 수 있다.

---

## 13.4 Behavioral Evidence

코드 변경 내역만으로 확인하기 어려운 작업이 있다.

### UI

- 화면 캡처
- 영상
- DOM 스냅샷
- 브라우저 추적 기록

### API

- 실행 기반 요청 / 응답
- 규약 테스트
- 오류 로그

### Performance

- 성능 평가 변경 전 / 변경 후
- 환경 정보

### Migration

- 스키마 변경 내역
- 실제 변경 없는 시험 실행 결과
- 이전 상태로 복구 검사

이런 근거는 검토 비용을 줄인다. 예를 들어 UI 작업에서 검토자가 저장소를 코드 가져오기하고 직접 앱을 띄우기 전에 변경 전후 화면 캡처를 볼 수 있다.

~~~text
Before
→ button overlap

After
→ no overlap
~~~

이런 방식은 일부 에이전트 제품과 운영 사례에서 볼 수 있는 “Demos over Diffs” 접근과 닿아 있다. UI나 실제 실행 결과를 빠르게 이해하는 데 유용하지만, 시연이 변경 내역 검토와 보안 검증을 완전히 대체하는 것은 아니다. 동작을 보여주는 근거와 코드의 위험은 다른 문제다.

---

## 13.5 Evidence와 Provenance는 다르다

두 개념을 구분할 필요가 있다.

### Evidence

~~~text
이 결과가 맞다는 근거는 무엇인가?
~~~

예:

- 테스트 PASS
- 화면 캡처
- 성능 평가
- API 응답

### Provenance

~~~text
이 결과는 어떤 과정과 주체를 거쳐 만들어졌는가?
~~~

예:

- 어떤 에이전트가 실행했는가
- 어떤 모델 버전인가
- 어떤 하네스 버전인가
- 어떤 워커 이미지인가
- 누가 승인했는가
- 어떤 정책이 적용됐는가

단순화하면 다음과 같다.

~~~text
Evidence
= correctness / behavior signal

Provenance
= lineage / accountability signal
~~~

둘 다 중요하지만 역할은 다르다.

---

## 13.6 Evidence Manifest

시스템이 읽을 수 있는 목록 파일을 하나 두면 다음 단계가 쉬워진다.

예:

~~~json
{
  "taskId": "T-100",
  "baseRevision": "f10aa0",
  "resultRevision": "abc123",
  "declaredScope": [
    "src/auth/**",
    "tests/auth/**"
  ],
  "changedFiles": [
    "AuthService.java",
    "AuthServiceTest.java"
  ],
  "verification": [
    {
      "name": "auth-unit",
      "status": "passed",
      "artifact": "artifact://T-100/auth-unit.xml"
    },
    {
      "name": "auth-integration",
      "status": "passed",
      "artifact": "artifact://T-100/auth-integration.xml"
    }
  ],
  "knownLimitations": [],
  "remainingRisk": "OAuth flow not modified"
}
~~~

사람이 읽을 수 있는 요약은 이 목록 파일에서 만들 수 있다.

~~~text
Task T-100
- Result: abc123
- Files: 2
- Verification: 2/2 PASS
- Known limitation: none
~~~

이 구조의 장점은 에이전트마다 결과를 제각각 설명하지 않아도 된다는 것이다.

---

## 13.7 Review Startup Cost를 줄인다

검토자의 시간은 결과 자체보다 맥락 정보를 복구하는 데 많이 쓰일 수 있다.

- 왜 바꿨는가
- 어디를 바꿨는가
- 무엇으로 검증했는가
- 위험한 부분은 무엇인가

검증 근거 묶음은 이 시작 비용을 줄이는 장치다.

예:

~~~text
Summary
- expired JWT → 401

Scope
- auth module only

Result
- commit abc123

Verification
- unit PASS
- integration PASS

Evidence
- response sample
- logs

Risk
- OAuth flow unchanged
~~~

검토자는 모든 명령을 다시 실행하기 전에 범위와 결과를 빠르게 판단할 수 있다.

---

## 13.8 Performance Task는 Environment도 Evidence다

성능 측정은 결과 숫자만 남기면 부족하다.

~~~text
Before: 210 ms
After: 140 ms
~~~

이 숫자는 다음 조건에 따라 달라질 수 있다.

- CPU
- 메모리
- 데이터셋
- JVM 옵션
- 예열
- 동시 실행 수

그래서 성능 검증 근거에는 환경 정보도 들어가야 한다.

~~~text
benchmark:
  before: 210ms
  after: 140ms
  environment:
    cpu: 8 vCPU
    memory: 16GiB
    dataset: sample-v3
    warmup: 5
~~~

근거는 결과만이 아니라 **재현 조건**도 포함할 수 있다.

---

## 13.9 어디까지 표준화할 것인가

처음부터 복잡한 산출물 플랫폼이나 모든 작업에 동일한 목록 파일을 강제할 필요는 없다. 13.2의 공통 골격에서 시작하고, UI에는 화면 캡처와 추적 기록을, 성능에는 환경 정보를 추가하는 식으로 작업 유형에 따라 확장하면 된다. 핵심은 필드 수가 아니라 **결과 코드 버전과 검증·산출물 사이의 연결을 일관되게 유지하는 것**이다.

---

## 다음 질문

근거가 실패를 보여주었다고 하자. 통합 테스트가 실패했다. 워커도 중간에 죽었다. 같은 오류가 세 번째 반복됐다. 이때 생산 시스템은 무엇을 해야 할까. 다음 장에서는 실패를 예외가 아니라 정상적인 상태로 보고 **재시도, 처음부터 재시작, 중단 지점부터 재개, 다른 워커에 재배정, 사람에게 판단 요청**을 구분한다.

---

## 참고 자료

- Anthropic, *Demystifying evals for AI agents*  
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  https://openai.com/index/harness-engineering/
- NIST NCCoE, *DevSecOps Functional Demonstration Scenarios*  
  https://pages.nist.gov/nccoe-devsecops/functional-demonstration-scenarios.html
- GitHub, *Turn one giant AI-generated pull request to a reviewable stack*  
  https://github.blog/engineering/turn-one-giant-ai-generated-pull-request-to-a-reviewable-stack/
- Caylent Solutions, *DevBench Architecture*  
  https://github.com/caylent-solutions/devbench/blob/main/docs/architecture.md
