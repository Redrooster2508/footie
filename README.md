# Matchday Hub (men's football)

Live scores, match statistics, win probabilities, season forecasts and player stats for the **Premier League**, **LaLiga**, **Champions League** and **national teams** (friendlies, the 2026 World Cup, UEFA and Concacaf Nations Leagues, World Cup and Africa Cup of Nations qualifying, the Africa Cup of Nations, and the Asian Cup and its qualifiers).

**Live site:** https://redrooster2508.github.io/footie/ (add `#pl`, `#laliga` or `#ucl` to open one competition)

The men's sister site of the [Women's Matchday Hub](https://redrooster2508.github.io/wosomatchday/), built from the same code.

A static site with no build step and no server. Visitors' browsers read ESPN's public soccer feed directly, every 30 seconds while a match is live. The player stats database is a set of JSON files in this repository, rebuilt from finished matches by a script.

Project notes, decisions and the change log are in the Obsidian vault in [`vault/`](vault/). Open that folder as a vault in Obsidian, or read the Markdown files on GitHub.

## What it shows

| Section | What's in it |
|---|---|
| Matches | Each match on the selected matchday: live score and clock, plus a home/draw/away probability bar. The arrows jump between matchdays. Times are in the viewer's own time zone, which is named on the page. |
| Match centre | Team photos with crests; win, draw and loss chances with fair odds; expected goals; a final-score probability grid; over/under, both teams to score and clean sheets; win probability by minute; match stats; **touch heatmap**, **progressive pass map** and **shot map** for either team or any player, a **goal-mouth chart**, updating every minute while live; **head to head** (earlier league meetings, last five seasons); line-ups with each player's numbers; the event timeline |
| News | The five latest ESPN stories for the competition (stories about the women's game that turn up in the feed are filtered out) |
| Season forecast | Predicted winner and each team's chance of the title and each table zone, from 10,000 simulations of the remaining fixtures |
| Bracket | Champions League knockouts with title chances, projected from the league-phase table until they start (1st–8th to the round of 16, 9th–24th to the knockout play-offs) |
| League table | Standings with qualification and relegation zones, goals scored and conceded per game |
| Player stats | Season table for every player: search, club and position filters, sortable columns |
| Player stats | (also) minutes, goals per 90, goals + assists per 90, progressive passes |
| Player pages | `player.html?l=<league>&id=<ESPN player id>`: portrait, profile (with birthplace), career history (clubs and national teams from Wikidata), season numbers with minutes and per-90 rates, league percentiles per 90, a per-match chart, season heatmap, shot map, progressive pass map and goal mouth, and the match log with minutes |
| Team pages | `team.html?l=<league>&id=<ESPN team id>`: photo, record and form, season forecast, results and fixtures, squad with minutes and per-90, team heatmap, shots, passes and goal mouth, head to head against any opponent |

## Files

| File | Purpose |
|---|---|
| `index.html`, `styles.css` | The hub page and all styles (light and dark themes) |
| `app.js` | Loads the feed, polls during live matches, renders the hub |
| `model.js` | Probability model: pure functions, testable without a browser |
| `tools/build_forecast.py` | Season forecasts (`data/<league>/forecast.json`) |
| `bracket.js` | Knockout bracket, title chances, pre-knockout projection |
| `players.js` | Player stats table and match-centre line-ups |
| `team.html`, `team-page.js` | Team pages |
| `h2h.js` | Head to head from ESPN team schedules |
| `heat.js` | Pitch drawing, touch heatmaps and shot maps from play-by-play |
| `player.html`, `player-page.js` | Individual player pages |
| `photos.js` | Team photos: uploaded, shared (`photos/manifest.json`) or illustrated |
| `data/<league>/` | Player stats database (`players.json`, `matches.json`, `heat.json`) |
| `photos/` | Shared team photos and `manifest.json` with credits |
| `tools/` | Scripts that build the database and find photos |
| `vault/` | Obsidian vault: project notes and change log |

## How the probabilities work

1. **Market rates.** When bookmaker moneyline odds are listed, the margin is removed and two goal rates are fitted so a Poisson model reproduces the market's home and away win chances.
2. **Form rates.** When odds are missing, the rates come from goals scored and conceded per game against the league average. They're shrunk toward average early in the season and include home advantage.
3. **Scorelines.** Poisson goals with the Dixon–Coles low-score correction (ρ = −0.08).
4. **In play.** Only the time left is simulated, on top of the current score, assuming 96 minutes including stoppage time. A red card cuts that side's rate by 25% and raises the opponent's by 15%.
5. **Season forecasts.** `tools/build_forecast.py` plays out every remaining fixture 10,000 times. Team strength comes from this season's goals, eased toward average by 8 games' worth of league-average form, with home advantage and a per-simulation strength spread (σ = 0.15 on a log scale) to allow for uncertainty.
6. **National teams.** Many internationals have no odds, so teams are rated on goals for and against in every international match this year in the database.
7. **Brackets.** Title chances combine each tie's chance to advance through the bracket. A level score after 90 minutes is split by relative strength.

"Draw" always means level after 90 minutes.

## Player stats database

`tools/build_players.py` reads every finished match of the current season from ESPN's match sheets and writes, for each competition:

- `data/<league>/matches.json`: every finished match, with each player's line (goals, assists, shots, shots on target, saves, goals conceded, cards, fouls, own goals)
- `data/<league>/players.json`: season totals per player, plus club names, logos and colours

`tools/build_heat.py` then reads each match's play-by-play (about 1,500 events with pitch coordinates) and writes `data/<league>/heat.json`: each player's touches on a 24 × 16 grid in his attacking direction; every shot with its spot, outcome and where it crossed the goal line; passes and **progressive passes** (ending at least 25% closer to goal, in the attacking half; corners and passes ending on the goal line excluded; ESPN doesn't mark completed passes, so these are attempts); and **minutes played**, from the starting XI, substitutions and red cards. It also writes a small `data/<league>/minutes.json` for the player table.

Both only fetch matches they haven't stored yet.

```sh
python3 tools/build_players.py              # every competition, clubs and national teams
python3 tools/build_players.py esp.1        # one competition
python3 tools/build_players.py --rebuild    # read every match again
python3 tools/build_heat.py                 # season heatmaps (after build_players)
```

**Automatic updates:** the **Update player stats** workflow (`.github/workflows/players.yml`, added on GitHub's website) runs every three hours: it rebuilds player stats, heatmaps and forecasts, and commits only if something changed. Run it by hand from the repository's **Actions** tab.

## Photos

**Team photos.** The match centre shows the first of these that exists:

1. A photo the viewer uploaded. This is saved only in their own browser.
2. A shared photo listed in `photos/manifest.json`. Every visitor sees these.
3. An illustrated squad line-up in the club's colours.

Shared photos are chosen by hand, after looking at them, and saved with:

```sh
python3 tools/fetch_photos.py --pick 359="File:Example.jpg"   # use this Commons file (checks licence and year)
python3 tools/fetch_photos.py --skip 359                      # remove a photo, keep the illustration
```

Each manifest entry can also set how the photo sits in the 16:10 card: `"pos": "50% 20%"` (focus point) or `"fit": "whole"` (show a tall photo whole, on a blurred copy).

**Player portraits.** A player page looks the player up on Wikidata. If he has a freely licensed portrait on Wikimedia Commons from 2023 or later, the page shows it; otherwise it shows his initials in club colours.

**Career history.** The same Wikidata item (matched on ESPN's date of birth, so a namesake isn't used) gives his birthplace and every team he has been registered with, through Wikidata's public query service (CC0 data). Appearances and goals are shown where Wikidata records them, with the date they were counted to. The data is community-edited, so it can be incomplete or behind.

**Recency.** Team photos must have been taken in **2023 or later**, going by the camera's recorded date or, failing that, a year in the title. Older photos show old squads and kits. `--pick` enforces this.

**Licences.** Every photo shows its photographer, licence and source site. Only freely licensed images are used: CC BY, CC BY-SA, CC0, public domain, and, because the site is non-commercial, CC BY-NC and CC BY-NC-SA. Crediting a photographer doesn't make a copyrighted photo free to use, so photos from club or news sites are not used.

## Run locally

```sh
python3 -m http.server 8000
# open http://localhost:8000/#pl
```

## Publishing

GitHub Pages serves the `main` branch root and lets browsers cache files for 10 minutes. On each release, raise the build number in three places: the `?v=` tags on CSS and JS links, the number at the end of the version-check script in `index.html`, `player.html` and `team.html`, and `version.json`. Pages that find a newer `version.json` reload themselves once.

## Data

ESPN's public APIs (`site.api.espn.com`, `site.web.api.espn.com`, `sports.core.api.espn.com` for play-by-play) supply scores, stats, line-ups, odds, standings, news and player profiles. It's unofficial and undocumented, so its fields can change without notice. Odds are shown for analysis only.
