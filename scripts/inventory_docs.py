#!/usr/bin/env python3
'''Read-only inventory of documentation-like files. Python standard library only.

From documentation-governance; unchanged behavior.
'''
from pathlib import Path
import argparse, csv, re, sys

DEFAULT_EXTS = {'.md', '.mdx', '.rst', '.txt', '.adoc'}
DEFAULT_SKIP = {'.git', 'node_modules', '.venv', 'venv', 'dist', 'build', '.cache'}

def title_for(path: Path) -> str:
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return ''
    for line in text.splitlines()[:80]:
        m = re.match(r'^\s{0,3}#\s+(.+?)\s*#*\s*$', line)
        if m:
            return m.group(1).strip()
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.M)
    return m.group(1).strip() if m else ''

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', nargs='?', default='.', help='directory to scan (default: current directory)')
    ap.add_argument('--out', help='CSV output path; omit to print CSV to stdout')
    ap.add_argument('--include', default=','.join(sorted(DEFAULT_EXTS)), help='comma-separated extensions')
    ap.add_argument('--exclude-dir', action='append', default=[], help='directory name to exclude (repeatable)')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f'error: not a directory: {root}', file=sys.stderr); return 2
    exts = {x.strip().lower() if x.strip().startswith('.') else '.' + x.strip().lower() for x in args.include.split(',') if x.strip()}
    skip = DEFAULT_SKIP | set(args.exclude_dir)
    rows = []
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        rel = p.relative_to(root)
        if any(part in skip for part in rel.parts):
            continue
        try:
            size = p.stat().st_size
        except OSError:
            size = -1
        rows.append({'path': rel.as_posix(), 'extension': p.suffix.lower(), 'bytes': size, 'title': title_for(p)})
    fields = ['path', 'extension', 'bytes', 'title']
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('w', newline='', encoding='utf-8-sig') as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
        print(f'Inventoried {len(rows)} files -> {out}')
    else:
        w = csv.DictWriter(sys.stdout, fieldnames=fields); w.writeheader(); w.writerows(rows)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
