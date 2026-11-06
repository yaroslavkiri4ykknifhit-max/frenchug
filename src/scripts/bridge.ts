import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const nav=document.querySelector('.bridge-nav');
const navItems=[...document.querySelectorAll<HTMLElement>('.nav-item')];
function closeMenus(){navItems.forEach(item=>{item.classList.remove('open');item.querySelector('button')?.setAttribute('aria-expanded','false');});}
navItems.forEach(item=>item.querySelector('button')?.addEventListener('click',()=>{const open=item.classList.contains('open');closeMenus();if(!open){item.classList.add('open');item.querySelector('button')?.setAttribute('aria-expanded','true');}}));
document.addEventListener('click',event=>{if(!(event.target as Element).closest('.nav-item'))closeMenus();});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){const focused=document.querySelector<HTMLButtonElement>('.nav-item.open button');closeMenus();focused?.focus();}});
document.querySelectorAll('.nav-drop a').forEach(a=>a.addEventListener('click',closeMenus));
addEventListener('scroll',()=>nav?.classList.toggle('scrolled',scrollY>100),{passive:true});
const hamburger=document.querySelector<HTMLButtonElement>('.hamburger');
const mobileMenu=document.querySelector<HTMLElement>('#mobile-menu');
function closeMobile(){hamburger?.setAttribute('aria-expanded','false');if(mobileMenu)mobileMenu.hidden=true;}
hamburger?.addEventListener('click',()=>{const open=hamburger.getAttribute('aria-expanded')==='true';hamburger.setAttribute('aria-expanded',String(!open));if(mobileMenu)mobileMenu.hidden=open;});
mobileMenu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMobile));
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMobile();});
// Explicit vector icons avoid missing glyphs on platforms with limited system fonts.
document.querySelectorAll<HTMLElement>('.store-icon,.pink-app span,.back-top').forEach(el=>{el.innerHTML='<svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" stroke-width="2"/></svg>';});
document.querySelectorAll('a').forEach(a=>{[...a.childNodes].filter(n=>n.nodeType===Node.TEXT_NODE&&n.textContent?.includes('↗')).forEach(n=>{const pieces=n.textContent!.split('↗');const fragment=document.createDocumentFragment();pieces.forEach((p,i)=>{fragment.append(document.createTextNode(p));if(i<pieces.length-1){const span=document.createElement('span');span.className='inline-arrow';span.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14" fill="none" stroke="currentColor" stroke-width="2"/></svg>';fragment.append(span);}});n.replaceWith(fragment);});});
document.querySelectorAll('.review-stars').forEach(el=>{el.innerHTML=Array.from({length:5},()=>'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 1 3.3 7 7.7 1-5.6 5.5 1.4 7.5-6.8-3.7L5.2 22l1.4-7.5L1 9l7.7-1Z" fill="currentColor"/></svg>').join('');});
if(!reduced){
  const track=document.querySelector<HTMLElement>('.word-track');
  if(track){let index=0;const count=track.children.length;const cycle=()=>{index++;gsap.to(track,{y:()=>-index*(track.firstElementChild as HTMLElement).getBoundingClientRect().height,duration:.65,ease:'power3.inOut',onComplete:()=>{if(index===count-1){index=0;gsap.set(track,{y:0});}}});};setInterval(cycle,2700);addEventListener('resize',()=>gsap.set(track,{y:-index*(track.firstElementChild as HTMLElement).getBoundingClientRect().height}));}
  gsap.from('.hero-type',{opacity:0,y:40,duration:1,ease:'power3.out'});
  document.querySelectorAll<HTMLElement>('.step-copy,.intro-copy,.how-heading,.gold-title h2').forEach(el=>gsap.from(el,{y:60,opacity:0,duration:.85,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 94%',once:true}}));
  document.querySelectorAll<HTMLElement>('.banknote').forEach((el,i)=>gsap.fromTo(el,{y:45,rotate:i?10:-8},{y:-45,rotate:i?-6:5,ease:'none',scrollTrigger:{trigger:'.intro',start:'top bottom',end:'bottom top',scrub:1}}));
  gsap.fromTo('.green-word',{rotate:-4,y:35},{rotate:3,y:-20,ease:'none',scrollTrigger:{trigger:'.gold-title',start:'top bottom',end:'bottom top',scrub:1}});
  const counter=document.querySelector<HTMLElement>('.counter');
  if(counter){const n={value:0};gsap.to(n,{value:4619,duration:2,ease:'power2.out',scrollTrigger:{trigger:'.warp',start:'top 65%',once:true},onUpdate:()=>counter.textContent='+'+n.value.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})});}
}
// Keep layout and links usable even on devices without WebGL.
import('./bridge-baked').then(({mountBakedScenes})=>mountBakedScenes(reduced)).catch(error=>{console.error('Rendered scene initialization failed',error);});
