# Profile artwork

The profile uses self-contained SVG images: aurora layers, rotating flowers,
constellations, floating devices, chart traces, a typing terminal, and wave dividers.
Desktop and mobile compositions are selected with GitHub-supported `<picture>`
elements. CSS animations respect `prefers-reduced-motion`; explicit static SVG fallbacks
are also selected by `<picture>` for browsers that do not forward motion preferences
to embedded SVGs. Regenerate these with `python3 scripts/build-static.py`. The snake switches
to the static contribution calendar when reduced motion is enabled.

## Lavender palette

`assets/theme.json` supplies the generated GitHub cards. Hand-authored SVG artwork
uses the same palette: lavender `#c4b5fd`, pink `#f0abfc`, sky `#89ddff`, background
`#171122`, readable text `#f5f0ff`, and muted text `#c7bddb`.
Update the SVG colors and workflow snake palette alongside the JSON when retheming.

## Daily GitHub artwork

`.github/workflows/profile-art.yml` runs daily at 01:25 UTC, on manual dispatch,
and when its source changes. The generation job has read-only repository access;
the separate publishing job can only publish the resulting SVG files.

- `python3 scripts/update-profile.py` uses authenticated `gh api graphql` to render
  real contribution counts, a weekly activity graph, an original contribution
  calendar, and the two repository cards. Locally, use an existing `gh` login;
  Actions uses its short-lived `GH_TOKEN`. No personal token is passed to the snake
  dependency.
- The pinned Platane/snk action renders the contribution snake with the lavender
  palette using the generation job's read-only token.
- `python3 scripts/finish-snake.py` adds an accessible title and reduced-motion CSS.
- Generated SVGs are committed to `assets/github/`. Existing files keep rendering
  if an API call or an Actions run fails. Cards show their contribution date range.

The first committed snake image is the real static contribution calendar as a
fallback until Actions generates its animated replacement.

The existing WakaTime workflow and README markers remain independent.
Shields.io contact badges and skillicons.dev icons are decorative enhancements;
contact links and the text toolkit remain usable without those services.

Upstream snake generator: https://github.com/Platane/snk (MIT license).

## Profile extensions

`profile-widgets.yml` generates the 3D contribution city, Galaga replay, and
Lowlighter Metrics in separate read-only jobs, then publishes their artifacts.
The contribution city has a separately generated static version; Galaga falls
back to the contribution calendar for reduced motion. The README renderer only
embeds files that exist. Snake remains available in a collapsible section.

Two personal integrations need account-specific configuration in repository
**Settings → Secrets and variables → Actions → Variables**:

- `PROFILE_BLOG_FEED`: your RSS/Atom URL (or comma-separated feeds). Blog Post
  Workflow imports up to four posts into `assets/feeds/posts.md`. The README shows
  the section only after real posts have been imported.
- `SPOTIFY_WIDGET_URL`: the HTTPS root URL of your deployed
  [Spotify Readme](https://github.com/tthn0/Spotify-Readme) instance. The renderer
  applies a dark theme, lavender equalizer, and spinning-disc option. A Spotify
  profile URL is not a widget URL. Upstream now hosts on PythonAnywhere, whose
  free web apps must be renewed monthly. Since Spotify's February 2026 API changes,
  the developer dashboard only enables Web API for Premium accounts, so both live
  playback and pinned tracks (`https://{user}.pythonanywhere.com/{TRACK_ID}`)
  need a Premium account to create the app. Keep OAuth credentials in
  your hosting provider's secrets, never in this repository or its public URL.

After configuring either variable, run **Profile extensions → Run workflow**.
Unconfigured personal sections remain absent instead of showing someone else's
content or a broken widget. The widget's `spin=false` setting disables the disc
for reduced motion; the upstream equalizer may still animate.

Upstreams: [3D Contrib](https://github.com/yoshi389111/github-profile-3d-contrib),
[Arcade Contribution Graph](https://github.com/abozanona/pacman-contribution-graph),
[Metrics](https://github.com/lowlighter/metrics),
[Blog Post Workflow](https://github.com/gautamkrishnar/blog-post-workflow), and
[Spotify Readme](https://github.com/tthn0/Spotify-Readme).
