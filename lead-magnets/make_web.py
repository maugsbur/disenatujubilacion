# -*- coding: utf-8 -*-
BASE_CSS = """
<style>
  body.web { background:#F8F9FA; }
  .web .page { box-shadow:0 2px 18px rgba(14,58,47,.10); margin:0 auto 26px;
               height:auto; min-height:0; padding-bottom:26mm; }
  .web .bar { position:fixed; left:50%; transform:translateX(-50%); bottom:18px; z-index:99;
              display:flex; gap:10px; align-items:center; }
  .web .hint { background:#0E3A2F; color:#F6E7B0; padding:11px 22px; border-radius:999px;
               font-size:14px; box-shadow:0 4px 18px rgba(0,0,0,.2); font-family:Poppins,sans-serif; }
  .web .pbtn { background:#E65F2B; color:#fff; border:0; padding:11px 20px; border-radius:999px;
               font-size:14px; cursor:pointer; box-shadow:0 4px 18px rgba(0,0,0,.2);
               font-family:Poppins,sans-serif; font-weight:500; }
  .web .bx { cursor:pointer; transition:all .12s; border-radius:2px; }
  .web .bx:hover { border-color:#E65F2B; color:#E65F2B; }
  .web .bx.on { background:#0E3A2F; border-color:#0E3A2F; color:#F6E7B0; }
  .web .cell.fill { background:#0E3A2F !important; border-color:#0E3A2F !important; color:#F6E7B0 !important; }
  .web .auto { font-family:'Lora',serif; font-size:15pt; font-weight:700; }
  .web .chk { cursor:pointer; transition:all .12s; position:relative; }
  .web .chk:hover { border-color:#E65F2B; }
  .web .chk.on { background:#0E3A2F; }
  .web .chk.on:after { content:"✓"; color:#F6E7B0; position:absolute; left:1mm; top:-1mm; font-size:11pt; }
  .web .blank[contenteditable] { outline:none; min-height:9mm; padding:1mm 2mm 0;
                                 font-size:11pt; font-family:Poppins,sans-serif; font-weight:300; }
  .web .blank[contenteditable]:focus { background:#F6E7B0; }
  @media print { .web .bar { display:none; } .web .page { box-shadow:none; margin:0; } }
</style>
"""

BAR = """
<script>
document.body.classList.add('web');
var bar=document.createElement('div'); bar.className='bar';
var hint=document.createElement('div'); hint.className='hint'; hint.id='hint';
var pb=document.createElement('button'); pb.className='pbtn'; pb.textContent='Imprimir o guardar en PDF';
pb.onclick=function(){window.print();};
bar.appendChild(hint); bar.appendChild(pb); document.body.appendChild(bar);
</script>
"""

DIAG_JS = """
<script>
var PIL=['Propósito','Físico','Mental','Social','Finanzas'];
document.querySelectorAll('.q').forEach(function(q){
  q.querySelectorAll('.bx').forEach(function(b,i){
    b.dataset.v=i+1;
    b.onclick=function(){
      q.querySelectorAll('.bx').forEach(function(x){x.classList.remove('on');});
      b.classList.add('on'); recalc();
    };
  });
});
function recalc(){
  var tot=[0,0,0,0,0], done=[0,0,0,0,0], ans=0;
  document.querySelectorAll('.q').forEach(function(q,i){
    var on=q.querySelector('.bx.on'), p=Math.floor(i/5);
    if(on){ tot[p]+=parseInt(on.dataset.v); done[p]++; ans++; }
  });
  document.querySelectorAll('.total-row .bl').forEach(function(el,i){
    el.innerHTML = done[i]===5 ? '<span class="auto">'+tot[i]+'</span>' : '';
  });
  document.querySelectorAll('.scoregrid tr').forEach(function(r,i){
    var full = done[i]===5;
    r.querySelectorAll('.cell').forEach(function(c,j){ c.classList.toggle('fill', full && (j+5)<=tot[i]); });
    var sc=r.querySelector('.sc .bl'); if(sc) sc.innerHTML = full ? '<span class="auto">'+tot[i]+'</span>' : '';
  });
  var h=document.getElementById('hint');
  if(ans<25){ h.textContent=ans+' de 25 respondidas'; }
  else { var min=Math.min.apply(null,tot);
    h.textContent='Listo. Tu pilar más bajo es '+PIL[tot.indexOf(min)]+', con '+min+' de 25'; }
}
recalc();
</script>
"""

PLAN_JS = """
<script>
document.querySelectorAll('.chk').forEach(function(c){
  c.onclick=function(){ c.classList.toggle('on'); upd(); };
});
function upd(){
  var n=document.querySelectorAll('.chk.on').length;
  var h=document.getElementById('hint');
  h.textContent = n===0 ? 'Marca cada una cuando la termines'
    : (n===4 ? 'Las cuatro listas. Bien ahí.' : n+' de 4 completadas');
}
upd();
</script>
"""

HABLAR_JS = """
<script>
var ph=['Nombre de la persona','Cuidados · Vivienda · Dinero · Bienes',
        'Escríbelo en una frase','Sé honesto acá','Qué le vas a decir, y cuándo'];
var pageBlanks=[];
document.querySelectorAll('.field').forEach(function(f,fi){
  f.querySelectorAll('.blank').forEach(function(b,bi){
    b.setAttribute('contenteditable','true');
    if(bi===0 && ph[fi]) b.dataset.ph=ph[fi];
    b.onfocus=function(){ if(b.textContent.trim()==='') b.textContent=''; upd(); };
    b.oninput=upd; pageBlanks.push(b);
  });
});
function upd(){
  var n=0; pageBlanks.forEach(function(b){ if(b.textContent.trim()!=='') n++; });
  var h=document.getElementById('hint');
  h.textContent = n===0 ? 'Puedes escribir directamente en la hoja de preparación'
                        : n+' de '+pageBlanks.length+' líneas escritas';
}
upd();
</script>
"""

def build(src_path, out_path, js):
    src = open(src_path).read()
    open(out_path,'w').write(src.replace('</body>', BASE_CSS + BAR + js + '</body>'))
    print("→", out_path.split('/')[-1])

build('autodiagnostico.html', '/mnt/user-data/outputs/autodiagnostico-interactivo.html', DIAG_JS)
build('plan.html',            '/mnt/user-data/outputs/guia-PLAN-interactiva.html',        PLAN_JS)
build('hablar.html',          '/mnt/user-data/outputs/guia-HABLAR-interactiva.html',      HABLAR_JS)
