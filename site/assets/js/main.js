/* Michel Gallone · site vitrine
   Navigation, filtres, liens « En discuter » et animations.
   Les textes dynamiques sont regroupés par langue pour la future version anglaise. */

(function () {
  "use strict";

  var TEXTES = {
    fr: {
      objet: "Prise de contact",
      bonjour: "Bonjour Michel,",
      intro: "Je vous contacte au sujet de :",
      projet: "Mon projet :",
      signature: "Bien à vous,"
    },
    en: {
      objet: "Getting in touch",
      bonjour: "Hello Michel,",
      intro: "I am contacting you about:",
      projet: "My project:",
      signature: "Best regards,"
    }
  };
  var langue = (document.documentElement.lang || "fr").slice(0, 2);
  var t = TEXTES[langue] || TEXTES.fr;
  var EMAIL = "michel@sowattmusic.com";

  /* ---------- Navigation ---------- */
  var nav = document.getElementById("nav");
  function majNav() { nav.classList.toggle("solide", window.scrollY > 40); }
  window.addEventListener("scroll", majNav, { passive: true });
  majNav();

  var menu = document.getElementById("menu");
  var menuBtn = document.getElementById("menu-btn");
  menuBtn.addEventListener("click", function () {
    var ouvert = menu.classList.toggle("ouvert");
    menuBtn.setAttribute("aria-expanded", ouvert);
  });
  menu.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      menu.classList.remove("ouvert");
      menuBtn.setAttribute("aria-expanded", "false");
    }
  });

  /* ---------- Filtres ---------- */
  var filtres = document.querySelectorAll(".filtre");
  var produits = document.querySelectorAll(".produit");
  filtres.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = btn.dataset.filtre;
      filtres.forEach(function (b) { b.setAttribute("aria-pressed", b === btn); });
      produits.forEach(function (p) {
        p.hidden = f !== "tout" && p.dataset.cat.split(" ").indexOf(f) === -1;
      });
    });
  });

  /* ---------- « En discuter » : e-mail prérempli par domaine ---------- */
  produits.forEach(function (p) {
    var lien = p.querySelector(".en-parler");
    var corps = [t.bonjour, "", t.intro + " " + p.dataset.nom, "", t.projet, "", "", t.signature].join("\n");
    lien.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(t.objet + " · " + p.dataset.nom) + "&body=" + encodeURIComponent(corps);
  });

  /* ---------- Apparition au défilement ---------- */
  var elements = document.querySelectorAll(".apparait");
  if ("IntersectionObserver" in window) {
    var obs = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("vu"); obs.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    elements.forEach(function (el) { obs.observe(el); });
  } else {
    elements.forEach(function (el) { el.classList.add("vu"); });
  }

  document.getElementById("annee").textContent = new Date().getFullYear();
})();
