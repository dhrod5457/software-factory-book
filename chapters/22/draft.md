# 22장. Minimum Viable AI Software Factory

지금까지 책에서는 많은 구성요소를 다뤘다.

- 지속 작업
- 제어 계층
- 워커
- 하네스
- 맥락 정보
- 검증
- 근거
- 복구
- 권한과 책임 관리
- 관측 가능성
- 플랫폼

이 목록만 보면 소프트웨어 생산 시스템을 시작하기 전에 거대한 플랫폼부터 만들어야 할 것처럼 보인다. 하지만 그럴 필요는 없다. 오히려 처음부터 여러 에이전트를 함께 운영하고, 작업을 자동으로 선택하고, 시스템 스스로 개선하는 기능까지 넣으면 무엇이 실제로 필요한지 확인하기 어렵다. 첫 생산 시스템은 작아야 한다.

> 반복 가능하고 수용 판단을 정의할 수 있는 한 가지 작업을 안정적으로 처리하는 것부터 시작한다.

---

## 22.1 첫 Use Case를 고른다

첫 작업은 화려할 필요가 없다.

좋은 후보:

- 문서 수정
- 테스트 추가
- 의존 패키지 갱신
- CI 실패 분류와 우선순위 판단
- 작은 버그 수정
- Static/Lint 수정

공통점:

- 범위가 비교적 좁다.
- 반복해서 발생한다.
- 검증을 만들기 쉽다.
- 실패 피해 범위가 작다.

나쁜 첫 후보:

- 전체 설계 구조 재설계
- 모호한 신규 제품
- 운영 환경 긴급 상황 자동 복구
- 수용 판단을 정의하기 어려운 대규모 구조 개선

첫 사용 사례의 목표는 에이전트의 수행 능력을 자랑하는 것이 아니다. 작업 관리, 실행, 검증의 책임을 나눈 구조가 실제로 동작하는지 확인하는 것이다.

---

## 22.2 권장 시작 구조

2장에서 정의한 생산 시스템의 최소 성질과, 조직이 처음 도입할 때 권장하는 시작 구성은 같지 않다. 여기서는 실패 비용을 낮추기 위해 **사람의 검토를 남겨 둔 시작 형태**를 사용한다.

~~~text
Human selects Task
        ↓
Durable Task
        ↓
Isolated Worker
        ↓
Coding Agent
        ↓
Deterministic Verification
        ↓
Evidence
        ↓
Human Review
~~~

에이전트 하나면 충분하다. 자동 할 일 목록 선택도 필요 없다. 자동 병합도 필요 없다. 반대로 낮은 위험의 작업에서 충분한 검증 정책이 이미 있다면 사람의 검토를 생략할 수도 있다. 사람의 검토는 생산 시스템 정의의 필수조건이 아니라 첫 도입에서 안전한 기본값이다. 그럼에도 대화형 에이전트와 다른 중요한 성질이 생긴다.

- 작업 상태가 남는다.
- 워커가 분리된다.
- 검증이 있다.
- 근거가 남는다.
- 동일 작업 흐름을 반복할 수 있다.

---

## 22.3 Baseline: Repository, Worker, Evidence

**단계 A — 에이전트가 작업하기 쉽게 준비된 저장소**

생산 시스템보다 먼저 저장소를 본다. 다음 질문에 답하기 어렵다면 에이전트도 고생한다.

~~~text
Build command는?
Targeted test는?
Environment setup은?
Architecture boundary는?
Generated file은?
Owner는?
~~~

생산 시스템이 저장소 혼란을 자동으로 해결해줄 것이라고 기대하면 안 된다. 오히려 혼란을 빠르게 반복할 수 있다. 먼저 다음을 정리한다.

- 기준으로 정한 빌드
- 빠른 테스트
- 환경 준비
- 문서
- 담당 관계
- 기본 실행 기반

---

**단계 B — 재현 가능한 워커**

다음 목표:

> 같은 작업이 다른 워커에서도 실행 가능한가?

필요:

- 깨끗한 코드 가져오기
- 정해진 실행 기반
- 의존 패키지
- 범위가 제한된 인증 정보
- 테스트 명령

아직 여러 워커의 작업 배정기는 필요 없다. 워커 하나가 재현 가능하면 된다.

---

**단계 C — 증거 계약**

규모를 늘리기 전에 결과 형식을 정한다.

~~~text
Task ID
Result Commit
Changed Files
Verification
Artifacts
Known Risk
~~~

이것이 없으면 워커 수가 늘었을 때 사람이 결과를 비교하기 어려워진다.

---

## 22.4 Reliability: Durable State와 Recovery

**단계 D — 지속 작업 상태**

다음으로 작업 상태를 세션 밖으로 꺼낸다.

~~~text
READY
RUNNING
VERIFYING
AWAITING_HUMAN
DONE
FAILED
~~~

시도와 재시도도 기록한다. 이 시점부터 워커 중단과 작업 손실을 분리할 수 있다.

---

**단계 E — 재시도와 중단 지점부터 재개**

정상 실행 경로가 반복적으로 안정적이라면 실패 복구를 넣는다.

시험:

~~~text
Worker kill
Network failure
Verification failure
Approval delay
~~~

확인:

- 작업 상태 보존
- 재시도 한도 유지
- 근거 연결
- 외부 변경이 중복해서 발생하는 것 없음

---

## 22.5 Scale: Event Trigger와 Parallel Worker

**단계 F — 이벤트 시작 조건을 시험 실행으로 연결한다**

사람이 직접 시작하지 않아도 되는 작업을 연결한다.

예:

- CI 실패
- 이슈 상태
- 일정

하지만 이벤트를 연결했다고 곧바로 저장소 쓰기나 에이전트 실행까지 켤 필요는 없다. 먼저 신호 경로만 검증할 수 있다.

~~~text
Issue / CI / Schedule
→ Factory receives signal
→ Task candidate visible
→ no code change
~~~

실제 공개 구현 예제에서도 프로젝트 저장소의 이슈와 라벨이 중앙 생산 시스템에 도달하는지만 먼저 확인한 뒤 실제 실행을 활성화하는 방식이 사용된다. 이 패턴을 일반화하면 다음과 같다.

~~~text
Signal Integration
→ Observe-only / Dry Run
→ Agent Execution
→ Repository Write
→ Delivery / Merge Permission
~~~

각 단계에서 확인할 것이 다르다.

~~~text
Dry Run
- 중복 Signal은 없는가
- 올바른 Repository / Task로 매핑되는가
- 예상하지 않은 사용자 입력이 Trigger하지 않는가

Execution
- 올바른 Worker가 선택되는가
- 필요한 Context만 전달되는가

Write
- 허용된 Branch / Path만 변경하는가

Delivery
- Verification과 Approval 정책을 통과하는가
~~~

중요:

~~~text
Auto Start
≠ Auto Write
≠ Auto Merge
~~~

작업 소스 자동화와 외부에 남는 변경 권한, 최종 수용 권한은 서로 다른 축이다. 이렇게 단계적으로 권한을 열면 이벤트 기반 생산 시스템을 처음부터 완전 자율 시스템으로 만들지 않아도 된다.

---

**단계 G — 병렬 워커**

대기열이 실제로 쌓이기 시작했을 때 워커를 늘린다. 먼저 측정한다.

~~~text
Ready Task 충분?
Review Capacity?
CI Capacity?
Conflict Rate?
~~~

이 조건이 없으면 워커 증가가 가치가 없다.

---

## 22.6 Risk-based Automation

작업 위험도에 따라 정책을 다르게 한다.

예:

~~~text
Docs
→ auto verify
→ auto merge possible

Business Logic
→ human review

Auth / Payment / Migration
→ stronger verification
→ specialist approval
~~~

이때부터 작업 유형에 따라 자율성을 높인다.

---

## 22.7 Work Selection Automation은 뒤에 둔다

할 일 목록에서 어떤 작업을 할지 에이전트가 고르는 것은 높은 수준의 자율성이다. 잘못된 작업을 완벽하게 실행해도 가치가 없다. 그래서 보통 신뢰성 비교 기준과 검증·복구·관측 기반을 확인한 뒤에 둔다.

~~~text
Reliability baseline
→ Recovery + Observability
→ Scale
→ Autonomy
~~~

이것은 고정된 성숙도 단계가 아니라 위험한 자동화를 너무 일찍 넣지 않기 위한 권장 순서다. 저장소와 작업 흐름 특성에 따라 복구와 관측 가능성의 구현 순서는 달라질 수 있다.

---

## 22.8 Measure Before Automation

자동화 전 비교 기준을 남긴다.

예:

~~~text
cycle time
human intervention
retry
acceptance
review time
CI time
cost
~~~

이 데이터가 없으면 다음 질문에 답하기 어렵다.

> 생산 시스템을 도입한 뒤 실제로 좋아졌는가?

---

## 예: CI Failure Fix부터 시작하기

첫 사용 사례:

~~~text
CI unit test failure
~~~

흐름:

~~~text
Human selects failure
      ↓
Task
      ↓
Worker
      ↓
Agent diagnosis/fix
      ↓
targeted test
      ↓
Evidence
      ↓
Human Review
~~~

처음에는 소수의 실제 작업을 반복해 비교 기준을 만든다. 몇 건이 충분한지는 작업 다양성과 실패 빈도에 따라 달라지므로 고정 숫자를 두지 않는다.

확인:

- 첫 시도 수용
- 재시도
- 사람의 검토 시간
- 잘못된 수정
- 워커 환경 준비 시간

문제가 관찰된 뒤에 다음 기능을 추가한다.

---

## Minimum Viable Factory 체크

~~~text
1. 반복 가능한 Work가 있는가?
2. Acceptance를 자동/반자동으로 확인할 수 있는가?
3. Worker를 재현할 수 있는가?
4. Result Evidence가 표준화돼 있는가?
5. Task State가 Session 밖에 있는가?
6. 실패를 관찰할 수 있는가?
7. Human Review가 감당 가능한가?
~~~

처음부터 7개 모두 완벽할 필요는 없다. 하지만 빠진 것이 무엇인지 알고 시작해야 한다.

---

## 다음 질문

최소 기능 생산 시스템의 구조는 이해했다. 그렇다면 책 전체 원칙을 실제로 눈으로 확인할 수 있는 작은 참조 구현은 어떤 모습이어야 할까. 다음 장에서는 **참조 생산 시스템**을 설계하고 정상 실행 경로보다 실패 시나리오를 중심으로 검증한다.

---

## 참고 자료

- DORA, *Platform Engineering Capability*  
  https://dora.dev/capabilities/platform-engineering/
- CNCF, *Platform Engineering Maturity Model*  
  https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  https://openai.com/index/harness-engineering/
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- *I Built the Simplest Software Factory*, YouTube video / user-provided transcript  
  https://www.youtube.com/watch?v=AsvzMlLyQ38
