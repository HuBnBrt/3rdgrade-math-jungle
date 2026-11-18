from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__SH=()=>SHEET.map(x=>{const q=x.make();return x.id+' '+x.cat+' | '+q.parts.map(p=>p.type+':'+(p.ans!==undefined?JSON.stringify(p.ans):(p.check?('chk '+[3700,201,5748,5487,2796,2976].filter(v=>p.check(v)).join('/')):'?'))).join(' ; ')});window.__Rec=ok=>record(ok);window.__LS=()=>sheetLeft().length;")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':780}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(600)
    for l in pg.evaluate("__SH()"): print(l)
    print('home:',pg.inner_text('.hero-bubble'))
    pg.click('#startBtn'); pg.wait_for_timeout(200)
    print(pg.evaluate("[__D()[0].topics.join(','),__D()[0].sheet.join(',')]"))
    seen=[]
    for i in range(8):
        seen.append(pg.evaluate("__D()[1].sheetId+':'+__D()[1].cat")); pg.screenshot(path=f'/tmp/t/sh{i}.png'); pg.evaluate("__Rec(true)"); pg.evaluate("__D()[0].done<8 && document.querySelector('[data-go]') ; 0")
        pg.evaluate("nextQ && 0") if False else None
        pg.evaluate("(()=>{})()")
        if i<7: pg.evaluate("window.__N && __N()")
    print(seen,'left',pg.evaluate("__LS()"),errs)
    b.close()
