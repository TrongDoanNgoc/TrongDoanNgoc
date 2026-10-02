"""Create static SVG fallbacks selected by README picture media queries."""
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
SOURCES=['header.svg','header-mobile.svg','footer.svg','footer-mobile.svg',
         'terminal.svg','terminal-mobile.svg','divider.svg',
         'github/activity.svg','github/activity-mobile.svg']
for name in SOURCES:
    tree=ET.parse(ROOT/'assets'/name)
    root=tree.getroot()
    for parent in root.iter():
        for child in list(parent):
            if child.tag==f'{{{NS}}}style':parent.remove(child)
    style=ET.SubElement(root,f'{{{NS}}}style')
    style.text='text{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Menlo,Consolas,monospace}.gradient-title{fill:url(#candy)}.shoot{display:none}.flow{stroke-dasharray:10 18}.dots{stroke-dasharray:2 28}'
    if name.startswith('terminal'):
        style.text+='text{font-family:Menlo,Consolas,monospace}'
    dest=ROOT/'assets/static'/name
    dest.parent.mkdir(parents=True,exist_ok=True)
    tree.write(dest,encoding='unicode')
