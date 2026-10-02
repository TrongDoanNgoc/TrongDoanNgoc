"""Restyle generated arcade art without altering the contribution data."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
p=Path('assets/widgets/galaga.svg')
if p.exists():
    svg=p.read_text()
    palette={'#0d1117':'#171122','#161b22':'#271d39','#010409':'#110e1b',
             '#0e4429':'#513a75','#006d32':'#815bb3','#26a641':'#ac87df',
             '#39d353':'#d8b4fe','#9be9a8':'#513a75','#40c463':'#815bb3',
             '#30a14e':'#ac87df','#216e39':'#d8b4fe'}
    svg=re.sub(r'#[0-9a-fA-F]{6}',lambda m:palette.get(m[0].lower(),m[0]),svg)
    svg=svg.replace('</svg>','<style>@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style></svg>')
    ET.fromstring(svg)
    p.write_text(svg)
