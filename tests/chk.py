from playwright.sync_api import sync_playwright
import sys
exec(open('/tmp/t/shot.py').read().split('sizes=')[0].split('import sys, re')[1].replace('from playwright.sync_api import sync_playwright',''))
stub_auth=stub_auth.replace("cb(null)","cb({displayName:'הרב חן בן-ברית - עורך טקסים (Rabbi BenBrit)',uid:'u',photoURL:'',email:'a@b.c'})")
html=html.replace("function nextQ() {","window.__S=(k,o)=>startSession(k,o);window.__E=()=>endSession();window.__D=()=>[session,Q];\nfunction nextQ() {",1)
sizes={'phone':(390,700),'phoneS':(360,640),'land':(844,300),'land2':(915,340),'desk':(1366,650)}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for n,(w,h) in sizes.items():
        pg=b.new_page(viewport={'width':w,'height':h})
        def route(r):
            u=r.request.url
            if u=='http://x/': r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(600)
        print(n,'home overflow',pg.evaluate("document.querySelector('main').scrollHeight-document.querySelector('main').clientHeight"),
         'bad',pg.evaluate("[...document.querySelectorAll('.topic-title')].filter(t=>t.scrollWidth>t.clientWidth+1||t.getBoundingClientRect().right>t.closest('.card').getBoundingClientRect().right+1).length"),
         'btnOut',pg.evaluate("[...document.querySelectorAll('.practice-btn')].filter(b=>{const r=b.getBoundingClientRect(),c=b.closest('.card').getBoundingClientRect();return r.bottom>c.bottom+1||r.right>c.right+1||r.left<c.left-1}).length"))
        pg.screenshot(path=f'/tmp/t/c_home_{n}.png')
        # play: order
        for cat in ['order','angledraw','decomp','nocalc']:
            pg.evaluate(f"__S('base','{cat}')"); pg.wait_for_timeout(120)
            if cat=='order':
                items=pg.locator('#qcard .opts.ord .opt'); 
                for i in range(5): pg.locator('#qcard .opts.ord .opt').first.click()
            if cat=='decomp':
                pg.fill('#qcard input','0')
            pg.evaluate("document.querySelector('#checkBtn').click()"); pg.wait_for_timeout(120)
            r=pg.evaluate("(()=>{const f=document.querySelector('#qcard .feedback');const c=document.querySelector('#qcard');return [f?f.scrollHeight-f.clientHeight:null,c.scrollHeight-c.clientHeight, document.querySelector('#qcard').getBoundingClientRect().bottom<=innerHeight]})()")
            print(' ',cat,r)
            pg.screenshot(path=f'/tmp/t/c_{cat}_{n}.png')
        pg.evaluate("__E()"); pg.wait_for_timeout(100)
        print(' summary',pg.evaluate("(()=>{const c=document.querySelector('#qcard');const last=document.querySelector('#homeBtn').getBoundingClientRect();return [c.scrollHeight-c.clientHeight,last.bottom,innerHeight,c.getBoundingClientRect().top]})()"))
        pg.screenshot(path=f'/tmp/t/c_sum_{n}.png')
        pg.close()
