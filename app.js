/* 29ers.com - minimal behaviour for the static spoof (vanilla JS, no deps) */

/* Mobile hamburger: toggle the mega-menu open/closed */
function menuExpand() {
  var menu = document.getElementById('siteheader-menuwrap');
  var ham = document.getElementById('hamburger');
  if (menu) menu.classList.toggle('menu-mobile');
  if (ham) ham.classList.toggle('is-active');
  return false;
}

/* Peak overview "Read more" toggle */
function readMore() {
  var more = document.getElementById('moreText');
  var btn = document.getElementById('moreButton');
  if (!more) return;
  var hidden = (more.style.display === 'none' || more.style.display === '');
  more.style.display = hidden ? 'inline' : 'none';
  if (btn) btn.textContent = hidden ? 'Read less' : 'Read more';
}

/* Peak-page tabs: show one content panel, check its radio */
function showTab(n) {
  var group = document.getElementById('tabGroup');
  if (!group) return;
  group.querySelectorAll('.content').forEach(function (c) { c.style.display = 'none'; });
  var panel = document.getElementById('tab' + n + '-content');
  if (panel) panel.style.display = 'block';
  var radio = document.getElementById('tab' + n);
  if (radio) radio.checked = true;
}

/* Peak-list sorting via the "Sort By" select */
function sortPeaks() {
  var sel = document.getElementById('sort');
  var cont = document.getElementById('peak-container');
  if (!sel || !cont) return;
  var key = sel.value;
  var cards = Array.prototype.slice.call(cont.querySelectorAll('.peak-card'));
  cards.sort(function (a, b) {
    var d = a.dataset, e = b.dataset;
    switch (key) {
      case 'elevation': return (+e.elevation - +d.elevation) || (+d.rank - +e.rank);
      case 'rank':      return (+d.rank - +e.rank);
      case 'ascents':   return (+e.ascents - +d.ascents) || (+d.rank - +e.rank);
      case 'name':      return d.name.localeCompare(e.name);
      case 'mrange':    return d.mrange.localeCompare(e.mrange);
      case 'planet':    return d.planet.localeCompare(e.planet) || (+d.rank - +e.rank);
      default:          return 0;
    }
  });
  cards.forEach(function (c) { cont.appendChild(c); });
}

/* Home hero: pick one of the backgrounds per page load, like the real site does server-side */
var HERO_BACKGROUNDS = [
  'images/backgrounds/olympus-scarp.jpg',
  'images/backgrounds/mount-sharp.jpg',
  'images/backgrounds/gale-vista.jpg'
];

function pickHeroBackground() {
  var main = document.getElementById('main');
  if (!main || !main.style.background) return;
  var pick = HERO_BACKGROUNDS[Math.floor(Math.random() * HERO_BACKGROUNDS.length)];
  main.style.background = 'linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, .15)), url(' + pick + ')';
}

/* Field Guide carousel: 3D dial of phone-sized screenshots.
   Positions are classes (is-center, is-left-1..3, is-right-1..3) that homeindex_main.css
   turns into the scaled/offset transforms; we only decide which item gets which class. */
function initFieldGuideDial() {
  var root = document.getElementById('mobileAppDial');
  if (!root) return;
  var items = Array.prototype.slice.call(root.querySelectorAll('.photoDial-item'));
  if (!items.length) return;
  var attribution = document.getElementById('mobileAppDialAttribution');
  var headerEl = document.getElementById('mobileAppDialCaptionHeader');
  var textEl = document.getElementById('mobileAppDialCaptionText');
  var active = 0;

  function render() {
    var len = items.length;
    active = ((active % len) + len) % len;
    items.forEach(function (item, i) {
      var delta = i - active;
      if (delta > len / 2) delta -= len;
      if (delta < -len / 2) delta += len;
      item.className = 'photoDial-item';
      if (delta === 0) item.classList.add('is-center');
      else if (Math.abs(delta) <= 3) {
        item.classList.add('is-' + (delta < 0 ? 'left' : 'right') + '-' + Math.abs(delta));
      }
    });
    if (headerEl) headerEl.textContent = items[active].dataset.header || '';
    if (textEl) textEl.textContent = items[active].dataset.caption || '';
    if (attribution) attribution.style.display = active === 0 ? '' : 'none';
  }

  function go(step) { active += step; render(); }

  var prev = root.querySelector('.photoDial-prev');
  var next = root.querySelector('.photoDial-next');
  if (prev) prev.addEventListener('click', function (e) { e.preventDefault(); go(-1); });
  if (next) next.addEventListener('click', function (e) { e.preventDefault(); go(1); });

  /* Clicking a side item centers it rather than following its link */
  items.forEach(function (item, i) {
    item.addEventListener('click', function (e) {
      if (!item.classList.contains('is-center')) {
        e.preventDefault();
        active = i;
        render();
      }
    });
  });

  render();
}

document.addEventListener('DOMContentLoaded', function () {
  var sel = document.getElementById('sort');
  if (sel) sel.addEventListener('change', sortPeaks);

  pickHeroBackground();
  initFieldGuideDial();

  /* Deep-link straight to the Weather tab via #weather */
  if (window.location.hash === '#weather' && document.getElementById('tab5-content')) {
    showTab(5);
  }
});
