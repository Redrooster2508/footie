---
tags: [photos]
---
# Team photos

Team photos are freely licensed (Wikimedia Commons), taken in 2023 or later, reviewed by eye and credited under the photo; they're listed in `photos/manifest.json`. A team without one shows the drawn men's squad in its colours. Picked on 2026-11-13 (women's session log, section 43) and brought here in build 3.

The women's site's rules: freely licensed, 2023 or later, reviewed by eye on contact sheets and checked at the 16:10 card crop. Searched: the 66 clubs in the Premier League, LaLiga and men's Champions League, and the 48 teams at the 2026 World Cup. **32 picked**: 12 clubs (Arsenal, Bournemouth, Brentford, Crystal Palace, Everton, Fulham, Hull, Leeds, Nottingham Forest, Sunderland, Inter, Real Sociedad) and 20 national teams (mostly 2026 World Cup starting XIs: Argentina, Australia, Belgium, Brazil, Canada, Colombia, Croatia, Ecuador, Egypt, France, Germany, Ghana, Japan, Norway, Panama, Portugal, Saudi Arabia, Scotland, Spain (World Cup winners' celebration), Uzbekistan). Licences: CC BY-SA 4.0 (19), CC BY 4.0 (6), CC0 (5), CC BY 2.0, public domain.

**Tool:** `tools/photo_candidates.py` (written for the women's repo as `men_photo_candidates.py`, moved here on 2026-11-23) finds each team's Commons category through Wikidata (club classes `Q476028` and `Q103229495`, FC Barcelona uses the newer one; national team classes `Q6979593` and the men's `Q135408445`, which most men's national teams now use), follows season, match, celebration and group-photo sub-folders, and searches titles. It skips women's, youth, B and reserve sides, other sports (basketball, handball, hockey) and the Copa de la Reina, and keeps at most two photos of one series. `--sheets` makes the contact sheets. Pick with `tools/fetch_photos.py --pick <team id>="File:..."`; the working files (`tools/candidates.json`, `tools/sheets/`) aren't in git.

**Rejected on review:** the opponent's line-up filed under this team's name was the most common trap (England's results were Ghana's and Panama's XIs, Uruguay's were Saudi Arabia's, Porto's were Salzburg's, Osasuna's were Bordeaux players, Málaga's was Las Palmas); also Manchester City's under-18s, Sweden's women, Paraguay's women's under-17s, a 1916 USA team, and two that didn't work at card size (Napoli, blurry; Bayern's title celebration, players too small on the balcony). Chelsea's only team photo has a politician front and centre.

**No photo yet:** most big clubs (Chelsea, Liverpool, both Manchester clubs, Real Madrid, Barcelona, Atlético, PSG, Bayern, Dortmund…) and 28 World Cup teams, including England, the USA, Mexico, the Netherlands and Morocco. They keep the drawn squad. Openverse/Flickr wasn't searched for men's teams yet.
