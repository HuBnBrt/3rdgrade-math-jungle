from playwright.sync_api import sync_playwright
import json
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","""window.__D=()=>[session,Q];window.__LEAK=()=>{const out={};const strip=h=>h.replace(/<[^>]+>/g,' ').replace(/&[a-z]+;/g,' ');
for(const c of CATS){let n=0,bad=[];for(let t=1;t<=3;t++)for(let i=0;i<700;i++){let q;try{q=c.gen(t)}catch(e){bad.push('ERR '+e);continue}n++;const txt=' '+strip(q.body||'')+' ';
(q.parts||[]).forEach(p=>{if(p.type!=='num')return;const a=p.ans;const forms=[String(a),fmt(a)];if(forms.some(f=>new RegExp('(^|[^0-9,])'+f.replace(/,/g,',')+'([^0-9,]|$)').test(txt)))bad.push(txt.replace(/\\s+/g,' ').trim().slice(0,140)+' => '+a)})}
out[c.id]=[n,bad.length,[...new Set(bad)].slice(0,4)]}return out};""")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1280,'height':720}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
    r=pg.evaluate("__LEAK()")
    for k,v in r.items(): print(k,v[0],v[1]); [print('   ',x) for x in v[2]]
    print(errs); b.close()
