from playwright.sync_api import sync_playwright
exec(open('/tmp/t/shot.py').read().split('sizes=')[0].split('import sys, re')[1].replace('from playwright.sync_api import sync_playwright',''))
html=html.replace("function nextQ() {","window.__C=()=>CATS;\nfunction nextQ() {",1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1000,'height':700})
    errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u=='http://x/': r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(400)
    r=pg.evaluate("""()=>{const out={};for(const c of __C()){let bad=0,ex=[];for(let t=1;t<=3;t++)for(let i=0;i<300;i++){try{const q=c.gen(t);if(!q.body||!q.parts.length)bad++;for(const p of q.parts){if(p.type==='num'&&!(Number.isInteger(p.ans)&&p.ans>=0))bad++;if(p.type==='buttons'&&!p.opts.includes(p.ans))bad++;if(p.type==='buttons'&&new Set(p.opts).size!==p.opts.length)bad++}
 if(typeof q.explain==='string'&&/undefined|NaN/.test(q.explain+q.body+q.hint))bad++;if(/undefined|NaN/.test(q.body))bad++;if(i<1&&t==2)ex.push(q.body.replace(/<[^>]+>/g,' ').slice(0,90))}catch(e){bad++;ex.push(String(e))}}out[c.id]=[bad,ex]}return out}""")
    for k,v in r.items(): print(k,v)
    print(errs)
