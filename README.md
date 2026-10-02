# Resume Studio

Write your career down once. Generate a tailored, page-perfect resume for every application after that.

Most AI resume tools take your resume plus a job description and hand back a rewrite. They don't know you contributed to a system rather than owned it, or that the impressive number came from a prototype that never shipped. They'll quietly upgrade "contributed to" into "built," and you won't notice until an interviewer asks a follow-up question.

Resume Studio splits the problem in two.

**The master resume** is an unbounded markdown document. Four pages, ten, twenty. Every project, every metric, every detail that won't fit anywhere. You never submit it. It exists so that no application ever starts from whatever you happen to remember that day.

**Target resumes** are derived from it. One page or two, LaTeX, fitted to the exact character budget of the template so nothing overflows or looks half-empty. Each one selects from the master and reframes for a specific reader, and each settled version is saved as v1, v2, and so on.

Everything is discussed in markdown and only becomes LaTeX after you say the content is right.

---

## Quick Start

1. **Get it:** `git clone https://github.com/Amruth-Ashok/resume-studio.git`
2. **Open the folder** in Cursor or Claude Code.
3. **Start a chat** and say *"Help me with my resume"*, or type `/resume-start`.

It asks a few questions to get set up: who you are, what resumes or documents you already have, and which roles you're aiming at. Then it walks you through everything else. Your resume data lives in this folder and is gitignored, so `git pull` updates the tool without touching your files.

Saying "start" always works, because `AGENTS.md` and `CLAUDE.md` tell the agent where the skills are. The `/resume-start` slash command appears once the plugin is installed (below).

### Keep your data in a separate folder

Install it as a plugin, then start a chat in any folder:

- **Cursor:** open Customize, add a plugin **From GitHub Repository**, enter `Amruth-Ashok/resume-studio`, and install it.
- **Claude Code:**
  ```
  /plugin marketplace add Amruth-Ashok/resume-studio
  /plugin install resume-studio@resume-studio
  ```

Or keep a clone anywhere and put an `AGENTS.md` in your data folder pointing at it:

```markdown
This folder holds my resume data for Resume Studio. The plugin is at ../resume-studio.
Read ../resume-studio/AGENTS.md and follow it. Skills are in ../resume-studio/skills/.
```

### Requirements

- **Python 3** for the character counter and the live preview
- **A LaTeX distribution** to produce PDFs. On macOS, TinyTeX installs into your home folder with no admin password, so the agent can run it for you:
  ```bash
  curl -fsSL https://github.com/rstudio/tinytex-releases/releases/download/daily/TinyTeX-1-darwin.tar.xz | tar -xJ -C ~/Library
  echo 'export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"' >> ~/.zshrc && source ~/.zshrc
  tlmgr install lastpage parskip enumitem fontawesome pgf fancyhdr moderncv fontawesome6 multirow colortbl ragged2e microtype babel-english lm
  ```
  Already have MacTeX or BasicTeX? Just run the `tlmgr install` line with `sudo`. Everything except the final PDF works without LaTeX.

---

## How It Works

Three phases, each a guided conversation. Every phase writes down where it stopped, so you can close the chat and pick up in a new one; `/resume-start` tells you where you left off.

**1. Setup.** `/resume-start` asks about you, what you already have (a master resume, role-specific resumes, review packets, or nothing at all), and what you're targeting, with job-description links where you have them. It creates your config, a `sources/originals/` folder for your documents, and one folder per target.

**2. The master resume.** `/master-resume` reads everything in `sources/originals/` and merges it into `sources/master-resume.md`. Then comes the deep dive: one experience at a time, one achievement at a time, it asks about what your old resumes compressed away, like what you actually owned, what the numbers were, and what shipped. With nothing written down, it runs as an interview instead. Expect this to take a while. You only do it once; later, new work gets appended.

**3. Targets, one at a time.** `/resume-target` proposes which achievements to use for that role and why, then drafts in markdown with you until it reads right. `/resume-render` turns it into LaTeX and a PDF that fits the page exactly. When you're happy, `/resume-version` saves it as **v1**. Then `/resume-review` for a scored critique, and `/cover-letter` if you need one.

While drafting, keep the live preview open:

```bash
python3 scripts/preview.py
```

It serves `http://localhost:8000` with every draft rendered in resume styling, A4 page boundaries drawn so overflow is obvious, and every bullet colour-coded against its character budget. Saves show up within a second. No dependencies, no LaTeX required.

---

## Versions

Each target keeps a numbered history. `draft.md` is always the working copy; when you say a resume is settled, the draft and its PDF are frozen into `versions/v1/`, and every later change becomes v2, v3, and so on. Each version records the date, what changed since the last one, and which master it came from.

Things you can just ask for:

- *"This one's good, save it."*
- *"What changed between v1 and v2?"*
- *"Go back to v1 and start from there."*
- *"I sent v2 to Acme."*

The file to send is always `targets/<name>/versions/vN/resume.pdf`.

---

## Skills

| Skill | What it does |
|-------|-------------|
| `resume-start` | Setup Q&A for new users, "where you left off" for returning ones |
| `master-resume` | Builds the master from documents or by interview, deep dives it, appends new work |
| `resume-target` | Selects and drafts a tailored resume in markdown, iterating with you |
| `resume-preview` | Live localhost render with page breaks and per-bullet budget colours |
| `resume-render` | Fits the confirmed draft to the character budget, compiles the PDF |
| `resume-version` | Saves settled resumes as v1, v2, ..., compares them, restores old ones |
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
resume-config.md            # Your contact info, preferences, links to your documents
sources/
  master-resume.md          # The source of truth
  originals/                # The resumes and documents you started from
targets/
  acme-senior-swe/          # One folder per target: a posting or a role family
    brief.md                # What it's for, decisions, version history
    jd.md                   # The job description text
    draft.md                # Working copy, iterated with you
    resume.tex/.pdf         # Latest build
    versions/
      v1/                   # Frozen: draft, LaTeX, PDF
      v2/
```

Your data is gitignored by default. The repo ships skills, not your career history. The full rules live in `references/workspace.md`.

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
