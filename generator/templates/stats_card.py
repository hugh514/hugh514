"""SVG template: telemetry pane in neofetch style (850x230).

Left pane holds a fixed star chart, right pane holds key/value rows with
dotted leaders. Monospace throughout, one accent colour for values. No blur
filters and no nested <svg> icons: both broke on GitHub's image pipeline and
made the digits collide with their own icons.
"""

from generator.utils import METRIC_LABELS, esc, format_number

WIDTH, HEIGHT = 850, 230

# Fixed chart so consecutive runs produce an identical file.
# (x, y) offsets from the pane centre, plus radius.
STARS = [
    (-52, -46, 1.3), (-18, -62, 1.0), (24, -50, 1.7), (56, -22, 1.1),
    (-64, -8, 1.0), (-30, -20, 2.4), (6, -14, 1.2), (44, 8, 1.4),
    (-56, 26, 1.1), (-20, 16, 1.6), (14, 32, 1.0), (52, 40, 1.2),
    (-38, 52, 1.3), (0, 58, 1.0), (34, 62, 1.5),
]
# Indices into STARS, joined to form the constellation.
EDGES = [(1, 5), (5, 2), (5, 6), (6, 7), (5, 9), (9, 4), (9, 10), (10, 13), (13, 12), (10, 14)]

LABEL_X = 232
VALUE_X = WIDTH - 30
ROW_TOP = 92
ROW_STEP = 25


def _rows(stats, metrics, languages, galaxy_arms, max_langs=3):
    """Build the (label, value) rows, longest-lived data first."""
    rows = []
    for key in metrics:
        rows.append((METRIC_LABELS.get(key, key.title()), format_number(stats.get(key, 0))))

    if languages:
        top = sorted(languages.items(), key=lambda kv: kv[1], reverse=True)[:max_langs]
        if top:
            rows.append(("Languages", ", ".join(name for name, _ in top)))

    if galaxy_arms:
        rows.append(("Focus", ", ".join(arm["name"] for arm in galaxy_arms)))

    return rows


def render(stats: dict, metrics: list, theme: dict, username: str = "",
           languages: dict | None = None, galaxy_arms: list | None = None) -> str:
    """Render the telemetry pane.

    Args:
        stats: dict with keys like commits, stars, prs, repos
        metrics: metric keys to display, in order
        theme: colour palette dict
        username: shown as `username@github` in the pane header
        languages: {language: bytes}, used for the Languages row
        galaxy_arms: arm configs, used for the Focus row
    """
    accent = theme["synapse_cyan"]
    dim = theme["text_dim"]
    faint = theme["text_faint"]
    bright = theme["text_bright"]
    rule = theme["star_dust"]

    handle = f"{username}@github:~$ ./telemetry" if username else "github:~$ ./telemetry"

    # Left pane: star chart centred in its own column.
    cx, cy = 116, 138
    chart = []
    for a, b in EDGES:
        x1, y1, _ = STARS[a]
        x2, y2, _ = STARS[b]
        chart.append(
            f'    <line x1="{cx + x1}" y1="{cy + y1}" x2="{cx + x2}" y2="{cy + y2}" '
            f'stroke="{accent}" stroke-width="0.6" opacity="0.28"/>'
        )
    for i, (dx, dy, r) in enumerate(STARS):
        colour = accent if r >= 1.5 else faint
        chart.append(
            f'    <circle class="star s{i % 3}" cx="{cx + dx}" cy="{cy + dy}" r="{r}" '
            f'fill="{colour}"/>'
        )
    chart_str = "\n".join(chart)

    # Right pane: label, dotted leader, value.
    rows = _rows(stats, metrics, languages or {}, galaxy_arms or [])
    row_svg = []
    for i, (label, value) in enumerate(rows):
        y = ROW_TOP + i * ROW_STEP
        numeric = value.replace(".", "").replace("k", "").isdigit()
        value_fill = accent if numeric else bright
        # Leader runs from just after the label to just before the value.
        leader_start = LABEL_X + len(label) * 7.4 + 10
        leader_end = VALUE_X - len(value) * 7.4 - 10
        leader = ""
        if leader_end - leader_start > 12:
            leader = (
                f'\n      <line x1="{leader_start:.0f}" y1="{y - 4}" x2="{leader_end:.0f}" y2="{y - 4}" '
                f'stroke="{rule}" stroke-width="1" stroke-dasharray="1 5"/>'
            )
        row_svg.append(
            f'''    <g>
      <text x="{LABEL_X}" y="{y}" fill="{dim}" font-size="13" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{esc(label)}</text>{leader}
      <text x="{VALUE_X}" y="{y}" text-anchor="end" fill="{value_fill}" font-size="13" font-weight="500" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{esc(value)}</text>
    </g>'''
        )
    rows_str = "\n".join(row_svg)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <style>
      .star {{ animation: twinkle 6s ease-in-out infinite; }}
      .s1 {{ animation-delay: 2s; }}
      .s2 {{ animation-delay: 4s; }}
      @keyframes twinkle {{
        0%, 100% {{ opacity: 0.45; }}
        50% {{ opacity: 1; }}
      }}
    </style>
  </defs>

  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="10" ry="10"
        fill="{theme['nebula']}" stroke="{rule}" stroke-width="1"/>

  <text x="30" y="42" fill="{accent}" font-size="13" font-family="ui-monospace, SFMono-Regular, Menlo, monospace">{esc(handle)}</text>
  <line x1="30" y1="54" x2="{WIDTH - 30}" y2="54" stroke="{rule}" stroke-width="1"/>

  <!-- star chart -->
{chart_str}

  <!-- divider between panes -->
  <line x1="204" y1="72" x2="204" y2="{HEIGHT - 26}" stroke="{rule}" stroke-width="1" opacity="0.6"/>

  <!-- key/value rows -->
{rows_str}
</svg>'''
