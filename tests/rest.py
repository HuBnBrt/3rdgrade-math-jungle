from playwright.sync_api import sync_playwright
from PIL import Image
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Fill=()=>{S.coins=40;GEAR.slice(0,9).forEach(g=>S.gear[g.id]=true);ITEMS.slice(0,4).forEach(i=>S.items[i.id]=1);mast('mult').trophy=true;save()};")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for (w,h) in [(1500,930),(390,780),(844,390)]:
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        pg.evaluate("__Fill()")
        pg.evaluate("document.querySelector('[data-go=camp]').click()"); pg.wait_for_timeout(300)
        print(w,'camp',pg.evaluate("(()=>{const m=document.querySelector('main');return [m.scrollHeight-m.clientHeight,[...document.querySelectorAll('.shop .card')].filter(c=>c.scrollHeight>c.clientHeight+1||c.scrollWidth>c.clientWidth+1).length]})()"))
        pg.screenshot(path=f'/tmp/t/r_{w}_camp.png')
        pg.evaluate("document.querySelector('[data-go=settings]').click()"); pg.wait_for_timeout(300); pg.screenshot(path=f'/tmp/t/r_{w}_set.png')
        pg.evaluate("__S('base')"); pg.evaluate("__D()[0].correct=7;__D()[0].coins=7;__D()[0].trophies=['לוח הכפל']"); pg.evaluate("__E()"); pg.wait_for_timeout(300)
        print(w,'sum',pg.evaluate("(()=>{const q=document.querySelector('#qcard'),m=document.querySelector('main');return [q.scrollHeight-q.clientHeight,Math.round(q.getBoundingClientRect().bottom-m.getBoundingClientRect().bottom)]})()"),errs)
        pg.screenshot(path=f'/tmp/t/r_{w}_sum.png')
    b.close()
for k in ['camp','set','sum']:
    ims=[Image.open(f'/tmp/t/r_{w}_{k}.png') for w in (1500,390,844)]
    c=Image.new('RGB',(1500+390+10,930+400),'white'); c.paste(ims[0],(0,0)); c.paste(ims[1],(1510,0)); c.paste(ims[2],(0,935)); c.save(f'/tmp/t/c_{k}.png')
