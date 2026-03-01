"""
G-code exporter.
Converts toolpath segments (lists of (x, y) points) into G-code moves.

Coordinate unit assumption: mm.

NOTE: THIS FILE WAS ENTIRELY GENERATED USING AI. PLEASE REVIEW utils/README.md for a more detailed explenation.
"""

def _header(feed_rate: int) -> list[str]:
    """Generate the G-code preamble lines.

    Sets units to millimetres, switches to absolute positioning, configures
    the feed rate, and lifts the tool before any moves.

    Args:
        feed_rate: Tool travel speed in mm/min.

    Returns:
        A list of G-code command strings forming the file header.
    """
    return [
        "G21       ; units: mm",
        "G90       ; absolute positioning",
        f"F{feed_rate} ; feed rate mm/min",
        "G0 Z5.0   ; lift pen/tool",
    ]

def _footer() -> list[str]:
    """Generate the G-code closing lines.

    Lifts the tool, returns it to the origin, and sends the end-of-program
    command.

    Returns:
        A list of G-code command strings forming the file footer.
    """
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
    """Convert toolpath regions into a G-code program string.

    Iterates over every region and its constituent polylines, emitting a
    rapid move (G0) to each polyline's start followed by linear moves (G1)
    along the remaining points.

    Args:
        all_paths: Ordered list of region path groups. Each element is a
            list of polylines, where each polyline is a list of (x, y) tuples.
        labels: Optional region names written as G-code comments. If omitted,
            regions are labelled ``region_0``, ``region_1``, etc.
        z_down: Z height when the tool is drawing (pen down). Defaults to 0.0.
        z_up: Z height when the tool is travelling between paths. Defaults to 5.0.
        feed_rate: Tool travel speed in mm/min. Defaults to 1200.

    Returns:
        A single string containing the complete G-code program, with lines
        separated by newline characters.
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
    """Write a G-code string to a file on disk.

    Creates or overwrites the file at the given path with the provided
    G-code content and prints a confirmation message to stdout.

    Args:
        gcode: The complete G-code program string to write.
        filepath: Absolute or relative path of the output ``.gcode`` file.
    """
    with open(filepath, "w") as file:
        file.write(gcode)
    print(f"G-code saved → {filepath}")