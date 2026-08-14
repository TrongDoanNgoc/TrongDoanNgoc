#!/usr/bin/env python3
"""Fill README WakaTime section from /users/current/summaries (stats API lags on free plans)."""

from __future__ import annotations

import base64
import collections
import json
import os
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

START = "<!--START_SECTION:waka-->"
END = "<!--END_SECTION:waka-->"
LANG_COUNT = 8
BAR_WIDTH = 24
README = Path("README.md")


def fmt_time(seconds: float) -> str:
    total = int(round(seconds))
    hours, rem = divmod(total, 3600)
    minutes = rem // 60
    if hours and minutes:
        return f"{hours} hrs {minutes} mins"
    if hours:
        return f"{hours} hrs"
    return f"{minutes} mins"


def bar(percent: float) -> str:
    filled = min(BAR_WIDTH, max(0, round(percent / 100 * BAR_WIDTH)))
    return "█" * filled + "░" * (BAR_WIDTH - filled)


def fetch_summaries(api_key: str) -> dict:
    token = base64.b64encode(f"{api_key}:".encode()).decode()
    req = urllib.request.Request(
        "https://wakatime.com/api/v1/users/current/summaries?range=last_7_days",
        headers={"Authorization": f"Basic {token}"},
    )
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=30) as res:
        return json.loads(res.read().decode())


def build_block(payload: dict) -> str:
    days = payload.get("data") or []
    langs: collections.Counter[str] = collections.Counter()
    for day in days:
        for lang in day.get("languages") or []:
            langs[lang["name"]] += float(lang.get("total_seconds") or 0)

    total = sum(langs.values())
    start = payload.get("start")
    end = payload.get("end")
    try:
        start_s = datetime.fromisoformat(start.replace("Z", "+00:00")).strftime("%d %B %Y")
        end_s = datetime.fromisoformat(end.replace("Z", "+00:00")).strftime("%d %B %Y")
        title = f"From: {start_s} - To: {end_s}"
    except Exception:
        title = "Last 7 days"

    if total <= 0:
        body = "No coding activity this week."
    else:
        lines = [
            title,
            "",
            f"Total Time: {fmt_time(total)}",
            "",
        ]
        top = langs.most_common(LANG_COUNT)
        name_w = max(len(name) for name, _ in top)
        time_w = max(len(fmt_time(secs)) for _, secs in top)
        for name, secs in top:
            pct = secs / total * 100
            lines.append(
                f"{name:<{name_w}}   {fmt_time(secs):<{time_w}} {bar(pct)}   {pct:5.2f} %"
            )
        body = "\n".join(lines)

    return f"{START}\n```text\n{body}\n```\n{END}\n"


def main() -> None:
    api_key = os.environ.get("WAKATIME_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("WAKATIME_API_KEY is missing")

    payload = fetch_summaries(api_key)
    block = build_block(payload)
    readme = README.read_text()
    if START not in readme or END not in readme:
        raise SystemExit("Waka markers not found in README.md")

    start_i = readme.index(START)
    end_i = readme.index(END) + len(END)
    updated = readme[:start_i] + block.rstrip() + readme[end_i:]
    if not updated.endswith("\n"):
        updated += "\n"
    README.write_text(updated)
    print("README WakaTime section updated")


if __name__ == "__main__":
    main()
