import math
import pyclipper

from utils.clipper_helpers import (
   pc, 
   _ensure_paths,
   _scale_from_clipper,
   _scale_to_clipper,
)

def rotate_poly_points(pt: int, angle_radians: int, origin=(0,0)) -> int:
  """Rotate a single 2D point about an origin by a given angle.

  Args:
      pt: The point to rotate as an (x, y) tuple.
      angle_radians: Rotation angle in radians (counter-clockwise positive).
      origin: The centre of rotation as an (x, y) tuple. Defaults to (0, 0).

  Returns:
      The rotated point as an (x, y) tuple.
  """
  x, y = pt
  ox, oy = origin
  dx, dy = x - ox, y - oy
  c, s = math.cos(angle_radians), math.sin(angle_radians)
  return (ox + dx * c - dy * s, oy + dx * s + dy * c)

def rotate_poly_paths(paths: list, angle_radians: int, origin=(0,0)) -> list:
  """Rotate every point in a list of polylines about an origin.

  Applies ``rotate_poly_points`` to each point in each polyline.

  Args:
      paths: A list of polylines, where each polyline is a list of
          (x, y) tuples.
      angle_radians: Rotation angle in radians (counter-clockwise positive).
      origin: The centre of rotation as an (x, y) tuple. Defaults to (0, 0).

  Returns:
      A new list of polylines with all points rotated by the given angle.
  """
  return [[rotate_poly_points(p, angle_radians, origin) for p in path] for path in paths]

def compute_path_bounding_box(paths: list) -> tuple:
  """Compute the axis-aligned bounding box of a collection of polylines.

  Args:
      paths: A list of polylines, where each polyline is a list of
          (x, y) tuples.

  Returns:
      A tuple (xmin, xmax, ymin, ymax) of the bounding box extents.
  """
  xs, ys = [], []

  for path in paths:
    for x,y in path:
        xs.append(x)
        ys.append(y)
    
  return min(xs), max(xs), min(ys), max(ys)

def generate_linear_hatch_pattern(polygon: list, spacing: float, angle_degrees: float = 0.0) -> list:
  """Generate a linear hatch fill pattern clipped to a polygon.

  Produces parallel lines at the given spacing and angle, then clips them
  to the interior of the polygon. Internally, the polygon is rotated so
  that horizontal lines can be generated before rotating everything back.

  Args:
      polygon: The clipping polygon as a list of [x, y] vertices, or a
          list of such polygons.
      spacing: Perpendicular distance between adjacent hatch lines in mm.
          Must be greater than 0.
      angle_degrees: Angle of the hatch lines in degrees, measured
          counter-clockwise from the horizontal. Defaults to 0.0
          (horizontal lines).

  Returns:
      A list of clipped polylines (each a list of (x, y) tuples)
      representing the hatch pattern inside the polygon.

  Raises:
      ValueError: If ``spacing`` is less than or equal to 0.
  """
  if spacing <= 0:
    raise ValueError("The spacing value for the linear hatch pattern must be greater than 0.")

  clip_paths = _ensure_paths(polygon)
  if not clip_paths:
    return []
  
  theta = math.radians(angle_degrees)

  rotated_paths = rotate_poly_paths(clip_paths, -theta)

  xmin, xmax, ymin, ymax = compute_path_bounding_box(rotated_paths)
  
  margin = spacing * 2
  y = ymin - margin 
  hatch_lines = []

  while y <= ymax + margin:
    hatch_lines.append([
        (xmin - margin, y),
        (xmax + margin, y)
    ])
    y += spacing

  hatch_lines = rotate_poly_paths(hatch_lines, theta)

  pc.Clear()
  pc.AddPaths(_scale_to_clipper(hatch_lines), pyclipper.PT_SUBJECT, False)
  pc.AddPaths(_scale_to_clipper(clip_paths), pyclipper.PT_CLIP, True)
  solution = pc.Execute2(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
  open_paths = pyclipper.OpenPathsFromPolyTree(solution)
  return _scale_from_clipper(open_paths)

def generate_spiral_pattern(polygon: list, a: float = 0.0, b: float = 0.1,
                    max_turns: float = 20, points_per_turn: int = 200) -> list:
    """Generate an Archimedean spiral fill pattern clipped to a polygon.

    The spiral follows r = a + b * θ, centred on the polygon's bounding box,
    and is clipped to the polygon interior.

    Args:
        polygon: The clipping polygon as a list of [x, y] vertices, or a
            list of such polygons.
        a: Starting radius offset in mm. Defaults to 0.0.
        b: Radial gap per radian in mm (controls line density). Defaults to 0.1.
        max_turns: Maximum number of full revolutions before the spiral is
            cut off. Defaults to 20.
        points_per_turn: Number of line segments per full revolution. Higher
            values yield a smoother curve. Defaults to 200.

    Returns:
        A list of clipped polylines (each a list of (x, y) tuples)
        representing the spiral inside the polygon.
    """
    clip_paths = _ensure_paths(polygon)
    if not clip_paths:
        return []

    xmin, xmax, ymin, ymax = compute_path_bounding_box(clip_paths)
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    max_r = math.sqrt((xmax - xmin) ** 2 + (ymax - ymin) ** 2)

    total_steps = int(max_turns * points_per_turn)
    d_theta = (2 * math.pi * max_turns) / total_steps

    spiral_pts = []
    theta = 0.0
    for _ in range(total_steps + 1):
        r = a + b * theta
        if r > max_r:
            break
        spiral_pts.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
        theta += d_theta

    if len(spiral_pts) < 2:
        return []

    lines = [spiral_pts]

    pc.Clear()
    pc.AddPaths(_scale_to_clipper(lines), pyclipper.PT_SUBJECT, False)
    pc.AddPaths(_scale_to_clipper(clip_paths), pyclipper.PT_CLIP, True)
    solution = pc.Execute2(
        pyclipper.CT_INTERSECTION,
        pyclipper.PFT_NONZERO,
        pyclipper.PFT_NONZERO,
    )
    return _scale_from_clipper(pyclipper.OpenPathsFromPolyTree(solution))

def generate_honeycomb_pattern(polygon: list, cell_size: float) -> list:
    """Generate a hexagonal (honeycomb) fill pattern clipped to a polygon.

    Builds a hexagonal grid that covers the polygon's bounding box, then
    clips it to the polygon interior.

    Args:
        polygon: The clipping polygon as a list of [x, y] vertices, or a
            list of such polygons.
        cell_size: Side length of each hexagonal cell in mm. Controls the
            horizontal spacing (= cell_size) and row height
            (= cell_size * √3 / 2).

    Returns:
        A list of clipped polylines (each a list of (x, y) tuples)
        representing the honeycomb pattern inside the polygon.
    """
    clip_paths = _ensure_paths(polygon)
    if not clip_paths:
        return []

    xmin, xmax, ymin, ymax = compute_path_bounding_box(clip_paths)
    margin = cell_size * 2
    h = cell_size * math.sqrt(3) / 2   # row height
    lines = []

    row = 0
    y = ymin - margin
    while y <= ymax + margin:
        # Even rows start at xmin, odd rows offset by half cell_size
        offset = (cell_size / 2) if (row % 2 == 1) else 0.0
        x = xmin - margin + offset
        while x <= xmax + margin:
            # Vertical segment of each hex column
            lines.append([(x, y), (x, y + h)])
            # Diagonal connectors
            lines.append([(x, y + h), (x + cell_size / 2, y + 2 * h)])
            lines.append([(x, y), (x + cell_size / 2, y - h)])
            x += cell_size
        y += 2 * h
        row += 1

    pc.Clear()
    pc.AddPaths(_scale_to_clipper(lines), pyclipper.PT_SUBJECT, False)
    pc.AddPaths(_scale_to_clipper(clip_paths), pyclipper.PT_CLIP, True)
    solution = pc.Execute2(
        pyclipper.CT_INTERSECTION,
        pyclipper.PFT_NONZERO,
        pyclipper.PFT_NONZERO,
    )
    return _scale_from_clipper(pyclipper.OpenPathsFromPolyTree(solution))