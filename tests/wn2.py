from playwright.sync_api import sync_playwright
exec(open('/tmp/t/shot.py').read().split('sizes=')[0].split('import sys, re')[1].replace('from playwright.sync_api import sync_playwright',''))
html=open('/home/claude/g4-jungle-math/index.html',encoding='utf-8').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for seen in ['v107','v110','v111']:
        ctx=b.new_context(viewport={'width':390,'height':780}); pg=ctx.new_page()
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/')
        pg.evaluate(f"""(()=>{{for(let i=0;i<localStorage.length;i++){{}};const k=Object.keys(localStorage);localStorage.setItem('jungle-seen-version','{seen}');}})()""")
        keys=pg.evaluate("Object.keys(localStorage)")
        pg.reload(); pg.wait_for_timeout(4200)
        print(seen, keys, pg.evaluate("document.querySelector('.modal h2')?.textContent||'none'"))
        ctx.close()
    b.close()
