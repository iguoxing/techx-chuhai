/* 文章页：渲染内联 Markdown、生成目录、阅读进度 */
(function () {
  var srcEl = document.getElementById('post-source');
  var body = document.getElementById('post-content');
  if (!srcEl || !body) return;

  var md = '';
  try { md = JSON.parse(srcEl.textContent); } catch (e) { md = srcEl.textContent; }

  if (!window.marked) {
    body.innerHTML = '<p class="noscript">Markdown 渲染组件未加载，请刷新页面重试。</p>';
    return;
  }
  var parse = typeof window.marked === 'function'
    ? window.marked
    : (window.marked.parse ? window.marked.parse.bind(window.marked) : null);
  if (!parse) return;

  body.classList.add('md');
  body.innerHTML = parse(md, { gfm: true, breaks: false });

  // 外链新窗口打开；图片懒加载
  Array.prototype.forEach.call(body.querySelectorAll('a[href^="http"]'), function (a) {
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');
  });
  Array.prototype.forEach.call(body.querySelectorAll('img'), function (img) {
    img.setAttribute('loading', 'lazy');
  });

  // 生成目录
  var tocBox = document.getElementById('toc-list');
  var heads = Array.prototype.slice.call(body.querySelectorAll('h2, h3'));
  if (tocBox && heads.length) {
    var html = '';
    heads.forEach(function (h, i) {
      var id = 'sec-' + (i + 1);
      h.setAttribute('id', id);
      var text = (h.textContent || '').trim().replace(/\s+/g, ' ');
      html += '<li class="' + (h.tagName === 'H3' ? 'lv3' : '') + '"><a href="#' + id + '" data-target="' + id + '">' +
              (text.length > 22 ? text.slice(0, 22) + '…' : text) + '</a></li>';
    });
    tocBox.innerHTML = html;
    Array.prototype.forEach.call(tocBox.querySelectorAll('a'), function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var el = document.getElementById(a.getAttribute('data-target'));
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  } else if (tocBox) {
    var toc = document.getElementById('toc');
    if (toc) toc.style.display = 'none';
  }

  // 阅读进度 + 目录高亮
  var bar = document.getElementById('progress');
  function onScroll() {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.width = (h > 0 ? Math.min(100, Math.max(0, window.scrollY / h * 100)) : 0) + '%';
    if (!tocBox || !heads.length) return;
    var current = null;
    heads.forEach(function (el) {
      if (el.getBoundingClientRect().top <= 120) current = el.id;
    });
    Array.prototype.forEach.call(tocBox.querySelectorAll('a'), function (a) {
      a.classList.toggle('active', a.getAttribute('data-target') === current);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();
