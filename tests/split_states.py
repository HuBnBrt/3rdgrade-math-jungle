exec(open('/tmp/sk/real.py').read().split("cases=")[0])
J2="""(()=>{const c=document.querySelector('#qcard');const g=s=>{const e=c.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]};return {cls:c.className,board:g('.question-board'),fb:g('.fbslot'),act:g('.qactions'),ans:g('.parts'),ov:c.scrollHeight>c.clientHeight+2}})()"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for W,H,touch in [(1280,800,True),(1024,768,True)]:
        ctx=b.new_context(viewport={'width':W,'height':H},has_touch=touch,is_mobile=touch); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if font_route(r): return
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(800); pg.evaluate("document.querySelectorAll('.modal-back').forEach(e=>e.remove())")
        pg.evaluate("__Q('column',Q=>Q.body.includes('במאונך'))"); pg.wait_for_timeout(300)
        a=pg.evaluate(J2)
        if pg.query_selector('#hintBtn'): pg.click('#hintBtn'); pg.wait_for_timeout(300)
        h=pg.evaluate(J2); pg.screenshot(path=f'st_hint_{W}_{touch}.png')
        if touch: pg.click('[data-k="1"]')
        else: pg.fill('#qcard input.num','1')
        pg.click('#checkBtn'); pg.wait_for_timeout(500); f=pg.evaluate(J2); pg.screenshot(path=f'st_fb_{W}_{touch}.png')
        print(W,H,touch,a['cls'],'\n  q',a,'\n  h',h,'\n  f',f,errs[:1]); ctx.close()
    b.close()
