# serve the real Noto Sans Hebrew (from npm @fontsource) instead of Google Fonts, so tests measure real text sizes
import os
FD='/tmp/fonts/node_modules/@fontsource/noto-sans-hebrew/'
FCSS=''.join(open(FD+f'{w}.css').read() for w in (400,600,700,800,900)).replace('url(./files/','url(http://x/fonts/')
def font_route(r):
    u=r.request.url
    if 'fonts.googleapis.com' in u: r.fulfill(body=FCSS,content_type='text/css'); return True
    if u.startswith('http://x/fonts/'):
        f=FD+'files/'+u.split('/fonts/')[1]
        if os.path.exists(f): r.fulfill(body=open(f,'rb').read(),content_type='font/woff2' if f.endswith('2') else 'font/woff'); return True
        r.abort(); return True
    return False
