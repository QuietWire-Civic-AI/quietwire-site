#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, tarfile
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'; RELEASES=ROOT/'releases'; RELEASES.mkdir(exist_ok=True)
subprocess.run(['python3',str(ROOT/'scripts/build.py')],check=True)
subprocess.run(['python3',str(ROOT/'scripts/check.py')],check=True)
files=[]
for p in sorted(x for x in DIST.rglob('*') if x.is_file()):
    files.append({'path':str(p.relative_to(DIST)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
try: commit=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip()
except Exception: commit='uncommitted'
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
manifest={'schema':'quietwire.site-release.v1','created_at':stamp,'source_commit':commit,'files':files}
manifest_bytes=(json.dumps(manifest,indent=2)+'\n').encode()
release_id=hashlib.sha256(manifest_bytes).hexdigest()
manifest['release_id']='sha256:'+release_id
manifest_path=RELEASES/f'{release_id}.manifest.json'; manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
archive=RELEASES/f'quietwire-site-{release_id}.tar.gz'
with tarfile.open(archive,'w:gz') as tf:
    tf.add(DIST,arcname='public'); tf.add(manifest_path,arcname='manifest.json')
print(archive)
print('release_id: sha256:'+release_id)
