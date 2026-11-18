from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Fill=()=>{GEAR.slice(0,9).forEach(g=>S.gear[g.id]=true);ITEMS.slice(0,4).forEach(i=>S.items[i.id]=1);save()};")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1500,'height':930}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
    pg.evaluate("__Fill()"); pg.evaluate("document.querySelector('[data-go=camp]').click()"); pg.wait_for_timeout(1000)
    print(pg.evaluate("[...document.querySelectorAll('.collection-shelf .owned-animal')].map(e=>Math.round(e.getBoundingClientRect().top))"), errs)
    pg.locator('.collection-shelf').screenshot(path='/tmp/t/wave.png')
    b.close()
