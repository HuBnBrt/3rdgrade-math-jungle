#!/usr/bin/env python3
"""One-off: split src.html into the shared engine and the math/jungle game files.

engine/engine.html            everything that is the same for every game
games/math3-jungle/game.json  names, texts and keys of this game (tokens {{NAME}} in the engine)
games/math3-jungle/head.html  page head: credit comment, share preview, title
games/math3-jungle/theme.js   shop animals, chest items, rarity names
games/math3-jungle/content.js topics, question generators, the teacher's sheet exercises

tools/build_game.py puts them back together; the result must equal src.html byte for byte.
"""
import json, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(root, 'src.html'), encoding='utf-8').read()
game = os.path.join(root, 'games', 'math3-jungle')
os.makedirs(game, exist_ok=True)
os.makedirs(os.path.join(root, 'engine'), exist_ok=True)


def cut(text, start, end_incl, token):
    """replace text[start .. end of end_incl] with token, return (new text, removed part)"""
    i = text.index(start)
    j = text.index(end_incl, i) + len(end_incl)
    return text[:i] + token + text[j:], text[i:j]


eng = src
# 1. page head (credit comment .. title line)
eng, head = cut(eng, '<!--\n', '<meta name="robots" content="noindex">', '{{@HEAD}}')
# 2. theme lists
eng, theme = cut(eng, 'const ITEMS = [', "const RARITY = ['רגיל', 'נדיר', 'אגדי'];", '/*{{@THEME}}*/')
# 3. content: generators .. sheet
eng, content = cut(eng, '/* ---------- question generators ---------- */',
                   'function sheetDraw(target) { angDrawBag = [target]; return genAngleDraw(); }', '/*{{@CONTENT}}*/')

# 4. texts and keys
tokens = {
    'GAME_TITLE': "הג'ונגל של המתמטיקה",
    'WELCOME': "ברוכים הבאים לג\\'ונגל!",
    'MASCOT': '🐵',
    'CAMP_ICON': '🏕️',
    'CAMP_NAV': 'המחנה',
    'CAMP_TITLE': 'חנות המחנה',
    'EMPTY_SHELF': 'סיום אימונים פותח תיבות עם ציוד הישרדות!',
    'HEADER_ICON': '🌴',
    'STORAGE_KEY': 'jungle-math-v4',
    'OLD_STORAGE_KEY': 'jungle-math-v3',
    'LS_PREFIX': 'jungle-',
    'UPDATE_IMG': 'monkey-update.png',
}
order = ['GAME_TITLE', 'WELCOME', 'CAMP_TITLE', 'CAMP_NAV', 'EMPTY_SHELF', 'STORAGE_KEY', 'OLD_STORAGE_KEY', 'UPDATE_IMG']
for k in order:
    v = tokens[k]
    assert v in eng, (k, v)
    eng = eng.replace(v, '{{' + k + '}}')
# emoji tokens only in their exact places
for k, a, b in [('MASCOT', "        🐵 ${user ? 'שלום '", "        {{MASCOT}} ${user ? 'שלום '"),
                ('CAMP_ICON', '<span class="e">🏕️</span>{{CAMP_NAV}}', '<span class="e">{{CAMP_ICON}}</span>{{CAMP_NAV}}'),
                ('CAMP_ICON', '<h2 class="camp-title">🏕️ {{CAMP_TITLE}}', '<h2 class="camp-title">{{CAMP_ICON}} {{CAMP_TITLE}}'),
                ('LS_PREFIX', "localStorage.getItem('jungle-install-no')", "localStorage.getItem('{{LS_PREFIX}}install-no')"),
                ('LS_PREFIX', "last = localStorage.getItem('jungle-seen-version'); localStorage.setItem('jungle-seen-version'", "last = localStorage.getItem('{{LS_PREFIX}}seen-version'); localStorage.setItem('{{LS_PREFIX}}seen-version'"),
                ('LS_PREFIX', "localStorage.setItem('jungle-install-no'", "localStorage.setItem('{{LS_PREFIX}}install-no'"),
                ('HEADER_ICON', '-webkit-tap-highlight-color:transparent">🌴</a>', '-webkit-tap-highlight-color:transparent">{{HEADER_ICON}}</a>')]:
    assert eng.count(a) == 1, (k, a)
    eng = eng.replace(a, b)

open(os.path.join(root, 'engine', 'engine.html'), 'w', encoding='utf-8').write(eng)
open(os.path.join(game, 'head.html'), 'w', encoding='utf-8').write(head)
open(os.path.join(game, 'theme.js'), 'w', encoding='utf-8').write(theme)
open(os.path.join(game, 'content.js'), 'w', encoding='utf-8').write(content)
json.dump({'subject': 'math3', 'tokens': tokens}, open(os.path.join(game, 'game.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('engine:', len(eng.splitlines()), 'lines; content:', len(content.splitlines()), 'lines; theme:', len(theme.splitlines()), 'lines')
