# Part II Draft Review

기준일: 2026-09-28

대상:

- `chapters/04/draft.md`
- `chapters/05/draft.md`
- `chapters/06/draft.md`

## 판정

**PASS WITH MINOR FOLLOW-UP**

Part II의 역할 분담은 명확하다.

~~~text
4장
Work의 의미와 Acceptance를 고정

5장
Work를 Durable Task State로 모델링

6장
Task를 실행·검증·복구 가능한 Graph로 분해
~~~

Part III로 넘어가도 된다.

---

## 4장 역할

핵심:

- Prompt만으로 큰 Work를 관리하기 어려운 이유
- Intent / Requirement / Acceptance 분리
- Requirement Generator와 Acceptance Authority 분리
- Ready Contract
- Requirement → Verification Traceability

좋은 점:

- Spec 문서 형식보다 durable artifact와 acceptance에 초점을 맞춤
- 작은 Task에 과도한 spec process를 강제하지 않음
- Agent가 Requirement와 Test를 동시에 오해할 위험을 포함

후속 line edit 후보:

- Requirements-first / Design-first 사례를 최종 원고에서 한 가지 실제 migration 예로 조금 더 구체화할 수 있음
- Ready Contract와 5장 Task schema의 중복은 현재 수준 유지, 최종 편집 시 5장에서 상세화

현재 상태:

**READY FOR PART III**

---

## 5장 역할

핵심:

- Prompt / Session / Task lifetime 분리
- Task / Attempt 분리
- State transition
- Worker보다 오래 사는 Task
- Carryover

좋은 점:

- Durable Task의 실무 의미가 명확함
- Context Window를 Task Database로 쓰지 않는 원칙 포함
- Worker A → Worker B continuation을 구체적으로 설명

후속 line edit 후보:

- Task schema는 본문 표 또는 그림으로 바꾸면 읽기 쉬움
- 15장 Durable Execution과 중복되지 않도록 여기서는 state model에 집중 유지

현재 상태:

**READY FOR PART III**

---

## 6장 역할

핵심:

- Task Size trade-off
- Independence
- Dependency Graph
- Retry Boundary
- Review Boundary
- Parallel candidate

좋은 점:

- "작게 쪼개라"가 아니라 execute / verify / recover / review 가능한 단위로 정의
- Runtime-Structured Decomposition 연구와 연결
- Large Task와 Large PR를 구분

후속 line edit 후보:

- Task size 개념 그림을 실제 manuscript 단계에서 추가
- Multi-Agent 운영 상세는 17장으로 유지

현재 상태:

**READY FOR PART III**

---

# Part II 전체 결론

Part II가 책에서 해야 할 역할은 다음 한 줄로 요약된다.

> Agent가 실행하기 전에 Work 자체를 시스템이 관리할 수 있는 형태로 만든다.

다음 Part III에서는 이 Work를 실제로 실행하는:

- Control Plane
- Worker
- Sandbox
- Harness
- Context
- Controlled Autonomy
- Verification

로 이동한다.
