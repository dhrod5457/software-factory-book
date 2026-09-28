# 20장. Event-driven Factory와 Closed-loop SDLC

지금까지의 Factory는 대부분 사람이 Task를 시작하는 구조였다.

하지만 실제 Software Delivery에서는 새로운 Work가 사람의 Prompt로만 생기지 않는다.

- CI Failure
- Security Alert
- Dependency Update
- Review Comment
- Scheduled Maintenance
- Production Incident
- Documentation Drift

이런 Signal을 Work Source로 사용할 수 있다.

문제는 Signal을 곧바로 Agent Action으로 연결하면 위험하다는 것이다.

~~~text
Alert
→ Agent
→ Production Change
~~~

이 구조에서는 잘못된 Alert, 중복 Signal, 일시적 장애가 실제 변경으로 이어질 수 있다.

그래서 Event-driven Factory에서는 중간에 해석 단계가 필요하다.

> Alert는 Task가 아니다.

---

## 20.1 Task Source를 확장한다

Factory가 받을 수 있는 Work Source는 다양하다.

~~~text
Human Request
Issue
CI Failure
Review
Vulnerability
Schedule
Production Signal
~~~

이 Signal은 모두 같은 의미가 아니다.

예를 들어 CI Failure는 재현 가능한 Engineering Problem에 가까울 수 있다.

반면 CPU Spike 하나는 아직 Task가 아니다.

원인이 코드인지, Traffic인지, Infra인지도 모른다.

그래서 Work Intake는 Signal을 먼저 분류해야 한다.

---

## 20.2 Signal에서 Task로

좋은 흐름은 다음에 가깝다.

~~~text
Signal
→ Diagnose
→ Scope
→ Risk
→ Acceptance
→ Task
→ Execute
~~~

예를 들어 Production Latency Alert가 발생했다.

바로 Code Change를 시작하지 않는다.

먼저 Diagnosis Task를 만든다.

~~~text
Goal
- latency 증가 원인 확인

Input
- traces
- metrics
- deployment revision

Acceptance
- top bottleneck identified
- evidence attached
~~~

Diagnosis 결과가 Code Issue로 확인되면 그다음 Fix Task를 만든다.

이렇게 하면 Alert와 Action 사이에 의미 있는 경계가 생긴다.

---

## 20.3 Event-driven은 Fully Autonomous와 다르다

Event가 자동으로 Task를 생성해도 Merge까지 자동일 필요는 없다.

예:

~~~text
CI Failure
→ auto task create
→ Agent fix
→ verification
→ human review
~~~

또는 Low-risk Task에서는:

~~~text
docs drift
→ auto task
→ agent fix
→ deterministic verification
→ auto merge by policy
~~~

즉 Event-driven은 **Work 시작 방식**에 관한 개념이다.

Autonomy는 별도 축이다.

---

## 20.4 Closed-loop SDLC

Software Delivery는 Deploy에서 끝나지 않는다.

~~~text
Plan
→ Build
→ Test
→ Release
→ Deploy
→ Operate
→ Observe
→ Learn
↺
~~~

Production에서 나온 Signal은 다시 Requirement, Test, Task로 돌아갈 수 있다.

예:

~~~text
Production Bug
→ Regression Test
→ Fix Task
→ Verification
→ Deploy
~~~

또는:

~~~text
Repeated Agent Failure
→ Missing Skill 발견
→ Factory Improvement Task
~~~

이 구조가 Closed-loop다.

---

## 20.5 Product Loop와 Factory Loop를 구분한다

두 가지 Feedback Loop가 있다.

### Product Loop

~~~text
Production Problem
→ Product Code Fix
~~~

예:

- latency bug
- validation bug
- UI defect

### Factory Loop

~~~text
Factory Friction
→ Factory Capability Improvement
~~~

예:

- slow Worker bootstrap
- missing Tool
- flaky Verification
- stale Context
- poor Evidence Package

둘을 섞지 않는다.

Product 문제가 Factory configuration 변경으로 잘못 이어지거나, Factory 문제를 Product Code 수정으로 해결하려 하면 혼란이 생긴다.

---

## 20.6 Noise를 Work로 증폭시키지 않는다

Production Signal은 noisy할 수 있다.

모든 Alert를 Task로 만들면 Backlog가 폭발한다.

예:

~~~text
same alert × 100
→ 100 tasks
~~~

필요한 제어:

- deduplication
- cooldown
- aggregation
- confidence threshold
- suppression
- change budget

예:

~~~text
same fingerprint
within 10m
→ one diagnosis task
~~~

---

## 20.7 Oscillation

Self-healing Loop가 잘못 설계되면 반복 변경이 발생할 수 있다.

~~~text
Agent
→ config increase

Metric improves briefly

Another signal
→ config decrease

Repeat
~~~

이런 Oscillation을 막기 위해 다음이 필요하다.

- observation window
- rollback rule
- change budget
- human escalation
- state/history

자동화가 많아질수록 “언제 아무것도 하지 않을 것인가”도 중요하다.

---

## 20.8 예: Nightly Test Failure

~~~text
02:00 Nightly Test FAIL
      ↓
Event received
      ↓
Deduplicate
      ↓
Task created
      ↓
Agent diagnoses
      ↓
Fix
      ↓
Targeted verification
      ↓
Regression test added
      ↓
Human / Policy Gate
~~~

좋은 점은 실패가 단순히 고쳐지고 끝나지 않는다는 것이다.

같은 문제가 다시 생기지 않도록 Regression Test가 Factory 자산으로 남는다.

---

## 20.9 Production Signal을 바로 Code Fix로 보내지 않는다

Latency Alert 예:

나쁜 흐름:

~~~text
latency high
→ Agent edits code
→ deploy
~~~

더 안전한 흐름:

~~~text
latency high
→ trace analysis
→ bottleneck identified
→ scope
→ risk
→ fix task
→ verification
→ deploy gate
~~~

이 구조는 속도를 조금 늦출 수 있다.

대신 잘못된 자동 수정의 Blast Radius를 줄인다.

---

## 다음 질문

Event-driven Factory가 Work를 만들기 시작하면 더 많은 Platform Capability가 필요해진다.

Database Provisioning, Deployment, Secret, Observability를 Agent가 직접 구현하게 해야 할까.

다음 장에서는 기존 **Developer Platform과 Golden Path를 Factory가 어떻게 활용하는가**를 다룬다.

---

## 참고 자료

- NIST NCCoE, *DevSecOps Notional Reference Model*  
  https://pages.nist.gov/nccoe-devsecops/notational-reference-model.html
- WorkOS, *The self-driving codebase: Building Horizon at WorkOS*  
  https://workos.com/blog/project-horizon
- Google, *Jules proactive updates*  
  https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/
