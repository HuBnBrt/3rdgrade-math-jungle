from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__St=o=>{S.stats=o};")
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
    pg.evaluate("__St({mult:{ok:9,bad:1,h:''},digit:{ok:10,bad:0,h:''},seq:{ok:1,bad:6,h:''},column:{ok:2,bad:5,h:''}})")
    for i in range(6):
        pg.evaluate("__S('base')"); t=pg.evaluate("__D()[0].topics"); print(len(t),len(set(t)),[x for x in t if x in('mult','digit','seq','column')])
    print(errs)
