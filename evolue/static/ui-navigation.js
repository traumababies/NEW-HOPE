/* ui-navigation.js — stub for Évolué nav. Full version loads from CDN or build. */
document.addEventListener('DOMContentLoaded', function() {
  // Dropdown submenus via hover/focus
  document.querySelectorAll('.nav-group').forEach(function(group) {
    var submenu = group.querySelector('.nav-submenu');
    if (!submenu) return;
    group.addEventListener('mouseenter', function() { submenu.style.display = 'flex'; });
    group.addEventListener('mouseleave', function() { submenu.style.display = 'none'; });
  });
});