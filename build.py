#!/usr/bin/env python3
"""Generator for 29ers.com - a pixel-perfect 14ers.com spoof for the
solar system's tallest mountains. Data-driven: one template renders the
ranked list (index.html), an explainer (about.html), and a detail page
for each of the 13 peaks taller than (or, for Everest, equal to the floor of)
Mount Everest. Reuses 14ers.com's real CSS/markup; content is ours."""
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
FA = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"

# ---------- Wikimedia thumbnail helper (keeps heavy originals off the page) ----------
def thumb(url, w):
    pre = "https://upload.wikimedia.org/wikipedia/commons/"
    if not url.startswith(pre):
        return url
    rest = url[len(pre):]                 # e.g. 1/15/Ascraeus_Mons.png
    name = rest.rsplit("/", 1)[1]
    return f"{pre}thumb/{rest}/{w}px-{name}"

def head(title, css):
    links = "\n".join(f'<link rel="stylesheet" type="text/css" href="css/{c}">' for c in css)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1.0, user-scalable=yes">
<title>{title}</title>
{links}
<link rel="stylesheet" type="text/css" href="css/29ers.css">
<link rel="stylesheet" type="text/css" href="{FA}">
<link rel="icon" href="images/site_logo.svg" type="image/svg+xml">
</head>
<body class="MainText1">

<div id="pageoverlay" class="pageoverlay"></div>'''

# ---- shared masthead + mega-nav (cloned structure, solar-system content) ----
SITEHEADER = '''<div id="siteheader">
  <div id="siteheader-logo">
   <a target="_top" tabindex="-1" href="index.html" title="29ers.com Home"><img src="images/site_logo.svg" alt="logo" width="130" height="50"></a>
  </div>

  <div id="hamburger" class="hamburger-menu" onclick="menuExpand();return false">
   <span></span><span></span><span></span>
  </div>

</div>

  <div id="siteheader-login" tabindex="0">
   <a href="login.html" class="newLoginLink" title="Log In">Log In&nbsp;<span class="fas fa-sign-in-alt"></span></a>
  </div>

<div id="siteheader-menuwrap">
<ul><li class="menu_topitem"><a href="peaks.html">Explore Peaks</a><ul class="mm_submenu"><li><div class="mm_submenu_divwrap"><div class="mm_submenu_columnlist_div"><ul><li><a href="peaks.html">All Peaks</a></li><li><a href="olympus-mons.html">Olympus Mons</a></li><li><a href="rheasilvia.html">Rheasilvia</a></li><li><a href="mount-everest.html">Mount Everest</a></li><li><a href="about.html">What are 29ers?</a></li></ul></div></div></li></ul></li><li class="menu_topitem"><a href="routes.html">Routes &amp; Planning</a><ul class="mm_submenu"><li><div class="mm_submenu_divwrap"><div class="mm_submenu_columnlist_div"><ul><li class="mm_column_header"><span>Routes</span></li><li><a href="routes.html">29er Routes</a></li><li><a href="route-selector.html">Easiest 29ers</a></li><li><a href="route-selector.html">Routes by Difficulty</a></li><li><a href="route-selector.html">Routes by Risk Factor</a></li><li><a href="route-selector.html">Route Selection Tool</a></li><li><a href="gpx.html">GPX Library</a></li><li><a href="reception.html">Relay-Sat Reception</a></li><li><a href="climb-times.html">User Climb Times</a></li></ul></div><div class="mm_submenu_columnlist_div"><ul><li class="mm_column_header"><span>Getting Started</span></li><li><a href="climbing.html">Climbing 29ers</a></li><li><a href="faq.html">29er FAQ</a></li><li><a href="safety.html">Mountaineering Safety</a></li><li><a href="difficulty.html">Difficulty Rating System</a></li><li><a href="gear.html">Spacesuit &amp; Gear List</a></li><li><a href="aphelion.html">Climbing 29ers in Aphelion</a></li><li class="external-icon"><a href="https://mars.nasa.gov/">NASA Mars Exploration <i class="fas fa-external-link-alt"></i></a></li></ul></div><div class="mm_submenu_columnlist_div"><ul><li class="mm_column_header"><span>Weather</span></li><li><a href="weather.html">Summit Forecasts</a></li><li class="external-icon"><a href="https://mars.nasa.gov/weather/">InSight/MEDA Weather <i class="fas fa-external-link-alt"></i></a></li><li><a href="weather.html#dust">Dust Storm Tracker</a></li><li><a href="weather.html#conjunction">Solar Conjunction</a></li></ul></div><div class="mm_submenu_columnlist_div"><ul><li class="mm_column_header"><span>Mission App</span></li><li><div class="menu_promo_block"><a href="app.html"><img src="images/peaks/olympus-mons.jpg" style="width: 100% !important; height: auto !important; margin-bottom: 8px; border-radius:6px;"></a></div></li></ul></div></div></li></ul></li><li class="menu_topitem"><a href="conditions.html">Conditions &amp; Reports</a><ul class="mm_submenu"><li><div class="mm_submenu_divwrap"><div class="mm_submenu_columnlist_div"><ul><li><a href="conditions.html">Peak Conditions</a></li><li><a href="conditions.html#post">Post a Condition Update</a></li><li class="sep nomobile"></li><li><a href="landing-sites.html">Landing Sites &amp; Status</a></li><li><a href="landing-sites.html#post">Post a Status Update</a></li><li class="sep nomobile"></li><li><a href="trip-reports.html">Trip Reports</a></li></ul></div></div></li></ul></li><li class="menu_topitem"><a href="forum.html">Community</a><ul class="mm_submenu"><li><div class="mm_submenu_divwrap"><div class="mm_submenu_columnlist_div"><ul><li><a href="forum.html">Forum</a></li><li class="sep nomobile"></li><li><a href="checklists.html">User Checklists</a></li><li><a href="checklists.html#stats">Checklist Statistics</a></li><li class="sep nomobile"></li><li class="external-icon"><a href="https://spencerboucher.com" rel="noopener">Spencer Boucher <i class="fas fa-external-link-alt"></i></a></li></ul></div></div></li></ul></li><li class="menu_topitem"><a href="about.html">More</a><ul class="mm_submenu"><li><div class="mm_submenu_divwrap"><div class="mm_submenu_columnlist_div"><ul><li><a href="about.html">About 29ers.com</a></li><li><a href="support.html">Support</a></li><li><a href="store.html">29ers.com Store</a></li><li class="sep nomobile"></li><li><a href="contact.html">Contact Site Admin</a></li><li><a href="search.html">Search the Site</a></li><li class="sep nomobile"></li><li><a href="about.html">What are 29ers?</a></li></ul></div></div></li></ul></li></ul>
</div>
'''

FOOTER = '''<div id="sfooter">
  <div class="footer-row">
    <div class="footer-section">
      <h3>29ers.com</h3>
      <ul>
        <li><a tabindex="0" href="about.html">About</a></li>
        <li><a tabindex="0" href="support.html">Your Support</a></li>
        <li><a tabindex="0" href="search.html">Search the Site</a></li>
        <li><a tabindex="0" href="contact.html">Contact Site Admin</a></li>
        <li><a tabindex="0" href="privacy.html">Privacy</a></li>
      </ul>
    </div>
    <div class="footer-section">
      <h3>Creator</h3>
      <ul>
        <li><a tabindex="0" href="https://spencerboucher.com" rel="noopener"><span class="fas fa-globe"></span>&nbsp; Spencer Boucher</a></li>
        <li><a tabindex="0" href="https://www.14ers.com" rel="noopener"><span class="fas fa-mountain-sun"></span>&nbsp; The original: 14ers.com</a></li>
      </ul>
    </div>
    <div class="footer-section">
      <h3>Mission App</h3>
      <ul>
        <li><a tabindex="0" href="app.html">More info</a></li>
        <li><a tabindex="0" href="https://mars.nasa.gov/" rel="noopener">NASA Mars Exploration</a></li>
        <li><a tabindex="0" href="https://science.nasa.gov/dwarf-planets/vesta/" rel="noopener">NASA Vesta / Dawn</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-row" style="margin-bottom:10px;">
    <div class="copyright" style="line-height:1.6;">
        <a tabindex="0" href="about.html">&copy; 2026 29ers.com<sup>&reg;</sup></a>, 29ers Inc.<br>
        <span style="font-size:0.85em;opacity:0.85;">Not affiliated with 14ers.com or 14ers Inc. Imagery: NASA/JPL and Wikimedia (public domain / CC, credited per photo). Hero: Olympus Mons by ESA/DLR/FU Berlin (CC BY-SA 3.0 IGO).</span>
    </div>
  </div>
</div>

<script src="app.js"></script>
</body>
</html>'''

def page(filename, title, css, body):
    html = head(title, css) + "\n" + SITEHEADER + "\n" + body + "\n" + FOOTER + "\n"
    with open(os.path.join(ROOT, filename), "w") as f:
        f.write(html)
    print("wrote", filename, len(html), "bytes")

LIST_CSS = ["variables.css","colors.css","colorssiteheader.css","site.css","siteheader.css","sitefooter.css","14ers.css"]
PEAK_CSS = ["variables.css","colors.css","colorssiteheader.css","site.css","siteheader.css","sitefooter.css","peak.css","tabs.css","forecast.css"]
HOME_CSS = ["variables.css","colors.css","colorssiteheader.css","site.css","siteheader.css","sitefooter.css","homeindex_main.css"]

# ---------- per-body flavour (history-section name, weather, map link) ----------
BODY = {
 "Mars":    dict(ology="Marsology",    maplink=("NASA Mars Trek","https://trek.nasa.gov/mars/"),
   weather="Thin carbon-dioxide air (about 600 Pa at the datum, far less at these summits), daytime highs near &minus;20&deg;F that plunge below &minus;150&deg;F at night, and planet-girdling dust storms. A pressure suit is mandatory."),
 "Io":      dict(ology="Iology",       maplink=("NASA &ndash; Io","https://science.nasa.gov/jupiter/jupiter-moons/io/"),
   weather="No breathable air, sulfur-dioxide frost, 300 km-high volcanic plumes, and a lethal bath of Jovian radiation. Io is the most volcanically active world in the solar system."),
 "Venus":   dict(ology="Venusology",   maplink=("NASA Magellan","https://science.nasa.gov/mission/magellan/"),
   weather="The worst weather anywhere: a ~465&deg;C surface, 90+ atmospheres of crushing carbon dioxide, and clouds of sulfuric acid. Maxwell Montes is the &ldquo;coolest&rdquo; spot on the planet &mdash; a balmy ~380&deg;C."),
 "Vesta":   dict(ology="Vestology",    maplink=("NASA &ndash; Vesta","https://science.nasa.gov/dwarf-planets/vesta/"),
   weather="Airless and frigid (about &minus;190&deg;F in sunlight). Surface gravity is roughly 0.025 g, so a careless step could launch you toward escape velocity."),
 "Iapetus": dict(ology="Iapetology",   maplink=("NASA &ndash; Iapetus","https://science.nasa.gov/saturn/moons/iapetus/"),
   weather="Airless, about &minus;225&deg;F, and famously two-faced &mdash; one hemisphere is coal-black, the other bright ice. The equatorial ridge makes the whole moon look like a walnut."),
 "Earth":   dict(ology="Geology",      maplink=("Google Maps","https://www.google.com/maps"),
   weather="Actual weather! Wind, snow, and breathable air (less of it the higher you go). Comparatively hospitable &mdash; and, by solar-system standards, comparatively tiny."),
}

# ============================ THE 13 PEAKS (ranked by base-to-peak height) ============================
PEAKS = [
 dict(rank=1, slug="olympus-mons", name="Olympus Mons", body="Mars", bodykey="Mars",
   type="Shield volcano", is29er=True, ft=72000, ht="72,000 ft", km="~22 km base-to-peak (up to ~26 km / 85,000 ft on its west scarp)",
   coords="18.65&deg; N, 226.2&deg; E", location="Tharsis Montes (western Tharsis rise)",
   discovery="Confirmed by Mariner 9, 1971 (long known as the albedo feature &ldquo;Nix Olympica&rdquo;)",
   img="https://upload.wikimedia.org/wikipedia/commons/0/00/Olympus_Mons_alt.jpg", img_credit="NASA/JPL (Viking 1 orbiter mosaic)",
   img_desc="Olympus Mons from orbit, the six-caldera summit complex visible at center",
   img2="https://upload.wikimedia.org/wikipedia/commons/7/75/Olympus_Mons.jpeg", img2_credit="NASA/JPL/MSSS (Mars Global Surveyor)",
   img2_desc="The shield and its aureole; the volcano spans ~600 km, the size of Arizona",
   lead="Olympus Mons is the tallest mountain and largest volcano in the solar system. This colossal shield volcano on the Tharsis rise of Mars stands about 69,840&#39; above the Martian datum and rises as much as ~85,000&#39; (26 km) from the plains at its base &mdash; roughly two and a half times the height of Mount Everest above sea level.",
   more="The volcano spans about 600 km (370 mi), an area the size of Arizona, ringed by an escarpment up to 8 km (5 mi) tall. Its summit holds a complex of six nested calderas measuring 60&times;80 km and up to 3.2 km deep. The flanks slope at only ~5&deg; on average, so a climber would never see the whole mountain at once. It last erupted an estimated 25 million years ago and may still be episodically active.",
   facts=["Tallest mountain and largest volcano in the solar system","About 600 km (370 mi) across &mdash; the size of Arizona","Summit caldera complex: six nested craters, 60&times;80 km, up to 3.2 km deep","Ringed by a basal escarpment up to 8 km (5 mi) tall","Summit air pressure ~72 Pa, about 12% of Mars's average"],
   weather_note="Summit air pressure is only ~72 Pa. The volcano is so wide that its base curves below the horizon &mdash; you can't see the whole mountain from anywhere on it."),

 dict(rank=2, slug="rheasilvia", name="Rheasilvia", body="Vesta (asteroid)", bodykey="Vesta",
   type="Impact central peak", is29er=True, ft=72000, ht="72,000 ft", km="19&ndash;22 km above its base",
   coords="71.95&deg; S, 86.3&deg; E", location="South polar region of asteroid 4 Vesta",
   discovery="Spotted by Hubble (1997); mapped by NASA's Dawn spacecraft (2011)",
   img="https://upload.wikimedia.org/wikipedia/commons/5/51/Vesta_in_natural_color.jpg", img_credit="NASA/JPL-Caltech/UCLA/MPS/DLR/IDA (Dawn)",
   img_desc="Vesta in natural color; the Rheasilvia basin and its central peak dominate the southern hemisphere",
   lead="Rheasilvia is the central peak of an enormous impact crater at the south pole of asteroid 4 Vesta. Rising 19&ndash;22 km (up to ~72,000&#39;) above its base, it is tied with Olympus Mons as the tallest mountain in the solar system &mdash; and it sits on a body only ~525 km across.",
   more="The Rheasilvia basin is 505 km (314 mi) wide &mdash; about 90% of Vesta's diameter &mdash; with a floor some 13 km below the surrounding terrain and an escarpment 4&ndash;12 km high. The impact, roughly 1 billion years ago, excavated about 1% of Vesta's entire volume and flung out the debris that became the Vesta asteroid family and the V-type asteroids. It overlaps an older 395 km crater, Veneneia.",
   facts=["Tied with Olympus Mons as the tallest mountain in the solar system","Central peak of a 505 km impact crater &mdash; ~90% of Vesta's diameter","Impact excavated about 1% of Vesta's total volume","Created the Vesta asteroid family and V-type asteroids","Overlaps an older 395 km crater, Veneneia"],
   weather_note="Gravity is so weak (~0.025 g) that the &ldquo;climb&rdquo; is mostly a very long, very slow float."),

 dict(rank=3, slug="iapetus-ridge", name="Equatorial Ridge of Iapetus", body="Iapetus (moon of Saturn)", bodykey="Iapetus",
   type="Equatorial ridge", is29er=True, ft=65617, ht="65,600 ft", km="~20 km at its tallest (ridge ~1,300 km long)",
   coords="along the 0&deg; equator (Cassini Regio)", location="Equator of the dark leading hemisphere",
   discovery="Imaged by Cassini, 31 Dec 2004 (Iapetus discovered by G. Cassini, 1671)",
   img="https://upload.wikimedia.org/wikipedia/commons/b/b4/Iapetus_equatorial_ridge.jpg", img_credit="NASA/JPL/Space Science Institute (Cassini)",
   img_desc="Cassini close-up of Iapetus showing the equatorial ridge cutting across the limb",
   lead="The Equatorial Ridge of Iapetus is a mountain belt that runs almost perfectly along the moon's equator for about 1,300 km, rising in places to roughly 20 km above the surrounding plains. Discovered by Cassini in 2004, it makes Iapetus look like a walnut and ranks among the tallest mountain features in the solar system.",
   more="Its origin remains unexplained, with hypotheses ranging from a fossil of the moon's early fast rotation, to the collapse of an ancient ring onto the surface, to upwelling interior material. The ridge is confined almost entirely to the dark hemisphere (Cassini Regio), and some segments exceed 200 km in length.",
   facts=["Follows the equator almost exactly for ~1,300 km","Peaks reach ~20 km, rivaling Olympus Mons depending on how you measure","Confined almost entirely to the dark hemisphere (Cassini Regio)","Origin still unexplained: spin fossil, collapsed ring, or convection","Makes Iapetus resemble a walnut"],
   weather_note=""),

 dict(rank=4, slug="boosaule-montes", name="Bo&ouml;saule Montes", body="Io (moon of Jupiter)", bodykey="Io",
   type="Tectonic mountain (uplifted crust)", is29er=True, ft=59711, ht="59,700 ft", km="17.5&ndash;18.2 km above the plains",
   coords="9.7&deg; S, 88.9&deg; E", location="Near Io's equator, just northwest of the volcano Pele",
   discovery="Photographed by Voyager 1, March 1979 (Io known since Galileo, 1610)",
   img="https://upload.wikimedia.org/wikipedia/commons/0/03/PIA00323_Bo%C3%B6saule_Montes_crop2_sharp.png", img_credit="NASA/JPL/USGS (Voyager 1)",
   img_desc="Voyager 1 view of South Bo&ouml;saule Montes rising above Io",
   lead="Bo&ouml;saule Montes (South) is the tallest mountain on Jupiter's moon Io and one of the tallest in the solar system, rising about 17.5 to 18.2 km above the surrounding plains. Unlike Io's many volcanoes, it is a tilted block of crust pushed up by the moon's intense tectonic stresses.",
   more="It sits just northwest of the giant volcano Pele and features a steep southeastern cliff up to 15 km high. The range spans roughly 145&times;159 km. Io's mountains are not volcanoes; they form as the constant resurfacing by lava compresses and buries older crust until blocks of it are thrust upward.",
   facts=["Tallest mountain on Io at ~18 km","A tectonic mountain, not a volcano","Steep southeastern cliff up to 15 km high","Spans about 145&times;159 km","Sits beside the giant volcano Pele"],
   weather_note=""),

 dict(rank=5, slug="ascraeus-mons", name="Ascraeus Mons", body="Mars", bodykey="Mars",
   type="Shield volcano", is29er=True, ft=49000, ht="49,000 ft", km="14.9 km base-to-peak (~18.2 km above the datum)",
   coords="11.92&deg; N, 255.92&deg; E", location="Northernmost of the three Tharsis Montes",
   discovery="Imaged by Mariner 9, 1971 (first called &ldquo;North Spot&rdquo;)",
   img="https://upload.wikimedia.org/wikipedia/commons/1/15/Ascraeus_Mons.png", img_credit="NASA/JPL/ASU (Mars Odyssey THEMIS)",
   img_desc="THEMIS daytime infrared mosaic of Ascraeus Mons",
   lead="Ascraeus Mons is a giant shield volcano in the Tharsis region of Mars and the northernmost of the three Tharsis Montes. It rises about 14.9 km from base to peak (roughly 18 km above the Martian datum) and stretches some 480 km across, making it the second-tallest volcano on Mars after Olympus Mons.",
   more="Discovered by Mariner 9 in 1971 during a global dust storm, it appeared as one of several dark &ldquo;spots&rdquo; poking above the dust. Its summit hosts a complex caldera with a central pit ~24 km wide and ~3.4 km deep, and its western flank shows fan-shaped glacial deposits.",
   facts=["Northernmost and tallest of the Tharsis Montes chain","Shield volcano ~480 km across with gentle ~7&deg; slopes","Summit caldera central pit ~24 km wide, ~3.4 km deep","Originally cataloged as &ldquo;North Spot&rdquo; by Mariner 9","Shows fan-shaped glacial deposits on its western flank"],
   weather_note=""),

 dict(rank=6, slug="ionian-mons", name="Ionian Mons", body="Io (moon of Jupiter)", bodykey="Io",
   type="Tectonic mountain (double ridge)", is29er=True, ft=41700, ht="41,700 ft", km="~12.7 km (east ridge)",
   coords="8.62&deg; N, 236.57&deg; W", location="Equatorial Io; an isolated ~159 km ridge massif",
   discovery="Characterized from NASA Galileo orbiter imagery (1990s)",
   img="https://upload.wikimedia.org/wikipedia/commons/7/7b/Io_highest_resolution_true_color.jpg", img_credit="NASA/JPL/University of Arizona (Galileo)",
   img_desc="Highest-resolution true-color view of Io (no dedicated image of Ionian Mons exists)",
   lead="Ionian Mons is a long, curved double-ridge mountain on Jupiter's moon Io, whose taller eastern ridge rises about 12.7 km, placing it among the tallest peaks in the solar system. Like Io's other mountains it is tectonic &mdash; a block of crust thrust upward and tilted &mdash; not a volcano.",
   more="It stretches roughly 159 km and was characterized from NASA Galileo images. Io has no global tectonic pattern, so its mountains appear as isolated massifs scattered between the volcanoes rather than in chains.",
   facts=["East ridge rises ~12.7 km, taller than Everest base-to-peak","A curved double-ridge tectonic massif, ~159 km long","Named after the Ionian Sea","Io's mountains form by crustal compression, not volcanism","Imaged in detail by NASA's Galileo orbiter"],
   weather_note=""),

 dict(rank=7, slug="elysium-mons", name="Elysium Mons", body="Mars", bodykey="Mars",
   type="Shield volcano", is29er=True, ft=41000, ht="41,000 ft", km="12.6 km base-to-peak (~14.1 km above the datum)",
   coords="25.02&deg; N, 147.21&deg; E", location="Elysium volcanic province, eastern hemisphere",
   discovery="Imaged by Mariner 9, 1972",
   img="https://upload.wikimedia.org/wikipedia/commons/c/cb/Elysium_Mons_%28PIA25925%29.jpg", img_credit="NASA/JPL-Caltech/ASU (THEMIS)",
   img_desc="THEMIS view of Elysium Mons including part of the summit caldera",
   lead="Elysium Mons is the largest volcano in Mars's Elysium province, the planet's second major volcanic region after Tharsis. It rises about 12.6 km from base to summit (roughly 14.1 km above the datum) and spans some 240 km across, topped by a ~14 km-wide summit caldera.",
   more="First imaged by Mariner 9 in 1972, it is flanked by the smaller volcanoes Hecates Tholus and Albor Tholus. Its profile has been likened to a stratovolcano, with relatively few visible flank lava flows compared with the Tharsis shields.",
   facts=["Largest volcano of Mars's Elysium province","About 240 km across with a ~14 km summit caldera","Anchors Mars's second-largest volcanic region","Flanked by Hecates Tholus and Albor Tholus","Steeper, more stratovolcano-like profile than the Tharsis shields"],
   weather_note=""),

 dict(rank=8, slug="arsia-mons", name="Arsia Mons", body="Mars", bodykey="Mars",
   type="Shield volcano", is29er=True, ft=38400, ht="38,400 ft", km="~11.7 km above the datum (>9 km above the plains)",
   coords="8.35&deg; S, 120.09&deg; W", location="Southernmost of the three Tharsis Montes",
   discovery="Mapped by Mariner 9, 1971&ndash;72 (albedo feature &ldquo;Nodus Gordii&rdquo;)",
   img="https://upload.wikimedia.org/wikipedia/commons/b/bf/Arsia_Mons_PIA02804.jpg", img_credit="NASA/JPL/MOLA Science Team",
   img_desc="Viking imagery draped over MOLA topography of Arsia Mons (vertical exaggeration)",
   lead="Arsia Mons is the southernmost of the three great Tharsis Montes shield volcanoes on Mars, rising about 11.7 km above the datum and more than 9 km above the surrounding plains. It is enormous &mdash; roughly 435 km wide with a summit caldera over 100 km across &mdash; and is the second-largest volcano known by volume after Olympus Mons.",
   more="It is famous for a recurring elongated orographic cloud that forms over its summit during southern winter, and it hosts several putative cave-entrance pits nicknamed &ldquo;Dena,&rdquo; &ldquo;Chloe,&rdquo; and &ldquo;Wendy.&rdquo;",
   facts=["About 435 km across with a 110&ndash;138 km summit caldera","Roughly 30 times the volume of Hawaii's Mauna Loa","Second-largest known volcano by volume after Olympus Mons","Hosts a recurring orographic cloud each southern winter","Contains several possible cave-entrance pits"],
   weather_note=""),

 dict(rank=9, slug="maxwell-montes", name="Maxwell Montes", body="Venus", bodykey="Venus",
   type="Compressional mountain range", is29er=True, ft=36000, ht="36,000 ft", km="~11 km above Venus's mean radius",
   coords="65.2&deg; N, 3.3&deg; E", location="Eastern edge of Lakshmi Planum, Ishtar Terra",
   discovery="Arecibo radar (1967); mapped by NASA's Magellan (early 1990s)",
   img="https://upload.wikimedia.org/wikipedia/commons/d/d8/Maxwell_Montes_of_planet_Venus.jpg", img_credit="NASA/JPL (Magellan radar)",
   img_desc="Magellan radar image of Lakshmi Planum and Maxwell Montes",
   lead="Maxwell Montes is the highest mountain range on Venus, rising about 11 km above the planet's mean radius in central Ishtar Terra. Built by compressional tectonics along the edge of the Lakshmi Planum plateau, it measures roughly 850 km long by 700 km wide.",
   more="It shows unusually bright radar returns thought to come from a high-altitude metallic &ldquo;frost,&rdquo; and hosts the ~100 km double-ring crater Cleopatra on its eastern flank. It is the only feature on Venus named after a man &mdash; James Clerk Maxwell, whose work on electromagnetism made radar mapping of the planet possible.",
   facts=["Highest point on Venus, ~11 km above the mean radius","About 853 km long by 700 km wide","Bright radar signature from metallic high-altitude &ldquo;frost&rdquo;","Hosts the ~100 km double-ring crater Cleopatra","The only Venusian feature named after a man"],
   weather_note="At ~380&deg;C, the summit is the &ldquo;coolest&rdquo; place on the planet's surface."),

 dict(rank=10, slug="euboea-montes", name="Euboea Montes", body="Io (moon of Jupiter)", bodykey="Io",
   type="Tectonic mountain (tilted block)", is29er=True, ft=34449, ht="34,400 ft", km="~10.5 km above the plains",
   coords="48.89&deg; S, 338.77&deg; W", location="South-polar region of Io, east of Creidne Patera",
   discovery="First imaged by Voyager 1, March 1979",
   img="https://upload.wikimedia.org/wikipedia/commons/6/6a/Euboea_Montes.png", img_credit="NASA/JPL/USGS (Voyager 1)",
   img_desc="Voyager 1 view of Euboea Montes and its landslide debris apron",
   lead="Euboea Montes is one of the tallest mountains on Io, towering roughly 10.5 km above the surrounding plains. It is a single block of crust thrust upward and tilted about 6 degrees by tectonic forces, not a volcano. A massive landslide along its northern flank produced one of the largest debris aprons in the solar system.",
   more="The mountain measures roughly 175&times;240 km at its base. The debris apron from its collapse contains an estimated 25,000 km&sup3; of material &mdash; among the largest landslide deposits known anywhere.",
   facts=["Stands ~10.5 km tall &mdash; taller than Everest above sea level","Formed by thrust faulting; tilted about 6 degrees","Northern-flank landslide left a ~25,000 km&sup3; debris apron","Roughly 175&times;240 km at its base","Imaged by NASA's Voyager 1 in 1979"],
   weather_note=""),

 dict(rank=11, slug="mauna-kea", name="Mauna Kea", body="Earth", bodykey="Earth",
   type="Dormant shield volcano", is29er=True, ft=33500, ht="33,500 ft", km="~10.2 km from the Pacific seafloor",
   coords="19.82&deg; N, 155.47&deg; W", location="Island of Hawai&#699;i, United States",
   discovery="First recorded summit ascent, 1823",
   img="https://upload.wikimedia.org/wikipedia/commons/8/8d/Mauna_Kea_from_the_ocean.jpg", img_credit="Vadim Kurland, CC BY 2.0",
   img_desc="Snow-capped Mauna Kea viewed across the ocean",
   lead="Mauna Kea is a dormant Hawaiian shield volcano whose summit reaches 13,803 ft above sea level &mdash; but whose base lies deep on the Pacific seafloor. Measured base-to-peak it rises about 10.2 km (33,500 ft), making it the tallest mountain on Earth by total height, even though only its top third pokes above the waves.",
   more="Its dry, high, stable summit hosts one of the world's premier collections of astronomical observatories. Mauna Kea last erupted roughly 4,500&ndash;6,000 years ago and holds Lake Waiau, among the highest lakes in the Pacific basin.",
   facts=["Summit is 13,803 ft above sea level but ~33,500 ft from its seafloor base","Tallest mountain on Earth measured base-to-peak","Last erupted roughly 4,500&ndash;6,000 years ago","Hosts 13 observatories funded by 11 countries","Earth's true champion &mdash; if you count the underwater part"],
   weather_note="The only peak here you can summit by road &mdash; bring a jacket, not a spacesuit."),

 dict(rank=12, slug="mauna-loa", name="Mauna Loa", body="Earth", bodykey="Earth",
   type="Active shield volcano", is29er=True, ft=30085, ht="30,085 ft", km="~9.17 km from the Pacific seafloor (~17 km counting the crust it depresses)",
   coords="19.48&deg; N, 155.61&deg; W", location="Island of Hawai&#699;i, United States",
   discovery="First recorded ascent 1794 (Archibald Menzies); last erupted 2022",
   img="https://upload.wikimedia.org/wikipedia/commons/e/e0/Mauna_Loa_Volcano.jpg", img_credit="J.D. Griggs / USGS (public domain)",
   img_desc="Mauna Loa's broad shield rising above the Island of Hawai&#699;i",
   lead="Mauna Loa is the largest active volcano on Earth &mdash; a vast Hawaiian shield whose summit reaches 13,678 ft above sea level but whose base sits on the Pacific seafloor. Measured base-to-peak it rises about 30,085 ft (9.2 km), making it the second-tallest mountain on Earth after its neighbor <a href='mauna-kea.html'>Mauna Kea</a> &mdash; and, together with Mauna Kea, one of only two Earth mountains that out-top Everest from base to summit.",
   more="Mauna Loa makes up about half of the Island of Hawai&#699;i and holds an estimated 75,000 km&sup3; of rock &mdash; so heavy it has pressed the ocean crust beneath it down by a further ~8 km. It last erupted in late 2022, its first activity since 1984.",
   facts=["Largest active volcano on Earth by volume (~75,000 km&sup3;)","Summit 13,678 ft above sea level; ~30,085 ft from its seafloor base","Second-tallest mountain on Earth base-to-peak, just behind Mauna Kea","Its weight depresses the ocean crust beneath it by a further ~8 km","Last erupted November&ndash;December 2022, after 38 years quiet"],
   weather_note="Like its taller twin Mauna Kea, the hard part is the drive, not the air &mdash; bring a jacket, not a spacesuit."),

 dict(rank=13, slug="mount-everest", name="Mount Everest", body="Earth", bodykey="Earth",
   type="Earth's highest peak &mdash; by sea level, not base-to-peak", is29er=True, ft=29032, ht="29,032 ft", note=True, km="8.849 km above sea level &mdash; only ~3.7&ndash;4.6 km of it is base-to-peak relief",
   coords="27.99&deg; N, 86.93&deg; E", location="Mahalangur Himal, China&ndash;Nepal border",
   discovery="First summited 29 May 1953 by Hillary &amp; Tenzing Norgay",
   img="https://upload.wikimedia.org/wikipedia/commons/d/d1/Mount_Everest_as_seen_from_Drukair2_PLW_edit.jpg", img_credit="shrimpo1967 / PLW2, CC BY-SA 2.0",
   img_desc="Mount Everest rising above the Nuptse&ndash;Lhotse ridge, from a Drukair flight",
   lead="Mount Everest is Earth's highest mountain above sea level at 29,032 ft &mdash; the crown jewel of human mountaineering. But it makes this list with an asterisk: measured base-to-summit, the way every other peak here is, Everest rises only ~12,000&ndash;15,000 ft from its base on the Tibetan Plateau and wouldn't qualify as a 29er at all. It is here on sea-level fame alone &mdash; out-topped from base to peak by two ocean-rooted Hawaiian volcanoes, and dwarfed by a tilted block of crust on a moon of Jupiter.",
   more="First climbed in 1953 by Edmund Hillary and Tenzing Norgay, it remains the ultimate Earth-bound summit and a humbling reminder of how modest our tallest mountain really is. Its nearest sea, the Bay of Bengal, is some 700 km away.",
   facts=["Listed by its 29,032 ft elevation above sea level &mdash; not base-to-peak, so it wears an asterisk here","Its true base-to-summit relief is only ~12,000&ndash;15,000 ft, short of the 29,000 ft bar","First summited in 1953 by Hillary and Tenzing Norgay","Out-topped base-to-peak by both Mauna Kea and Mauna Loa","Even Mars's third-string volcanoes look down on it"],
   weather_note="Compared with every other peak on this list, Everest has weather you could (barely) survive."),
]

NPEAKS = len(PEAKS)

# Host planet for each body (moons grouped under their parent planet) - used by the "Planet" sort
PLANET_OF = {"Mars": "Mars", "Io": "Jupiter", "Venus": "Venus",
             "Vesta": "Asteroid Belt", "Iapetus": "Saturn", "Earth": "Earth"}

# The Everest asterisk footnote (reused on the list page and Everest's own page)
EVEREST_NOTE = ('<p style="font-size:0.85em;color:#666;max-width:980px;margin-top:16px;border-top:1px solid #ddd;padding-top:10px;">'
  '<sup>*</sup> <strong>Mount Everest</strong> is listed by its <strong>29,032 ft elevation above sea level</strong> &mdash; '
  'the number that made it famous as Earth&rsquo;s highest peak. Measured base-to-summit like every other mountain here, '
  'Everest rises only ~12,000&ndash;15,000 ft from its base on the Tibetan Plateau and wouldn&rsquo;t qualify as a 29er at all. '
  'Earth&rsquo;s real base-to-peak giants are the Hawaiian volcanoes <a href="mauna-kea.html">Mauna Kea</a> (33,500 ft) and '
  '<a href="mauna-loa.html">Mauna Loa</a> (30,085 ft). The world&rsquo;s most famous mountain makes this list on a technicality.</p>')

# ============================ INDEX (the ranked list) ============================
def card(p):
    star = '<sup>*</sup>' if p.get("note") else ''
    badge = (f'<span style="background:#f6a828;color:#fff;font-size:0.6em;font-weight:bold;'
             f'padding:2px 7px;border-radius:9px;vertical-align:middle;margin-left:6px;'
             f'letter-spacing:.3px;">29er{"*" if p.get("note") else ""}</span>') if p["is29er"] else ""
    return f'''<div class="groupCard peak-card cardhover" onclick="location.href='{p['slug']}.html';" data-rank="{p['rank']}" data-ascents="0" data-elevation="{p['ft']}" data-name="{p['name']}" data-mrange="{p['body']}" data-planet="{PLANET_OF[p['bodykey']]}">
    <div class="thumbnail-container"><img src="images/peaks/{p['slug']}.jpg" alt="{p['name']}"></div>
    <div class="content-container">
        <div class="peak-name linkButton">{p['name']}{badge}</div>
        <div class="peak-stats">
            <div class="stat" title="Height">{p['ht']}{star}</div>
            <div class="stat" title="Rank">Solar System Rank: <strong>{p['rank']} of {NPEAKS}</strong></div>
            <div class="stat" title="Body">{p['body']}</div>
        </div>
    </div>
    <div class="content-container extra-stats">
        <div class="peak-name linkButton">&nbsp;</div>
        <div class="peak-stats">
            <ul class="bullets-withicon">
                <li><i class="fa-solid fa-hiking"></i>&nbsp;&nbsp;<a href="{p['slug']}.html">Routes: </a>1</li>
                <li><i class="fa fa-cloud-sun"></i>&nbsp;&nbsp;<a href="{p['slug']}.html#weather">Weather Forecast</a></li>
                <li><i class="fa fa-user-group"></i>&nbsp;&nbsp;0 Member Ascents</li>
            </ul>
        </div>
    </div>
    <div class="rank-badge" title="Rank">{p['rank']}</div></div>'''

cards = "\n\n".join(card(p) for p in PEAKS)
index_body = f'''<div id="wrap">

<div class="breadcrumb" id="breadcrumbwrap">
  <ul class="breadcrumb">
   <li><a href="index.html">Home</a></li>
   <li><a>Tallest Mountains</a></li>
  </ul>
</div>

<a id="top" accesskey="t"></a>
<div style="width:100%;clear:both;"></div>

<h1>The Tallest Mountains in the Solar System</h1>
The <strong>29ers</strong>: every mountain in the solar system that out-tops Mount Everest, measured base-to-summit. A <a href="about.html">29er</a> rises at least <strong>29,000 feet</strong> from base to peak &mdash; and all <strong>{NPEAKS}</strong> here clear that bar, from Earth's own Hawaiian volcanoes up to the ~72,000-ft co-champions <a href="olympus-mons.html">Olympus Mons</a> and <a href="rheasilvia.html">Rheasilvia</a>. All except one: <a href="mount-everest.html">Mount Everest</a> &mdash; the most famous mountain on the planet sneaks onto the list on its sea-level height alone, and earns an asterisk for it.<sup>*</sup>
<form name="formsubset">
<div class="filterBox">
    <label for="sort">Sort By</label>
    <select id="sort">
        <option value="rank">Rank</option>
        <option value="elevation">Height</option>
        <option value="name">Name</option>
        <option value="mrange">Body</option>
        <option value="planet">Planet</option>
        <option value="ascents">Member Ascents</option>
    </select>
</div>
</form>

<div id="peak-container" class="peak-container">

{cards}

</div>

{EVEREST_NOTE}

</div>'''

page("peaks.html", "The Tallest Mountains in the Solar System | 29ers.com", LIST_CSS, index_body)

# ============================ HOME PAGE (faithful clone of 14ers.com landing page) ============================
home_body = '''<div id="wrap">

<a id="top" accesskey="t"></a>

<div id="dhtmlpoptip"></div>
<div id="backimage-wrapper"></div>
<main style="background:linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,.55)), url(images/peaks/olympus-mons-hero.jpg) center/cover fixed no-repeat;" id="main">

    <div id="mainFloatButtons">
        <div id="jumpRecentActivity" style="right:5px;z-index:1;margin-bottom:20px;" class="show-10"><a href="#recentActivityPanel" onclick="document.getElementById('recentActivityPanel').scrollIntoView({behavior:'smooth'});return false;" class="buttonf orangef" style="margin-right:0;background-color:#eb8f00;border:solid 1px #eb8f00;border-radius:4px;" title="Jump to Recent Activity"><i class="fa-solid fa-chart-simple"></i><span class="hide-4">&nbsp;&nbsp;Recent Activity</span></a></div>
    </div>

<div id="sectionMain" class="homeSection  notLoggedIn">
<h1>The Tallest Mountains in the Solar System</h1>
<h2 class="helloText" style="font-size:1.4em;margin-top:0.5em;">Everything you need to plan, track and document your ascents of the solar system's highest peaks</h2>
<h2 class="helloText" style="margin-top:0;font-size:1em;">Your field guide to the giants of the solar system &mdash; <a style="font-size:1em;color:yellow;" href="about.html">what's a 29er?</a></h2>
<div style="width:100%;"></div>
</div>

<div id="sectionPlanning" class="homeSection">
<div class="sectionHeader"><h2><span class="sectionPlanningArrow" style="font-size:0.5em;"><i class="fa-solid fa-arrow-down fa-beat" style="--fa-animation-duration: 4s;color:#999;"></i>&nbsp;&nbsp;&nbsp;</span>Planning<span class="sectionPlanningArrow" style="font-size:0.5em;">&nbsp;&nbsp;&nbsp;<i class="fa-solid fa-arrow-down fa-beat" style="--fa-animation-duration: 4s;color:#999;"></i></span></h2></div>

<div class="sectionWrapper flex">
<div class="sectionText">
    A safe and successful summit starts with proper planning &mdash; a thorough review of the route, the relief profile, and the local conditions. Gravity, air pressure, temperature and radiation vary wildly from peak to peak, so the prep for a Mars shield volcano looks nothing like the prep for a tilted block of crust on a moon of Jupiter.
    <br><br>
    Browse the full ranked list of the solar system's 13 tallest mountains, dig into each peak's stats, photos, routes and conditions, and figure out whether you'll need a pressure suit, a spacecraft, or just a warm jacket.
    <br><br>
    <div class="sectionImage" style="padding-left:7px;">
        <div class="show-10" style="width:97%">
            <img src="images/peaks/ascraeus-mons.jpg" alt="Ascraeus Mons" title="Mars from orbit" loading="lazy" style="width:100%;max-width:100%;height:auto;margin-bottom:10px;border-radius:6px;">
        </div>
    </div>
    Every peak page carries the elevation, body, type, coordinates, discovery, a photo gallery and a themed weather forecast.<br><a href="peaks.html" class="buttonf orangef">Explore the Peaks</a>
    <br><br>
    New to interplanetary mountaineering?<br><a href="about.html" class="buttonf orangef">What are 29ers?</a>
</div>

<div class="sectionImage largeDisplay">
    <img src="images/peaks/maxwell-montes.jpg" alt="Maxwell Montes radar" title="Maxwell Montes (Venus)" loading="lazy" style="border-radius:6px;">
    <br>
    <img class="planningBookmarks" src="images/peaks/olympus-mons-2.jpg" alt="Olympus Mons" title="Olympus Mons (Mars)" loading="lazy" style="border-radius:6px;">
</div>

</div>
</div>

<div id="sectionTracking" class="homeSection">
<div class="sectionHeader"><h2>Track Your Progress</h2></div>
<div class="sectionWrapper flex">
<div class="sectionText">A peak checklist is an easy way to document your ascents. Tick off all 13 of the solar system's <strong>29ers</strong> &mdash; every peak that out-tops Everest &mdash; or just chase the two co-tallest, Olympus Mons and Rheasilvia.<br><br>Track winter<span class='far fa-snowflake ficon'></span> ascents, ski/snowboard<span class='fa-solid fa-person-skiing ficon'></span> descents (good luck on Io), repeats and solo climbs. Compare your list with a partner when planning the next expedition.
<br>
<a href="peaks.html" class="buttonf orangef">The 29ers List</a><br><br>
</div>
<div class="sectionImage largeDisplay">
<img src="images/peaks/rheasilvia.jpg" alt="Vesta" title="Rheasilvia (Vesta)" loading="lazy" style="border-radius:6px;">
</div>
</div>
</div>


<div id="sectionCommunity" class="homeSection">
    <div class="sectionHeader"><h2>Living History and Community</h2></div>
    <div class="sectionWrapper flex">
        <div class="sectionText" style="width:100%;max-width:100%;">Every one of these summits was mapped by robotic explorers &mdash; Mariner, Viking, Voyager, Pioneer, Magellan, Galileo, Cassini and Dawn &mdash; and not one of them has ever been climbed. The first ascents are still out there, waiting.
            <div style="width:100%;height:55px;"><a href="peaks.html" class="buttonf orangef">Browse Peaks</a></div>
            Recorded summits so far, by humans or robots: <strong>zero</strong>. Be the first. Whether your future rope team forms on Mars, Io, or a moon of Saturn, the biggest mountains in existence aren't going anywhere.
        </div>
    </div>
</div>

<div id="sectionMobileApps" class="homeSection">
    <div class="sectionHeader" style="padding-left:0;"><h2 style="width:100%;text-align:center;">Field Guide</h2></div>
    <div style="width:100%;text-align:center;">
        Heading off-world soon? Every peak page packs the stats, imagery, conditions and routes you'll want in the field.<br><br>
        <img src="images/peaks/ionian-mons.jpg" alt="Io" title="Io, home of three of the tallest mountains" loading="lazy" style="max-width:90%;border-radius:8px;">
        <br><br>
        <a href="peaks.html" class="buttonf orangef">Open the Field Guide</a>
        <br>
    </div>
</div>

<div id="sectionSupport" class="homeSection">
<div class="sectionHeader" style="padding-left:0;"><h2 style="width:100%;text-align:center;">About this site</h2></div>
<div class="sectionWrapper flex">
<div class="sectionText" style="width:100%;max-width:100%;">29ers.com is the complete guide to the tallest mountains in the solar system &mdash; every peak that out-tops Mount Everest, from the giant shield volcanoes of Mars to the tilted crustal blocks of Io. The peaks, their stats and their photos are all real. Built by <a href="https://spencerboucher.com" rel="noopener">Spencer Boucher</a>.<br><br>
</div>
</div>
</div>


</main>


    <div id="recentActivityPanel" class="recentactivity-wrapper notLoggedIn">
        <div id="recentActivityHeader" style="display: flex; justify-content: space-between; align-items: center; user-select: none;">
            <h2 id="recentActivityTitle">Recent Activity</h2>
            <button id="recentActivityChevron" aria-label="Toggle Recent Activity"><svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
        </div>
        <div id="recentActivityContent">
<div class="v3-darkback" style="margin-top:0;">
<div id="tinyTabGroup" class="v3-tinyTabGroup" style="font-size:9pt;">
<ul id="tabs" class="tinyTabs" style="background:#3e3e3e;">
	<li class="tinyTab active"><a href="conditions.html" id="a3"><span class="hide-4">Conditions</span><span class="show-4">Condits</span></a></li>
	<li class="tinyTab"><a href="landing-sites.html" id="a5"><span class="hide-4">Trailheads</span><span class="show-4">THs</span></a></li>
	<li class="tinyTab"><a href="trip-reports.html" id="a2"><span class="hide-3">Trips</span><span class="show-3">TRs</span></a></li>
	<li class="tinyTab"><a href="forum.html" id="a4"><span>Forum</span></a></li>
</ul>
<div id="content" aria-live="polite" style="border:0;height:100%;font-size:10pt;color:#ddd;padding:10px 14px;text-align:left;">
<ul style="list-style:none;margin:0;padding:0;line-height:1.9;">
<li><i class="fa fa-cloud-sun" style="color:#f6a828;"></i>&nbsp; <a href="olympus-mons.html#weather"><strong>Olympus Mons</strong></a> &mdash; summit dusty, ~&minus;100&deg;C, 72 Pa. Regional dust on the flanks. <span style="opacity:.6;">(Sol 4012)</span></li>
<li><i class="fa fa-cloud-sun" style="color:#f6a828;"></i>&nbsp; <a href="maxwell-montes.html#weather"><strong>Maxwell Montes</strong></a> &mdash; a brisk ~380&deg;C, 90 atm, sulfuric haze. Coolest spot on Venus. <span style="opacity:.6;">(today)</span></li>
<li><i class="fa-solid fa-hiking" style="color:#f6a828;"></i>&nbsp; <a href="rheasilvia.html"><strong>Rheasilvia</strong></a> &mdash; 0 recorded ascents. Be the first. <span style="opacity:.6;">(all-time)</span></li>
<li><i class="fa fa-triangle-exclamation" style="color:#ff6d19;"></i>&nbsp; <a href="boosaule-montes.html"><strong>Bo&ouml;saule Montes</strong></a> &mdash; 15 km basal scarp; rockfall likely. Mind the radiation. <span style="opacity:.6;">(Io)</span></li>
<li><i class="fa fa-mountain" style="color:#f6a828;"></i>&nbsp; <a href="mount-everest.html"><strong>Mount Everest</strong></a> &mdash; still the shortest peak on the list. <span style="opacity:.6;">(Earth)</span></li>
</ul>
</div>
</div>
</div>
        </div>
</div>

<div class="push"></div>
</div>'''

page("index.html", "29ers.com | The Tallest Mountains in the Solar System", HOME_CSS, home_body)

# ============================ ABOUT ============================
about_body = '''<div id="wrap">

<div class="breadcrumb" id="breadcrumbwrap">
  <ul class="breadcrumb">
   <li><a href="index.html">Home</a></li>
   <li><a>What are 29ers?</a></li>
  </ul>
</div>

<a id="top" accesskey="t"></a>
<div style="width:100%;clear:both;"></div>

<h1>What are 29ers?</h1>
<div class="overviewText" style="max-width:900px;">
Colorado mountaineers have the <a href="https://www.14ers.com" rel="noopener">14ers</a> &mdash; the 58 peaks that rise above 14,000 feet. Out here the bar is Mount Everest itself. A <strong>29er</strong> is a mountain that rises at least <strong>29,000 feet</strong> base-to-summit &mdash; the height of Everest (29,032 ft), Earth's tallest peak. Measured that way, every mountain in the solar system that out-tops Everest makes the list &mdash; from <a href="olympus-mons.html">Olympus Mons</a> and <a href="rheasilvia.html">Rheasilvia</a>, tied for the title of tallest mountain anywhere at ~72,000 ft, all the way down to Everest, the shortest 29er of them all.
<br><br>
Every one is ranked base-to-summit, biggest first. See the <a href="peaks.html">full ranked list of all thirteen</a>.
<br><br>
<h2>How we measure</h2>
Earth's peaks are ranked by height above sea level, but most worlds have no sea. So solar-system mountains are compared <strong>base to peak</strong> &mdash; the same way Hawaii's <a href="mauna-kea.html">Mauna Kea</a> (~33,500 ft from the ocean floor) and <a href="mauna-loa.html">Mauna Loa</a> (~30,085 ft) both out-top Everest. By that yardstick, Olympus Mons and Rheasilvia are the undisputed giants. Mount Everest is the lone exception we grandfather in: we list it by its famous 29,032 ft <em>above sea level</em>, but measured base-to-peak like everything else it rises only ~12,000&ndash;15,000 ft &mdash; so Earth's most famous mountain makes the list with an asterisk, out-towered by two volcanoes most people have never heard of.
<br><br>
<h2>About this site</h2>
29ers.com is a parody of <a href="https://www.14ers.com" rel="noopener">14ers.com</a>, built by <a href="https://spencerboucher.com" rel="noopener">Spencer Boucher</a>. Same look, bigger mountains. The peaks are real; the website is a joke. Imagery is courtesy of NASA/JPL and Wikimedia contributors, credited on each peak page.
</div>

</div>'''
page("about.html", "What are 29ers? | 29ers.com", LIST_CSS, about_body)

# ============================ PEAK DETAIL PAGES ============================
def stat(label, value):
    return f'<div class="stat"><span class="label">{label}</span><span class="value">{value}</span></div>'
def stat_empty(value):
    return f'<div class="stat"><span class="label empty"></span><span class="value">{value}</span></div>'

def routes_html(p):
    earth = p["bodykey"] == "Earth"
    if p["slug"] == "mount-everest":
        return ('<h2 style="margin-top:4px;">Routes</h2><ul class="bullet1 right-arrows">'
                '<li><a href="routes.html"><strong>South Col (Nepal)</strong></a> &mdash; the classic line</li>'
                '<li><a href="routes.html"><strong>North Col / Northeast Ridge (Tibet)</strong></a></li></ul>'
                '<p>Real, hard, and deadly &mdash; thousands have summited since 1953 and hundreds have died trying. '
                'But on <em>this</em> list it is the gentle one: the only peak with breathable air, and the shortest of the bunch.</p>')
    if p["slug"] == "mauna-kea":
        return ('<h2 style="margin-top:4px;">Routes</h2><ul class="bullet1 right-arrows">'
                '<li><a href="routes.html"><strong>Summit Road</strong></a> &mdash; drive to ~13,800 ft</li>'
                '<li><a href="routes.html"><strong>Humu&#699;ula Trail</strong></a> &mdash; ~6 mi on foot</li></ul>'
                '<p>The catch: only the top ~13,800 ft is above water. The other ~19,700 ft of this mountain is underwater, '
                'so nobody actually climbs the full ~33,500 ft. Still counts.</p>')
    if p["slug"] == "mauna-loa":
        return ('<h2 style="margin-top:4px;">Routes</h2><ul class="bullet1 right-arrows">'
                '<li><a href="routes.html"><strong>Mauna Loa Observatory Trail</strong></a> &mdash; ~6&ndash;13 mi from the end of the observatory road</li>'
                '<li><a href="routes.html"><strong>&#699;Ainap&#333; Trail</strong></a> &mdash; the long historic route up from near sea level</li></ul>'
                '<p>You can drive the Mauna Loa Observatory Road to ~11,000 ft, then hike a high, lava-strewn trail to the 13,678 ft summit. '
                'But like its neighbor Mauna Kea, only the top ~13,700 ft is above water &mdash; the rest of the mountain is underwater, '
                'so nobody climbs the full ~30,085 ft.</p>')
    return ('<h2 style="margin-top:4px;">Routes (1)</h2><ul class="bullet1 right-arrows">'
            f'<li><a href="routes.html"><strong>Standard Route</strong></a> &mdash; <em>Class 6 ({p["body"].split(" (")[0]} environment; spacecraft &amp; pressure suit required)</em></li></ul>'
            f'<p>The standard ascent of this {p["type"].lower()} gains roughly <strong>{p["ht"]}</strong> of vertical relief. '
            'There are no technical cruxes &mdash; the entire difficulty is logistics, cold, and a hard vacuum (or near-vacuum).</p>'
            '<p><strong>Recorded ascents:</strong> 0 &mdash; be the first.</p>')

def trips_html(p):
    if p["slug"] == "mount-everest":
        return ('<h2 style="margin-top:4px;">Trip Reports</h2><p>Everest has more trip reports than any mountain on Earth '
                '&mdash; just not here. On 29ers.com it is simply the shortest peak on the list. Humbling, isn&rsquo;t it?</p>')
    if p["bodykey"] == "Earth":
        return ('<h2 style="margin-top:4px;">Trip Reports</h2><p>Plenty of visitors reach this summit &mdash; most of them '
                'never realizing they are standing on Earth&rsquo;s tallest mountain. Post your report!</p>')
    return ('<h2 style="margin-top:4px;">Trip Reports (0)</h2><p>No trip reports yet. No human or robot has stood on this summit. '
            '<strong>Be the first to summit and post one!</strong></p>')

def peak_page(p):
    bi = BODY[p["bodykey"]]
    stats = "\n".join([
        stat("Height", p["ht"] + ('<sup>*</sup>' if p.get("note") else "")),
        stat_empty(p["km"]),
        stat("Solar System Rank", f'{p["rank"]} of {NPEAKS}'),
        stat("Body", p["body"]),
        stat("Type", p["type"]),
        stat("Location", p["location"]),
        stat("Coordinates", p["coords"]),
        stat("Discovered", p["discovery"]),
    ])
    facts = "\n".join(f"<li>{f}</li>" for f in p["facts"])
    hero = f'images/peaks/{p["slug"]}.jpg'
    photos = (f'<i class="fa-solid fa-panorama" style="font-size:1.5em;"></i>&nbsp;&nbsp;'
              f'Photos of {p["name"]}.<br><br>'
              f'<div class="peakGroupedPhotosWrap">{p["img_desc"]} <em>({p["img_credit"]})</em><br>'
              f'<span><a href="{p["img"]}" target="_blank" rel="noopener"><img src="{hero}" '
              f'style="width:560px;max-width:100%;border-radius:4px;" alt="{p["name"]}"></a></span></div>')
    if p.get("img2"):
        photos += (f'<div class="peakGroupedPhotosWrap">{p["img2_desc"]} <em>({p["img2_credit"]})</em><br>'
                   f'<span><a href="{p["img2"]}" target="_blank" rel="noopener"><img src="images/peaks/{p["slug"]}-2.jpg" '
                   f'style="width:420px;max-width:100%;border-radius:4px;" alt="{p["name"]}"></a></span></div>')
    photos += f'<div style="clear:both;padding-top:8px;"><strong>Quick facts</strong><ul class="bullets-withicon">{facts}</ul></div>'

    wnote = f' {p["weather_note"]}' if p.get("weather_note") else ""
    weather = (f'<h2 style="margin-top:4px;">Conditions &mdash; {p["name"]}</h2>'
               f'<p>{bi["weather"]}{wnote}</p>'
               f'<p style="margin-top:6px;"><i class="fa-solid fa-mountain" style="color:#b36602;"></i>&nbsp; '
               f'<strong>Summit:</strong> {p["ht"]} ({p["km"]}).</p>')
    coords_line = (f'<p>{p["location"]} &mdash; <strong>{p["coords"]}</strong>.</p>'
                   if p["coords"] != "n/a" else f'<p>{p["location"]}.</p>')
    mapc = (f'<h2 style="margin-top:4px;">Map</h2>{coords_line}'
            f'<a href="{p["img"]}" target="_blank" rel="noopener"><img src="{hero}" '
            f'style="width:560px;max-width:100%;border:1px solid #999;border-radius:4px;" alt="{p["name"]} location"></a>'
            f'<p style="margin-top:8px;"><a href="{bi["maplink"][1]}" rel="noopener">{bi["maplink"][0]} '
            f'<i class="fas fa-external-link-alt"></i></a></p>')

    more_block = (f'<span id="moreText" style="display:none;"><br><br>{p["more"]}</span>'
                  f'<button onclick="readMore()" id="moreButton" class="buttonfs orangef">Read more</button>') if p.get("more") else ""
    badge = (f' <span style="background:#f6a828;color:#fff;font-size:0.5em;font-weight:bold;'
             f'padding:3px 8px;border-radius:9px;vertical-align:middle;">29er{"*" if p.get("note") else ""}</span>') if p["is29er"] else ""
    note_block = EVEREST_NOTE if p.get("note") else ""

    body = f'''<div id="wrap">

<div class="breadcrumb" id="breadcrumbwrap">
  <ul class="breadcrumb">
   <li><a href="index.html">Home</a></li>
   <li><a href="peaks.html">Tallest Mountains</a></li>
   <li><a>{p['name']}</a></li>
  </ul>
</div>

<a id="top" accesskey="t"></a>
<div style="width:100%;clear:both;"></div>

<div id="wrap_inner">
<h1>{p['name']}{badge}</h1>
<div class="overviewText" style="margin-top:0;">{p['lead']}
{more_block}</div>
{note_block}

<div id="sidebar">
<table class="v3-table" style="height:100%;width:100%;">
<tr>
<td><a href="{p['img']}" target="_blank" rel="noopener" style="display:flex;"><img src="images/peaks/{p['slug']}.jpg" style="display:inline-block;border:0;width:400px;max-width:100%;border-radius:3px;" alt="{p['name']}"></a>
<div style="font-size:0.8em;color:#666;padding:3px 2px;">{p['img_credit']}</div>
</td>
</tr>
<tr>
<td>
<div class="sidebar_content">
{stats}
</div>
</td>
</tr>
<tr>
<th>Checklists</th>
</tr>
<tr>
<td>
<div class="sidebar_content">
<ul class="bullets-withicon">
<li><i class="fa-li fa fa-user-group"></i><a href="checklists.html">0 Member Ascents</a></li>
<li><i class="fa-li far fa-snowflake"></i><a href="checklists.html">0 Member Winter Ascents</a></li>
<li><i class="fa-li fa fa-person-skiing"></i><a href="checklists.html">0 Member Ski Descents</a></li>
</ul>
</div>
</td>
</tr>
<tr>
<th>Planning</th>
</tr>
<tr>
<td>
<div class="sidebar_content">
<ul class="bullet1 right-arrows">
<li><a href="#weather" onclick="showTab(5)">Weather</a></li>
<li><a href="conditions.html">Peak Conditions&nbsp;(Last: never)</a></li>
<li><a href="gpx.html">GPX Library Entries (0)</a></li>
<li><a href="reception.html">Relay-Sat Reception</a></li>
<li><a href="climb-times.html">User Climb Times</a></li>
</ul>
</div>
</td>
</tr>
<tr class="hide-6">
<th>{bi['ology']}</th>
</tr>
<tr class="hide-6">
<td>
<div class="sidebar_content">
<ul class="bullet1 right-arrows">
<li><a href="worlds.html">Name History</a></li>
<li><a href="worlds.html">Discovery History</a></li>
<li><a href="worlds.html">Geology</a></li>
<li><a href="worlds.html">More Information</a></li>
</ul>
<div style="text-align:right;margin-right:10px;"><a href="worlds.html">View All</a></div>
</div>
</td>
</tr>

</table>

</div>

<div id="tabGroup">

<div style="width:100%;float:left;clear:both;">
 <ul class="tabs no-wrap">
  <li class="tab"><input type="radio" name="tabs" checked="checked" id="tab1"><label for="tab1" id="tabs1-link" onclick="showTab(1)">Photos</label></li>
  <li class="tab"><input type="radio" name="tabs" id="tab2"><label for="tab2" id="tabs2-link" onclick="showTab(2)">Routes</label></li>
  <li class="tab"><input type="radio" name="tabs" id="tab3"><label for="tab3" id="tabs3-link" onclick="showTab(3)"><span class="hide-5">Trip Reports</span><span class="show-5">Trips</span></label></li>
  <li class="tab"><input type="radio" name="tabs" id="tab4"><label for="tab4" id="tabs4-link" onclick="showTab(4)">Map</label></li>
  <li class="tab"><input type="radio" name="tabs" id="tab5"><label for="tab5" id="tabs5-link" onclick="showTab(5)"><i class="fa-solid fa-cloud-sun fa-lg" style="color:#FFF900;"></i></label></li>
 </ul>
</div>

<div id="tab1-content" class="content" style="display:block;width:100%;"><div style="padding:8px 10px;color:#222;">{photos}</div></div>
<div id="tab2-content" class="content" style="display:none;width:100%;"><div style="padding:8px 10px;color:#222;">{routes_html(p)}</div></div>
<div id="tab3-content" class="content" style="display:none;width:100%;"><div style="padding:8px 10px;color:#222;">{trips_html(p)}</div></div>
<div id="tab4-content" class="content" style="display:none;width:100%;"><div style="padding:8px 10px;color:#222;">{mapc}</div></div>
<div id="tab5-content" class="content" style="display:none;width:100%;"><div style="padding:8px 10px;color:#222;">{weather}</div></div>

</div>

</div>

</div>'''
    page(f'{p["slug"]}.html', f'{p["name"]} | 29ers.com', PEAK_CSS, body)

for p in PEAKS:
    peak_page(p)

# ============================ SPOOF SECTION PAGES (mirror 14ers.com sections) ============================
# Shared little helpers so every new page reuses the masthead/footer + existing CSS.
TH = 'style="text-align:left;padding:7px 10px;border-bottom:2px solid #eb8f00;color:#633;"'
TD = 'style="padding:6px 10px;border-bottom:1px solid #ddd;"'
BTN = ('style="display:inline-block;background:#eb8f00;color:#fff;border:0;padding:9px 16px;'
       'border-radius:5px;font-weight:bold;cursor:pointer;text-decoration:none;"')
BODY_ORDER = ["Mars", "Io", "Venus", "Vesta", "Iapetus", "Earth"]

def wrap(crumb, inner, h1=None):
    """Standard breadcrumb + #top + #wrap shell. The current-page crumb is an href-less
    <a> so the chevron styling in siteheader.css/colors.css applies without linking anywhere."""
    h1html = f"<h1>{h1}</h1>\n" if h1 else ""
    return f'''<div id="wrap">

<div class="breadcrumb" id="breadcrumbwrap">
  <ul class="breadcrumb">
   <li><a href="index.html">Home</a></li>
   <li><a>{crumb}</a></li>
  </ul>
</div>

<a id="top" accesskey="t"></a>
<div style="width:100%;clear:both;"></div>
{h1html}{inner}
</div>'''

def route_class(p):
    if p["slug"] == "mount-everest":
        return "Class 3", "South Col (Nepal)"
    if p["slug"] == "mauna-kea":
        return "Class 1", "Summit Road"
    if p["slug"] == "mauna-loa":
        return "Class 2", "Mauna Loa Observatory Trail"
    return "Class 6", "Standard Route"

def peaks_by_body():
    d = {}
    for p in PEAKS:
        d.setdefault(p["bodykey"], []).append(p)
    return d

def first_sentence(text):
    return text.split(".")[0]

# ---- Routes index (mirrors /routes.php sortable table) ----
def routes_index():
    rows = ""
    for p in PEAKS:
        cls, route = route_class(p)
        rows += (f'<tr><td {TD}><a href="{p["slug"]}.html"><strong>{route}</strong></a></td>'
                 f'<td {TD}>{p["name"]}</td><td {TD}>{p["body"]}</td>'
                 f'<td {TD}>{cls}</td><td {TD}>{p["ht"]}{"<sup>*</sup>" if p.get("note") else ""}</td><td {TD} style="text-align:center;">0</td></tr>')
    inner = ('<div class="overviewText" style="max-width:980px;">Every standard route to the summit of the '
             'solar system&rsquo;s 29ers, ranked by height. Difficulty uses our extended '
             '<a href="difficulty.html">class system</a> &mdash; where <strong>Class 6</strong> means '
             '&ldquo;spacecraft and pressure suit required.&rdquo; Recorded ascents: still zero.</div><br>'
             '<table style="width:100%;border-collapse:collapse;font-size:0.95em;">'
             f'<thead><tr><th {TH}>Route</th><th {TH}>Peak</th><th {TH}>Body</th><th {TH}>Difficulty</th>'
             f'<th {TH}>Vertical relief</th><th {TH} style="text-align:center;">Ascents</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>')
    return wrap("29er Routes", inner, "29er Routes")
page("routes.html", "29er Routes | 29ers.com", LIST_CSS, routes_index())

# ---- Route Selection Tool (mirrors /routeselector.php filter sidebar + results) ----
def route_selector():
    def sel(label, opts):
        o = "".join(f"<option>{x}</option>" for x in opts)
        return (f'<label style="display:block;font-weight:bold;color:#633;margin:10px 0 3px;">{label}</label>'
                f'<select style="width:100%;">{o}</select>')
    sidebar = ('<div style="flex:0 0 230px;background:#f2efe9;border:1px solid #ddd;border-radius:6px;padding:12px;">'
               '<h2 style="margin-top:0;font-size:1.1em;">Filters</h2>'
               + sel("Body", ["Any", "Mars", "Io", "Venus", "Vesta", "Iapetus", "Earth"])
               + sel("Route type", ["Any", "Shield volcano", "Tectonic block", "Impact peak", "Ridge"])
               + sel("Difficulty", ["Any", "Class 1", "Class 3", "Class 6"])
               + sel("Surface gravity", ["Any", "Under 0.1 g", "0.1&ndash;0.4 g", "Over 0.4 g"])
               + sel("Atmosphere", ["Any", "None (vacuum)", "Thin", "Breathable", "Crushing"])
               + sel("Road access", ["Any", "Yes (Mauna Kea only)", "No"])
               + f'<br><br><button {BTN} onclick="return false;">Reset filters</button></div>')
    rows = ""
    for p in PEAKS:
        cls, route = route_class(p)
        rows += (f'<tr><td {TD}><a href="{p["slug"]}.html">{route} &mdash; {p["name"]}</a></td>'
                 f'<td {TD}>{p["body"]}</td><td {TD}>{cls}</td></tr>')
    results = (f'<div style="flex:1;min-width:260px;"><h2 style="margin-top:0;">156 routes &rarr; {NPEAKS} matches</h2>'
               '<table style="width:100%;border-collapse:collapse;font-size:0.95em;">'
               f'<thead><tr><th {TH}>Route</th><th {TH}>Body</th><th {TH}>Difficulty</th></tr></thead>'
               f'<tbody>{rows}</tbody></table></div>')
    inner = ('<div class="overviewText" style="max-width:980px;">Narrow the solar system&rsquo;s routes by body, '
             'difficulty, gravity and atmosphere. (The filters are for show &mdash; out here, every route is '
             'hard.)</div><br><div style="display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start;">'
             + sidebar + results + '</div>')
    return wrap("Route Selection Tool", inner, "Route Selection Tool")
page("route-selector.html", "Route Selection Tool | 29ers.com", LIST_CSS, route_selector())

# ---- Peak Conditions (mirrors /peakstatus_main.php, grouped by body) ----
def conditions_page():
    bb = peaks_by_body()
    badge = '<span style="background:#c0392b;color:#fff;padding:2px 8px;border-radius:9px;font-size:0.8em;">Severe</span>'
    blocks = ""
    for bk in BODY_ORDER:
        if bk not in bb:
            continue
        rows = ""
        for p in bb[bk]:
            rows += (f'<tr><td {TD}><a href="{p["slug"]}.html"><strong>{p["name"]}</strong></a></td>'
                     f'<td {TD}>{badge}</td><td {TD}>{first_sentence(BODY[bk]["weather"])}.</td>'
                     f'<td {TD} style="opacity:.6;">never</td></tr>')
        blocks += (f'<h2 style="border-bottom:2px solid #eb8f00;padding-bottom:3px;">{bk}</h2>'
                   '<table style="width:100%;border-collapse:collapse;font-size:0.92em;margin-bottom:18px;">'
                   f'<thead><tr><th {TH}>Peak</th><th {TH}>Status</th><th {TH}>Latest report</th>'
                   f'<th {TH}>Updated</th></tr></thead><tbody>{rows}</tbody></table>')
    post = ('<div id="post" style="background:#f2efe9;border:1px solid #ddd;border-radius:6px;padding:14px;margin-top:10px;">'
            '<h2 style="margin-top:0;">Post a Condition Update</h2>'
            '<p>Been to a summit lately? You haven&rsquo;t &mdash; nobody has. When the first expedition '
            'returns, this is where it files the beta.</p>'
            f'<button {BTN} onclick="return false;">Post a Condition Update</button></div>')
    inner = ('<div class="overviewText" style="max-width:980px;">Current summit conditions across the solar '
             'system, grouped by body. Spoiler: uniformly hostile.</div><br>' + blocks + post)
    return wrap("Peak Conditions", inner, "Peak Conditions")
page("conditions.html", "Peak Conditions | 29ers.com", LIST_CSS, conditions_page())

# ---- Landing Sites & Status (mirrors Trailheads /trailheadsmain.php) ----
def landing_sites_page():
    bb = peaks_by_body()
    rows = ""
    for bk in BODY_ORDER:
        if bk not in bb:
            continue
        names = ", ".join(p["name"] for p in bb[bk])
        access = "Road / trailhead" if bk == "Earth" else "Spacecraft landing required"
        status = ('<span style="background:#2e7d32;color:#fff;padding:2px 8px;border-radius:9px;font-size:0.8em;">Open</span>'
                  if bk == "Earth" else
                  '<span style="background:#c0392b;color:#fff;padding:2px 8px;border-radius:9px;font-size:0.8em;">No infrastructure</span>')
        rows += (f'<tr><td {TD}><strong>{bk}</strong></td><td {TD}>{names}</td>'
                 f'<td {TD}>{access}</td><td {TD}>{status}</td></tr>')
    post = ('<div id="post" style="background:#f2efe9;border:1px solid #ddd;border-radius:6px;padding:14px;margin-top:10px;">'
            '<h2 style="margin-top:0;">Post a Status Update</h2>'
            '<p>Report a closed landing site, a blocked approach, or a dust storm rolling in.</p>'
            f'<button {BTN} onclick="return false;">Post a Status Update</button></div>')
    inner = ('<div class="overviewText" style="max-width:980px;">Landing sites and approach status for every '
             'body on the list. None has so much as a parking lot &mdash; except one.</div><br>'
             '<table style="width:100%;border-collapse:collapse;font-size:0.92em;">'
             f'<thead><tr><th {TH}>Body</th><th {TH}>Peaks</th><th {TH}>Access</th><th {TH}>Status</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>' + post)
    return wrap("Landing Sites &amp; Status", inner, "Landing Sites &amp; Status")
page("landing-sites.html", "Landing Sites & Status | 29ers.com", LIST_CSS, landing_sites_page())

# ---- Trip Reports (mirrors /tripmain.php chronological feed; empty by gag) ----
def trip_reports_page():
    post = (f'<div id="post" style="margin:10px 0;"><button {BTN} onclick="return false;">Post a Trip Report</button></div>')
    empty = ('<div style="text-align:center;padding:50px 20px;color:#666;border:2px dashed #ccc;border-radius:8px;">'
             '<i class="fa-solid fa-flag" style="font-size:2.4em;color:#eb8f00;"></i>'
             '<h2 style="margin:14px 0 6px;">0 Trip Reports</h2>'
             '<p>No human or robot has ever stood on any of these summits, so there are no trip reports yet.<br>'
             'The first ascents of the solar system&rsquo;s tallest mountains are still out there, waiting.</p>'
             '<p><strong>Be the first &mdash; and file the report here.</strong></p></div>')
    inner = ('<div class="overviewText" style="max-width:980px;">The newest summit trip reports from the 29ers '
             'community.</div><br>' + post + empty)
    return wrap("Trip Reports", inner, "Trip Reports")
page("trip-reports.html", "Trip Reports | 29ers.com", LIST_CSS, trip_reports_page())

# ---- Forum (mirrors /forum category index) ----
def forum_page():
    boards = [
        ("Route Conditions &amp; Beta", "Summit reports, dust storms, and where the ice is."),
        ("Trip Planning &amp; Logistics", "Launch windows, transfer orbits, and ride-shares to Mars."),
        ("Spacesuits &amp; Gear", "Pressure suits, vacuum crampons, and what works at &minus;190&deg;F."),
        ("Off-World General", "Everything else above 29,000 feet."),
        ("The 14ers.com Lounge", "Tip your hat to the Colorado original that started it all."),
    ]
    rows = ""
    for name, desc in boards:
        rows += (f'<tr><td {TD}><i class="fa-solid fa-comments" style="color:#eb8f00;"></i>&nbsp;&nbsp;'
                 f'<strong>{name}</strong><div style="font-size:0.85em;color:#666;">{desc}</div></td>'
                 f'<td {TD} style="text-align:center;">0</td><td {TD} style="text-align:center;">0</td>'
                 f'<td {TD} style="opacity:.6;">Never</td></tr>')
    inner = ('<div class="overviewText" style="max-width:980px;">Welcome to the 29ers.com forum &mdash; the first '
             'community for interplanetary mountaineering. Be the first to post.</div><br>'
             '<table style="width:100%;border-collapse:collapse;font-size:0.95em;">'
             f'<thead><tr><th {TH}>Board</th><th {TH} style="text-align:center;">Topics</th>'
             f'<th {TH} style="text-align:center;">Posts</th><th {TH}>Last post</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>')
    return wrap("Forum", inner, "Forum")
page("forum.html", "Forum | 29ers.com", LIST_CSS, forum_page())

# ---- User Checklists + Checklist Statistics ----
def checklists_page():
    box = '<input type="checkbox" disabled>'
    rows = ""
    for p in PEAKS:
        rows += (f'<tr><td {TD}>{p["rank"]}</td><td {TD}><a href="{p["slug"]}.html">{p["name"]}</a></td>'
                 f'<td {TD}>{p["body"]}</td><td {TD} style="text-align:center;">{box}</td>'
                 f'<td {TD} style="text-align:center;">{box}</td><td {TD} style="text-align:center;">{box}</td></tr>')
    cards = "".join(
        f'<div style="flex:1;min-width:140px;background:#f2efe9;border-radius:6px;padding:14px;text-align:center;">'
        f'<div style="font-size:2em;font-weight:bold;color:#eb8f00;">{v}</div><div>{k}</div></div>'
        for k, v in [("Members", 0), ("Peaks summited", 0), ("Full lists finished", 0), ("Winter ascents", 0)])
    stats = ('<h2 id="stats" style="border-bottom:2px solid #eb8f00;padding-bottom:3px;">Checklist Statistics</h2>'
             f'<div style="display:flex;gap:18px;flex-wrap:wrap;">{cards}</div>')
    inner = ('<div class="overviewText" style="max-width:980px;">Track your ascents of all 13 of the solar '
             'system&rsquo;s 29ers. Log in to tick off peaks, winter ascents, and ski descents.</div><br>'
             '<table style="width:100%;border-collapse:collapse;font-size:0.92em;margin-bottom:22px;">'
             f'<thead><tr><th {TH}>#</th><th {TH}>Peak</th><th {TH}>Body</th>'
             f'<th {TH} style="text-align:center;">Ascent</th><th {TH} style="text-align:center;">Winter</th>'
             f'<th {TH} style="text-align:center;">Ski</th></tr></thead><tbody>{rows}</tbody></table>' + stats)
    return wrap("User Checklists", inner, "User Checklists")
page("checklists.html", "User Checklists | 29ers.com", LIST_CSS, checklists_page())

# ---- Search the Site ----
def search_page():
    items = ""
    for p in PEAKS:
        items += (f'<li style="margin:8px 0;"><a href="{p["slug"]}.html"><strong>{p["name"]}</strong></a> '
                  f'&mdash; {p["body"]}, {p["ht"]} <span style="color:#666;">({p["type"]})</span></li>')
    form = ('<form onsubmit="return false;" style="margin:6px 0 16px;">'
            '<input type="text" placeholder="Search 29ers.com&hellip;" '
            'style="width:68%;max-width:520px;padding:9px 12px;border:1px solid #bbb;border-radius:6px;font-size:1em;">'
            f'<button {BTN} style="margin-left:6px;">Search</button></form>')
    inner = ('<div class="overviewText" style="max-width:980px;">Search peaks, routes, conditions and reports '
             'across 29ers.com.</div>' + form
             + '<h2>All peaks</h2><ul style="list-style:none;padding-left:0;">' + items + '</ul>')
    return wrap("Search", inner, "Search the Site")
page("search.html", "Search | 29ers.com", LIST_CSS, search_page())

# ---- Weather hub (Summit Forecasts + Dust Storm Tracker + Solar Conjunction) ----
def weather_page():
    rows = ""
    for p in PEAKS:
        rows += (f'<tr><td {TD}><a href="{p["slug"]}.html#weather"><strong>{p["name"]}</strong></a></td>'
                 f'<td {TD}>{p["body"]}</td><td {TD}>{first_sentence(BODY[p["bodykey"]]["weather"])}.</td></tr>')
    tools = ('<h2 id="dust" style="border-bottom:2px solid #eb8f00;padding-bottom:3px;">Dust Storm Tracker</h2>'
             '<p>Global and regional dust storms on Mars can blot out a summit for weeks. Current status: '
             '<strong>regional activity on the Tharsis rise.</strong></p>'
             '<h2 id="conjunction" style="border-bottom:2px solid #eb8f00;padding-bottom:3px;">Solar Conjunction</h2>'
             '<p>When a body passes behind the Sun, relay-sat contact drops for days to weeks. Plan your summit '
             'window around it.</p>')
    inner = ('<div class="overviewText" style="max-width:980px;">Summit forecasts for every 29er, plus the '
             'space-weather you won&rsquo;t find on 14ers.com.</div><br>'
             '<h2 style="border-bottom:2px solid #eb8f00;padding-bottom:3px;">Summit Forecasts</h2>'
             '<table style="width:100%;border-collapse:collapse;font-size:0.92em;margin-bottom:18px;">'
             f'<thead><tr><th {TH}>Peak</th><th {TH}>Body</th><th {TH}>Outlook</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>' + tools)
    return wrap("Weather", inner, "Weather &amp; Forecasts")
page("weather.html", "Weather & Forecasts | 29ers.com", LIST_CSS, weather_page())

# ---- The Worlds (reference; absorbs peak-sidebar Name/Discovery/Geology/More Info links) ----
def worlds_page():
    bb = peaks_by_body()
    blocks = ""
    for bk in BODY_ORDER:
        if bk not in bb:
            continue
        links = ", ".join(f'<a href="{p["slug"]}.html">{p["name"]}</a>' for p in bb[bk])
        ml = BODY[bk]["maplink"]
        blocks += (f'<h2 id="{bk.lower()}" style="border-bottom:2px solid #eb8f00;padding-bottom:3px;">'
                   f'{bk} &mdash; {BODY[bk]["ology"]}</h2>'
                   f'<p>{BODY[bk]["weather"]}</p>'
                   f'<p><strong>29ers on {bk}:</strong> {links}.</p>'
                   f'<p><a href="{ml[1]}" rel="noopener">{ml[0]} <i class="fas fa-external-link-alt"></i></a></p>')
    inner = ('<div class="overviewText" style="max-width:980px;">A field primer on the worlds that host the solar '
             'system&rsquo;s tallest mountains &mdash; their geology, names, discovery and hazards.</div><br>' + blocks)
    return wrap("The Worlds", inner, "The Worlds")
page("worlds.html", "The Worlds | 29ers.com", LIST_CSS, worlds_page())

# ---- GPX Library (gated, mirrors the login-required /gpxlib_main.php) ----
def gpx_page():
    inner = ('<div style="max-width:620px;margin:30px auto;text-align:center;background:#f2efe9;border:1px solid #ddd;'
             'border-radius:8px;padding:34px;"><i class="fa-solid fa-lock" style="font-size:2.2em;color:#eb8f00;"></i>'
             '<h2 style="margin:14px 0 6px;">Members only</h2>'
             '<p>The GPX Library holds relay-sat GPS tracks for every standard route. Like the original 14ers.com '
             'library, downloads require a (free) account.</p>'
             f'<a {BTN} href="login.html">Log in to download</a></div>')
    return wrap("GPX Library", inner, "GPX Library")
page("gpx.html", "GPX Library | 29ers.com", LIST_CSS, gpx_page())

# ---- Log In ----
def login_page():
    inner = ('<div style="max-width:420px;margin:24px auto;background:#f2efe9;border:1px solid #ddd;border-radius:8px;padding:26px;">'
             '<form onsubmit="return false;">'
             '<label style="display:block;font-weight:bold;color:#633;margin-bottom:3px;">Email</label>'
             '<input type="text" style="width:100%;padding:8px;margin-bottom:12px;border:1px solid #bbb;border-radius:5px;">'
             '<label style="display:block;font-weight:bold;color:#633;margin-bottom:3px;">Password</label>'
             '<input type="password" style="width:100%;padding:8px;margin-bottom:16px;border:1px solid #bbb;border-radius:5px;">'
             f'<button {BTN} style="width:100%;">Log In</button></form>'
             '<p style="font-size:0.85em;color:#666;margin-top:14px;">Accounts aren&rsquo;t real on this parody &mdash; '
             'but the mountains are. <a href="about.html">What are 29ers?</a></p></div>')
    return wrap("Log In", inner, "Log In")
page("login.html", "Log In | 29ers.com", LIST_CSS, login_page())

# ---- Relay-Sat Reception (mirrors Cell Phone Reception) ----
def reception_page():
    bb = peaks_by_body()
    delays = {"Mars": "3&ndash;22 min", "Io": "33&ndash;53 min", "Venus": "2&ndash;14 min",
              "Vesta": "9&ndash;25 min", "Iapetus": "68&ndash;84 min", "Earth": "under 1 sec"}
    rows = ""
    for bk in BODY_ORDER:
        if bk not in bb:
            continue
        rows += f'<tr><td {TD}><strong>{bk}</strong></td><td {TD}>{delays.get(bk, "varies")}</td></tr>'
    inner = ('<div class="overviewText" style="max-width:820px;">There is no cell signal on any of these peaks. '
             'Comms go through orbital relay satellites &mdash; with a one-way light delay measured in minutes, not '
             'bars.</div><br><table style="width:60%;min-width:300px;border-collapse:collapse;">'
             f'<thead><tr><th {TH}>Body</th><th {TH}>One-way signal delay (from Earth)</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>')
    return wrap("Relay-Sat Reception", inner, "Relay-Sat Reception")
page("reception.html", "Relay-Sat Reception | 29ers.com", LIST_CSS, reception_page())

# ---- User Climb Times ----
def climb_times_page():
    inner = ('<div style="text-align:center;padding:50px 20px;color:#666;border:2px dashed #ccc;border-radius:8px;max-width:760px;margin:0 auto;">'
             '<i class="fa-solid fa-stopwatch" style="font-size:2.2em;color:#eb8f00;"></i>'
             '<h2 style="margin:14px 0 6px;">No climb times logged</h2>'
             '<p>Member climb times will appear here once someone records an ascent. Current record on every peak: '
             '<strong>unset</strong>.</p></div>')
    return wrap("User Climb Times", inner, "User Climb Times")
page("climb-times.html", "User Climb Times | 29ers.com", LIST_CSS, climb_times_page())

# ============================ PROSE ARTICLE PAGES (mirror /about, /difficultyratings.php, etc.) ============================
def article_body(a):
    secs = "".join(f'<h2>{h}</h2>\n{html}\n' for h, html in a["sections"])
    inner = f'<div class="overviewText" style="max-width:900px;">{a["lead"]}<br><br>{secs}</div>'
    return wrap(a["title"], inner, a["title"])

ARTICLES = [
 dict(slug="difficulty", title="Difficulty Rating System",
   lead="29ers.com extends the familiar Colorado class system to the rest of the solar system.",
   sections=[
     ("The classes", "<ul class='bullet1'><li><strong>Class 1</strong> &mdash; a walk-up. On this list, only the road up <a href='mauna-kea.html'>Mauna Kea</a>.</li>"
       "<li><strong>Class 2&ndash;3</strong> &mdash; steep hiking and scrambling. <a href='mount-everest.html'>Everest</a> lives here.</li>"
       "<li><strong>Class 4&ndash;5</strong> &mdash; exposed climbing; ropes advisable.</li>"
       "<li><strong>Class 6</strong> &mdash; <em>spacecraft and a pressure suit required.</em> Vacuum, radiation, and &minus;190&deg;F. Every off-world route on this site.</li></ul>"),
     ("Why Class 6?", "<p>No Colorado peak needs life support; every 29er beyond Earth does. Class 6 simply admits that the crux is getting there alive.</p>"),
   ]),
 dict(slug="faq", title="29er FAQ",
   lead="Common questions about the solar system&rsquo;s tallest mountains.",
   sections=[
     ("What is a 29er?", "<p>Any mountain in the solar system that rises at least ~29,000 ft base-to-summit &mdash; the height of Mount Everest. See <a href='about.html'>What are 29ers?</a></p>"),
     ("Has anyone climbed one?", "<p>No. Recorded ascents across all 13 peaks: zero. The first ascents are unclaimed.</p>"),
     ("How are heights measured?", "<p>Base-to-peak, since most of these worlds have no sea level &mdash; that&rsquo;s how <a href='mauna-kea.html'>Mauna Kea</a> out-tops Everest.</p>"),
   ]),
 dict(slug="climbing", title="Climbing 29ers",
   lead="New to interplanetary mountaineering? Start here.",
   sections=[
     ("Getting started", "<p>Pick a peak from the <a href='peaks.html'>list</a>, study its <a href='routes.html'>route</a> and <a href='conditions.html'>conditions</a>, and assemble a launch vehicle. The summit push is the easy part; the hundred-million-mile drive to the trailhead is not.</p>"),
     ("Fitness &amp; acclimatization", "<p>Microgravity deconditioning, not altitude, is the enemy. Train for months in transit, then expect a summit day measured in slow, low-gravity bounds.</p>"),
   ]),
 dict(slug="safety", title="Mountaineering Safety",
   lead="The hazards out here are unlike anything in Colorado.",
   sections=[
     ("The big four", "<ul class='bullet1'><li><strong>Vacuum</strong> &mdash; a suit breach is fatal in seconds.</li>"
       "<li><strong>Radiation</strong> &mdash; especially in Jupiter&rsquo;s belts around <a href='boosaule-montes.html'>Io</a>.</li>"
       "<li><strong>Cold</strong> &mdash; routinely below &minus;150&deg;F.</li>"
       "<li><strong>Low gravity</strong> &mdash; a careless step on <a href='rheasilvia.html'>Vesta</a> can approach escape velocity.</li></ul>"),
     ("Leave no trace", "<p>These are pristine worlds mapped only by robots. Pack out everything &mdash; including yourself.</p>"),
   ]),
 dict(slug="gear", title="Spacesuit &amp; Gear List",
   lead="What to bring when the trailhead is in a hard vacuum.",
   sections=[
     ("Essentials", "<ul class='bullet1'><li>Pressure suit + life support, rated for your destination&rsquo;s temperature and radiation</li>"
       "<li>Crampons that bite regolith and water ice</li><li>Relay-sat comms (no <a href='reception.html'>cell signal</a> exists)</li>"
       "<li>Days-to-weeks of consumables &mdash; summit pushes run long in low gravity</li></ul>"),
     ("Leave at home", "<p>Down jackets do nothing in a vacuum, and your phone won&rsquo;t find a bar.</p>"),
   ]),
 dict(slug="aphelion", title="Climbing 29ers in Aphelion",
   lead="A niche art: timing an ascent for when a body is farthest from the Sun.",
   sections=[
     ("Why bother?", "<p>At aphelion you get the longest, coldest nights and the weakest sunlight &mdash; brutal for warmth, but good for thermal stability on Mars&rsquo;s <a href='olympus-mons.html'>Tharsis</a> shields and for dodging peak dust-storm season.</p>"),
     ("The catch", "<p>Aphelion also means the longest comms delay and the longest ride home. Plan accordingly.</p>"),
   ]),
 dict(slug="support", title="Support 29ers.com",
   lead="29ers.com is a free, non-commercial parody &mdash; built for the love of big mountains.",
   sections=[("How to help", "<p>Support the real <a href='https://www.14ers.com' rel='noopener'>14ers.com</a> that inspired this, and the NASA/ESA missions whose imagery makes it possible. That&rsquo;s the only donation we&rsquo;ll ever ask for.</p>")]),
 dict(slug="store", title="29ers.com Store",
   lead="The 29ers.com gift shop.",
   sections=[("Coming soon", "<p>Summit pennants for peaks nobody has summited, pressure-suit patches, and &ldquo;I climbed all thirteen&rdquo; mugs (aspirational). The store opens after the first ascent.</p>")]),
 dict(slug="contact", title="Contact Site Admin",
   lead="Questions, corrections, or a first-ascent claim to report?",
   sections=[("Get in touch", "<p>This is a parody built by <a href='https://spencerboucher.com' rel='noopener'>Spencer Boucher</a> &mdash; reach out there. For the real Colorado fourteeners, see <a href='https://www.14ers.com' rel='noopener'>14ers.com</a>.</p>")]),
 dict(slug="privacy", title="Privacy",
   lead="The short version.",
   sections=[("What we collect", "<p>Nothing. 29ers.com is a static parody with no accounts, no tracking, and no analytics. The only data leaving your browser goes to NASA/Wikimedia for shared CSS, fonts, and image links.</p>")]),
 dict(slug="app", title="Mission App",
   lead="The 29ers.com field app &mdash; for when your trailhead is on another planet.",
   sections=[("On the roadmap", "<p>Offline peak data, relay-sat forecast sync, and a summit log that works at &minus;190&deg;F. Until the first crewed expedition, it lives here on the web. Browse the <a href='peaks.html'>peaks</a> to get started.</p>")]),
]
for a in ARTICLES:
    page(f'{a["slug"]}.html', f'{a["title"]} | 29ers.com', LIST_CSS, article_body(a))

SECTION_PAGES = 14  # routes, route-selector, conditions, landing-sites, trip-reports, forum,
                    # checklists, search, weather, worlds, gpx, login, reception, climb-times
print("done. generated", NPEAKS, "peak pages + index + about +",
      SECTION_PAGES + len(ARTICLES), "spoof section/article pages")
