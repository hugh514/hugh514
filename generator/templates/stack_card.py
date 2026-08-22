"""SVG template: stack card (850 wide, height follows content).

Replaces the markdown table that used to hold the stack. A markdown table
renders in GitHub's own theme, with light borders and cell backgrounds, so it
read as a foreign block sitting between the dark SVG cards. Rendering the same
rows as SVG keeps the page on one palette.
"""

from generator.utils import esc, wrap_text

WIDTH = 850
PAD_X = 30
LABEL_X = PAD_X
VALUE_X = 168
HEADER_H = 74
LINE_H = 21
ROW_GAP = 13
BOTTOM_PAD = 24
# Monospace at 12px sits near 7.05px per glyph; 86 keeps the longest row inside
# the card with margin to spare.
WRAP_CHARS = 86


def render(stack: list, theme: dict, username: str = "") -> str:
    """Render the stack card.

    Args:
        stack: list of {"label": str, "items": str}
        theme: colour palette dict
        username: shown in the prompt-style header
    """
    accent = theme["synapse_cyan"]
    dim = theme["text_dim"]
    faint = theme["text_faint"]
    bright = theme["text_bright"]
    rule = theme["star_dust"]

    handle = username or "github"
    prompt = f"{handle}@github:~$ cat stack.txt"

    rows = []
    y = HEADER_H
    first = True
    for entry in stack:
        label = entry.get("label", "")
        lines = wrap_text(entry.get("items", ""), WRAP_CHARS) or [""]

        if not first:
            rows.append(
                f'  <line x1="{PAD_X}" y1="{y - ROW_GAP + 2}" x2="{WIDTH - PAD_X}" '
                f'y2="{y - ROW_GAP + 2}" stroke="{rule}" stroke-width="1" opacity="0.45"/>'
            )
        first = False

        rows.append(
            f'  <text x="{LABEL_X}" y="{y}" fill="{faint}" font-size="12" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
            f'letter-spacing="0.5">{esc(label)}</text>'
        )
        for i, line in enumerate(lines):
            fill = bright if i == 0 else dim
            rows.append(
                f'  <text x="{VALUE_X}" y="{y + i * LINE_H}" fill="{fill}" font-size="12" '
                f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{esc(line)}</text>'
            )

        y += len(lines) * LINE_H + ROW_GAP

    height = y - ROW_GAP + BOTTOM_PAD
    rows_str = "\n".join(rows)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10" ry="10"
        fill="{theme['nebula']}" stroke="{rule}" stroke-width="1"/>

  <text x="{PAD_X}" y="42" fill="{accent}" font-size="13" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{esc(prompt)}</text>
  <line x1="{PAD_X}" y1="54" x2="{WIDTH - PAD_X}" y2="54" stroke="{rule}" stroke-width="1"/>

{rows_str}
</svg>'''
