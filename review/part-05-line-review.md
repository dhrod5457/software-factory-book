# Part V Phase 7 Review

기준일: 2026-09-28

대상:
- chapters/17/draft.md
- chapters/18/draft.md
- chapters/19/draft.md

판정: **PASS**

## 주요 수정

### 17장
- Anthropic 2026 multi-agent 결과를 12시간 open-world game simulation이라는 실험 범위로 제한
- 일부 Model의 낮은 merge fraction / shared-file conflict와 최신 Model의 file ownership 전략을 구분
- 동일 Model/Context의 conformity 예시를 30 Agent 중 18개 동일 branch name 사례로 구체화
- queue-management experiment의 초당 30회 polling / 240만 요청 / 117 accepted 사례를 극단적 simulation으로 contextualize

### 18장
- Reviewability를 이 책의 Factory 품질 속성으로 명시
- GitHub stacked pull requests를 2026-07 public preview / 2026-08 engineering 사례로 업데이트
- stacked PR을 universal answer가 아닌 reviewability 구현 방식 중 하나로 제한
- AI Reviewer도 Harness/Eval이 필요하다는 논리를 9장 사례와 연결해 중복 축소

### 19장
- Accepted Change / Cost per Accepted Change를 업계 표준이 아닌 책의 synthesis로 명시
- First-pass Acceptance Rate도 후보 운영 지표로 제한
- Microsoft 2026 GitHub Copilot production-scale trace의 3.2M users / 13M sessions / 761M LLM calls / 95T tokens를 preprint 범위와 함께 추가
- GitHub 2026 efficiency 사례를 통해 per-call token 최소화와 end-to-end task efficiency를 구분

## 현재성 검증

확인:
- Anthropic, Patterns and problems in emerging multiagent systems, 2026-08-13
- GitHub Stacked Pull Requests public preview, 2026-07-30
- GitHub giant AI PR → reviewable stack, 2026-08-04
- Microsoft Research, Agentic Coding in the Wild, July 2026 preprint
- GitHub, coding agent cost efficiency, 2026-09-02

## 남은 후속

- Anthropic simulation의 model names와 수치는 출간 직전 재검증
- GitHub stacked PR는 preview 상태가 바뀔 수 있으므로 출간 직전 제품 상태 재검증
- Metric 이름은 final terminology pass에서 일괄 정리
