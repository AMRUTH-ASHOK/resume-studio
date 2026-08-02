#!/usr/bin/env python3
"""
Count rendered characters in LaTeX resume bullets and skill lines.
Strips LaTeX markup to show what a reader actually sees on the page.

Usage:
  python3 char_count.py "Built \\textbf{Spark} pipelines across 12 teams"
  echo "bullet text" | python3 char_count.py
  python3 char_count.py output/Acme/e2e_acme_resume.tex
  python3 char_count.py --raw "bullet text"              # just the number
"""

import re
import sys
import argparse

# Calibrated against resume.cls at 10pt, textwidth=7.5in.
# See resume_builder/reference/resume_reference.md for the source of these numbers.
BASE_LINE_LIMIT = 119
BOLD_PENALTY = 0.5

# (variant, target_low, target_high, hard_max, orphan_threshold)
TIERS = [
    ('1L', 105, 111, 117, None),
    ('2L', 189, 205, 218, 78),
]


def strip_latex(text):
    """Strip LaTeX markup to get rendered text."""
    # Remove \item[] / \skilldash{ prefixes
    text = re.sub(r'\\item\s*(\[\s*\])?\s*', '', text)
    text = re.sub(r'\\skilldash\{', '', text)
    # \href{url}{text} -> text
    text = re.sub(r'\\href\{[^}]*\}\{([^}]*)\}', r'\1', text)
    # Inline styling -> contents
    for cmd in ('textbf', 'textit', 'underline', 'emph', 'texttt'):
        text = re.sub(r'\\' + cmd + r'\{([^}]*)\}', r'\1', text)
    # Superscripts / subscripts -> contents
    text = re.sub(r'\$\^\{([^}]*)\}\$', r'\1', text)
    text = re.sub(r'\$\^(.)\$', r'\1', text)
    text = re.sub(r'\$_\{([^}]*)\}\$', r'\1', text)
    text = re.sub(r'\$_(.)\$', r'\1', text)
    # \sim -> 1 char (~)
    text = text.replace('$\\sim$', '~')
    text = text.replace('\\sim', '~')
    text = text.replace('\\textasciitilde', '~')
    # $<$ $>$ -> 1 char
    text = re.sub(r'\$([<>])\$', r'\1', text)
    # $\vert$ -> 1 char
    text = re.sub(r'\$\\vert\$', '|', text)
    # --- -> em-dash (1 char but ~2x wide), -- -> en-dash (1 char)
    text = text.replace('---', '\u2014')
    text = text.replace('--', '\u2013')
    # Remaining math delimiters
    text = text.replace('$', '')
    # Remaining \commands
    text = re.sub(r'\\[a-zA-Z]+\s*', '', text)
    # Remaining braces
    text = text.replace('{', '').replace('}', '')
    # Collapse multiple spaces
    text = re.sub(r'  +', ' ', text)
    return text.strip()


def count_bold_chars(text):
    """Count characters inside \\textbf{} commands."""
    return sum(len(m) for m in re.findall(r'\\textbf\{([^}]*)\}', text))


def count_em_dashes(text):
    """Count em-dashes (---) which render ~2x wide."""
    return len(re.findall(r'---', text))


def classify_bullet(char_count, bold_chars):
    """Classify a bullet into a variant and check limits."""
    effective = BASE_LINE_LIMIT - (BOLD_PENALTY * bold_chars)

    for variant, lo, hi, hard_max, orphan in TIERS:
        if char_count <= hard_max:
            if char_count < lo:
                status = 'SHORT'
            elif char_count <= hi:
                status = 'OK'
            else:
                status = 'NEAR MAX'
            return variant, status, lo, hi, hard_max, orphan, effective

    return 'OVER', 'OVER LIMIT', 0, 0, 0, None, effective


def format_one(raw, kind='bullet'):
    """Format the analysis for a single bullet or skill line."""
    rendered = strip_latex(raw)
    n = len(rendered)
    bold = count_bold_chars(raw)
    em = count_em_dashes(raw)

    if kind == 'skill':
        # Skill dashes must fit exactly one rendered line.
        effective = BASE_LINE_LIMIT - (BOLD_PENALTY * bold)
        status = 'OK' if n <= effective else 'OVER LINE'
        parts = [f"  {n:3d} chars | SKILL | {status} (effective limit {effective:.0f})"]
        if bold:
            parts.append(f"  Bold: {bold} chars")
        parts.append(f"  Rendered: {rendered}")
        return '\n'.join(parts), 'skill'

    variant, status, lo, hi, hard_max, orphan, eff = classify_bullet(n, bold)

    parts = [f"  {n:3d} chars | {variant} | {status} (target {lo}-{hi}, max {hard_max})"]
    if bold:
        parts.append(f"  Bold: {bold} chars -> effective limit/line: {eff:.0f}")
    if em:
        parts.append(f"  Em-dashes: {em} (each ~2x wide, budget +{em} extra)")
    parts.append(f"  Rendered: {rendered}")
    return '\n'.join(parts), variant


def extract_items(text):
    """Extract \\item bullets and \\skilldash lines from .tex source."""
    bullets, skills = [], []
    for line in text.split('\n'):
        s = line.strip()
        if s.startswith('%'):
            continue
        if s.startswith('\\item'):
            bullets.append(s)
        elif s.startswith('\\skilldash'):
            skills.append(s)
    return bullets, skills


def report_file(path, raw_mode):
    with open(path) as f:
        bullets, skills = extract_items(f.read())

    if not bullets and not skills:
        print("No \\item or \\skilldash lines found.")
        return

    if raw_mode:
        for item in bullets + skills:
            print(len(strip_latex(item)))
        return

    total_lines = 0
    violations = []

    if bullets:
        print(f"Found {len(bullets)} bullets:\n")
        for i, item in enumerate(bullets, 1):
            report, variant = format_one(item, 'bullet')
            print(f"Bullet {i}:")
            print(report)
            print()
            if variant == 'OVER':
                violations.append(f"Bullet {i}: OVER LIMIT")
            else:
                total_lines += int(variant[0])

    if skills:
        print(f"Found {len(skills)} skill lines:\n")
        for i, item in enumerate(skills, 1):
            report, _ = format_one(item, 'skill')
            print(f"Skill {i}:")
            print(report)
            print()
            if 'OVER LINE' in report:
                violations.append(f"Skill {i}: exceeds one line")

    print(f"Total rendered bullet lines: {total_lines}")
    print(f"Total skill lines: {len(skills)}")
    if violations:
        print("\nVIOLATIONS:")
        for v in violations:
            print(f"  - {v}")
    else:
        print("\nNo violations.")


def main():
    parser = argparse.ArgumentParser(
        description='Count rendered characters in LaTeX resume bullets')
    parser.add_argument('input', nargs='?',
                        help='Bullet text or .tex file path')
    parser.add_argument('--raw', action='store_true',
                        help='Output only char counts (for scripting)')
    args = parser.parse_args()

    if args.input and args.input.endswith('.tex'):
        report_file(args.input, args.raw)
    elif args.input:
        if args.raw:
            print(len(strip_latex(args.input)))
        else:
            report, _ = format_one(args.input)
            print(report)
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if args.raw:
                print(len(strip_latex(line)))
            else:
                report, _ = format_one(line)
                print(report)
                print()


if __name__ == '__main__':
    main()
