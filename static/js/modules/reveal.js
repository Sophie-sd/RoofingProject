export function initReveal() {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    }),
    { threshold: 0.12, rootMargin: '0px 0px -48px 0px' },
  );

  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
}
