from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Show=id=>{session={kind:'base',only:null,total:8,done:0,correct:0,coins:0,sheet:[id,'s13'],topics:['decomp','decomp']};nextQ();};window.__G=()=>[S.coins,S.owner||null];window.__Add=(g,c)=>addProgress(g,c);")
html=html.replace('window.__D=()=>[session,Q];','window.__D=()=>[session,Q];'+"window.__Set=(v)=>{S.stats={digit:{ok:9,bad:1,h:'1111111110'},compare:{ok:2,bad:4,h:'001010'},mult:{ok:1,bad:1,h:'10'},seq:{ok:5,bad:2,h:'1101110'}};S.mastery={digit:{score:80,tier:3,trophy:true,medal:true},compare:{score:50,tier:2},seq:{score:20,tier:1}};S.settings.statsView=v;S.autoRec=null;S.recCool={};renderHome();};window.__TF=(a)=>{teacherFocus=a;renderHome();};window.__AR=()=>S.autoRec;",1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w,h in [(1280,720),(390,780),(844,390),(800,1180),(1511,932)]:
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        J="(()=>{const m=document.querySelector('main')||document.body;const cs=[...document.querySelectorAll('.cats .card')].map(c=>{const b=c.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)]});const tt=[...document.querySelectorAll('.cats .card')].map(c=>{const q=s=>{const e=c.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)].join(',')};return [q('.topic-title span'),getComputedStyle(c.querySelector('.topic-title')).fontSize,q('.bar.prog'),q('.stars'),q('.rankbadge'),q('.practice-btn')].join('|')});const bad=[...document.querySelectorAll('.cats .card .topic-content')].filter(t=>t.scrollHeight>t.clientHeight+1).length;return {ov:m.scrollHeight-m.clientHeight,bad,cs:cs.slice(0,2),tt}})()"
        pg.evaluate("__Set(false)"); pg.wait_for_timeout(200); a=pg.evaluate(J); ar=pg.evaluate("__AR()")
        pg.screenshot(path=f'hm_n_{w}.png')
        pg.click('#statToggle'); pg.wait_for_timeout(250); c=pg.evaluate(J)
        pg.screenshot(path=f'hm_s_{w}.png')
        diff=[(i,x,y) for i,(x,y) in enumerate(zip(a['tt'],c['tt'])) if x!=y]; print(w,h,'cards', 'same' if a['cs']==c['cs'] else 'MOVED','bad',a['bad'],c['bad'],'title/bar diffs',diff[:3], errs)
        pg.close()
    b.close()
