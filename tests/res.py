from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Rec=ok=>record(ok);")
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
    pg.click('#startBtn'); 
    for i in range(3): pg.evaluate("__Rec(true)"); pg.evaluate("__S.length")  if False else None
    t1=pg.evaluate("__D()[0].topics"); 
    pg.click('[data-go=home]'); pg.wait_for_timeout(200)
    print(pg.inner_text('#startBtn'))
    pg.click('#startBtn'); pg.wait_for_timeout(200)
    d=pg.evaluate("[__D()[0].done,__D()[0].topics]"); print(d[0], d[1]==t1)
    pg.click('[data-go=home]'); pg.click('[data-practice=mult]'); pg.evaluate("__Rec(true)"); pg.click('[data-go=home]')
    pg.click('[data-practice=mult]'); print(pg.evaluate("__D()[0].done"), errs)
