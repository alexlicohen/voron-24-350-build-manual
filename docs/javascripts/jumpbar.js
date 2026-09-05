/* R6 B9 — Sticky section jump bar for long chapters.
 * Lists each chapter's `##` sections (including "Part A" / "Part B") as
 * chips in a horizontal bar under the header; the active chip highlights on
 * scroll. Hidden entirely when a chapter has fewer than 3 sections. Sticky
 * positioning and 44px tap targets are CSS-only (docs/stylesheets/extra.css).
 */
(function () {
  var observer = null;

  function buildJumpBar() {
    var old = document.querySelector('.jump-bar');
    if (old) old.remove();
    if (observer) {
      observer.disconnect();
      observer = null;
    }

    var content = document.querySelector('.md-content__inner');
    if (!content) return;

    var sections = Array.prototype.filter.call(content.querySelectorAll('h2'), function (h) {
      return !!h.id;
    });
    if (sections.length < 3) return;

    var bar = document.createElement('nav');
    bar.className = 'jump-bar';
    bar.setAttribute('aria-label', 'Jump to section');

    var chips = sections.map(function (h) {
      var a = document.createElement('a');
      a.className = 'jump-bar__chip';
      a.href = '#' + h.id;
      a.textContent = (h.textContent || '').trim();
      bar.appendChild(a);
      return { link: a, target: h };
    });

    content.insertBefore(bar, content.firstChild);

    function setActive(target) {
      chips.forEach(function (c) {
        c.link.classList.toggle('jump-bar__chip--active', c.target === target);
      });
    }

    if ('IntersectionObserver' in window) {
      observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              var chip = chips.filter(function (c) {
                return c.target === entry.target;
              })[0];
              if (chip) setActive(chip.target);
            }
          });
        },
        { rootMargin: '-88px 0px -70% 0px', threshold: 0 }
      );
      sections.forEach(function (h) {
        observer.observe(h);
      });
    }

    setActive(sections[0]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildJumpBar);
  } else {
    buildJumpBar();
  }

  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(buildJumpBar);
  }
})();
