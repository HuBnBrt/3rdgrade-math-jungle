from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
html=html.replace("window.__D=()=>[session,Q];","window.__D=()=>[session,Q];window.__M=(a,b)=>mergeProgress(a,b);")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
    print(pg.evaluate("""(o=>JSON.stringify({c:o.coins,i:o.items,g:o.gear,s:o.sheetOk,m:o.mastery,st:o.stats,p:o.profile}))(__M(
     {coins:12,items:{lion:1},gear:{hat:true},sheetOk:{s1:true,s2:true},mastery:{mult:{score:70,tier:3,trophy:true},seq:{score:20,tier:1}},stats:{mult:{ok:9,bad:1,h:''}},profile:{nick:'אדיר',gender:'m'}},
     {coins:30,items:{frog:1},gear:{map:true},sheetOk:{s5:true},mastery:{seq:{score:45,tier:2,medal:false}},stats:{mult:{ok:2,bad:0,h:''}},profile:{nick:'',gender:''}}))"""), errs)
    b.close()
