---
name: resume-preview
description: Starts a local live-reloading server that renders resume drafts with real resume styling, A4 page boundaries, and per-bullet character budget colours. Use when the user wants to see how a resume actually looks, asks to preview or render their resumes, wants to compare several resumes side by side, wants to check whether content fits one page or two, or asks why a resume is overflowing.
---

# Resume Preview

Renders markdown drafts as they will actually look, in the browser, updating as they're
edited. No LaTeX required, which matters because most people hit this step before they
have a TeX distribution installed.

## Paths

- **Plugin root** holds `references/`, `assets/`, `scripts/`. If a path doesn't resolve, glob for the filename.
- **Workspace** is the user's current folder.

## Start It

```bash
python3 <plugin-root>/scripts/preview.py
```

Serves `http://localhost:8000`. Options: `--port N`, `--dir PATH`, `--no-open`.

Run it in the background so the conversation isn't blocked. If the port is taken,
pick another rather than killing whatever holds it.

Tell the user the URL and leave it running for the rest of the session. The whole
point is that it updates while you both work.

## What It Shows

**Resume layout** for anything at `targets/<slug>/draft.md`. A4 sheet with the real
margins from `resume.cls`, section rules, right-aligned dates, tight bullet spacing.

**Page boundaries** as red dashed lines wherever a page break falls, with the page
number. This is the fastest way to answer "will this fit on one page."

**Budget colours** on every bullet, with exact counts on hover:

| Colour | Meaning |
|--------|---------|
| none | Within target |
| amber | Awkward length. Fill it out or cut it to one line. |
| orange | Near the limit. Risky with wide characters. |
| red | Over 218 characters. Will silently become three lines. |

Skills lines are judged differently from bullets: they only need to fit one line and
have no minimum. Publications, education, and certifications are treated as
informational.

**Reference documents** get a plain document layout and an amber banner saying so.
`master-resume.md` is deliberately not shown as a resume, because it isn't one. If a
user asks "is this how my resume will look?" while viewing the master, the answer is
no, and the banner should already be telling them that.

## Rendering Every Resume

Choose **All resumes** in the dropdown to stack every target draft with its own page
count, fill percentage, bullet count, and over-limit chip. This is the right view for:

- Comparing tailored versions of the same history
- Spotting which resume is out of date
- Deciding which one to use as the base for a new target

## How to Use It During Drafting

Keep it open through `resume-target`'s iteration loop. Seeing the layout changes what
people ask for, and it turns the one-page-versus-two decision from a guess into an
observation.

When the user reports a problem, read the numbers rather than speculating:

| Symptom | Look at | Usual fix |
|---------|---------|-----------|
| Runs onto an extra page | Red bullets | Trim the over-limit ones first, they cost a full line each |
| Last page looks empty | Fill percentage | Promote a held-back achievement, or drop to fewer pages |
| Looks ragged | Amber bullets | Those are stranded mid-length; commit to one line or two |
| Skills section wraps | Red skill lines | Shorten, or move a tool to another group |

## Accuracy

The preview uses a web font stack rather than Computer Modern, so line breaks land
close but not identically to the compiled PDF. Character counts are exact, and those
are what actually govern fit.

Treat the preview as authoritative for content and layout decisions, and
`resume-render` as authoritative for the final page count.

## Stopping It

Ctrl-C in the terminal running it. Don't use a broad process kill to clear a port;
targeted or nothing.
