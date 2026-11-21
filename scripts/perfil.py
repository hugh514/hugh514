"""Desenha a moldura do print do Almofadada usada no README.

Uso: python scripts/perfil.py assets
"""
import base64, os, sys
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "fontes")
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


def navegador(caminho, imagem, iw, ih, endereco, rotulo):
    """Print dentro de uma janela de navegador, com barra de endereço e sombra."""
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
    c.append(f'<image href="{jpeg(imagem)}" x="{m}" y="{m + barra}" width="{iw}" height="{ih}" clip-path="url(#tela)" preserveAspectRatio="xMinYMin slice"/>')
    salvar(caminho, w, h, rotulo, c)


if __name__ == "__main__":
    pasta = sys.argv[1]
    navegador(os.path.join(pasta, "molduras", "almofadada.svg"), os.path.join(pasta, "projetos", "almofadada.jpg"), 960, 416,
              "Almofadada na TV", "Quatro jogadores numa partida de futebol de duplas no Almofadada")
