from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1274,'height':590})
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(600)
    print(pg.evaluate("(()=>{const g=document.querySelector('.grid.cats'),cs=getComputedStyle(g),m=document.querySelector('main'),v=document.querySelector('#view-home');return [g.clientHeight,cs.gridTemplateRows,cs.getPropertyValue('--an'),m.clientHeight,v.clientHeight,getComputedStyle(document.querySelector('.cats .slot')).paddingTop]})()"))
    print(pg.evaluate("""(()=>{const c=document.querySelector('.cats .card');const t=c.querySelector('.topic-content');
      return {c:[c.clientWidth,c.clientHeight,c.scrollWidth,c.scrollHeight],t:[t.clientHeight,t.scrollHeight],kids:[...t.children].map(k=>[k.className,k.offsetHeight,getComputedStyle(k).display]),all:[...c.children].map(k=>[k.className,k.offsetHeight])}})()"""))
    pg.screenshot(path='/tmp/t/dbg.png'); b.close()
