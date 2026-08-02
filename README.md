# Resume Studio

Write your career down once. Generate a tailored, page-perfect resume for every application after that.

Most AI resume tools take your resume plus a job description and hand back a rewrite. They don't know you contributed to a system rather than owned it, or that the impressive number came from a prototype that never shipped. They'll quietly upgrade "contributed to" into "built," and you won't notice until an interviewer asks a follow-up question.

Resume Studio splits the problem in two.

**The master resume** is an unbounded markdown document. Four pages, ten, twenty. Every project, every metric, every detail that won't fit anywhere. You never submit it. It exists so that no application ever starts from whatever you happen to remember that day.

**Target resumes** are derived from it. One page or two, LaTeX, fitted to the exact character budget of the template so nothing overflows or looks half-empty. Each one selects from the master and reframes for a specific reader.

Everything is discussed in markdown and only becomes LaTeX after you say the content is right.

---

## Install

**Cursor** — clone it and open the folder, or add it as a plugin:

```
/plugin marketplace add Amruth-Ashok/resume-studio
```

**Claude Code:**

```
/plugin marketplace add Amruth-Ashok/resume-studio
/plugin install resume-studio@resume-studio
```

**Or just clone it** and work inside the folder. The skills are plain markdown in `skills/` and both tools discover them.

### Requirements

- **Python 3** for the character counter
- **A LaTeX distribution** to produce PDFs. On macOS:
  ```bash
  brew install --cask basictex
  eval "$(/usr/libexec/path_helper)"
  sudo tlmgr install fontawesome lastpage enumitem moderncv ragged2e
  ```
  Everything except the final PDF works without it.

---

## Use

Start here, in a folder where you want your resume data to live:

```
/resume-start
```

It figures out what you have and routes you. From a standing start the path is:

**1. Build the master.** Drop your existing resume into `sources/` and run `/master-resume`. It reads what you have, then asks about everything the resume compressed away: what you actually owned, what the numbers were, what shipped and what didn't. If you have nothing written down, it runs as an interview instead. Expect this to take a while. It's the only step you do once.

**2. Target a role.** Run `/resume-target`. It asks what the application is for, takes the job description, asks whether you want one page or two, then proposes which achievements to use and why. You confirm the selection, it writes a full draft in markdown, and you go back and forth until it reads right.

While iterating, keep the live preview open:

```bash
python3 scripts/preview.py
```

It serves `http://localhost:8000` with your draft rendered in resume styling, A4 page boundaries drawn so overflow is obvious, and every bullet colour-coded against its character budget. Saves show up within a second. No dependencies, no LaTeX required.

**3. Render.** Run `/resume-render`. Now it becomes LaTeX, gets fitted to the character budget, and compiles. If it overflows or underfills, it tells you exactly what to cut or add rather than silently trimming.

**4. Review.** Run `/resume-review` for a scored critique from five reader perspectives, with ranked fixes. Best in a fresh session.

**5. Cover letter.** Run `/cover-letter` if you need one.

Later applications skip straight to step 2. Adding new work to the master is `/master-resume` again, which switches to append mode.

---

## Skills

| Skill | What it does |
|-------|-------------|
| `resume-start` | Detects your state, sets up the workspace, routes |
| `master-resume` | Builds or updates the master, from documents or by interview |
| `resume-target` | Selects and drafts a tailored resume in markdown, iterating with you |
| `resume-preview` | Live localhost render with page breaks and per-bullet budget colours |
| `resume-render` | Fits the confirmed draft to the character budget, compiles the PDF |
| `resume-review` | Five-perspective critique, seven-dimension score, ranked fixes |
| `cover-letter` | One-page letter that complements the resume rather than repeating it |

Works for job applications, internal transfers, grad school (Master's and PhD), and fellowships. The target type changes what gets emphasized: an admissions committee cares about trajectory and research fit, a hiring manager cares about shipped impact.

---

## Why It Produces Better Resumes

**Ownership is tracked, not guessed.** Every achievement in the master carries a `scope:` tag: sole owner, tech lead, contributor. The verb on the generated bullet has to match. A `contributor` achievement can't become "Built."

**The numbers fit.** A two-line bullet in this template holds 189 to 205 rendered characters, and its second line has to reach 78 or it looks ragged. Bold text costs extra width. `scripts/char_count.py` enforces all of it before anything compiles.

**The theme line does the tailoring.** Above each job sits a bold line that isn't your title, with the real title underneath in italics. The same role reads as "Distributed Systems & Platform Reliability" for one application and "Customer-Facing Data Solutions" for another. Both true, and it's the first thing a reader's eye lands on.

**It doesn't sound generated.** Banned word lists, a rule against bullets ending in `-ing` phrases, an em-dash cap, and a twelve-item scan before anything is presented.

**Detail that won't fit still gets captured.** The master records what was hard about each project and who else was involved. That never reaches the resume, but it's what makes a cover letter specific and what you'll actually say in the interview.

---

## Layout

```
resume-config.md      # Your contact info and preferences
master-resume.md      # The source of truth
sources/              # Documents you drop in
targets/
  acme-senior-swe/
    brief.md          # What this application is for
    draft.md          # Markdown, iterated with you
    resume.tex/.pdf
    cover-letter.tex/.pdf
    review.md
```

Your data is gitignored by default. The repo ships skills, not your career history.

---

## Customizing

- **Visual style** lives in `assets/templates/resume.cls`. Change fonts, spacing, colors there.
- **Character budgets** live in `references/latex-budgets.md`. If you change the font size or margins, recalibrate them or the fitting logic will be wrong.
- **Writing rules** live in `references/bullet-craft.md` and `references/ai-fingerprint.md`.
- **Scoring weights** live in `references/review-rubric.md`.

---

## Credits

Derived from [claude-resume-kit](https://github.com/ARPeeketi/claude-resume-kit) by ARPeeketi (MIT), with the academic and publication machinery removed, the extraction layer generalized, and the master-resume-as-source-of-truth model added. The LaTeX class descends from a template by Trey Hunner via LaTeXTemplates.com.

MIT licensed. See [LICENSE](LICENSE).
