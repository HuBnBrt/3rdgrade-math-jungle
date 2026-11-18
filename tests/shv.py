from playwright.sync_api import sync_playwright
from PIL import Image
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Show=id=>{session={kind:'base',only:null,total:8,done:0,correct:0,coins:0,sheet:[id],topics:[SHEET.find(x=>x.id===id).cat]};nextQ();};")
ids=['s5','s16','s25','s30','s33','s34','s79','s83','s48','s72']
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for (w,h) in [(390,780),(1280,720)]:
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        ims=[]
        for i in ids:
            pg.evaluate(f"__Show('{i}')"); pg.wait_for_timeout(150)
            ov=pg.evaluate("(()=>{const q=document.querySelector('#qcard'),m=document.querySelector('main');return [q.scrollHeight-q.clientHeight,Math.round(q.getBoundingClientRect().bottom-m.getBoundingClientRect().bottom),[...document.querySelectorAll('#qcard .opt')].filter(o=>o.scrollWidth>o.clientWidth+1).length]})()")
            print(w,i,ov)
            pg.screenshot(path=f'/tmp/t/v_{w}_{i}.png'); ims.append(Image.open(f'/tmp/t/v_{w}_{i}.png'))
        print(errs)
        W=ims[0].width; c=Image.new('RGB',(W*5,ims[0].height*2),'white')
        for k,im in enumerate(ims): c.paste(im,((k%5)*W,(k//5)*ims[0].height))
        c.save(f'/tmp/t/vc_{w}.png')
    b.close()
