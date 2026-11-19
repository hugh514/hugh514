"""Desenha as imagens do README: o cabeçalho e as molduras dos prints dos projetos.

Uso: python scripts/perfil.py assets
"""
import base64, os, random, sys
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "fontes")
TOKENS = ["const", "await", "func", "SELECT", "git push", "return", "import", "async", "type", "defer",
          "JOIN", "interface", "npm run", "go test", "useEffect", "prisma", "docker", "WHERE", "=>", "{ }",
          "err != nil", "map()", "export", "grpc", "redis", "commit", "merge", "deploy", "fetch", "schema"]
SOMBRA = '<filter id="sombra" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity="0.35"/></filter>'


def texto_em_curvas(fonte, texto, tamanho, x, base, cor, centro=False):
    """Desenha o texto como path, para não depender da fonte de quem abre o SVG."""
    font = TTFont(os.path.join(FONTES, fonte + ".ttf"))
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    escala = tamanho / font["head"].unitsPerEm
    nomes = [cmap[ord(c)] for c in texto]
    if centro:
        x -= sum(glyphs[n].width for n in nomes) * escala / 2
    partes = []
    for n in nomes:
        pen = SVGPathPen(glyphs)
        glyphs[n].draw(TransformPen(pen, (escala, 0, 0, -escala, x, base)))
        partes.append(pen.getCommands())
        x += glyphs[n].width * escala
    return f'<path fill="{cor}" d="{" ".join(p for p in partes if p)}"/>'


def jpeg(caminho):
    with open(caminho, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def salvar(caminho, w, h, rotulo, corpo):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{rotulo}">\n'
                + "\n".join(corpo) + "\n</svg>")


def cabecalho(caminho):
    """Faixa escura com o nome, e uma parede de código bem apagada ao fundo."""
    w, h = 850, 220
    c = [f'<defs><clipPath id="canto"><rect width="{w}" height="{h}" rx="14"/></clipPath>'
         f'<linearGradient id="luz" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e0b583"/><stop offset="1" stop-color="#e0b583" stop-opacity="0"/></linearGradient></defs>',
         '<g clip-path="url(#canto)">', f'<rect width="{w}" height="{h}" fill="#101216"/>', '<g opacity="0.35">']
    y = 0
    while y < h:
        x = -random.uniform(0, 40)
        while x < w:
            t = random.choice(TOKENS)
            bw = max(52, len(t) * 6.4 + 22) + random.uniform(0, 26)
            c.append(f'<rect x="{x + 1.5:.1f}" y="{y + 1.5:.1f}" width="{bw - 3:.1f}" height="18" rx="2" fill="#1c1f25"/>')
            c.append(f'<text x="{x + bw / 2:.1f}" y="{y + 14:.1f}" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace" '
                     f'font-size="9" fill="#5d636d">{t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</text>')
            x += bw
        y += 21
    c.append('</g>')
    c.append(f'<rect width="{w}" height="{h}" fill="#101216" opacity="0.55"/>')
    c.append(f'<rect x="48" y="{h - 4}" width="420" height="4" fill="url(#luz)"/>')
    c.append(texto_em_curvas("BarlowCondensed-ExtraBold", "Hugo Santos", 72, 48, 112, "#f4f1ec"))
    c.append(texto_em_curvas("BarlowCondensed-Medium", "Full stack em Ji-Paraná, Rondônia", 24, 50, 150, "#e0b583"))
    c.append(texto_em_curvas("BarlowCondensed-Medium", "Cuido de vários sistemas internos num provedor de internet daqui.", 19, 50, 182, "#9ea3ab"))
    c.append('</g>')
    salvar(caminho, w, h, "Hugo Santos, full stack em Ji-Paraná, Rondônia. Cuido de vários sistemas internos num provedor de internet daqui.", c)


def navegador(caminho, imagem, iw, ih, endereco, rotulo, corte=0):
    """Print dentro de uma janela de navegador, com barra de endereço e sombra. corte tira pixels da direita do print."""
    m, barra = 24, 40
    w, h = iw + 2 * m, ih + barra + 2 * m
    c = [f'<defs>{SOMBRA}<clipPath id="tela"><path d="M{m},{m + barra} H{m + iw} V{m + barra + ih - 12} '
         f'Q{m + iw},{m + barra + ih} {m + iw - 12},{m + barra + ih} H{m + 12} Q{m},{m + barra + ih} {m},{m + barra + ih - 12} Z"/></clipPath></defs>',
         f'<rect x="{m}" y="{m}" width="{iw}" height="{ih + barra}" rx="12" fill="#1f2228" filter="url(#sombra)"/>',
         f'<rect x="{m}" y="{m}" width="{iw}" height="{ih + barra}" rx="12" fill="none" stroke="#33373f"/>']
    for i, cor in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        c.append(f'<circle cx="{m + 22 + i * 20}" cy="{m + barra / 2}" r="6" fill="{cor}"/>')
    c.append(f'<rect x="{m + iw / 2 - 170}" y="{m + 9}" width="340" height="22" rx="11" fill="#2b2f36"/>')
    c.append(texto_em_curvas("BarlowCondensed-Medium", endereco, 15, m + iw / 2, m + 25, "#a7acb4", centro=True))
    c.append(f'<image href="{jpeg(imagem)}" x="{m}" y="{m + barra}" width="{iw + corte}" height="{ih}" clip-path="url(#tela)" preserveAspectRatio="xMinYMin slice"/>')
    salvar(caminho, w, h, rotulo, c)


def celular(caminho, imagem, iw, ih, rotulo):
    """Print de celular deitado, com borda arredondada e sombra."""
    m, b = 24, 14
    w, h = iw + 2 * (m + b), ih + 2 * (m + b)
    c = [f'<defs>{SOMBRA}<clipPath id="tela"><rect x="{m + b}" y="{m + b}" width="{iw}" height="{ih}" rx="26"/></clipPath></defs>',
         f'<rect x="{m}" y="{m}" width="{iw + 2 * b}" height="{ih + 2 * b}" rx="40" fill="#0c0d10" filter="url(#sombra)"/>',
         f'<rect x="{m}" y="{m}" width="{iw + 2 * b}" height="{ih + 2 * b}" rx="40" fill="none" stroke="#3a3e46" stroke-width="2"/>',
         f'<image href="{jpeg(imagem)}" x="{m + b}" y="{m + b}" width="{iw}" height="{ih}" clip-path="url(#tela)"/>',
         f'<rect x="{m + 4}" y="{m + b + ih / 2 - 40}" width="6" height="80" rx="3" fill="#1d1f24"/>']
    salvar(caminho, w, h, rotulo, c)


if __name__ == "__main__":
    random.seed(514)
    pasta = sys.argv[1]
    fotos = os.path.join(pasta, "projetos")
    cabecalho(os.path.join(pasta, "cabecalho.svg"))
    navegador(os.path.join(pasta, "molduras", "almofadada.svg"), os.path.join(fotos, "almofadada.jpg"), 960, 416,
              "Almofadada na TV", "Quatro jogadores numa partida de futebol de duplas no Almofadada")
    celular(os.path.join(pasta, "molduras", "controle.svg"), os.path.join(fotos, "controle.jpg"), 844, 390,
            "O celular virando controle, com joystick e botões")
    navegador(os.path.join(pasta, "molduras", "silvanias.svg"), os.path.join(fotos, "silvanias.jpg"), 960, 570,
              "silvanias-site.vercel.app", "Página inicial do site da Silvania's Cacau", corte=14)
    navegador(os.path.join(pasta, "molduras", "barbearia.svg"), os.path.join(fotos, "barbearia.jpg"), 960, 600,
              "Painel da barbearia", "Dashboard do painel da barbearia com receita, atendimentos e clientes do mês")
