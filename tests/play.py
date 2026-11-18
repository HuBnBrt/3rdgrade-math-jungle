from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Chk=()=>{Q.parts.forEach(p=>{p.v=p.type==='draw'?undefined:p.ans});Q.result=false;renderPlay()};")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for (w,h) in [(1485,990),(390,780),(844,390),(820,1100)]:
        pg=b.new_page(viewport={'width':w,'height':h})
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        for cat in ['angleid','nocalc','column','order']:
            pg.evaluate(f"__S('base','{cat}')"); pg.wait_for_timeout(150)
            if cat in('angleid','nocalc'): pg.evaluate("__Chk()"); pg.wait_for_timeout(150)
            ov=pg.evaluate("(()=>{const q=document.querySelector('#qcard'),m=document.querySelector('main');const f=document.querySelector('.feedback');return [q.scrollHeight-q.clientHeight, q.getBoundingClientRect().bottom-m.getBoundingClientRect().bottom, f?f.scrollHeight-f.clientHeight:0]})()")
            print(w,h,cat,ov)
            pg.screenshot(path=f'/tmp/t/p_{w}_{cat}.png')
