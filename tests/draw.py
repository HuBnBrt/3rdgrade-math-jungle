from playwright.sync_api import sync_playwright
html=open('/home/claude/g4-jungle-math/index.html',encoding='utf-8').read()
auth="export const getAuth=()=>({});export class GoogleAuthProvider{static credential(){}};export const signInWithCredential=async()=>{};export const signOut=async()=>{};export const onAuthStateChanged=(a,cb)=>{cb(null)};"
stubs={'firebase-app':"export const initializeApp=()=>({});",'firebase-auth':auth,'firebase-firestore':"export const getFirestore=()=>({});export const doc=()=>({});export const getDoc=async()=>({exists:()=>false});export const setDoc=async()=>{};export const serverTimestamp=()=>0;"}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for name,(w,h) in {'desk':(1366,650),'phone':(390,760)}.items():
        found=False
        for attempt in range(30):
            pg=b.new_page(viewport={'width':w,'height':h})
            def route(r):
                u=r.request.url
                if u=='http://x/': r.fulfill(body=html,content_type='text/html'); return
                for k,v in stubs.items():
                    if k in u: r.fulfill(body=v,content_type='text/javascript'); return
                r.abort()
            pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(200); pg.click('#startBtn')
            for i in range(8):
                if pg.query_selector('#qcard [data-draw]'):
                    pg.screenshot(path=f'draw_{name}.png'); found=True; break
                if pg.query_selector('#qcard input'):
                    for inp in pg.query_selector_all('#qcard input'): inp.fill('7')
                elif pg.query_selector('#qcard .opts .opt'): pg.click('#qcard .opts .opt')
                while pg.query_selector('#qcard .opts .opt') and pg.query_selector('#qcard .seq'): pg.click('#qcard .opts .opt')
                pg.click('#checkBtn'); pg.wait_for_timeout(80)
                
                if pg.query_selector('#nextBtn'): pg.click('#nextBtn')
                pg.wait_for_timeout(80)
            pg.close()
            if found: break
        print(name,found)
    b.close()
