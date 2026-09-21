const viewer=document.querySelector('#image-viewer');
document.querySelectorAll('[data-zoom]').forEach(button=>button.addEventListener('click',()=>{
  const img=viewer.querySelector('img');img.src=button.dataset.zoom;img.alt=button.dataset.caption||'Project screen';
  viewer.querySelector('p').textContent=img.alt;viewer.showModal();
}));
viewer?.querySelector('button').addEventListener('click',()=>viewer.close());
viewer?.addEventListener('click',event=>{if(event.target===viewer)viewer.close()});
if(!matchMedia('(prefers-reduced-motion: reduce)').matches){const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in-view');observer.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll('.project-card,.about-teaser').forEach(el=>observer.observe(el));}
