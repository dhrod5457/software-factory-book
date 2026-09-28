# Release Candidate 01

기준일: 2026-09-28

## Candidate

- File: `manuscript/book.md`
- Content SHA: `abf5bcea3c2320e34f0c848d28e7ac1c5e4fe92a`
- State: **RC1**
- Structure: **FROZEN**

## Release Proof

PASS:

- Part 7
- Chapter 24
- Missing Chapter 0
- Duplicate Chapter 0
- Section numbering issue 0
- Preface 1
- Epilogue 1
- Glossary 1
- References 1
- Unique Reference entries 53
- Mermaid Figure 21
- Figure ID missing 0
- Case Study Box 14
- Case ID missing 0
- Unclosed Markdown fence 0
- Cross-type fence error 0
- Chapter-level duplicate reference section 0
- TODO / FIXME / TBD / XXX 0
- Replacement character 0
- Tab character 0
- stale `다음 장에서는` transition 0
- stale transition heading 0

## Production Assets

### Figure

- F01~F21 Mermaid source complete
- 21 Figures embedded directly in `book.md`
- 21 captions complete
- `manuscript/figures/render.sh` added for SVG export

### Case Study

- C01~C14 working copy complete
- 14 Boxes embedded in `book.md`
- Vendor / preprint / simulation limitations kept inside relevant boxes

### References

- 53 unique references
- chapter-local duplicate lists removed from assembled manuscript
- source recheck snapshot: `source-recheck-2026-09-28.md`

## 2026-09-28 Current-state Recheck

Confirmed:

- GitHub Stacked Pull Requests: public preview
- NIST Software and AI Agent Identity and Authorization: Draft concept paper + ongoing NCCoE project
- MCP latest specification: 2026-07-28
- Building to the Test: ArXiv preprint
- AgentLens: ArXiv publication
- Wink: ArXiv paper
- Runtime-Structured Task Decomposition: ArXiv paper
- Jules Suggested Tasks: experimental / opt-in
- Google Agent Executor: current durable runtime example
- Backstage AI Catalog: Skill / Rule / MCP Server modeling currently documented

## Remaining Release Gates

RC1은 내용/구조 Release Candidate다.

최종 Release Manuscript 승격 전 남은 작업:

1. 최종 제목 / 부제 결정
2. Mermaid → final SVG/PDF artwork export
3. 인쇄 축소 / 흑백 가독성 확인
4. 53개 Reference 전체 dead-link + metadata pass
5. 사람 기준 최종 교정
6. 최종 PDF/EPUB/DOCX 필요 산출물 build

이후 핵심 논지나 Chapter 구조를 새로 확장하지 않는다.
