import { initAnchors } from './modules/anchors.js';
import { initChatWidget } from './modules/chat.js';
import { initMobileNav, syncMobileNav } from './modules/mobile-nav.js';
import { initReveal } from './modules/reveal.js';

document.addEventListener('DOMContentLoaded', () => {
  initReveal();
  initAnchors();
  initMobileNav();
  initChatWidget();
});

document.body.addEventListener('htmx:afterSettle', () => {
  syncMobileNav();
});

document.body.addEventListener('htmx:afterSwap', () => {
  initReveal();
  syncMobileNav();
});
