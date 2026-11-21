/* 明暗主题：默认深色，选择记在 localStorage */
(function () {
  var KEY = 'techx-theme';
  var SUN = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  document.documentElement.dataset.theme = (saved === 'light' || saved === 'dark') ? saved : 'dark';

  function sync() {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    var dark = document.documentElement.dataset.theme === 'dark';
    btn.innerHTML = dark ? SUN : MOON;
    var label = dark ? '切换到浅色模式' : '切换到深色模式';
    btn.setAttribute('aria-label', label);
    btn.setAttribute('title', label);
  }

  window.techxToggleTheme = function () {
    var next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem(KEY, next); } catch (e) {}
    sync();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      sync();
      var btn = document.getElementById('theme-toggle');
      if (btn) btn.addEventListener('click', window.techxToggleTheme);
    });
  } else {
    sync();
    var b = document.getElementById('theme-toggle');
    if (b) b.addEventListener('click', window.techxToggleTheme);
  }
})();
