import math
import pyclipper

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