(function () {
  var container = document.getElementById('intro-slideshow');
  if (!container) return;

  var slides = container.querySelectorAll('.intro-slide');
  var dots = container.querySelectorAll('.intro-dots li');
  var prevBtn = container.querySelector('.intro-prev');
  var nextBtn = container.querySelector('.intro-next');
  var current = 0;
  var total = slides.length;
  var interval = 8000;   // 8 seconds between slides
  var speed = 500;       // 500ms fade transition (set via CSS)
  var timer = null;
  var paused = false;

  function goTo(index) {
    if (index < 0) index = total - 1;
    if (index >= total) index = 0;

    // Fade out current
    slides[current].classList.remove('active');
    dots[current].classList.remove('active');

    // Fade in target
    current = index;
    slides[current].classList.add('active');
    dots[current].classList.add('active');
  }

  function next() {
    goTo(current + 1);
  }

  function prev() {
    goTo(current - 1);
  }

  function startAutoplay() {
    stopAutoplay();
    timer = setInterval(function () {
      if (!paused) next();
    }, interval);
  }

  function stopAutoplay() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  // Arrow buttons
  prevBtn.addEventListener('click', function () {
    prev();
    startAutoplay(); // reset timer after manual nav
  });

  nextBtn.addEventListener('click', function () {
    next();
    startAutoplay();
  });

  // Dot buttons
  dots.forEach(function (dot, i) {
    dot.querySelector('button').addEventListener('click', function () {
      goTo(i);
      startAutoplay();
    });
  });

  // Pause on hover
  container.addEventListener('mouseenter', function () {
    paused = true;
  });

  container.addEventListener('mouseleave', function () {
    paused = false;
  });

  // Keyboard navigation
  container.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') {
      prev();
      startAutoplay();
    } else if (e.key === 'ArrowRight') {
      next();
      startAutoplay();
    }
  });

  // Touch/swipe support
  var touchStartX = 0;
  var touchEndX = 0;

  container.addEventListener('touchstart', function (e) {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  container.addEventListener('touchend', function (e) {
    touchEndX = e.changedTouches[0].screenX;
    var diff = touchStartX - touchEndX;
    if (Math.abs(diff) > 50) {
      if (diff > 0) next(); else prev();
      startAutoplay();
    }
  }, { passive: true });

  // Start
  startAutoplay();
})();
