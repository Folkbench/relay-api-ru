#!/usr/bin/env python3
"""Fail if editorial checks reintroduce a station-name word ban."""
from pathlib import Path
import re, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
check = (ROOT / 'scripts' / 'check.py').read_text()
# A list of names used as a rejection set is the forbidden pattern.
if re.search(r"for bad in \['modelflare','castaly','hollymoon'\]", check):
    sys.exit('scripts/check.py still rejects content that merely contains station/product names')
# Fixture must remain in the tree so CI fails if the ban is restored.
fx = ROOT / 'tests' / 'fixtures' / 'station-names-allowed.md'
text = fx.read_text()
for name in ('Modelflare', 'Castaly', 'Hollymoon'):
    if name not in text:
        sys.exit(f'{fx} must mention {name}')
subprocess.check_call([sys.executable, str(ROOT / 'scripts' / 'check.py')])
print('OK: station names allowed; scripts/check.py passed')
