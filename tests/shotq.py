import sys
import sys
exec(open('/tmp/t/enter.py').read().split("with sync_playwright")[0])
html=html.replace('window.__D=()=>[session,Q];','window.__D=()=>[session,Q];window.__C=()=>CATS.map(c=>c.id);window.__Gen=(cat,re)=>{for(let k=0;k<300;k++){session={kind:"base",only:cat,total:8,done:0,correct:0,coins:0,topics:[cat]};nextQ();if(new RegExp(re).test(document.querySelector("#qcard .question-board").textContent.replace(/[\\u0591-\\u05c7]/g,"")))return true;}return false;};',1)
from playwright.sync_api import sync_playwright
J="(()=>{const bd=document.querySelector('#qcard .question-board');const q=document.querySelector('#qcard');const els=[...document.querySelectorAll('#qcard .question-board *')];const clip=els.filter(e=>{const r=e.getBoundingClientRect(),b=bd.getBoundingClientRect();return r.height>0&&(r.top<b.top-1||r.bottom>b.bottom+1)}).length;return {bd:[bd.clientHeight,bd.scrollHeight],clip,q:[q.clientHeight,q.scrollHeight],fs:getComputedStyle(bd.querySelector('.prompt')).fontSize}})()"
cases=[('digit','האם המספר החדש'),('digit','.'),('words','.'),('decomp','.'),('compare','.'),('seq','.'),('wordp','.'),('nocalc','.'),('order','.'),('angles','.')]

from playwright.sync_api import sync_playwright
w,h=int(sys.argv[1]),int(sys.argv[2])
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':w,'height':h})
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
    for c,rx in [('digit','האם המספר החדש'),('equation','.')]:
        pg.evaluate(f"__Gen('{c}','{rx}')"); pg.wait_for_timeout(100); pg.screenshot(path=f'/tmp/t/q_{c}.png')
        print(c, pg.evaluate(J))
    b.close()
