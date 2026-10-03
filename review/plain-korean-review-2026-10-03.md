# 쉬운 한국어 편집 검증 — Software Factory

- 기준 커밋: `a812a23bf03c85f94ae109414e43df8ced795d78`
- 편집 범위: 24장 전체, 에필로그, 서문, 용어집, 사례 상자, 도식 설명 및 조립본.
- 전문용어를 문맥에 맞게 설명하고 문장을 연결했다. 장 제목, 코드, 수치, URL은 원본대로 유지했다. 독립 검토에서 발견한 조사 오류·중복·고유명사 손상도 교정했다.
- 원본 29개 파일에서 코드 블록, 제목, URL 목록, 숫자 출현 횟수 대조를 통과했다. 이 검사는 의미 동일성을 자동으로 보장하지 않으므로 변경 문장 직접 검토와 함께 수행했다.
- 조립본은 최신 장별 원본보다 오래된 상태였다. `manuscript/assemble_book.py`로 원본 전체를 다시 반영했다. 아래 목록은 새 내용 집필이 아니라 기존 원본과의 동기화다. 이 중 `다음 질문` 21개 제목은 README에 기록된 기존 조립본의 의도된 소제목 생략을 원본 장구조에 다시 맞춘 것이며, 실수성 누락으로 분류하지 않는다. 나머지 12개는 최신 원본에 있는 절의 조립 누락 복원이다.
- 조립 본문 27개 구간(24장·서문·에필로그·용어집)이 원본과 일치한다. 대조에서 출판용 도식·사례 상자, 제목의 깊이, 구분선과 공백만 정규화했다. 장별 참고 자료는 통합 참고문헌에 모으고 모든 원본 URL 포함을 별도로 검사했다.
- 기존 도식 21개와 사례 16개의 식별자, 기존 조립본의 모든 URL을 보존했다. 원본에 이미 있는 C16 사례는 중복 삽입하지 않았다.
- 제목 수는 465개에서 498개로 증가했다. 원본 코드 자체는 변경하지 않았다. 조립본에 남아 있던 이전 코드 설명 4개는 최신 장별 원본으로 동기화했으며, 이전 본문은 JSON의 `original_book_code_variants_superseded`에 기록했다.
- 조립 스크립트 연속 실행 결과가 동일함을 확인했다. Pandoc HTML 변환 및 `git diff --check`를 통과했다. PDF는 검증하지 않았다. 최종 HTML/EPUB 미리보기는 상위 작업에서 별도 생성한다.

## 원본과 동기화한 제목과 절

- 3장: 다음 질문
- 4장: WorkOS: 빈 문서를 Agent가 먼저 채우고 사람이 Scope를 결정한다; 다음 질문
- 5장: 다음 질문
- 6장: 다음 질문
- 7장: 다음 질문
- 8장: Prepared Snapshot과 Fresh Task State; 다음 질문
- 9장: 9.10 Context, Capability, Outcome, Guardrail, Evidence; 다음 질문
- 10장: 다음 질문
- 11장: 모든 Triage에 LLM이 필요한 것은 아니다; 다음 질문
- 12장: 다음 질문
- 13장: 다음 질문
- 14장: 다음 질문
- 15장: 15.11 Persistent Agent, Persistent Worker, Durable Task를 구분한다; 다음 질문
- 16장: 다음 질문
- 17장: 17.10 Role Separation은 Task Independence가 아니다; 다음 질문
- 18장: 다음 질문
- 19장: Human-facing Observability와 Telemetry는 다르다; 다음 질문
- 20장: 20.10 Routine은 Trigger이고 Task는 Work다; 다음 질문
- 21장: 21.11 Agent Execution Golden Path; 다음 질문
- 22장: 다음 질문
- 23장: 작은 구현 사례: GitHub-native Hub-and-Spoke; 23.9 Operator Surface; 다음 질문
- 24장: Learned Skill은 Candidate로 시작한다

## 재검증

저장소 루트에서 `python3 manuscript/assemble_book.py`와 `python3 review/validate_plain_korean.py`를 실행한다. 검증은 고정 기준 커밋을 사용한다. 자동 비교 결과는 `plain-korean-validation-2026-10-03.json`에 저장된다.
