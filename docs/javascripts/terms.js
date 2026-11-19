/* Tap a dotted-underlined word on a plain-style step page to read its glossary
   line. The page carries the meaning in <abbr title> (scripts/build_steps.py
   term_defs, from 16-glossary.md); a touch screen never shows a title, so this
   puts it in a small bubble. One bubble at a time; any other tap closes it. */
(function () {
  var bubble = null;

  function close() {
    if (bubble) { bubble.remove(); bubble = null; }
  }

  document.addEventListener("click", function (ev) {
    var el = ev.target.closest ? ev.target.closest("abbr[title], abbr[data-term]") : null;
    var was = bubble && bubble._for;
    close();
    if (!el || el === was) return;
    if (el.closest("a")) return;            /* inside a link: let the link work */
    if (el.hasAttribute("title")) {         /* keep it, minus the native tooltip */
      el.setAttribute("data-term", el.getAttribute("title"));
      el.removeAttribute("title");
    }
    bubble = document.createElement("div");
    bubble.className = "term-bubble";
    bubble.setAttribute("role", "tooltip");
    var name = document.createElement("strong");
    name.textContent = el.textContent;
    bubble.appendChild(name);
    bubble.appendChild(document.createTextNode(" " + el.getAttribute("data-term")));
    bubble._for = el;
    document.body.appendChild(bubble);
    var r = el.getBoundingClientRect();
    var w = Math.min(340, window.innerWidth - 24);
    bubble.style.width = w + "px";
    var left = Math.max(12, Math.min(r.left, window.innerWidth - w - 12));
    bubble.style.left = (left + window.scrollX) + "px";
    var below = r.bottom + 8 + bubble.offsetHeight < window.innerHeight - 110;
    var top = below ? r.bottom + 8 : r.top - 8 - bubble.offsetHeight;
    bubble.style.top = (top + window.scrollY) + "px";
    ev.stopPropagation();
  });

  window.addEventListener("resize", close);
})();
