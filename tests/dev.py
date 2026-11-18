exec(open('/tmp/t/enter.py').read().split("with sync_playwright")[0].replace('updatever.html','index.html'))
html2=html
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for url,body,pre in [('http://x/updatever.html',html,None),('http://x/',html2,'v95'),('http://x/',html2,None),('http://x/',html2,'v96')]:
        ctx=b.new_context(viewport={'width':1280,'height':720}); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); reqs=[]
        def mk(body):
          def route(r):
              u=r.request.url
              if u.startswith('http://x/') and 'fresh' in u: reqs.append(u.split('?')[0]); r.fulfill(body=body,content_type='text/html')
            elif u.startswith('http://x/') and not u.endswith('.png') and not u.endswith('.js'): r.fulfill(body=body,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route)
        if pre: pg.add_init_script(f"localStorage.setItem('jungle-seen-version','{pre}')")
        pg.goto(url); pg.wait_for_timeout(4200)
        print(url, pre, 'chip:', pg.evaluate("document.querySelector('.dev-chip')?.textContent||''"), 'modal:', pg.evaluate("document.querySelector('.modal')?.innerText.replace(/\\n/g,' | ')||''")[:120], reqs, errs)
        if 'updatever' in url: pg.screenshot(path='/tmp/t/dev.png')
        ctx.close()
    b.close()
