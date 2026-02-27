import pyclipper

CLIPPER_SCALE = 1_000_000
pc = pyclipper.Pyclipper()

"""
This function allows us to handle single polygons and lists of polygons in a consistent way. 
If the input is a single polygon (a list of points), we wrap it in another list to create a list of polygons. 
If the input is already a list of polygons, we return it as is.
"""
def _ensure_paths(polygon: list) -> list:
  if not polygon:
    return []
  
  if isinstance(polygon[0], (list, tuple)) and len(polygon[0]) == 2 and not isinstance(polygon[0][0], (list, tuple)):
    return [polygon]
  return polygon

def _scale_to_clipper(paths: list)-> list:
  return pyclipper.scale_to_clipper(paths, CLIPPER_SCALE)

def _scale_from_clipper(paths: list)-> list:
  return pyclipper.scale_from_clipper(paths, CLIPPER_SCALE)

"""Clip open polylines (hatch/spiral lines) against a closed polygon."""
def _run(open_paths: list, clip_paths: list, op, subject_closed: bool = False) -> list:
  pc.Clear()
  pc.AddPaths(_scale_to_clipper(open_paths), pyclipper.PT_SUBJECT, subject_closed)
  pc.AddPaths(_scale_to_clipper(clip_paths), pyclipper.PT_CLIP, True)
  solution = pc.Execute2(op, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
  
  return _scale_from_clipper(pyclipper.OpenPathsFromPolyTree(solution))