/** Original physically rendered Blender scenes. Canvas only composites their animation frames.
 * This matches the reference's pre-rendered media approach and works without WebGL.
 */
const base=import.meta.env.BASE_URL+'visuals/';
function load(src:string){return new Promise<HTMLImageElement>((resolve,reject)=>{const i=new Image();i.onload=()=>resolve(i);i.onerror=reject;i.src=src;});}
export async function mountBakedScenes(reduced:boolean){
 const staticScenes:Record<string,string>={note:'banknote.webp',phone:'phone-welcome.webp','phone-stats':'phone-stats.webp',card:'card.webp',green:'green.webp'};
 document.querySelectorAll<HTMLElement>('[data-scene]').forEach(el=>{const src=staticScenes[el.dataset.scene!];if(!src)return;const img=document.createElement('img');img.src=base+src;img.alt='';img.decoding='async';img.loading=el.dataset.scene==='note'?'eager':'lazy';img.className='rendered-scene';el.append(img);});
 const atlas=await load(base+'coins.webp');
 const slots=[...document.querySelectorAll<HTMLElement>('[data-scene="coin"],[data-scene="ribbon"],[data-scene="warp"]')].map((el,index)=>{const canvas=document.createElement('canvas');canvas.className='baked-canvas';el.append(canvas);return {el,canvas,ctx:canvas.getContext('2d')!,index,visible:false};});
 const observer=new IntersectionObserver(entries=>entries.forEach(e=>{const s=slots.find(s=>s.el===e.target);if(s)s.visible=e.isIntersecting;}),{rootMargin:'100px'});slots.forEach(s=>observer.observe(s.el));
 function drawCoin(ctx:CanvasRenderingContext2D,x:number,y:number,size:number,frame:number,rotation=0){const f=((Math.floor(frame)%32)+32)%32;ctx.save();ctx.translate(x,y);ctx.rotate(rotation);ctx.drawImage(atlas,(f%8)*256,Math.floor(f/8)*256,256,256,-size/2,-size/2,size,size);ctx.restore();}
 let last=0;const started=performance.now();
 function render(now:number){requestAnimationFrame(render);if(document.hidden||now-last<1000/(innerWidth<768?24:30))return;last=now;const t=reduced?0:(now-started)/1000;
 for(const s of slots){if(!s.visible)continue;const r=s.el.getBoundingClientRect(),w=r.width,h=r.height;if(!w||!h)continue;const dpr=Math.min(devicePixelRatio,1.75);if(s.canvas.width!==Math.round(w*dpr)||s.canvas.height!==Math.round(h*dpr)){s.canvas.width=Math.round(w*dpr);s.canvas.height=Math.round(h*dpr);}s.ctx.setTransform(dpr,0,0,dpr,0,0);s.ctx.clearRect(0,0,w,h);
 if(s.el.dataset.scene==='coin')drawCoin(s.ctx,w/2,h/2+Math.sin(t+s.index)*h*.015,w,t*6+s.index*11,s.index===0?-.15:.12);
 if(s.el.dataset.scene==='ribbon'){const size=h*1.08;for(let i=0;i<5;i++)drawCoin(s.ctx,w/2+(i-2)*w*.313,h/2,size,t*6+i*3);}
 if(s.el.dataset.scene==='warp'){for(let i=0;i<18;i++){const phase=(t*.062+i/18)%1;const angle=i*2.39996+t*.025;const radius=.12+phase*.75;const size=(.03+phase*.23)*w;drawCoin(s.ctx,w/2+Math.cos(angle)*radius*w,h/2+Math.sin(angle)*radius*h,size,t*6+i*4,Math.sin(i)*.25);}}
 }}requestAnimationFrame(render);
}
