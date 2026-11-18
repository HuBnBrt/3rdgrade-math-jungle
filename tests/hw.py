from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__H=v=>hebWordsNum(v);window.__Show=id=>{session={kind:'base',only:null,total:8,done:0,correct:0,coins:0,sheet:[id],topics:[SHEET.find(x=>x.id===id).cat]};nextQ();};")
tests=['שבעה אלפים','שבעת אלפים','7 אלפים','מאה','מאתיים','שלוש מאות וארבעים','חמשת אלפים שבע מאות שמונים וארבע','אלפיים שבע מאות שישים ותשע','שלושה עשר','עשרים ואחת','אלף ומאה','מֵאָה','ארבעה אלפים','שלום','100','תשע מאות תשעים ותשע']
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1468,'height':918}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
    for t in tests: print(t, pg.evaluate(f"__H({t!r})"))
    pg.evaluate("__Show('s13')"); pg.fill('#qcard input','מאה'); pg.click('#checkBtn'); pg.wait_for_timeout(200)
    print(pg.inner_text('.feedback')); pg.screenshot(path='/tmp/t/hw.png'); print(errs)
    b.close()
