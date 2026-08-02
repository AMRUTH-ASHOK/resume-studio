---
name: resume-render
description: Typesets a confirmed markdown resume draft into LaTeX and compiles it to a page-perfect PDF, enforcing character budgets, orphan rules, and page-fill targets. Use when a resume draft has been confirmed and needs to become a PDF, when a rendered resume overflows or underfills its page budget, or when the user asks to compile, typeset, or export their resume to LaTeX or PDF.
---

# Resume Render

Turns a confirmed markdown draft into a compiled PDF that hits its page target exactly.

## Paths

- **Plugin root** holds `references/`, `assets/`, `scripts/`. If a path doesn't resolve, glob for the filename.
- **Workspace** is the user's current folder.

## Prerequisites

1. `targets/<slug>/draft.md` exists with `**Status:** CONFIRMED`. If it says `DRAFTING`, stop and route back to `resume-target`. Rendering unconfirmed content wastes the fitting work.
2. A LaTeX toolchain. Check with `which pdflatex`. If missing:

   > "No LaTeX found. Install BasicTeX (~100MB): `brew install --cask basictex`, then `eval "$(/usr/libexec/path_helper)"` and `sudo tlmgr install fontawesome lastpage enumitem`. I can generate the `.tex` now and you compile later, or wait until it's installed."

   Generating the `.tex` without compiling is a legitimate outcome. Say clearly that page fit is unverified.

## Step 1: Load

Read, in order:

1. `targets/<slug>/draft.md` — the confirmed content
2. `targets/<slug>/brief.md` — page target
3. `resume-config.md` — contact details, work authorization, provenance flags
4. `references/latex-budgets.md` — the numbers that govern everything below

Copy the template into the target folder on first render so the user can customize per application without touching the shared original:

```bash
cp <plugin-root>/assets/templates/resume.cls targets/<slug>/
```

## Step 2: Fit Before You Write

This is the part that determines whether the PDF works. Do it before generating LaTeX, not after.

For each piece of content, compute the rendered character count and compare against the budget:

| Element | Target | Hard max | Orphan rule |
|---------|--------|----------|-------------|
| 2-line bullet | 189-205 | 218 | last line >= 78 chars |
| 1-line bullet | 105-111 | 117 | n/a |
| Skill line | one line | 119 minus bold penalty | must not wrap |
| Summary | 500-555 total | 570 | last line >= 78 chars |
| Tagline | 80-95 | one line | n/a |

Bold text renders wider. Effective per-line limit is `119 - (0.5 × bold_chars)`.

Aim for the middle of each range. A bullet sitting at the hard max will overflow if it happens to contain wide characters, and proportional fonts make that unpredictable.

Where a draft bullet doesn't fit, rewrite it to fit and note the change. Where it's far too short, it'll look thin next to its neighbors, so either enrich it from the master or accept it as a 1-line bullet.

**Bullet budget by page count:**
- One page: roughly 8-10 bullets, 8-10 skill lines, minimal optional sections
- Two pages: roughly 20-21 bullets, 13 skill lines

Exact counts shift with which optional sections are present. `references/latex-budgets.md` has the adjustment table.

## Step 3: Generate the LaTeX

Read `assets/templates/resume.tex` for structure.

Fill the header from `resume-config.md`. Drop any line the user left blank rather than emitting an empty link.

For each position, the bold argument is the theme line from the draft and the italic subtitle is the real title and employer. Escape LaTeX specials in all user content: `&` `%` `$` `#` `_` `{` `}`. An unescaped `&` in a company name is the most common compile failure here.

Drop sections the draft doesn't use. Omit Honors and Awards entirely if empty rather than leaving a bare heading.

Write to `targets/<slug>/resume.tex`.

## Step 4: Verify

Run the counter:

```bash
python3 <plugin-root>/scripts/char_count.py targets/<slug>/resume.tex
```

It checks every bullet and every skill line, and prints a violations list. **Fix every violation before compiling.** The tool is authoritative; don't override it with your own estimate.

Then compile:

```bash
pdflatex -interaction=nonstopmode -output-directory=targets/<slug> targets/<slug>/resume.tex
```

Read the resulting PDF and check:

| Check | Requirement |
|-------|-------------|
| Page count | Matches the target exactly |
| Last page fill | No more than ~3 lines of white space |
| Orphans | No bullet whose last line is a stub |
| Header wrap | Position title and date share one line |
| Escapes | No stray `\&` or literal `$` in the output |

## Step 5: When It Doesn't Fit

Both directions are common on a first render. **Never silently truncate.** Report the overage and offer specific options.

**Content overflows:**
> "Runs 6 lines onto page 3. Options: drop the weakest bullet from [Position] (-2 lines), tighten three bullets from 2L to 1L (-3 lines), or drop a skills line (-1). My pick: [X], because [reason]."

**Page underfills:**
> "Page 2 ends halfway. Either promote a held-back achievement from the master, expand two 1L bullets to 2L, or switch to a single page. Given [context], I'd [recommendation]."

Apply the user's choice, re-run the counter, recompile.

If the same content fails to fit after two rounds, that's a signal the page target is wrong. Say so.

## Step 6: Report

> "Compiled: `targets/<slug>/resume.pdf`, [N] pages, [M] bullets, 0 violations. [Anything reworded to fit.] Next: `resume-review` for a scored critique, or `cover-letter` if you need one."

List any bullet you reworded during fitting. The user confirmed specific wording and deserves to know what changed, even when the change was mechanical.

## Re-Rendering

When `resume.tex` already exists:

- **Draft changed** → regenerate from scratch. Don't patch.
- **Cosmetic fix only** (a typo, an escape) → edit the `.tex` directly, recompile, and mirror the fix back into `draft.md` so the two don't drift.
- **Page target changed** → full regenerate against the new budget.

Never edit `.tex` for a content change. Content lives in the draft; the `.tex` is a build artifact.
