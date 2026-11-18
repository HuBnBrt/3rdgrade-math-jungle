from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for (w,h) in [(800,1100),(753,1000),(600,900)]:
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        pg.evaluate("document.querySelector('[data-go=settings]').click()"); pg.wait_for_timeout(300)
        r=pg.evaluate("(()=>{const v=document.querySelector('#view-settings');const hs=[...v.querySelectorAll('h2')].map(h=>Math.round(h.getBoundingClientRect().top));const vis=[...document.querySelectorAll('main>section')].filter(x=>x.offsetHeight>0).length;return {scroll:v.scrollHeight-v.clientHeight,h2tops:hs,sections:vis,cards:[...v.querySelectorAll('.card')].filter(c=>c.scrollHeight>c.clientHeight+1).length}})()")
        print(w,h,r,errs); pg.screenshot(path=f'/tmp/t/st_{w}x{h}.png')
        pg.evaluate("document.querySelector('[data-go=home]').click()"); pg.wait_for_timeout(200)
        print('  home sections',pg.evaluate("[...document.querySelectorAll('main>section')].filter(x=>x.offsetHeight>0).length"))
    b.close()
