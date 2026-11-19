import os, random, sys
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

random.seed(514)
FONTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes")


def texto_em_curvas(fonte, texto, tamanho, cx, base, cor):
    """Desenha o texto como path, para não depender da fonte de quem abre o SVG."""
    font = TTFont(os.path.join(FONTES, fonte + ".ttf"))
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    escala = tamanho / font["head"].unitsPerEm
    nomes = [cmap[ord(c)] for c in texto]
    largura = sum(glyphs[n].width for n in nomes) * escala
    x, partes = cx - largura / 2, []
    for n in nomes:
        pen = SVGPathPen(glyphs)
        glyphs[n].draw(TransformPen(pen, (escala, 0, 0, -escala, x, base)))
        partes.append(pen.getCommands())
        x += glyphs[n].width * escala
    return f'<path fill="{cor}" d="{" ".join(p for p in partes if p)}"/>'

W, H = 850, 300
WALL_Y = 168
tokens = ["const","await","func","SELECT","git push","return","import","async","type","defer","JOIN","interface","npm run","go test","useEffect","nest g","prisma","docker","SELECT *","WHERE","=>","{ }","err != nil","map()","export","grpc","redis","commit","merge","deploy","tsc","lint","fetch","schema","yield","enum","struct","chan","ctx","main"]
out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hugo Santos, desenvolvedor full stack em Ji-Paraná, Rondônia">')
a('''<defs>
<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#14121c"/><stop offset="0.45" stop-color="#3a2230"/><stop offset="0.8" stop-color="#9a4a2e"/><stop offset="1" stop-color="#d9823f"/>
</linearGradient>
<linearGradient id="muro" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#4a4650"/><stop offset="1" stop-color="#25232b"/>
</linearGradient>
<radialGradient id="sol" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffd08a" stop-opacity="0.9"/><stop offset="1" stop-color="#ffb060" stop-opacity="0"/></radialGradient>
<filter id="nevoa" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="6"/></filter>
<radialGradient id="leitura" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#18161d" stop-opacity="0.85"/><stop offset="1" stop-color="#18161d" stop-opacity="0"/></radialGradient>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="url(#ceu)"/>')
a(f'<circle cx="610" cy="{WALL_Y-8}" r="120" fill="url(#sol)"/>')
for i in range(40):
    x, y = random.uniform(0, W), random.uniform(5, 70)
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([0.6,0.8,1.1])}" fill="#fff" opacity="{random.uniform(.25,.7):.2f}"/>')
def gigante(cx, top, s, fill, olhos=False):
    # cabeça, pescoço e ombros genéricos, saindo de trás do muro
    hw, hh = 26*s, 34*s
    sh = top + hh*1.7
    p = (f'M{cx-hw*3.2:.1f},{WALL_Y+4} C{cx-hw*3.1:.1f},{sh:.1f} {cx-hw*1.4:.1f},{sh-6*s:.1f} {cx-hw*0.55:.1f},{top+hh*1.35:.1f} '
         f'L{cx-hw*0.6:.1f},{top+hh*0.9:.1f} C{cx-hw*1.05:.1f},{top+hh*0.6:.1f} {cx-hw*1.05:.1f},{top:.1f} {cx:.1f},{top:.1f} '
         f'C{cx+hw*1.05:.1f},{top:.1f} {cx+hw*1.05:.1f},{top+hh*0.6:.1f} {cx+hw*0.6:.1f},{top+hh*0.9:.1f} '
         f'L{cx+hw*0.55:.1f},{top+hh*1.35:.1f} C{cx+hw*1.4:.1f},{sh-6*s:.1f} {cx+hw*3.1:.1f},{sh:.1f} {cx+hw*3.2:.1f},{WALL_Y+4} Z')
    a(f'<path d="{p}" fill="{fill}" stroke="#e07a45" stroke-opacity="0.4" stroke-width="1.5"/>')
    if olhos:
        for dx in (-0.38, 0.38):
            a(f'<ellipse cx="{cx+hw*dx:.1f}" cy="{top+hh*0.48:.1f}" rx="{3.2*s:.1f}" ry="{1.8*s:.1f}" fill="#ffcf7a" opacity="0.85"/>')
    # vapor
    for k in range(3):
        x0 = cx + random.uniform(-hw*2, hw*2); y0 = top + hh*1.2
        d = random.uniform(5, 9); r = random.uniform(9, 16)*s
        a(f'<circle cx="{x0:.0f}" cy="{y0:.0f}" r="{r:.1f}" fill="#f3e6dc" opacity="0" filter="url(#nevoa)">'
          f'<animate attributeName="cy" values="{y0:.0f};{y0-60*s:.0f}" dur="{d:.1f}s" begin="{k*d/3:.1f}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0;0.35;0" dur="{d:.1f}s" begin="{k*d/3:.1f}s" repeatCount="indefinite"/></circle>')
gigante(150, 92, 1.0, "#2b1d24")
gigante(700, 58, 1.45, "#22171d", olhos=True)
gigante(430, 120, 0.75, "#33222a")
# muro
a(f'<rect x="0" y="{WALL_Y}" width="{W}" height="{H-WALL_Y}" fill="url(#muro)"/>')
a(f'<rect x="0" y="{WALL_Y}" width="{W}" height="5" fill="#6b6570"/>')
a(f'<rect x="0" y="{WALL_Y+5}" width="{W}" height="2" fill="#1a181e" opacity="0.6"/>')
row_h = 21
y = WALL_Y + 7
r = 0
while y < H:
    x = -random.uniform(0, 40) if r % 2 else -20
    while x < W:
        t = random.choice(tokens)
        bw = max(52, len(t)*6.4 + 22) + random.uniform(0, 26)
        a(f'<rect x="{x+1.5:.1f}" y="{y+1.5:.1f}" width="{bw-3:.1f}" height="{row_h-3}" rx="2" fill="#3b3842" stroke="#1c1a20" stroke-width="1" opacity="{random.uniform(.75,1):.2f}"/>')
        a(f'<text x="{x+bw/2:.1f}" y="{y+row_h/2+3.5:.1f}" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="9" fill="#a7a1ad" opacity="{random.uniform(.25,.5):.2f}">{t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")}</text>')
        x += bw
    y += row_h; r += 1
# placa com o nome
a(f'<ellipse cx="{W/2}" cy="{WALL_Y+70}" rx="260" ry="62" fill="url(#leitura)"/>')
a(texto_em_curvas("BarlowCondensed-ExtraBold", "HUGO SANTOS", 62, W/2, WALL_Y+80, "#f4ede4"))
a(texto_em_curvas("BarlowCondensed-Medium", "full stack em Ji-Paraná, Rondônia", 19, W/2, WALL_Y+106, "#e0b583"))
a('</svg>')
with open(sys.argv[1], 'w', encoding='utf-8') as f:
    f.write("\n".join(out))
