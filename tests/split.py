exec(open('/tmp/sk/sk.py').read().split("BASE=")[0])
J="""(()=>{const c=document.querySelector('#qcard');const q=s=>{const e=c.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]};
const bd=c.querySelector('.question-board');return {rows:getComputedStyle(c).gridTemplateRows,ch:c.clientHeight,cls:c.className,board:q('.question-board'),zoom:getComputedStyle(bd.querySelector('.prompt')||bd).fontSize,clip:bd.scrollHeight>bd.clientHeight+1||bd.scrollWidth>bd.clientWidth+1,fb:q('.fbslot'),ans:q('.parts'),act:q('.qactions'),card:q('#qcard')?null:null,cardOv:c.scrollHeight>c.clientHeight+2,key:q('.kp-key')}})()"""
cases=[('column',"!Q.body.includes('prompt')"),('equation','true'),('word','true'),('column',"Q.body.includes('במאונך')"),('column',"!Q.body.includes('במאונך')"),('seq',"Q.parts.length===2&&Q.parts[0].type==='num'"),('numline',"Q.parts[0].type==='num'"),('equation','true'),('word','Q.parts[0].type==="num"'),('decomp','true'),('mult','Q.parts[0].type==="num"'),('words','Q.parts[0].type==="text"||Q.parts[0].type==="num"'),('digit','Q.parts[0].type==="num"')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for W,H in [(1280,800),(1024,768),(960,600)]:
        ctx=b.new_context(viewport={'width':W,'height':H},device_scale_factor=1,has_touch=True,is_mobile=True)
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if font_route(r): return
            if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(800); pg.evaluate("document.querySelectorAll('.modal-back').forEach(e=>e.remove())")
        for cat,cond in cases:
            pg.evaluate(f"__Q('{cat}',Q=>{cond})"); pg.wait_for_timeout(250)
            r=pg.evaluate(J); bad=r['clip'] or r['cardOv'] or not 'split' in r['cls']
            print(r['rows'],r['ch']) if 'wideq' in r['cls'] else None; print(W,H,cat,'BAD' if bad else 'ok',r['cls'].replace('card',''),r['zoom'],r['board'],r['key'])
            if W==1280: pg.screenshot(path=f'r_{cat}_{cond[:6].replace("/","")}.png')
        print(errs[:2]); ctx.close()
    b.close()
