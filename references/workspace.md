# Workspace

The single definition of where a user's resume data lives, what each file is for, how
progress is recorded, and how versions work. Every skill reads paths from here.

The **workspace** is the folder the user works in. It's either the cloned plugin repo
itself (data is gitignored) or a separate folder of their own. The **plugin root** is
wherever `skills/`, `references/`, `assets/`, and `scripts/` live; glob for a filename if
a path doesn't resolve.

---

## Layout

```
resume-config.md            Who the user is, defaults, source links, provenance rules
sources/
  master-resume.md          The source of truth. Never submitted. No length limit.
  originals/                What the user started from: .docx, .pdf, exported docs
targets/
  <slug>/
    brief.md                What this target is, decisions made, version history
    jd.md                   The job or program description, pasted in full
    draft.md                The working copy, edited in chat
    resume.tex, resume.pdf  The latest build (plus resume.cls, copied on first render)
    cover-letter-draft.md   Optional
    cover-letter.tex/.pdf   Optional, latest build
    review.md               Optional, latest review
    versions/
      v1/                   Frozen snapshot. Never edited.
      v2/
```

**Slugs** are lowercase and hyphenated. A target can be a specific posting
(`acme-ml-engineer`) or a role family the user applies to repeatedly
(`ml-engineer`). For a role family, `jd.md` holds one or more representative
postings.

**Why `jd.md` exists:** job links die when the posting closes. Save the text the first
time it's shared, so a later revision or review can still read it.

---

## Phases

Every workspace moves through three phases. `resume-start` works out which one the user
is in by reading the files, never by asking them to remember.

| Phase | Skill | Done when |
|-------|-------|-----------|
| 1. Setup | `resume-start` | `resume-config.md` has contact details, `sources/originals/` has their documents (or they chose interview mode), and every target they named has a `brief.md` |
| 2. Master | `master-resume` | `sources/master-resume.md` exists and its header says the deep dive is complete |
| 3. Targets | `resume-target`, `resume-render`, `resume-version` | Each target has at least one saved version |

Phase 3 runs one target at a time. Phases can be revisited: new work goes back through
`master-resume`, new applications start a new target.

---

## Recording Progress

Chats end and context is lost. Anything needed to resume must be in the files.

- **Master header** carries a `> Deep dive:` line (see `master-resume`) and a
  `> Next:` line.
- **Each brief** carries a `**Next:**` line: the single next action for that target.
- **Each draft** carries `**Status:**` and `**Based on:**` lines.

Update the relevant line whenever a session stops partway. Write it for someone who
remembers nothing: "Next: answer the two ownership questions under the payments migration",
not "Next: continue."

---

## Draft Status

The header of every `draft.md`:

```markdown
**Target:** [role] | **Pages:** [1 or 2] | **Status:** [status] | **Based on:** [vN or none]
```

| Status | Meaning |
|--------|---------|
| `IMPORTED` | Copied from an old resume. Not yet derived from the master. |
| `DRAFTING` | Being iterated with the user. |
| `CONFIRMED` | User approved the content. Ready to render. |

Any edit to a `CONFIRMED` draft flips it back to `DRAFTING`.

---

## Versioning

Versions apply to targets only. The master isn't versioned; it accumulates, and each
target version records which master it came from.

### Saving a version

A version is a frozen snapshot of a target the user has explicitly called settled.
Never save one on your own judgment that it looks done.

1. **Next number** is one more than the highest existing `versions/vN/`. Numbers are
   never reused or renumbered, even after a restore.
2. **Point the draft at it first:** set `**Based on:** vN` in `draft.md` before copying,
   so the saved draft and the working draft stay byte-identical until the next edit.
3. **Copy** into `targets/<slug>/versions/vN/`: `draft.md`, `resume.tex`, `resume.cls`,
   `resume.pdf`. Also copy `cover-letter-draft.md`, `cover-letter.tex`, and
   `cover-letter.pdf` if they exist, and `review.md` if it reviewed this build.
4. **Check it stands alone:** the folder must recompile on its own, which is why
   `resume.cls` is copied in.
5. **Record it** as a new row in the brief's `## Versions` table: date, page count,
   one line on what changed since the previous version (written from a diff of the two
   `draft.md` files, in plain language), and the master's `Last updated` date.

If the draft is `CONFIRMED` but hasn't been rendered since its last edit, render first.
A version without a matching PDF is not a version.

### Rules

- **Frozen means frozen.** Never edit anything under `versions/`. A fix to a saved
  version is a new version. The one exception is adding files that didn't exist yet: a
  cover letter or review written against vN after it was saved can be copied into
  `vN/`, because nothing already saved changes.
- **Restoring** copies `versions/vN/draft.md` over `draft.md`, sets `Based on: vN` and
  `Status: DRAFTING`. If the current draft has changes that aren't in any saved version,
  say so and offer to save them first. Later versions stay where they are; the next
  save is the next unused number, and its "What changed" line notes it was rebuilt from
  vN.
- **Comparing** two versions means diffing their `draft.md` files and reporting the
  change section by section in plain language. Don't paste a raw diff.
- **Deleting** a version only happens on explicit request, after confirming.
- **A different role** at the same company is a new target folder, not a new version.

---

## Templates

### `resume-config.md`

```markdown
# Resume Config

## Contact
- **Name:**
- **Email:**
- **Phone:**
- **Location:**
- **LinkedIn:**
- **GitHub:**
- **Website:**

## Defaults
- **Default page count:** 2
- **Work authorization line:** [text, or "none"]

## Source Documents
Where the user's existing material came from. Links are recorded here because they
can't be read directly; their contents live as files in `sources/originals/`.

| Document | Link or file | Notes |
|----------|--------------|-------|

## Provenance Flags
Things that must never be overstated. Every generation skill checks this before output.

| Item | Status | Correct framing |
|------|--------|-----------------|

## Corrections Log
Errors caught once, never to reappear.

| Correction | Detail |
|-----------|--------|
```

Leave blank anything the user doesn't have. The LaTeX template drops empty fields.

### `brief.md`

```markdown
# Brief: [slug]

**Target:** [role] at [company, team, or program]
**Type:** [job | job, no JD | internal transfer | grad program | fellowship]
**Job description:** [link, or "none yet"] (full text in jd.md)
**Pages:** [1 or 2]
**Emphasize / avoid:** [anything the user asked for, or "nothing specific"]
**Next:** [the single next action for this target]

## Research
[What the target builds, what this reader screens for, keywords that matter.]

## Decisions
- [date]: [decision and the reason]

## Versions

| Version | Date | Pages | What changed | Master as of | Notes |
|---------|------|-------|--------------|--------------|-------|
```

`Notes` is for the user: where a version was submitted, feedback received.

---

## Migrating an Older Workspace

Workspaces created before this layout have `master-resume.md` at the root, raw
documents loose in `sources/`, and sometimes a notes file of links (`info.txt` or
similar). When `resume-start` finds that, tell the user what will move, then:

1. Move `master-resume.md` to `sources/master-resume.md`
2. Move loose files in `sources/` (anything that isn't `master-resume.md`) into
   `sources/originals/`
3. Copy links and notes from the notes file into `## Source Documents` in
   `resume-config.md`, then remove the notes file. Keep anything that doesn't fit as a
   note in that table rather than dropping it.
4. Rewrite each existing `brief.md` to the template above, preserving what it said, with
   an empty `## Versions` table. Don't create versions retroactively.
5. Add `**Based on:** none` to each draft header.
