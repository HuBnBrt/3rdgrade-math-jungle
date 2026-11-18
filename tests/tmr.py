from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Show=id=>{session={kind:'base',only:null,total:8,done:0,correct:0,coins:0,sheet:[id,'s13'],topics:['decomp','decomp']};nextQ();};window.__G=()=>[S.coins,S.owner||null];window.__T=()=>{S.settings.timer='gentle'};window.__Add=(g,c)=>addProgress(g,c);")
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w,h in [(1280,720),(390,780),(844,390)]:
        pg=b.new_page(viewport={'width':w,'height':h})
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(400)
        pg.evaluate('__T()'); pg.evaluate("__Show('s12')"); pg.wait_for_timeout(300)
        r=lambda: pg.evaluate("[...document.querySelectorAll('#qcard .qhead > *')].map(e=>{const b=e.getBoundingClientRect();return [e.className,Math.round(b.left),Math.round(b.top),Math.round(b.width)]})")
        a=r(); pg.screenshot(path=f'tmr_{w}.png'); pg.fill('#qcard input','20'); pg.keyboard.press('Enter'); pg.wait_for_timeout(200); print(w,a,r())
    b.close()
