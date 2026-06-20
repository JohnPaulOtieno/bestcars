/* BestCars — main.js */

// ── NAV: transparent → solid on scroll ──────────────
const nav = document.getElementById('siteNav');
if (nav) {
  const onScroll = () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// ── MOBILE NAV TOGGLE ────────────────────────────────
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      navToggle.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

// ── SCROLL REVEAL (IntersectionObserver) ─────────────
const revealEls = document.querySelectorAll('.reveal-up');
if (revealEls.length) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -48px 0px' });
  revealEls.forEach(el => observer.observe(el));
}

// ── COUNT-UP ANIMATION (stats bar) ───────────────────
const countEls = document.querySelectorAll('.stat-num[data-target]');
if (countEls.length) {
  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el     = entry.target;
      const target = parseInt(el.dataset.target, 10);
      const dur    = 1600;
      const start  = performance.now();
      const tick   = (now) => {
        const p = Math.min((now - start) / dur, 1);
        const ease = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(ease * target);
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      countObserver.unobserve(el);
    });
  }, { threshold: 0.5 });
  countEls.forEach(el => countObserver.observe(el));
}

// ── TESTIMONIAL CAROUSEL ─────────────────────────────
// Runs after full layout so scrollWidth / offsetWidth are accurate
window.addEventListener('load', function initCarousel() {
  const track       = document.getElementById('testimonialsTrack');
  const prevBtn     = document.getElementById('tPrev');
  const nextBtn     = document.getElementById('tNext');
  const dotsWrap    = document.getElementById('tDots');
  if (!track || !prevBtn || !nextBtn) return;

  const cards = Array.from(track.querySelectorAll('.testimonial-card'));
  if (cards.length <= 1) return;

  let current   = 0;
  let autoTimer = null;

  // How many cards fit in the visible area right now
  function visibleCount() {
    const trackW = track.parentElement.offsetWidth;
    const cardW  = cards[0].offsetWidth;
    return Math.max(1, Math.floor(trackW / (cardW + 24)));
  }

  // Max index we can scroll to
  function maxIdx() { return Math.max(0, cards.length - visibleCount()); }

  // Build / rebuild dots
  function buildDots() {
    if (!dotsWrap) return;
    dotsWrap.innerHTML = '';
    const total = maxIdx() + 1;
    for (let i = 0; i < total; i++) {
      const d = document.createElement('button');
      d.className = 't-dot' + (i === current ? ' active' : '');
      d.setAttribute('aria-label', `Slide ${i + 1}`);
      d.addEventListener('click', () => { stopAuto(); goTo(i); startAuto(); });
      dotsWrap.appendChild(d);
    }
  }

  function syncDots() {
    if (!dotsWrap) return;
    dotsWrap.querySelectorAll('.t-dot').forEach((d, i) =>
      d.classList.toggle('active', i === current)
    );
  }

  function goTo(idx) {
    current = Math.max(0, Math.min(idx, maxIdx()));
    // Use scrollLeft — works regardless of card pixel width
    const cardW = cards[0].offsetWidth + 24; // card + gap
    track.scrollTo({ left: current * cardW, behavior: 'smooth' });
    cards.forEach((c, i) => c.classList.toggle('active', i === current));
    syncDots();
  }

  function next() { goTo(current >= maxIdx() ? 0 : current + 1); }
  function prev() { goTo(current <= 0 ? maxIdx() : current - 1); }

  function startAuto() { autoTimer = setInterval(next, 5000); }
  function stopAuto()  { clearInterval(autoTimer); autoTimer = null; }

  nextBtn.addEventListener('click', () => { stopAuto(); next(); startAuto(); });
  prevBtn.addEventListener('click', () => { stopAuto(); prev(); startAuto(); });

  // Touch swipe
  let touchX = 0;
  track.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; }, { passive: true });
  track.addEventListener('touchend',   e => {
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 48) { stopAuto(); dx < 0 ? next() : prev(); startAuto(); }
  }, { passive: true });

  // Rebuild on resize
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { current = 0; buildDots(); goTo(0); }, 200);
  }, { passive: true });

  buildDots();
  goTo(0);
  startAuto();
});

// ── HERO: trigger reveals immediately ───────────────
window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.hero .reveal-up').forEach(el => {
    setTimeout(() => el.classList.add('visible'), 200);
  });
});
