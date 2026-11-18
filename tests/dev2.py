from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Show=id=>{session={kind:'base',only:null,total:8,done:0,correct:0,coins:0,sheet:[id,'s13'],topics:['decomp','decomp']};nextQ();};window.__G=()=>[S.coins,S.owner||null];window.__Add=(g,c)=>addProgress(g,c);")

import re
prod=html
dev=open('/home/claude/g4-jungle-math/updatever.html').read()
for k in ['window.__D=()=>[session,Q];']: pass
from playwright.sync_api import sync_playwright
def mk(body,reqs):
    def route(r):
        u=r.request.url
        if u.startswith('http://x/') and 'fresh' in u: reqs.append(u.split('?')[0]); r.fulfill(body=body,content_type='text/html')
        elif u.startswith('http://x/') and not u.endswith('.png') and not u.endswith('.js'): r.fulfill(body=body,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    return route
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for url,body,pre in [('http://x/updatever.html',dev,None),('http://x/',prod,'v95'),('http://x/',prod,None),('http://x/',prod,'v96')]:
        ctx=b.new_context(viewport={'width':1280,'height':720}); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); reqs=[]
        pg.route('**/*',mk(body,reqs))
        if pre: pg.add_init_script(f"localStorage.setItem('jungle-seen-version','{pre}')")
        pg.goto(url); pg.wait_for_timeout(4200)
        print(url, pre, 'chip:', pg.evaluate("document.querySelector('.dev-chip')?.textContent||''"), 'modal:', pg.evaluate("document.querySelector('.modal')?.innerText.replace(/\\n/g,' | ')||''")[:140], reqs, errs)
        if pre=='v95': pg.screenshot(path='/tmp/t/whatsnew.png')
        ctx.close()
    b.close()
