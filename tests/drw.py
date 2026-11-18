from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Chk=()=>{Q.result=true;Q.earned=1;renderPlay()};")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for (w,h) in [(1468,990),(360,640),(844,390)]:
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        pg.evaluate("__S('base','angledraw')"); pg.wait_for_timeout(200)
        chk="(()=>{const h=document.querySelector('.draw-help'),f=document.querySelector('.fbslot').getBoundingClientRect(),s=document.querySelector('svg[data-draw]').getBoundingClientRect();return [h?Math.round(f.top-h.getBoundingClientRect().bottom):null,Math.round(s.height),Math.round(f.top-s.bottom)]})()"
        print(w,pg.evaluate(chk)); pg.screenshot(path=f'/tmp/t/drw_{w}.png')
        pg.evaluate("__Chk()"); pg.wait_for_timeout(200); print(' after',pg.evaluate(chk),errs)
    b.close()
