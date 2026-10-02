---
name: master-resume
description: Builds, deepens, and updates the master resume, an unbounded markdown document that serves as the single source of truth for all tailored resumes. Use when the user wants to create a master resume from existing documents or from scratch, go through their master experience by experience to add detail, add a new job or project, record recent accomplishments, or when a target resume is blocked because the master is missing or out of date.
---

# Master Resume

Builds and maintains `sources/master-resume.md`, the source of truth every tailored resume is derived from.

## Paths

Read `references/workspace.md` for the layout and `references/master-resume-format.md`
for the required structure before writing anything. If a path doesn't resolve, glob for
the filename.

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

Check `sources/master-resume.md`:

- **Missing** → Build mode. Go to Step 1.
- **Exists, header says `Deep dive: complete`** → Update mode, unless the user asks to go deeper.
- **Exists, deep dive not complete** → Deep Dive mode, resuming where the header says it stopped.

## Step 1: Choose an Input Path

Check `sources/originals/` for files.

**Files present** → Document mode. Go to Step 2.

**Empty** → Ask which applies:
- They have a resume or docs to share → have them drop files into `sources/originals/`, then Document mode
- They'd rather talk it through → Interview mode, Step 4
- Some of each → Document mode first, then Interview mode to fill the gaps

Check `## Source Documents` in `resume-config.md` for links. If you have a connector that can read one, export it into `sources/originals/`; otherwise ask for a `.md`, `.txt`, `.pdf`, or `.docx` export into that folder.

## Step 2: Read the Documents

**Convert anything that isn't already markdown or text.** Write the results to
`sources/originals/converted/` as `.md` so the user can read them in preview mode and
diff them against each other. Delete that folder once the master is written; the
originals stay as the record, and leftover conversions get mistaken for a second master.

```bash
mkdir -p sources/originals/converted
# Preferred, preserves headings and bullets:
pandoc -f docx -t markdown --wrap=none "sources/originals/FILE.docx" -o "sources/originals/converted/FILE.md"
# macOS fallback when pandoc isn't installed (plain text, add structure by hand):
textutil -convert txt -output "sources/originals/converted/FILE.txt" "sources/originals/FILE.docx"
```

With the `textutil` fallback, the output is unstructured. Rewrite it as markdown with
headings and bullet lists, preserving the wording exactly. Never paraphrase source
material during conversion; fidelity matters because these are the record of what the
user actually claimed.

Normalize filenames while converting. Ampersands and spaces in filenames cause shell
quoting failures later.

PDFs can go straight through the Read tool. Only ask the user to re-export if a file
resists every conversion path.

Read every converted file.

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

Write the file to `sources/master-resume.md`, with `> Deep dive: not started` and a `> Next:` line in the header. Then report: positions, projects, achievements, and how many lack metrics.

### >>>>>> STOP <<<<<<
Present the master resume and the gap list. Wait for the user to review.

Expect corrections. People spot errors in their own history immediately, and the first read usually produces several. Apply them, then offer the deep dive.

## Deep Dive Mode

A first build captures what the documents said. The deep dive recovers what they
compressed away. It walks the master **one experience at a time, one achievement at a
time**, and it's what turns a merged document into a source of truth.

It's long, so it's built to stop and resume. Progress lives in the header:

```markdown
> Deep dive: in progress | [Employer, Title] | [Achievement name] next | [N] open questions
> Next: [the exact question or entry to pick up]
```

### Order

Work in the order the master lists things: positions newest first, achievements top to
bottom within each, then education, then the optional sections. Start with
**Profile** and **Team context** for each position before its achievements, since they
frame everything below.

### Per achievement

1. **Show it.** Quote the current entry briefly, so the user is reacting to what's
   written rather than to what they remember.
2. **Ask only what's missing.** Use the Step 4 questions, but skip any the entry already
   answers well. Typical gaps: ownership, the baseline behind a metric, whether it
   shipped, who else was involved, what was hard. Two or three questions at a time,
   never the full list.
3. **Apply the answers** to the entry, including its `scope:` and `status:` tags and
   provenance notes. If an answer conflicts with what a source document claimed, flag it
   and ask which is right.
4. **Move items** the user can't answer now into `## Gaps & TODOs`, rather than
   blocking on them.
5. **Update the header** to point at the next achievement.

Accept "skip", "remove this", and "merge this with X" as answers. Removing something
still needs a one-line confirmation.

### Checkpoints

After each position: "[Employer] is done: [N] achievements, [K] open questions. Next is
[Position]. Carry on, or stop here?" Stopping is always fine; the header already says
where to resume.

### Finishing

When every section has been through, run the Quality Bar below. Set
`> Deep dive: complete` and `> Next: build a target with resume-target`, then hand off.
Remaining open questions can stay in `## Gaps & TODOs`; they don't block targets.

## Update Mode

Triggered when `sources/master-resume.md` exists and the deep dive is complete.

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

After a first build:

> "Master resume written: [N] positions, [M] achievements, [K] flagged as thin. Next: the deep dive, one experience at a time, starting with [first position]."

After the deep dive:

> "Master resume complete: [N] positions, [M] achievements, [K] open questions parked in Gaps & TODOs. Next: `resume-target`, starting with [first target in targets/]."
