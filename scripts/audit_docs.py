#!/usr/bin/env python3
'''Find common documentation hygiene candidates: empty pages, missing headings,
placeholder markers. Static findings require human review.

From document-governance-skills; unchanged behavior.
'''
from pathlib import Path
import argparse
import re
import sys

EXCLUDED = {'.git', 'node_modules', 'dist', 'build', '.venv', 'venv', '__pycache__', '.next', 'coverage'}
PLACEHOLDERS = re.compile(r'\b(TODO|TBD|FIXME|XXX)\b|Lorem ipsum', re.I)
HEADING = re.compile(r'^#{1,6}\s+\S')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='.', help='Repository root (default: current directory)')
    parser.add_argument('--strict', action='store_true', help='Return non-zero when any candidate is found')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f'ERROR: root is not a directory: {root}', file=sys.stderr)
        return 2
    files = [p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in {'.md', '.mdx'} and not any(part in EXCLUDED for part in p.parts)]
    findings = []
    for path in sorted(files):
        try:
            lines = path.read_text(encoding='utf-8-sig').splitlines()
        except (OSError, UnicodeError) as exc:
            findings.append((path, 0, f'cannot read file: {exc}'))
            continue
        meaningful = [line for line in lines if line.strip() and not line.strip().startswith('<!--')]
        if not meaningful:
            findings.append((path, 1, 'empty or whitespace-only documentation file'))
            continue
        if not any(HEADING.match(line) for line in lines) and path.name.lower() not in {'license.md', 'changelog.md'}:
            findings.append((path, 1, 'no Markdown heading found; check whether this page has a clear title'))
        for line_no, line in enumerate(lines, 1):
            if PLACEHOLDERS.search(line):
                findings.append((path, line_no, f'placeholder marker candidate: {line.strip()[:160]}'))
    print(f'Scanned {len(files)} Markdown/MDX files.')
    if findings:
        for path, line_no, message in findings:
            try:
                display = path.relative_to(root).as_posix()
            except ValueError:
                display = str(path)
            print(f'{display}:{line_no}: {message}')
        print(f'Found {len(findings)} candidate(s). Review each finding; a keyword hit is not automatically a defect.')
        return 1 if args.strict else 0
    print('No empty-page, missing-heading, or common-placeholder candidates detected.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
