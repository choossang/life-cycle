# ✍️ 글쓰기 12단계 워크플로우 스킬 패키지

작가가 백지에서 발행까지 가는 12단계를 각각 독립된 Claude Code 스킬로 구현하고, 메타 오케스트레이터(`writing-orchestrator`)가 이들을 유기적으로 연결합니다.

## 📚 스킬 목록

| 단계 | 스킬 | 핵심 활동 |
|---|---|---|
| 0 | `writing-orchestrator` ⭐ | 메타 — 단계 판단·진행률·스킬 호출 |
| 1 | `cartesian-doubt` | 생각/구상 — 데카르트적 의심 |
| 2 | `socratic-method` | 주제 정하기 — 산파술 |
| 3 | `material-curation` | 자료 준비 — 3채널 수집 |
| 4 | `structural-logic` | 정리 — 우선순위 분류 |
| 5 | `blueprint-outline` | 목차 — 3가지 구조 비교 |
| 6 | `voice-persona` | 문체 — 페르소나 카드 |
| 7 | `drafting-sprint` | 초안 — 10분 스프린트 / AI 초안 |
| 8 | `self-correction` | 다듬기 — 리듬 점검 |
| 9 | `master-critique` | 첨삭 — 거장 페르소나 |
| 10 | `polishing-refining` | 퇴고 — 번역투·중언부언 잡기 |
| 11 | `final-touch` | 완성 — 제목·체크리스트 |
| 12 | `publishing-meta` | 발행 — 플랫폼별 패키지 |

## 🚀 시작하기

설치 후 Claude Code에서 다음 중 하나를 입력하면 자동으로 워크플로우가 시작됩니다:

- "글쓰기 시작할래"
- "에세이 한 편 쓰고 싶어"
- "주제를 못 정하겠어"
- "초안 다듬어 줘"

오케스트레이터가 입력을 분석해 적절한 단계를 호출하고 진행률을 트래킹합니다.

## 📁 작업 산출물

원하면 각 단계의 결과를 `./writing-workspace/01-doubt.md` ~ `12-publish-package.md` 형식으로 저장해 다음 세션에서 이어 쓸 수 있습니다.

## 📦 기본 샘플 (선택)

다음 샘플은 입력값이 없을 때 자동으로 사용됩니다:
- `docs/6.나의글샘플.txt` — 6단계 문체 분석용
- `docs/9.첨삭샘플.txt` — 9단계 첨삭 페르소나용
- `docs/10.퇴고샘플.txt` — 10단계 퇴고 기준용

## 🔧 설치

`INSTALL.md` 파일을 참고하세요.
