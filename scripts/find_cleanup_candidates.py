#!/usr/bin/env python3
'''Find documentation cleanup candidates. Read-only; standard library only.

Categories:
  orphan     no inbound Markdown link and not an entry point (README/index)
  stub       empty or near-empty page
  dead-ref   backtick source-path reference that does not exist on disk
             (evidence that documented code was deleted or moved)
  duplicate  identical or near-identical normalized bodies
  plan-word  plan/proposal wording that may read as shipped behavior
  temp       temporary/working docs: backup artifacts, dated or draft-named files,
             drafts without a review date, drafts past their review age

Static candidates require human review; a finding is not a verdict.
Exit 0 unless --strict and any candidate is found.
'''
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import hashlib
import re
import sys
from datetime import date, datetime

EXCLUDED = {'.git', 'node_modules', 'dist', 'build', '.venv', 'venv', '__pycache__', '.next', 'coverage', '.governance'}
DOC_EXTS = {'.md', '.mdx'}
LINK_RE = re.compile(r'(?<!!)\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))[^)]*\)')
REF_RE = re.compile(r'^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))', re.M)
CODE_REF_RE = re.compile(r'`([\w][\w.\\/-]*\.(?:py|ts|tsx|js|jsx|mjs|java|go|rs|cs|rb|php|c|h|cpp|hpp|sql|toml|json|yml|yaml))`')
MENTION_RE = re.compile(r'`([\w][\w.\\/-]*\.(?:md|mdx))`')
FENCE_RE = re.compile(r'^\s*(```|~~~)')
PLAN_RE = re.compile(r'\b(coming soon|will be (?:added|supported|implemented|released)|planned feature|not yet (?:available|implemented|supported))\b', re.I)
TEMP_NAME_RE = re.compile(r'(?:^|[-_. ])(?:tmp|temp|draft|wip|scratch|bak|copy)(?:[-_. ]|$)', re.I)
BACKUP_RE = re.compile(r'(~\$|\.bak$|\.orig$|\.tmp$)')
DATE_NOTE_RE = re.compile(r'(?:^|[-_. ])\d{4}[-_]?\d{2}[-_]?\d{2}(?:[-_.]|$)')
FM_STATUS_RE = re.compile(r'^status\s*:\s*["\']?([\w-]+)', re.M)
FM_REVIEWED_RE = re.compile(r'^last_reviewed\s*:\s*["\']?(\d{4}[-/]\d{2}[-/]\d{2})', re.M)
STUB_MIN_CHARS = 200
STUB_MIN_LINES = 3


def collect_docs(root, extra_skip):
    skip = EXCLUDED | set(extra_skip)
    docs = []
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.suffix.lower() not in DOC_EXTS:
            continue
        rel = p.relative_to(root)
        if any(part in skip for part in rel.parts):
            continue
        docs.append(p)
    return docs


def read_text(p):
    try:
        return p.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError):
        return None


def strip_fences(text):
    out = []
    fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            fence = not fence
            continue
        if not fence:
            out.append(line)
    return '\n'.join(out)


def local_targets(root, src, text):
    targets = []
    for m in LINK_RE.finditer(text):
        targets.append(m.group(1) or m.group(2) or '')
    for m in REF_RE.finditer(text):
        targets.append((m.group(1) or m.group(2) or '').strip('<>'))
    resolved = set()
    for raw in targets:
        if not raw or raw.startswith(('#', 'mailto:', 'tel:', 'data:')):
            continue
        parts = urlsplit(raw)
        if parts.scheme or parts.netloc:
            continue
        t = unquote(parts.path)
        if not t:
            continue
        cand = (src.parent / t).resolve() if not t.startswith('/') else (root / t.lstrip('/')).resolve()
        if cand.suffix.lower() in DOC_EXTS and cand.is_file():
            try:
                cand.relative_to(root)
            except ValueError:
                continue
            resolved.add(cand)
    return resolved




def mentions(root, src, text):
    '''Resolve backtick-mentioned relative .md/.mdx paths (nav tables, tree lists).'''
    found = set()
    for m in MENTION_RE.finditer(strip_fences(text)):
        t = unquote(m.group(1).replace('\\', '/'))
        cand = (src.parent / t).resolve() if not t.startswith('/') else (root / t.lstrip('/')).resolve()
        if not cand.is_file() and not t.startswith('/'):
            cand = (root / t).resolve()  # root-relative mention, common in nav tables
        try:
            cand.relative_to(root)
        except ValueError:
            continue
        if cand.is_file():
            found.add(cand)
    return found


def parse_frontmatter(text):
    '''Extract status and last_reviewed from simple frontmatter, if present.'''
    fm = {}
    if not text.startswith('---\n'):
        return fm
    end = text.find('\n---', 4)
    if end < 0:
        return fm
    block = text[4:end]
    m = FM_STATUS_RE.search(block)
    if m:
        fm['status'] = m.group(1)
    m = FM_REVIEWED_RE.search(block)
    if m:
        fm['last_reviewed'] = m.group(1)
    return fm


def normalized_body(text):
    body = strip_fences(text)
    body = re.sub(r'^#{1,6}\s+.*$', '', body, flags=re.M)  # drop headings
    body = re.sub(r'\s+', ' ', body).strip().lower()
    return body


def entry_points(root, docs):
    entries = set()
    for p in docs:
        rel = p.relative_to(root)
        if len(rel.parts) <= 2 and p.name.lower() in {'readme.md', 'index.md', 'skill.md'}:
            entries.add(p)
    return entries


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', nargs='?', default='.', help='Repository root (default: current directory)')
    ap.add_argument('--exclude-dir', action='append', default=[], help='directory name to exclude (repeatable)')
    ap.add_argument('--out', help='CSV output path; omit to print a report to stdout')
    ap.add_argument('--max-age', type=int, default=90, help='Maximum age in days for draft documents (default: 90)')
    ap.add_argument('--strict', action='store_true', help='Return non-zero when any candidate is found')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f'ERROR: root is not a directory: {root}', file=sys.stderr)
        return 2
    docs = collect_docs(root, args.exclude_dir)
    if not docs:
        print('No Markdown documents found in scope.')
        return 0
    texts = {}
    for p in docs:
        t = read_text(p)
        if t is None:
            texts[p] = ''
        else:
            texts[p] = t
    inbound = {p: 0 for p in docs}
    for p in docs:
        seen = set()
        for tgt in local_targets(root, p, texts[p]) | mentions(root, p, texts[p]):
            if tgt in inbound and tgt != p and tgt not in seen:
                seen.add(tgt)
                inbound[tgt] += 1
    entries = entry_points(root, docs)

    candidates = []  # (category, path, evidence, suggestion)

    # orphans
    for p in docs:
        if p not in entries and inbound[p] == 0:
            candidates.append(('orphan', p, 'no inbound Markdown link and not an entry point',
                               'run the existence test; usually delete or merge'))

    # stubs
    for p in docs:
        body = strip_fences(texts[p])
        meaningful = [ln for ln in body.splitlines() if ln.strip() and not ln.strip().startswith('<!--')]
        if len(meaningful) < STUB_MIN_LINES and len(body.strip()) < STUB_MIN_CHARS:
            candidates.append(('stub', p, f'{len(meaningful)} meaningful lines, {len(body.strip())} chars',
                               'fill with real content or delete; a stub misleads readers'))

    # dead source references
    for p in docs:
        for line_no, line in enumerate(strip_fences(texts[p]).splitlines(), 1):
            for m in CODE_REF_RE.finditer(line):
                ref = m.group(1).replace('\\', '/')
                if '/' not in ref:
                    continue  # bare filenames are too ambiguous to judge
                cand = (root / ref).resolve()
                if not cand.is_file():
                    candidates.append(('dead-ref', p, f'line {line_no}: source path not found: {ref}',
                                       'update the reference, or delete/archive this page if the code is gone'))

    # duplicates
    by_hash = {}
    for p in docs:
        nb = normalized_body(texts[p])
        if nb:
            by_hash.setdefault(hashlib.sha256(nb.encode('utf-8')).hexdigest(), []).append(p)
    for group in by_hash.values():
        if len(group) > 1:
            names = ', '.join(q.relative_to(root).as_posix() for q in group)
            candidates.append(('duplicate', group[0], f'identical normalized body shared by: {names}',
                               'keep one canonical page; merge or delete the rest'))

    # plan wording
    for p in docs:
        for line_no, line in enumerate(strip_fences(texts[p]).splitlines(), 1):
            m = PLAN_RE.search(line)
            if m:
                snippet = line.strip()[:160]
                candidates.append(('plan-word', p, f'line {line_no}: possible plan stated as shipped: {snippet}',
                                   'mark as proposed/planned or move out of the published tree'))


    # temporary and working documents
    today = date.today()
    for p in docs:
        name = p.name.lower()
        reasons = []
        if BACKUP_RE.search(name):
            reasons.append('backup artifact name')
        elif TEMP_NAME_RE.search(name):
            reasons.append('temporary/working name')
        elif DATE_NOTE_RE.search(name):
            reasons.append('date-stamped note name')
        fm = parse_frontmatter(texts[p])
        reviewed = fm.get('last_reviewed')
        if fm.get('status') == 'draft':
            if not reviewed:
                reasons.append('draft status without a last_reviewed date')
            else:
                try:
                    d = datetime.strptime(reviewed.replace('/', '-'), '%Y-%m-%d').date()
                    age = (today - d).days
                    if age > args.max_age:
                        reasons.append(f'draft last reviewed {age} days ago (max age {args.max_age})')
                except ValueError:
                    reasons.append(f'unparseable last_reviewed date: {reviewed}')
        if reasons:
            candidates.append(('temp', p, '; '.join(reasons),
                               'keep only in the agreed scratch location with owner and review date; promote, archive, or delete on expiry'))


    categories = ['orphan', 'stub', 'dead-ref', 'duplicate', 'plan-word', 'temp']
    counts = {c: sum(1 for x in candidates if x[0] == c) for c in categories}
    if args.out:
        import csv
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerow(['category', 'document', 'evidence', 'suggestion'])
            for cat, p, ev, sug in candidates:
                w.writerow([cat, p.relative_to(root).as_posix(), ev, sug])
        print(f'Wrote {len(candidates)} candidate(s) -> {out}')
    else:
        print(f'Scanned {len(docs)} Markdown files; {len(candidates)} candidate(s).')
        for c in categories:
            print(f'  {c}: {counts[c]}')
        for cat, p, ev, sug in candidates:
            print(f'[{cat}] {p.relative_to(root).as_posix()}: {ev}')
            print(f'         suggestion: {sug}')
        print('Static candidates only: every finding requires human review.')
    if args.strict and candidates:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
