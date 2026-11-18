# LaTeX Budgets

Character and page budgets for `assets/templates/resume.cls`. Read by `resume-render`.

These numbers are compile-verified against **10pt, `textwidth=7.5in`**. If you change the font size, margins, or text width, every number below is invalid and must be recalibrated.

---

## Character Limits

A line holds roughly 111-115 rendered characters, varying with the character mix.

| Variant | Lines | Target | Hard max | Orphan threshold |
|---------|-------|--------|----------|------------------|
| 1L bullet | 1 | 105-111 | 117 | n/a |
| 2L bullet | 2 | 189-205 | 218 | last line >= 78 |
| Skill line | 1 | 105-111 | 117 | must not wrap |
| Summary | 5 | 500-555 | 570 | last line >= 78 |
| Tagline | 1 | 80-95 | 111 | n/a |

**Rendered characters** means what a reader sees. Strip markup before counting: `\textbf{X}` → `X`, `\textit{X}` → `X`, `\href{url}{text}` → `text`, `--` → 1 char, `$\vert$` → 1 char.

### Aim for the middle

A bullet at 218 characters is not "just within budget," it's a coin flip. Proportional fonts give `m`, `w`, `W`, and capitals far more width than `i` or `l`, so two bullets with identical character counts can differ by most of a line in rendered width. Target 200 for a 2L bullet and the variance stops mattering.

### Bold costs width

```
effective line limit = 119 - (0.5 × bold_chars)
```

| Bold chars | Effective limit | Practical target |
|-----------|----------------|------------------|
| 0 | 119 | 105-111 |
| 10-25 (2-4 tools) | 107-112 | 105-111 |
| 28+ (5+ tools) | ~105 | 99-105 |

This bites hardest in the skills section, where bolding five tool names on one line can cost a whole line of capacity.

### Em-dashes

`---` counts as one character but renders about twice as wide. Budget two extra characters per em-dash. Cap the whole document at two em-dashes regardless.

### The orphan rule

A multi-line bullet whose last line holds four words looks careless. The last rendered line must fill at least 70% of the width, which is 78 characters. If it doesn't, either enrich the bullet to fill the line or cut it down to one fewer line.

---

## Page Budgets

### Two pages

| Section | Lines |
|---------|-------|
| Header (name, contact, links, tagline) | 5-6 |
| Summary | 6 (1 heading + 5 body) |
| Skills, 5 groups at 4-3-2-2-2 | 18 (1 heading + 5 group names + 13 dashes) |
| Experience bullets | ~40-42 rendered lines |
| Education | 4-5 |
| Honors & Awards | 4-5 |
| Work authorization | 2 |

Working budget: **20-21 two-line bullets.**

Adjustments:

| Change | Effect on bullet budget |
|--------|------------------------|
| Skills 4-4-2-2-2 instead of 4-3-2-2-2 | -1 bullet |
| Drop Honors & Awards | +2 bullets |
| Drop work authorization line | +1 bullet |
| Add a fourth position header | -1 bullet |
| Each optional section added | -2 to -3 bullets |

### One page

| Section | Lines |
|---------|-------|
| Header | 4-5 |
| Summary | 4 (1 heading + 3 body) |
| Skills, 3-4 groups | 11-13 |
| Experience bullets | ~18-20 rendered lines |
| Education | 3 |

Working budget: **8-10 two-line bullets.**

One page forces real choices. Guidance:
- Two or three positions maximum. Older roles collapse to a title line with no bullets, or drop off.
- Shorten the summary to three body lines.
- Skills drops to three or four groups.
- Drop every optional section. Awards, work authorization, side projects all go.
- Weight bullets heavily toward the most recent position. A one-page resume that spreads evenly across four jobs says nothing about any of them.

### Page fill

The last page should end with no more than about three lines of white space. A second page that stops halfway looks unfinished and reads worse than a well-packed single page. If a two-page draft can't fill past roughly two-thirds of page two, switch to one page.

---

## Verification

```bash
python3 scripts/char_count.py targets/<slug>/resume.tex
```

Checks every `\item` bullet and every `\skilldash` line, applies the bold penalty, and prints a violations list. The tool is authoritative. Never override it with an estimate.

Single string check:

```bash
python3 scripts/char_count.py "Built \textbf{Spark} pipelines that cut latency 80%"
```

---

## Immutable Elements

Never modify these in generated output. They're calibrated, and adjusting them to make content fit is how a resume ends up looking subtly wrong.

- `\vspace` values between sections
- `\geometry` settings (margins, textwidth, textheight)
- `.cls` formatting: font sizes, section rules, item separators, skill group spacing
- Header layout structure

When content doesn't fit, change the content. Not the geometry.

---

## Common Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Spills to an extra page | A "2L" bullet rendering as 3L | Run the counter; find the bullet over 218 |
| Date wraps below the title | Position theme line too long | Shorten the theme, not the date |
| Skills line wraps | Bold penalty ignored | Recompute against `119 - 0.5 × bold` |
| Ragged bullet endings | Orphan rule ignored | Enrich to fill, or cut to one line |
| Compile error on a company name | Unescaped `&` | Escape `& % $ # _ { }` |
| Stray `~` renders as a space | `~` is a non-breaking space in LaTeX | Use `$\sim$` for "approximately" |
