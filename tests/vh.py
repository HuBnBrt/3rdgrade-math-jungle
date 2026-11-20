exec(open('/tmp/t/s25.py').read().split("from playwright.sync_api import sync_playwright")[0])
from playwright.sync_api import sync_playwright
NB="(()=>{const n=document.querySelector('.nav').getBoundingClientRect();return [Math.round(n.bottom),innerHeight,getComputedStyle(document.documentElement).getPropertyValue('--app-h')]})()"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':384,'height':740},device_scale_factor=2.8)
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(600)
    print('start',pg.evaluate(NB))
    pg.evaluate("document.documentElement.style.setProperty('--app-h','800px')"); print('broken',pg.evaluate(NB))
    pg.evaluate("dispatchEvent(new Event('resize'))"); pg.wait_for_timeout(100); print('after resize event',pg.evaluate(NB))
    pg.set_viewport_size({'width':384,'height':690}); pg.wait_for_timeout(300); print('shorter',pg.evaluate(NB))
    pg.set_viewport_size({'width':740,'height':384}); pg.wait_for_timeout(300); print('rotated',pg.evaluate(NB))
    b.close()
