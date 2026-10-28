/* Michel Gallone · CV en ligne
   Navigation et animations d'apparition. */

(function () {
  "use strict";

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
