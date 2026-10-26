from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(P/'archive/scalar_candidate113.zip') as z:
    assert sha((P/'archive/scalar_candidate113.zip').read_bytes())=='5d7c6bf0ebd4ac8cca2a1a6fe6959456e5b80939ae37b442db3f12949dcd494a'
    assert z.testzip() is None
    manifest=json.loads(z.read('manifest.json'))
    for name in z.namelist():
        assert z.read(name)==(P/'reproduce'/name).read_bytes(),name
m=json.loads((P/'release_manifest.json').read_text())
for x in m['files']:
    data=(P/x['path']).read_bytes()
    assert len(data)==x['bytes'] and sha(data)==x['sha256'],x['path']
r=subprocess.run([sys.executable,'-I',str(P/'reproduce/audit.py')],check=True,capture_output=True,text=True)
a=json.loads(r.stdout);e=json.loads((P/'reproduce/expected_results.json').read_text())
assert a==e,'expected JSON differs'
assert a['paper_rounding_checks']=='passed'
print('PASS: file hashes, paper rounding checks, and exact expected JSON')
