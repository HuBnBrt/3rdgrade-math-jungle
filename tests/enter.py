from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__Show=id=>{session={kind:'base',only:null,total:8,done:0,correct:0,coins:0,sheet:[id,'s13'],topics:['decomp','decomp']};nextQ();};window.__G=()=>[S.coins,S.owner||null];window.__Add=(g,c)=>addProgress(g,c);")
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
    pg.evaluate("__Show('s12')"); pg.fill('#qcard input','20'); pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
    print('after 1st enter result', pg.evaluate("__D()[1].result"))
    pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
    print('after 2nd enter q', pg.evaluate("__D()[1].sheetId"), pg.evaluate("__D()[1].result"))
    pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
    print('empty enter ->', pg.evaluate("__D()[1].result"), pg.evaluate("document.querySelector('#hintBox')?.textContent||''")[:40])
    o=pg.evaluate("""(o=>JSON.stringify({c:o.coins,s:o.sessions,st:o.stats,i:o.items,m:o.mastery}))(__Add({coins:20,sessions:2,stats:{mult:{ok:5,bad:1,h:'111110'}},items:{lion:1},mastery:{mult:{score:40,tier:2}}},{coins:30,sessions:5,stats:{mult:{ok:9,bad:1,h:'1'}},items:{frog:1},mastery:{mult:{score:70,tier:3,trophy:true}}}))""")
    print(o, errs)
    b.close()
