from playwright.sync_api import sync_playwright
html=open('/home/claude/g4-jungle-math/admin.html').read()
app="export const initializeApp=()=>({});"
auth="export class GoogleAuthProvider{};export const getAuth=()=>({});export const signInWithPopup=async()=>{};export const signOut=async()=>{};export const onAuthStateChanged=(a,cb)=>setTimeout(()=>cb({email:'BenBritCRM@gmail.com'}),50);"
fs='''export const getFirestore=()=>({});export const doc=(d,...p)=>({p});export const collection=(d,n)=>({n});export const serverTimestamp=()=>0;export const setDoc=async()=>{};export const updateDoc=async()=>{};export const deleteDoc=async()=>{};
const T=(ok,bad,h,t)=>({name:'x',ok,bad,h,tier:t||1});
export const getDoc=async()=>({exists:()=>true});
export const getDocs=async(c)=>({docs: c.n==='admins'?[{id:'bencritcrm@gmail.com',data:()=>({})}]:[
 {id:'u1',data:()=>({name:'דנה',email:'d@x.com',sessions:5,lastSeen:{toDate:()=>new Date()},topics:{mult:{...T(9,1,'1111011111',3),name:'לוח הכפל'},seq:{...T(1,6,'0000100',1),name:'סדרות'},col:{...T(0,0,'',1),name:'חיבור וחיסור'}}})},
 {id:'u2',data:()=>({name:'יואב',email:'y@x.com',sessions:2,lastSeen:{toDate:()=>new Date()},topics:{mult:{...T(3,3,'000111',2),name:'לוח הכפל'},seq:{...T(5,0,'11111',2),name:'סדרות'},col:{...T(4,1,'11011',2),name:'חיבור וחיסור'}}})}]});'''
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1300,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if u.startswith('http://x/'): r.fulfill(body=html,content_type='text/html')
        elif 'firebase-app' in u: r.fulfill(body=app,content_type='text/javascript')
        elif 'firebase-auth' in u: r.fulfill(body=auth,content_type='text/javascript')
        elif 'firebase-firestore' in u: r.fulfill(body=fs,content_type='text/javascript')
        else: r.abort()
    pg.route('**/*',route); pg.goto('http://x/'); pg.wait_for_timeout(500)
    pg.click('td.name'); pg.wait_for_timeout(300)
    pg.screenshot(path='/tmp/t/admin.png',full_page=True); print(errs)
