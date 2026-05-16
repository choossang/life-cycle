# Writing Skills Package Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the writing-skills package so the source skill assets, the packaged zip file, and the install guide all describe and ship the same deployable structure.

**Architecture:** Treat `.claude/skills/` in the source workspace as the canonical package source, reflect those assets into the current worktree, verify the shipped zip contents against that source, and only rebuild the zip if the archive diverges from the documented package structure. Keep `writing/INSTALL.md` focused on package installation while using simple verification scripts to prove folder counts, `SKILL.md` presence, sample-doc presence, and archive structure.

**Tech Stack:** Markdown, static package assets, Python stdlib (`pathlib`, `zipfile`), Git worktree workflow

---

## File Structure Map

- Create in worktree from source copy: `.claude/skills/README.md`
  - Package-level README included in the distributed skill set.
- Create in worktree from source copy: `.claude/skills/blueprint-outline/SKILL.md`
- Create in worktree from source copy: `.claude/skills/cartesian-doubt/SKILL.md`
- Create in worktree from source copy: `.claude/skills/drafting-sprint/SKILL.md`
- Create in worktree from source copy: `.claude/skills/final-touch/SKILL.md`
- Create in worktree from source copy: `.claude/skills/master-critique/SKILL.md`
- Create in worktree from source copy: `.claude/skills/material-curation/SKILL.md`
- Create in worktree from source copy: `.claude/skills/polishing-refining/SKILL.md`
- Create in worktree from source copy: `.claude/skills/publishing-meta/SKILL.md`
- Create in worktree from source copy: `.claude/skills/self-correction/SKILL.md`
- Create in worktree from source copy: `.claude/skills/socratic-method/SKILL.md`
- Create in worktree from source copy: `.claude/skills/structural-logic/SKILL.md`
- Create in worktree from source copy: `.claude/skills/voice-persona/SKILL.md`
- Create in worktree from source copy: `.claude/skills/writing-orchestrator/SKILL.md`
- Modify if needed: `writing/INSTALL.md`
  - Package-only installation guide aligned to the verified package structure.
- Modify if needed: `writing/writing-skills.zip`
  - Rebuilt only if archive content diverges from the documented package structure.

---

### Task 1: Restore the skill asset tree into the worktree

**Files:**
- Create: `.claude/skills/README.md`
- Create: `.claude/skills/blueprint-outline/SKILL.md`
- Create: `.claude/skills/cartesian-doubt/SKILL.md`
- Create: `.claude/skills/drafting-sprint/SKILL.md`
- Create: `.claude/skills/final-touch/SKILL.md`
- Create: `.claude/skills/master-critique/SKILL.md`
- Create: `.claude/skills/material-curation/SKILL.md`
- Create: `.claude/skills/polishing-refining/SKILL.md`
- Create: `.claude/skills/publishing-meta/SKILL.md`
- Create: `.claude/skills/self-correction/SKILL.md`
- Create: `.claude/skills/socratic-method/SKILL.md`
- Create: `.claude/skills/structural-logic/SKILL.md`
- Create: `.claude/skills/voice-persona/SKILL.md`
- Create: `.claude/skills/writing-orchestrator/SKILL.md`
- Test: `.claude/skills/**/SKILL.md`

- [ ] **Step 1: Write the failing asset-tree verifier**

Create `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_skills_tree.py` with this content:

```python
from pathlib import Path

ROOT = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion")
skills_root = ROOT / ".claude" / "skills"
expected = [
    "README.md",
    "blueprint-outline/SKILL.md",
    "cartesian-doubt/SKILL.md",
    "drafting-sprint/SKILL.md",
    "final-touch/SKILL.md",
    "master-critique/SKILL.md",
    "material-curation/SKILL.md",
    "polishing-refining/SKILL.md",
    "publishing-meta/SKILL.md",
    "self-correction/SKILL.md",
    "socratic-method/SKILL.md",
    "structural-logic/SKILL.md",
    "voice-persona/SKILL.md",
    "writing-orchestrator/SKILL.md",
]
missing = [item for item in expected if not (skills_root / item).exists()]
if missing:
    raise SystemExit("MISSING:\n" + "\n".join(missing))
print("SKILLS_TREE_OK")
```

- [ ] **Step 2: Run the verifier to confirm it fails**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_skills_tree.py"
```

Expected: FAIL with missing entries because the current worktree does not yet contain `.claude/skills/`.

- [ ] **Step 3: Copy the canonical skill tree from the source workspace**

Run:

```bash
mkdir -p "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/.claude" && cp -r "C:/Users/user/Desktop/workspaces/day4-writting/.claude/skills" "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/.claude/skills"
```

- [ ] **Step 4: Re-run the verifier**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_skills_tree.py"
```

Expected: PASS with `SKILLS_TREE_OK`.

- [ ] **Step 5: Commit**

Run:

```bash
git add ".claude/skills"
git commit -m "$(cat <<'EOF'
chore: restore writing skills asset tree to worktree

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Verify the package archive matches the documented structure

**Files:**
- Modify if needed: `writing/writing-skills.zip`
- Test: `writing/writing-skills.zip`

- [ ] **Step 1: Write the failing archive verifier**

Create `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_zip.py` with this content:

```python
from pathlib import Path
import zipfile

ROOT = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion")
zip_path = ROOT / "writing" / "writing-skills.zip"
required = [
    ".claude/skills/README.md",
    ".claude/skills/blueprint-outline/SKILL.md",
    ".claude/skills/cartesian-doubt/SKILL.md",
    ".claude/skills/drafting-sprint/SKILL.md",
    ".claude/skills/final-touch/SKILL.md",
    ".claude/skills/master-critique/SKILL.md",
    ".claude/skills/material-curation/SKILL.md",
    ".claude/skills/polishing-refining/SKILL.md",
    ".claude/skills/publishing-meta/SKILL.md",
    ".claude/skills/self-correction/SKILL.md",
    ".claude/skills/socratic-method/SKILL.md",
    ".claude/skills/structural-logic/SKILL.md",
    ".claude/skills/voice-persona/SKILL.md",
    ".claude/skills/writing-orchestrator/SKILL.md",
    "docs/6.나의글샘플.txt",
    "docs/9.첨삭샘플.txt",
    "docs/10.퇴고샘플.txt",
    "INSTALL.md",
]
with zipfile.ZipFile(zip_path) as zf:
    names = set(zf.namelist())
missing = [item for item in required if item not in names]
if missing:
    raise SystemExit("MISSING:\n" + "\n".join(missing))
print("WRITING_ZIP_OK")
```

- [ ] **Step 2: Run the archive verifier**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_zip.py"
```

Expected:
- If it already passes, note that no zip rebuild is required.
- If it fails, continue to Step 3 to rebuild the archive.

- [ ] **Step 3: Rebuild the archive only if the verifier failed**

If Step 2 failed, first create a staging directory and copy the expected package contents:

```bash
rm -rf "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/writing_zip_stage" && mkdir -p "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/writing_zip_stage/.claude" && cp -r "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/.claude/skills" "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/writing_zip_stage/.claude/skills" && mkdir -p "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/writing_zip_stage/docs" && cp "C:/Users/user/Desktop/workspaces/day4-writting/docs/6.나의글샘플.txt" "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/writing_zip_stage/docs/6.나의글샘플.txt" && cp "C:/Users/user/Desktop/workspaces/day4-writting/docs/9.첨삭샘플.txt" "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/writing_zip_stage/docs/9.첨삭샘플.txt" && cp "C:/Users/user/Desktop/workspaces/day4-writting/docs/10.퇴고샘플.txt" "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/writing_zip_stage/docs/10.퇴고샘플.txt" && cp "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/writing/INSTALL.md" "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/writing_zip_stage/INSTALL.md"
```

Then rebuild the zip:

```bash
python - <<'PY'
from pathlib import Path
import zipfile
root = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion")
stage = root / "tmp_review_files" / "writing_zip_stage"
zip_path = root / "writing" / "writing-skills.zip"
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in stage.rglob("*"):
        if path.is_file():
            zf.write(path, path.relative_to(stage).as_posix())
print("ZIP_REBUILT")
PY
```

If Step 2 already passed, skip this step entirely.

- [ ] **Step 4: Re-run the archive verifier**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_zip.py"
```

Expected: PASS with `WRITING_ZIP_OK`.

- [ ] **Step 5: Commit only if the zip changed**

If `writing/writing-skills.zip` changed, run:

```bash
git add "writing/writing-skills.zip"
git commit -m "$(cat <<'EOF'
fix: align writing skills archive with package structure

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

If the archive already passed in Step 2 and no file changed, skip the commit and note that the zip was already aligned.

---

### Task 3: Align the install guide to the verified package structure

**Files:**
- Modify if needed: `writing/INSTALL.md`
- Test: `writing/INSTALL.md`

- [ ] **Step 1: Write the failing install-guide verifier**

Create `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_install.py` with this content:

```python
from pathlib import Path

text = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/writing/INSTALL.md").read_text(encoding="utf-8")
required = [
    "글쓰기 12단계 스킬",
    "writing-skills.zip",
    ".claude/skills/",
    "6.나의글샘플.txt",
    "9.첨삭샘플.txt",
    "10.퇴고샘플.txt",
    "글쓰기 워크플로우 시작 가능",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit("MISSING:\n" + "\n".join(missing))
print("WRITING_INSTALL_OK")
```

- [ ] **Step 2: Run the verifier**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_install.py"
```

Expected:
- If it fails, continue to Step 3 and repair the guide.
- If it already passes, skip directly to Step 4.

- [ ] **Step 3: Repair `writing/INSTALL.md` only if needed**

If the verifier failed, ensure the guide still includes the package-focused pointer and these exact structure notes near the top:

```markdown
저장소 전체 사용/탐색 가이드는 `../INSTALL.md`를 참고하세요. 이 문서는 `writing/` 패키지 설치 절차에만 집중합니다.
```

Also ensure the structure example still includes:
- `.claude/skills/`
- `docs/6.나의글샘플.txt`
- `docs/9.첨삭샘플.txt`
- `docs/10.퇴고샘플.txt`
- `INSTALL.md`

If all of those already exist in the guide, do not make unnecessary edits.

- [ ] **Step 4: Re-run the verifier**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_install.py"
```

Expected: PASS with `WRITING_INSTALL_OK`.

- [ ] **Step 5: Commit only if the guide changed**

If `writing/INSTALL.md` changed, run:

```bash
git add "writing/INSTALL.md"
git commit -m "$(cat <<'EOF'
docs: align writing package install guide

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

If the guide already passed and no file changed, skip the commit and note that no guide edit was necessary.

---

### Task 4: Run the full package verification checklist

**Files:**
- Test: `.claude/skills/**`, `writing/INSTALL.md`, `writing/writing-skills.zip`

- [ ] **Step 1: Write the final package verifier**

Create `C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_package_complete.py` with this content:

```python
from pathlib import Path
import zipfile

ROOT = Path(r"C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion")
skills_root = ROOT / ".claude" / "skills"
expected_dirs = [
    "blueprint-outline",
    "cartesian-doubt",
    "drafting-sprint",
    "final-touch",
    "master-critique",
    "material-curation",
    "polishing-refining",
    "publishing-meta",
    "self-correction",
    "socratic-method",
    "structural-logic",
    "voice-persona",
    "writing-orchestrator",
]
for directory in expected_dirs:
    skill_file = skills_root / directory / "SKILL.md"
    if not skill_file.exists():
        raise SystemExit(f"MISSING_SKILL:{skill_file}")

if not (skills_root / "README.md").exists():
    raise SystemExit("MISSING_SKILL_README")

sample_docs = [
    ROOT / "docs" / "6.나의글샘플.txt",
    ROOT / "docs" / "9.첨삭샘플.txt",
    ROOT / "docs" / "10.퇴고샘플.txt",
]
for path in sample_docs:
    if not path.exists():
        raise SystemExit(f"MISSING_SAMPLE:{path}")

zip_path = ROOT / "writing" / "writing-skills.zip"
with zipfile.ZipFile(zip_path) as zf:
    names = set(zf.namelist())
    for directory in expected_dirs:
        zipped = f".claude/skills/{directory}/SKILL.md"
        if zipped not in names:
            raise SystemExit(f"MISSING_ZIP_SKILL:{zipped}")
    for sample in ["docs/6.나의글샘플.txt", "docs/9.첨삭샘플.txt", "docs/10.퇴고샘플.txt", "INSTALL.md", ".claude/skills/README.md"]:
        if sample not in names:
            raise SystemExit(f"MISSING_ZIP_FILE:{sample}")

install_text = (ROOT / "writing" / "INSTALL.md").read_text(encoding="utf-8")
for item in ["글쓰기 12단계 스킬", "writing-skills.zip", ".claude/skills/", "글쓰기 워크플로우 시작 가능"]:
    if item not in install_text:
        raise SystemExit(f"MISSING_INSTALL_TEXT:{item}")

print("WRITING_PACKAGE_COMPLETE")
```

- [ ] **Step 2: Run the final verifier**

Run:

```bash
python "C:/Users/user/Desktop/workspaces/day4-writting/.claude/worktrees/saju-flask-app-completion/tmp_review_files/check_writing_package_complete.py"
```

Expected: PASS with `WRITING_PACKAGE_COMPLETE`.

- [ ] **Step 3: Clean up verifier artifacts if needed**

Leave the temporary verifier scripts untracked unless you intentionally want to keep them for local package QA. Do not commit them.

- [ ] **Step 4: Report completion status**

Summarize whether:
- `.claude/skills/` exists in the worktree,
- the zip matches the documented package structure,
- the install guide matches the real package,
- all final verification checks pass.

No commit in this step unless one of the earlier tasks changed files.

---

## Self-Review Notes

- **Spec coverage:**
  - Worktree skill assets restored: Task 1
  - Zip archive verified/rebuilt if needed: Task 2
  - Install guide aligned to actual package structure: Task 3
  - Full package checklist verification: Task 4
- **Placeholder scan:** No TODO/TBD placeholders remain in the plan.
- **Type consistency:** The same 13 skill directories, sample docs, archive paths, and install-guide markers are referenced consistently across all tasks.
