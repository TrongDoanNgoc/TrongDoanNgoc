#!/usr/bin/env python3
"""Render lavender GitHub cards from the public GitHub GraphQL API via gh."""
from __future__ import annotations
import json
import subprocess
import textwrap
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/github'
THEME = json.loads((ROOT / 'assets/theme.json').read_text())
QUERY = '''query {
  user(login: "TrongDoanNgoc") {
    contributionsCollection { contributionCalendar {
      totalContributions weeks { contributionDays { contributionCount contributionLevel date } }
    } }
    repositories(first: 1, privacy: PUBLIC, ownerAffiliations: OWNER) { totalCount }
    followers { totalCount }
  }
  nodebase: repository(owner: "TrongDoanNgoc", name: "nodebase") {
    name description stargazerCount forkCount primaryLanguage { name }
  }
  portfolio: repository(owner: "TrongDoanNgoc", name: "portfolio-dnt") {
    name description stargazerCount forkCount primaryLanguage { name }
  }
}'''

def svg(w: int, h: int, title: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title><style>text{{font-family:Arial,Helvetica,sans-serif}}.mono{{font-family:Menlo,Consolas,monospace}}.trace{{stroke-dasharray:1800;animation:draw 8s ease-in-out infinite}}@keyframes draw{{0%{{stroke-dashoffset:1800}}65%,100%{{stroke-dashoffset:0}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<defs><linearGradient id="gradient"><stop stop-color="{THEME['lavender']}"/><stop offset=".5" stop-color="{THEME['pink']}"/><stop offset="1" stop-color="{THEME['sky']}"/></linearGradient></defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{THEME['background']}" stroke="{THEME['border']}"/>{body}</svg>\n'''

def text(x, y, value, size=16, color=None, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color or THEME["text"]}" {extra}>{escape(str(value))}</text>'

def render(data):
    user = data['user']
    calendar = user['contributionsCollection']['contributionCalendar']
    weeks = calendar['weeks']
    days = [d for week in weeks for d in week['contributionDays']]
    date_range = f"{days[0]['date']} — {days[-1]['date']}"
    body = text(32, 40, 'GITHUB / THE BUILD LOG', 13, THEME['lavender'], 'class="mono"')
    body += text(32, 66, date_range, 12, THEME['muted'])
    values = [(f"{calendar['totalContributions']:,}", 'Contributions in this period'),
              (f"{user['repositories']['totalCount']:,}", 'Public repositories'),
              (f"{sum(d['contributionCount'] > 0 for d in days):,}", 'Days with contributions')]
    for i, (value, label) in enumerate(values):
        x = 32 + i * 320
        body += text(x, 132, value, 44, THEME['lavender'], 'font-weight="bold"')
        body += text(x, 163, label, 15, THEME['muted'])
    weekly = [sum(d['contributionCount'] for d in week['contributionDays']) for week in weeks]
    peak = max(weekly) or 1
    points = [(32 + i * 936 / max(1, len(weekly)-1), 270 - v / peak * 65) for i,v in enumerate(weekly)]
    path = 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x,y in points)
    body += '<path d="M32 270H968" stroke="#49345f"/>'
    body += f'<path class="trace" d="{path}" stroke="url(#gradient)" stroke-width="3" fill="none"/>'
    body += text(32, 300, 'Weekly contribution activity · last 12 months', 12, THEME['muted'])
    body += text(968, 300, f'Updated {datetime.now(timezone.utc):%Y-%m-%d} UTC', 11, THEME['muted'], 'text-anchor="end"')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'activity.svg').write_text(svg(1000,325,'GitHub activity based on real contribution data. '+date_range,body))
    # Compact stats keep labels legible on mobile; the full graph remains linked.
    compact = text(24,34,'GITHUB / THE BUILD LOG',14,THEME['lavender'],'class="mono"')
    compact += text(24,60,date_range,13,THEME['muted'])
    for i,(value,label) in enumerate(values):
        compact += text(24,111+i*57,value,28,THEME['lavender'],'font-weight="bold"')
        compact += text(150,108+i*57,label,15,THEME['muted'])
    (OUT/'activity-mobile.svg').write_text(svg(500,260,'GitHub contribution summary. '+date_range,compact))
    heat = text(32,36,'A YEAR, ONE COMMIT AT A TIME',13,THEME['lavender'],'class="mono"')
    palette=THEME['contributions']
    levels=['NONE','FIRST_QUARTILE','SECOND_QUARTILE','THIRD_QUARTILE','FOURTH_QUARTILE']
    for col,week in enumerate(weeks):
        for day in week['contributionDays']:
            row=(datetime.fromisoformat(day['date']).weekday()+1)%7
            color=palette[levels.index(day['contributionLevel'])]
            heat+=f'<rect x="{32+col*17.5}" y="{60+row*18}" width="13" height="13" rx="3" fill="{color}"><title>{day["date"]}: {day["contributionCount"]} contributions</title></rect>'
    heat += text(32,211,date_range,12,THEME['muted'])
    for i,color in enumerate(palette):
        heat+=f'<rect x="{852+i*20}" y="196" width="13" height="13" rx="3" fill="{color}"/>'
    (OUT/'contributions.svg').write_text(svg(1000,235,'Contribution calendar. '+date_range,heat))
    for key in ['nodebase','portfolio']:
        repo=data[key]
        body=text(26,40,'↗  '+repo['name'],24,THEME['lavender'],'font-weight="bold"')
        description=repo['description'] or 'Explore the code, commits, and project details on GitHub.'
        lines=textwrap.wrap(description,width=48)
        for i,line in enumerate(lines[:3]):
            if i==2 and len(lines)>3: line=line.rstrip('.')+'…'
            body+=text(26,80+i*23,line,15,THEME['muted'])
        language=(repo.get('primaryLanguage') or {}).get('name','Code')
        body+=text(26,182,f"{language}   ·   {repo['stargazerCount']} stars   ·   {repo['forkCount']} forks",13,THEME['pink'])
        (OUT/f'{key}.svg').write_text(svg(500,210,repo['name']+' GitHub repository',body))

if __name__ == '__main__':
    result = subprocess.run(['gh','api','graphql','-f',f'query={QUERY}'],check=True,capture_output=True,text=True,timeout=60)
    payload = json.loads(result.stdout)
    if payload.get('errors'):
        raise SystemExit('GitHub returned GraphQL errors; existing assets retained.')
    render(payload['data'])
