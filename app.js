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

document.addEventListener('DOMContentLoaded', function () {
  var sel = document.getElementById('sort');
  if (sel) sel.addEventListener('change', sortPeaks);

  /* Deep-link straight to the Weather tab via #weather */
  if (window.location.hash === '#weather' && document.getElementById('tab5-content')) {
    showTab(5);
  }
});
