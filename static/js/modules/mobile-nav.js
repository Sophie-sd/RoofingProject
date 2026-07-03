export function syncMobileNav() {
  const isOpen = Boolean(document.querySelector('.mobile-drawer.is-open'));
  document.body.classList.toggle('nav-open', isOpen);
}

export function initMobileNav() {
  syncMobileNav();
}
