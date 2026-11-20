exec(open('/tmp/t/nl2.py').read().split("with sync_playwright")[0])
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__R2=()=>{S.resume={base:{kind:'base',total:8,done:3},samedigits:{kind:'topic',total:8,done:5}};renderHome();};",1)
from playwright.sync_api import sync_playwright
J="""(()=>{const out=[];document.querySelectorAll('.cats .card').forEach((c,i)=>{const q=s=>{const e=c.querySelector(s);if(!e||getComputedStyle(e).display==='none')return null;return e.getBoundingClientRect()};const st=q('.stars'),rb=q('.rankbadge'),bar=q('.bar.prog'),bt=q('.practice-btn');const ov=(a,b)=>a&&b&&a.bottom>b.top+0.5;out.push([i,!!rb,ov(st,rb),ov(rb,bar),ov(bar,bt),Math.round(c.getBoundingClientRect().height)])});return out.filter(x=>x[2]||x[3]||x[4]).slice(0,4).concat([['cards',document.querySelectorAll('.cats .card').length,out[0]]])})()"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w,h,d in [(384,740,2.8125),(360,700,3),(412,800,2.625),(390,780,3),(384,860,2.8)]:
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=d)
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500); pg.evaluate("__Set(false)"); pg.evaluate("__R2()"); pg.wait_for_timeout(300)
        print(w,h,pg.evaluate(J)); pg.screenshot(path=f's25_{w}.png'); pg.close()
    b.close()
