from playwright.sync_api import sync_playwright
exec(open('/tmp/t/shot.py').read().split('sizes=')[0].split('import sys, re')[1].replace('from playwright.sync_api import sync_playwright',''))
html=html.replace("function nextQ() {","window.__S=(k,o)=>startSession(k,o);\nfunction nextQ() {",1)
ids=['column','numline','compare','equation','words','word','mult','moreless']
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for name,(w,h) in {'phone':(390,760),'desk':(1366,650)}.items():
        pg=b.new_page(viewport={'width':w,'height':h})
        def route(r):
            u=r.request.url
            if u=='http://x/': r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'/tmp/t/n_home_{name}.png')
        print(name,'main overflow',pg.evaluate("document.querySelector('main').scrollHeight-document.querySelector('main').clientHeight"))
        for i in ids:
            pg.evaluate(f"__S('base','{i}')"); pg.wait_for_timeout(150)
            pg.screenshot(path=f'/tmp/t/n_{i}_{name}.png')
            print(name,i,pg.evaluate("(()=>{const c=document.querySelector('#qcard');return [c.scrollHeight,c.clientHeight]})()"))
        pg.close()
