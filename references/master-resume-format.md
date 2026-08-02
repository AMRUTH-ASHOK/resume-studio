# Master Resume Format

The structure of `master-resume.md`. Read by `master-resume` when writing, and by `resume-target` when selecting.

The format is optimized for two readers: a human skimming their own history, and a generator selecting evidence for a specific target. That's why metadata sits inline with each achievement rather than in a separate index.

---

## Skeleton

````markdown
# Master Resume — [Full Name]

> Source of truth. Never submitted. No length limit.
> Last updated: [date] | [N] positions | [M] achievements

---

## Profile

**Current role:** [title] at [employer]
**Years of experience:** [N]
**Core domains:** [3-5 areas you have real depth in]
**Open to:** [role types you'd take]

---

## Experience

### [Employer] — [Team or Org]
**[Title]** | [Mon YYYY] – [Mon YYYY or Present] | [Location]

**Team context:** [What the team owned. One or two sentences. This helps a future
reader understand the scope your work sat inside.]

**Titles held:** [Only if you were promoted. List each with dates.]

---

#### [Project or System Name]
`scope: tech lead` `status: shipped & running` `tags: platform, data, backend`

**Problem:** [What was broken, missing, or slow. Who it hurt. Why it mattered
to the business.]

**What I built:** [Specifics. Components, architecture decisions, what you
personally wrote versus what the team wrote.]

**Tech:** [Languages, frameworks, platforms, infra actually used]

**Metrics:**
- [Metric with baseline: "p99 latency 1.8s → 340ms"]
- [Scale: "12 internal teams, ~4M events/day"]
- [Business: "roughly $30k/month compute saved" — mark estimates]

**Scale & scope:** [Team size, who reported to you, budget, blast radius]

**Collaboration:** [Who else, doing what. Cross-functional partners.]

**What was hard:** [The genuinely difficult part. Rarely fits on a resume,
often the best interview material.]

**Confidential:** [Anything that can't appear verbatim. Customer names,
unreleased products, internal revenue. Note how to describe it generically.]

**Provenance notes:** [What needs hedging and why]

---

#### [Next Project]
[Same structure. Repeat for every project in this position.]

---

### [Previous Employer] — [Team]
[Same structure. Repeat for every position, oldest last.]

---

## Education

### [Degree], [Field]
**[Institution]** | [Year] – [Year] | [Location]
- **GPA:** [if worth listing]
- **Thesis:** [title and one-line summary, if any]
- **Relevant coursework:** [only if targeting grad programs or early career]
- **Activities:** [if meaningful]

---

## Projects (outside work)
[Side projects, open source, hackathons. Same block structure as work projects,
minus the employer framing.]

---

## Publications & Talks
[Optional. Include if you have any — grad school and research targets need them,
most engineering roles don't. Format: authors, title, venue, year, link.]

---

## Patents
[Optional. Title, number or application status, year.]

---

## Certifications
[Name, issuing body, year, expiry if relevant.]

---

## Awards & Recognition
[Award, granting body, year, one line of context. Include internal awards.]

---

## Leadership & Mentorship
[People managed, mentees, interviewing, onboarding, communities of practice,
on-call ownership, tech lead rotations. Easy to forget, valuable to have.]

---

## Skills Inventory

Grouped, with honest proficiency. `resume-target` picks from this.

### [Category, e.g. Languages]
| Skill | Proficiency | Evidence |
|-------|------------|----------|
| [skill] | expert / proficient / familiar | [which projects] |

---

## Gaps & TODOs
[Things to fill in later. Kept in the file so they don't get lost.]
- [ ] [e.g. "Find the actual adoption number for the feature store"]
````

---

## Metadata Tags

The backtick line under each project heading. `resume-target` reads it to filter.

**`scope:`** — how much of this was yours
| Value | Meaning | Verbs it licenses |
|-------|---------|-------------------|
| `sole owner` | You built it, start to finish | Built, Designed, Architected, Owned |
| `tech lead` | You drove it, others contributed | Led, Drove, Designed |
| `co-owner` | Shared roughly equally | Co-designed, Partnered on |
| `contributor` | You did a defined piece | Contributed, Implemented, Supported |
| `advisor` | You reviewed or guided | Advised, Reviewed |

**`status:`** — what actually happened
| Value | Constraint on framing |
|-------|----------------------|
| `shipped & running` | No constraint |
| `shipped & sunset` | Past tense; don't claim ongoing adoption |
| `prototype` | Must say prototype or proof of concept |
| `internal` | Fine to claim; describe generically if confidential |
| `poc` | Never imply production |
| `cancelled` | Usually omit; can be honest interview material |

**`tags:`** — free-form role-type hints (`platform`, `ml`, `customer-facing`, `research`, `leadership`, `data`, `infra`). Used for coarse filtering, so approximate is fine.

---

## Proficiency Definitions

Use these consistently. Inflation here propagates into every resume.

- **Expert** — owned production systems with it, made architecture decisions, colleagues came to you with questions
- **Proficient** — shipped real work with it, comfortable working independently
- **Familiar** — used it on one project, or worked next to someone who owned it

A skill listed in a job description does not become Expert because you want the job.

---

## Metric Hygiene

- Always include the baseline. "340ms p99" means nothing without the 1.8s it replaced.
- Mark estimates explicitly: `[estimated]`. Estimates are usable if hedged, dangerous if presented as measured.
- Prefer the number you can defend over the number that sounds best. Every figure on a resume is an invitation to be asked about it.
- Record the measurement window. "Adopted by 12 teams" is stronger with "within two quarters."
- No lines-of-code or test counts. They signal activity, not impact.

---

## Why Detail That Won't Fit

"What was hard" and "Collaboration" never appear on a two-page resume. They earn their place because:

- Cover letters need the texture. A letter built only from resume bullets reads like a resume in paragraph form.
- Interview prep comes free. The story behind a bullet is the answer to the follow-up question.
- Reframing needs raw material. The same project sold to a platform team and a customer-facing team leans on completely different details, and you can't reframe what you didn't record.
