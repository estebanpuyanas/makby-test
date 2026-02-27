

CLIPPER_SCALE = 1_000_000

def _ensure_paths(polygon: list) -> list:

  # Base case: if the polygon is empty, return an empty list.
  if not polygon:
    return []
  
  """
  This function allows us to handle single polygons and lists of polygons in a consistent way. 
  If the input is a single polygon (a list of points), we wrap it in another list to create a list of polygons. 
  If the input is already a list of polygons, we return it as is.
  """
  if isinstance(polygon[0], (list, tuple)) and len(polygon[0]) == 2 and not isinstance(polygon[0][0], (list, tuple)):
    return [polygon]

  return polygon

def _scale_to_clipper(paths: list)-> list:
  return pyclipper.scale_to_clipper(paths, CLIPPER_SCALE)

def _scale_from_clipper(paths: list)-> list:
  return pyclipper.scale_from_clipper(paths, CLIPPER_SCALE)