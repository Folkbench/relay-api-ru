# SPDX-License-Identifier: MIT
"""Offline editorial integrity checks. No keys, paid APIs or network access."""
from pathlib import Path
import json,re
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
KIND='providers'
data=json.loads((ROOT/('data/'+KIND+'.json')).read_text())
items=data[KIND]
assert data['timezone']=='Asia/Shanghai'
assert len({x['id'] for x in items})==len(items)
sources=json.loads((ROOT/'sources.json').read_text())
assert sources and all(s['checked_at'] and s['timezone']=='Asia/Shanghai' for s in sources)
for s in sources:
 assert s['resource_id'] in {x['id'] for x in items}
 assert urlsplit(s['url']).scheme=='https' and not urlsplit(s['url']).username
for r in items:
 assert re.fullmatch(r'[a-z0-9-]+',r['id']) and r['checked_at']
 assert any(s['resource_id']==r['id'] for s in sources)
if KIND=='providers':
 import struct
 icon=(ROOT/'docs/favicon.ico').read_bytes()
 assert struct.unpack_from('<HHH',icon)==(0,1,1) and icon[6:8]==bytes([32,32])
 assert len(icon)>1000
 from build import outputs
 assert len(items)==7 and len({r['group'] for r in items})==6
 assert data['official_database_sync'] is False
 for path,wanted in outputs().items():
  assert (ROOT/path).read_text()==wanted, 'Пересоберите: '+path
 for r in items:
  assert r['protocols_documented'] and set(r['protocols_documented'])<=set(['chat','messages','responses','gemini'])
  assert r['currency'] in ['RUB','USD']
  assert r['monitoring']=='Не выполнялось'
  for k in ['website','documentation','pricing_url']:
   assert any(s['resource_id']==r['id'] and s['url']==r[k] for s in sources)
else:
 assert len(items)==6
 assert [r['section'] for r in items].count('cloud')==1
 md=(ROOT/'RESOURCES.md').read_text()
 for r in items:
  for k in ['purpose','allowance','period','rate','region','card','license','limitations','testing']:
   assert r[k] and r[k] in md,(r['id'],k)
  assert 'id="'+r['id']+'"' in md
  assert all(any(s['resource_id']==r['id'] and s['url']==u for s in sources) for u in r['sources'])
# Relative Markdown links must resolve inside this repository. External URLs are editorially reviewed separately.
for p in ROOT.rglob('*.md'):
 if '.git' in p.parts:continue
 text=p.read_text()
 if p.name!='maintenance.zh-CN.md':assert not re.search(r'[\u4e00-\u9fff]',text),str(p)
 for link in re.findall(r'\]\(([^)]+)\)',text):
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  if not u.path:continue
  target=(p.parent/unquote(u.path)).resolve()
  assert target.is_relative_to(ROOT) and target.exists(),(str(p),link)
# Content-only scans, deliberately excluding checks themselves and git internals.
for p in ROOT.rglob('*'):
 if not p.is_file() or '.git' in p.parts or p.suffix in {'.py','.ico'} or '__pycache__' in p.parts:continue
 t=p.read_text()
 for pattern in [r'gh[pousr]_[A-Za-z0-9]{20,}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'sk-(?:proj-)?[A-Za-z0-9]{30,}']:
  assert not re.search(pattern,t),'Возможный секрет: '+str(p)
 assert not any(bad in t.lower() for bad in ['modelflare','castaly','hollymoon']),str(p)
print('OK: JSON, ссылки, источники, границы, языки, отсутствие типовых секретов; записей:',len(items))
