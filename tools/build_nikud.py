#!/usr/bin/env python3
"""Build updatever.html (the vocalized test version) from src.html (the plain source we edit).
Publishing to everyone (index.html) is done by tools/release.py publish using tools/nikud-map.json.
Prints any Hebrew phrase that has no vocalized form yet (it is left unvocalized)."""
import json, re, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(root, 'tools', 'nikud-map.json'), encoding='utf-8'))
s = open(os.path.join(root, 'src.html'), encoding='utf-8').read()
i = s.index('<body>')
pat = re.compile(r"[א-ת][א-ת׳״]*(?:(?:[ ,\-]|\.\s|:\s|\?\s|!\s|\s-\s)+[א-ת][א-ת׳״]*)*[.?!]?")
missing = []
def sub(m):
    t = m.group(0)
    if t in M: return M[t]
    if t not in missing: missing.append(t)
    return t
# regions between /*NIKUD-OFF*/ and /*NIKUD-ON*/ hold words used for matching typed answers: keep them plain
body = s[i:]
chunks = re.split(r'(/\*NIKUD-OFF\*/.*?/\*NIKUD-ON\*/)', body, flags=re.S)
out = s[:i] + ''.join(c if c.startswith('/*NIKUD-OFF*/') else pat.sub(sub, c) for c in chunks)
# vowel marks need room and a font that draws them correctly
out = out.replace("\n</style>", """
/* nikud version: room for vowel marks */
.cats .card .topic-title,.cats .card .topic-title.wrap{line-height:1.3 !important}
#qcard .prompt{line-height:1.7}
.feedback .fb-text{line-height:1.45}
@media (max-height:480px){#qcard .prompt{line-height:1.3}.feedback .fb-text{line-height:1.25}}
</style>""", 1)
out = out.replace("getBoundingClientRect().height > size * 2.5", "getBoundingClientRect().height > size * 2.9")
a, b = out.index('<style>'), out.index('</style>')
css = re.sub(r"\b(Rubik|Heebo)\b", "'Noto Sans Hebrew'", out[a:b])
out = out[:a] + css + out[b:]
out = out.replace("family=Heebo:wght@400;600;800&family=Rubik:wght@700;900", "family=Noto+Sans+Hebrew:wght@400;600;700;800;900", 1)
out = out.replace("Rubik,sans-serif", "'Noto Sans Hebrew',sans-serif").replace("Heebo,sans-serif", "'Noto Sans Hebrew',sans-serif")
open(os.path.join(root, 'updatever.html'), 'w', encoding='utf-8').write(out)
print('updatever.html rebuilt.', 'Missing:' if missing else 'All phrases vocalized.')
for t in missing: print('  ', t)
sys.exit(1 if missing else 0)
