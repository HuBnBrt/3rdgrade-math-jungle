#!/usr/bin/env python3
"""Build and version a game.

  python3 tools/release.py build     engine + game files -> src.html -> updatever.html (test page, with nikud)
  python3 tools/release.py dev       next test version: 2.0 -> 2.1 -> 2.2 ... (after a publish: next whole number, e.g. 3.0), then build
  python3 tools/release.py publish   test page -> index.html (what the parents open), new service-worker cache name,
                                     records the published version. "release_notes" in game.json must be filled first
                                     (shown once to returning users after they update).

Add --game games/<folder> to work on another game (default games/math3-jungle).
Versions live in games/<folder>/game.json -> "version". APP_VERSION keeps the old 'vNN' form, because copies
already installed look for exactly that text to know an update exists.
"""
import json, os, re, subprocess, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
gdir = args[args.index('--game') + 1] if '--game' in args else 'games/math3-jungle'
gf = os.path.join(root, gdir, 'game.json')
G = json.load(open(gf, encoding='utf-8'))
V = G['version']


def rd(name):
    return open(os.path.join(root, name), encoding='utf-8').read()


def wr(name, text):
    open(os.path.join(root, name), 'w', encoding='utf-8').write(text)


def save_game():
    json.dump(G, open(gf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def build():
    for step in (['build_game.py', gdir], ['build_nikud.py']):
        if subprocess.run([sys.executable, os.path.join(root, 'tools', step[0])] + step[1:]).returncode:
            sys.exit('stopped: ' + step[0] + ' failed (for nikud: add the missing phrases to tools/nikud-map.json)')


cmd = args[0] if args else ''
if cmd == 'build':
    build()
elif cmd == 'dev':
    major, minor = (int(x) for x in V['label'].split('.'))
    pmajor = int(V['published'].split('.')[0])
    label = f'{major + 1}.0' if major == pmajor else f'{major}.{minor + 1}'
    if label.endswith('.0'):
        G['release_notes'] = []  # first test version after a publish: start a fresh what's-new list
    V['build'] += 1
    V['label'] = label
    save_game()
    build()
    print(f'test version {label} (build v{V["build"]})')
elif cmd == 'publish':
    if not G.get('release_notes'):
        sys.exit('fill "release_notes" in game.json first')
    build()
    wr('index.html', rd('updatever.html').replace('<meta name="robots" content="noindex">', '', 1))
    wr('sw.js', re.sub(r"jungle-v\d+", f"jungle-v{V['build']}", rd('sw.js')))
    V['published'] = V['label']
    V['publishedBuild'] = V['build']
    save_game()
    print(f'published {V["label"]} (build v{V["build"]}) to index.html')
else:
    print(__doc__)
