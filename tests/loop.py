from playwright.sync_api import sync_playwright
html=open('/home/claude/g4-jungle-math/index.html',encoding='utf-8').read()
stub_auth="export const getAuth=()=>({});export class GoogleAuthProvider{static credential(){}};export const signInWithCredential=async()=>{};export const signOut=async()=>{};export const onAuthStateChanged=(a,cb)=>{cb(null)};"
stubs={'firebase-app':"export const initializeApp=()=>({});",'firebase-auth':stub_auth,'firebase-firestore':"export const getFirestore=()=>({});export const doc=()=>({});export const getDoc=async()=>({exists:()=>false});export const setDoc=async()=>{};export const serverTimestamp=()=>0;"}
sizes={'desk':(1366,650),'phone':(390,760),'smallphone':(360,640),'land':(780,360),'tablet':(820,1100)}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for name,(w,h) in sizes.items():
        bad=[]
        for rep in range(3):
            pg=b.new_page(viewport={'width':w,'height':h})
            def route(r):
                u=r.request.url
                if u=='http://x/': r.fulfill(body=html,content_type='text/html'); return
                for k,v in stubs.items():
                    if k in u: r.fulfill(body=v,content_type='text/javascript'); return
                r.abort()
            pg.on('pageerror',lambda e:print('ERR',e)); pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(300)
            pg.click('#startBtn')
            for i in range(8):
                pg.wait_for_timeout(100)
                # answer
                if pg.query_selector('#qcard input'):
                    for inp in pg.query_selector_all('#qcard input'): inp.fill('7')
                elif pg.query_selector('#qcard .opts .opt'):
                    pg.click('#qcard .opts .opt')
                elif pg.query_selector('#qcard [data-draw]'): pass
                # order type
                while pg.query_selector('#qcard .opts .opt') and pg.query_selector('#qcard .seq'):
                    pg.click('#qcard .opts .opt')
                pg.click('#checkBtn'); pg.wait_for_timeout(100)
                m=pg.evaluate("(()=>{const c=document.querySelector('#qcard');const bd=document.querySelector('.question-board').getBoundingClientRect();const pr=document.querySelector('.parts').getBoundingClientRect();return {o:c.scrollHeight-c.clientHeight,bh:Math.round(bd.height),h:Math.round(c.getBoundingClientRect().height),q:document.querySelector('.question-board').scrollHeight-document.querySelector('.question-board').clientHeight}})()")
                if m['o']>1 or m['q']>1: 
                    bad.append(m); pg.screenshot(path=f'bad_{name}_{rep}_{i}.png')
                if pg.query_selector('#nextBtn'): pg.click('#nextBtn')
                else: break
            pg.close()
        print(name,'bad:',bad[:3],len(bad))
    b.close()
