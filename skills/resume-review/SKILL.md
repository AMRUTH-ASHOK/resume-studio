---
name: resume-review
description: Reviews a tailored resume against its target from five reader perspectives and scores it across seven weighted dimensions, returning ranked fixes and an interview-likelihood estimate. Use when the user wants feedback on a resume, asks how strong their resume is for a specific role, wants to know what to improve before applying, or asks for a critique, review, or score.
---

# Resume Review

Scores a rendered resume against its target and returns ranked, specific fixes.

## Paths

- **Plugin root** holds `references/`, `assets/`, `scripts/`. If a path doesn't resolve, glob for the filename.
- **Workspace** is the user's current folder.

## Best Practice

Run this in a **fresh session**. A review written in the same context that produced the resume inherits every assumption that went into it, and inherited assumptions are exactly what a critique is supposed to catch.

## Load

1. `targets/<slug>/brief.md` — what this is for
2. `targets/<slug>/draft.md` — confirmed content
3. `targets/<slug>/resume.tex` and `resume.pdf` — what actually renders
4. The job or program description
5. `references/review-rubric.md` — the full scoring protocol
6. `references/ai-fingerprint.md` — the detection scan
7. `resume-config.md` — provenance flags and the corrections log
8. `master-resume.md` — needed to verify claims and to find unused evidence
9. Any prior `targets/<slug>/review.md` — note the previous score

If the resume hasn't been rendered, review the draft and say that visual checks were skipped.

## Run

Follow `references/review-rubric.md` in full. It produces:

1. **Reader lens** — who actually reads this, what they've seen a hundred times, what would surprise them
2. **Five perspectives** — ATS scan, recruiter at 10 seconds, HR at 30, hiring manager at 2 minutes, technical reviewer at 10, each with a verdict
3. **Seven-dimension score** out of 100
4. **Interview likelihood** per reader, plus a ceiling estimate
5. **Ranked fixes** in three tiers by point impact
6. **Interview bridges** — how to talk about each claim out loud
7. **AI fingerprint scan** — the 12-item checklist
8. **Mechanical verification** — character counts, orphans, page fill, escapes

Scoring weights: ATS keywords 15, summary 10, skills 10, bullet quality 30, narrative coherence 15, page fill and visual 5, credibility signals 15.

## Two Checks That Need the Master

**Truthfulness.** Every metric and ownership claim on the resume must trace back to an entry in `master-resume.md` with compatible `scope:` and `status:` tags. A bullet saying "Built" where the master says `contributor` is a Tier 1 fix, not a style note. Verify each one rather than spot-checking.

**Unused evidence.** You can see the full master, so you can see what was left out. If a stronger achievement was passed over, say so. This is the highest-value thing a reviewer with master access can offer, and it's invisible to any external reader.

## Report

Write to `targets/<slug>/review.md`.

Lead with the score and the three highest-impact fixes. The full breakdown goes below for whoever wants it, but most of the value is in the first ten lines.

Be specific. "Strengthen the summary" is useless. "The summary's second sentence describes what your team did, not what you did; replace it with the feature-store bullet's ownership claim" is actionable.

Be honest about the ceiling. If the background genuinely doesn't fit and no rewrite closes the gap, say so plainly. Telling someone their resume is an 85 when it's a 68 costs them weeks.

### >>>>>> STOP <<<<<<
Present the score, the Tier 1 fixes, and the interview likelihood. Wait for the user.

If they want changes: route to `resume-target` for content, then `resume-render`. Content changes belong in the draft, never in the `.tex`.

## Re-Review

On a second pass, state what changed since the last review, re-score only the affected dimensions, and track the trajectory. Declare a ceiling when the score stops moving, usually after two or three passes. Continuing past that point is polish with no return.
