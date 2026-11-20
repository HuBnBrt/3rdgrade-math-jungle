#!/usr/bin/env python3
"""Build a game's src.html from the shared engine and the game's own files.

  python3 tools/build_game.py games/math3-jungle          writes src.html
  python3 tools/build_game.py games/math3-jungle --check  only checks that src.html is up to date

A game folder holds: game.json (subject id + texts/keys), head.html (page head),
theme.js (shop animals, chest items, rarity names), content.js (topics, generators, teacher's sheet),
theme.css (optional: colors and looks that override the engine's jungle look).
After this, the usual steps apply: tools/build_nikud.py (test page) and tools/release.py.
"""
import json, os, re, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
game = os.path.join(root, args[0]) if args else os.path.join(root, 'games', 'math3-jungle')
rd = lambda p: open(p, encoding='utf-8').read()

g = json.load(open(os.path.join(game, 'game.json'), encoding='utf-8'))
out = rd(os.path.join(root, 'engine', 'engine.html'))
out = out.replace('{{@HEAD}}', rd(os.path.join(game, 'head.html')), 1)
out = out.replace('/*{{@THEME}}*/', rd(os.path.join(game, 'theme.js')), 1)
out = out.replace('/*{{@CONTENT}}*/', rd(os.path.join(game, 'content.js')), 1)
css = rd(os.path.join(game, 'theme.css')) if os.path.exists(os.path.join(game, 'theme.css')) else ''
out = out.replace('\n/*{{@THEME_CSS}}*/', ('\n' + css.rstrip('\n')) if css.strip() else '', 1)
v = g['version']
out = out.replace('{{BUILD}}', 'v%d' % v['build']).replace('{{LABEL}}', v['label'])
out = out.replace('{{NOTES_BUILD}}', str(g.get('notes_build', 0)))
out = out.replace('{{RELEASE_NOTES}}', json.dumps(g.get('release_notes', []), ensure_ascii=False).replace('", "', "', '").replace('["', "['").replace('"]', "']"))
for k, v in g['tokens'].items():
    out = out.replace('{{' + k + '}}', v)
left = sorted(set(re.findall(r'\{\{[A-Z_@]+\}\}', out)))
if left:
    sys.exit('missing values in game.json: ' + ', '.join(left))
target = os.path.join(root, 'src.html')
if '--check' in sys.argv:
    same = os.path.exists(target) and rd(target) == out
    print('src.html is up to date' if same else 'src.html differs from engine + game files')
    sys.exit(0 if same else 1)
open(target, 'w', encoding='utf-8').write(out)
print('src.html built from', os.path.relpath(game, root))
