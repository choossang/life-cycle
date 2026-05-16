# 글쓰기 스킬 패키지 완성 설계서

작성일: 2026-05-16
범위: `.claude/skills/`, `writing/INSTALL.md`, `writing/writing-skills.zip` 패키지 정합성 완성
목표: source 자산, zip 배포물, 설치 문서가 서로 모순 없이 배포 가능한 패키지 상태가 되도록 정리한다.

## 1. 목표와 완료 정의

### 목표
- 글쓰기 12단계 스킬 패키지의 실제 자산과 설치 문서가 일치하도록 맞춘다.
- 배포용 zip이 문서에서 설명하는 구조를 실제로 담고 있게 한다.
- worktree에서도 패키지 실체를 확인할 수 있는 상태로 만든다.

### 완료 정의
다음이 모두 충족되면 이 트랙을 완료로 본다.
1. worktree에 `.claude/skills/` 자산이 반영되어 있다.
2. `writing/INSTALL.md` 설명이 실제 패키지 구조와 일치한다.
3. `writing/writing-skills.zip` 내부 구조가 설치 문서 설명과 일치한다.
4. 스킬 폴더 수, 각 `SKILL.md`, 샘플 문서 존재 여부를 검증할 수 있다.
5. source 자산, zip 배포물, 설치 문서가 서로 모순되지 않는다.

## 2. 현재 상태 요약

### source tree
- `.claude/skills/` 아래에 13개 스킬 폴더와 `README.md`가 존재한다.
- `writing/INSTALL.md`와 `writing/writing-skills.zip`이 존재한다.

### current worktree
- `writing/INSTALL.md`와 `writing/writing-skills.zip`은 존재한다.
- `.claude/skills/` 패키지 자산은 아직 worktree에 반영되어 있지 않다.
- 따라서 설치 문서가 설명하는 패키지 실체와 현재 worktree 상태가 어긋나 있다.

## 3. 패키지 구성 설계

패키지 기준 실체를 다음처럼 잡는다.

1. `.claude/skills/`
   - 실제 스킬 자산의 기준 원본
   - 13개 스킬 폴더와 `README.md` 포함

2. `writing/INSTALL.md`
   - 사용자가 zip을 받아 설치하는 절차 설명
   - 패키지 구조와 검증 항목 정의

3. `writing/writing-skills.zip`
   - 배포용 압축 산출물
   - `.claude/skills/`, 샘플 문서, 설치 안내 구조를 실제로 담아야 함

즉, `.claude/skills/`가 원본 자산, zip은 배포 산출물, `writing/INSTALL.md`는 설치 절차 문서 역할을 맡는다.

## 4. 정합성 원칙

- 문서가 설명하는 경로와 실제 zip 내부 경로는 같아야 한다.
- source `.claude/skills/`와 zip 내용이 어긋나면 source를 기준으로 zip을 다시 만든다.
- `writing/INSTALL.md`는 상위 저장소 안내를 반복하지 않고 패키지 설치에만 집중한다.
- 루트 `INSTALL.md`와 `docs/index.html`은 패키지 진입 링크만 제공하고, 설치 절차 자체는 `writing/INSTALL.md`로 위임한다.

## 5. 배포 패키지 설계

zip 내부 기대 구조는 문서 설명과 동일해야 한다.

```text
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
└── INSTALL.md
```

이 구조가 zip 안에 실제로 존재하는지 검증하고, 다르면 zip을 재구성한다.

## 6. 작업 순서

1. source tree의 `.claude/skills/`를 current worktree에 반영한다.
2. source와 worktree의 스킬 자산 구조가 일치하는지 확인한다.
3. `writing/writing-skills.zip` 내부 목록을 검사한다.
4. zip이 문서 설명과 다르면 source 자산 기준으로 zip을 다시 만든다.
5. `writing/INSTALL.md`의 설명과 검증 항목을 현재 패키지 기준으로 보정한다.
6. 설치 안내에 나온 점검 항목을 실제로 검증한다.

## 7. 검증 전략

다음을 확인한다.
- `.claude/skills/` 아래 13개 스킬 폴더가 존재하는가
- 각 스킬 폴더 안에 `SKILL.md`가 존재하는가
- `.claude/skills/README.md`가 존재하는가
- 샘플 문서 `docs/6.나의글샘플.txt`, `docs/9.첨삭샘플.txt`, `docs/10.퇴고샘플.txt`가 존재하는가
- zip 내부 파일 목록이 설치 문서 설명과 일치하는가
- `writing/INSTALL.md`의 확인 프롬프트가 현재 패키지 구조에 맞는가

## 8. 비범위

이번 트랙에서는 다음을 하지 않는다.
- 스킬 내용 자체의 대규모 개편
- 새 글쓰기 단계 추가
- Claude Code 외 플랫폼용 설치 방식 추가
- 패키지 브랜딩/디자인 리뉴얼

## 9. 결정 기록

1. 글쓰기 스킬 패키지는 배포 패키지까지 포함해 완성한다.
2. source `.claude/skills/`를 기준 원본으로 삼는다.
3. zip과 설치 문서가 원본 자산 구조를 정확히 반영하도록 맞춘다.
