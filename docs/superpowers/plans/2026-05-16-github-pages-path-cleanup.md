# GitHub Pages Path Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize this repository's GitHub Pages output around `docs/` so the public home page, directory entry pages, and Markdown direct links resolve under `/life-cycle/` without 404s.

**Architecture:** Keep `docs/` as the sole Pages publishing root. Update the two existing landing pages to describe the same public URL model, move the public install document into `docs/`, and add lightweight `index.html` files for public document directories so directory URLs resolve instead of 404ing.

**Tech Stack:** Static HTML, Markdown, GitHub Pages

---

### Task 1: Publish the install document inside `docs/`

**Files:**
- Create: `docs/INSTALL.md`
- Modify: `writing/INSTALL.md` (only if needed to point readers to the published path)

- [ ] **Step 1: Copy the current install document content into the published path**

```md
# ✍️ 글쓰기 12단계 스킬 — 설치 안내

이 패키지는 Claude Code에서 글쓰기 12단계 워크플로우를 자동화하는 스킬 모음입니다. 다음 절차로 5분 안에 설치할 수 있습니다.
```

Create `docs/INSTALL.md` with the same body as `writing/INSTALL.md` so the public URL becomes `/life-cycle/INSTALL.md`.

- [ ] **Step 2: Verify the published install file exists in the Pages root**

Run: `ls "docs/INSTALL.md"`
Expected: prints `docs/INSTALL.md`

- [ ] **Step 3: Optionally point the source copy at the published copy**

If you keep `writing/INSTALL.md`, append one short note near the top:

```md
> 공개 링크: `/life-cycle/INSTALL.md`
```

Skip this step if keeping the source copy untouched is clearer.

- [ ] **Step 4: Commit**

```bash
git add docs/INSTALL.md writing/INSTALL.md
git commit -m "fix: publish install guide under docs"
```

### Task 2: Normalize the public home pages

**Files:**
- Modify: `docs/index.html`
- Modify: `index.html`

- [ ] **Step 1: Update `docs/index.html` to link only to published paths**

Replace the links section so it includes the public install guide and public spec index, for example:

```html
<div class="links">
  <a href="essay.html">에세이 보기 — 인생의 점을 잇다</a>
  <a href="INSTALL.md">설치 안내 보기</a>
  <a href="superpowers/specs/">설계 문서 모음 보기</a>
</div>
```

Keep the existing `/life-cycle/` example note and remove any references to non-published paths.

- [ ] **Step 2: Update the root `index.html` to match the Pages model**

Change the root landing page copy so it no longer advertises `tmp_review_files/...` or other non-published files. Use the same published links as `docs/index.html`, for example:

```html
<div class="links">
  <a href="docs/index.html">GitHub Pages 홈 보기</a>
  <a href="docs/essay.html">에세이 보기</a>
  <a href="docs/INSTALL.md">설치 안내 보기</a>
  <a href="docs/superpowers/specs/">설계 문서 모음 보기</a>
</div>
```

- [ ] **Step 3: Verify both landing pages reference only real files**

Run: `python - <<'PY'
from pathlib import Path
for path in [Path('docs/index.html'), Path('index.html')]:
    text = path.read_text(encoding='utf-8')
    for ref in ['tmp_review_files/', 'writing/INSTALL.md', 'docs/superpowers/specs/2026-04-26-saju-diary-no-api-summary-for-kids.md']:
        print(path, ref, ref in text)
PY`
Expected: `False` for non-published path checks that were removed.

- [ ] **Step 4: Commit**

```bash
git add docs/index.html index.html
git commit -m "fix: align home pages with published urls"
```

### Task 3: Add directory index pages for public docs

**Files:**
- Create: `docs/superpowers/index.html`
- Create: `docs/superpowers/specs/index.html`

- [ ] **Step 1: Create `docs/superpowers/index.html`**

Use a minimal static page with links to the specs directory and any other public document groups, for example:

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Superpowers Docs</title>
</head>
<body>
  <h1>Superpowers 문서</h1>
  <ul>
    <li><a href="specs/">설계 문서 모음</a></li>
  </ul>
</body>
</html>
```

- [ ] **Step 2: Create `docs/superpowers/specs/index.html`**

List the public spec files that should be browsable from the directory URL, for example:

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Spec Index</title>
</head>
<body>
  <h1>설계 문서 모음</h1>
  <ul>
    <li><a href="2026-04-26-saju-diary-no-api-design.md">사주 일기 설계 문서</a></li>
    <li><a href="2026-04-26-saju-diary-no-api-summary-for-kids.md">쉬운 요약 문서</a></li>
    <li><a href="2026-04-26-saju-diary-security-consistency-design.md">보안 일관성 설계 문서</a></li>
    <li><a href="2026-05-16-saju-flask-app-completion-design.md">사주 Flask 앱 완성 설계서</a></li>
    <li><a href="2026-05-16-github-pages-path-cleanup-design.md">GitHub Pages 경로 정리 설계서</a></li>
  </ul>
</body>
</html>
```

- [ ] **Step 3: Verify the new directory index files exist**

Run: `ls "docs/superpowers/index.html" "docs/superpowers/specs/index.html"`
Expected: both file paths print.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/index.html docs/superpowers/specs/index.html
git commit -m "fix: add public index pages for docs directories"
```

### Task 4: Verify the Pages path model locally

**Files:**
- Test: `docs/index.html`
- Test: `docs/INSTALL.md`
- Test: `docs/superpowers/index.html`
- Test: `docs/superpowers/specs/index.html`

- [ ] **Step 1: Check that every published target file exists**

Run: `python - <<'PY'
from pathlib import Path
paths = [
    Path('docs/index.html'),
    Path('docs/essay.html'),
    Path('docs/INSTALL.md'),
    Path('docs/superpowers/index.html'),
    Path('docs/superpowers/specs/index.html'),
    Path('docs/superpowers/specs/2026-05-16-saju-flask-app-completion-design.md'),
]
for path in paths:
    print(path, path.exists())
PY`
Expected: every line ends with `True`.

- [ ] **Step 2: Check that `docs/index.html` points at the intended published links**

Run: `python - <<'PY'
from pathlib import Path
text = Path('docs/index.html').read_text(encoding='utf-8')
for ref in ['essay.html', 'INSTALL.md', 'superpowers/specs/']:
    print(ref, ref in text)
PY`
Expected: every line ends with `True`.

- [ ] **Step 3: Optionally preview with a local static server**

Run: `python -m http.server 8000 --directory docs`
Expected: local preview is available at `http://localhost:8000/`

Then manually open:
- `http://localhost:8000/`
- `http://localhost:8000/INSTALL.md`
- `http://localhost:8000/superpowers/`
- `http://localhost:8000/superpowers/specs/`

- [ ] **Step 4: Commit**

```bash
git add docs/index.html docs/INSTALL.md docs/superpowers/index.html docs/superpowers/specs/index.html index.html
git commit -m "test: verify published github pages paths"
```
