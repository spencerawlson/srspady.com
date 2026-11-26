// srspady.com — theme toggle + mobile nav. Client-side only.
(function () {
  var toggle = document.getElementById("theme-toggle");
  var root = document.documentElement;
  function label() {
    if (toggle) toggle.textContent = root.getAttribute("data-theme") === "dark" ? "Light" : "Dark";
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("srspady-theme", next); } catch (e) {}
      label();
    });
    label();
  }
  var navToggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("mainnav");
  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
      navToggle.textContent = open ? "Close" : "Menu";
    });
  }
})();
