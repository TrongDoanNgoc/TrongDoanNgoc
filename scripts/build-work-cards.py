"""Render Selected work project cards (desktop, mobile, and static variants)."""
from pathlib import Path
from html import escape
import base64
import random
import textwrap
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
BG,BORDER,TEXT,MUTED,SOFT='#171122','#49345f','#f5f0ff','#c7bddb','#b8a5d0'

PROJECTS=[
    dict(slug='hd-invest',index='01',title='HD Invest',accent='#89ddff',visual='chart',
         kicker='FINTECH · HD SECURITIES',badge='NOW BUILDING',
         text='Trading workflows that connect identity, market data, and execution, from NFC-based eKYC onboarding to orders, portfolio NAV, and investment research.',
         chips=['NFC eKYC','Live markets','Orders','Portfolio NAV','Research'],
         stack='React Native · TypeScript',platforms='iOS · Android'),
    dict(slug='sanxinha',index='02',title='SanXinHa',accent='#f0abfc',visual='ticker',
         kicker='FINTECH · SHINHAN SECURITIES VIETNAM',badge='SHIPPED',
         text='A securities app with realtime KRX market feeds, OCR, NFC, and FaceID identity verification, and an AI chatbot that makes complex workflows approachable.',
         chips=['Realtime KRX feeds','OCR · NFC · FaceID','AI chatbot','FireAnt news'],
         stack='Zustand · React Query · Socket.io',platforms='iOS · Android'),
    dict(slug='vinmec',index='03',title='Vinmec EMR',accent='#c4b5fd',visual='pulse',
         kicker='HEALTHCARE · VINSMART FUTURE / VINGROUP',badge='CLINICAL',
         text='Electronic medical records for doctors and clinical staff: detailed interfaces that keep every step of a patient visit connected, from exam to treatment.',
         chips=['Examination','Diagnosis','Prescriptions','Lab & imaging','Treatment'],
         stack='Connected clinical workflows',platforms='Doctors · Clinical staff'),
    dict(slug='private-nest',index='04',title='Private Nest',accent='#f9a8d4',visual='orbit',
         kicker='INDIE PRODUCT · CREATOR & OWNER',badge='INDIE',
         text='A couple-focused app for shared funds, wardrobes, AI outfit ideas, and memories, taken from an idea to App Store and Google Play releases.',
         chips=['Shared funds','Wardrobes','AI outfit ideas','Memories'],
         stack='Idea → design → store release',platforms='iOS · Android'),
]

CSS=('text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Menlo,Consolas,monospace}'
     '.trace{stroke-dasharray:900;stroke-dashoffset:900;animation:draw 6s ease-in-out infinite}'
     '.bar{transform-box:fill-box;transform-origin:50% 100%;animation:bar 1.6s ease-in-out infinite alternate}'
     '.blink{animation:blink 1.4s steps(2,end) infinite}'
     '.beat{stroke-dasharray:120 640;animation:beat 3.2s linear infinite}'
     '.spin{transform-box:view-box;animation:spin 14s linear infinite}'
     '.heart{transform-box:fill-box;transform-origin:center;animation:heart 1.8s ease-in-out infinite}'
     '.twinkle{animation:blink 3s ease-in-out infinite}'
     '.halo{animation:halo 4s ease-in-out infinite}'
     '@keyframes draw{0%{stroke-dashoffset:900}55%,100%{stroke-dashoffset:0}}'
     '@keyframes bar{from{transform:scaleY(.35)}to{transform:scaleY(1)}}'
     '@keyframes blink{50%{opacity:.2}}'
     '@keyframes beat{from{stroke-dashoffset:760}to{stroke-dashoffset:0}}'
     '@keyframes spin{to{transform:rotate(360deg)}}'
     '@keyframes heart{50%{transform:scale(1.15)}}'
     '@keyframes halo{50%{opacity:.35}}'
     '@media(prefers-reduced-motion:reduce){*{animation:none!important}.trace,.beat{stroke-dasharray:none;stroke-dashoffset:0}}')
STATIC_CSS='text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Menlo,Consolas,monospace}'

def width(text,size,bold=False,spacing=0):
    return len(text)*size*(0.6 if bold else 0.52)+len(text)*spacing

def wrap(text,chars,limit):
    lines=textwrap.wrap(text,chars)
    if len(lines)>limit:
        raise ValueError(f'Shorten copy to {limit} lines: {text}')
    return lines

def icon(slug):
    data=base64.b64encode((ROOT/'assets/work/icons'/f'{slug}.jpg').read_bytes()).decode()
    return f'data:image/jpeg;base64,{data}'

def chips(items,x,y,maxw,accent,size=13):
    out=[];cx,cy=x,y
    for item in items:
        w=width(item,size)+26
        if cx+w>x+maxw and cx>x:
            cx=x;cy+=38
        out.append(f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="28" rx="14" fill="{accent}" fill-opacity=".12" stroke="{accent}" stroke-opacity=".55"/>'
                   f'<text x="{cx+w/2:.0f}" y="{cy+19}" font-size="{size}" fill="{TEXT}" text-anchor="middle">{escape(item)}</text>')
        cx+=w+8
    return ''.join(out),cy+28

def chart(x,y,w,h,accent):
    rnd=random.Random(7);price=0.;pts=[];candles=[];raw=[]
    for i in range(14):
        o=price;price+=rnd.uniform(-.8,1.1);c=price
        raw.append((o,c,max(o,c)+rnd.uniform(.15,.45),min(o,c)-rnd.uniform(.15,.45)))
    low=min(r[3] for r in raw);high=max(r[2] for r in raw)
    Y=lambda v:y+h-(v-low)/(high-low)*h
    for i,(o,c,hi,lo) in enumerate(raw):
        cx=x+12+i*(w-24)/13
        color=accent if c>=o else '#f0abfc'
        candles.append(f'<line x1="{cx:.1f}" y1="{Y(hi):.1f}" x2="{cx:.1f}" y2="{Y(lo):.1f}" stroke="{color}" stroke-opacity=".7"/>'
                       f'<rect x="{cx-4:.1f}" y="{Y(max(o,c)):.1f}" width="8" height="{max(2,abs(Y(o)-Y(c))):.1f}" rx="1.5" fill="{color}" fill-opacity=".85"/>')
        pts.append((cx,Y(c)))
    grid=''.join(f'<line x1="{x}" y1="{y+i*h/3:.0f}" x2="{x+w}" y2="{y+i*h/3:.0f}" stroke="{BORDER}" stroke-dasharray="3 6"/>' for i in range(4))
    line=' '.join(f'{a:.1f},{b:.1f}' for a,b in pts)
    ex,ey=pts[-1]
    return (grid+''.join(candles)+
            f'<polyline class="trace" points="{line}" fill="none" stroke="url(#sweep)" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<circle class="blink" cx="{ex:.1f}" cy="{ey:.1f}" r="5" fill="{accent}"/>'
            f'<text class="mono" x="{x+w}" y="{y-10}" font-size="11" fill="{SOFT}" text-anchor="end">NAV ▲ live</text>')

def ticker(x,y,w,h,accent):
    rnd=random.Random(3);n=18;bw=(w-(n-1)*5)/n;out=[]
    for i in range(n):
        bh=h*rnd.uniform(.35,1)
        color=accent if i%3 else '#89ddff'
        out.append(f'<rect class="bar" style="animation-delay:-{rnd.uniform(0,1.6):.2f}s" x="{x+i*(bw+5):.1f}" y="{y+h-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="{color}" fill-opacity=".8"/>')
    return (''.join(out)+f'<line x1="{x}" y1="{y+h+1}" x2="{x+w}" y2="{y+h+1}" stroke="{BORDER}"/>'
            f'<circle class="blink" cx="{x+w-58}" cy="{y-14}" r="4" fill="#f0abfc"/>'
            f'<text class="mono" x="{x+w}" y="{y-10}" font-size="11" fill="{SOFT}" text-anchor="end">KRX LIVE</text>')

def pulse(x,y,w,h,accent):
    mid=y+h*.6;seg=w/3;d=f'M{x},{mid}'
    for k in range(3):
        b=x+k*seg
        d+=(f' L{b+seg*.35:.1f},{mid} L{b+seg*.42:.1f},{mid-h*.18:.1f} L{b+seg*.48:.1f},{mid+h*.12:.1f}'
            f' L{b+seg*.55:.1f},{y+h*.05:.1f} L{b+seg*.62:.1f},{y+h*.95:.1f} L{b+seg*.69:.1f},{mid} L{b+seg:.1f},{mid}')
    cx,cy=x+w-14,y-14
    return (f'<path d="{d}" fill="none" stroke="{accent}" stroke-opacity=".25" stroke-width="2"/>'
            f'<path class="beat" d="{d}" fill="none" stroke="url(#sweep)" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<rect x="{cx-3}" y="{cy-9}" width="6" height="18" rx="1.5" fill="{accent}"/><rect x="{cx-9}" y="{cy-3}" width="18" height="6" rx="1.5" fill="{accent}"/>'
            f'<text class="mono" x="{cx-18}" y="{cy+4}" font-size="11" fill="{SOFT}" text-anchor="end">EMR · 72 bpm</text>')

def orbit(x,y,w,h,accent):
    cx,cy=x+w/2,y+h/2;r=min(w,h)/2-8
    heart=(f'M{cx},{cy+14} C{cx-30},{cy-6} {cx-14},{cy-28} {cx},{cy-12} C{cx+14},{cy-28} {cx+30},{cy-6} {cx},{cy+14}Z')
    rnd=random.Random(11)
    stars=''.join(f'<circle class="twinkle" style="animation-delay:-{rnd.uniform(0,3):.1f}s" cx="{x+rnd.uniform(0,w):.0f}" cy="{y+rnd.uniform(0,h):.0f}" r="{rnd.choice([1,1.5,2])}" fill="{TEXT}" fill-opacity=".7"/>' for _ in range(14))
    return (stars+
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.6:.0f}" ry="{r*.62:.0f}" fill="none" stroke="{BORDER}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.1:.0f}" ry="{r*.95:.0f}" fill="none" stroke="{BORDER}" stroke-dasharray="2 6"/>'
            f'<g class="spin" style="transform-origin:{cx}px {cy}px"><circle cx="{cx+r*1.1:.0f}" cy="{cy}" r="6" fill="#89ddff"/><circle cx="{cx-r*1.1:.0f}" cy="{cy}" r="4" fill="#c4b5fd"/></g>'
            f'<path class="heart" d="{heart}" fill="{accent}"/>')

VISUALS=dict(chart=chart,ticker=ticker,pulse=pulse,orbit=orbit)

def frame(w,h,p,animated,body):
    a=p['accent']
    defs=(f'<defs><linearGradient id="sweep" x1="0" x2="1"><stop stop-color="#c4b5fd"/><stop offset=".5" stop-color="{a}"/><stop offset="1" stop-color="#89ddff"/></linearGradient>'
          f'<radialGradient id="glow"><stop stop-color="{a}" stop-opacity=".22"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>'
          f'<clipPath id="card"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20"/></clipPath></defs>')
    title=f'{p["title"]}: {p["kicker"].title()}. {p["text"]}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">'
            f'<title id="title">{escape(title)}</title><style>{CSS if animated else STATIC_CSS}</style>{defs}'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="{BG}" stroke="{BORDER}"/><g clip-path="url(#card)">{body}</g></svg>')

def icon_block(p,x,y,s,animated):
    a=p['accent'];r=s*.23
    return (f'<circle class="{"halo" if animated else ""}" cx="{x+s/2}" cy="{y+s/2}" r="{s*.78:.0f}" fill="url(#glow)"/>'
            f'<clipPath id="i-{p["slug"]}"><rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{r:.0f}"/></clipPath>'
            f'<image xlink:href="{icon(p["slug"])}" x="{x}" y="{y}" width="{s}" height="{s}" clip-path="url(#i-{p["slug"]})" preserveAspectRatio="xMidYMid slice"/>'
            f'<rect x="{x-.5}" y="{y-.5}" width="{s+1}" height="{s+1}" rx="{r:.0f}" fill="none" stroke="{a}" stroke-opacity=".6"/>')

def badge(text,x,y,accent,anchor_end=False):
    w=width(text,11,True,1)+22
    x0=x-w if anchor_end else x
    return (f'<rect x="{x0:.0f}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{accent}" fill-opacity=".16" stroke="{accent}" stroke-opacity=".7"/>'
            f'<text x="{x0+w/2:.0f}" y="{y+16}" font-size="11" font-weight="bold" letter-spacing="1" fill="{accent}" text-anchor="middle">{escape(text)}</text>')

def desktop(p,animated):
    W,H,a=1000,300,p['accent'];tx=160
    lines=wrap(p['text'],80,2)
    body=[f'<circle cx="840" cy="150" r="230" fill="url(#glow)"/>',
          f'<text x="968" y="282" font-size="150" font-weight="bold" fill="{TEXT}" fill-opacity=".04" text-anchor="end">{p["index"]}</text>',
          icon_block(p,36,42,100,animated),
          f'<text x="{tx}" y="60" font-size="12" font-weight="bold" letter-spacing="1.6" fill="{a}">{escape(p["kicker"])}</text>',
          f'<text x="{tx}" y="102" font-size="34" font-weight="bold" fill="{TEXT}">{escape(p["title"])}</text>',
          badge(p['badge'],968,36,a,True)]
    body+= [f'<text x="{tx}" y="{136+i*22}" font-size="15" fill="{MUTED}">{escape(l)}</text>' for i,l in enumerate(lines)]
    c,bottom=chips(p['chips'],tx,186,556,a)
    if bottom>220:
        raise ValueError(f'Chips for {p["title"]} need a second row')
    body.append(c)
    body.append(VISUALS[p['visual']](716,96,244,108,a))
    body+= [f'<line x1="36" y1="234" x2="964" y2="234" stroke="{BORDER}"/>',
            f'<text x="36" y="266" font-size="13" fill="{SOFT}"><tspan fill="{a}">◆</tspan>  {escape(p["stack"])}</text>',
            f'<text class="mono" x="964" y="266" font-size="12" fill="{SOFT}" text-anchor="end">{escape(p["platforms"])}  ·  {p["index"]}/04</text>']
    return frame(W,H,p,animated,''.join(body))

def mobile(p,animated):
    W,a=600,p['accent'];tx=124
    lines=wrap(p['text'],52,5)
    body=[f'<circle cx="480" cy="80" r="200" fill="url(#glow)"/>',
          icon_block(p,28,32,84,animated),
          f'<text x="{tx+4}" y="52" font-size="12" font-weight="bold" letter-spacing="1" fill="{a}">{escape(p["kicker"])}</text>',
          f'<text x="{tx+4}" y="92" font-size="32" font-weight="bold" fill="{TEXT}">{escape(p["title"])}</text>',
          badge(p['badge'],tx+4,106,a)]
    y=176
    body+= [f'<text x="28" y="{y+i*27}" font-size="19" fill="{MUTED}">{escape(l)}</text>' for i,l in enumerate(lines)]
    y+=len(lines)*27+4
    c,y=chips(p['chips'],28,y,544,a,15);body.append(c)
    y+=44
    body.append(VISUALS[p['visual']](28,y+18,544,90,a))
    y+=132
    body+= [f'<line x1="28" y1="{y}" x2="572" y2="{y}" stroke="{BORDER}"/>',
            f'<text x="28" y="{y+34}" font-size="16" fill="{SOFT}"><tspan fill="{a}">◆</tspan>  {escape(p["stack"])}</text>',
            f'<text class="mono" x="572" y="{y+34}" font-size="13" fill="{SOFT}" text-anchor="end">{p["index"]}/04</text>']
    return frame(W,y+56,p,animated,''.join(body))

if __name__=='__main__':
    for p in PROJECTS:
        for animated,base in [(True,ROOT/'assets/work'),(False,ROOT/'assets/static/work')]:
            base.mkdir(parents=True,exist_ok=True)
            for suffix,render in [('',desktop),('-mobile',mobile)]:
                svg=render(p,animated)
                ET.fromstring(svg)
                (base/f'{p["slug"]}{suffix}.svg').write_text(svg)
