# Docs and Deployment Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the repository entry points, public docs hub, and install guides so users can understand the project quickly and navigate to the right materials without duplicated or conflicting guidance.

**Architecture:** Keep the existing file set and HTML style lightweight, but separate responsibilities clearly: root `index.html` becomes the repository hub, `docs/index.html` becomes the public Pages/docs hub, root `INSTALL.md` becomes the repository usage guide, and `writing/INSTALL.md` remains the package-specific installer. Bring missing source-only files into the current worktree first so the implementation can update the real deliverables rather than writing around absent assets.

**Tech Stack:** Static HTML, Markdown, Git worktree workflow, Python stdlib for optional link checks

---

## File Structure Map

- Create in worktree from source copy: `INSTALL.md`
  - Repository-level usage/install guide for this repo.
- Create in worktree from source copy: `writing/INSTALL.md`
  - Package-specific install guide for writing skills.
- Create in worktree from source copy: `writing/writing-skills.zip`
  - Packaged writing skills archive referenced by install docs.
- Modify: `index.html`
  - Root repository hub page with three clear navigation lanes.
- Modify: `docs/index.html`
  - Public Pages/docs hub page with public-facing artifact links.
- Modify if needed: `INSTALL.md`
  - Refine copied repository guide to remove overlap and align links.
- Modify if needed: `writing/INSTALL.md`
  - Minimal wording/link cleanup so it fits the new hub structure.

---

### Task 1: Bring missing documentation assets into the worktree

**Files:**
- Create: `INSTALL.md`
- Create: `writing/INSTALL.md`
- Create: `writing/writing-skills.zip`
- Test: `INSTALL.md`, `writing/INSTALL.md`, `writing/writing-skills.zip`

- [ ] **Step 1: Write the failing verification script**

Create a temporary verification script at `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_docs_assets.py` with this content:

```python
from pathlib import Path

ROOT = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion")
required = [
    ROOT / "INSTALL.md",
    ROOT / "writing" / "INSTALL.md",
    ROOT / "writing" / "writing-skills.zip",
]

missing = [str(path) for path in required if not path.exists()]
if missing:
    raise SystemExit("MISSING:\n" + "\n".join(missing))

print("ALL_PRESENT")
```

- [ ] **Step 2: Run the script to verify it fails**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_docs_assets.py"
```

Expected: FAIL with `MISSING:` entries for `INSTALL.md` and the `writing/` files because those assets are not yet present in the worktree.

- [ ] **Step 3: Copy the missing assets into the current worktree**

Run:

```bash
mkdir -p "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/writing" && cp "C:/Users/user/Desktop/workspaces/day4-writting/INSTALL.md" "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/INSTALL.md" && cp "C:/Users/user/Desktop/workspaces/day4-writting/writing/INSTALL.md" "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/writing/INSTALL.md" && cp "C:/Users/user/Desktop/workspaces/day4-writting/writing/writing-skills.zip" "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/writing/writing-skills.zip"
```

- [ ] **Step 4: Run the verification script again**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_docs_assets.py"
```

Expected: PASS with output `ALL_PRESENT`.

- [ ] **Step 5: Commit**

Run:

```bash
git add "INSTALL.md" "writing/INSTALL.md" "writing/writing-skills.zip"
git commit -m "$(cat <<'EOF'
chore: restore docs and writing package assets to worktree

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Rebuild the root repository hub page

**Files:**
- Modify: `index.html`
- Test: `index.html`

- [ ] **Step 1: Write the failing content check**

Create `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_root_index.py` with this content:

```python
from pathlib import Path

html = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/index.html").read_text(encoding="utf-8")
required = [
    "공개 페이지 / 문서",
    "Flask 사주 앱 산출물",
    "글쓰기 스킬 패키지",
    "docs/index.html",
    "tmp_review_files/flask_saju_app_v3/flask_app/",
    "INSTALL.md",
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit("MISSING:\n" + "\n".join(missing))
print("ROOT_INDEX_OK")
```

- [ ] **Step 2: Run the check to verify it fails**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_root_index.py"
```

Expected: FAIL because the current root page does not yet present the three-lane repository hub structure.

- [ ] **Step 3: Replace the root hub page**

Overwrite `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/index.html` with this content:

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Life Cycle Repository Hub</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; background: #0b1220; color: #e6edf3; }
    .wrap { max-width: 960px; margin: 48px auto; padding: 0 20px; }
    .hero, .card { background: #111a2b; border: 1px solid #26334d; border-radius: 14px; }
    .hero { padding: 28px; margin-bottom: 22px; }
    .grid { display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
    .card { padding: 20px; }
    h1 { margin: 0 0 10px; font-size: 30px; }
    h2 { margin: 0 0 10px; font-size: 18px; }
    p, li { color: #b7c3d4; line-height: 1.6; }
    a { color: #9cd1ff; }
    .link-list { display: grid; gap: 10px; margin-top: 14px; }
    .link-list a { display: block; text-decoration: none; background: #0f1728; border: 1px solid #2b3a58; padding: 12px 14px; border-radius: 10px; }
    .link-list a:hover { border-color: #4ea1ff; }
    .note { margin-top: 18px; font-size: 13px; color: #9fb0c6; }
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>Life Cycle</h1>
      <p>이 저장소는 공개 문서, Flask 사주 앱 산출물, 글쓰기 스킬 패키지를 함께 담고 있는 작업 허브입니다.</p>
      <p class="note">원하는 목적에 따라 아래 세 갈래 중 하나로 바로 이동하세요.</p>
    </section>

    <section class="grid">
      <article class="card">
        <h2>공개 페이지 / 문서</h2>
        <p>GitHub Pages에서 바로 볼 수 있는 공개 문서와 산출물 허브입니다.</p>
        <div class="link-list">
          <a href="docs/index.html">docs/index.html 열기</a>
        </div>
      </article>

      <article class="card">
        <h2>Flask 사주 앱 산출물</h2>
        <p>사주 앱 구현물, 설계 문서, 템플릿 파일이 모여 있는 작업 영역입니다.</p>
        <div class="link-list">
          <a href="tmp_review_files/flask_saju_app_v3/flask_app/">Flask 앱 디렉터리 보기</a>
          <a href="docs/superpowers/specs/2026-05-16-saju-flask-app-completion-design.md">사주 앱 설계서 보기</a>
        </div>
      </article>

      <article class="card">
        <h2>글쓰기 스킬 패키지</h2>
        <p>Claude Code용 글쓰기 12단계 스킬 패키지와 설치 안내입니다.</p>
        <div class="link-list">
          <a href="INSTALL.md">저장소 사용 안내 보기</a>
          <a href="writing/INSTALL.md">패키지 설치 안내 보기</a>
        </div>
      </article>
    </section>
  </div>
</body>
</html>
```

- [ ] **Step 4: Run the content check again**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_root_index.py"
```

Expected: PASS with output `ROOT_INDEX_OK`.

- [ ] **Step 5: Commit**

Run:

```bash
git add "index.html"
git commit -m "$(cat <<'EOF'
feat: turn root page into repository hub

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Expand the public docs hub page

**Files:**
- Modify: `docs/index.html`
- Test: `docs/index.html`

- [ ] **Step 1: Write the failing docs-hub check**

Create `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_docs_index.py` with this content:

```python
from pathlib import Path

html = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/docs/index.html").read_text(encoding="utf-8")
required = [
    "에세이",
    "사주 관련 설계 문서",
    "글쓰기 스킬 설치 안내",
    "essay.html",
    "superpowers/specs/2026-05-16-saju-flask-app-completion-design.md",
    "../writing/INSTALL.md",
]
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit("MISSING:\n" + "\n".join(missing))
print("DOCS_INDEX_OK")
```

- [ ] **Step 2: Run the check to verify it fails**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_docs_index.py"
```

Expected: FAIL because the current docs page only links to the essay.

- [ ] **Step 3: Replace the docs hub page**

Overwrite `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/docs/index.html` with this content:

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Life Cycle — Public Docs</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; background: #0b1220; color: #e6edf3; }
    .wrap { max-width: 920px; margin: 48px auto; padding: 0 20px; }
    .card { background: #111a2b; border: 1px solid #26334d; border-radius: 14px; padding: 24px; }
    .grid { display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); margin-top: 18px; }
    .item { background: #0f1728; border: 1px solid #2b3a58; border-radius: 12px; padding: 18px; }
    h1 { margin: 0 0 10px; font-size: 28px; }
    h2 { margin: 0 0 8px; font-size: 18px; }
    p { color: #b7c3d4; line-height: 1.6; }
    a { color: #9cd1ff; }
    .item a { text-decoration: none; }
    .back { display: inline-block; margin-top: 18px; font-size: 14px; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>Life Cycle Public Docs</h1>
      <p>공개적으로 바로 볼 수 있는 문서와 산출물을 모아 둔 허브입니다.</p>

      <div class="grid">
        <section class="item">
          <h2>에세이</h2>
          <p>공개 페이지로 정리된 에세이를 바로 읽습니다.</p>
          <a href="essay.html">essay.html 열기</a>
        </section>

        <section class="item">
          <h2>사주 관련 설계 문서</h2>
          <p>사주 앱 설계와 관련된 최신 문서를 확인합니다.</p>
          <a href="superpowers/specs/2026-05-16-saju-flask-app-completion-design.md">사주 앱 완성 설계서 보기</a>
        </section>

        <section class="item">
          <h2>글쓰기 스킬 설치 안내</h2>
          <p>글쓰기 12단계 스킬 패키지를 설치하고 시작하는 방법입니다.</p>
          <a href="../writing/INSTALL.md">writing/INSTALL.md 보기</a>
        </section>
      </div>

      <a class="back" href="../index.html">← 저장소 허브로 돌아가기</a>
    </div>
  </div>
</body>
</html>
```

- [ ] **Step 4: Run the docs-hub check again**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_docs_index.py"
```

Expected: PASS with output `DOCS_INDEX_OK`.

- [ ] **Step 5: Commit**

Run:

```bash
git add "docs/index.html"
git commit -m "$(cat <<'EOF'
feat: expand public docs hub links

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Rewrite the repository-level INSTALL guide

**Files:**
- Modify: `INSTALL.md`
- Test: `INSTALL.md`

- [ ] **Step 1: Write the failing install-guide check**

Create `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_root_install.py` with this content:

```python
from pathlib import Path

md = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/INSTALL.md").read_text(encoding="utf-8")
required = [
    "저장소 개요",
    "주요 디렉터리 안내",
    "공개 문서 위치",
    "Flask 사주 앱 관련 위치",
    "글쓰기 스킬 패키지 위치",
    "writing/INSTALL.md",
]
missing = [item for item in required if item not in md]
if missing:
    raise SystemExit("MISSING:\n" + "\n".join(missing))
print("ROOT_INSTALL_OK")
```

- [ ] **Step 2: Run the check to verify it fails**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_root_install.py"
```

Expected: FAIL because the copied root install document is still package-centric instead of repository-centric.

- [ ] **Step 3: Replace the root install guide**

Overwrite `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/INSTALL.md` with this content:

```markdown
# 저장소 사용 안내

이 저장소는 세 가지 흐름을 함께 담고 있습니다.

1. 공개 문서와 에세이
2. Flask 사주 앱 산출물
3. Claude Code용 글쓰기 스킬 패키지

---

## 저장소 개요

이 저장소는 단일 애플리케이션 배포본만 담는 구조가 아니라, 여러 작업 산출물을 함께 보관하는 작업 허브입니다. 따라서 먼저 어떤 목적로 들어왔는지 정한 뒤 맞는 경로로 이동하는 것이 가장 빠릅니다.

## 주요 디렉터리 안내

- `index.html` — 저장소 허브 시작 화면
- `docs/` — 공개 문서와 Pages용 산출물
- `tmp_review_files/flask_saju_app_v3/flask_app/` — Flask 사주 앱 관련 파일
- `writing/` — 글쓰기 스킬 패키지와 설치 자료
- `writing-workspace/` — 글쓰기 워크플로우 산출물 예시

## 공개 문서 위치

공개 문서와 페이지는 아래에서 시작하세요.

- `docs/index.html`
- `docs/essay.html`

## Flask 사주 앱 관련 위치

사주 앱 관련 산출물은 아래에서 확인하세요.

- `tmp_review_files/flask_saju_app_v3/flask_app/app.py`
- `tmp_review_files/flask_saju_app_v3/flask_app/templates/index.html`
- `docs/superpowers/specs/2026-05-16-saju-flask-app-completion-design.md`

## 글쓰기 스킬 패키지 위치

글쓰기 스킬 패키지 자체를 설치하려면 아래 문서를 보세요.

- `writing/INSTALL.md`
- `writing/writing-skills.zip`

루트 문서인 이 파일은 저장소 전체 안내만 담당합니다. 패키지 설치 단계는 `writing/INSTALL.md`를 기준으로 진행하세요.
```

- [ ] **Step 4: Run the install-guide check again**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_root_install.py"
```

Expected: PASS with output `ROOT_INSTALL_OK`.

- [ ] **Step 5: Commit**

Run:

```bash
git add "INSTALL.md"
git commit -m "$(cat <<'EOF'
docs: rewrite repository install guide

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Align the package install guide and verify links

**Files:**
- Modify if needed: `writing/INSTALL.md`
- Test: `index.html`, `docs/index.html`, `INSTALL.md`, `writing/INSTALL.md`

- [ ] **Step 1: Write the failing link verification script**

Create `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_docs_links.py` with this content:

```python
from pathlib import Path
import re

ROOT = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion")
checks = {
    ROOT / "index.html": [
        "docs/index.html",
        "tmp_review_files/flask_saju_app_v3/flask_app/",
        "INSTALL.md",
        "writing/INSTALL.md",
    ],
    ROOT / "docs" / "index.html": [
        "essay.html",
        "superpowers/specs/2026-05-16-saju-flask-app-completion-design.md",
        "../writing/INSTALL.md",
        "../index.html",
    ],
    ROOT / "INSTALL.md": [
        "writing/INSTALL.md",
        "writing/writing-skills.zip",
    ],
}

for file_path, required in checks.items():
    text = file_path.read_text(encoding="utf-8")
    for item in required:
        if item not in text:
            raise SystemExit(f"MISSING in {file_path.name}: {item}")

writing_install = (ROOT / "writing" / "INSTALL.md").read_text(encoding="utf-8")
if "글쓰기 12단계 스킬" not in writing_install:
    raise SystemExit("writing INSTALL lost package-specific focus")

print("DOC_LINKS_OK")
```

- [ ] **Step 2: Run the script to verify current gaps**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_docs_links.py"
```

Expected: it may FAIL before the package guide is aligned or before all hub links are in place.

- [ ] **Step 3: Apply minimal package-guide cleanup if needed**

If the link check fails because `writing/INSTALL.md` needs a repository-level pointer, add this section right after the opening paragraph in `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/writing/INSTALL.md`:

```markdown
> 저장소 전체 안내가 필요하면 상위 문서인 `../INSTALL.md`를 먼저 확인하세요. 이 문서는 글쓰기 12단계 스킬 패키지 설치만 다룹니다.
```

If the check already passes without this addition, do not change `writing/INSTALL.md`.

- [ ] **Step 4: Run the link verification script again**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_docs_links.py"
```

Expected: PASS with output `DOC_LINKS_OK`.

- [ ] **Step 5: Commit**

If `writing/INSTALL.md` changed, run:

```bash
git add "writing/INSTALL.md"
git commit -m "$(cat <<'EOF'
docs: align package install guide with repository hub

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

If no file content changed in this task, skip the commit and note that verification passed without doc edits.

---

## Self-Review Notes

- **Spec coverage:**
  - Missing source-only assets brought into worktree: Task 1
  - Root repository hub: Task 2
  - Public docs hub: Task 3
  - Repository-level install guide: Task 4
  - Package-guide alignment + cross-link verification: Task 5
- **Placeholder scan:** No TODO/TBD placeholders remain in the plan.
- **Type consistency:** Paths and roles are consistent across `index.html`, `docs/index.html`, `INSTALL.md`, and `writing/INSTALL.md`.
