"""Restyle generated widget art without altering the contribution data."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
WIDGETS=Path('assets/widgets')
REDUCED='<style>@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style>'
LANGS=['#c4b5fd','#f0abfc','#89ddff','#ac87df','#e9d5ff','#a5b4fc']

def galaga(svg):
    palette={'#0d1117':'#171122','#161b22':'#271d39','#010409':'#110e1b',
             '#0e4429':'#513a75','#006d32':'#815bb3','#26a641':'#ac87df',
             '#39d353':'#d8b4fe','#9be9a8':'#513a75','#40c463':'#815bb3',
             '#30a14e':'#ac87df','#216e39':'#d8b4fe'}
    svg=re.sub(r'#[0-9a-fA-F]{6}',lambda m:palette.get(m[0].lower(),m[0]),svg)
    return svg if REDUCED in svg else svg.replace('</svg>',REDUCED+'</svg>')

def city(svg):
    legend=re.findall(r'<rect [^>]*fill="(#[0-9a-fA-F]{6})" class="stroke-bg"',svg)
    palette={}
    for color in legend:
        palette.setdefault(color.lower(),LANGS[len(palette)%len(LANGS)])
    def recolor(m):
        return m[1]+palette.get(m[2].lower(),m[2])
    svg=re.sub(r'(fill="|fill: )(#[0-9a-fA-F]{6})',recolor,svg)
    # Zero stars and forks read as a weakness rather than information.
    empty=r'<g transform="translate\(\d+, 802\), scale\(2\)"><path [^>]*></path></g><text [^>]*>0<title>0</title></text>'
    if len(re.findall(empty,svg))==2:
        svg=re.sub(empty,'',svg)
        svg=svg.replace('x="384" y="830" text-anchor="end"','x="630" y="830" text-anchor="end"')
        svg=svg.replace('x="394" y="830" text-anchor="start"','x="640" y="830" text-anchor="start"')
    return svg

for name,restyle in [('galaga.svg',galaga),('lavender-city.svg',city),('lavender-city-static.svg',city)]:
    p=WIDGETS/name
    if p.exists():
        svg=restyle(p.read_text())
        ET.fromstring(svg)
        p.write_text(svg)
