from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for (w,h) in [(1485,830),(360,640)]:
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        pg.evaluate("__S('base','order')"); pg.wait_for_timeout(200)
        pos=lambda: pg.evaluate("[...document.querySelectorAll('.opts.ord .opt')].map(e=>Math.round(e.getBoundingClientRect().left))")
        a=pos(); pg.locator('.opts.ord .opt').nth(2).click(); pg.locator('.opts.ord .opt').nth(0).click(); pg.wait_for_timeout(200)
        print(w, a==pos(), pg.evaluate("[...document.querySelectorAll('.opts.ord .opt,.seq span')].filter(e=>e.scrollWidth>e.clientWidth+1).length"), errs)
        pg.screenshot(path=f'/tmp/t/ord_{w}.png')
    b.close()
