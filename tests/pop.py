from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Rec=ok=>record(ok);window.__Up=()=>{pendingUpdate='99';maybePrompts()};")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':780}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u.endswith('monkey-update.png'): r.fulfill(body=open('/home/claude/g4-jungle-math/monkey-update.png','rb').read(),content_type='image/png')
        elif 'fresh=' in u: r.fulfill(body="const APP_VERSION = 'v1';",content_type='text/html')
        elif u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/?install=1'); pg.wait_for_timeout(4500)
    print('install modal:',pg.locator('.modal h2').all_inner_texts())
    pg.screenshot(path='/tmp/t/m1.png')
    pg.click('[data-m=no]'); pg.wait_for_timeout(200)
    pg.evaluate("__Up()"); pg.wait_for_timeout(500); pg.screenshot(path='/tmp/t/upd.png'); print('update modal:',pg.locator('.modal h2').all_inner_texts()); pg.click('[data-m=no]')
    pg.click('[data-go=settings]'); pg.wait_for_timeout(300)
    pg.fill('#nickInput','עדיר'); pg.click('[data-gender=m]'); pg.click('[data-go=home]'); pg.wait_for_timeout(300)
    print(pg.inner_text('.hero-bubble')[:30])
    pg.click('[data-go=settings]'); pg.screenshot(path='/tmp/t/m2.png',full_page=True)
    pg.evaluate("__S('base','compare')")
    for i in range(3): pg.evaluate("__D()[1].cat='compare'; __Rec(true)")
    print(pg.inner_text('#toast'),errs)
