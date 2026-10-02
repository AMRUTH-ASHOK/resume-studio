---
name: resume-target
description: Creates or updates a resume tailored to one specific target, drafting in markdown and iterating with the user until the content is confirmed. Use when the user wants a resume for a particular job, company, job description, internal role, grad school application, master's or PhD program, or fellowship, or when they want to revise a tailored resume they already started.
---

# Resume Target

Turns the master resume into one tailored resume for one specific target.

**This skill never writes LaTeX.** It produces a confirmed markdown draft. `resume-render` handles typesetting. That separation exists so content is cheap to argue about.

## Paths

Read `references/workspace.md` for where everything lives, the `brief.md` template, and
the draft header. If a path doesn't resolve, glob for the filename.

## Prerequisite

`sources/master-resume.md` must exist. If it doesn't, stop and route to `master-resume`. Building a target resume without a source of truth produces whatever the user happens to remember today, which is the problem this plugin exists to solve.

If the master's deep dive isn't complete, say so once and let the user choose: finish it first, or go ahead with what's there.

## Mode Detection

Check `targets/` for a folder matching what the user described.

- **No match** → Create mode. Step 1.
- **Match with only a `brief.md`** (created during setup) → Create mode, but read the brief first and ask only what it doesn't already answer.
- **Match with an `IMPORTED` draft** → Create mode. The imported draft is a reference for what the user used to send, not a starting point; build fresh from the master.
- **Match with a `DRAFTING` or `CONFIRMED` draft** → Update mode. Read the brief and draft, ask what should change, then jump to Step 5.

## Step 1: The Brief

Ask these. Conversationally, not as a form. Skip anything already answered in an existing brief.

**1. What is this for?**

| Target type | What changes |
|---|---|
| Job, with a JD | Strongest case. JD drives keyword and requirement mapping. |
| Job, no JD | Speculative or referral. Research the company and role family instead. |
| Internal transfer | Reader already knows the company. Skip the credibility-building; lead with what you've delivered internally. |
| Grad program (Master's, PhD) | Reader is faculty or an admissions committee. Research, projects, coursework, and publications outrank job titles. Trajectory and intellectual fit matter more than business impact. |
| Fellowship or scholarship | Match the stated selection criteria explicitly. |

**2. The details.** Company or institution, role or program title, team or department, link or pasted text of the description. Save the full description text to `targets/<slug>/jd.md`, fetching it from the link if you can. Links die when postings close, and later revisions and reviews need the text. For a role family rather than one posting, save one or two representative postings.

**3. One page or two?**

Ask, but recommend. Reasoning to apply:
- Under ~5 years of experience → one page, almost always
- 5+ years, or several distinct domains worth showing → two pages
- Grad applications → two pages is normal and often expected; academic readers don't penalize length the way recruiters do
- Startups and fast-moving teams skew one page; large enterprises and senior roles tolerate two
- If a two-page draft can't fill the second page past about two-thirds, one page is the better document

Say which you'd pick and why, in one sentence, then let them decide.

**4. Anything to emphasize or avoid?** Sometimes they know something you can't infer: a hiring manager they've met, a project they're sick of being known for, a gap they want handled a specific way.

Write or update `targets/<slug>/brief.md` from the template in `references/workspace.md`. Slug format: `<company>-<role>` for a specific posting, or the role family (`ai-solutions-engineer`) for a target applied to repeatedly; lowercase, hyphens.

## Step 2: Research the Target

For a company: 2-3 web searches on what they build, the team, recent launches, and the vocabulary they use publicly. For a grad program: the department, the specific faculty or research groups, the program's stated priorities.

If search returns little, say so. Generic research produces generic framing, and it's better for the user to know that up front.

Extract from the description:
- Requirements, each classed **Direct** (clear evidence in the master), **Bridge** (adjacent experience that transfers, with a confidence level), or **Gap** (no honest claim available)
- The keywords that matter, ranked by placement and repetition
- What this reader is actually screening for, which is often narrower than the posting suggests

## Step 3: Map the Master to the Target

Read `sources/master-resume.md`. Read `references/bullet-craft.md`.

For every achievement in the master, judge fit against this target. Present per position:

| | ID | Achievement | Fit | Why |
|---|---|-------------|-----|-----|
| ✓ | P1-1 | [short description] | Direct | [which requirement it answers] |
| ✓ | P1-4 | [short description] | Direct | |
| ~ | P1-2 | [short description] | Bridge | [what transfers] |
| ✗ | P1-7 | [short description] | Weak | [why it's not earning space] |

Then show:
- **Budget:** how many bullets fit the chosen page count (see `references/latex-budgets.md`)
- **Selected vs available:** what's in, what's held in reserve
- **Coverage:** which JD requirements end up with evidence, and which don't
- **Gaps:** requirements with no honest claim. Name them plainly. A gap the user knows about is manageable; one they discover in the interview is not.
- **Provenance constraints:** anything from `resume-config.md` that limits framing

### >>>>>> STOP <<<<<<
Present the mapping. Ask the user to confirm, add, or drop selections.

This gate matters more than any other in the plugin. A confirmed wrong selection wastes the entire draft.

## Step 4: Draft in Markdown

Write `targets/<slug>/draft.md`. Full content, final wording, zero markup.

Follow `references/bullet-craft.md` for bullet construction and `references/ai-fingerprint.md` for what to avoid.

```markdown
# [Name] — [Role] at [Company]

**Target:** [role] | **Pages:** [1 or 2] | **Status:** DRAFTING | **Based on:** none

## Header
[Name] | [email] | [phone] | [location]
[links]
**Tagline:** [Role Title | Domain | Key Strength]

## Summary
[4-5 sentences]

## Skills
**[Group 1]**
- [line]
- [line]

**[Group 2]**
- [line]

## Experience

### [JD-customized theme line]
*[Real Title], [Employer]* | [dates]
- [Bullet]
- [Bullet]

### [Theme line]
*[Real Title], [Employer]* | [dates]
- [Bullet]

## Education
[Degree], [Institution], [Year]

## [Optional sections as the target warrants]
```

Four things to get right:

**The theme line.** The bold line above each position is a JD-customized theme, and the real title sits underneath in italics. This is the single strongest tailoring lever available, because it's the first thing read under each job. The real title never changes; only the theme does.

**Write in the target's language from the start.** Don't draft in your own team's internal vocabulary and translate afterwards. Translation leaves seams.

**Respect provenance.** Check `scope:` and `status:` on every achievement you pull. A `contributor` achievement gets a hedged verb. A `prototype` says prototype.

**Rough length awareness.** You aren't counting characters yet, that's `resume-render`'s job. But a bullet running past about 35 words will not fit two lines, so keep drafts in the neighborhood.

## Step 5: Iterate

Offer the live preview on the first iteration. Seeing the real layout changes what
people ask for, and it makes the one-page-versus-two decision concrete instead of
theoretical:

```bash
python3 <plugin-root>/scripts/preview.py
```

It serves `http://localhost:8000`, renders the draft with resume styling, draws A4
page boundaries so overflow is visible, and colour-codes every bullet against its
character budget. It reloads within a second of a file being saved, so the user can
watch edits land while you make them.

Present the draft as readable markdown, not a file path.

Then ask what to change. Expect several rounds; that's the design, not a failure. Common asks: swap a bullet, lead with something else, cut a position, make the summary less generic, work in a keyword.

Each round:
1. Apply the change
2. Note the knock-on effects (adding a bullet means something else gives)
3. Re-present the affected section only, not the whole document
4. Ask again

Two things to push back on, once and politely:
- **Overclaiming.** If a requested edit outruns what the master supports, say so and offer the strongest honest version.
- **Length creep.** Every addition costs something. Name the trade rather than silently absorbing it.

### >>>>>> STOP <<<<<<
Keep iterating until the user explicitly confirms. Do not proceed to rendering on your own judgment that it looks good.

## Step 6: Lock and Hand Off

On confirmation, set `**Status:** CONFIRMED` in `draft.md`, add any decisions that changed along the way to the brief's `## Decisions`, and set the brief's `**Next:**` line to rendering.

> "Draft confirmed: [N] bullets across [M] positions, targeting [1/2] page[s]. Next: `resume-render` to typeset and check it actually fits. Once the PDF looks right, it gets saved as v[N]."

If the session ends before confirmation, set the brief's `**Next:**` line to the open question or the section still being iterated.

## Update Mode

When a draft already exists and the user wants changes, usually to an already-saved version:

1. Read `brief.md` and `draft.md`. The draft's `Based on:` line says which saved version it started from.
2. Ask what should change and why. If it came from `review.md`, read that too.
3. Flip status back to `DRAFTING`
4. Apply changes, then iterate from Step 5
5. Re-confirm, then re-render. Once it's settled, `resume-version` saves it as the next version, so the earlier one stays intact.

To start over from an older version rather than the latest, route to `resume-version` restore first.

If the target itself changed (different role at the same company, say), start a new target folder rather than overwriting. Old drafts are useful reference.
