from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Show=id=>{session={kind:'base',only:null,total:8,done:0,correct:0,coins:0,sheet:[id],topics:['order']};nextQ();};")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for hasTouch in [False,True]:
        ctx=b.new_context(viewport={'width':1280,'height':720} if not hasTouch else {'width':390,'height':780},has_touch=hasTouch)
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        pg.evaluate("__Show('s24')"); pg.wait_for_timeout(200)
        v=lambda: pg.evaluate("__D()[1].parts[0].v")
        def center(sel,i):
            bb=pg.locator(sel).nth(i).bounding_box(); return bb['x']+bb['width']/2, bb['y']+bb['height']/2
        def dragm(a,bpt):
            pg.mouse.move(*a); pg.mouse.down(); pg.mouse.move(a[0]+20,a[1]+20,steps=3); pg.mouse.move(*bpt,steps=8); pg.mouse.up(); pg.wait_for_timeout(120)
        # tap bank item 0 -> slot 0
        pg.locator('.opts.ord .opt').nth(0).click(); pg.wait_for_timeout(100); print('tap',v())
        # drag bank item 1 to slot 3
        dragm(center('.opts.ord .opt',1),center('.seq span',3)); print('drag to slot3',v())
        # drag slot0 to slot5 (swap with empty)
        dragm(center('.seq span',0),center('.seq span',5)); print('slot0->5',v())
        # drag bank item2 onto occupied slot3 -> replace
        dragm(center('.opts.ord .opt',2),center('.seq span',3)); print('replace slot3',v())
        # tap filled slot5 -> back to bank
        pg.locator('.seq span').nth(5).click(); pg.wait_for_timeout(100); print('tap slot5',v())
        # drag slot3 to bank
        dragm(center('.seq span',3),center('.opts.ord .opt',0)); print('slot3->bank',v(), errs)
        pg.screenshot(path=f'/tmp/t/drag_{hasTouch}.png')
    b.close()
