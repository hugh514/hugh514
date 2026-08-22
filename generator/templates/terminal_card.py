"""SVG template: terminal panel (850 wide, height follows content).

A prompt line plus its output on one dark surface. The prompt used to live in a
markdown inline-code chip while the text under it was plain markdown, so the
command and its own description sat on two different backgrounds and read as
unrelated. Putting both inside one panel makes the pair read as a terminal
session and keeps the page on a single palette.
"""

from generator.utils import esc, wrap_text

WIDTH = 850
PAD_X = 30
LINE_H = 21
PARA_GAP = 12
BODY_TOP = 84
BOTTOM_PAD = 26
WRAP_CHARS = 88


def _paragraphs(body: str) -> list:
    """Split on blank lines, collapsing internal newlines into spaces."""
    blocks = [b.strip() for b in body.replace("\r\n", "\n").split("\n\n")]
    return [" ".join(b.split()) for b in blocks if b.strip()]


def render(prompt: str, body: str, theme: dict, username: str = "") -> str:
    """Render a terminal panel.

    Args:
        prompt: the command shown after the shell prompt, e.g. "whoami"
        body: output text; blank lines separate paragraphs
        theme: colour palette dict
        username: prefix for the prompt, e.g. "hugh514"
    """
    accent = theme["synapse_cyan"]
    dim = theme["text_dim"]
    bright = theme["text_bright"]
    rule = theme["star_dust"]

    handle = f"{username}@github" if username else "github"
    prompt_line = f"{handle}:~$ {prompt}"

    lines = []
    y = BODY_TOP
    for p_index, para in enumerate(_paragraphs(body)):
        # First paragraph is the identity line and gets the brighter fill.
        fill = bright if p_index == 0 else dim
        for line in wrap_text(para, WRAP_CHARS) or [""]:
            lines.append(
                f'  <text x="{PAD_X}" y="{y}" fill="{fill}" font-size="12.5" '
                f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{esc(line)}</text>'
            )
            y += LINE_H
        y += PARA_GAP

    height = y - PARA_GAP + BOTTOM_PAD
    lines_str = "\n".join(lines)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10" ry="10"
        fill="{theme['nebula']}" stroke="{rule}" stroke-width="1"/>

  <text x="{PAD_X}" y="42" fill="{accent}" font-size="13" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{esc(prompt_line)}</text>
  <line x1="{PAD_X}" y1="54" x2="{WIDTH - PAD_X}" y2="54" stroke="{rule}" stroke-width="1"/>

{lines_str}
</svg>'''
