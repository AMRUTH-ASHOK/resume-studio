# Bullet Craft

How to turn a master resume entry into a bullet for a specific target. Read by `resume-target`.

---

## The Core Move

Write the bullet fresh, from the master entry, in the target's vocabulary.

Do not copy the master's phrasing. Do not write it in your own team's language and translate afterwards. Translation leaves seams: a bullet drafted as "optimized our Delta ingestion DAGs" and then find-replaced into "built scalable data pipelines" reads like exactly what it is.

Reframing done during writing is the single highest-return step in the whole process. It moves a resume from roughly a 60 to roughly an 85 on the review rubric, and no amount of polish afterwards substitutes for it.

---

## Anatomy

```
[Verb matching your actual scope] + [what you built, in their words]
+ [the result, quantified] + [scale or adoption, if it strengthens]
```

**Good:**
> Built a Spark Structured Streaming pipeline that replaced a nightly batch job, cutting p99 ingest latency from 1.8s to 340ms and unblocking near-real-time reporting for 12 internal teams.

Concrete verb, named technology, before-and-after metric, scope, and it ends on a business outcome.

**Bad:**
> Leveraged cutting-edge streaming technologies to significantly improve data pipeline performance, enabling enhanced reporting capabilities across the organization.

Banned verb, no named technology, no number, vague scope, ends on an `-ing` phrase.

Same work. The second one tells a reader nothing they can ask a follow-up question about.

---

## Verb Discipline

The verb must match the `scope:` tag in the master. This is not stylistic.

| Master says | Verbs available | Never use |
|-------------|----------------|-----------|
| `sole owner` | Built, Designed, Architected, Owned, Created | — |
| `tech lead` | Led, Drove, Designed, Directed | Single-handedly |
| `co-owner` | Co-designed, Partnered on, Built with | Built (unqualified) |
| `contributor` | Contributed, Implemented, Supported, Added | Built, Led, Owned, Designed |
| `advisor` | Advised, Reviewed, Guided | Any build verb |

When two verbs both seem defensible, take the weaker one. The cost of under-claiming is a slightly less impressive bullet. The cost of over-claiming is a hiring manager discovering it in an interview, which ends the process and does it while thinking about your integrity rather than your skills.

## Status Discipline

| Master says | Required framing |
|-------------|-----------------|
| `shipped & running` | No constraint |
| `shipped & sunset` | Past tense. No ongoing-adoption claims. |
| `prototype` / `poc` | Must contain "prototype" or "proof of concept" |
| `internal` | Fine to claim. Describe generically if flagged confidential. |
| `cancelled` | Usually omit |

---

## The Theme Line

Above each position sits a bold line that is **not** the job title. The real title goes underneath in italics.

```
Streaming Data Platforms & Real-Time Analytics
Senior Software Engineer, Acme                              Mar 2023 – Present
```

This is the strongest tailoring lever available, because it's the first thing a reader's eye lands on under each job, and unlike the title it's yours to choose. The same position becomes "Distributed Systems & Platform Reliability" for an infrastructure role and "Customer-Facing Data Solutions" for a solutions engineering role.

Two constraints: the theme must be an honest description of what you did, and the real title underneath never changes. Inventing a title is fraud; choosing which true aspect of the job to foreground is just writing.

The theme line plus the date must fit on one line. If the date wraps, shorten the theme.

---

## Ordering

Within a position, the first bullet is the one most relevant to this target, not the most impressive in absolute terms and not the chronologically first. Many readers read only the first bullet under each job.

Across positions, reverse chronological. Weight bullet counts by relevance rather than splitting evenly: a role that maps directly onto the target earns five or six bullets, a tangential one earns two.

---

## Bridging Gaps

When the target wants something you don't have, but you have something adjacent:

**Honest bridge:**
> Deep experience with Databricks and Spark; the same distributed-execution model underlies Snowflake's compute layer.

The substitution is visible. A reader knows exactly what you have.

**Dishonest bridge:**
> Experienced with Snowflake and other modern data warehouses.

A reader comes away believing you've used it. You haven't.

Bridge only when the underlying skill genuinely transfers. For a true gap, say nothing on the resume and prepare an answer for the interview. A resume that quietly claims a skill you lack converts a "we'd like to teach you this" into a "you misrepresented yourself."

---

## What Not to Include

- Lines of code, test counts, commit counts. Activity, not impact.
- Internal project code names a reader won't recognize. Describe what it does.
- Responsibilities without outcomes. "Responsible for maintaining the build system" is a job description, not an achievement.
- Numbers you can't defend under questioning.
- Confidential customer names, unreleased products, internal revenue figures.

---

## Sentence Endings

Never end a bullet with an `-ing` analysis phrase. It's the most reliable structural tell of generated text.

| Bad | Why | Fixed |
|-----|-----|-------|
| ...improving system reliability | Vague, `-ing`, no number | ...cutting incident volume by half |
| ...enabling faster development | Vague, `-ing` | ...cutting CI time from 22 to 6 minutes |
| ...contributing to a 15% reduction | `-ing` but lands on a metric | Acceptable |

End on a result, a metric, or a concrete object.

---

## Length Targets

Roughly 23-25 words for a two-line bullet, 13 for a one-line bullet, at about 7.9 characters per word.

These are drafting heuristics only. `resume-render` does the real measurement, and skills lines have no word proxy at all because technical tool lists run near 11 characters per word.

---

## Quality Check

Per bullet:

- [ ] Verb matches the master's `scope:` tag
- [ ] Framing respects the `status:` tag
- [ ] Contains a number, or a good reason it doesn't
- [ ] Every number traces to the master
- [ ] Uses the target's vocabulary, not your team's
- [ ] Doesn't end on an `-ing` phrase
- [ ] No banned words (see `ai-fingerprint.md`)
- [ ] A stranger could ask one follow-up question about it
