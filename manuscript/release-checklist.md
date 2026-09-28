# Release Manuscript Checklist

이 체크리스트는 구조/논지 편집이 끝난 이후 출판용 원고를 만들기 위한 마지막 단계다.

## 1. Figure

- [x] F01~F21 Mermaid source 작성 및 본문 삽입
- [ ] 중복 Figure 통합
- [x] Figure Caption 작성
- [x] 본문 marker와 Mermaid Figure 연결
- [ ] 흑백/축소 인쇄에서도 읽히는지 확인

## 2. Case Study Box

- [x] C01~C14 working copy 작성
- [x] Vendor internal / preprint / simulation 조건 명시
- [ ] 본문과 Case Study 중복 문장 최종 proof에서 확인
- [x] Runmesh는 자체 Case Study로 라벨링

## 3. Copy Proof

- [ ] 오탈자
- [ ] 띄어쓰기
- [ ] 영문 대소문자
- [ ] 한글/영문 괄호
- [ ] 숫자 표기
- [ ] 코드/필드명 monospace 일관성
- [x] Chapter/Section 번호

## 4. References

- [ ] 53개 Reference URL 재확인
- [ ] publication style 결정
- [ ] 날짜/저자/기관 metadata 보강
- [ ] dead link 확인
- [x] duplicate 제거 확인

## 5. Publication-time Source Recheck

- [x] GitHub Stacked PR preview/GA 상태
- [x] NIST Agent Identity draft/final 상태
- [x] 주요 preprint publication status
- [x] 주요 current product feature status
- [x] MCP latest protocol version
- [ ] vendor-reported metric 변경/정정

## 6. Front Matter

- [ ] 최종 제목
- [ ] 부제
- [ ] 들어가며
- [ ] 대상 독자
- [ ] 책 읽는 법
- [ ] 용어 원칙

## 7. Release Build

- [x] manuscript/book.md RC1 hash 기록
- [ ] Markdown render 확인
- [ ] PDF/EPUB/DOCX 등 필요한 산출물 생성
- [ ] 목차 link / page reference 확인
- [x] Source recheck snapshot 보관

## Release Gate

다음 조건을 모두 만족할 때 release manuscript로 승격한다.

```text
Structure Frozen
+ Copy Proof PASS
+ Figure/Box Complete
+ Source Recheck PASS
+ Reference PASS
= Release Manuscript
```
