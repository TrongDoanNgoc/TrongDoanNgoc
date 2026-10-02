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
