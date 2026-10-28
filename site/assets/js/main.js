/* Michel Gallone · site vitrine
   Navigation, filtres, demande de devis (panier) et animations.
   Les textes dynamiques sont regroupés par langue pour la future version anglaise. */

(function () {
  "use strict";

  var TEXTES = {
    fr: {
      ajouter: "Ajouter",
      ajoute: "Ajouté ✓",
      retirer: "Retirer",
      objet: "Demande de devis",
      bonjour: "Bonjour Michel,",
      intro: "Je souhaite un devis pour :",
      aucune: "(prestation à définir)",
      projet: "Mon projet :",
      signature: "Merci et à bientôt,"
    },
    en: {
      ajouter: "Add",
      ajoute: "Added ✓",
      retirer: "Remove",
      objet: "Quote request",
      bonjour: "Hello Michel,",
      intro: "I would like a quote for:",
      aucune: "(service to be defined)",
      projet: "My project:",
      signature: "Thank you, best regards,"
    }
  };
  var langue = (document.documentElement.lang || "fr").slice(0, 2);
  var t = TEXTES[langue] || TEXTES.fr;
  var EMAIL = "michel@sowattmusic.com";
  var CLE = "mg-demande";

  /* ---------- Stockage local (facultatif) ---------- */
  function lire() {
    try { return JSON.parse(localStorage.getItem(CLE)) || []; } catch (e) { return []; }
  }
  function ecrire(liste) {
    try { localStorage.setItem(CLE, JSON.stringify(liste)); } catch (e) { /* navigation privée */ }
  }

  var selection = lire();

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

  /* ---------- Demande de devis ---------- */
  var tiroir = document.getElementById("tiroir");
  var voile = document.getElementById("voile");
  var lignes = document.getElementById("lignes");
  var vide = document.getElementById("vide");
  var pastille = document.getElementById("pastille");
  var envoyer = document.getElementById("envoyer");
  var champNom = document.getElementById("nom");
  var champProjet = document.getElementById("projet");

  function nomDe(id) {
    var p = document.querySelector('.produit[data-id="' + id + '"]');
    return p ? p.dataset.nom : id;
  }

  function majMailto() {
    var corps = [t.bonjour, "", t.intro];
    if (selection.length) {
      selection.forEach(function (id) { corps.push("• " + nomDe(id)); });
    } else {
      corps.push(t.aucune);
    }
    corps.push("", t.projet, champProjet.value.trim() || "…", "", t.signature, champNom.value.trim());
    var objet = t.objet + (champNom.value.trim() ? " · " + champNom.value.trim() : "");
    envoyer.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(objet) + "&body=" + encodeURIComponent(corps.join("\n"));
  }

  function rendre() {
    lignes.innerHTML = "";
    selection.forEach(function (id) {
      var div = document.createElement("div");
      div.className = "ligne-panier";
      var b = document.createElement("b");
      b.textContent = nomDe(id);
      var btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = t.retirer;
      btn.addEventListener("click", function () { basculer(id); });
      div.appendChild(b);
      div.appendChild(btn);
      lignes.appendChild(div);
    });
    vide.hidden = selection.length > 0;
    pastille.textContent = selection.length;
    pastille.classList.toggle("visible", selection.length > 0);
    produits.forEach(function (p) {
      var btn = p.querySelector(".ajouter");
      var dedans = selection.indexOf(p.dataset.id) !== -1;
      btn.setAttribute("aria-pressed", dedans);
      btn.textContent = dedans ? t.ajoute : t.ajouter;
    });
    majMailto();
  }

  function basculer(id) {
    var i = selection.indexOf(id);
    if (i === -1) selection.push(id); else selection.splice(i, 1);
    ecrire(selection);
    rendre();
  }

  function ouvrir() {
    tiroir.classList.add("ouvert");
    voile.classList.add("ouvert");
    tiroir.setAttribute("aria-hidden", "false");
    document.getElementById("fermer-panier").focus();
  }
  function fermer() {
    tiroir.classList.remove("ouvert");
    voile.classList.remove("ouvert");
    tiroir.setAttribute("aria-hidden", "true");
  }

  produits.forEach(function (p) {
    p.querySelector(".ajouter").addEventListener("click", function () { basculer(p.dataset.id); });
  });
  document.getElementById("ouvrir-panier").addEventListener("click", ouvrir);
  document.querySelectorAll("[data-ouvre-panier]").forEach(function (b) { b.addEventListener("click", ouvrir); });
  document.getElementById("fermer-panier").addEventListener("click", fermer);
  voile.addEventListener("click", fermer);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") fermer(); });
  champNom.addEventListener("input", majMailto);
  champProjet.addEventListener("input", majMailto);

  rendre();

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
