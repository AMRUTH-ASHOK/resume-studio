#!/usr/bin/env python3
"""
Live resume preview server.

Renders markdown resume drafts with styling that approximates the LaTeX output of
resume.cls, overlays A4 page boundaries so overflow is visible, and colour-codes every
bullet against its character budget.

No dependencies. Python 3.8+.

Usage:
  python3 scripts/preview.py                    # serve the current directory
  python3 scripts/preview.py --port 8080
  python3 scripts/preview.py --dir ~/resumes
  python3 scripts/preview.py --no-open          # don't launch a browser

Then edit any markdown file and the browser updates within a second.
"""

import argparse
import html as html_mod
import http.server
import json
import re
import socketserver
import threading
import webbrowser
from pathlib import Path

# Budgets from references/latex-budgets.md, calibrated for resume.cls at 10pt.
BULLET_1L = (105, 111, 117)
BULLET_2L = (189, 205, 218)
ORPHAN_MIN = 78
SKILL_MAX = 119

ROOT = Path.cwd()


# --------------------------------------------------------------------------
# markdown -> html
# --------------------------------------------------------------------------

INLINE = [
    (re.compile(r'\*\*(.+?)\*\*'), r'<strong>\1</strong>'),
    (re.compile(r'(?<!\*)\*([^*\n]+?)\*(?!\*)'), r'<em>\1</em>'),
    (re.compile(r'`([^`]+?)`'), r'<code>\1</code>'),
    (re.compile(r'\[([^\]]+)\]\(([^)]+)\)'), r'<a href="\2">\1</a>'),
]


def inline(text):
    text = html_mod.escape(text)
    for pattern, repl in INLINE:
        text = pattern.sub(repl, text)
    return text


def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def md_to_html(text, resume_mode):
    lines = text.split('\n')
    out = []
    i = 0
    n = len(lines)

    def close_list(stack):
        while stack:
            out.append(f'</{stack.pop()}>')

    list_stack = []
    cur_kind = 'bullet'

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            close_list(list_stack)
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r'-{3,}|\*{3,}|_{3,}', stripped):
            close_list(list_stack)
            out.append('<hr class="rule">')
            i += 1
            continue

        # table
        if stripped.startswith('|') and i + 1 < n and re.match(r'^\|[\s:|-]+\|?$', lines[i + 1].strip()):
            close_list(list_stack)
            header = split_row(stripped)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(split_row(lines[i].strip()))
                i += 1
            out.append('<table><thead><tr>')
            out.extend(f'<th>{inline(c)}</th>' for c in header)
            out.append('</tr></thead><tbody>')
            for row in rows:
                out.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in row) + '</tr>')
            out.append('</tbody></table>')
            continue

        # blockquote
        if stripped.startswith('>'):
            close_list(list_stack)
            block = []
            while i < n and lines[i].strip().startswith('>'):
                block.append(lines[i].strip().lstrip('>').strip())
                i += 1
            out.append(f'<blockquote>{inline(" ".join(block))}</blockquote>')
            continue

        # heading
        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            close_list(list_stack)
            level = len(m.group(1))
            content = m.group(2).strip()

            # In resume mode an h3 is a position header. The line beneath it,
            # "*Title, Employer* | dates", becomes a right-aligned subtitle.
            if resume_mode and level == 3:
                subtitle = ''
                dates = ''
                if i + 1 < n:
                    nxt = lines[i + 1].strip()
                    if nxt.startswith('*') and not nxt.startswith('**'):
                        body = nxt
                        if '|' in nxt:
                            head, _, tail = nxt.rpartition('|')
                            body, dates = head.strip(), tail.strip()
                        subtitle = body.strip().strip('*')
                        i += 1
                out.append('<div class="position">')
                out.append(
                    f'<div class="pos-head"><span class="pos-theme">{inline(content)}</span>'
                    f'<span class="pos-date">{inline(dates)}</span></div>'
                )
                if subtitle:
                    out.append(f'<div class="pos-sub">{inline(subtitle)}</div>')
                out.append('</div>')
                i += 1
                continue

            if level == 2:
                cur_kind = section_kind(content)
            cls = ' class="section"' if (resume_mode and level == 2) else ''
            out.append(f'<h{level}{cls}>{inline(content)}</h{level}>')
            i += 1
            continue

        # list item
        m = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', line)
        if m:
            indent, marker, content = m.group(1), m.group(2), m.group(3)
            tag = 'ol' if marker[0].isdigit() else 'ul'
            depth = len(indent) // 2
            while len(list_stack) > depth + 1:
                out.append(f'</{list_stack.pop()}>')
            if len(list_stack) == depth:
                out.append(f'<{tag}>')
                list_stack.append(tag)
            body = inline(content)
            if resume_mode:
                rendered = strip_md(content)
                cls, note = classify(rendered, cur_kind)
                out.append(f'<li class="{cls}" data-chars="{len(rendered)}" data-note="{note}">{body}</li>')
            else:
                out.append(f'<li>{body}</li>')
            i += 1
            continue

        # paragraph
        close_list(list_stack)
        block = []
        while i < n and lines[i].strip() and not re.match(r'^(#{1,6}\s|\s*([-*+]|\d+\.)\s|\||>)', lines[i]):
            block.append(lines[i].strip())
            i += 1
        joined = ' '.join(block)
        # A bold-only line introduces a skills group.
        if resume_mode and re.fullmatch(r'\*\*.+\*\*', joined):
            out.append(f'<div class="skill-group">{inline(joined)}</div>')
        else:
            out.append(f'<p>{inline(joined)}</p>')

    close_list(list_stack)
    return '\n'.join(out)


# --------------------------------------------------------------------------
# character budget analysis
# --------------------------------------------------------------------------

def strip_md(text):
    """Reduce markdown to what a reader actually sees."""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'\1', text)
    text = re.sub(r'`([^`]+?)`', r'\1', text)
    text = text.replace('---', '\u2014').replace('--', '\u2013')
    return re.sub(r'\s+', ' ', text).strip()


SKILL_WORDS = ('skill', 'expertise', 'technolog', 'stack')
INFO_WORDS = ('publication', 'certification', 'education', 'award', 'honor',
              'header', 'patent', 'talk', 'coursework', 'language')


def section_kind(heading):
    """Different sections have different budgets. A skills line is not a bullet."""
    h = heading.lower()
    if any(w in h for w in SKILL_WORDS):
        return 'skill'
    if any(w in h for w in INFO_WORDS):
        return 'info'
    return 'bullet'


def classify(rendered, kind='bullet'):
    """Return (css class, human note) for one list item."""
    n = len(rendered)
    if n == 0:
        return 'ok', ''

    if kind == 'skill':
        if n <= SKILL_MAX:
            return 'ok', f'{n} chars, fits one line (max {SKILL_MAX} before the bold penalty)'
        return 'over', f'{n} chars, will wrap. Skills lines must fit exactly one line'

    if kind == 'info':
        if n <= BULLET_2L[2]:
            return 'ok', f'{n} chars'
        return 'warn', f'{n} chars, runs past two lines'

    if n <= BULLET_1L[2]:
        lo, hi, _ = BULLET_1L
        if n < lo:
            return 'short', f'{n} chars, short for a 1-line bullet (target {lo}-{hi})'
        if n <= hi:
            return 'ok', f'{n} chars, clean 1-line bullet'
        return 'warn', f'{n} chars, near the 1-line max of {BULLET_1L[2]}'
    if n <= BULLET_2L[2]:
        lo, hi, mx = BULLET_2L
        if n < lo:
            return 'short', f'{n} chars, awkward length. Either fill to {lo}+ or cut to {BULLET_1L[1]}'
        if n <= hi:
            return 'ok', f'{n} chars, clean 2-line bullet'
        return 'warn', f'{n} chars, near the 2-line max of {mx}. Risky with wide characters'
    return 'over', f'{n} chars, OVER the {BULLET_2L[2]} limit. Will spill to a third line'


def walk_items(text):
    """Yield (kind, rendered_text) for every list item, tracking the enclosing section."""
    kind = 'bullet'
    for line in text.split('\n'):
        h = re.match(r'^##\s+(.*)$', line.strip())
        if h:
            kind = section_kind(h.group(1))
            continue
        m = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', line)
        if m:
            yield kind, strip_md(m.group(3))


def summarize(text):
    counts = {'ok': 0, 'short': 0, 'warn': 0, 'over': 0}
    bullets = lines = skills = 0
    for kind, body in walk_items(text):
        cls, _ = classify(body, kind)
        counts[cls] += 1
        if kind == 'bullet':
            bullets += 1
            lines += 1 if len(body) <= BULLET_1L[2] else 2
        elif kind == 'skill':
            skills += 1
    return {'bullets': bullets, 'lines': lines, 'skills': skills, **counts}


# --------------------------------------------------------------------------
# page shell
# --------------------------------------------------------------------------

SHELL = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Resume Preview</title>
<style>
  :root {
    --page-w: 8.27in; --page-h: 11.69in;
    --pad-x: 0.385in; --pad-t: 0.5in; --pad-b: 0.2in;
    --ink: #111; --muted: #6b7280; --line: #d4d4d8;
    --ok: #16a34a; --short: #d97706; --warn: #ea580c; --over: #dc2626;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: #52525b; font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--ink); }

  header { position: sticky; top: 0; z-index: 20; display: flex; gap: 14px; align-items: center;
           padding: 10px 18px; background: #18181b; color: #f4f4f5; box-shadow: 0 1px 6px rgba(0,0,0,.4); }
  header h1 { font-size: 13px; font-weight: 600; margin: 0 8px 0 0; letter-spacing: .3px; }
  select, button { font: inherit; font-size: 12px; padding: 5px 9px; border-radius: 6px;
                   border: 1px solid #3f3f46; background: #27272a; color: #f4f4f5; cursor: pointer; }
  button.on { background: #2563eb; border-color: #2563eb; }
  .stats { margin-left: auto; display: flex; gap: 12px; font-size: 12px; color: #a1a1aa; }
  .stats b { color: #f4f4f5; font-weight: 600; }
  .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; vertical-align: 1px; }

  main { padding: 26px 0 80px; display: flex; justify-content: center; }
  .sheet { position: relative; width: var(--page-w); background: #fff;
           padding: var(--pad-t) var(--pad-x) var(--pad-b); box-shadow: 0 6px 28px rgba(0,0,0,.35); }

  /* Approximates resume.cls at 10pt / 7.5in text width. */
  .doc { font-family: "Latin Modern Roman", "Computer Modern", Georgia, "Times New Roman", serif;
         font-size: 10.5pt; line-height: 1.28; color: #000; }
  .doc h1 { font-size: 25pt; font-weight: 700; margin: 0 0 2px; letter-spacing: .2px; }
  .doc h2.section { font-size: 10.5pt; font-weight: 700; margin: 11px 0 0; padding-bottom: 2px;
                    border-bottom: 1px solid #000; text-transform: none; }
  .doc h2 { font-size: 12pt; margin: 14px 0 4px; }
  .doc h3 { font-size: 11pt; margin: 9px 0 2px; }
  .doc h4 { font-size: 10.5pt; margin: 8px 0 2px; }
  .doc p { margin: 4px 0; }
  .doc ul, .doc ol { margin: 3px 0 3px 0; padding-left: 1.15em; }
  .doc li { margin: 0 0 1.5px; }
  .doc ul { list-style: none; }
  .doc ul > li::before { content: "\00b7"; position: absolute; margin-left: -0.75em; font-weight: 700; }
  .doc ul > li { position: relative; }
  .doc hr.rule { border: 0; border-top: 1px solid #000; margin: 9px 0; }
  .doc blockquote { margin: 6px 0; padding-left: 10px; border-left: 3px solid var(--line);
                    color: var(--muted); font-size: 9.5pt; }
  .doc code { font-family: ui-monospace, Menlo, monospace; font-size: .85em; background: #f4f4f5;
              padding: 1px 4px; border-radius: 3px; }
  .doc table { border-collapse: collapse; width: 100%; margin: 6px 0; font-size: 9pt; }
  .doc th, .doc td { border: 1px solid var(--line); padding: 3px 6px; text-align: left; }
  .doc th { background: #fafafa; font-weight: 600; }
  .doc a { color: #1d4ed8; text-decoration: none; }

  .pos-head { display: flex; justify-content: space-between; align-items: baseline; margin-top: 8px; }
  .pos-theme { font-weight: 700; }
  .pos-date { color: #52525b; font-size: 9.5pt; white-space: nowrap; padding-left: 12px; }
  .pos-sub { font-style: italic; margin-bottom: 2px; }
  .skill-group { font-weight: 700; margin: 5px 0 1px; }

  /* budget colour coding */
  body.budget .doc li.short { background: rgba(217,119,6,.13); box-shadow: -3px 0 0 var(--short); }
  body.budget .doc li.warn  { background: rgba(234,88,12,.14);  box-shadow: -3px 0 0 var(--warn); }
  body.budget .doc li.over  { background: rgba(220,38,38,.14);  box-shadow: -3px 0 0 var(--over); }
  body.budget .doc li[data-note]:hover::after {
    content: attr(data-note); position: absolute; left: 0; top: 100%; z-index: 30;
    background: #18181b; color: #fafafa; font-family: -apple-system, sans-serif; font-size: 11px;
    padding: 5px 9px; border-radius: 5px; white-space: nowrap; box-shadow: 0 3px 10px rgba(0,0,0,.35);
  }

  .pagebreak { position: absolute; left: 0; right: 0; height: 0;
               border-top: 2px dashed #ef4444; pointer-events: none; z-index: 5; }
  .pagebreak span { position: absolute; right: 6px; top: 3px; font: 600 10px -apple-system, sans-serif;
                    color: #fff; background: #ef4444; padding: 1px 7px; border-radius: 0 0 4px 4px; }
  body.nopages .pagebreak { display: none; }

  /* Reference documents are NOT resumes. Make that impossible to miss. */
  .refbanner { display: none; background: #fef3c7; border: 1px solid #f59e0b; border-left-width: 5px;
               color: #78350f; padding: 10px 14px; margin: -0.1in 0 16px; border-radius: 4px;
               font: 13px/1.45 -apple-system, BlinkMacSystemFont, sans-serif; }
  .refbanner b { display: block; font-size: 13px; margin-bottom: 2px; }
  .card.reference .refbanner { display: block; }
  .card.reference { background: #fbfbfa; }
  .card.reference .doc { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                         font-size: 13.5px; line-height: 1.55; }
  .card.reference .doc h1 { font-size: 24px; }
  .card.reference .pagebreak { display: none; }

  .caption { width: var(--page-w); margin: 0 auto 8px; display: flex; align-items: baseline;
             gap: 12px; color: #e4e4e7; font-size: 13px; font-weight: 600; }
  .caption .path { font-weight: 400; font-size: 11px; color: #a1a1aa; }
  .caption .chips { margin-left: auto; display: flex; gap: 8px; font-weight: 400; font-size: 11px; }
  .chip { background: #3f3f46; padding: 2px 8px; border-radius: 10px; color: #e4e4e7; }
  .chip.bad { background: #7f1d1d; color: #fecaca; }
  .chip.mid { background: #7c2d12; color: #fed7aa; }

  .stack { display: flex; flex-direction: column; align-items: center; gap: 34px; }
  .empty { color: #a1a1aa; text-align: center; padding: 60px; font-size: 14px; }
</style></head><body class="budget">
<header>
  <h1>Resume Preview</h1>
  <select id="file"></select>
  <button id="budget" class="on">Budget colours</button>
  <button id="pages" class="on">Page breaks</button>
  <div class="stats" id="stats"></div>
</header>
<main><div class="stack" id="stage"><div class="empty">Loading…</div></div></main>
<script>
const PAGE_CONTENT_PX = %PAGEPX%;
const ALL = '__all__';
let current = null, lastStamp = null;

const ACRONYMS = new Set(['ai','ml','sde','swe','api','ux','ui','pm','sre','llm','nlp',
                          'genai','mlops','devops','qa','hr','it','phd','ms','msc','bi']);
const labelOf = p => !p.startsWith('targets/') ? p
  : p.split('/')[1].split('-')
      .map(w => ACRONYMS.has(w.toLowerCase()) ? w.toUpperCase() : w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ');

async function listFiles() {
  const g = await (await fetch('/api/files')).json();
  const sel = document.getElementById('file');
  let html = '';
  if (g.resumes.length) {
    html += `<option value="${ALL}">All resumes (${g.resumes.length})</option>`;
    html += '<optgroup label="Resumes">' +
      g.resumes.map(f => `<option value="${f}">${labelOf(f)}</option>`).join('') + '</optgroup>';
  }
  html += '<optgroup label="Reference — not resumes">' +
    g.reference.map(f => `<option value="${f}">${f}</option>`).join('') + '</optgroup>';
  sel.innerHTML = html;

  const valid = [ALL, ...g.resumes, ...g.reference];
  const saved = localStorage.getItem('rs-file');
  // Default to a real resume, never to the master.
  sel.value = (saved && valid.includes(saved)) ? saved
            : (g.resumes.length ? g.resumes[0] : g.reference[0]);
  current = sel.value;
  sel.onchange = () => {
    current = sel.value; localStorage.setItem('rs-file', current);
    lastStamp = null; poll();
  };
}

function buildCard(html, isResume, label, path) {
  const wrap = document.createElement('div');
  if (label) {
    const cap = document.createElement('div');
    cap.className = 'caption';
    cap.innerHTML = `<span>${label}</span><span class="path">${path}</span><span class="chips"></span>`;
    wrap.appendChild(cap);
  }
  const card = document.createElement('div');
  card.className = 'sheet card' + (isResume ? '' : ' reference');
  card.innerHTML =
    `<div class="refbanner"><b>Reference document, not a resume.</b>
       This file is a working document. It is never submitted anywhere and has no page limit,
       so it is shown in plain document styling. Pick a resume from the dropdown to see real layout.</div>
     <div class="doc">${html}</div>`;
  wrap.appendChild(card);
  return wrap;
}

function drawBreaks(card) {
  card.querySelectorAll('.pagebreak').forEach(e => e.remove());
  if (card.classList.contains('reference')) return { pages: 1, fill: 100 };
  const doc = card.querySelector('.doc');
  const top = doc.offsetTop;
  const total = doc.scrollHeight;
  let page = 1;
  for (let y = PAGE_CONTENT_PX; y < total; y += PAGE_CONTENT_PX) {
    page++;
    const el = document.createElement('div');
    el.className = 'pagebreak';
    el.style.top = (top + y) + 'px';
    el.innerHTML = `<span>page ${page}</span>`;
    card.appendChild(el);
  }
  return { pages: Math.max(1, Math.ceil(total / PAGE_CONTENT_PX)),
           fill: Math.round((total % PAGE_CONTENT_PX || PAGE_CONTENT_PX) / PAGE_CONTENT_PX * 100) };
}

const budgetLine = s =>
  `<span><b>${s.bullets}</b> bullets · <b>${s.lines}</b> lines · <b>${s.skills}</b> skill lines</span>
   <span><i class="dot" style="background:var(--ok)"></i><b>${s.ok}</b> ok</span>
   <span><i class="dot" style="background:var(--short)"></i><b>${s.short}</b> short</span>
   <span><i class="dot" style="background:var(--warn)"></i><b>${s.warn}</b> tight</span>
   <span><i class="dot" style="background:var(--over)"></i><b>${s.over}</b> over</span>`;

async function renderAll() {
  const r = await fetch('/api/all');
  const d = await r.json();
  if (d.stamp === lastStamp) return;
  lastStamp = d.stamp;
  const stage = document.getElementById('stage');
  stage.innerHTML = '';
  let totalOver = 0;
  d.docs.forEach(doc => {
    const wrap = buildCard(doc.html, true, doc.label, doc.path);
    stage.appendChild(wrap);
    const g = drawBreaks(wrap.querySelector('.card'));
    const s = doc.stats;
    totalOver += s.over;
    const chips = wrap.querySelector('.chips');
    chips.innerHTML =
      `<span class="chip">${g.pages} page${g.pages > 1 ? 's' : ''}</span>
       <span class="chip">${g.fill}% fill</span>
       <span class="chip">${s.bullets} bullets</span>
       ${s.over ? `<span class="chip bad">${s.over} over limit</span>` : ''}
       ${s.warn ? `<span class="chip mid">${s.warn} tight</span>` : ''}`;
  });
  document.getElementById('stats').innerHTML =
    `<span><b>${d.docs.length}</b> resumes</span>` +
    (totalOver ? `<span><i class="dot" style="background:var(--over)"></i><b>${totalOver}</b> bullets over limit</span>`
               : `<span><i class="dot" style="background:var(--ok)"></i>all bullets within budget</span>`);
}

async function renderOne() {
  const r = await fetch(`/api/content?f=${encodeURIComponent(current)}`);
  if (!r.ok) return;
  const d = await r.json();
  if (d.stamp === lastStamp) return;
  lastStamp = d.stamp;
  const stage = document.getElementById('stage');
  stage.innerHTML = '';
  const wrap = buildCard(d.html, d.resume_mode, null, null);
  stage.appendChild(wrap);
  const g = drawBreaks(wrap.querySelector('.card'));
  document.getElementById('stats').innerHTML = d.resume_mode
    ? `<span><b>${g.pages}</b> page${g.pages > 1 ? 's' : ''}</span>
       <span>last page <b>${g.fill}%</b> full</span>` + budgetLine(d.stats)
    : `<span>reference document — not a resume</span>`;
}

const poll = () => (current === ALL ? renderAll() : renderOne()).catch(() => {});

document.getElementById('budget').onclick = e => {
  document.body.classList.toggle('budget');
  e.target.classList.toggle('on', document.body.classList.contains('budget'));
};
document.getElementById('pages').onclick = e => {
  document.body.classList.toggle('nopages');
  e.target.classList.toggle('on', !document.body.classList.contains('nopages'));
};
listFiles().then(poll);
setInterval(poll, 900);
</script></body></html>
"""

# A4 height minus top and bottom padding, at 96 css px per inch.
PAGE_CONTENT_PX = round((11.69 - 0.5 - 0.2) * 96)


def is_resume(path):
    """A resume is a target draft. Everything else is reference material."""
    p = Path(path)
    return len(p.parts) >= 2 and p.parts[0] == 'targets' and p.name == 'draft.md'


def find_markdown(root):
    """Split markdown into actual resumes and reference documents."""
    skip = {'.git', 'node_modules', '__pycache__', '.venv'}
    resumes, reference = [], []
    for p in sorted(root.rglob('*.md')):
        if any(part in skip for part in p.parts):
            continue
        rel = str(p.relative_to(root))
        (resumes if is_resume(rel) else reference).append(rel)
    # Your own material first, plugin docs last.
    reference.sort(key=lambda s: ('resume-studio/' in s, s))
    return {'resumes': resumes, 'reference': reference}


ACRONYMS = {'ai', 'ml', 'sde', 'swe', 'api', 'ux', 'ui', 'pm', 'sre', 'llm', 'nlp',
            'genai', 'mlops', 'devops', 'qa', 'hr', 'it', 'phd', 'ms', 'msc', 'bi'}


def label_for(path):
    """targets/data-ai-sde/draft.md -> 'Data AI SDE'"""
    if not is_resume(path):
        return path
    words = Path(path).parts[1].split('-')
    return ' '.join(w.upper() if w.lower() in ACRONYMS else w.capitalize() for w in words)


def is_reference_doc(path, text):
    if is_resume(path):
        return False
    name = Path(path).name.lower()
    if name in ('master-resume.md', 'resume-config.md', 'readme.md', 'brief.md', 'review.md'):
        return True
    if 'Source of truth' in text[:400]:
        return True
    return path.startswith('resume-studio/')


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, body, ctype='application/json'):
        data = body.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', f'{ctype}; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs, unquote
        u = urlparse(self.path)
        q = parse_qs(u.query)

        if u.path == '/':
            return self._send(SHELL.replace('%PAGEPX%', str(PAGE_CONTENT_PX)), 'text/html')

        if u.path == '/api/files':
            return self._send(json.dumps(find_markdown(ROOT)))

        if u.path == '/api/all':
            docs, stamp = [], []
            for rel in find_markdown(ROOT)['resumes']:
                path = ROOT / rel
                text = path.read_text(encoding='utf-8', errors='replace')
                stamp.append(str(path.stat().st_mtime_ns))
                docs.append({
                    'path': rel,
                    'label': label_for(rel),
                    'html': md_to_html(text, True),
                    'stats': summarize(text),
                })
            return self._send(json.dumps({'stamp': '-'.join(stamp), 'docs': docs}))

        if u.path == '/api/content':
            rel = unquote(q.get('f', [''])[0])
            target = (ROOT / rel).resolve()
            if not str(target).startswith(str(ROOT.resolve())) or not target.is_file():
                self.send_error(404)
                return
            text = target.read_text(encoding='utf-8', errors='replace')
            forced = q.get('mode', [None])[0]
            if forced:
                resume_mode = forced == 'resume'
            else:
                resume_mode = not is_reference_doc(rel, text)
            return self._send(json.dumps({
                'stamp': f'{target.stat().st_mtime_ns}-{resume_mode}',
                'html': md_to_html(text, resume_mode),
                'stats': summarize(text),
                'resume_mode': resume_mode,
            }))

        self.send_error(404)


def main():
    global ROOT
    ap = argparse.ArgumentParser(description='Live resume preview server')
    ap.add_argument('--dir', default='.', help='directory to scan for markdown (default: cwd)')
    ap.add_argument('--port', type=int, default=8000)
    ap.add_argument('--no-open', action='store_true')
    args = ap.parse_args()

    ROOT = Path(args.dir).resolve()
    if not ROOT.is_dir():
        raise SystemExit(f'Not a directory: {ROOT}')

    groups = find_markdown(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', args.port), Handler) as srv:
        url = f'http://localhost:{args.port}'
        print(f'Resume preview  ->  {url}')
        print(f'Watching {ROOT}')
        print(f'  {len(groups["resumes"])} resume(s), {len(groups["reference"])} reference document(s)')
        for r in groups['resumes']:
            print(f'    - {label_for(r)}')
        print('Edit any file and the page refreshes within a second. Ctrl-C to stop.')
        if not args.no_open:
            threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print('\nStopped.')


if __name__ == '__main__':
    main()
