exec(open('/tmp/t/stab.py').read().split("with sync_playwright")[0])
from playwright.sync_api import sync_playwright
J2="(()=>{const out=[];document.querySelectorAll('#qcard *').forEach((e,i)=>{const b=e.getBoundingClientRect();out.push([e.tagName+'.'+e.className,Math.round(b.top),Math.round(b.height)])});return out})()"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1468,'height':918})
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
    for i in ['s24']:
        pg.evaluate(f"__Show('{i}')"); pg.wait_for_timeout(120); a=pg.evaluate(J2)
        pg.evaluate("__Ans()"); pg.wait_for_timeout(150); c=pg.evaluate(J2)
        print(i,[ (x,y) for x,y in zip(a,c) if abs(x[1]-y[1])>2 or abs(x[2]-y[2])>2][:8], len(a),len(c))
    b.close()
