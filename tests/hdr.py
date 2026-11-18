from playwright.sync_api import sync_playwright
html=open('/home/claude/g4-jungle-math/index.html',encoding='utf-8').read()
auth="export const getAuth=()=>({});export class GoogleAuthProvider{static credential(){}};export const signInWithCredential=async()=>{};export const signOut=async()=>{};export const onAuthStateChanged=(a,cb)=>{cb({displayName:'הרב חן בן-ברית - עורך טקסים (Rabbi BenBrit)',email:'a@b.c',photoURL:'',uid:'u'})};"
stubs={'firebase-app':"export const initializeApp=()=>({});",'firebase-auth':auth,'firebase-firestore':"export const getFirestore=()=>({});export const doc=()=>({});export const getDoc=async()=>({exists:()=>false});export const setDoc=async()=>{};export const serverTimestamp=()=>0;"}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for name,(w,h) in {'n373':(373,560),'n746':(746,1000),'d1366':(1366,650)}.items():
        pg=b.new_page(viewport={'width':w,'height':h})
        def route(r):
            u=r.request.url
            if u=='http://x/': r.fulfill(body=html,content_type='text/html'); return
            for k,v in stubs.items():
                if k in u: r.fulfill(body=v,content_type='text/javascript'); return
            r.abort()
        pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
        pg.screenshot(path=f'hdr_{name}.png')
        print(name,pg.evaluate("document.querySelector('header').getBoundingClientRect().height"))
    b.close()
