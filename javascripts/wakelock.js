/* R5 F10/B5 — Screen Wake Lock toggle for bench mode.
 * Adds a header button that keeps the screen on while the manual is open.
 * Re-acquires the lock on visibilitychange (the OS drops it whenever the
 * tab/app is backgrounded). Degrades silently where unsupported (iPadOS
 * Safari < 16.4, or 16.4-18.3 inside a Home Screen standalone web app —
 * see docs/index.md "Bench mode").
 */
(function () {
  if (!('wakeLock' in navigator)) return;

  var lock = null;
  var want = false;

  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'md-header__button md-icon wakelock-toggle';
  btn.style.cssText =
    'min-width:44px;min-height:44px;font:inherit;background:none;border:0;color:inherit;cursor:pointer';
  btn.title = 'Keep screen awake';
  btn.setAttribute('aria-label', 'Keep screen awake');

  function paint() {
    btn.textContent = want ? '☀' : '☼'; // filled / outline sun
    btn.setAttribute('aria-pressed', String(want));
    btn.title = want ? 'Screen will stay awake (tap to allow sleep)' : 'Keep screen awake';
  }

  async function acquire() {
    try {
      lock = await navigator.wakeLock.request('screen');
      lock.addEventListener('release', function () {
        lock = null;
      });
    } catch (e) {
      // Denied, low battery, or unsupported in this context (e.g. standalone
      // Home Screen app on iPadOS < 18.4) — degrade silently.
      want = false;
    }
    paint();
  }

  btn.addEventListener('click', async function () {
    want = !want;
    if (want) {
      await acquire();
    } else if (lock) {
      await lock.release();
      lock = null;
      paint();
    } else {
      paint();
    }
  });

  document.addEventListener('visibilitychange', function () {
    if (want && !lock && document.visibilityState === 'visible') acquire();
  });

  function mount() {
    var host =
      document.querySelector('.md-header__inner .md-header__option') ||
      document.querySelector('.md-header__inner .md-header__source') ||
      document.querySelector('.md-header__inner');
    if (host && host.parentNode && !document.querySelector('.wakelock-toggle')) {
      host.parentNode.insertBefore(btn, host);
      paint();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }

  // Material re-renders parts of the header on instant-navigation; re-mount if lost.
  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(mount);
  }
})();
