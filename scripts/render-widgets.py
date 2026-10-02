"""Publish only available widget assets and explicitly configured personal feeds."""
from pathlib import Path
from html import escape
import os
import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
ROOT=Path(__file__).resolve().parents[1]
START='<!--START_SECTION:extensions-->'
END='<!--END_SECTION:extensions-->'

def section(root, feed_url='', spotify_url=''):
    blocks=[]
    def exists(name):return (root/'assets/widgets'/name).is_file()
    if exists('lavender-city.svg') and exists('lavender-city-static.svg'):
        blocks.append('''### A year in lavender / 3D contribution city

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/widgets/lavender-city-static.svg" />
  <img src="assets/widgets/lavender-city.svg" width="100%" alt="A 3D lavender city built from my GitHub contribution calendar, with contribution and language summaries." />
</picture>

<sub>Generated with <a href="https://github.com/yoshi389111/github-profile-3d-contrib">GitHub Profile 3D Contrib</a>.</sub>''')
    if exists('galaga.svg'):
        blocks.append('''### Insert commit, start game / Galaga

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/github/contributions.svg" />
  <img src="assets/widgets/galaga.svg" width="100%" alt="A Galaga-style spaceship turns my real GitHub contributions into an animated arcade scene." />
</picture>

<sub>Contribution replay powered by <a href="https://github.com/abozanona/pacman-contribution-graph">Arcade Contribution Graph</a>.</sub>''')
    if exists('metrics.svg'):
        blocks.append('''### The code behind the craft

<img src="assets/widgets/metrics.svg" width="100%" alt="GitHub Metrics: most-used languages and notable public contributions." />

<sub>Public repository language composition, not a measure of expertise. Generated with <a href="https://github.com/lowlighter/metrics">Metrics</a>.</sub>''')
    posts=root/'assets/feeds/posts.md'
    if feed_url and posts.exists():
        content=posts.read_text()
        content=content.split('<!-- BLOG-POST-LIST:START -->')[-1].split('<!-- BLOG-POST-LIST:END -->')[0].strip()
        if content:
            blocks.append('## ✎ 07 / Field notes\n\nLatest writing and videos.\n\n'+content)
    if spotify_url:
        parts=urlsplit(spotify_url)
        if parts.scheme!='https' or not parts.hostname or parts.username or parts.password:
            raise ValueError('SPOTIFY_WIDGET_URL must be a public HTTPS widget URL without credentials.')
        query=dict(parse_qsl(parts.query));query.update(theme='dark',spin='true',eq_color='c4b5fd')
        url=escape(urlunsplit(parts._replace(query=urlencode(query))))
        static=dict(query);static['spin']='false'
        reduced=escape(urlunsplit(parts._replace(query=urlencode(static))))
        blocks.append(f'''## ♫ 08 / After hours

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="{reduced}" />
  <img src="{url}" width="480" alt="My Spotify listening card: the currently playing or most recently played track." />
</picture>

<sub>Powered by <a href="https://github.com/tthn0/Spotify-Readme">Spotify Readme</a>.</sub>''')
    return '\n\n'.join(blocks)

if __name__=='__main__':
    path=ROOT/'README.md';readme=path.read_text()
    if readme.count(START)!=1 or readme.count(END)!=1:
        raise ValueError('README widget markers must occur exactly once.')
    body=section(ROOT,os.getenv('PROFILE_BLOG_FEED',''),os.getenv('SPOTIFY_WIDGET_URL',''))
    begin=readme.index(START)+len(START);end=readme.index(END)
    path.write_text(readme[:begin]+'\n\n'+body+'\n\n'+readme[end:])
