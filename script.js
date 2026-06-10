(function () {
  "use strict";

  var sunPath = "M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10ZM12 1v3M12 20v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M1 12h3M20 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12";
  var moonPath = "M20.99 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 20.99 12.79Z";

  function setTheme(theme, persist) {
    var root = document.documentElement;
    theme = theme === "light" ? "light" : "dark";
    root.setAttribute("data-theme", theme);
    root.style.colorScheme = theme;
    if (persist) {
      try {
        localStorage.setItem("theme", theme);
      } catch (error) {}
    }
    var button = document.getElementById("theme-toggle");
    if (!button) return;
    button.setAttribute("aria-pressed", String(theme === "dark"));
    var path = button.querySelector(".theme-toggle__path");
    if (path) path.setAttribute("d", theme === "dark" ? moonPath : sunPath);
  }

  function initTheme() {
    var current = document.documentElement.getAttribute("data-theme") || "dark";
    setTheme(current, false);
    var button = document.getElementById("theme-toggle");
    if (!button) return;
    button.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      setTheme(next, true);
    });
  }

  function initGallery() {
    document.querySelectorAll("[data-gallery]").forEach(function (gallery) {
      var track = gallery.querySelector("[data-gallery-track]");
      if (!track) return;
      var amount = function () {
        return Math.max(280, Math.floor(track.clientWidth * 0.82));
      };
      var prev = gallery.querySelector("[data-gallery-prev]");
      var next = gallery.querySelector("[data-gallery-next]");
      if (prev) prev.addEventListener("click", function () { track.scrollBy({ left: -amount(), behavior: "smooth" }); });
      if (next) next.addEventListener("click", function () { track.scrollBy({ left: amount(), behavior: "smooth" }); });
    });
  }

  function initDeferredImages() {
    var images = Array.prototype.slice.call(document.querySelectorAll("img[data-src]"));
    if (!images.length) return;

    function loadImage(img) {
      if (!img || !img.dataset || !img.dataset.src) return;
      var src = img.dataset.src;
      delete img.dataset.src;
      img.addEventListener("load", function () {
        img.classList.add("is-loaded");
      }, { once: true });
      img.src = src;
      if (img.complete) img.classList.add("is-loaded");
    }

    if (!("IntersectionObserver" in window)) {
      setTimeout(function () {
        images.forEach(loadImage);
      }, 1200);
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        loadImage(entry.target);
      });
    }, { rootMargin: "80px 0px", threshold: 0.01 });

    images.forEach(function (img) {
      observer.observe(img);
    });
  }

  function initVideoPlaceholders() {
    document.addEventListener("click", function (event) {
      var button = event.target.closest && event.target.closest(".video-placeholder[data-video-id]");
      if (!button) return;
      var videoId = button.getAttribute("data-video-id");
      var title = button.getAttribute("data-video-title") || "Vídeo tutorial";
      if (!videoId) return;
      var iframe = document.createElement("iframe");
      iframe.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(videoId) + "?autoplay=1&rel=0";
      iframe.title = title;
      iframe.loading = "lazy";
      iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.allowFullscreen = true;
      button.replaceWith(iframe);
    });
  }

  function initImageModal() {
    var modal = document.getElementById("image-modal");
    var frame = document.getElementById("image-modal-frame");
    if (!modal || !frame) return;

    function close() {
      modal.hidden = true;
      frame.textContent = "";
      document.body.style.overflow = "";
    }

    document.addEventListener("click", function (event) {
      var opener = event.target.closest && event.target.closest("[data-modal-image]");
      if (opener) {
        var image = document.createElement("img");
        image.src = opener.getAttribute("data-modal-image");
        image.alt = opener.getAttribute("data-modal-alt") || "Imagem ampliada";
        image.width = 1200;
        image.height = 720;
        image.loading = "lazy";
        frame.replaceChildren(image);
        modal.hidden = false;
        document.body.style.overflow = "hidden";
      }
      if (event.target.closest && event.target.closest("[data-modal-close]")) {
        close();
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !modal.hidden) close();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTheme();
    initGallery();
    initDeferredImages();
    initVideoPlaceholders();
    initImageModal();
  });
})();
