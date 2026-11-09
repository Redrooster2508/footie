#!/usr/bin/env python3
"""Save hand-picked, freely licensed team photos from Wikimedia Commons for the site.

Every photo is chosen by a person after looking at it; this script never picks one by itself.
It checks the licence (CC BY / CC BY-SA / CC0 / public domain) and that the photo was taken in
2023 or later, downloads a 1280px copy to photos/<espn team id>.<ext>, and records the photographer
and licence in photos/manifest.json (the site shows that credit under the photo, as the licences require).

Usage:
  python3 tools/fetch_photos.py --pick 359="File:Arsenal team 2025.jpg"   # use this exact Commons file
  python3 tools/fetch_photos.py --skip 359                                # remove a team's photo (keeps the illustration)
"""
import html, json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS = os.path.join(ROOT, "photos")
MANIFEST = os.path.join(PHOTOS, "manifest.json")
SINCE = 2023  # photos taken before this year show old squads and kits
UA = "MatchdayHub/1.0 (men's football; https://github.com/Redrooster2508/footie)"
LEAGUES = ["eng.1", "esp.1", "uefa.champions"]
OK_LICENCE = re.compile(r"^(cc[ -]by(-sa)?([ -][\d.]+)?|cc0|public domain|pd)", re.I)


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def teams():
    seen = {}
    for slug in LEAGUES:
        d = json.loads(get(f"https://site.api.espn.com/apis/v2/sports/soccer/{slug}/standings"))
        for e in d["children"][0]["standings"]["entries"]:
            t = e["team"]
            seen.setdefault(str(t["id"]), {"id": str(t["id"]), "name": t["displayName"], "league": slug})
    return list(seen.values())


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def credit(page):
    meta = (page.get("imageinfo") or [{}])[0].get("extmetadata", {})
    artist = plain(meta.get("Artist", {}).get("value")) or "Unknown author"
    artist = re.sub(r"\s+", " ", artist)[:80]
    return artist, plain(meta.get("LicenseShortName", {}).get("value"))


def save(man, tid, team_name, page):
    """Download a page's 1280px rendition to photos/<tid> and record its credit."""
    ii = page["imageinfo"][0]
    url = ii.get("thumburl") or ii["url"]
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp"):
        ext = ".jpg"
    for old in os.listdir(PHOTOS):
        if os.path.splitext(old)[0] == tid:
            os.remove(os.path.join(PHOTOS, old))
    fname = tid + ext
    data = get(url)
    with open(os.path.join(PHOTOS, fname), "wb") as f:
        f.write(data)
    artist, lic = credit(page)
    man[tid] = {"file": fname, "team": team_name, "credit": f"{artist}, {lic}, via Wikimedia Commons", "source": ii.get("descriptionurl", "")}


def pick(man, choices):
    """--pick id="File:Title" ...: use exactly these Commons files."""
    names = {t["id"]: t["name"] for t in teams()}
    for c in choices:
        if "=" not in c:
            print(f"  expected id=\"File:...\", got {c!r}"); continue
        tid, title = c.split("=", 1)
        p = {"action": "query", "format": "json", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": "1280"}
        page = next(iter(json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))["query"]["pages"].values()))
        if "imageinfo" not in page:
            print(f"  not found  {title}"); continue
        meta = page["imageinfo"][0].get("extmetadata", {})
        lic = plain(meta.get("LicenseShortName", {}).get("value"))
        if not OK_LICENCE.search(lic):
            print(f"  refused (licence {lic!r})  {title}"); continue
        years = [int(y) for y in re.findall(r"(?<!\d)(20[0-3]\d)(?!\d)", plain(meta.get("DateTimeOriginal", {}).get("value")) or title)]
        if not years or max(years) < SINCE:
            print(f"  refused (taken {max(years) if years else 'on an unknown date'}, before {SINCE})  {title}"); continue
        save(man, tid, names.get(tid, tid), page)
        print(f"  saved  {names.get(tid, tid):<26} {title[:70]}")
        time.sleep(0.3)


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ("--pick", "--skip"):
        print(__doc__); return
    os.makedirs(PHOTOS, exist_ok=True)
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    if args[0] == "--skip":
        for sid in args[1:]:
            for old in os.listdir(PHOTOS):
                if os.path.splitext(old)[0] == sid:
                    os.remove(os.path.join(PHOTOS, old))
            man[sid] = None
    else:
        pick(man, args[1:])
    with open(MANIFEST, "w") as f:
        json.dump(man, f, indent=1, ensure_ascii=False, sort_keys=True)


if __name__ == "__main__":
    main()
