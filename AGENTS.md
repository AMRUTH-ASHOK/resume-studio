# Resume Studio

This repository is Resume Studio: agent skills for building a master resume and
generating tailored, versioned, page-perfect LaTeX resumes from it. The skills are plain
markdown at `skills/<name>/SKILL.md`. If they aren't loaded as skills in this session,
read the right `SKILL.md` and follow it exactly as if it were.

## Where to Start

When the user opens a chat about their resume, says "start", "set me up", "where was
I", or "what's next", or doesn't make a specific request, read
`skills/resume-start/SKILL.md` and follow it. It runs the setup Q&A for a new user and
reports where a returning user left off.

## Skills

| Skill | Use when the user wants to |
|-------|----------------------------|
| `resume-start` | Begin, get set up, or find out where they left off |
| `master-resume` | Build the master resume, go through it experience by experience, or add new work |
| `resume-target` | Create or revise a resume for a specific role, posting, or program |
| `resume-preview` | See resumes rendered with page breaks and length checks at localhost |
| `resume-render` | Turn a confirmed draft into LaTeX and a PDF |
| `resume-version` | Save a settled resume as v1, v2, ..., compare versions, or go back to one |
| `resume-review` | Get a scored critique of a resume against its target |
| `cover-letter` | Write a cover letter to go with a resume |

## Rules for Every Session

- `references/workspace.md` defines where user data lives, how progress is recorded,
  and how versions work. Read it before touching user files.
- User data (`resume-config.md`, `sources/`, `targets/`) is gitignored. Never commit it,
  and never force-add it.
- Accuracy beats impressiveness. Never upgrade what someone did ("contributed to" into
  "built") and never invent a number.
- Before a session stops partway, update the relevant `Next:` line so the next chat can
  resume without the user remembering anything.
