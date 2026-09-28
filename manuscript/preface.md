# 들어가며

AI Coding Agent를 처음 쓰기 시작하면 관심은 자연스럽게 Agent 자체에 간다.

어떤 Model이 코드를 더 잘 쓰는가.  
어떤 Tool을 연결해야 하는가.  
얼마나 긴 Task를 맡길 수 있는가.  
여러 Agent를 동시에 돌리면 얼마나 빨라지는가.

이 질문들은 중요하다.

하지만 Agent가 실제 개발 작업을 더 많이 수행하기 시작하면 곧 다른 문제가 보인다.

작업을 누가 정의하는가.  
Agent가 중간에 죽으면 어디서 이어가는가.  
완료했다는 말을 무엇으로 믿는가.  
여러 Worker가 같은 코드를 동시에 바꾸면 누가 조정하는가.  
Agent가 만든 Pull Request가 늘어났는데 Review와 CI가 감당하지 못하면 어떻게 하는가.  
더 많은 권한을 주면서도 어떻게 안전하게 운영할 것인가.

관심의 중심이 Model에서 System으로 이동한다.

이 책은 그 시스템을 **AI Software Factory**라고 부른다.

여기서 Factory는 사람을 없앤 완전 자동 개발 조직을 뜻하지 않는다. Agent를 여러 개 실행하는 시스템과도 같은 말이 아니다.

이 책에서 관심을 두는 것은 더 현실적인 문제다.

> 소프트웨어 작업을 지속 가능한 상태로 관리하고, Agent에게 실행을 위임하며, 결과를 독립적으로 검증하고, 실패를 복구하고, 필요한 지점에서 사람이 책임을 유지할 수 있는 생산 시스템은 어떻게 설계해야 하는가?

## 이 책이 다루는 것

이 책은 AI Agent를 Software Delivery System 안의 Worker로 배치할 때 필요한 구조를 다룬다.

주요 주제는 다음과 같다.

- Requirement와 Acceptance
- Durable Task
- Control Plane과 Execution Plane
- Worker와 Sandbox
- Harness와 Context
- Controlled Autonomy
- Verification과 Evidence
- Failure와 Recovery
- Durable Execution
- Security와 Governance
- Parallel Worker와 Multi-Agent
- Review / CI / Integration
- Observability와 Metrics
- Event-driven Work
- Developer Platform
- Minimum Viable Factory
- Maturity와 Autonomy

개별 기술을 따로 설명하기보다 하나의 Software Production System 안에서 어떻게 연결되는지를 중심으로 본다.

## 이 책이 다루지 않는 것

이 책은 특정 Coding Agent 제품의 사용 설명서가 아니다.

현재 가장 좋은 Model을 고르는 책도 아니다.

다음 주제도 중심 범위에서 제외한다.

- AI 역사
- Software Factory 개념의 긴 역사
- Prompt Engineering 기법 모음
- 특정 Agent Framework 튜토리얼
- Kubernetes나 CI/CD 구축 자체
- 완전 자율 조직에 대한 미래 예측
- 개발자 직업의 소멸 여부

제품과 연구 사례는 사용한다.

다만 제품 자체를 주인공으로 만들지는 않는다. 제품이 바뀌더라도 남을 수 있는 설계 원칙을 먼저 찾는다.

## 누구를 위한 책인가

주요 독자는 Software Engineer, Tech Lead, Architect, Platform Engineer다.

특히 다음 상황에 있는 독자를 생각했다.

- Coding Agent를 개인 도구 이상으로 사용하려는 팀
- 여러 Agent/Worker를 병렬로 운영하려는 팀
- Agent 작업을 CI/CD와 연결하려는 팀
- Agent 결과의 검증과 증거가 필요한 팀
- 장시간 Task와 Recovery를 고민하는 팀
- 개발 조직의 Agent 운영 기반을 만들려는 Platform Team

Agent를 처음 접하는 입문서라기보다, 이미 Software Engineering 경험이 있는 독자가 Agent를 기존 개발 시스템 안에 배치하는 방법을 고민할 때 읽는 책에 가깝다.

## 이 책에서 사용하는 접근

AI Agent 영역은 변화가 빠르다.

제품 기능과 Model 이름은 몇 달 안에도 바뀔 수 있다. Benchmark도 빠르게 포화되거나 평가 방식이 수정된다.

그래서 이 책은 세 종류의 내용을 구분한다.

첫째, 여러 독립 사례에서 반복되는 설계 원칙이다.

예를 들어 Task State를 Agent Session 밖에 두는 것, Agent의 완료 보고와 실제 검증을 분리하는 것, 높은 Autonomy에 Isolation과 Governance가 필요하다는 것은 여러 시스템에서 반복해서 나타난다.

둘째, 특정 회사나 제품의 운영 사례다.

이 경우 해당 조직의 환경에서 관찰된 사례임을 명시한다. 특정 회사가 Agent를 몇 개 운영했다고 해서 그것을 모든 조직의 기준으로 사용하지 않는다.

셋째, 아직 연구 중인 가설이나 이 책에서 제안하는 설계 패턴이다.

예를 들어 이 책에서 사용하는 Evidence Contract, Cost per Accepted Change, M0~M5 Maturity Model은 업계 표준이 아니다. Software Factory를 설명하고 비교하기 위한 작업 개념이다.

## 책을 읽는 순서

Part I은 왜 Coding Agent만으로는 Software Delivery 문제를 설명하기 어려운지 다룬다.

Part II는 Agent가 실행하기 전에 Work 자체를 Requirement, Acceptance, Durable Task로 구조화한다.

Part III는 Control Plane, Worker, Harness, Context, Autonomy, Verification으로 실제 실행 구조를 만든다.

Part IV는 Evidence, Recovery, Durable Execution, Security를 통해 그 결과를 신뢰할 수 있게 만든다.

Part V는 Worker 수가 늘어났을 때 Parallelism과 Review/CI 병목, Observability를 다룬다.

Part VI는 Production Signal과 Developer Platform까지 Factory의 경계를 확장한다.

Part VII은 처음 Factory를 어떻게 시작하고, 어떤 조건에서 Scale과 Autonomy를 높일지 정리한다.

각 장은 앞 장의 문제를 다음 장의 설계 문제로 연결하도록 구성했다. 처음 읽을 때는 순서대로 읽는 편이 좋다.

이미 Agent Platform이나 Developer Platform을 운영하는 독자라면 필요한 Part부터 참고해도 된다.

## 이 책의 기준

이 책이 계속 확인할 기준은 Agent가 얼마나 많은 코드를 생성했는지가 아니다.

다음 질문에 더 가깝다.

> Agent가 실패할 수 있다는 전제에서도, 검증된 소프트웨어 변경을 지속적으로 전달할 수 있는가?

Software Factory의 품질은 Agent가 한 번에 성공했을 때보다 실패했을 때 더 잘 드러난다.

Task는 남아 있는가.  
유효한 작업을 이어받을 수 있는가.  
잘못된 결과가 완료로 보이지 않는가.  
사람이 필요한 지점에서 개입할 수 있는가.  
전체 Delivery Flow가 실제로 좋아지고 있는가.

이 질문을 하나씩 시스템 구조로 바꾸는 것이 이 책의 목적이다.
