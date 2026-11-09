const base = import.meta.env.BASE_URL + 'visuals/';
const version = '?v=original-3d-20261106b';

export function mountBakedScenes() {
  const staticScenes: Record<string, string> = {
    note: 'banknote.webp',
    phone: 'phone-welcome.webp',
    'phone-stats': 'phone-stats.webp',
    card: 'card.webp',
    wordmark: 'frenugo.webp',
  };

  document.querySelectorAll<HTMLElement>('[data-scene]').forEach(el => {
    const src = staticScenes[el.dataset.scene!];
    if (!src) return;
    const img = document.createElement('img');
    img.src = base + src + (src.startsWith('phone-') ? '?v=ru' : version);
    img.alt = '';
    img.decoding = 'async';
    img.loading = el.dataset.scene === 'note' ? 'eager' : 'lazy';
    img.className = 'rendered-scene';
    el.append(img);
  });

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const scenes = new Map(
    Array.from(document.querySelectorAll<HTMLElement>('[data-coin-motion]'), scene => [
      scene,
      Array.from(scene.querySelectorAll<HTMLImageElement>('.coin-image'), image => ({
        image,
        still: image.src,
      })),
    ]),
  );

  const setCoinSource = (scene: HTMLElement) => {
    const spin = !reducedMotion.matches && scene.classList.contains('coin-motion-active')
      ? scene.dataset.coinMotion
      : undefined;
    for (const { image, still } of scenes.get(scene) ?? []) {
      const src = spin ?? still;
      if (image.getAttribute('src') !== src) image.src = src;
    }
  };

  const observer = new IntersectionObserver(entries => {
    for (const { target, isIntersecting } of entries) {
      const scene = target as HTMLElement;
      scene.classList.toggle('coin-motion-active', isIntersecting);
      setCoinSource(scene);
    }
  }, { rootMargin: '80px' });

  for (const scene of scenes.keys()) observer.observe(scene);
  reducedMotion.addEventListener('change', () => {
    for (const scene of scenes.keys()) setCoinSource(scene);
  });
}
