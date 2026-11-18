from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__F=t=>{teacherFocus=t;renderHome()};window.__GF=()=>teacherFocus;window.__Rec=ok=>record(ok);")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':360,'height':780}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
    pg.evaluate("__F('angleid')"); pg.wait_for_timeout(200); pg.screenshot(path='/tmp/t/rec.png')
    pg.click('[data-practice=angleid]')
    for i in range(8): pg.evaluate("__D()[1].cat='angleid';__Rec(true)")
    pg.evaluate("__E()"); print('focus after:',pg.evaluate("__GF()"),errs)
    print(pg.inner_text('.qhead') if pg.locator('.qhead').count() else 'summary')
