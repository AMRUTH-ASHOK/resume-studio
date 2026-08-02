---
name: master-resume
description: Builds or updates the master resume, an unbounded markdown document that serves as the single source of truth for all tailored resumes. Use when the user wants to create a master resume from existing documents or from scratch, add a new job or project to their master resume, record recent accomplishments, or when a target resume is blocked because the master is missing or out of date.
---

# Master Resume

Builds and maintains `master-resume.md`, the source of truth every tailored resume is derived from.

## Paths

- **Plugin root** holds `references/`, `assets/`, `scripts/`. If a path doesn't resolve, glob for the filename.
- **Workspace** is the user's current folder.

Read `references/master-resume-format.md` before writing anything. It defines the required structure.

## The One Rule

**The master resume has no length limit.** Not two pages. Not five. However long it takes.

This inverts every instinct trained by normal resume writing, so state it out loud to the user once. The master is never submitted anywhere. Its only job is to hold every fact a future resume might need, in enough detail that a tailored version can be assembled without going back to the user.

Concretely, that means:
- Every position, including old and tangential ones
- Every project inside each position, not just the headline ones
- Multiple achievements per project
- Full metrics, even ones that seem unimpressive today
- Detail that will never fit on a page: what was hard, what you'd do differently, who else was involved
- Failed or sunset projects. They're often the best interview material.

When in doubt, include it. Cutting is `resume-target`'s job, and it can only cut what exists.

## Mode Detection

Check for `master-resume.md`:

- **Missing** → Build mode. Go to Step 1.
- **Exists** → Update mode. Skip to Update Mode below.

## Step 1: Choose an Input Path

Check `sources/` for files.

**Files present** → Document mode. Go to Step 2.

**Empty** → Ask which applies:
- They have a resume or docs to share → have them drop files into `sources/`, then Document mode
- They'd rather talk it through → Interview mode, Step 4
- Some of each → Document mode first, then Interview mode to fill the gaps

Cloud document links can't be read. Ask for an export to `.md`, `.txt`, `.pdf`, or `.docx` in `sources/`.

## Step 2: Read the Documents

Read every file in `sources/`.

**Treat existing resume bullets as pointers to work, never as finished text.** A resume bullet is already compressed and has already lost detail. "Improved pipeline reliability" is a pointer to a story you need to recover: what was breaking, what you changed, what the numbers were before and after. Never copy a bullet straight into the master.

Multiple source documents will overlap. **Merge, don't duplicate.** The same job described in three resume variants usually yields three partial views of the same work; combine them into one richer entry. Where two sources conflict on a number or a date, flag it and ask.

Extract per position:
- Employer, team, title, dates, location
- Every distinct project or system
- Technologies actually used
- Every number present
- Any hint about scope and ownership

## Step 3: Report the Gaps

Before writing, show the user what you found and what's missing. A table works well here:

| Position | Projects found | Has metrics | Ownership clear |
|----------|---------------|-------------|-----------------|

Then ask about the gaps. Go to Step 5.

## Step 4: Interview Mode

Work backwards from the current role. For each position, establish the frame first (title, employer, team, dates, what the team was responsible for), then work through projects one at a time.

**Ask about one project at a time.** Batching questions produces thin answers on all of them.

Per project:
1. What was the problem? What was broken, missing, or slow, and who did it hurt?
2. What did you personally build? Where does your work end and a teammate's begin?
3. Were you the owner, the tech lead, or a contributor?
4. What are the numbers? Before and after, scale, adoption, cost, latency, revenue, time saved.
5. Did it ship? Is it still running?
6. What was genuinely hard about it?
7. Who else was involved, and what did they do?

**Push once on vague metrics, then move on.** "It got faster" becomes "roughly how much faster, and from what baseline?" If they don't know, record it as unquantified and flag it. Don't interrogate; a flagged gap they can fill later beats an invented number.

**Watch for understatement.** People routinely bury their best work. If someone mentions in passing that they "also set up the on-call rotation for the team," that's a leadership signal worth its own entry.

Between positions, checkpoint: "That's [Employer] captured, [N] projects. Ready for the next one, or want to add more here?"

## Step 5: Write the Master Resume

Follow the structure in `references/master-resume-format.md` exactly.

Sections beyond work history are optional and should only appear when the user has real content for them: education, projects, publications, patents, talks, open source, certifications, awards, leadership, coursework. Grad school and research applications lean on these heavily, so capture them even if no current job target needs them.

Every achievement entry carries metadata that `resume-target` depends on:
- `Scope` — sole owner, tech lead, co-owner, contributor
- `Status` — shipped and running, shipped and sunset, prototype, internal, POC
- `Metrics` — with baselines where known
- `Tech` — what was actually used
- `Tags` — which kinds of roles this is evidence for
- `Confidential` — anything that can't appear verbatim in a public document

Write the file. Then report: positions, projects, achievements, and how many lack metrics.

### >>>>>> STOP <<<<<<
Present the master resume and the gap list. Wait for the user to review.

Expect corrections. People spot errors in their own history immediately, and the first read usually produces several. Apply them, then confirm.

## Update Mode

Triggered when `master-resume.md` already exists.

1. Read the current master
2. Ask what's new. Common cases: a new job, a new project in the current job, a promotion or title change, new metrics on existing work now that time has passed, a new certification or talk
3. Interview on the new material using the Step 4 questions
4. **Append, don't rewrite.** Insert new entries in the right position and leave everything else untouched. The master accumulates.
5. If the new work supersedes an old entry, keep both and note the relationship. Old versions of a story are still true.
6. Update the metadata block at the top of the file with the new date and counts

Never silently delete anything from the master. If the user wants something gone, confirm first, because deleted context is expensive to reconstruct.

### >>>>>> STOP <<<<<<
Show a diff-style summary of what was added. Wait for confirmation.

## Quality Bar

Before declaring the master done, check:

- [ ] Every position has dates, title, employer, and team
- [ ] Every achievement states scope and status
- [ ] Metrics have baselines where the user knew them
- [ ] Confidential material is flagged
- [ ] Nothing was copied verbatim from an old resume bullet
- [ ] Thin entries are flagged rather than padded with filler
- [ ] Older positions are present even if brief

## Handing Off

> "Master resume ready: [N] positions, [M] achievements, [K] flagged as thin. Next: `resume-target` when you have a role in mind. Worth filling the flagged gaps first if you can find the numbers."
