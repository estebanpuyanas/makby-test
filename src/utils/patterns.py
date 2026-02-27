import math
import pyclipper

from utils.clipper_helpers import (
   pc, 
   _ensure_paths,
   _scale_from_clipper,
   _scale_to_clipper,
)

"""
Since hatcg lines are "diagonal" parallel lines, its easiest if we rotate the polygon, 
draw horizontal lines, and rotate back.
"""
def rotate_poly_points(pt: int, angle_radians: int, origin=(0,0)) -> int:
  x, y = pt
  ox, oy = origin
  dx, dy = x - ox, y - oy
  c, s = math.cos(angle_radians), math.sin(angle_radians)
  return (ox + dx * c - dy * s, oy + dx * s + dy * c)

"""
Since a path is just a list of points, we use the function above to rotate each point in a path,
and then apply that to each path in a list of paths.
"""
def rotate_poly_paths(paths: list, angle_radians: int, origin=(0,0)) -> list:
  return [[rotate_poly_points(p, angle_radians, origin) for p in path] for path in paths]

"""
The filling of a pattern must be done within the area of the polygon, 
for that we can just compute the intersection of the pattern with the polygon, and then visualize the result.
"""
def compute_path_bounding_box(paths: list)-> tuple:
  xs, ys = [], []

  for path in paths:
    for x,y in path:
        xs.append(x)
        ys.append(y)
    
  return min(xs), max(xs), min(ys), max(ys)

def generate_linear_hatch_pattern(polygon: list, spacing: float, angle_degrees: float = 0.0) -> list:
  
  # Make sure that there is some (even if minimal) spacing between the lines:

  if spacing <= 0:
    raise ValueError("The spacing value for the linear hatch pattern must be greater than 0.")
  
  """
  Normalize to a list of paths so errors with the AddPaths() function are avoided.
  """
  clip_paths = _ensure_paths(polygon)
  if not clip_paths:
    return []
  
  theta = math.radians(angle_degrees)

  rotated_paths = rotate_poly_paths(clip_paths, -theta)

  xmin, xmax, ymin, ymax = compute_path_bounding_box(rotated_paths)
  
  """
  Generate horizontal lines at the specified spacing.
  """
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
    """
    r = a + b*θ  clipped to polygon.
    a : starting radius offset
    b : radial gap per radian
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
    """
    Hexagonal grid clipped to polygon.
    Horizontal spacing  = cell_size
    Vertical spacing    = cell_size * sqrt(3) / 2
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