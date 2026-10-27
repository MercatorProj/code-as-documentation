#!/usr/bin/env python3
'''Validate basic structure and source paths in a simple YAML-like governance map.

Intentionally avoids a YAML dependency and supports only a conservative subset.
From documentation-governance; unchanged behavior.
'''
from pathlib import Path
import argparse, re, sys

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('config', nargs='?', default='.governance/docs.yml')
    ap.add_argument('--root', default='.', help='project root')
    args = ap.parse_args()
    cfg = Path(args.config)
    root = Path(args.root).resolve()
    if not cfg.is_file():
        print(f'error: config not found: {cfg}', file=sys.stderr); return 2
    text = cfg.read_text(encoding='utf-8', errors='replace')
    if not text.strip():
        print('error: configuration is empty'); return 1
    paths = []
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r'^\s*(?:doc_root|source|document|path|config|output)\s*:\s*["\']?([^\s"\'#]+)', line)
        if m:
            value = m.group(1)
            if value.startswith(('http://', 'https://', '${')):
                continue
            paths.append((i, value))
        m2 = re.match(r'^\s*-\s*(?:source|document|path)\s*:\s*["\']?([^\s"\'#]+)', line)
        if m2:
            paths.append((i, m2.group(1)))
    issues = []
    for line, value in paths:
        if any(ch in value for ch in '*?['):
            continue
        p = (root / value).resolve()
        if not p.exists():
            issues.append((line, value))
    for line, value in issues:
        print(f'{cfg}:{line}: path does not exist relative to {root}: {value}')
    print(f'Checked {len(paths)} path-like entry/entries; {len(issues)} missing path(s).')
    print('This is a conservative path check, not full YAML schema validation.')
    return 1 if issues else 0

if __name__ == '__main__':
    raise SystemExit(main())
