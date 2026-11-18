---
name: cover-letter
description: Writes a one-page cover letter that complements a finished resume, drafting in markdown first and rendering to LaTeX after the user confirms. Use when the user needs a cover letter, a letter of intent, or a statement of purpose to accompany a resume or application.
---

# Cover Letter

Writes a one-page letter that deepens the resume rather than restating it.

## Paths

Read `references/workspace.md` for where everything lives. If a path doesn't resolve,
glob for the filename.

## Prerequisite

A confirmed resume draft at `targets/<slug>/draft.md`, ideally already saved as a version. The letter is written against a known resume so the two documents don't contradict each other or repeat each other.

## Load

1. `targets/<slug>/brief.md` — target type and research
2. `targets/<slug>/jd.md` — the description the letter answers
3. `targets/<slug>/draft.md` — what the resume already says
4. `sources/master-resume.md` — specifically the "What was hard" and "Collaboration" fields, which is where letter material lives
5. `references/cover-letter-craft.md` — structure and anti-patterns
6. `references/ai-fingerprint.md` — letters are the most detectable document, so this matters more here than anywhere else
7. `resume-config.md` — contact details

## The Governing Idea

The resume says what you did. The letter says why it mattered, why you want this specific job, and what you'd do next. If a paragraph could survive being pasted into a different application, it's not doing its job.

**Every claim must trace to a resume bullet.** The letter adds context and motivation, never new achievements. A letter introducing work the resume doesn't mention reads as padding, and it means the resume can't stand alone, which it must, since plenty of hiring managers never open the letter.

## Structure

One page. 250-300 words. Three paragraphs.

**Opening.** Reference something specific they build or a problem they have, and connect it to something you've actually done. Never open with "I am writing to express my interest." The first sentence decides whether the rest gets read.

**Evidence.** Two or three achievements translated into what they'd mean for this employer. Three or four quantified claims, no more. Use their vocabulary.

**Close.** What you'd contribute, and an active ask. Not "thank you for your consideration."

Adjust emphasis by target type:

| Target | Emphasis |
|--------|----------|
| Product company | Ship velocity, user impact, ownership |
| Enterprise or platform | Scale, reliability, customer outcomes |
| Consulting or customer-facing | Communication, ambiguity, stakeholder management |
| Startup | Range, autonomy, working outside your title |
| Internal transfer | Skip "why this company" entirely. Use that space for "why this team, now." |
| Grad program | Intellectual trajectory, research fit, named faculty or groups, what you want to work on |

## Draft First

Write `targets/<slug>/cover-letter-draft.md` in plain markdown. Present it inline and iterate, same as the resume. Cover letters attract more revision than resumes because voice is personal, so expect several rounds.

Verify before presenting: web-search every external reference. Product names, launches, team names, faculty names. A wrong product name in the opening sentence is fatal in a way no other error is. Flag anything unverified rather than guessing.

### >>>>>> STOP <<<<<<
Iterate until the user confirms.

## Then Render

Read `assets/templates/cover-letter.tex`. Fill from `resume-config.md`. Compile in two passes, like the resume:

```bash
for pass in 1 2; do
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=targets/<slug> targets/<slug>/cover-letter.tex > /dev/null
done
grep -E "^!|Output written" targets/<slug>/cover-letter.log
```

Once it's clean, delete the `.aux`, `.log`, and `.out` files.

Verify: exactly one page, 250-300 words, three paragraphs, at most two em-dashes in the whole letter, no generic opener, no contradiction with the resume.

If the letter was written against the latest saved version, copy `cover-letter-draft.md`, `cover-letter.tex`, and `cover-letter.pdf` into that `versions/vN/` folder so the pair stays together, and note it in that version's row in the brief.

If it runs long, cut words. Never shrink the font or the margins to fit.

## Sounding Human

Letters are prose, and readers have strong instincts about how people write. `references/ai-fingerprint.md` has the full list, but three things carry most of the weight:

- **Vary sentence length.** Uniform 15-to-20-word sentences read as generated. Mix short and long deliberately.
- **One concrete human detail.** An outage you owned, a customer conversation that changed your mind, a bug that took a week. Brief and specific.
- **Contractions are fine.** "I've" and "didn't" read as a person.
