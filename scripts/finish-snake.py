"""Add reduced-motion support and an accessible name to generated snake SVG."""
from pathlib import Path
p = Path('assets/github/snake.svg')
s = p.read_text()
if 'prefers-reduced-motion' not in s:
    s=s.replace('</svg>','<style>@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style></svg>')
if '<title>' not in s:
    pos=s.index('>')+1
    s=s[:pos]+'<title>Snake animation of TrongDoanNgoc’s GitHub contributions</title>'+s[pos:]
p.write_text(s)
