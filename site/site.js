// Progressive disclosure: native links stay visible until initialization succeeds.
const initialized = new WeakMap();
export function initNavigation(root = document, { matchMedia } = {}) {
  const header = root.querySelector('header');
  if (!header || initialized.has(header)) return initialized.get(header);
  const button = header.querySelector('[data-navigation-toggle]');
  const nav = header.querySelector('nav');
  if (!button || !nav || button.getAttribute('aria-controls') !== nav.id) return;
  const win = root.defaultView;
  const media = (matchMedia || win.matchMedia.bind(win))('(min-width: 48rem)');
  let open = false;
  function measureHeader() {
    if (header.classList.contains('site-header')) {
      root.documentElement.style.setProperty('--header-height', `${header.getBoundingClientRect().height}px`);
    }
  }
  if (header.classList.contains('site-header') && win.ResizeObserver) {
    const observer = new win.ResizeObserver(measureHeader);
    observer.observe(header);
  }
  function render() {
    if (media.matches) {
      nav.hidden = false;
      if (root.activeElement === button) nav.querySelector('a')?.focus();
      button.hidden = true;
    } else {
      button.hidden = false;
      if (!open && nav.contains(root.activeElement)) button.focus();
      nav.hidden = !open;
    }
    button.setAttribute('aria-expanded', String(media.matches || open));
    measureHeader();
  }
  function close() { open = false; render(); }
  button.addEventListener('click', () => { open = !open; render(); });
  header.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !media.matches && open) {
      close(); button.focus();
    }
  });
  nav.addEventListener('click', event => {
    if (event.target.closest('a[href]')) close(); // Never cancel native navigation.
  });
  media.addEventListener('change', close);
  const state = { close };
  initialized.set(header, state);
  render();
  return state;
}
initNavigation();
