import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

const root = document.querySelector('.fn-app');
if (root) {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const titleWord = document.getElementById('fn-changing-word');
  const words = ['EARN', 'TRADE', 'THINK', 'WIN'];
  if (titleWord && !reduceMotion) {
    let index = 0;
    window.setInterval(() => {
      gsap.to(titleWord, { yPercent: -110, opacity: 0, duration: .28, ease: 'power2.in', onComplete: () => {
        index = (index + 1) % words.length;
        titleWord.textContent = words[index];
        gsap.fromTo(titleWord, { yPercent: 105, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .48, ease: 'power3.out' });
      }});
    }, 3300);
  }

  if (!reduceMotion) {
    const heroTimeline = gsap.timeline({ defaults: { ease: 'power3.out' } });
    heroTimeline.from('.fn-hero-title .fn-swap-word', { y: 80, opacity: 0, duration: .9 }, 0)
      .from('.fn-hero-title-lower', { y: 100, opacity: 0, duration: .95 }, .13)
      .from('.fn-hero-sticker', { scale: .2, rotate: -35, opacity: 0, duration: .85 }, .38)
      .from('.fn-hero-coins .fn-coin', { scale: .1, y: 140, rotate: -50, opacity: 0, duration: 1.15, stagger: .14 }, .3)
      .from('.fn-hero-footer', { y: 20, opacity: 0, duration: .65 }, .75);

    gsap.to('.fn-hero-title', { yPercent: -24, ease: 'none', scrollTrigger: { trigger: '.fn-hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.fn-hero-coins .fn-coin', { y: (index: number) => index % 2 ? -180 : 180, rotate: (index: number) => index % 2 ? -30 : 40, ease: 'none', stagger: .02, scrollTrigger: { trigger: '.fn-hero', start: 'top top', end: 'bottom top', scrub: 1.2 } });

    gsap.utils.toArray<HTMLElement>('.fn-fade-up').forEach((el) => {
      gsap.from(el, { y: 85, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
    });
    gsap.utils.toArray<HTMLElement>('.fn-how-art').forEach((el) => {
      gsap.fromTo(el, { rotate: -4, y: 55 }, { rotate: 3, y: -35, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
    gsap.utils.toArray<HTMLElement>('.fn-earn-art .fn-coin, .fn-metal .fn-coin, .fn-counter .fn-coin').forEach((el, i) => {
      gsap.fromTo(el, { y: 90 }, { y: -80, rotate: i % 2 ? 24 : -24, ease: 'none', scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: 1 } });
    });

    const counter = document.querySelector<HTMLElement>('[data-counter]');
    if (counter) {
      const values = { value: 0 };
      gsap.to(values, { value: 4619, duration: 2.25, ease: 'power2.out', scrollTrigger: { trigger: counter, start: 'top 83%', once: true }, onUpdate: () => {
        counter.textContent = Math.round(values.value).toLocaleString('en-US');
      }});
    }
  }
}
