# 13장. Evidence Contract: 완료를 설명하지 말고 증명한다

Verification이 끝났다고 Review가 자동으로 쉬워지는 것은 아니다.

Reviewer가 매번 다음을 직접 찾아야 한다고 해보자.

- 어떤 Commit이 결과인가
- 어떤 파일이 바뀌었는가
- 어떤 Test가 실행됐는가
- Screenshot은 어디 있는가
- 실패했던 Attempt가 있었는가
- 남은 Risk는 무엇인가

Agent가 자연어로 길게 설명할 수도 있다.

하지만 설명은 재현성과 추적성이 약하다.

Factory에서는 결과를 **Evidence Contract**로 표준화하는 편이 낫다.

> 완료를 설명하는 것보다, 무엇으로 완료를 판단했는지 남긴다.

---

## 13.1 Result Contract가 필요한 이유

Agent마다 결과 보고 형식이 다르면 downstream이 복잡해진다.

Agent A:

~~~text
수정 완료했습니다.
테스트도 정상입니다.
~~~

Agent B:

~~~text
Changed 4 files.
Unit test passed.
~~~

Agent C:

~~~text
PR created.
Screenshot attached.
~~~

사람은 의미를 해석할 수 있다.

하지만 자동 시스템은 다음을 알기 어렵다.

- 어떤 Revision인가
- 어떤 Verification이 필수였는가
- 실제 Exit Code는 무엇인가
- Artifact가 해당 Revision에서 만들어졌는가
- Risk가 남았는가

그래서 Factory Result는 일정한 구조를 갖는 편이 좋다.

~~~text
Task
→ Result
→ Verification
→ Evidence
→ Review / Acceptance
~~~

---

## 13.2 Evidence 최소 필드

모든 Task에 같은 Evidence가 필요한 것은 아니다.

그래도 공통 골격은 만들 수 있다.

예:

~~~text
task_id
base_revision
result_revision
changed_files
verification
artifacts
known_limitations
remaining_risk
~~~

Verification에는 실제 실행 정보가 들어간다.

~~~text
verification:
  - command: ./gradlew test --tests AuthServiceTest
    exit_code: 0
    duration_ms: 8421
~~~

Artifact는 별도 저장소를 참조할 수 있다.

~~~text
artifacts:
  - type: screenshot
    ref: artifact://task-100/mobile-after.png
  - type: log
    ref: artifact://task-100/integration.log
~~~

중요한 것은 Agent가 “Test했다”고 말하는 것이 아니라 **무엇을 어떻게 실행했고 결과가 무엇인지** 확인할 수 있다는 것이다.

---

## 13.3 Commit과 Evidence를 연결한다

Evidence가 있어도 어떤 코드 기준인지 모르면 의미가 약해진다.

예를 들어 Screenshot이 있다.

그런데 Screenshot을 찍은 뒤 코드가 또 바뀌었다.

현재 Commit과 Screenshot의 관계를 알 수 없다.

그래서 최소한 다음 연결이 필요하다.

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

이 연결이 있어야 Reviewer가 현재 결과와 Evidence가 같은 상태를 가리키는지 알 수 있다.

---

## 13.4 Behavioral Evidence

Source Diff만으로 확인하기 어려운 Task가 있다.

### UI

- Screenshot
- Video
- DOM Snapshot
- Browser Trace

### API

- Runtime Request / Response
- Contract Test
- Error Log

### Performance

- Benchmark Before / After
- Environment Metadata

### Migration

- Schema Diff
- Dry-run Result
- Rollback Check

이런 Evidence는 Review 비용을 줄인다.

예를 들어 UI Task에서 Reviewer가 Repository를 Checkout하고 직접 앱을 띄우기 전에 Before/After Screenshot을 볼 수 있다.

~~~text
Before
→ button overlap

After
→ no overlap
~~~

이것이 Demos over Diffs의 장점이다.

하지만 Demo가 Diff Review와 Security Verification을 완전히 대체하는 것은 아니다.

Behavior를 보여주는 Evidence와 Source Risk는 다른 문제다.

---

## 13.5 Evidence와 Provenance는 다르다

두 개념을 구분할 필요가 있다.

### Evidence

~~~text
이 결과가 맞다는 근거는 무엇인가?
~~~

예:

- Test PASS
- Screenshot
- Benchmark
- API Response

### Provenance

~~~text
이 결과는 어떤 과정과 주체를 거쳐 만들어졌는가?
~~~

예:

- 어떤 Agent가 실행했는가
- 어떤 Model Version인가
- 어떤 Harness Version인가
- 어떤 Worker Image인가
- 누가 승인했는가
- 어떤 Policy가 적용됐는가

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

Machine-readable Manifest를 하나 두면 다음 단계가 쉬워진다.

예:

~~~json
{
  "taskId": "T-100",
  "baseRevision": "f10aa0",
  "resultRevision": "abc123",
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

Human-readable Summary는 이 Manifest에서 만들 수 있다.

~~~text
Task T-100
- Result: abc123
- Files: 2
- Verification: 2/2 PASS
- Known limitation: none
~~~

이 구조의 장점은 Agent마다 결과를 제각각 설명하지 않아도 된다는 것이다.

---

## 13.7 Review Startup Cost를 줄인다

Reviewer의 시간은 결과 자체보다 Context를 복구하는 데 많이 쓰일 수 있다.

- 왜 바꿨는가
- 어디를 바꿨는가
- 무엇으로 검증했는가
- 위험한 부분은 무엇인가

Evidence Package는 이 Startup Cost를 줄이는 장치다.

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

Reviewer는 모든 Command를 다시 실행하기 전에 Scope와 Result를 빠르게 판단할 수 있다.

---

## 13.8 Performance Task는 Environment도 Evidence다

Performance Benchmark는 결과 숫자만 남기면 부족하다.

~~~text
Before: 210 ms
After: 140 ms
~~~

이 숫자는 다음 조건에 따라 달라질 수 있다.

- CPU
- Memory
- Dataset
- JVM Option
- Warmup
- Concurrency

그래서 Performance Evidence에는 Environment Metadata도 들어가야 한다.

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

Evidence는 결과만이 아니라 **재현 조건**도 포함할 수 있다.

---

## 13.9 Evidence Contract의 최소 시작점

처음부터 복잡한 Artifact Platform을 만들 필요는 없다.

다음 정도면 시작할 수 있다.

~~~text
Task ID
Result Commit
Changed Files
Verification Commands
Verification Result
Artifact Paths
Known Limitation
~~~

이 정도만 표준화해도 Review와 Automation이 쉬워진다.

---

## 다음 질문

Evidence가 실패를 보여주었다고 하자.

Integration Test가 실패했다.

Worker도 중간에 죽었다.

같은 오류가 세 번째 반복됐다.

이때 Factory는 무엇을 해야 할까.

다음 장에서는 Failure를 예외가 아니라 정상적인 State로 보고 **Retry, Restart, Resume, Reassignment, Human Escalation**을 구분한다.

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
