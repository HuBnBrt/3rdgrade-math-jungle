from playwright.sync_api import sync_playwright
src=open('/tmp/t/chk.py').read().split("sizes={'phone'")[0]
exec(src)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':700})
    def route(r):
        u=r.request.url
        if u=='http://x/': r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
    pg.evaluate("__S('base','order')"); pg.wait_for_timeout(100)
    for i in range(5): pg.locator('#qcard .opts.ord .opt').first.click()
    pg.evaluate("document.querySelector('#checkBtn').click()")
    print(pg.evaluate("document.querySelector('#qcard .feedback').innerHTML"))
    print(pg.evaluate("(()=>{const s=document.querySelector('#qcard .feedback .ltr');return [getComputedStyle(s).direction,getComputedStyle(s).unicodeBidi,getComputedStyle(s).display]})()"))
    pg.screenshot(path='/tmp/t/ord.png')
