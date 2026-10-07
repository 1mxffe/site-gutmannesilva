(function () {
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
