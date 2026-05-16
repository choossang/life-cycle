# ✍️ 글쓰기 12단계 스킬 — 설치 안내

이 패키지는 Claude Code에서 글쓰기 12단계 워크플로우를 자동화하는 스킬 모음입니다. 다음 절차로 5분 안에 설치할 수 있습니다.

---

## 0. 사전 준비

- Claude Code가 설치되어 있어야 합니다. ([설치 가이드](https://docs.claude.com/en/docs/claude-code))
- Windows / macOS / Linux 모두 지원합니다.

## 1. 받기

`writing-skills.zip` 파일을 다운로드합니다.

## 2. 압축 풀기

원하는 작업 폴더(예: `~/my-writing/`)에 압축을 풉니다. 풀고 나면 다음 구조가 보여야 합니다.

```
my-writing/
├── .claude/
│   └── skills/
│       ├── writing-orchestrator/
│       ├── cartesian-doubt/
│       ├── socratic-method/
│       ├── material-curation/
│       ├── structural-logic/
│       ├── blueprint-outline/
│       ├── voice-persona/
│       ├── drafting-sprint/
│       ├── self-correction/
│       ├── master-critique/
│       ├── polishing-refining/
│       ├── final-touch/
│       ├── publishing-meta/
│       └── README.md
├── docs/
│   ├── 6.나의글샘플.txt
│   ├── 9.첨삭샘플.txt
│   └── 10.퇴고샘플.txt
└── INSTALL.md  (이 문서)
```

## 3. Claude Code 실행

압축을 푼 폴더에서 Claude Code를 엽니다.

```bash
cd ~/my-writing
claude
```

## 4. 설치 확인 — Claude에게 직접 시켜보기

Claude Code 프롬프트 창에 **다음 설치 프롬프트**를 그대로 붙여넣으세요.

````
아래 폴더에 글쓰기 12단계 스킬 패키지가 설치되어 있는지 확인해줘.

확인 항목:
1) `.claude/skills/` 하위에 13개의 스킬 폴더(`writing-orchestrator` 외 12개)가 모두 존재하는가?
2) 각 폴더 안에 `SKILL.md` 파일이 있는가?
3) `docs/` 폴더에 `6.나의글샘플.txt`, `9.첨삭샘플.txt`, `10.퇴고샘플.txt` 세 개의 기본 샘플이 있는가?

확인 후, 결과를 표로 정리해줘. 누락이 있으면 알려주고, 모두 정상이면 "글쓰기 워크플로우 시작 가능" 메시지를 보여줘.
그리고 Claude Code의 스킬 자동 인식이 동작하는지 테스트하려면 어떤 문장을 입력하면 되는지도 알려줘.
````

설치가 정상이면 Claude가 표로 확인해주고, 다음과 같은 시작 문장을 알려줄 겁니다:

- "글쓰기 시작할래"
- "주제를 못 정하겠어"
- "초안을 다듬고 싶어"

## 5. 첫 워크플로우 시작

설치가 끝나면 다음 한 문장으로 시작합니다.

```
글쓰기 시작할래. 첫 단계부터 안내해줘.
```

오케스트레이터(`writing-orchestrator`)가 자동으로 호출되어 1~12단계를 안내합니다.

---

## 🩺 자주 묻는 질문

**Q1. 스킬이 자동 호출되지 않아요.**
- `.claude/skills/` 폴더 위치가 프로젝트 루트가 맞는지 확인하세요.
- Claude Code를 재시작하세요. (`/exit` 후 다시 `claude`)

**Q2. 전역으로 설치하고 싶어요.**
- `.claude/skills/` 폴더 전체를 `~/.claude/skills/`로 복사하면 모든 프로젝트에서 사용할 수 있습니다.
  - macOS/Linux: `cp -r .claude/skills ~/.claude/`
  - Windows (PowerShell): `Copy-Item -Recurse .claude\skills $env:USERPROFILE\.claude\`

**Q3. 일부 단계만 쓰고 싶어요.**
- 자연어로 단계를 지정하면 됩니다. 예: "퇴고만 도와줘" → `polishing-refining` 호출.
- 또는 슬래시로 직접 부르세요: `/polishing-refining`

**Q4. 작업 진행 상태를 다음 세션에서도 이어가고 싶어요.**
- 오케스트레이터에게 "산출물을 `writing-workspace/` 폴더에 저장해줘"라고 요청하면 단계별 파일로 저장됩니다.

---

## 📄 라이선스 / 배포

학습용 자료입니다. 자유롭게 수정·재배포하세요.
