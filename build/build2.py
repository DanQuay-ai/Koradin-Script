import json,math
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
import pathops
VOW={'a':'a','e':'e','eopen':'ɛ','i':'i','o':'o','oopen':'ɔ','u':'u'}
def P_from(ds,sh,dx=0,dy=0):
    P=pathops.Path();pen=P.getPen()
    for d in ds: parse_path(d,TransformPen(pen,(1,0,-sh,-1,dx,dy)))
    try:P.simplify(fix_winding=True)
    except Exception:pass
    return P
import re
from fontTools.svgLib import SVGPath
def P_svg(fn,flip=False):
    t=open(fn).read();t=re.sub(r'<g id="Layer_1" display="none">.*?</g>','',t,flags=re.S)
    P=pathops.Path();SVGPath.fromstring(t.encode(),transform=(1,0,0,-1,0,1000)).draw(P.getPen())
    try:P.simplify(fix_winding=True)
    except Exception:pass
    if flip:
        b=P.bounds;Q=pathops.Path();P.draw(TransformPen(Q.getPen(),(1,0,0,-1,0,b[1]+b[3])));P=Q
    return P
OVR_D={'zeopen.liga':'ovr/zeps.svg','hyeopen.liga':('ovr/ze.svg',True),'hye.liga':'ovr/hye.svg','ze.liga':'ovr/ze.svg','nyu.liga':'ovr/nyu.svg','niu.liga':'ovr/nyu.svg'}
def build(src,fam,sty,slant,gap,space,out):
    D=json.load(open(src));sh=math.tan(math.radians(slant))
    glyphs={};adv={};order=['.notdef','space'];cmap={32:'space'};anchors={};paths={}
    def add(name,P,a=None,lsb=gap/2,zero=False):
        b=P.bounds
        if zero:
            a=0;pen=T2CharStringPen(0,None);P.draw(pen);paths[name]=P
        elif b!=(0,0,0,0):
            a=int(b[2]-b[0]+gap);pen=T2CharStringPen(a,None);P.draw(TransformPen(pen,(1,0,0,1,lsb-b[0],0)))
            Q0=pathops.Path();P.draw(TransformPen(Q0.getPen(),(1,0,0,1,lsb-b[0],0)));paths[name]=Q0;OFF[name]=lsb-b[0]
            R=pathops.Path();rp=R.getPen();rp.moveTo((b[0]-10,b[1]-10));rp.lineTo((b[2]+10,b[1]-10));rp.lineTo((b[2]+10,b[1]+180));rp.lineTo((b[0]-10,b[1]+180));rp.closePath()
            I=pathops.op(P,R,pathops.PathOp.INTERSECTION);ib=I.bounds if I.bounds!=(0,0,0,0) else b
            anchors[name]=int((ib[0]+ib[2])/2+lsb-b[0])
        else:
            pen=T2CharStringPen(0,None)
        glyphs[name]=pen.getCharString();adv[name]=a or 0;order.append(name) if name not in order else None
    SH={};OFF={}
    CLIP={'pa.liga','ba.liga'}
    def clipr(P):
        # cut anything sticking out right of the box's vertical side (diagonal end cap)
        b=P.bounds;h=b[3]-b[1]
        R=pathops.Path();rp=R.getPen();rp.moveTo((b[0]-500,b[1]+h*0.15));rp.lineTo((b[2]+500,b[1]+h*0.15));rp.lineTo((b[2]+500,b[1]+h*0.5));rp.lineTo((b[0]-500,b[1]+h*0.5));rp.closePath()
        I=pathops.op(P,R,pathops.PathOp.INTERSECTION);xr=I.bounds[2]+ (b[3]-b[1])*0.0
        K2=pathops.Path();kp=K2.getPen();kp.moveTo((b[0]-500,b[1]-500));ym=b[1]+h*0.325;kp.lineTo((xr+sh*(b[1]-500-ym),b[1]-500));kp.lineTo((xr+sh*(b[3]+500-ym),b[3]+500));kp.lineTo((b[0]-500,b[3]+500));kp.closePath()
        return pathops.op(P,K2,pathops.PathOp.INTERSECTION)
    for g,v in D.items():
        if '#s' in g:
            P0=P_from(v['d'],sh);SH[g.split('#')[0].replace('.','_')]=clipr(P0) if g.split('#')[0] in CLIP else P0;continue
        if g.startswith('adk_') or g in('m.pre','n.pre','ng.pre','ng.liga') or g in('koopena.liga','koopene.liga'):continue
        add(g.replace('.','_'),(P_svg(*OVR_D[g]) if isinstance(OVR_D[g],tuple) else P_svg(OVR_D[g])) if ('Display' in fam and g in OVR_D) else P_svg('ovr/text-nyu.svg') if (g in ('nyu.liga','niu.liga')) else (clipr(P_from(v['d'],sh)) if g in CLIP else P_from(v['d'],sh)))
    # opening nasals (before the sign)
    for n in['m','n','ng']: add(n+'_pre',P_from(D[n+'.pre']['d'],sh))
    # closing nasals: marks centred on x=0 under the baseline
    def mark(ds,ref_y):
        P=P_from(ds,0);b=P.bounds;cx=(b[0]+b[2])/2;cy=(b[1]+b[3])/2
        Q=pathops.Path();P.draw(TransformPen(Q.getPen(),(1,0,0,1,-cx,ref_y-cy)));return Q
    ngP=P_from(D['ng.liga']['d'],0);yb=(ngP.bounds[1]+ngP.bounds[3])/2
    add('ng_close',mark(D['ng.liga']['d'],yb),zero=True)
    add('n_close',mark(D['n.pre']['d'],yb),zero=True)
    add('m_close',mark(D['m.pre']['d'],yb),zero=True)
    NASG={}
    for g0 in list(glyphs):
        if (g0.endswith('_liga') or g0 in VOW) and g0 in anchors:
            for n in ['n','m','ng']:
                Q=pathops.Path();paths[g0].draw(Q.getPen());paths[n+'_close'].draw(TransformPen(Q.getPen(),(1,0,0,1,anchors[g0],0)))
                try:Q.simplify(fix_winding=True)
                except Exception:pass
                nm=g0+'.'+n;pen=T2CharStringPen(adv[g0],None);Q.draw(pen);paths[nm]=Q;glyphs[nm]=pen.getCharString();adv[nm]=adv[g0];order.append(nm);NASG[(g0,n)]=nm
    # adinkra PUA
    pua=0xE000
    for g in sorted(k for k in D if k.startswith('adk_')):
        P=P_from(D[g]['d'],sh);b=P.bounds;h=b[3]-b[1];s=900/h if h else 1
        Q=pathops.Path();P.draw(TransformPen(Q.getPen(),(s,0,0,s,0,-b[1]*s)));nm=g.replace('-','_');add(nm,Q);cmap[pua]=nm;pua+=1
    glyphs['.notdef']=T2CharStringPen(space,None).getCharString();adv['.notdef']=space
    glyphs['space']=T2CharStringPen(space,None).getCharString();adv['space']=space
    for v,ch in VOW.items(): cmap[ord(ch)]=v
    for n,ch in [('zero','0'),('one','1'),('two','2'),('three','3'),('four','4'),('five','5'),('six','6'),('seven','7'),('eight','8'),('nine','9'),('period','.'),('comma',','),('exclam','!'),('question','?')]:
        if n in glyphs: cmap[ord(ch)]=n
    # bare consonant inputs: empty, zero width (only used inside ligatures)
    for c in sorted(set('hwypbktdjgszfvrlnm')):
        add('c_'+c,pathops.Path(),zero=True);cmap[ord(c)]='c_'+c
    gl=lambda ch:cmap[ord(ch)]
    rules=[]
    for g in glyphs:
        if g.endswith('_liga'):
            base=g[:-5];vk=next((v for v in['eopen','oopen','a','e','i','o','u'] if base.endswith(v)),None);on=base[:-len(vk)] if vk else ''
            if vk and on and (all(c in 'hwypbktdjgszfvrlnm' for c in on) or on=='ni'): rules.append((len(on)+1,' '.join([gl(c) if c in 'hwypbktdjgszfvrlnm' else c for c in on]+[vk]),g))
    for al,tg in [('ts','t'),('dz','d')]:
        for v in['eopen','oopen','a','e','i','o','u']:
            g=tg+v+'_liga'
            if g in glyphs: rules.append((3,' '.join([gl(al[0]),gl(al[1]),v]),g))
    rules.sort(key=lambda r:-r[0])
    syl=[g for g in glyphs if g.endswith('_liga')]+list(VOW)
    fea='languagesystem DFLT dflt;\n@SYL=['+' '.join(syl)+'];\n'
    fea+='lookup DROPM { sub c_m by NULL; } DROPM;\n'
    fea+='lookup TSDZ { sub c_t c_s by c_t; sub c_d c_z by c_d; } TSDZ;\n'
    fea+='lookup SYLL {\n'+''.join(f'  sub {s} by {g};\n' for _,s,g in rules)+'} SYLL;\n'
    fea+='lookup NGL { sub c_n c_g by ng_pre; } NGL;\n'
    fea+='lookup TOCLOSE { sub c_n by n_close; sub c_m by m_close; sub ng_pre by ng_close; } TOCLOSE;\n'
    fea+='lookup TOPRE { sub c_n by n_pre; sub c_m by m_pre; } TOPRE;\n'
    def vw(g):
        b=g[:-5]
        for v in ('oopen','eopen','a','e','i','o','u'):
            if b.endswith(v): return v
    SY=[g for g in glyphs if g.endswith('_liga') and '.' not in g]
    # filler before any following sign: back vowel -> ɔ, front -> ɛ (CRV rule extended to codas, e.g. Fante dawurbɔ = da-wu-rɔ-bɔ)
    R_BACK=[g for g in SY if vw(g) in('a','o','oopen','u')]
    R_FRONT=[g for g in SY if vw(g) in('e','eopen','i')]
    EP=[c for c in 'bdfgkptsrlhyvzj' if c+'oopen_liga' in glyphs and c+'eopen_liga' in glyphs]
    fea+='lookup EPO {'+''.join(f' sub c_{c} by {c}oopen_liga;' for c in EP)+' } EPO;\n'
    fea+='lookup EPE {'+''.join(f' sub c_{c} by {c}eopen_liga;' for c in EP)+' } EPE;\n'
    epi='  sub ['+' '.join('c_'+c for c in EP)+"]' lookup EPO ["+' '.join(R_BACK)+'];\n  sub ['+' '.join('c_'+c for c in EP)+"]' lookup EPE ["+' '.join(R_FRONT)+'];\n'
    FB=[c for c in 'hypbktdjgszfvrl' if c+'eopen_liga' in glyphs]
    fea+='lookup FALLB {'+''.join(f' sub c_{c} by {c}eopen_liga;' for c in FB)+' } FALLB;\n'
    vo=[g for g in glyphs if g in('oopen','ɔ')] or ['oopen']
    fea+='lookup WO { sub c_w by '+vo[0]+'; } WO;\n'
    fea+='feature liga {\n lookup TSDZ; lookup SYLL; lookup NGL;\n} liga;\n'
    fea+='feature calt {\n'+epi+'  sub ['+' '.join('c_'+c for c in FB)+"]' lookup FALLB;\n"+"  sub @SYL [c_n c_m ng_pre]' lookup TOCLOSE;\n  sub m_close c_m' lookup DROPM;\n  sub c_w' lookup WO;\n  sub [c_n c_m]' lookup TOPRE [@SYL "+' '.join('c_'+c for c in EP)+"];\n} calt;\n"
    fea+='lookup NASLIG {\n'+''.join(f'  sub {g0} {n}_close by {nm};\n' for (g0,n),nm in NASG.items())+'} NASLIG;\n'
    fea+='feature calt { lookup NASLIG; } calt;\n'
    # reduplication: short sign (height x0.74, same stroke) + dash inside the glyph box, as wide as the sign
    tk=110 if 'Slanted' in sty else 80
    def short(base):
        if base in SH:
            Q=pathops.Path();SH[base].draw(TransformPen(Q.getPen(),(1,0,0,1,OFF[base],0)));return Q
        P=paths[base];bb=P.bounds;cx=(bb[0]+bb[2])/2;f=0.74
        Q=pathops.Path();P.draw(TransformPen(Q.getPen(),(f,0,0,f,cx*(1-f),0)));return Q
    def dupg(g0,kind):
        base=g0.split('.')[0];nas=g0.split('.')[1] if '.' in g0 else None
        Q0=short(base);qb=Q0.bounds;top=CAP;T=CAP-tk*2.1;sy=T/max(qb[3],1)
        Q=pathops.Path();Q0.draw(TransformPen(Q.getPen(),(1,0,sh*(sy-1),sy,0,0)))
        if nas:
            paths[nas+'_close'].draw(TransformPen(Q.getPen(),(1,0,0,1,anchors[base],0)))
        sb=Q.bounds;x0=sb[0];x1=(adv[g0]+gap/2) if kind=='L' else sb[2]
        pn=Q.getPen();y0=top-tk;y1=top
        pn.moveTo((x0+sh*y0,y0));pn.lineTo((x1+sh*y0,y0));pn.lineTo((x1+sh*y1,y1));pn.lineTo((x0+sh*y1,y1));pn.closePath()
        try:Q.simplify(fix_winding=True)
        except Exception:pass
        nm=g0+'.dup'+kind;pen=T2CharStringPen(adv[g0],None);Q.draw(pen);glyphs[nm]=pen.getCharString();adv[nm]=adv[g0];order.append(nm);return nm
    import statistics
    CAP=statistics.median(paths[g].bounds[3] for g in order if g.endswith('_liga') and g in paths and paths[g].bounds[3]>0)
    BASES=[g for g in order if g.endswith('_liga') and g in anchors]+[v for v in VOW if v in anchors]
    ALLS=BASES+list(NASG.values())
    D1={g:dupg(g,'') for g in ALLS}
    DL={g:dupg(g,'L') for g in BASES};DR={g:dupg(g,'R') for g in BASES}
    fea+='lookup REDUP1 {\n'+''.join(f'  sub {g} {g} by {d};\n' for g,d in D1.items())+'} REDUP1;\n'
    fea+='lookup TOL {\n'+''.join(f'  sub {g} by {d};\n' for g,d in DL.items())+'} TOL;\n'
    fea+='lookup TOR {\n'+''.join(f'  sub {g} by {d};\n' for g,d in DR.items())+'} TOR;\n'
    pen=T2CharStringPen(0,None);glyphs['dupnull']=pen.getCharString();adv['dupnull']=0;order.append('dupnull')
    fea+='lookup DEL {\n'+''.join(f'  sub {g} by dupnull;\n' for g in BASES)+'} DEL;\n'
    fea+='lookup REDUP2 {\n'+''.join(f"  sub {a}' lookup TOL {b}' lookup TOR {a}' lookup DEL {b}' lookup DEL;\n" for a in BASES for b in BASES if a!=b)+'} REDUP2;\n'
    fea+='feature calt { lookup REDUP2; lookup REDUP1; } calt;\n'
    json.dump(sorted(g[:-5] for g in glyphs if g.endswith('_liga')),open(out+'.syl.json','w'))
    famd={}
    for g in glyphs:
        if g.endswith('_liga'):
            b=g[:-5];vk=next((v for v in['eopen','oopen','a','e','i','o','u'] if b.endswith(v)),None)
            if vk: famd.setdefault(b[:-len(vk)],[]).append(g)
    fea+='feature aalt {\n'+''.join(f'  sub {g} from [{" ".join(x for x in F if x!=g)}];\n' for F in famd.values() if len(F)>1 for g in F)+'} aalt;\n'
    # mark attachment: closing nasals hang under the centre of the sign
    fea+='markClass [n_close m_close ng_close] <anchor 0 0> @NAS;\n'
    fea+='feature mark {\n'+''.join(f'  pos base {g} <anchor {anchors[g]} 0> mark @NAS;\n' for g in syl if g in anchors)+'} mark;\n'
    fea+='table GDEF { GlyphClassDef ['+' '.join(g for g in glyphs if g not in('n_close','m_close','ng_close'))+'], , [n_close m_close ng_close], ; } GDEF;\n'
    order=['.notdef','space']+[n for n in order if n not in('.notdef','space')]
    fb=FontBuilder(1000,isTTF=False);fb.setupGlyphOrder(order);fb.setupCharacterMap(cmap)
    for n in order: glyphs[n]=glyphs[n]
    fb.setupCFF(fam.replace(' ','')+'-'+sty.replace(' ',''),{'FullName':fam+' '+sty},glyphs,{})
    fb.setupHorizontalMetrics({n:(adv[n],0) for n in order})
    fb.setupHorizontalHeader(ascent=1000,descent=-260);ps=fam.replace(' ','')+'-'+sty.replace(' ','')
    fb.setupNameTable({'familyName':fam,'styleName':('Bold Italic' if 'Slanted' in sty else sty),'uniqueFontIdentifier':ps+';0.4','fullName':fam+' '+sty,'psName':ps,'version':'Version 0.400','copyright':'(c) 2026 Ntirikwaamaa, Merankron','manufacturer':'Merankron','designer':'Ntirikwaamaa','typographicFamily':fam,'typographicSubfamily':sty})
    fb.setupMaxp()
    fb.setupOS2(fsSelection=(0x21 if 'Slanted' in sty else 0x40),usWeightClass=(700 if 'Slanted' in sty else 400),sTypoAscender=1000,sTypoDescender=-260,usWinAscent=1050,usWinDescent=300);fb.setupPost(italicAngle=-slant)
    addOpenTypeFeaturesFromString(fb.font,fea);fb.font['head'].macStyle=(3 if 'Slanted' in sty else 0);fb.save(out);print(out,len(order),'ligas',len(rules))
build('display.json','Sakyira Display','Bold Slanted',12,110,950,'SakyiraDisplay-BoldSlanted.otf')
build('text.json','Sakyira Text','Regular',0,90,800,'SakyiraText-Regular.otf')
