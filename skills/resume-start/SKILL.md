---
name: resume-start
description: Entry point for all resume work. Detects what the user already has, sets up the workspace, and routes to the right skill. Use when the user wants help with a resume or CV, mentions tailoring a resume to a job, asks where to begin with job applications, or says something general like "help me with my resume" without specifying what they need.
---

# Resume Studio

The front door. Figure out where the user is, then route. **Do not do the actual resume work in this skill** — hand off.

## Paths

- **Plugin root** holds `references/`, `assets/`, `scripts/`. If a path doesn't resolve, glob for the filename (e.g. `**/latex-budgets.md`).
- **Workspace** is the user's current folder, where their resume data lives.

## The Model

Two artifacts with deliberately opposite disciplines:

| | Master resume | Target resume |
|---|---|---|
| Purpose | Source of truth | One application |
| Format | Markdown | LaTeX → PDF |
| Length | Unbounded. 4, 8, 20 pages. Whatever it takes. | 1 or 2 pages, hard limit |
| Discipline | Capture everything | Select ruthlessly |
| Submitted? | Never | Always |

Every target resume is derived from the master. The master is never sent to anyone.

## Workspace Layout

```
resume-config.md            # Contact info, preferences, provenance flags
master-resume.md            # The source of truth
sources/                    # Raw documents the user drops in
targets/
  <company>-<role>/
    brief.md                # What this application is for
    draft.md                # Markdown draft, iterated with the user
    resume.tex, resume.pdf
    cover-letter.tex, cover-letter.pdf
    review.md
```

## Step 1: Detect State

Check the workspace, in order:

1. Does `master-resume.md` exist?
2. Does `resume-config.md` exist?
3. What's in `targets/`?
4. Any unprocessed files in `sources/`?

Report what you found in one or two sentences. Don't dump a file listing.

## Step 2: Route

**No master resume yet.** This is the fork that matters most. Ask what they have:

- *"I have a resume already"* → they put the file in `sources/`, then run `master-resume`. This is the fastest path and the most common.
- *"I have several resumes"* → all of them into `sources/`. `master-resume` merges and deduplicates. Different versions often contain different details about the same job, which is useful rather than redundant.
- *"I have nothing written down"* → `master-resume` in interview mode. Budget real time; this is a conversation, not a form.
- *"I have scattered notes, docs, promo packets"* → into `sources/`, then `master-resume`.

Do not offer to build a target resume before a master exists. Explain why briefly: without a source of truth, every application starts from zero and quality depends on what the user happens to remember that day.

**Master exists, user wants to apply somewhere** → `resume-target`.

**Master exists, user has new work to add** → `master-resume` (it detects the existing file and switches to update mode).

**A target draft exists and is confirmed** → `resume-render`.

**A rendered PDF exists** → `resume-review`, then `cover-letter` if they want one.

## Step 3: First-Run Setup

Only when nothing exists yet. Create:

```bash
mkdir -p sources targets
```

Then write `resume-config.md`:

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

## Provenance Flags
Things that must never be overstated. The generation skills check this before every output.

| Item | Status | Correct framing |
|------|--------|-----------------|

## Corrections Log
Errors caught once, never to reappear.

| Correction | Detail |
|-----------|--------|
```

Ask for contact details conversationally rather than making them fill in a form. Leave anything they don't have blank; the template drops empty fields.

## Step 4: Hand Off

End by naming the next skill and what it will do. One line, not a menu.

> "Next: run `master-resume`. Drop your resume into `sources/` first and it'll read from there."

## The Whole Flow

```
resume-start
     |
     v
master-resume  <-------------+
     |                       | (new work to add)
     v                       |
resume-target  --------------+     resume-preview
     |  (iterate in markdown)  <--  (live localhost render,
     v                               keep it open while iterating)
resume-render  (LaTeX + compile)
     |
     v
resume-review  (scored critique)
     |
     v
cover-letter   (optional)
```

`resume-preview` runs alongside the others rather than in sequence. Offer it as soon
as there's a draft to look at.

## Working Style

This applies to every skill in the plugin:

- **Ask, don't assume.** Especially about ownership and metrics. Guessing produces resumes that collapse in interviews.
- **Stop at decision points.** Never chain through a confirmation gate on your own.
- **Iterate on content, not markup.** Everything is discussable while it's markdown. Once it's LaTeX, changes cost more.
- **Accuracy beats impressiveness.** Every time, without exception.
