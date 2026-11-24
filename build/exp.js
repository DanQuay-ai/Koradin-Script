const {KE,K,A,T}=require('./eng.js');const fs=require('fs');require('./ovr.js')(K);
function run(name,w,o,style){const out={};
 for(const g in K){const sk=K[g];if(!sk.s.length&&!(sk.d||[]).length)continue;
  const cw=KE.capWeight(sk,w,o);const L=KE.layout(sk,cw,o);out[g]={d:[...KE.render(L,{style}).matchAll(/ d="([^"]+)"/g)].map(m=>m[1]),fr:[...KE.render(L,{style}).matchAll(/fill-rule="([^"]+)"/g)].map(m=>m[1])};
  if(/\.liga$/.test(g)||g.length==1){const os=Object.assign({},o,{kv:o.kv*0.76});const Ls=KE.layout(sk,KE.capWeight(sk,w*(w>150?0.84:0.95),os),os);out[g+'#s']={d:[...KE.render(Ls,{style}).matchAll(/ d="([^"]+)"/g)].map(m=>m[1])}}}
 for(const a in A){const sk=A[a];const ao=Object.assign({},o,{S:43,kv:Math.max(.75,o.kv),kh:Math.max(.75,o.kh),grow:sk.grow||1.3});
  const L=KE.layout(sk,KE.capWeight(sk,w,ao),ao);const r=KE.render(L,{style});out['adk_'+a]={d:[...r.matchAll(/ d="([^"]+)"/g)].map(m=>m[1]),name:T[a]||a}}
 fs.writeFileSync(name+'.json',JSON.stringify(out))}
run('display',175,{S:80,kv:1,kh:1.1,kr:0.5},'cut');
run('text',88,{S:62,kv:1,kh:1,kr:1.6},'cut');
