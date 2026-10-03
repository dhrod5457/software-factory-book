# 3장. CI/CD, DevOps, Platform Engineering, Agent Platform과의 경계

2장에서 AI Software Factory의 최소 정의를 정했다.

하지만 실제 조직에는 이미 많은 시스템이 있다.

- Git
- 이슈 추적 도구
- CI/CD
- 내부 개발자 플랫폼
- 운영 감시
- 배포 플랫폼
- 비밀 정보 관리
- 에이전트 실행 기반

그래서 새로운 이름을 붙이는 것보다 더 중요한 질문이 생긴다.

> AI Software Factory는 기존 시스템과 정확히 무엇이 다른가?

이 경계를 잘못 잡으면 두 가지 문제가 생긴다. 하나는 기존에 잘 동작하던 CI/CD와 플랫폼을 무시하고 모든 것을 다시 만드는 것이다. 다른 하나는 반대로 기존 파이프라인에 에이전트 호출 하나를 추가하고 그것을 소프트웨어 생산 시스템이라고 부르는 것이다. 둘 다 피해야 한다. 이 장에서는 AI Software Factory를 기존 소프트웨어 전달 시스템 위에 놓고 경계를 정리한다.

---

## 3.1 CI/CD는 무엇을 이미 잘하고 있는가

CI/CD는 이미 소프트웨어 생산 자동화의 핵심이다. 일반적인 흐름은 다음과 같다.

```text
Source Change
→ Build
→ Test
→ Package
→ Release
→ Deploy
```

이 구조를 갖추면 사람이 매번 수동으로 빌드하고 테스트하지 않아도 된다. 같은 코드 버전(Revision)을 반복해서 검증할 수 있고, 정책에 따라 릴리스와 배포를 자동화할 수도 있다. 소프트웨어 생산 시스템은 이 기반을 버리지 않는다. 오히려 적극적으로 사용한다. 차이는 CI/CD가 보통 **정의된 변경 이후**를 잘 다룬다는 데 있다. 예를 들어 CI는 다음 질문에 답한다.

- 이 커밋이 빌드되는가?
- 테스트가 통과하는가?
- 산출물을 만들 수 있는가?
- 배포가 성공하는가?

하지만 일반적인 CI/CD는 다음 질문까지 스스로 책임지지 않는다.

- 어떤 문제를 해결해야 하는가?
- 어떤 작업을 지금 시작해야 하는가?
- 어떤 파일을 수정해야 하는가?
- 실패한 테스트를 어떻게 고칠 것인가?
- 같은 작업을 다른 워커에게 재배정해야 하는가?
- 사람의 승인을 기다려야 하는가?

AI Software Factory는 이 앞단과 중간을 확장한다.

```text
Intent
→ Requirement
→ Task
→ Agent Work
→ Code Change
→ CI/CD
→ Delivery
→ Feedback
```

이 관점에서는 CI/CD가 사라지는 것이 아니다. 생산 시스템의 중요한 검증·전달 하위 시스템이 된다. 특히 에이전트 시대에는 CI가 파이프라인의 끝에만 있는 것도 아니다.

```text
Agent Change
→ Targeted Test
→ CI
→ Failure
→ Agent Fix
→ CI
```

CI 결과가 에이전트에게 다시 피드백되어 수정 루프 안으로 들어올 수 있다. 즉, 생산 시스템이 CI/CD를 대체하는 것이 아니라 CI/CD를 더 자주 호출하고 더 중요한 피드백 자료로 사용한다.

---

## 3.2 DevOps와 DevSecOps를 대체하지 않는다

AI Software Factory를 새로운 개발 방법론으로 오해할 필요도 없다. DevOps와 DevSecOps가 강조해 온 원칙은 에이전트 시대에도 그대로 중요하다.

- 작은 변경
- 빠른 피드백
- 자동화된 검증
- 운영 가시성
- 개발과 운영의 연결
- 보안의 조기 통합

오히려 에이전트가 더 많은 변경을 더 빠르게 만들수록 이런 원칙은 더 중요해질 수 있다. NIST NCCoE가 2026년 9월 갱신한 DevSecOps live 참조 모델을 보면 소프트웨어 전달을 다음과 같은 연속된 흐름으로 본다.

```text
Plan
→ Develop
→ Build
→ Test
→ Release
→ Deploy
→ Operate
        ↘
     Feedback
        ↖
```

여기에 CI/CD, 보안, 운영 감시, 제어 통과 조건이 횡단으로 들어간다. 중요한 점은 AI가 이 구조를 없애는 것이 아니라는 것이다. 2026년 9월 기준 NIST의 현재 공개 구현은 사람이 지시하는 생성형 AI를 계획·개발·지속적 피드백에 넣고 있으며, 다음 Build 3에서 에이전트 중심 AI가 개발·빌드·테스트를 수행하는 구조를 검토하고 있다.

NIST 역시 AI를 별도 SDLC로 떼어내기보다 기존 DevSecOps 생애주기 안에 통제된 실행 주체로 넣는 방향을 취한다. 이 관점에서 생산 시스템은 사람, 기존 자동화, 에이전트를 하나의 작업 흐름 안에서 연결한다.

```text
Human / Product
      ↓
Plan / Requirement
      ↓
Human + Automation + Agent
      ↓
Build / Test / Release / Deploy
      ↓
Operate / Feedback
```

DevOps가 사라지는 것이 아니라 실행 주체가 늘어나는 것이다.

---

## 3.3 Platform Engineering과 Factory는 경쟁 관계가 아니다

Platform Engineering과 소프트웨어 생산 시스템은 자주 겹쳐 보인다. 둘 다 다음을 이야기하기 때문이다.

- 표준화
- 자동화
- 사용자의 직접 이용
- 표준 개발 경로
- 정책
- 개발자 경험

하지만 책임의 중심이 다르다. 플랫폼 엔지니어링(Platform Engineering)은 조직의 여러 팀이 함께 쓸 수 있는 **개발과 운영 기능**을 제공한다. 예를 들면 다음과 같다.

- 표준 저장소 서식
- 빌드 환경
- CI
- 비밀 정보 관리
- 배포
- 관측 가능성
- 데이터베이스 준비
- 소프트웨어 목록
- 정책

개발자는 이 기능을 사용해 제품을 만든다. AI Software Factory도 똑같이 이 기능을 사용할 수 있다. 경계를 단순화하면 다음과 같다.

```text
Platform Engineering
= 안전하고 표준화된 생산 능력을 제공

Software Factory
= 그 능력을 사용해 실제 Work를 완료
```

예를 들어 작업이 "사전 검증용 데이터베이스를 준비하라"라고 하자. 에이전트에게 Terraform과 Kubernetes 설정을 매번 새로 생성하게 할 수도 있다. 하지만 조직에 이미 표준 개발 경로가 있다면 다음처럼 만드는 편이 낫다.

```text
provision_database(
  profile = "staging-small"
)
```

에이전트는 구현 세부사항을 직접 만들지 않는다. 플랫폼이 검증된 방식으로 자원을 준비한다. 이 구조의 장점은 명확하다.

- 정책이 중앙에서 적용된다.
- 이름 지정과 자원 크기가 표준화된다.
- 감사가 쉬워진다.
- 에이전트에게 과도한 인프라 권한을 주지 않아도 된다.
- 팀마다 Terraform 설정이 서로 달라지는 문제를 줄일 수 있다.

즉, 생산 시스템이 플랫폼을 대체하려고 하면 안 된다. 다음 구조가 더 자연스럽다.

```text
Factory
→ Platform API / Golden Path
→ Infrastructure
```

---

### Agent도 Platform User가 된다

에이전트가 플랫폼의 소비자가 되면 포털과 문서만으로는 부족할 수 있다. 안정적인 API, 구조화된 결과, 범위가 제한된 권한처럼 시스템이 읽을 수 있는 인터페이스가 중요해진다. 다만 이 장에서는 경계만 확인한다. 표준 개발 경로를 에이전트 도구로 만드는 방법과 소프트웨어 목록, 구조화된 오류, 멱등성 같은 구체적인 플랫폼 설계는 21장에서 다룬다.

---

## 3.4 Agent Platform과 Software Factory

에이전트 플랫폼과 소프트웨어 생산 시스템은 더 쉽게 혼동된다. 에이전트 플랫폼은 보통 에이전트를 만들고 운영하는 범용 기반을 제공한다. 예를 들면 다음 기능이다.

- 실행 기반
- 모델 접근
- 도구 연결 관문
- 신원
- 메모리
- 관측 가능성
- 정책
- 평가

이 기능은 코딩 에이전트뿐 아니라 다른 에이전트에도 사용할 수 있다.

- 고객 지원 에이전트
- 데이터 에이전트
- 영업 에이전트
- 운영 에이전트
- 연구 에이전트

소프트웨어 생산 시스템은 이보다 업무 영역이 좁다. 소프트웨어 전달에 특화된 대상과 상태를 다룬다.

- 요구사항
- 저장소
- 브랜치
- 커밋
- 빌드
- 테스트
- 변경 검토 요청
- 산출물
- 승인
- 릴리스
- 배포
- 수용 판단

그래서 다음처럼 구분하는 편이 유용하다.

```text
Agent Platform
= Agent를 실행할 수 있는 범용 기반

AI Software Factory
= Software Work를 완료하는 Domain System
```

에이전트 플랫폼이 충분히 좋아도 다음을 자동으로 제공하지는 않는다.

- 어떤 작업이 실행 준비가 된 상태인가
- 이 작업의 의존 관계는 무엇인가
- 어떤 검증이 필수인가
- 이 변경 검토 요청을 병합해도 되는가
- 워커가 죽었을 때 같은 작업을 어떻게 이어받는가
- 같은 스키마를 수정하는 작업을 동시에 시작해도 되는가

이것은 소프트웨어 생산 시스템이 알아야 하는 업무 영역 상태다.

---

### Runtime과 Factory도 구분한다

에이전트 런타임(Agent Runtime)은 에이전트가 실제로 동작하는 기반이다.

```text
Agent Runtime
- process
- container
- model call
- tool call
- filesystem
- isolation
```

생산 시스템은 실행 기반을 사용할 수 있다. 하지만 생산 시스템의 작업은 실행 기반보다 오래 살아야 한다. 실행 기반이 죽어도 다음은 남아야 한다.

- 작업
- 시도 이력
- 검증
- 근거
- 승인
- 재시도 상태

그래서 단순하게 다음과 같이 계층화하면 오해가 생긴다.

```text
Agent Runtime
< Agent Platform
< Software Factory
```

항상 포함 관계는 아니다. 더 정확한 표현은 다음에 가깝다.

```text
Software Factory
uses
- Agent Runtime
- Agent Platform
- Developer Platform
- CI/CD
```

생산 시스템은 이 기반 위에서 소프트웨어 전달 영역의 작업을 관리한다.

---

## 3.5 경계를 나누면 무엇이 좋아지는가

경계를 나누는 이유는 용어 정리를 하기 위해서만은 아니다. 실제 설계 구조가 단순해진다. 예를 들어 생산 시스템을 만든다고 다음 기능을 모두 직접 구현한다고 해보자.

- 비밀 정보 관리 도구
- CI 실행기
- 컨테이너 작업 배정기
- 배포 시스템
- 로그 기록
- 지표
- 산출물 저장소
- 에이전트 실행 기반

거대한 프로젝트가 된다. 실제로 필요한 것은 기존 기능을 연결하는 것일 수 있다.

```text
Task
      ↓
Factory Control Plane
      ↓
Agent Runtime
      ↓
Developer Platform
      ↓
CI/CD / Deploy / Observability
```

이 구조에서는 생산 시스템이 모든 기능을 직접 구현하지 않는다. 생산 시스템은 작업 상태, 워커 선택, 검증, 복구, 승인 같은 소프트웨어 전달의 흐름을 책임지고, 플랫폼과 CI/CD는 환경·인증 정보·빌드·테스트·배포 같은 기존 기능을 제공한다. 에이전트 실행 기반은 실제 에이전트 실행을 담당한다. 각 시스템이 잘하는 일을 그대로 사용한다. 이렇게 하면 생산 시스템 구조를 새 인프라 전체로 만들지 않아도 된다.

---

## Software Factory는 새로운 섬이 아니다

이 책에서 AI Software Factory를 기존 소프트웨어 공학과 분리된 새로운 세계로 보지 않는 이유가 있다. 실제 조직에서 가장 현실적인 생산 시스템은 기존 자산을 재사용할 가능성이 높다.

```text
Git
+ Issue Tracker
+ CI/CD
+ Internal Developer Platform
+ Agent Runtime
+ Task Orchestration
+ Verification
+ Governance
```

이 조합이 조직마다 다를 뿐이다. 새롭게 필요한 것은 모든 도구를 다시 만드는 것이 아니라 **에이전트가 이 시스템 안에서 작업을 수행할 수 있도록 상태와 권한과 피드백을 연결하는 것**이다. 그래서 생산 시스템을 설계할 때 첫 질문은 다음이 아니다.

> 어떤 에이전트 플랫폼을 도입할까?

먼저 물어야 할 것은 이것이다.

> 우리 조직에 이미 어떤 소프트웨어 전달 수행 능력이 있고, 그중 에이전트가 안전하게 사용할 수 없는 부분은 어디인가?

이 질문을 하면 구축 범위가 줄어든다. 그리고 무엇을 새로 만들어야 하는지도 선명해진다.

---

## 다음 질문

지금까지는 생산 시스템의 외곽 경계를 정리했다. 이제부터는 내부로 들어간다. 에이전트에게 작업을 주기 전에 먼저 결정해야 할 것이 있다. 에이전트가 무엇을 구현해야 하는지 어떻게 정의할 것인가. 어떤 상태가 되어야 "작업할 준비가 됐다"고 볼 것인가. 다음 장에서는 지시문을 바로 에이전트에게 던지는 대신 **의도를 요구사항과 수용 판단으로 바꾸는 과정**부터 시작한다.

---

## 참고 자료

- NIST NCCoE, *Notional Reference Model for DevSecOps*  
  https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
- DORA, *Platform Engineering Capability*  
  https://dora.dev/capabilities/platform-engineering/
- CNCF, *Platform Engineering Maturity Model*  
  https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/
- CNCF, *Platform Engineering for the Agentic Enterprise*  
  https://www.cncf.io/blog/2026/07/21/platform-engineering-for-the-agentic-enterprise-managing-applications-resources-and-ai-agents/
- Backstage, *AI in the Software Catalog*  
  https://backstage.io/docs/ai/ai-in-the-catalog/
