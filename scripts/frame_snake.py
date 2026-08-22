"""Envolve o SVG do snake num painel igual aos outros cards do perfil.

O Platane/snk gera um SVG solto, sem fundo nem borda, de 880x192. Solto na
pagina ele era o unico bloco sem moldura, entre cinco cards escuros com
cabecalho em prompt. Este script embute o SVG original num <svg> aninhado
(que preserva o viewBox e as animacoes dele) dentro de um card com o mesmo
fundo, borda e cabecalho dos demais.

Uso: python3 scripts/frame_snake.py <entrada.svg> <saida.svg> [username]
"""

import re
import sys
from xml.sax.saxutils import escape

CARD_W = 850
PAD_X = 30
HEADER_H = 74
BOTTOM_PAD = 26

NEBULA = "#0f1623"
STAR_DUST = "#1a2332"
ACCENT = "#00d4ff"


def frame(svg_text: str, username: str = "") -> str:
    open_tag = re.search(r"<svg\b[^>]*>", svg_text)
    if not open_tag:
        raise ValueError("SVG de entrada sem tag <svg>")

    attrs = open_tag.group(0)
    view_box = re.search(r'viewBox="([^"]+)"', attrs)
    width = re.search(r'width="([\d.]+)"', attrs)
    height = re.search(r'height="([\d.]+)"', attrs)
    if not (view_box and width and height):
        raise ValueError("SVG de entrada sem viewBox, width ou height")

    src_w, src_h = float(width.group(1)), float(height.group(1))
    inner_w = CARD_W - 2 * PAD_X
    inner_h = src_h * inner_w / src_w
    card_h = round(HEADER_H + inner_h + BOTTOM_PAD)

    body = svg_text[open_tag.end():]
    body = re.sub(r"</svg>\s*$", "", body).strip()

    handle = f"{username}@github" if username else "github"
    prompt = escape(f"{handle}:~$ ./contributions")

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{card_h}" '
        f'viewBox="0 0 {CARD_W} {card_h}">\n'
        f'  <rect x="0.5" y="0.5" width="{CARD_W - 1}" height="{card_h - 1}" rx="10" ry="10"\n'
        f'        fill="{NEBULA}" stroke="{STAR_DUST}" stroke-width="1"/>\n'
        f'  <text x="{PAD_X}" y="42" fill="{ACCENT}" font-size="13" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{prompt}</text>\n'
        f'  <line x1="{PAD_X}" y1="54" x2="{CARD_W - PAD_X}" y2="54" '
        f'stroke="{STAR_DUST}" stroke-width="1"/>\n'
        f'  <svg x="{PAD_X}" y="{HEADER_H}" width="{inner_w}" height="{inner_h:.1f}" '
        f'viewBox="{view_box.group(1)}">\n'
        f"{body}\n"
        f"  </svg>\n"
        f"</svg>\n"
    )


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    src, dst = sys.argv[1], sys.argv[2]
    user = sys.argv[3] if len(sys.argv) > 3 else ""
    with open(src, encoding="utf-8") as f:
        out = frame(f.read(), user)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"card gerado: {dst} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
