import sys
from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
S=[(1511,932),(390,780),(844,390),(800,1180),(1280,720)]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for (w,h) in S:
        pg=b.new_page(viewport={'width':w,'height':h})
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(600)
        r=pg.evaluate("""(()=>{const cs=[...document.querySelectorAll('.cats .card')];const ts=[...document.querySelectorAll('.topic-title')];
         const m=document.querySelector('main');
         const bad=cs.filter(c=>{const t=c.querySelector('.topic-content');return t.scrollHeight>t.clientHeight+1||c.scrollWidth>c.clientWidth+1}).length;
         const broken=ts.filter(t=>t.scrollWidth>t.clientWidth+1||t.firstElementChild.getBoundingClientRect().top<t.closest('.card').getBoundingClientRect().top).length+([...document.querySelectorAll('main>section')].filter(x=>x.offsetHeight>0).length-1)*100;
         const ct=cs[0].getBoundingClientRect(); const hb=document.querySelector('.hero-board').getBoundingClientRect();
         const last=cs[cs.length-1].getBoundingClientRect();
         return {fs:getComputedStyle(ts[0]).fontSize,bad,broken,card:[Math.round(ct.width),Math.round(ct.height)],hero:Math.round(hb.height),lastBottom:Math.round(last.bottom),mainOv:m.scrollHeight-m.clientHeight}})()""")
        print(w,h,r)
        pg.screenshot(path=f'/tmp/t/s_{w}x{h}.png')
