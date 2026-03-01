import pyclipper

CLIPPER_SCALE = 1_000_000
pc = pyclipper.Pyclipper()

def _ensure_paths(polygon: list) -> list:
  """Normalize input into a list of paths (list of polylines).

  Accepts either a single flat polygon (list of [x, y] pairs) or an
  already-nested list of polylines and always returns the latter form,
  which is required by pyclipper's ``AddPaths``.

  Args:
      polygon: A single polygon (list of [x, y] vertices) or a list of
          such polygons.

  Returns:
      A list of polylines, each polyline being a list of [x, y] points.
      Returns an empty list if the input is empty.
  """
  if not polygon:
    return []
  
  if isinstance(polygon[0], (list, tuple)) and len(polygon[0]) == 2 and not isinstance(polygon[0][0], (list, tuple)):
    return [polygon]
  return polygon

def _scale_to_clipper(paths: list) -> list:
  """Scale floating-point paths to pyclipper's integer coordinate space.

  Multiplies every coordinate by ``CLIPPER_SCALE`` (1 000 000) to convert
  millimetre values to the integers that pyclipper requires.

  Args:
      paths: A list of polylines in floating-point millimetre coordinates.

  Returns:
      The same structure with all coordinates scaled to integers.
  """
  return pyclipper.scale_to_clipper(paths, CLIPPER_SCALE)

def _scale_from_clipper(paths: list) -> list:
  """Scale pyclipper integer paths back to floating-point coordinates.

  Divides every coordinate by ``CLIPPER_SCALE`` (1 000 000), reversing
  the transformation applied by ``_scale_to_clipper``.

  Args:
      paths: A list of polylines in pyclipper integer coordinates.

  Returns:
      The same structure with all coordinates converted back to
      floating-point millimetre values.
  """
  return pyclipper.scale_from_clipper(paths, CLIPPER_SCALE)

def _run(open_paths: list, clip_paths: list, op, subject_closed: bool = False) -> list:
  """Execute a pyclipper boolean operation on open subject paths.

  Scales the inputs to clipper space, runs the requested operation, and
  returns the clipped open paths scaled back to millimetre coordinates.

  Args:
      open_paths: Subject polylines (open paths) to be clipped.
      clip_paths: Closed polygon(s) used as the clip region.
      op: A pyclipper clip-type constant (e.g. ``pyclipper.CT_INTERSECTION``).
      subject_closed: Whether to treat the subject paths as closed polygons.
          Defaults to ``False`` (open polylines).

  Returns:
      A list of clipped open polylines in floating-point millimetre coordinates.
  """
  pc.Clear()
  pc.AddPaths(_scale_to_clipper(open_paths), pyclipper.PT_SUBJECT, subject_closed)
  pc.AddPaths(_scale_to_clipper(clip_paths), pyclipper.PT_CLIP, True)
  solution = pc.Execute2(op, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
  
  return _scale_from_clipper(pyclipper.OpenPathsFromPolyTree(solution))