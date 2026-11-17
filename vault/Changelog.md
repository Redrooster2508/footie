---
tags: [log]
---
# Changelog

Newest first. The narrative is in [[Log/2026-11-09]] and [[Log/2026-11-13]].

## 2026-11-17 · Player names in the match heatmap (build 4)
- Fix: the match centre's touch map could list players as "Player 158678" instead of their names (Caitlin Foord, London City v Arsenal). The names come with the match summary, which often arrives after the play-by-play was asked for, and the map kept the first, empty list of names. It now uses the newest one when the play-by-play arrives
- While the play-by-play loads, the panel says so instead of briefly saying the match has no pitch positions

## 2026-11-13 · Improvements from the women's site, new font, team photos (build 3)
- One page per team, whichever tab it's opened from: Arsenal's shows Premier League, Champions League and cup results and fixtures together, colour-coded and labelled by competition, with a forecast block for each competition and a squad, heatmaps and head to head covering all of them. National teams list fixtures from every competition
- New font: Archivo throughout, condensed for headings and tabs (replaces Big Shoulders Display and IBM Plex Mono)
- 32 teams have freely licensed team photos (12 clubs, 20 World Cup teams), reviewed by eye; the rest keep the drawn squad
- Player pages link to each competition the player is in, with appearances (Saka: Premier League 7, World Cup 7); a national team player's page names his club
- Phones: the tabs scroll in one row; wide tables show a shadow where there's more to scroll; compact head to head in the match centre; dark initials on pale team colours
- Match sheets stored as rows with names and teams once per file, heatmap spots as whole numbers: data 16 → 13 MB, identical season totals
- Fix: the Champions League forecast listed every zone twice (ESPN's own and the ones added for the women's table); now only ESPN's four

## 2026-11-09 · National teams (build 2)
- "National teams" tab with a competition picker: friendlies, World Cup 2026, UEFA and Concacaf Nations Leagues, UEFA World Cup play-offs, AFCON and its qualifying, Asian Cup and its qualifying
- Player database for them: 1,013 matches, with heatmaps; first build run locally

## 2026-11-09 · First version (build 1)
- Premier League, LaLiga and Champions League from ESPN's public feed: live scores and probabilities, match centre, tables, news, season forecasts, Champions League bracket and projection (1st–8th to the round of 16, 9th–24th to the play-offs)
- Player stats database, heatmaps, shot and pass maps, minutes and per-90, player pages with career history, team pages with head to head
- Copied from the women's site and adapted: men's squad illustrations, women's stories filtered from the news, male players on Wikidata, separate browser-storage keys (`mmh-`), manual-only photo script
