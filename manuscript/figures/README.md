# Manuscript Figures

AI Software Factory 원고의 출판용 Figure source.

## 원칙

- Source format: Mermaid (`.mmd`)
- Canonical ID: F01~F21
- Caption source: `../figure-captions.md`
- Placement source: `../book.md`
- Render output: `rendered/*.svg`

Figure source는 특정 출판 툴에 종속되지 않게 텍스트로 유지한다.

## Mapping

| ID | File | Chapter |
| --- | --- | --- |
| F01 | F01-model-agent-factory.mmd | 1 |
| F02 | F02-reference-loop.mmd | 2 |
| F03 | F03-work-artifact-traceability.mmd | 4 |
| F04 | F04-task-attempt-worker.mmd | 5 |
| F05 | F05-control-execution-plane.mmd | 7 |
| F06 | F06-worker-isolation-boundary.mmd | 8 |
| F07 | F07-harness-context-runtime.mmd | 9 |
| F08 | F08-controlled-autonomy-stack.mmd | 11 |
| F09 | F09-verification-pyramid.mmd | 12 |
| F10 | F10-evidence-vs-provenance.mmd | 13 |
| F11 | F11-recovery-ladder.mmd | 14 |
| F12 | F12-durable-execution-timeline.mmd | 15 |
| F13 | F13-agent-security-delegation.mmd | 16 |
| F14 | F14-parallel-fanout-fanin.mmd | 17 |
| F15 | F15-throughput-bottleneck.mmd | 18 |
| F16 | F16-task-timeline-observability.mmd | 19 |
| F17 | F17-signal-to-task.mmd | 20 |
| F18 | F18-factory-platform.mmd | 21 |
| F19 | F19-minimum-viable-factory.mmd | 22 |
| F20 | F20-reference-factory-scenarios.mmd | 23 |
| F21 | F21-maturity-autonomy.mmd | 24 |

## Render

Mermaid CLI가 설치된 환경에서:

```bash
bash manuscript/figures/render.sh
```

Script는 각 `.mmd`를 같은 basename의 SVG로 변환한다.

## Publication Notes

- 색상은 출판 테마에서 결정한다.
- 흑백 출력에서도 edge와 label만으로 의미가 유지되어야 한다.
- Vendor logo는 사용하지 않는다.
- Figure의 의미가 Mermaid syntax에 종속되지 않게 caption을 별도로 유지한다.
