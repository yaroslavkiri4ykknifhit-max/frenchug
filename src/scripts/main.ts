import {gsap} from 'gsap';
import {ScrollTrigger} from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);
const menu=document.querySelector<HTMLButtonElement>('.menu-toggle');
const nav=document.querySelector<HTMLElement>('.mobile-nav');
function closeMenu(){if(!menu||!nav)return;menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Открыть меню');nav.hidden=true;}
menu?.addEventListener('click',()=>{if(!nav)return;const opened=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(opened));menu.setAttribute('aria-label',opened?'Закрыть меню':'Открыть меню');nav.hidden=!opened;});
nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus();}});
window.matchMedia('(min-width:701px)').addEventListener('change',e=>{if(e.matches)closeMenu();});
// No tracking network requests: a configured analytics adapter can consume this event.
document.querySelectorAll<HTMLElement>('[data-track]').forEach(el=>el.addEventListener('click',()=>{window.dispatchEvent(new CustomEvent('frenchug:analytics',{detail:{event:el.dataset.track,path:location.pathname}}));}));
const mm=gsap.matchMedia();
mm.add('(prefers-reduced-motion: no-preference)',()=>{
 const hero=document.querySelector('.hero');
 if(hero){
 const intro=gsap.timeline({defaults:{ease:'power3.out'}});
 intro.from('.hero-title .line',{yPercent:115,opacity:0,rotation:4,stagger:.11,duration:1.05},.08)
 .from('.hero-mark .f-object',{scale:.35,rotation:40,opacity:0,duration:1.25},.35)
 .from('.hero-mark .metal-chip,.hero-mark .spark',{scale:0,opacity:0,stagger:.09,duration:.8},.7)
 .from('.hero-meta,.hero-bottom',{opacity:0,y:12,duration:.65},.85);
 gsap.to('.hero-mark .f-object',{y:100,rotation:15,rotateY:30,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:1}});
 gsap.to('.hero-title',{y:-65,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:1}});
 gsap.to('.hero-mark .chip-one',{y:150,rotation:55,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:1}});
 gsap.to('.hero-mark .chip-two',{y:-100,rotation:-50,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:1}});
 }
 gsap.to('.scroll-progress',{scaleX:1,ease:'none',scrollTrigger:{trigger:document.documentElement,start:'top top',end:'bottom bottom',scrub:.2}});
 if(document.querySelector('.ticker-track'))gsap.to('.ticker-track',{xPercent:-50,duration:28,repeat:-1,ease:'none'});
 document.querySelectorAll<HTMLElement>('.word-reveal').forEach(el=>{
 el.childNodes.forEach(node=>{
 if(node.nodeType!==Node.TEXT_NODE)return;
 const fragment=document.createDocumentFragment();
 (node.textContent||'').split(/(\s+)/).filter(Boolean).forEach(part=>{
 if(/^\s+$/.test(part)){fragment.append(document.createTextNode(part));return;}
 const word=document.createElement('span');word.className='word';word.textContent=part;fragment.append(word);
 });node.replaceWith(fragment);
 });
 const words=el.querySelectorAll('.word');
 gsap.to(words,{color:'#fff',stagger:.2,ease:'none',scrollTrigger:{trigger:el,start:'top 85%',end:'bottom 50%',scrub:.3}});
 });
 if(document.querySelector('.asterisk'))gsap.to('.asterisk',{rotation:100,ease:'none',scrollTrigger:{trigger:'.manifesto',start:'top bottom',end:'bottom top',scrub:1}});
 document.querySelectorAll<HTMLElement>('.scene').forEach((el,index)=>{
 const art=el.querySelector('.scene-art>div');
 gsap.fromTo(art,{rotate:index===1?-22:-12,y:35},{rotate:index===1?18:8,y:-20,ease:'none',scrollTrigger:{trigger:el,start:'top bottom',end:'bottom top',scrub:1}});
 ScrollTrigger.create({trigger:el,start:'top center',end:'bottom center',onToggle:self=>{if(self.isActive){document.querySelectorAll('.step-index span').forEach((item,i)=>item.classList.toggle('active',i===index));}}});
 });
 if(document.querySelector('.telegram-art')){
 gsap.fromTo('.post-back',{y:70,rotation:-16},{y:-30,rotation:-7,ease:'none',scrollTrigger:{trigger:'.telegram-art',start:'top bottom',end:'bottom top',scrub:1}});
 gsap.fromTo('.post-front',{y:90,rotation:12},{y:-45,rotation:3,ease:'none',scrollTrigger:{trigger:'.telegram-art',start:'top bottom',end:'bottom top',scrub:1}});
 gsap.to('.paper-plane',{y:-65,x:15,rotation:23,ease:'none',scrollTrigger:{trigger:'.telegram-art',start:'top bottom',end:'bottom top',scrub:1}});
 }
 if(document.querySelector('.data-symbol'))gsap.to('.data-symbol',{rotation:10,ease:'none',scrollTrigger:{trigger:'.stats-tease',start:'top bottom',end:'bottom top',scrub:1}});
 if(document.querySelector('.final-link'))gsap.from('.final-arrow',{rotation:-40,scale:.7,ease:'none',scrollTrigger:{trigger:'.finale',start:'top bottom',end:'center center',scrub:1}});
 return()=>ScrollTrigger.getAll().forEach(t=>t.kill());
});
