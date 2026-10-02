---
name: resume-start
description: Entry point and guided setup for Resume Studio. Works out where the user is from their files, runs a short setup Q&A on first use (contact details, existing resumes, target roles), tells returning users where they left off, and routes to the next phase. Use when the user starts a chat about their resume or CV, says "start", "set me up", "where was I", or "what's next", or asks for help with a resume without saying what they need.
---

# Resume Studio

The front door. Two jobs: run the setup Q&A for a new user, and tell a returning user
exactly where they left off. **Don't do the resume work itself here.** Hand off.

## Paths

Read `references/workspace.md` first. It defines the layout, the templates for
`resume-config.md` and `brief.md`, the progress markers, and versioning. If a path
doesn't resolve, glob for the filename.

## The Model

Two artifacts with deliberately opposite disciplines:

| | Master resume | Target resume |
|---|---|---|
| Lives at | `sources/master-resume.md` | `targets/<slug>/` |
| Purpose | Source of truth | One application or role family |
| Format | Markdown | Markdown draft, then LaTeX and PDF |
| Length | Unbounded. 4, 8, 20 pages. | 1 or 2 pages, hard limit |
| Discipline | Capture everything | Select ruthlessly |
| Submitted? | Never | Always, as a saved version |

Every target is derived from the master. The master is never sent to anyone.

## Step 1: Read the State

Check silently, in order:

1. **Older layout?** `master-resume.md` at the workspace root, loose files directly in
   `sources/`, or a notes file of links such as `info.txt`. If so, tell the user what
   will move and follow "Migrating an Older Workspace" in `references/workspace.md`
   before anything else.
2. **`resume-config.md`**: does it exist, and are the contact fields filled?
3. **`sources/originals/`**: any documents?
4. **`sources/master-resume.md`**: does it exist? Read its `> Deep dive:` and `> Next:`
   lines.
5. **Each `targets/<slug>/`**: the brief's `**Next:**` line, the draft's `**Status:**`,
   whether `resume.pdf` is newer than `draft.md`, and the highest `versions/vN/`.

## Step 2: Report

**No `resume-config.md`** → this is a new user. Go to Step 3.

**Config exists but setup is incomplete** (blank contact fields, no documents and no
interview choice, or no targets named yet) → say what's already in place in one line,
then run Step 3 for the missing topics only. Offer values found in existing files (an
imported draft's header, say) as suggestions to confirm, never as facts.

**Otherwise** → a returning user. Report where they are in a few lines, not a file
listing:

> **Master:** built, deep dive at position 2 of 3, 4 open questions.
> **Targets:**
> - `acme-ml-engineer`: v2 saved Oct 3, no edits since
> - `data-engineer`: imported from an old resume, not rebuilt yet
>
> **Next:** finish the master deep dive, starting with the open questions under [Employer].

Take the "Next" from the files' `Next:` lines, not from memory. Then go to Step 4.

## Step 3: Setup Q&A (Phase 1)

Open by setting expectations in one or two sentences: a few questions now, about five
minutes; then the master resume gets built properly; then tailored resumes, one at a
time.

Ask conversationally, **one topic at a time**, and skip anything already answered.

### Topic 1: About you

Name, email, phone, city and country, and whichever of LinkedIn, GitHub, or a personal
site they want on a resume. Anything skipped stays blank and is dropped from the PDF.

### Topic 2: What you already have

Ask which of these exist:
- A **master resume**: one long document with everything
- **Role-specific resumes**: versions already tailored to different roles
- **Other material**: LinkedIn export, performance reviews, promotion packets, project
  notes, a portfolio
- **Nothing written down**, which is fine; Phase 2 becomes an interview

For **files**, have them drop everything into `sources/originals/` (create it). For
**cloud links** (Google Docs, Notion, Drive), record each one in
`## Source Documents` in the config. If you have a connector that can read the link,
use it and save the export into `sources/originals/`; otherwise ask them to download it
(`.docx`, `.md`, or `.pdf`) into that folder.

Two things to say plainly:
- An existing "master resume" document is a **source**, not the finished master. It
  goes into `originals/`, and the real master gets built from it in Phase 2.
- Role-specific resumes are useful twice: as sources for the master, and as starting
  points for targets. Offer to register each one as a target now, importing its content
  as a draft with `Status: IMPORTED`, so it shows up in the preview. Optional.

### Topic 3: What you're aiming at

For each target they name:
- **What:** role or program, and whether it's one specific posting or a role family
  they'll apply to repeatedly
- **Where:** company, team, or program, if known
- **The description:** a link, or the pasted text. Save the text to
  `targets/<slug>/jd.md`; links stop working when postings close.
- **Pages:** ask, but recommend. Under about five years of experience, one page; more,
  or several distinct domains, two. Grad applications, two.
- **Anything to emphasize or avoid**

Write `targets/<slug>/brief.md` from the template in `references/workspace.md`, with
`**Next:** Build from the master with resume-target once Phase 2 is done.`

Not knowing yet is fine. Say targets can be added any time and move on.

### Topic 4: Defaults

Default page count, and a work authorization line only if they apply across countries.

### Topic 5: Anything never to overstate

Confidential projects, customer names under NDA, a title that needs verifying, work
that was a prototype rather than shipped. Most of this surfaces during Phase 2, so
capture what they volunteer and move on.

### Write it

Create `sources/originals/` and `targets/`, write `resume-config.md` from the template,
and write the briefs. Then show what was set up:

```
resume-config.md                   contact details, 2 source links
sources/originals/                 3 documents
targets/
  acme-ml-engineer/brief.md        1 page, JD saved
  data-engineer/brief.md           1 page, no JD yet
```

### >>>>>> STOP <<<<<<
Ask them to confirm the setup or correct anything. Then go to Step 4.

## Step 4: Route

Work through targets **one at a time**, in the order the user listed them, unless they
pick one.

| State | Next skill |
|-------|-----------|
| No config | Setup Q&A, Step 3 |
| Config, no master | `master-resume`: build it from `sources/originals/`, or by interview |
| Master exists, deep dive not complete | `master-resume`: deep dive, resuming where it stopped |
| Master complete, target has no draft or an `IMPORTED` one | `resume-target` for that target |
| Draft `DRAFTING` | `resume-target`, continue iterating |
| Draft `CONFIRMED`, PDF missing or older than the draft | `resume-render` |
| Rendered, not saved as a version | `resume-version`: ask whether this one is settled |
| Version saved | `resume-review`, `cover-letter`, or the next target |
| New work to add | `master-resume`, update mode |

Don't build a target before the master exists. Explain why in a sentence: without a
source of truth, every application starts from whatever the user remembers that day.
Imported drafts can still be previewed in the meantime.

## Step 5: Hand Off

End by naming the next skill and what it will do. One line, not a menu.

> "Next: `master-resume`. It reads your three documents in `sources/originals/` and
> merges them into one master, then asks about what they left out."

## The Whole Flow

```
resume-start  (setup Q&A, or "where you left off")
     |
     v
master-resume  (build, then deep dive)  <------+
     |                                         | (new work to add)
     v                                         |
resume-target  (iterate in markdown) ----------+     resume-preview
     |                                               (live localhost render,
     v                                                open while iterating)
resume-render  (LaTeX + PDF)
     |
     v
resume-version (save as v1, v2, ... once settled)
     |
     v
resume-review  (scored critique)  -->  cover-letter (optional)
```

`resume-preview` runs alongside the others. Offer it as soon as there's a draft.

## Working Style

This applies to every skill in the plugin:

- **Ask, don't assume.** Especially about ownership and metrics. Guessing produces resumes that collapse in interviews.
- **Stop at decision points.** Never chain through a confirmation gate on your own.
- **Iterate on content, not markup.** Everything is discussable while it's markdown. Once it's LaTeX, changes cost more.
- **Accuracy beats impressiveness.** Every time, without exception.
- **Leave a trail.** Before a session ends partway, update the relevant `Next:` line so the next chat can pick up without the user remembering anything.
