# Part VI Draft Review

기준일: 2026-09-28

대상:

- `chapters/20/draft.md`
- `chapters/21/draft.md`

## 판정

**PASS WITH MINOR FOLLOW-UP**

Part VI 역할:

~~~text
20장
Production/CI Signal을 Work로 되돌리는 Closed-loop

21장
기존 Developer Platform Capability를 Agent가 안전하게 사용
~~~

## 20장

유지할 핵심:

- Alert != Task
- Signal → Diagnose → Scope → Risk → Task
- Event-driven != Fully Autonomous
- Product Loop / Factory Loop 분리
- Deduplication / Cooldown / Oscillation Control

후속 line edit:

- Closed-loop 사례가 Self-healing 홍보처럼 읽히지 않도록 현재의 risk boundary 유지
- NIST/Google 등 최신 사례는 final source pass에서 재검증

상태:

**READY FOR REVIEW PHASE**

## 21장

유지할 핵심:

- Platform = Capability Provider
- Factory = Work Flow
- Agent also Platform Consumer
- Golden Path as machine contract
- Catalog as index/context source
- structured error / idempotency / scoped identity

후속 line edit:

- 3장과 중복되는 경계 설명은 최종 편집에서 축약
- Backstage/Kubernetes product detail로 확장하지 않음

상태:

**READY FOR REVIEW PHASE**
