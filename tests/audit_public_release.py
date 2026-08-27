"""Fail closed if the public repository contains private data or author-controlled files."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
forbidden_suffixes = {'.dta', '.xlsx', '.xls', '.parquet', '.feather', '.sav', '.rds', '.pkl', '.pickle', '.zip'}
forbidden_dirs = {'raw', 'derived', 'private', 'paper', 'submission'}
forbidden_name_tokens = ('.env', 'credential', 'secret', 'token', 'id_rsa')
violations = []

for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts:
        continue
    relative = path.relative_to(ROOT)
    if path.suffix.lower() in forbidden_suffixes:
        violations.append(f'forbidden data/archive suffix: {relative}')
    if any(part.lower() in forbidden_dirs for part in relative.parts):
        violations.append(f'forbidden private directory: {relative}')
    if any(token in path.name.lower() for token in forbidden_name_tokens):
        violations.append(f'forbidden sensitive filename: {relative}')
    if path.suffix.lower() == '.csv':
        header = path.read_text(encoding='utf-8', errors='ignore').splitlines()[:1]
        if header and re.search(r'(^|,)(firm_id|stockcode|股票代码)(,|$)', header[0], flags=re.I):
            violations.append(f'row-level identifier in public CSV header: {relative}')
    if path.suffix.lower() in {'.md', '.txt', '.py', '.yml', '.yaml', '.json'}:
        text = path.read_text(encoding='utf-8', errors='ignore')
        if re.search(r'gh[puo]_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}', text):
            violations.append(f'potential credential value: {relative}')

if violations:
    raise SystemExit('PUBLIC RELEASE AUDIT FAILED:\n' + '\n'.join(f'- {v}' for v in violations))
print('PASS: public release audit found no raw archives, row-level IDs, private manuscript files, or token-like credentials.')
