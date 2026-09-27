(function () {
  "use strict";

  // Menu mobile
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  if (header && toggle) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  // Submenu de Áreas (clique para toque/teclado; hover resolve no desktop)
  document.querySelectorAll(".nav__item--has-sub").forEach(function (item) {
    var btn = item.querySelector(".nav__link");
    btn.addEventListener("click", function () {
      var open = item.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", String(open));
    });
    item.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") {
        item.classList.remove("is-open");
        btn.setAttribute("aria-expanded", "false");
        btn.focus();
      }
    });
  });
  document.addEventListener("click", function (ev) {
    document.querySelectorAll(".nav__item--has-sub.is-open").forEach(function (item) {
      if (!item.contains(ev.target)) {
        item.classList.remove("is-open");
        item.querySelector(".nav__link").setAttribute("aria-expanded", "false");
      }
    });
  });

  // Filtro de categorias do blog
  var chips = document.querySelectorAll("[data-filter]");
  if (chips.length) {
    var posts = document.querySelectorAll("[data-category]");
    var empty = document.querySelector("[data-empty]");
    var apply = function (cat) {
      var shown = 0;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.dataset.filter === cat)); });
      posts.forEach(function (p) {
        var match = cat === "todas" || p.dataset.category === cat;
        p.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    };
    chips.forEach(function (c) {
      c.addEventListener("click", function () { apply(c.dataset.filter); });
    });
    var initial = (location.hash || "").replace("#", "");
    var valid = Array.prototype.some.call(chips, function (c) { return c.dataset.filter === initial; });
    apply(valid ? initial : "todas");
  }

  // Formulários: enviam para o endpoint em data-endpoint (configurado no build).
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    var status = form.querySelector(".form__status");
    var show = function (msg) { status.textContent = msg; status.hidden = false; };
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (!form.reportValidity()) return;
      var endpoint = form.dataset.endpoint;
      if (!endpoint) {
        show("O envio pelo site ainda não está disponível. Utilize um dos canais de contato direto.");
        return;
      }
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      fetch(endpoint, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (res) {
          if (!res.ok) throw new Error(res.status);
          form.reset();
          show(form.dataset.success);
        })
        .catch(function () {
          show("Não foi possível enviar agora. Tente novamente ou utilize um dos canais de contato direto.");
        })
        .then(function () { btn.disabled = false; });
    });
  });
})();
