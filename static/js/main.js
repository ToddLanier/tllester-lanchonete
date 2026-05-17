document.addEventListener('DOMContentLoaded', function() {
  'use strict';

  // Search toggle
  var searchToggle = document.querySelector('.search-toggle');
  if (searchToggle) {
    searchToggle.addEventListener('click', function(e) {
      e.preventDefault();

      var header = document.querySelector('.site-header');
      var drawer = document.querySelector('.search-drawer');

      // Toggle class on header if it exists
      if (header) header.classList.toggle('search-drawer-open');

      if (drawer) {
        var expanded = drawer.getAttribute('aria-expanded');
        drawer.setAttribute('aria-expanded', expanded === 'false' ? 'true' : 'false');

        // Check if drawer is visible (look for display:none in inline style or computed)
        var computedStyle = window.getComputedStyle(drawer);
        var isHidden = computedStyle.display === 'none' || drawer.style.display === 'none';

        if (isHidden) {
          drawer.style.display = 'block';
          document.body.classList.add('search-open');
          var input = drawer.querySelector('.search-input');
          if (input) input.focus();
        } else {
          drawer.style.display = 'none';
          document.body.classList.remove('search-open');
        }
      }

      // Toggle search icons (svg or i)
      var icons = this.querySelectorAll('svg, i');
      icons.forEach(function(icon) {
        icon.style.display = icon.style.display === 'none' ? '' : 'none';
      });
    });
  }

  // Close search drawer on Escape key
  document.addEventListener('keyup', function(e) {
    if (e.keyCode === 27) {
      var drawer = document.querySelector('.search-drawer');
      if (drawer) {
        drawer.setAttribute('aria-expanded', 'false');
        drawer.style.display = 'none';
      }
      document.body.classList.remove('search-open');
      var header = document.querySelector('.site-header');
      if (header) header.classList.remove('search-drawer-open');

      // Reset search toggle icons
      var searchToggle = document.querySelector('.search-toggle');
      if (searchToggle) {
        var icons = searchToggle.querySelectorAll('svg, i');
        // Reset to default state: show search icon, hide times icon
        if (icons[0]) icons[0].style.display = '';
        if (icons[1]) icons[1].style.display = 'none';
      }
    }
  });
});
