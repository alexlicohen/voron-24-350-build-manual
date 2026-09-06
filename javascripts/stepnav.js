/* Step-page navigation: ← / → keys and a horizontal swipe move between the
 * generated step pages. The links themselves are static markup emitted by
 * scripts/build_steps.py, so navigation never depends on nav order or JS.
 */
(function () {
  var bound = false;

  function link(which) {
    var a = document.querySelector('.step-nav__' + which + '[href]');
    return a && a.getAttribute('href') ? a : null;
  }

  function go(which) {
    var a = link(which);
    if (a) a.click();
  }

  function typing(el) {
    if (!el) return false;
    var tag = (el.tagName || '').toLowerCase();
    return tag === 'input' || tag === 'textarea' || tag === 'select' || el.isContentEditable;
  }

  function onKey(e) {
    if (!document.querySelector('.step-nav')) return;
    if (e.metaKey || e.ctrlKey || e.altKey || e.shiftKey) return;
    if (typing(e.target)) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); go('next'); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); go('prev'); }
  }

  var x0 = null, y0 = null, t0 = 0;

  function onStart(e) {
    if (e.touches.length !== 1) { x0 = null; return; }
    x0 = e.touches[0].clientX;
    y0 = e.touches[0].clientY;
    t0 = Date.now();
  }

  function onEnd(e) {
    if (x0 === null || !document.querySelector('.step-nav')) return;
    var t = e.changedTouches && e.changedTouches[0];
    if (!t) return;
    var dx = t.clientX - x0;
    var dy = t.clientY - y0;
    x0 = null;
    if (Date.now() - t0 > 700) return;
    if (Math.abs(dx) < 70 || Math.abs(dx) < Math.abs(dy) * 2) return;
    // Never hijack a swipe that started inside something scrollable sideways.
    var el = t.target;
    while (el && el !== document.body) {
      if (el.scrollWidth > el.clientWidth + 4) return;
      el = el.parentElement;
    }
    go(dx < 0 ? 'next' : 'prev');
  }

  function mount() {
    if (bound) return;
    bound = true;
    document.addEventListener('keydown', onKey);
    document.addEventListener('touchstart', onStart, { passive: true });
    document.addEventListener('touchend', onEnd, { passive: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
