"""
G-code exporter.
Converts toolpath segments (lists of (x, y) points) into G-code moves.

Coordinate unit assumption: mm.
"""
def _header(feed_rate: int) -> list[str]:
    return [
        "G21       ; units: mm",
        "G90       ; absolute positioning",
        f"F{feed_rate} ; feed rate mm/min",
        "G0 Z5.0   ; lift pen/tool",
    ]


def _footer() -> list[str]:
    return [
        "G0 Z5.0   ; lift at end",
        "G0 X0 Y0  ; return to origin",
        "M2        ; end program",
    ]


def paths_to_gcode(
    all_paths: list[list[list[tuple]]],
    labels: list[str] | None = None,
    z_down: float = 0.0,
    z_up: float = 5.0,
    feed_rate: int = 1200,
) -> str:
    """
    Parameters
    ----------
    all_paths : list of region path groups.
                Each element is a list of polylines (list of (x,y) tuples).
    labels    : optional region names written as G-code comments.
    z_down    : Z height when drawing.
    z_up      : Z height when travelling.
    """
    lines = _header(feed_rate)

    for region_idx, paths in enumerate(all_paths):
        label = labels[region_idx] if labels and region_idx < len(labels) else f"region_{region_idx}"
        lines.append(f"\n; ── {label} ──")

        for path in paths:
            if len(path) < 2:
                continue
            x0, y0 = path[0]
            lines.append(f"G0 Z{z_up:.3f}")
            lines.append(f"G0 X{x0:.4f} Y{y0:.4f}")
            lines.append(f"G1 Z{z_down:.3f}")
            for x, y in path[1:]:
                lines.append(f"G1 X{x:.4f} Y{y:.4f}")

    lines += _footer()
    return "\n".join(lines)


def save_gcode(gcode: str, filepath: str) -> None:
    with open(filepath, "w") as file:
        file.write(gcode)
    print(f"G-code saved → {filepath}")