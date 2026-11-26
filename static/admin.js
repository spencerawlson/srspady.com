// srspady.com admin — rich-text editor toolbar + filter-lab preview.
// Vanilla JS, no CDN, no framework. The editor is a contenteditable div;
// on submit its HTML is copied into the hidden input, then sanitized
// server-side with a bleach allowlist.
(function () {
  // --- Rich-text editor ---
  var editor = document.getElementById("rte-editor");
  var form = document.getElementById("record-form");
  var hidden = document.getElementById("rte-body");
  if (editor) {
    document.querySelectorAll(".rte-toolbar [data-cmd]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        editor.focus();
        document.execCommand(btn.getAttribute("data-cmd"), false,
          btn.getAttribute("data-value") || null);
      });
    });
    var linkBtn = document.getElementById("rte-link");
    if (linkBtn) {
      linkBtn.addEventListener("click", function () {
        editor.focus();
        var url = window.prompt("Link URL (https://…):");
        if (url) document.execCommand("createLink", false, url);
      });
    }
    if (form && hidden) {
      form.addEventListener("submit", function () {
        hidden.value = editor.innerHTML;
      });
    }
  }

  // --- Filter lab: live CSS preview of the server-side Pillow presets ---
  var CSS_FILTERS = {
    "none": "none",
    "warm": "sepia(0.35) saturate(1.25) hue-rotate(-12deg)",
    "cool": "hue-rotate(18deg) saturate(1.15)",
    "black-and-white": "grayscale(1)",
    "faded": "contrast(0.75) brightness(1.08) saturate(0.8)",
    "high-contrast": "contrast(1.6)"
  };
  var sourceSel = document.getElementById("filter-source");
  var previewImg = document.getElementById("filter-preview-img");
  var previewNote = document.getElementById("filter-preview-note");
  var deriveSource = document.getElementById("derive-source");
  var deriveFilter = document.getElementById("derive-filter");
  var currentFilter = "none";
  function showPreview() {
    if (!sourceSel || !previewImg) return;
    var name = sourceSel.value;
    deriveSource.value = name;
    previewImg.src = "/admin/media/originals/" + encodeURIComponent(name);
    previewImg.style.display = "block";
    previewImg.style.filter = CSS_FILTERS[currentFilter] || "none";
    if (previewNote) previewNote.textContent = "Preview: " + name + " — " + currentFilter + " (CSS preview; the saved copy is rendered with Pillow).";
  }
  if (sourceSel) {
    sourceSel.addEventListener("change", showPreview);
    if (sourceSel.value) showPreview();
  }
  document.querySelectorAll(".filter-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      currentFilter = btn.getAttribute("data-filter");
      deriveFilter.value = currentFilter;
      document.querySelectorAll(".filter-btn").forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      showPreview();
    });
  });
})();
