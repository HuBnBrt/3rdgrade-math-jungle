from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__C=()=>CATS;window.__R=()=>S.rot;")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for n,(w,h) in {'phone':(390,780),'phoneS':(360,640),'tab':(820,1100),'desk':(1366,650)}.items():
        pg=b.new_page(viewport={'width':w,'height':h})
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/?install=1'); pg.wait_for_timeout(700)
        print(n,pg.evaluate("""[...document.querySelectorAll('.cats .card')].filter(c=>c.scrollHeight>c.clientHeight+1||[...c.querySelectorAll('.topic-title')].some(t=>t.scrollWidth>t.clientWidth+1)).length"""),
          pg.evaluate("document.querySelector('main').scrollHeight-document.querySelector('main').clientHeight"))
        print(' titlepx',pg.evaluate("getComputedStyle(document.querySelector('.topic-title')).fontSize"));pg.screenshot(path=f'/tmp/t/d_{n}.png')
        if n=='phone':
            seen=[]
            for k in range(3):
                pg.evaluate("__S('base')")
                ts=[]
                for i in range(8):
                    ts.append(pg.evaluate("__D()[1].cat")); pg.evaluate("__D()[0].done++; document.querySelector('#nextBtn')?0:0")
                    pg.evaluate("(()=>{})()")
                    pg.evaluate("window.__n&&0")
                    break
                print(' topics',pg.evaluate("__D()[0].topics"))
                seen+=pg.evaluate("__D()[0].topics")
                pg.evaluate("__E()")
            print(' unique across 3 sessions',len(set(seen)),'of',pg.evaluate("__C().length"), 'rot left',pg.evaluate("__R()"))
