/* Troubleshooting decision tree (R7 F4).
 *
 * `hooks/gatecalc.py` wraps a ```tap-tree fence in
 *   <div class="tap-tree" markdown="1"> …the nested list… </div>
 * so Python-Markdown renders an ordinary nested <ul> (and mkdocs rewrites and
 * validates every relative link inside it). This file reads that <ul>, hides
 * it, and draws the same tree as tappable cards with a breadcrumb and Back.
 *
 * No content lives here: a leaf's paragraph and its step link are whatever the
 * list already said. With JavaScript off the list stays visible and usable.
 */
(function () {
  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  var BLOCK = { P: 1, BLOCKQUOTE: 1, TABLE: 1, PRE: 1, DIV: 1 };

  /* An <li> is: a label, an optional body (the leaf paragraph), and optional
   * children. Python-Markdown renders a tight item as bare inline content and
   * a loose one as <p> blocks, so both shapes are handled. */
  function readItem(li) {
    var kids = [];
    var labelHtml = '';
    var bodyHtml = '';
    var seenBlock = false;

    Array.prototype.forEach.call(li.childNodes, function (node) {
      if (node.nodeType === 1 && (node.tagName === 'UL' || node.tagName === 'OL')) {
        kids = kids.concat(readList(node));
        return;
      }
      if (node.nodeType === 1 && BLOCK[node.tagName]) {
        if (!seenBlock && !labelHtml.trim()) labelHtml = node.innerHTML;
        else bodyHtml += node.outerHTML;
        seenBlock = true;
        return;
      }
      var html = node.nodeType === 1 ? node.outerHTML : node.nodeValue;
      if (seenBlock) { if (html && html.trim()) bodyHtml += html; }
      else labelHtml += html;
    });

    return {
      label: labelHtml.trim(),
      body: bodyHtml.trim(),
      children: kids
    };
  }

  function readList(list) {
    return Array.prototype.filter.call(list.children, function (n) {
      return n.tagName === 'LI';
    }).map(readItem).filter(function (item) {
      return item.label;
    });
  }

  function build(root) {
    if (root.dataset.tapTreeMounted) return;
    var list = root.querySelector('ul, ol');
    if (!list) return;
    var tree = readList(list);
    if (!tree.length) return;
    root.dataset.tapTreeMounted = '1';

    var ui = el('div', 'tap-tree__ui');
    var crumbs = el('nav', 'tap-tree__crumbs');
    crumbs.setAttribute('aria-label', 'Where you are in the tree');
    var cards = el('div', 'tap-tree__cards');
    var leaf = el('div', 'tap-tree__leaf');
    ui.appendChild(crumbs);
    ui.appendChild(cards);
    ui.appendChild(leaf);
    root.insertBefore(ui, list);
    list.classList.add('tap-tree__source');

    var path = [];

    function nodesAt(depth) {
      var level = tree;
      for (var i = 0; i < depth; i++) level = level[path[i]].children;
      return level;
    }

    function current() {
      return path.length ? nodesAt(path.length - 1)[path[path.length - 1]] : null;
    }

    function crumb(text, depth) {
      var b = el('button', 'tap-tree__crumb', text);
      b.type = 'button';
      b.addEventListener('click', function () {
        path = path.slice(0, depth);
        render();
      });
      return b;
    }

    function render() {
      crumbs.textContent = '';
      crumbs.appendChild(crumb('Start', 0));
      path.forEach(function (idx, depth) {
        crumbs.appendChild(el('span', 'tap-tree__sep', '›'));
        var node = nodesAt(depth)[idx];
        var b = crumb('', depth + 1);
        b.innerHTML = node.label;
        crumbs.appendChild(b);
      });
      if (path.length) {
        var back = el('button', 'tap-tree__back', '← Back');
        back.type = 'button';
        back.addEventListener('click', function () { path.pop(); render(); });
        crumbs.appendChild(back);
      }

      var node = current();
      var level = node ? node.children : tree;

      leaf.textContent = '';
      if (node && node.body) {
        leaf.innerHTML = node.body;
        leaf.hidden = false;
      } else {
        leaf.hidden = true;
      }

      cards.textContent = '';
      cards.hidden = !level.length;
      level.forEach(function (child, idx) {
        var card = el('button', 'tap-card');
        card.type = 'button';
        var text = el('span', 'tap-card__label');
        text.innerHTML = child.label;
        card.appendChild(text);
        if (child.children.length) card.appendChild(el('span', 'tap-card__more', '›'));
        card.addEventListener('click', function () {
          path.push(idx);
          render();
          ui.scrollIntoView({ block: 'nearest' });
        });
        cards.appendChild(card);
      });
    }

    render();
  }

  function mount() {
    document.querySelectorAll('.tap-tree').forEach(build);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }

  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(mount);
  }
})();
