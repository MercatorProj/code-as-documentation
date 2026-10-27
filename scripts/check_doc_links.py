#!/usr/bin/env python3
'''Check local Markdown links (inline and reference-style) and heading anchors.

Merge of the link checkers from document-governance-skills and
documentation-governance: fence-aware scanning, anchor validation,
reference-style links, --ignore filters, and directory-to-index resolution.
No network calls; read-only.
'''
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import re
import sys

EXCLUDED = {'.git', 'node_modules', 'dist', 'build', '.venv', 'venv', '__pycache__', '.next', 'coverage'}
LINK_RE = re.compile(r'(?<!!)\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+["\'][^)]*["\'])?\)')
REF_RE = re.compile(r'^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))', re.M)
HEADING_RE = re.compile(r'^#{1,6}\s+(.+?)\s*#*\s*$')
INDEX_NAMES = ('index.md', 'README.md')


def slugify(text):
    text = re.sub(r'[`*_~]', '', text).strip().lower()
    text = re.sub(r'[^\w\-\s]', '', text, flags=re.UNICODE)
    return re.sub(r'\s+', '-', text).strip('-')


def collect_markdown(root):
    for path in root.rglob('*.md'):
        if any(part in EXCLUDED for part in path.parts):
            continue
        yield path


def anchors_for(path):
    anchors = set()
    counts = {}
    try:
        lines = path.read_text(encoding='utf-8-sig').splitlines()
    except (OSError, UnicodeError):
        return anchors
    for line in lines:
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = slugify(m.group(1))
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f'{base}-{count}')
    return anchors


def target_exists(target):
    if target.exists():
        return True
    if target.is_dir() and any((target / n).exists() for n in INDEX_NAMES):
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='.', help='Repository root (default: current directory)')
    parser.add_argument('--ignore', action='append', default=[], help='Substring to ignore in link targets (repeatable)')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f'ERROR: root is not a directory: {root}', file=sys.stderr)
        return 2
    files = list(collect_markdown(root))
    anchor_cache = {}
    issues = []
    checked = 0
    for source in files:
        try:
            text = source.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeError) as exc:
            issues.append((source, 0, f'cannot read Markdown file: {exc}'))
            continue
        raw_targets = []
        in_fence = False
        for line_no, line in enumerate(text.splitlines(), 1):
            if re.match(r'^\s*(```|~~~)', line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_RE.finditer(line):
                raw_targets.append((line_no, match.group(1) or match.group(2) or ''))
        for match in REF_RE.finditer(text):
            raw_targets.append((0, (match.group(1) or match.group(2) or '').strip('<>')))
        for line_no, raw in raw_targets:
            if not raw or raw.startswith(('#', 'mailto:', 'tel:', 'data:')):
                continue
            if any(sub in raw for sub in args.ignore):
                continue
            parts = urlsplit(raw)
            if parts.scheme or parts.netloc:
                continue
            checked += 1
            target_text = unquote(parts.path)
            if not target_text:
                continue  # anchor-only link
            target = (source.parent / target_text).resolve() if not target_text.startswith('/') else (root / target_text.lstrip('/')).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                issues.append((source, line_no, f'link points outside repository root: {raw}'))
                continue
            if not target_exists(target):
                issues.append((source, line_no, f'missing link target: {raw}'))
                continue
            real = target
            if real.is_dir():
                real = next((target / n) for n in INDEX_NAMES if (target / n).exists())
            if parts.fragment and real.is_file() and real.suffix.lower() in {'.md', '.markdown'}:
                if real not in anchor_cache:
                    anchor_cache[real] = anchors_for(real)
                frag = unquote(parts.fragment).lower()
                if frag not in anchor_cache[real]:
                    issues.append((source, line_no, f'heading anchor not found: {raw}'))
    print(f'Checked {len(files)} Markdown files; examined {checked} local links.')
    if issues:
        for path, line_no, message in issues:
            try:
                display = path.relative_to(root).as_posix()
            except ValueError:
                display = str(path)
            print(f'{display}:{line_no}: {message}')
        print(f'Found {len(issues)} issue(s).')
        return 1
    print('No broken local Markdown link targets detected.')
    print('Note: best-effort static check; does not validate Vue imports, VitePress aliases, or all public-root semantics.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
