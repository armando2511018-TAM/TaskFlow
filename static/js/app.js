document.addEventListener('DOMContentLoaded', () => {
  const todayLabel = document.querySelector('#todayLabel');
  if (todayLabel) todayLabel.textContent = new Intl.DateTimeFormat('es-MX', { day: 'numeric', month: 'short' }).format(new Date());

  const menuButton = document.querySelector('#menuButton');
  const sidebar = document.querySelector('#sidebar');
  const overlay = document.querySelector('#sidebarOverlay');
  const toggleMenu = () => {
    const open = sidebar.classList.toggle('open');
    overlay.classList.toggle('show', open);
    menuButton.setAttribute('aria-expanded', String(open));
  };
  menuButton?.addEventListener('click', toggleMenu);
  overlay?.addEventListener('click', toggleMenu);

  document.querySelectorAll('.flash button').forEach(button => button.addEventListener('click', () => button.parentElement.remove()));
  setTimeout(() => document.querySelectorAll('.flash').forEach(flash => flash.classList.add('leaving')), 4200);

  const cards = [...document.querySelectorAll('.task-card')];
  const filters = [...document.querySelectorAll('.filter-chip')];
  const search = document.querySelector('#globalSearch');
  const noResults = document.querySelector('#noResults');
  let activeFilter = 'all';
  const updateTasks = () => {
    const term = (search?.value || '').trim().toLowerCase();
    let visible = 0;
    cards.forEach(card => {
      const matchesFilter = activeFilter === 'all' || card.dataset.priority === activeFilter;
      const matchesSearch = !term || card.dataset.search.includes(term);
      card.hidden = !(matchesFilter && matchesSearch);
      if (!card.hidden) visible++;
    });
    if (noResults) noResults.hidden = visible !== 0 || cards.length === 0;
  };
  filters.forEach(filter => filter.addEventListener('click', () => {
    filters.forEach(item => item.classList.remove('active'));
    filter.classList.add('active');
    activeFilter = filter.dataset.filter;
    updateTasks();
  }));
  search?.addEventListener('input', updateTasks);
  document.addEventListener('keydown', event => {
    if (event.key === '/' && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
      event.preventDefault(); search?.focus();
    }
  });

  const title = document.querySelector('#titulo');
  const titleCount = document.querySelector('#titleCount');
  title?.addEventListener('input', () => { titleCount.textContent = title.value.length; });
  const date = document.querySelector('#fecha_limite');
  if (date) date.min = new Date().toISOString().split('T')[0];
});
