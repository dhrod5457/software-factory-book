# Part III Phase 7 Review

기준일: 2026-09-28

대상:
- chapters/07/draft.md
- chapters/08/draft.md
- chapters/09/draft.md
- chapters/10/draft.md
- chapters/11/draft.md
- chapters/12/draft.md

판정: **PASS**

## 주요 수정

### 7장
- Issue Tracker를 Work control surface로 표현
- Symphony도 별도 authoritative orchestrator runtime state를 가진다는 점 추가
- Execution Plane의 상태를 business state가 아닌 orchestration state로 정리

### 8장
- Branch는 history 분리이지 execution isolation이 아님을 수정
- Persistent vs ephemeral을 vendor 선택이 아닌 setup cost / contamination / security / reproducibility trade-off로 정리

### 9장
- Harness와 Sandbox 경계를 분명히 함
- Anthropic Managed Agents의 Session/Harness/Sandbox 분리를 사례로 반영
- GitHub Copilot code review tool regression과 instruction 재설계 후 약 20% review cost 감소를 회사 내부 사례로 범위 제한

### 10장
- vague한 “최근 Context File 연구” 표현 제거
- OpenAI 2026 Harness Engineering의 giant AGENTS.md 실패와 약 100-line map 사례로 교체
- Agent가 접근할 수 없는 조직 지식의 문제를 vendor 사례와 일반 원칙으로 분리

### 11장
- Agentless를 현재 SOTA 근거가 아니라 복잡한 agent loop가 필수는 아니라는 역사적 반례로 조정
- AIware 2026 COBOL modernization 연구의 scope와 최대 3.5x token 차이를 명시
- Autonomy cost를 조건부 표현으로 조정

### 12장
- Building to the Test를 18-run preprint라는 실험 범위와 함께 명시
- METR maintainer review 연구의 4 maintainers / 3 repos / 95 issues 및 single-shot 한계 추가
- OpenAI reward hacking을 rare but high severity의 내부 deployment 관찰로 제한
- AgentLens의 2,614 trajectories / 1,815 subset / 10.7% Lucky Pass 범위 명시

## 현재성 검증

확인:
- Anthropic Managed Agents, 2026-04-08
- OpenAI Harness Engineering, 2026-02-11
- SWE-agent ACI docs
- GitHub Copilot code review engineering post, 2026-07-10
- AIware 2026 deterministic vs LLM orchestration
- Microsoft Building to the Test, 2026-06 preprint
- METR maintainer review note, 2026-03
- OpenAI coding agent monitoring, 2026-03
- Microsoft AgentLens, 2026-05

## 남은 후속

- 도식은 manuscript에서 정식 그림으로 변환
- Verification / Evidence 용어는 전체 책 final terminology pass에서 통일
