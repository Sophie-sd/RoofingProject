const HEADER_OFFSET = 96;

function scrollToSection(hash, behavior = 'smooth') {
  if (!hash || hash === '#') {
    return;
  }

  const target = document.querySelector(hash);
  if (!target) {
    return;
  }

  const top = target.getBoundingClientRect().top + window.scrollY - HEADER_OFFSET;
  window.scrollTo({ top: Math.max(top, 0), behavior });
}

function currentSection() {
  return window.location.hash === '#contacts' ? 'contacts' : 'faq';
}

function setActiveNav(section) {
  const isContactsPage = window.location.pathname.replace(/\/$/, '') === '/contacts';

  document.querySelectorAll('[data-nav-section]').forEach((link) => {
    const linkSection = link.dataset.navSection;
    let isActive = false;

    if (isContactsPage && (linkSection === 'faq' || linkSection === 'contacts')) {
      isActive = linkSection === section;
    } else {
      isActive = link.classList.contains('site-nav__link--active')
        || link.classList.contains('mobile-nav__link--active');
    }

    if (link.classList.contains('site-nav__link')) {
      link.classList.toggle('site-nav__link--active', isActive);
    }
    if (link.classList.contains('mobile-nav__link')) {
      link.classList.toggle('mobile-nav__link--active', isActive);
    }
  });
}

export function initAnchors() {
  if (window.location.hash) {
    requestAnimationFrame(() => scrollToSection(window.location.hash, 'auto'));
  }

  setActiveNav(currentSection());

  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href*="#"]');
    if (!link) {
      return;
    }

    const url = new URL(link.href, window.location.origin);
    if (!url.hash) {
      return;
    }

    const samePage = url.pathname.replace(/\/$/, '') === window.location.pathname.replace(/\/$/, '');
    if (samePage) {
      event.preventDefault();
      history.pushState(null, '', `${url.pathname}${url.hash}`);
      scrollToSection(url.hash);
      setActiveNav(url.hash === '#contacts' ? 'contacts' : 'faq');
    }
  });

  window.addEventListener('hashchange', () => {
    scrollToSection(window.location.hash);
    setActiveNav(currentSection());
  });
}
