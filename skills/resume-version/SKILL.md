---
name: resume-version
description: Saves, lists, compares, and restores numbered versions (v1, v2, ...) of a tailored resume, so each settled resume is frozen with its PDF and every change after it becomes the next version. Use when the user says a resume is settled, final, or good to go, wants to save or freeze a version, asks what changed between versions or since the last one, wants to go back to an earlier version, or wants to record where a version was sent.
---

# Resume Version

Keeps a numbered history of each target resume. The rules live in "Versioning" in
`references/workspace.md`; this skill applies them.

## Paths

Read `references/workspace.md`. Everything here happens inside `targets/<slug>/`. If a
path doesn't resolve, glob for the filename.

## Which Target

If the user didn't say and more than one target exists, ask. If only one has been
touched this session, use it and name it.

## Save

**Preconditions.** Check all three, and route rather than proceed if one fails:

| Check | If it fails |
|-------|-------------|
| `draft.md` says `Status: CONFIRMED` | Route to `resume-target` to finish and confirm the content |
| `resume.pdf` exists and is newer than `draft.md` | Route to `resume-render` first. A version without a matching PDF is not a version. |
| The user called it settled | Ask: "Save this as vN?" A yes to that question counts. |

**Steps.**

1. Find the highest existing `versions/vN/` and use the next number. With none, it's v1.
2. Set `**Based on:** vN` in `draft.md` **before** copying, so the saved draft and the
   working draft are byte-identical and the unsaved-changes check below stays exact.
3. Copy the build into the new folder:
   ```bash
   cd targets/<slug>
   mkdir -p versions/vN
   cp draft.md resume.tex resume.cls resume.pdf versions/vN/
   ```
   Also copy `cover-letter-draft.md`, `cover-letter.tex`, and `cover-letter.pdf` if they
   exist, and `review.md` if it's newer than `resume.pdf`.
4. Confirm the snapshot compiles on its own, without writing into the frozen folder:
   ```bash
   mkdir -p /tmp/rs-version-check
   cd targets/<slug>/versions/vN
   for pass in 1 2; do pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/rs-version-check resume.tex > /dev/null; done
   grep -E "^!|Output written" /tmp/rs-version-check/resume.log
   ```
   The `Output written` line also gives the page count.
5. Add a row to `## Versions` in `brief.md`:
   - **Date:** today
   - **Pages:** from step 4
   - **What changed:** "First version" for v1. Otherwise diff the previous version's
     `draft.md` against this one and summarize in one plain line: "Led with Retrieval
     Studio, cut the internship to one bullet, added Kubernetes to skills."
   - **Master as of:** the `Last updated` date from the master's header
   - **Notes:** empty, for the user
6. Update the brief's `**Next:**` line.

**Report:**

> "Saved **v2** of `acme-ml-engineer`: 2 pages. Since v1: [what changed]. The file
> to send is `targets/acme-ml-engineer/versions/v2/resume.pdf`. Tell me where you
> send it and I'll note it against this version."

## List

Show the brief's `## Versions` table. Then say whether the current draft has changes
that aren't in any version:

```bash
cmp -s targets/<slug>/draft.md targets/<slug>/versions/vN/draft.md && echo "no unsaved changes"
```

## Compare

Default to the latest version against the current draft ("what have I changed since
v2?"). Otherwise compare the two versions the user names:

```bash
diff -u targets/<slug>/versions/vA/draft.md targets/<slug>/versions/vB/draft.md
```

Report section by section in plain language: summary reworded, which bullets were
added, cut, or rewritten, skills changes, page count. Quote a line only where the
wording itself is the point. Paste the raw diff only if asked.

## Restore

When the user wants to go back to an earlier version and continue from it:

1. **Check for unsaved work.** If `draft.md` differs from the latest version's
   `draft.md`, say so and offer to save it as a version first. If they decline, those
   edits are gone, so get an explicit yes.
2. **Copy** `versions/vN/draft.md` over `draft.md`. Set `Status: DRAFTING` and
   `Based on: vN`.
3. **Leave later versions alone.** Restoring v1 when v3 exists doesn't delete v2 or v3.
   The next save is v4, and its "What changed" line says it was rebuilt from v1.
4. Update the brief's `**Next:**` line, then hand off to `resume-target` for the edits.

## Record Where It Was Sent

When the user mentions submitting a version, add it to that row's `Notes`: "Sent to
Acme, Oct 4". If they don't say which version, assume the latest and confirm.

## Delete

Only on an explicit request, and only after confirming. Remove the folder, keep the row
in the table with `deleted` in `Notes`, and never reuse the number.
