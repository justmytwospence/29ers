# 29ers.com

A pixel-perfect **parody** of [14ers.com](https://www.14ers.com) — the Colorado fourteeners
site — rebuilt for the tallest mountains in the *solar system*. Same look, same layout, same
fonts and colors; only the content is different.

Instead of Colorado's 14,000-foot peaks, 29ers.com ranks **every mountain in the solar system
that out-tops Mount Everest**. A **29er** is any peak that rises at least ~29,000 ft base-to-summit
— the height of Everest itself (29,032 ft), Earth's tallest. All **13** qualify, from **Olympus
Mons** (Mars) and **Rheasilvia** (Vesta) — tied as the solar system's tallest at ~72,000 ft — down
through Earth's own Hawaiian giants **Mauna Kea** and **Mauna Loa**. The lone exception is **Mount
Everest**: the world's most famous peak makes the list only on its 29,032 ft *above sea level* —
measured base-to-peak like everything else it falls well short, so it carries an asterisk.

## Live

**https://29ers.vercel.app**

## Run it locally

The CSS uses root-relative asset paths, so serve from this folder:

```
cd 29ers
python3 -m http.server 8029
# open http://localhost:8029/
```

Everything is self-hosted — peak photos, stylesheets and site chrome all live in this repo — so
the site works offline apart from two web fonts: Roboto (Google Fonts) and Font Awesome (cdnjs).

`python3 build.py` regenerates every page from the peak data at the top of the script. Edit
`build.py`, never the generated `*.html`.

## Files

- `index.html` — the home page (faithful clone of 14ers.com's landing page: hero, marketing sections, recent-activity panel)
- `peaks.html` — the ranked list of all 13 peaks (clone of 14ers.com's `/14ers` list page)
- `about.html` — "What are 29ers?" explainer
- `<peak>.html` — a detail page per peak (olympus-mons, rheasilvia, iapetus-ridge, boosaule-montes,
  ascraeus-mons, ionian-mons, elysium-mons, arsia-mons, maxwell-montes, euboea-montes, mauna-kea, mauna-loa,
  mount-everest) — stats sidebar, photos, routes, weather, and a per-body history section
- `css/` — 14ers.com's stylesheets, kept as-is except for asset paths repointed at `images/vendor/`
- `css/29ers.css` — the handful of rules this parody adds on top of them
- `images/vendor/` — the site-chrome images those stylesheets reference, served locally rather
  than hotlinked from 14ers.com
- `images/site_logo.svg` — the 14ers logo recreated as "29ers.com" (Lilita One + eroded-edge filter)
- `images/peaks/` — locally bundled, resized NASA/Wikimedia photos (public domain / CC, credited on-page)
- `app.js` — sorting, tabs, mobile menu, read-more
- `fonts/`, `build.py` — logo font + the data-driven page generator (`python3 build.py` rebuilds all pages)

## Disclaimer

This is a non-commercial parody / fan tribute. Not affiliated with 14ers.com or 14ers Inc.
The mountains are real; the website is a joke. Image credits are shown on each peak page
(NASA/JPL public domain except Mauna Kea © Vadim Kurland CC BY 2.0 and Everest © shrimpo1967/PLW2
CC BY-SA 2.0). The homepage hero is Olympus Mons's western scarp by ESA/DLR/FU Berlin (CC BY-SA 3.0 IGO).
