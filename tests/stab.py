from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Show=id=>{session={kind:'base',only:null,total:8,done:0,correct:0,coins:0,sheet:[id],topics:[SHEET.find(x=>x.id===id).cat]};nextQ();};window.__Ans=()=>{Q.parts.forEach(p=>{if(p.type==='order')p.v=[...p.ans];else if(p.type==='text')p.v='3700';else if(p.type!=='draw')p.v=p.ans});check()};")
ids=['s1','s6','s12','s16','s17','s19','s24','s26','s27','s33','s34','s35','s48','s57','s64','s71','s76','s84']
J="(()=>{const r=e=>{const b=e.getBoundingClientRect();return [Math.round(b.top),Math.round(b.height),Math.round(b.left),Math.round(b.width)]};return [...document.querySelectorAll('#qcard .question-board, #qcard .parts, #qcard input, #qcard .opt, #qcard svg, #qcard .seq')].map(r)})()"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for (w,h) in [(1468,918),(390,780),(844,390),(800,1180)]:
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        bad=[]
        for i in ids:
            pg.evaluate(f"__Show('{i}')"); pg.wait_for_timeout(120); a=pg.evaluate(J)
            pg.evaluate("__Ans()"); pg.wait_for_timeout(150); c=pg.evaluate(J)
            mx=max([max(abs(x-y) for x,y in zip(u,v)) for u,v in zip(a,c)]+[0])
            ov=pg.evaluate("document.querySelector('#qcard').scrollHeight-document.querySelector('#qcard').clientHeight")
            if mx>2 or len(a)!=len(c) or ov>0: bad.append((i,mx,len(a),len(c),ov))
        print(w,h,bad,errs)
    b.close()
