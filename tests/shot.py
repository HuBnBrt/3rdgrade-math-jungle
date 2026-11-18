import sys, re
from playwright.sync_api import sync_playwright
html=open('/home/claude/g4-jungle-math/updatever.html',encoding='utf-8').read()
stub_auth="export const getAuth=()=>({});export class GoogleAuthProvider{static credential(){}};export const signInWithCredential=async()=>{};export const signOut=async()=>{};export const onAuthStateChanged=(a,cb)=>{cb(null)};"
stub_app="export const initializeApp=()=>({});"
stub_fs="export const getFirestore=()=>({});export const doc=()=>({});export const getDoc=async()=>({exists:()=>false});export const setDoc=async()=>{};export const serverTimestamp=()=>0;"
sizes={'desk':(1366,650),'big':(1920,1000),'phone':(390,760),'tablet':(820,1100),'land':(780,360)}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for name,(w,h) in sizes.items():
        pg=b.new_page(viewport={'width':w,'height':h})
        def route(r):
            u=r.request.url
            if u=='http://x/': r.fulfill(body=html,content_type='text/html')
            elif 'firebase-app' in u: r.fulfill(body=stub_app,content_type='text/javascript')
            elif 'firebase-auth' in u: r.fulfill(body=stub_auth,content_type='text/javascript')
            elif 'firebase-firestore' in u: r.fulfill(body=stub_fs,content_type='text/javascript')
            else: r.abort()
        pg.route('**/*',route)
        pg.goto('http://x/'); pg.wait_for_timeout(500)
        pg.screenshot(path=f'home_{name}.png')
        sc=pg.evaluate("[document.documentElement.scrollHeight,innerHeight,document.querySelector('main').scrollHeight,document.querySelector('main').clientHeight]")
        print(name,'home',sc)
        pg.click('#startBtn'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'play_{name}.png')
        q=pg.evaluate("(()=>{const c=document.querySelector('#qcard');return [c.scrollHeight,c.clientHeight,c.getBoundingClientRect().height]})()")
        pg.click('#hintBtn'); 
        pg.click('#checkBtn'); pg.wait_for_timeout(200)
        pg.screenshot(path=f'play2_{name}.png')
        q2=pg.evaluate("(()=>{const c=document.querySelector('#qcard');return [c.scrollHeight,c.clientHeight,c.getBoundingClientRect().height]})()")
        print(name,'qcard',q,q2)
        pg.click('.nav [data-go=camp]'); pg.wait_for_timeout(200)
        pg.screenshot(path=f'camp_{name}.png')
        print(name,'camp',pg.evaluate("(()=>{const m=document.querySelector('#view-camp');return [m.scrollHeight,m.clientHeight]})()"))
        pg.click('.nav [data-go=settings]'); pg.wait_for_timeout(200)
        print(name,'settings',pg.evaluate("(()=>{const m=document.querySelector('#view-settings');return [m.scrollHeight,m.clientHeight]})()"))
        pg.close()
    b.close()
