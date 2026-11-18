import sys
exec(open('/tmp/t/enter.py').read().split("with sync_playwright")[0])
html=html.replace('window.__D=()=>[session,Q];','window.__D=()=>[session,Q];window.__C=()=>CATS.map(c=>c.id);window.__Gen=(cat,re)=>{for(let k=0;k<300;k++){session={kind:"base",only:cat,total:8,done:0,correct:0,coins:0,topics:[cat]};nextQ();if(new RegExp(re).test(document.querySelector("#qcard .question-board").textContent.replace(/[\\u0591-\\u05c7]/g,"")))return true;}return false;};',1)
from playwright.sync_api import sync_playwright
J="(()=>{const bd=document.querySelector('#qcard .question-board');const q=document.querySelector('#qcard');const els=[...document.querySelectorAll('#qcard .question-board *')];const act=[...document.querySelectorAll('#qcard .qactions button')].map(x=>x.getBoundingClientRect().bottom);const nav=document.querySelector('.nav').getBoundingClientRect().top;const cb=q.getBoundingClientRect().bottom;const clip=els.filter(e=>{const r=e.getBoundingClientRect(),b=bd.getBoundingClientRect();return r.height>0&&(r.top<b.top-1||r.bottom>b.bottom+1)}).length;return {gapNav:Math.round(nav-Math.max(...act)),gapCard:Math.round(cb-Math.max(...act)),bd:[bd.clientHeight,bd.scrollHeight],clip,q:[q.clientHeight,q.scrollHeight],fs:getComputedStyle(bd.querySelector('.prompt')).fontSize}})()"
cases=[('digit','האם המספר החדש'),('digit','.'),('words','.'),('decomp','.'),('compare','.'),('seq','.'),('wordp','.'),('nocalc','.'),('order','.'),('angles','.')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w,h in [(369,610),(360,640)]:
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        bad=[];g=[]
        for c in pg.evaluate("__C()"):
            for k in range(25):
                pg.evaluate(f"__Gen('{c}','.')"); pg.wait_for_timeout(30)
                r=pg.evaluate(J)
                g.append((r['gapNav'],r['gapCard'],c))
                if r['clip'] or r['bd'][1]>r['bd'][0]+2 or r['q'][1]>r['q'][0]+1:
                    bad.append((c,r)); pg.screenshot(path=f'/tmp/t/fit_{w}_{c}.png'); break
        print(w,h,len(bad),'min gap to menu / card edge:',min(g),min(g,key=lambda x:x[1]),errs)
        pg.close()
    b.close()
