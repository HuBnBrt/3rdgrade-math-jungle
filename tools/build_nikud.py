#!/usr/bin/env python3
"""Rebuild nikud.html from index.html using tools/nikud-map.json.
Prints any Hebrew phrase that has no vocalized form yet (it is left unvocalized)."""
import json, re, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(root, 'tools', 'nikud-map.json'), encoding='utf-8'))
s = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
i = s.index('<body>')
pat = re.compile(r"[א-ת][א-ת׳״]*(?:(?:[ ,\-]|\.\s|:\s|\?\s|!\s|\s-\s)+[א-ת][א-ת׳״]*)*[.?!]?")
missing = []
def sub(m):
    t = m.group(0)
    if t in M: return M[t]
    if t not in missing: missing.append(t)
    return t
out = s[:i] + pat.sub(sub, s[i:])
# vowel marks need room and a font that draws them correctly
out = out.replace("\n</style>", """
/* nikud version: room for vowel marks */
.cats .card .topic-title,.cats .card .topic-title.wrap{line-height:1.3 !important}
#qcard .prompt{line-height:1.7}
.feedback .fb-text{line-height:1.45}
</style>""", 1)
out = out.replace("<title>ארץ הג'ונגל במתמטיקה</title>", "<title>ארץ הג'ונגל במתמטיקה (מנוקד)</title><meta name=\"robots\" content=\"noindex\">", 1)
out = out.replace("getBoundingClientRect().height > size * 2.5", "getBoundingClientRect().height > size * 2.9")
a, b = out.index('<style>'), out.index('</style>')
css = re.sub(r"\b(Rubik|Heebo)\b", "'Noto Sans Hebrew'", out[a:b])
out = out[:a] + css + out[b:]
out = out.replace("family=Heebo:wght@400;600;800&family=Rubik:wght@700;900", "family=Noto+Sans+Hebrew:wght@400;600;700;800;900", 1)
out = out.replace("Rubik,sans-serif", "'Noto Sans Hebrew',sans-serif").replace("Heebo,sans-serif", "'Noto Sans Hebrew',sans-serif")
open(os.path.join(root, 'nikud.html'), 'w', encoding='utf-8').write(out)
print('nikud.html rebuilt.', 'Missing:' if missing else 'All phrases vocalized.')
for t in missing: print('  ', t)
sys.exit(1 if missing else 0)
