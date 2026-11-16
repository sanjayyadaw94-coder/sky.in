const menu = document.querySelector('.menu-button');
const nav = document.querySelector('#navigation');
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); menu.focus();
  }
});
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.remove('awaiting'); observer.unobserve(entry.target); }
  }), {threshold: 0.08});
  document.querySelectorAll('.reveal').forEach(el => { el.classList.add('awaiting'); observer.observe(el); });
}
const cards = [...document.querySelectorAll('[data-category]')];
document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-filter]').forEach(other => {
    const active = other === button; other.classList.toggle('active', active); other.setAttribute('aria-pressed', String(active));
  });
  cards.forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; });
  document.querySelector('#filter-status').textContent = `${cards.filter(card => !card.hidden).length} credentials shown`;
}));
