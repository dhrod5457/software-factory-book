# 14장. Failure와 Recovery: 실패를 정상 상태로 설계한다

소프트웨어 생산 시스템에서 실패는 예외가 아니다. 에이전트가 틀리거나 도구 실행이 실패할 수 있고, 네트워크가 끊기거나 워커가 멈출 수도 있다. 같은 조건에서도 테스트가 간헐적으로 실패할 수 있으며, 필요한 권한이 부족할 수도 있다. 문제는 실패 자체가 아니다.

**실패 종류를 구분하지 못하고 항상 같은 방식으로 다시 실행하는 것**이 더 큰 문제다.

예를 들어 컨테이너 이미지 저장소가 잠시 503을 반환했다. 이때 코딩 에이전트에게 “문제를 고쳐라”라고 다시 시키면 엉뚱한 코드 변경을 시작할 수 있다. 반대로 실제 단위 테스트가 깨졌는데 단순 도구 재시도만 반복해도 해결되지 않는다. 그래서 복구는 다음 두 질문에서 시작한다.

> 무엇이 실패했는가?

> 어느 범위부터 다시 해야 하는가?

---

## 14.1 Failure Taxonomy

생산 시스템에서 실패를 몇 가지 범주로 나눌 수 있다.

### Tool Failure

예:

- GitHub API 502
- 이미지 저장소 시간 초과
- 로그 API의 일시적 오류

코드 자체와 무관할 수 있다.

### Harness Failure

예:

- 도구 스키마 불일치
- 잘못된 형식의 출력
- 맥락 정보 조합 실패
- 에이전트 연결 어댑터 비정상 종료

### Worker Failure

예:

- 프로세스 비정상 종료
- VM 종료
- 디스크 용량 부족
- 메모리 부족

### Network Failure

예:

- 묶음 저장소 접근 불가
- 내부 API 시간 초과
- 일시적인 DNS 오류

### Verification Failure

예:

- 단위 테스트 실패
- 통합 테스트 실패
- 보안 검사 실패

실제 코드 문제일 가능성이 있다.

### Permission Failure

예:

- 보호된 브랜치 푸시 거부
- 운영 환경 인증 정보 사용 불가
- 네트워크 정책 거부

### Agent Drift

예:

- 범위 밖 파일 수정
- 수용 판단과 무관한 구조 개선
- 같은 잘못된 가설 반복

### Environment Failure

예:

- 오래된 캐시
- 오염된 테스트 DB
- 잘못된 실행 기반 버전

이 분류가 완벽할 필요는 없다. 중요한 것은 모든 실패를 “에이전트 실패” 하나로 합치지 않는 것이다.

---

## 14.2 Recovery Ladder

실패가 났다고 바로 워커 전체를 새로 만들 필요는 없다. 가장 작은 범위부터 복구할 수 있다.

~~~text
Tool Retry
→ Step Retry
→ Agent Nudge
→ Subtask Retry
→ Worker Restart
→ Reassignment
→ Human Escalation
~~~

### Tool Retry

외부 API의 일시적 오류.

### Step Retry

특정 빌드·테스트 단계만 다시 실행.

### Agent Nudge

방향은 맞지만 작은 오해가 있을 때 수정을 준다.

### Subtask Retry

실패한 작업 부분만 다시 수행.

### Worker Restart

워커 상태가 오염됐거나 프로세스가 죽었을 때.

### Reassignment

다른 워커가 같은 작업을 이어받는다.

### Human Escalation

자동 복구가 의미 없거나 위험할 때 사람에게 넘긴다. 복구 범위가 커질수록 비용도 커진다. 그래서 가능한 한 작은 범위를 선택한다.

---

## 14.3 Infinite Retry를 막는다

다음 구조는 위험하다.

~~~text
while failed:
    retry()
~~~

같은 실패가 반복되면 비용만 늘고 외부에 남는 변경도 커질 수 있다. 그래서 재시도 한도가 필요하다.

예:

~~~text
max_retries: 2
~~~

하지만 횟수만으로는 부족할 수 있다. 같은 실패가 반복되는지도 봐야 한다. 이를 위해 이 책에서는 반복 오류를 식별할 수 있는 **실패 식별 정보**를 두는 방식을 사용한다. 이것 역시 특정 업계 표준이 아니라 동일 실패의 반복 여부를 판단하기 위한 설계 패턴이다.

예:

~~~text
type: integration-test
test: AuthIntegrationTest.expiredToken
exception: IllegalStateException
~~~

시도가 바뀌어도 같은 실패 식별 정보가 반복된다면 단순 재시도보다 판단 요청이나 다른 복구가 필요하다.

~~~text
A1
→ same fingerprint

A2
→ same fingerprint

System
→ stop retry
→ escalate
~~~

---

## 14.4 Restart, Resume, Reassign은 다르다

세 단어는 비슷해 보이지만 의미가 다르다.

### Restart

처음부터 다시 시작한다.

~~~text
Task
→ new attempt
→ start from base revision
~~~

장점:

- 깨끗한 상태

단점:

- 이미 완료한 작업을 잃는다.

### Resume

이미 완료한 작업을 인정하고 중단 지점 이후부터 이어간다.

~~~text
Task
→ restore checkpoint
→ continue
~~~

장점:

- 재작업 감소

단점:

- 복구 지점 품질이 필요하다.

### Reassign

다른 워커가 이어받는다.

~~~text
Worker A lost
→ Worker B continues
~~~

이 경우 같은 워커가 중단 지점부터 재개하는 것보다 더 어렵다. 다른 워커가 부분 상태까지 이해할 수 있어야 하기 때문이다.

---

## 14.5 Carryover Contract

다른 워커가 이어받으려면 “왜 중단됐는가”만으로는 부족하다. 다음 정보가 필요할 수 있다.

~~~text
Goal
Completed Work
Changed Files
Current Revision
Uncommitted Diff
Latest Verification
Failed Command
Failure Fingerprint
Known Blocker
Next Action
~~~

예:

~~~text
Goal
- expired JWT → 401

Completed
- AuthService 수정
- unit test PASS

Remaining
- integration test FAIL

Uncommitted
- patch artifact://T-100/A1.patch

Failure
- AuthIntegrationTest.expiredToken
- IllegalStateException

Next
- inspect exception mapping
~~~

인계 정보의 품질은 다음 질문으로 평가할 수 있다.

> 새로운 워커가 이전 워커와 대화하지 않고 이어갈 수 있는가?

---

## 14.6 Infra Failure와 Code Failure를 섞지 않는다

예를 들어 다음 오류가 발생했다.

~~~text
docker pull registry.example.com/app:latest
→ 503 Service Unavailable
~~~

이 실패는 애플리케이션 코드와 무관할 수 있다. 코딩 에이전트에게 다시 “고쳐라”라고 하면 에이전트는 다음을 시도할 수 있다.

- Dockerfile 수정
- 의존 패키지 변경
- 빌드 스크립트 변경

실제 원인은 이미지 저장소 장애인데 코드가 바뀐다. 반대로 다음 실패는 코드 문제일 수 있다.

~~~text
AuthServiceTest.expiredToken
expected: 401
actual: 500
~~~

이 경우 에이전트 수정이 적절하다. 실패 분류가 없으면 복구가 잘못된 계층에서 일어난다.

---

## 14.7 Targeted Intervention

복구는 재시도 아니면 사람 직접 인수 두 가지만 있는 것이 아니다.

2026년 arXiv 동료 심사 전 논문인 Wink 연구는 실제 운영에서 발생한 사용 기록에서 수집한 10,000개 이상의 코딩 에이전트 실행 경로를 바탕으로 외부 관찰자가 작은 개입으로 복구하는 패턴을 연구했다. 저자들은 분석 대상에서 명세에서 벗어나는 행동, 추론 문제, 도구 호출 실패 같은 잘못된 행동이 전체 실행 경로의 약 30%에서 관찰됐고, 한 번의 개입이 필요한 사례 중 90%를 Wink가 해결했다고 보고했다. 이 수치는 해당 운영 환경과 분류 체계에서 나온 결과이며 일반적인 코딩 에이전트 실패율로 해석하면 안 된다.

개념적으로 다음과 같다.

~~~text
Primary Agent
      ↓
Trajectory
      ↓
Observer
      ↓
Targeted Correction
      ↓
Primary Agent continues
~~~

예를 들어 에이전트가 범위 밖 디렉터리로 가기 시작했다고 하자. 전체 워커를 버리는 대신 다음과 같은 수정 지시를 줄 수 있다.

~~~text
변경 범위를 auth module로 제한하라.
현재 수정한 frontend 파일은 되돌려라.
~~~

이 방식은 처음부터 완전히 재시작보다 비용이 낮을 수 있다. 모든 작업에 관찰자 에이전트가 필요하다는 뜻은 아니다. 중요한 것은 복구할 때도 어디까지 다시 수행할지 범위를 여러 크기로 나눌 수 있다는 것이다.

---

## 14.8 Human Escalation은 실패가 아니다

자동화 시스템에서는 사람에게 판단을 요청하는 절차를 실패처럼 보기 쉽다. 하지만 실제 생산 시스템에서는 정상적인 상태일 수 있다.

예:

- 요구사항 모호함
- 설계 구조 결정 필요
- 보안 예외 필요
- 운영 환경 위험 높음
- 재시도 한도 소진
- 동일 실패 반복

이 경우 다음 상태가 적절할 수 있다.

~~~text
Task
→ BLOCKED / AWAITING_HUMAN
~~~

사람이 결정을 내린 뒤 다시 READY로 돌아간다.

~~~text
Human Decision
→ Task READY
→ new attempt
~~~

사람에게 판단을 요청하는 절차가 있다는 이유로 생산 시스템이 덜 자율적인 것은 아니다. 잘못된 자동화를 멈출 수 있다는 점에서 오히려 신뢰성이 높을 수 있다.

---

## 14.9 Recovery Policy 예시

다음처럼 실패 유형마다 정책을 둘 수 있다.

~~~text
registry_timeout
→ tool retry
→ max 3
→ exponential backoff

unit_test_failure
→ agent fix
→ max 2 attempts

worker_lost
→ resume if checkpoint exists
→ otherwise reassign

permission_denied
→ no retry
→ human/policy escalation

same_failure_repeated
→ stop
→ escalation
~~~

이 정책은 에이전트 지시문에만 두지 않는다. 제어 계층이 소유하는 편이 좋다.

---

## 다음 질문

재시도와 중단 지점부터 재개를 설계했어도 한 가지 어려운 문제가 남는다. 외부 API 호출이 실제로 성공했는데 응답만 유실되면 어떻게 할까. PR을 이미 만들었는데 실행 기반이 그 사실을 모르고 다시 생성하면 어떻게 할까. 사람의 승인을 하루 동안 기다리는 동안 워커를 계속 붙잡고 있어야 할까. 다음 장에서는 장시간 실행 작업을 현실의 비정상 종료와 대기에서 살아남게 만드는 **지속 실행**을 다룬다.

---

## 참고 자료

- Anthropic, *Effective harnesses for long-running agents*  
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Microsoft, *Durable Task for AI agents*  
  https://learn.microsoft.com/en-us/azure/durable-task/sdks/durable-task-for-ai-agents
- *Wink: Recovering from Misbehaviors in Coding Agents*  
  https://arxiv.org/abs/2602.17037
- Anthropic, *Patterns and problems in emerging multiagent systems*  
  https://www.anthropic.com/research/multiagent-systems
