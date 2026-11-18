from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__G=()=>S.gear;window.__X=()=>{S.coins=40;save()};")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':780})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(600)
    pg.evaluate("__S('base')"); pg.evaluate("__D()[0].correct=8"); pg.evaluate("__E()")
    pg.wait_for_timeout(200); pg.screenshot(path='/tmp/t/end.png')
    for i in range(3): pg.evaluate("__S('base')"); pg.evaluate("__D()[0].correct=5"); pg.evaluate("__E()")
    print(pg.evaluate("Object.keys(__G()).length"))
    pg.evaluate("__X()"); pg.click('[data-go=camp]'); pg.wait_for_timeout(300)
    pg.click('[data-buy=lion]'); pg.wait_for_timeout(200)
    pg.screenshot(path='/tmp/t/camp.png'); print(errs)
