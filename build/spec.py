import uharfbuzz as hb,cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
def line(fp,text,size,y,fill):
    blob=hb.Blob.from_file_path(fp);face=hb.Face(blob);font=hb.Font(face);buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();hb.shape(font,buf,{"liga":True,"calt":True,"mark":True})
    t=TTFont(fp);gs=t.getGlyphSet();order=t.getGlyphOrder();s=size/1000;x=60;o=''
    for i,p in zip(buf.glyph_infos,buf.glyph_positions):
        pen=SVGPathPen(gs);gs[order[i.codepoint]].draw(pen);o+=f'<path transform="translate({x+p.x_offset*s:.1f},{y-p.y_offset*s}) scale({s},{-s})" d="{pen.getCommands()}" fill="{fill}"/>';x+=p.x_advance*s
    return o,x
D,T='SakyiraDisplay-BoldSlanted.otf','SakyiraText-Regular.otf'
parts=[];w=0
for fp,txt,sz,y,c in [(D,'mfantse',110,160,'#c8262b'),(D,'bayir aboakyer',90,320,'#efe7da'),(T,'mfantse bayir aboakyer nkwa akan kɔm',44,440,'#efe7da'),(T,'dzi tsetse fra kyer nii onie',44,510,'#ee9fb3')]:
    o,x=line(fp,txt,sz,y,c);parts.append(o);w=max(w,x)
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(w+60)}" height="600"><rect width="100%" height="100%" fill="#0d1322"/>{"".join(parts)}</svg>'
open('specimen.svg','w').write(svg);cairosvg.svg2png(bytestring=svg.encode(),write_to='specimen.png')
