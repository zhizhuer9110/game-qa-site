(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var header = document.getElementById("siteHeader");
  var nav = document.getElementById("primaryNav");
  var menuBtn = document.getElementById("menuBtn");
  var navLinks = Array.prototype.slice.call(nav ? nav.querySelectorAll("a") : []);

  /* ---------- sticky header state ---------- */
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 12);
    updateActiveNav();
  }

  /* ---------- scroll spy ---------- */
  var sections = navLinks
    .map(function (link) {
      var id = link.getAttribute("data-nav");
      return id ? document.getElementById(id) : null;
    })
    .filter(Boolean);

  function updateActiveNav() {
    if (!sections.length) return;
    var probe = window.scrollY + (window.innerHeight * 0.32);
    var current = null;

    sections.forEach(function (section) {
      if (section.offsetTop <= probe) current = section;
    });

    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 4) {
      current = sections[sections.length - 1];
    }

    navLinks.forEach(function (link) {
      var isActive = current && link.getAttribute("data-nav") === current.id;
      link.classList.toggle("is-active", !!isActive);
      if (isActive) {
        link.setAttribute("aria-current", "true");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ---------- mobile menu ---------- */
  function setMenu(open) {
    if (!nav || !menuBtn) return;
    nav.classList.toggle("is-open", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.setAttribute("aria-label", open ? "关闭菜单" : "打开菜单");
    document.body.classList.toggle("nav-open", open);
  }

  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      setMenu(!nav.classList.contains("is-open"));
    });

    navLinks.forEach(function (link) {
      link.addEventListener("click", function () {
        setMenu(false);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setMenu(false);
    });

    var scrim = document.getElementById("navScrim");
    if (scrim) scrim.addEventListener("click", function () { setMenu(false); });

    document.addEventListener("click", function (event) {
      if (!nav.classList.contains("is-open")) return;
      if (nav.contains(event.target) || menuBtn.contains(event.target)) return;
      setMenu(false);
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 1080) setMenu(false);
    });
  }

  /* ---------- reveal on scroll ---------- */
  var revealItems = Array.prototype.slice.call(document.querySelectorAll(".reveal"));

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealItems.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        revealObserver.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

    revealItems.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ---------- number counters ---------- */
  var counters = Array.prototype.slice.call(document.querySelectorAll("[data-count]"));
  var easeOut = function (t) { return 1 - Math.pow(1 - t, 3); };

  function runCounter(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var suffix = el.getAttribute("data-suffix") || "";
    if (isNaN(target)) return;

    if (reduceMotion) {
      el.textContent = target + suffix;
      return;
    }

    var duration = 1100;
    var start = null;

    function step(now) {
      if (start === null) start = now;
      var progress = Math.min((now - start) / duration, 1);
      el.textContent = Math.round(target * easeOut(progress)) + suffix;
      if (progress < 1) window.requestAnimationFrame(step);
    }

    el.textContent = "0" + suffix;
    window.requestAnimationFrame(step);
  }

  if ("IntersectionObserver" in window && !reduceMotion) {
    var counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        runCounter(entry.target);
        counterObserver.unobserve(entry.target);
      });
    }, { threshold: 0.5 });

    counters.forEach(function (el) { counterObserver.observe(el); });
  } else {
    counters.forEach(runCounter);
  }

  /* ---------- copy phone number ---------- */
  var toast = document.getElementById("toast");
  var toastTimer = null;

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("is-visible");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () {
      toast.classList.remove("is-visible");
    }, 2200);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (err) { ok = false; }
      document.body.removeChild(area);
      ok ? resolve() : reject(new Error("copy failed"));
    });
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-copy]"), function (button) {
    button.addEventListener("click", function () {
      copyText(button.getAttribute("data-copy")).then(function () {
        showToast("号码已复制：186 0129 1984");
      }).catch(function () {
        showToast("请手动记录：186 0129 1984");
      });
    });
  });

  /* ---------- mobile bottom bar: hide at contact, tuck away on scroll down ---------- */
  var mobileCta = document.querySelector(".mobile-cta");
  var contactSection = document.getElementById("contact");
  var ctaAtContact = false;
  var ctaTucked = false;

  function applyCtaState() {
    if (!mobileCta) return;
    mobileCta.classList.toggle("is-hidden", ctaAtContact || ctaTucked);
  }

  if (mobileCta && contactSection && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      ctaAtContact = entries[0].isIntersecting;
      applyCtaState();
    }, { threshold: 0.12 }).observe(contactSection);
  }

  var lastCtaScroll = window.scrollY;
  window.addEventListener("scroll", function () {
    var y = window.scrollY;
    if (y > lastCtaScroll + 8 && y > 480) {
      ctaTucked = true;
    } else if (y < lastCtaScroll - 8) {
      ctaTucked = false;
    }
    lastCtaScroll = y;
    applyCtaState();
  }, { passive: true });

  /* ---------- footer year ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());
})();
