const menu = document.querySelector('.menu-button');
const nav = document.querySelector('#navigation');

function setMenuOpen(open) {
  if (!menu || !nav) return;
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
}
menu?.addEventListener('click', () => {
  setMenuOpen(menu.getAttribute('aria-expanded') !== 'true');
});
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenuOpen(false)));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    setMenuOpen(false);
    menu.focus();
  }
});
document.addEventListener('click', event => {
  if (nav && menu && !nav.contains(event.target) && !menu.contains(event.target)) {
    setMenuOpen(false);
  }
});

if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.remove('awaiting');
      observer.unobserve(entry.target);
    }
  }), { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(element => {
    element.classList.add('awaiting');
    observer.observe(element);
  });
}

const filterButtons = [...document.querySelectorAll('[data-filter]')];
const filterCards = [...document.querySelectorAll('[data-category]')];
const filterStatus = document.querySelector('#filter-status');

function applyCardFilter(value) {
  if (!filterButtons.length || !filterCards.length) return;
  filterButtons.forEach(button => {
    const selected = button.dataset.filter === value;
    button.classList.toggle('active', selected);
    button.setAttribute('aria-pressed', String(selected));
  });
  filterCards.forEach(card => {
    card.hidden = value !== 'all' && card.dataset.category !== value;
  });
  if (filterStatus) {
    const count = filterCards.filter(card => !card.hidden).length;
    const noun = filterStatus.dataset.noun || 'credentials';
    filterStatus.textContent = `${count} ${noun} shown`;
  }
}
filterButtons.forEach(button => button.addEventListener('click', () => applyCardFilter(button.dataset.filter)));
if (filterButtons.length) applyCardFilter(filterButtons.find(button => button.classList.contains('active'))?.dataset.filter || 'all');
