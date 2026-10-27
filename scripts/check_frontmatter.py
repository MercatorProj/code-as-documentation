#!/usr/bin/env python3
'''Lightweight frontmatter validator; no YAML dependency required.

From documentation-governance; unchanged behavior.
'''
from pathlib import Path
import argparse, re, sys

ALLOWED = {'draft', 'active', 'needs-review', 'deprecated', 'archived'}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', nargs='?', default='docs')
    ap.add_argument('--require', action='store_true', help='fail when Markdown files lack frontmatter')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f'error: directory not found: {root}', file=sys.stderr); return 2
    files = sorted(set(root.rglob('*.md')) | set(root.rglob('*.mdx')))
    issues = []
    for p in files:
        text = p.read_text(encoding='utf-8', errors='replace')
        rel = p.relative_to(root).as_posix()
        if not text.startswith('---\n'):
            if args.require:
                issues.append((rel, 'missing frontmatter'))
            continue
        end = text.find('\n---', 4)
        if end < 0:
            issues.append((rel, 'frontmatter opening delimiter has no closing delimiter')); continue
        fm = text[4:end]
        title = re.search(r'^title\s*:\s*\S', fm, re.M)
        status = re.search(r'^status\s*:\s*["\']?([\w-]+)', fm, re.M)
        if not title:
            issues.append((rel, 'frontmatter missing non-empty title'))
        if status and status.group(1) not in ALLOWED:
            issues.append((rel, 'unknown status: ' + status.group(1))
        )
    for p, msg in issues:
        print(f'{p}: {msg}')
    print(f'Checked {len(files)} Markdown files; {len(issues)} issue(s).')
    if not args.require:
        print('Legacy files without frontmatter are allowed unless --require is supplied.')
    return 1 if issues else 0

if __name__ == '__main__':
    raise SystemExit(main())
