// Glyph overrides on top of the Kɔradin Structure skeletons (Text weight; Display uses the hand-drawn SVGs in ovr/)
module.exports=function(K){
 const C=o=>JSON.parse(JSON.stringify(o));
 const flip=k=>{k=C(k);k.s.forEach(s=>s.v=s.v.map(([x,y])=>[x,-910-y]));return k};
 // ze: long bottom bar running right from the foot, as in the drawn Display ze
 const ze=C(K['se.liga']);ze.s[1].v=[[1250,-20],[549,-20],...ze.s[1].v.slice(1)];ze.s[1].r=[0,90,...(ze.s[1].r||[]).slice(1)];K['ze.liga']=ze;
 // zɛ: foot turns into a long bar to the right
 const zo=C(K['seopen.liga']);zo.s[1].v=[[1060,-20],[190,-20],...zo.s[1].v.slice(1)];zo.s[1].r=[0,120,...(zo.s[1].r||[]).slice(1)];K['zeopen.liga']=zo;
 // hy: z shapes flipped, bar on top (hye from zɛ, hyɛ from ze, as in Display)
 K['hye.liga']=flip(zo);K['hyeopen.liga']=flip(ze);
};
