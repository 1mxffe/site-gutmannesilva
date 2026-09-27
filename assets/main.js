(function () {
  "use strict";

  // Mega menu de Áreas de Atuação
  var mega = document.querySelector(".has-mega");
  if (mega) {
    var megaBtn = mega.querySelector(".nav__link");
    var setMega = function (open) {
      mega.classList.toggle("is-open", open);
      megaBtn.setAttribute("aria-expanded", String(open));
    };
    megaBtn.addEventListener("click", function () { setMega(!mega.classList.contains("is-open")); });
    document.addEventListener("click", function (ev) { if (!mega.contains(ev.target)) setMega(false); });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && mega.classList.contains("is-open")) { setMega(false); megaBtn.focus(); }
    });
  }

  // Painel lateral (menu completo; único menu em telas estreitas)
  var panel = document.getElementById("painel");
  var burger = document.querySelector(".burger");
  if (panel && burger) {
    var closeBtn = panel.querySelector(".panel__close");
    var setPanel = function (open) {
      panel.hidden = !open;
      burger.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("is-locked", open);
      if (open) closeBtn.focus(); else burger.focus();
    };
    burger.addEventListener("click", function () { setPanel(true); });
    closeBtn.addEventListener("click", function () { setPanel(false); });
    panel.addEventListener("click", function (ev) { if (ev.target === panel) setPanel(false); });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && !panel.hidden) setPanel(false); });
  }

  // Abas (Nossa história)
  document.querySelectorAll("[data-tabs]").forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll("[role=tab]"));
    var select = function (tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (ev) {
        var d = ev.key === "ArrowRight" ? 1 : ev.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        var next = tabs[(i + d + tabs.length) % tabs.length];
        select(next);
        next.focus();
      });
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
