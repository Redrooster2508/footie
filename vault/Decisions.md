---
tags: [decisions]
---
# Decisions

| Date | Decision | Why |
|---|---|---|
| 2026-11-09 | Separate repo, copied from the women's site | The user wanted the same site for men's football, kept apart from the women's |
| 2026-11-09 | **Premier League, LaLiga, Champions League** | The user's choice |
| 2026-11-09 | **National teams** (user's request): friendlies, World Cup 2026, UEFA and Concacaf Nations Leagues, UEFA World Cup play-offs, AFCON and its qualifying, Asian Cup and its qualifying | The competitions ESPN has men's matches for in 2026, plus the Asian Cup (January 2027) |
| 2026-11-09 | First national-team build run locally, not in the workflow | About 720 matches; the workflow has a 30-minute limit. Later runs only add new matches |
| 2026-11-09 | Storage keys prefixed `mmh-` (women's site: `wmh-`) | Both sites live on `redrooster2508.github.io`, so they share browser storage; separate keys keep their settings and update checks apart |
| 2026-11-09 | `fetch_photos.py` only saves hand-picked photos | The copied script auto-picked when run without options; on the women's site that downloaded unreviewed photos by accident |
| 2026-11-09 | Same photo rules as the women's site | Freely licensed, credited, taken 2023 or later; no club, agency or news photos |
| 2026-11-09 | No neural network | Bookmaker odds and a Poisson goals model, as on the women's site |
