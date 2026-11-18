#!/usr/bin/env python3
"""Versions of the app.

  python3 tools/release.py dev       next test version: 2.0 -> 2.1 -> 2.2 ... (after a publish: next major, e.g. 3.0)
                                     updates src.html and rebuilds updatever.html (the test page)
  python3 tools/release.py publish   copies the test page to index.html (what the parents open),
                                     refreshes the service-worker cache name and records the published version.
                                     RELEASE_NOTES in src.html must be filled first (shown once after updating).

State lives in tools/version.json. APP_VERSION keeps the old 'vNN' build form, because copies already
installed look for exactly that text to know an update exists.
"""
import json, os, re, subprocess, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vf = os.path.join(root, 'tools', 'version.json')
V = json.load(open(vf, encoding='utf-8'))


def rd(name):
    return open(os.path.join(root, name), encoding='utf-8').read()


def wr(name, text):
    open(os.path.join(root, name), 'w', encoding='utf-8').write(text)


def set_src(build, label):
    s = rd('src.html')
    s, a = re.subn(r"const APP_VERSION = 'v\d+';", f"const APP_VERSION = 'v{build}';", s)
    s, b = re.subn(r"const APP_LABEL = '[\d.]+';", f"const APP_LABEL = '{label}';", s)
    assert a == 1 and b == 1, 'version lines not found in src.html'
    wr('src.html', s)


def build():
    r = subprocess.run([sys.executable, os.path.join(root, 'tools', 'build_nikud.py')])
    if r.returncode:
        sys.exit('nikud build reported missing phrases - add them to tools/nikud-map.json')


cmd = sys.argv[1] if len(sys.argv) > 1 else ''
if cmd == 'dev':
    major, minor = (int(x) for x in V['label'].split('.'))
    pmajor = int(V['published'].split('.')[0])
    label = f'{major + 1}.0' if major == pmajor else f'{major}.{minor + 1}'
    V['build'] += 1
    if label.endswith('.0'):  # first test version after a publish: start a fresh what's-new list
        wr('src.html', re.sub(r'const RELEASE_NOTES = \[.*?\];', 'const RELEASE_NOTES = [];', rd('src.html'), flags=re.S))
    V['label'] = label
    set_src(V['build'], label)
    build()
    json.dump(V, open(vf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'test version {label} (build v{V["build"]})')
elif cmd == 'publish':
    s = rd('src.html')
    notes = re.search(r'const RELEASE_NOTES = \[(.*?)\];', s, re.S)
    if not notes or not notes.group(1).strip():
        sys.exit('fill RELEASE_NOTES in src.html first')
    build()
    page = rd('updatever.html').replace('<meta name="robots" content="noindex">', '', 1)
    wr('index.html', page)
    sw = re.sub(r"jungle-v\d+", f"jungle-v{V['build']}", rd('sw.js'))
    wr('sw.js', sw)
    V['published'] = V['label']
    V['publishedBuild'] = V['build']
    json.dump(V, open(vf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'published {V["label"]} (build v{V["build"]}) to index.html')
else:
    print(__doc__)
