const base = import.meta.env.BASE_URL + 'visuals/';
const version = '?v=original-3d-20261106b';

export function mountBakedScenes() {
  const staticScenes: Record<string, string> = {
    note: 'banknote.webp',
    phone: 'phone-welcome.webp',
    'phone-stats': 'phone-stats.webp',
    card: 'card.webp',
    green: 'green.webp',
  };

  document.querySelectorAll<HTMLElement>('[data-scene]').forEach(el => {
    const src = staticScenes[el.dataset.scene!];
    if (!src) return;
    const img = document.createElement('img');
    img.src = base + src + version;
    img.alt = '';
    img.decoding = 'async';
    img.loading = el.dataset.scene === 'note' ? 'eager' : 'lazy';
    img.className = 'rendered-scene';
    el.append(img);
  });

  const observer = new IntersectionObserver(entries => {
    for (const { target, isIntersecting } of entries) {
      target.classList.toggle('coin-motion-active', isIntersecting);
    }
  }, { rootMargin: '80px' });

  document.querySelectorAll('[data-coin-motion]').forEach(el => observer.observe(el));
}
