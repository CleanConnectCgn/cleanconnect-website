/* Google Maps wird erst nach ausdruecklicher Einwilligung geladen (Art. 6 Abs. 1 lit. a DSGVO, § 25 TDDDG). */
(function () {
  var STYLE = [
    '.cc-map{position:relative;display:block;min-height:inherit}',
    '.cc-map iframe{display:block;width:100%}',
    '.cc-map-veil{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;',
    'padding:20px;text-align:center;background:#1a1a1a;border:1px solid #2a2a2a;border-radius:14px;z-index:2}',
    '.cc-map-veil p{margin:0;font-size:13px;line-height:1.6;color:#999;max-width:34ch}',
    '.cc-map-veil a{color:#00C5C4}',
    '.cc-map-veil button{appearance:none;border:0;cursor:pointer;font:600 13px/1 inherit;color:#111;background:#00C5C4;',
    'padding:10px 18px;border-radius:8px}',
    '.cc-map-veil button:hover{filter:brightness(1.08)}'
  ].join('');

  function injectStyle() {
    if (document.getElementById('cc-map-style')) return;
    var s = document.createElement('style');
    s.id = 'cc-map-style';
    s.textContent = STYLE;
    document.head.appendChild(s);
  }

  function load(frame, veil) {
    frame.src = frame.getAttribute('data-src');
    if (veil && veil.parentNode) veil.parentNode.removeChild(veil);
  }

  function privacyHref() {
    return document.querySelector('a[href$="datenschutz.html"]')
      ? document.querySelector('a[href$="datenschutz.html"]').getAttribute('href')
      : 'datenschutz.html';
  }

  function init() {
    var frames = document.querySelectorAll('.cc-map iframe[data-src]');
    if (!frames.length) return;
    injectStyle();

    Array.prototype.forEach.call(frames, function (frame) {
      var wrap = frame.closest('.cc-map');

      if (sessionStorage.getItem('cc-maps-ok') === '1') {
        load(frame, null);
        return;
      }

      var veil = document.createElement('div');
      veil.className = 'cc-map-veil';

      var text = document.createElement('p');
      text.innerHTML = 'Hier wird eine Karte von Google Maps eingebunden. Beim Laden werden Daten ' +
        'an Google übertragen. Näheres in unserer <a href="' + privacyHref() + '">Datenschutzerklärung</a>.';

      var btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = 'Karte laden';
      btn.addEventListener('click', function () {
        try { sessionStorage.setItem('cc-maps-ok', '1'); } catch (e) {}
        load(frame, veil);
      });

      veil.appendChild(text);
      veil.appendChild(btn);
      wrap.appendChild(veil);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
