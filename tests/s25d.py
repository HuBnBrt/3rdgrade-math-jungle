exec(open('/tmp/t/s25.py').read().split("from playwright.sync_api import sync_playwright")[0])
exec(open('/tmp/t/fonts.py').read())
from playwright.sync_api import sync_playwright
J="""(()=>{const n=document.querySelector('.nav')||document.querySelector('nav');const r=n?n.getBoundingClientRect():null;const m=document.querySelector('main');const c=document.querySelector('.cats .card').getBoundingClientRect();return [r?Math.round(r.top):null,r?Math.round(r.bottom):null,innerHeight,document.documentElement.scrollHeight,m.scrollHeight-m.clientHeight,Math.round(c.height)]})()"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w in [360,384,412]:
      for h in range(640,900,20):
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=2.8)
        def route(r):
            u=r.request.url
            if font_route(r): return
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(400); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300); pg.evaluate("__Set(false)"); pg.evaluate("__R2()"); pg.wait_for_timeout(250)
        r=pg.evaluate(J)
        if r[1] is None or r[1]>h+1 or r[3]>h+1 or r[4]>1: print('BAD',w,h,r); pg.screenshot(path=f'bad_{w}_{h}.png')
        pg.close()
    print('done'); b.close()
