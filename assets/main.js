(function () {
  // Animações de entrada ao rolar e cabeçalho
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
  var root = document.documentElement;
  var animOn = root.classList.contains('anim') && 'IntersectionObserver' in window;

  // ---- Entrada: cortina de carregamento e transição entre páginas ----
  var loader = document.querySelector('.loader');
  var heroQueue = [];
  var ready = false;
  function setReady() {
    if (ready) return; ready = true;
    root.classList.add('ready');
    heroQueue.forEach(function (fn) { fn(); });
    heroQueue = [];
  }
  function runLoader() {
    if (!loader || !root.classList.contains('has-loader')) { setReady(); return; }
    var first = root.classList.contains('loader-first');
    var started = Date.now();
    var leave = function () {
      loader.classList.add('leaving');
      setTimeout(setReady, first ? 520 : 420);
      setTimeout(function () { root.classList.remove('has-loader', 'loader-first', 'loader-nav'); loader.classList.remove('leaving'); }, 1300);
    };
    var go = function () { setTimeout(leave, Math.max(0, (first ? 1100 : 120) - (Date.now() - started))); };
    if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
    setTimeout(leave, 3500); // segurança: nunca prender a página
  }
  runLoader();

  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { root.classList.remove('has-loader', 'loader-first', 'loader-nav', 'covering', 'covering-in'); if (loader) loader.classList.remove('leaving'); }
  });
  if (animOn && loader) {
    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a || a.target || a.hasAttribute('download')) return;
      var u;
      try { u = new URL(a.href, location.href); } catch (err) { return; }
      if (u.origin !== location.origin || u.pathname === location.pathname || !/(\.html|\/)$/.test(u.pathname)) return;
      e.preventDefault();
      try { sessionStorage.setItem('gs-nav', '1'); } catch (err) {}
      root.classList.add('has-loader', 'loader-nav', 'covering');
      void loader.offsetWidth;
      root.classList.add('covering-in');
      setTimeout(function () { location.href = u.href; }, 650);
    });
  }

  if (animOn) {
    var EASE_MS = 1700;
    var reveal = function (el, delay, hero) {
      var fire = function () {
        el.style.setProperty('--d', delay + 'ms');
        el.classList.add('in');
        setTimeout(function () {
          el.classList.remove('rv', 'rvi', 'split', 'in');
          el.style.removeProperty('--d');
          el.querySelectorAll('.sw').forEach(function (s) { s.classList.add('done'); });
        }, EASE_MS + delay + 400);
      };
      if (hero && !ready) heroQueue.push(fire); else fire();
    };

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        var t = en.target;
        reveal(t, parseInt(t.getAttribute('data-d'), 10) || 0, false);
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -6% 0px' });

    var watch = function (el, cls, delay) {
      el.classList.add(cls);
      el.setAttribute('data-d', delay || 0);
      io.observe(el);
    };

    // Títulos: palavras sobem por trás de uma máscara
    var splitTitle = function (h) {
      if (h.children.length) return false;
      var words = h.textContent.trim().split(/\s+/);
      h.setAttribute('aria-label', h.textContent.trim());
      h.textContent = '';
      words.forEach(function (w, i) {
        var m = document.createElement('span'); m.className = 'sw'; m.setAttribute('aria-hidden', 'true');
        var s = document.createElement('span'); s.textContent = w; s.style.setProperty('--i', i);
        m.appendChild(s); h.appendChild(m);
        if (i < words.length - 1) h.appendChild(document.createTextNode(' '));
      });
      return true;
    };
    var heroEls = '.hero .h-display, .page-hero .h-page';
    document.querySelectorAll('.h-display, .h-page, .h-lead, .h-section, .cta-copy h2').forEach(function (h) {
      var isHero = h.matches(heroEls);
      var split = splitTitle(h);
      h.classList.add(split ? 'split' : 'rv');
      if (isHero) reveal(h, 0, true); else { h.setAttribute('data-d', 0); io.observe(h); }
    });

    // Resto do hero: sobe em sequência logo depois do título
    var heroItems = document.querySelectorAll('.breadcrumb, .page-hero-copy > p, .hero-sub, .hero .text-lg, .hero-actions, .scroll-cue, .page-hero-copy > .hero-actions');
    var seen = [];
    heroItems.forEach(function (el, i) {
      if (seen.indexOf(el) > -1) return; seen.push(el);
      el.classList.add('rv');
      reveal(el, 180 + seen.length * 110, true);
    });

    // Imagens: cortina que abre + zoom que assenta
    document.querySelectorAll('.img-slot.has-img').forEach(function (el, i) {
      el.classList.add('rvi');
      var inHero = !!el.closest('.hero, .page-hero');
      if (inHero) reveal(el, 300, true); else { el.setAttribute('data-d', 0); io.observe(el); }
    });

    // Grupos: filhos entram em escalonado
    var groups = '.bento-row, .awards, .areas-grid, .stats, .services, .accordion, .other-areas, .footer-cols, .partners, .timeline, .mvv, .channels';
    document.querySelectorAll(groups).forEach(function (g) {
      Array.prototype.forEach.call(g.children, function (c, i) { watch(c, 'rv', Math.min(i, 8) * 90); });
    });
    var singles = '.section-head, .two-col-head, .intro-copy, .cta-box, .faq-title, .areas-more, .article-cta, .highlight, .prose, .contact-grid > *, .newsletter > *, .filters, .empty';
    document.querySelectorAll(singles).forEach(function (el) { if (!el.classList.contains('rv')) watch(el, 'rv', 0); });
  }

  // ---- Contadores (números dos destaques) ----
  var stats = document.querySelectorAll('.stat-num');
  stats.forEach(function (el) {
    var m = el.textContent.match(/^(\d+)(.*)$/);
    if (!m) return;
    var n = document.createElement('span'); n.textContent = m[1]; n.setAttribute('data-count', m[1]);
    el.textContent = ''; el.appendChild(n); el.appendChild(document.createTextNode(m[2]));
  });
  if (animOn && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return; cio.unobserve(en.target);
        var el = en.target, target = Number(el.getAttribute('data-count')), t0 = performance.now();
        var step = function (now) {
          var t = Math.min(1, (now - t0) / 1600);
          el.textContent = String(Math.round(target * (1 - Math.pow(2, -10 * t))));
          if (t < 1) requestAnimationFrame(step);
        };
        el.textContent = '0'; requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('[data-count]').forEach(function (el) { cio.observe(el); });
  }

  // ---- Parallax suave em imagens e brilhos ----
  if (animOn) {
    var px = [];
    document.querySelectorAll('.page-hero .img-slot img, .intro .img-slot img, .split .img-slot img, .awards .img-slot img').forEach(function (img) {
      img.classList.add('px-img'); px.push({ el: img, f: 0.07, clamp: true });
    });
    document.querySelectorAll('.glow').forEach(function (g) { px.push({ el: g, f: 0.14, clamp: false }); });
    var pending = false;
    var update = function () {
      pending = false;
      var vh = window.innerHeight;
      px.forEach(function (p) {
        var host = p.clamp ? p.el.parentNode : p.el;
        var r = host.getBoundingClientRect();
        if (r.bottom < -300 || r.top > vh + 300) return;
        var off = (r.top + r.height / 2 - vh / 2) * -p.f;
        if (p.clamp) { var lim = r.height * 0.045; off = Math.max(-lim, Math.min(lim, off)); }
        p.el.style.translate = '0 ' + off.toFixed(1) + 'px';
      });
    };
    window.addEventListener('scroll', function () { if (!pending) { pending = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener('resize', update, { passive: true });
    update();
  }

  // ---- Barra de leitura no cabeçalho ----
  if (header) {
    var bar = document.createElement('div'); bar.className = 'reading-progress'; bar.setAttribute('aria-hidden', 'true');
    header.appendChild(bar);
    var rp = false;
    var setBar = function () {
      rp = false;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.setProperty('--p', max > 0 ? Math.min(1, window.scrollY / max).toFixed(4) : '0');
    };
    window.addEventListener('scroll', function () { if (!rp) { rp = true; requestAnimationFrame(setBar); } }, { passive: true });
    setBar();
  }

  // Menu mobile
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.querySelector('.i-menu').style.display = open ? 'none' : '';
      toggle.querySelector('.i-close').style.display = open ? '' : 'none';
    });
  }

  // Menu suspenso "Áreas de Atuação"
  document.querySelectorAll('.has-dropdown').forEach(function (item) {
    var trigger = item.querySelector('.nav-trigger');
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var open = item.classList.toggle('open');
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (!item.contains(e.target)) { item.classList.remove('open'); trigger.setAttribute('aria-expanded', 'false'); }
    });
    item.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { item.classList.remove('open'); trigger.setAttribute('aria-expanded', 'false'); trigger.focus(); }
    });
  });

  // Acordeão: apenas um item aberto por vez
  document.querySelectorAll('.accordion').forEach(function (acc) {
    var items = acc.querySelectorAll('details');
    items.forEach(function (d) {
      d.addEventListener('toggle', function () {
        if (d.open) items.forEach(function (o) { if (o !== d) o.open = false; });
      });
    });
  });

  // Filtro do blog
  var filters = document.querySelectorAll('.filter');
  if (filters.length) {
    var posts = document.querySelectorAll('[data-category]');
    var empty = document.querySelector('.empty');
    var emptyCat = document.querySelector('[data-empty-cat]');
    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filters.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        var cat = btn.dataset.filter;
        var shown = 0;
        posts.forEach(function (p) {
          var match = cat === 'todos' || p.dataset.category === cat;
          p.hidden = !match;
          if (match) shown++;
        });
        if (empty) {
          empty.hidden = shown > 0;
          if (emptyCat) emptyCat.textContent = cat === 'todos' ? '' : ' de ' + btn.textContent.trim();
        }
      });
    });
  }

  // Formulários.
  // Para conectar o envio, preencha data-endpoint no <form> com a URL do serviço
  // (ex.: Formspree, RD Station, endpoint próprio). Sem endpoint, nada é enviado.
  document.querySelectorAll('form[data-endpoint]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var status = form.querySelector('.form-status');
      var endpoint = form.dataset.endpoint;
      var show = function (msg) { if (status) { status.textContent = msg; status.hidden = false; } };
      if (!endpoint) {
        show(form.dataset.offline || 'O envio por formulário ainda não está ativo. Fale conosco pelo telefone, WhatsApp ou e-mail.');
        return;
      }
      fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error();
          form.reset();
          show(form.dataset.success || 'Mensagem enviada. Nossa equipe entrará em contato em breve.');
        })
        .catch(function () { show('Não foi possível enviar agora. Tente novamente ou fale conosco pelo telefone.'); });
    });
  });
})();
