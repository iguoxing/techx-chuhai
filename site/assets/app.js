/* 首页：分类 / 标签 / 搜索 / 主题。数据直接内联在页面里，无需 fetch，file:// 也能打开 */
(function () {
  var dataEl = document.getElementById('site-data');
  if (!dataEl) return;
  var data;
  try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }

  var posts = data.posts || [];
  var categories = data.categories || [];
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };

  // Hero 统计
  if ($('stat-posts')) $('stat-posts').textContent = posts.length;
  if ($('stat-cats')) $('stat-cats').textContent = categories.filter(function (c) { return c.count > 0; }).length;
  if ($('stat-updated')) $('stat-updated').textContent = data.updated || '—';

  var params = new URLSearchParams(location.search);
  var state = { q: params.get('q') || '', cat: params.get('c') || '' };
  var input = $('search-input');
  if (input) input.value = state.q;

  function syncUrl() {
    var p = new URLSearchParams();
    if (state.q) p.set('q', state.q);
    if (state.cat) p.set('c', state.cat);
    var s = p.toString();
    try { history.replaceState(null, '', s ? '?' + s : location.pathname); } catch (e) {}
  }

  function renderChips() {
    var box = $('chips');
    if (!box) return;
    var html = '<button class="chip' + (state.cat ? '' : ' active') + '" data-cat="">全部 <span class="n">' + posts.length + '</span></button>';
    categories.forEach(function (c) {
      if (!c.count) return;
      html += '<button class="chip' + (state.cat === c.name ? ' active' : '') + '" data-cat="' + esc(c.name) + '">' +
              esc(c.name) + ' <span class="n">' + c.count + '</span></button>';
    });
    box.innerHTML = html;
    Array.prototype.forEach.call(box.querySelectorAll('.chip'), function (btn) {
      btn.addEventListener('click', function () {
        state.cat = btn.getAttribute('data-cat') || '';
        syncUrl(); render();
      });
    });
  }

  function match(p) {
    if (state.cat && p.category !== state.cat) return false;
    if (!state.q) return true;
    var q = state.q.trim().toLowerCase();
    if (!q) return true;
    var hay = [p.title, p.summary, p.category, (p.tags || []).join(' ')].join(' ').toLowerCase();
    return hay.indexOf(q) !== -1;
  }

  function render() {
    renderChips();
    var list = posts.filter(match);
    var box = $('posts');
    var count = $('result-count');
    if (count) count.textContent = '共 ' + list.length + ' 篇';
    if (!box) return;

    if (!list.length) {
      box.innerHTML = '<div class="empty"><b>没找到相关文章</b>换个关键词，或者点「全部」看看其他栏目</div>';
      return;
    }

    box.innerHTML = list.map(function (p, i) {
      var tags = (p.tags || []).slice(0, 3).map(function (t) {
        return '<span class="tag" data-tag="' + esc(t) + '">#' + esc(t) + '</span>';
      }).join('');
      return '<a class="card" href="' + esc(p.url) + '" style="animation-delay:' + Math.min(i, 9) * 35 + 'ms">' +
               '<div class="card-top"><span class="cat">' + esc(p.category) + '</span><span>' + esc(p.date) + '</span></div>' +
               '<h2>' + esc(p.title) + '</h2>' +
               '<p>' + esc(p.summary) + '</p>' +
               '<div class="card-foot">' + tags +
                 '<span class="read-time">' + p.reading_time + ' 分钟读完</span>' +
               '</div>' +
             '</a>';
    }).join('');

    Array.prototype.forEach.call(box.querySelectorAll('.tag'), function (tag) {
      tag.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        state.q = tag.getAttribute('data-tag');
        state.cat = '';
        if (input) input.value = state.q;
        syncUrl(); render();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });
  }

  if (input) {
    input.addEventListener('input', function () {
      state.q = input.value; syncUrl(); render();
    });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { input.value = ''; state.q = ''; syncUrl(); render(); input.blur(); }
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input && input) {
      e.preventDefault(); input.focus();
    }
  });

  render();
})();
