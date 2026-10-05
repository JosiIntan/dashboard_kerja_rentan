import json

TEMPLATE = r"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700&family=Source+Sans+3:wght@400;600;700&display=swap');
html,body{margin:0;padding:0;background:transparent;color:#14213D;font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif}
#bc{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:2px 0 10px}
#angka{padding-right:14px;border-right:2px solid #E3E9F0;min-width:118px}
#v{display:block;font-family:'Bricolage Grotesque','Source Sans 3',sans-serif;font-weight:700;font-size:24px;line-height:1.05}
#p{display:block;font-size:12px;color:#5A6778;margin-top:2px}
#crumbs{display:flex;align-items:center;flex-wrap:wrap;gap:6px}
.chip{border:1px solid #CBD9E6;background:#fff;border-radius:999px;padding:6px 15px;font-family:inherit;font-weight:700;font-size:14px;color:#14213D;cursor:pointer}
.chip:hover{background:#EAF3FA}
.chip.aktif{background:linear-gradient(135deg,#0A84C8,#005B8F);color:#fff;border-color:transparent;cursor:default}
.sep{color:#9AA5B1;font-size:20px;line-height:1}
#wrap{position:relative;width:100%}
svg{display:block}
g.k{cursor:pointer}
g.k:hover rect{filter:brightness(1.08)}
text{font-family:'Source Sans 3','Segoe UI',system-ui,sans-serif}
#tip{position:absolute;display:none;pointer-events:none;background:#fff;border:1px solid #D5E2EE;border-radius:8px;
     padding:6px 10px;font-size:12px;line-height:1.4;box-shadow:0 8px 18px rgba(20,33,61,.2);white-space:nowrap;z-index:5}
</style></head>
<body>
<div id="bc"><div id="angka"><span id="v"></span><span id="p"></span></div><div id="crumbs"></div></div>
<div id="wrap"><svg id="svg"></svg><div id="tip"></div></div>
<script>
(function(){
const DATA = __DATA__;
const H0 = __H__;
const WARNA = ['#D9D9D9','#0072B2','#009E73','#E69F00'];
const TEKS  = ['#1A1A1A','#FFFFFF','#FFFFFF','#1A1A1A'];
const NS = 'http://www.w3.org/2000/svg';
const svg = document.getElementById('svg'), wrap = document.getElementById('wrap'), tip = document.getElementById('tip');
const total = DATA.value;

function fmtFull(n){ return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,'.'); }
function fmtPersen(x){ return (x*100).toFixed(1).replace('.',',') + '%'; }
function ringkas(n){
  if (n >= 1e6) return (n/1e6).toFixed(1).replace('.',',') + ' jt';
  if (n >= 1e3) return Math.round(n/1e3) + ' rb';
  return String(Math.round(n));
}
function juta(n){ return (n/1e6).toFixed(1).replace('.',',') + ' juta'; }

const nodes = [];
function bangun(n, depth, y0, parent){
  n.depth = depth; n.parent = parent; n.y0 = y0; n.y1 = y0 + n.value/total;
  nodes.push(n);
  let c = y0;
  (n.children||[]).forEach(function(ch){ bangun(ch, depth+1, c, n); c += ch.value/total; });
}
bangun(DATA, 0, 0, null);
function kedalaman(n){ let m = n.depth; (n.children||[]).forEach(function(c){ m = Math.max(m, kedalaman(c)); }); return m; }

let fokus = DATA;
const view = {y0:0, y1:1, d0:0, cols: kedalaman(DATA)+1};
function sasaran(){ return {y0:fokus.y0, y1:fokus.y1, d0:fokus.depth, cols: kedalaman(fokus)-fokus.depth+1}; }

const els = new Map();
nodes.forEach(function(n){
  const g = document.createElementNS(NS,'g'); g.setAttribute('class','k');
  const r = document.createElementNS(NS,'rect');
  const t = document.createElementNS(NS,'text');
  r.setAttribute('fill', WARNA[n.depth]); r.setAttribute('stroke','#fff'); r.setAttribute('stroke-width','2');
  t.setAttribute('fill', TEKS[n.depth]); t.setAttribute('pointer-events','none');
  g.appendChild(r); g.appendChild(t); svg.appendChild(g);
  g.addEventListener('click', function(){ klik(n); });
  g.addEventListener('mousemove', function(e){ tampil(n, e); });
  g.addEventListener('mouseleave', function(){ tip.style.display = 'none'; });
  els.set(n, {g:g, r:r, t:t});
});

function susunTeks(n, vw, vh){
  const pad = 8, tersedia = vw - 2*pad;
  const kata = n.name.split(' ');
  const terpanjang = Math.max.apply(null, kata.map(function(k){ return k.length; }));
  let fs = Math.min(14, tersedia/(terpanjang*0.62));
  if (fs < 8) return null;
  const baris = []; let cur = '';
  kata.forEach(function(k){
    const coba = cur ? cur+' '+k : k;
    if (!cur || coba.length*0.62*fs <= tersedia) cur = coba; else { baris.push(cur); cur = k; }
  });
  baris.push(cur);
  const angka = ringkas(n.value);
  let denganAngka = angka.length*0.58*fs <= tersedia;
  if (denganAngka && (baris.length+1)*fs*1.2 + pad > vh) denganAngka = false;
  if (baris.length*fs*1.2 + pad > vh) return null;
  return {fs:fs, baris:baris, angka: denganAngka ? angka : null, pad:pad};
}

function gambar(){
  const W = Math.max(wrap.clientWidth || 300, 120), H = H0;
  svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', '0 0 '+W+' '+H);
  const colW = W / view.cols, span = view.y1 - view.y0;
  nodes.forEach(function(n){
    const e = els.get(n);
    const x = (n.depth - view.d0) * colW, w = colW;
    const y = (n.y0 - view.y0)/span*H, h = (n.y1 - n.y0)/span*H;
    const tampilkan = x + w > 1 && x < W - 1 && y + h > 1 && y < H - 1;
    e.g.style.display = tampilkan ? '' : 'none';
    if (!tampilkan) return;
    e.r.setAttribute('x', x); e.r.setAttribute('y', y); e.r.setAttribute('width', w); e.r.setAttribute('height', Math.max(h,0));
    while (e.t.firstChild) e.t.removeChild(e.t.firstChild);
    const vx = Math.max(x,0), vy = Math.max(y,0);
    const vw = Math.min(x+w,W) - vx, vh = Math.min(y+h,H) - vy;
    if (vw < 40 || vh < 14) return;
    const s = susunTeks(n, vw, vh);
    if (!s) return;
    s.baris.forEach(function(b, i){
      const ts = document.createElementNS(NS,'tspan');
      ts.setAttribute('x', vx + s.pad); ts.setAttribute('y', vy + s.pad + s.fs*(i+0.85));
      ts.setAttribute('font-size', s.fs); ts.setAttribute('font-weight','700');
      ts.textContent = b; e.t.appendChild(ts);
    });
    if (s.angka){
      const ts = document.createElementNS(NS,'tspan');
      ts.setAttribute('x', vx + s.pad); ts.setAttribute('y', vy + s.pad + s.fs*(s.baris.length+0.85));
      ts.setAttribute('font-size', s.fs*0.92); ts.setAttribute('opacity','0.92');
      ts.textContent = s.angka; e.t.appendChild(ts);
    }
  });
}

let token = 0;
function animasi(){
  const awal = {y0:view.y0, y1:view.y1, d0:view.d0, cols:view.cols}, akhir = sasaran();
  const t0 = performance.now(), dur = 480, id = ++token;
  function langkah(t){
    if (id !== token) return;
    let p = Math.min(1, (t - t0)/dur);
    p = p < 0.5 ? 2*p*p : 1 - Math.pow(-2*p+2, 2)/2;
    ['y0','y1','d0','cols'].forEach(function(k){ view[k] = awal[k] + (akhir[k]-awal[k])*p; });
    gambar();
    if (p < 1) requestAnimationFrame(langkah);
  }
  requestAnimationFrame(langkah);
}

function perbaruiBC(){
  const jalur = []; for (let a = fokus; a; a = a.parent) jalur.unshift(a);
  const c = document.getElementById('crumbs'); c.innerHTML = '';
  jalur.forEach(function(n, i){
    if (i > 0){ const s = document.createElement('span'); s.className = 'sep'; s.textContent = '\u203A'; c.appendChild(s); }
    const b = document.createElement('button'); b.className = 'chip' + (n === fokus ? ' aktif' : '');
    b.textContent = n.name; b.addEventListener('click', function(){ pindah(n); }); c.appendChild(b);
  });
  document.getElementById('v').textContent = juta(fokus.value);
  document.getElementById('p').textContent = 'jiwa \u00B7 ' + fmtPersen(fokus.value/total) + ' dari total';
}
function pindah(n){ if (n === fokus) return; fokus = n; perbaruiBC(); animasi(); }
function klik(n){
  if (n === fokus){ if (n.parent) pindah(n.parent); return; }
  if (n.children && n.children.length) pindah(n);
}
function tampil(n, e){
  const r = wrap.getBoundingClientRect();
  tip.innerHTML = '<b>'+n.name+'</b><br>'+fmtFull(n.value)+' jiwa<br>'+fmtPersen(n.value/total)+' dari total'
    + (n.parent ? '<br>'+fmtPersen(n.value/n.parent.value)+' dari '+n.parent.name : '');
  tip.style.display = 'block';
  let left = e.clientX - r.left + 14; const top = e.clientY - r.top + 14;
  if (left + tip.offsetWidth > r.width) left = e.clientX - r.left - tip.offsetWidth - 10;
  tip.style.left = Math.max(left,0) + 'px'; tip.style.top = top + 'px';
}

perbaruiBC(); gambar();
window.addEventListener('resize', gambar);
if (window.ResizeObserver) new ResizeObserver(gambar).observe(wrap);
})();
</script></body></html>
"""


def icicle_zoom(pohon: dict, tinggi: int) -> str:
    """Kembalikan HTML siap pakai untuk st.components.v1.html (tinggi = tinggi area grafik dalam piksel)."""
    data = json.dumps(pohon, ensure_ascii=False)
    return TEMPLATE.replace("__DATA__", data).replace("__H__", str(int(tinggi)))
