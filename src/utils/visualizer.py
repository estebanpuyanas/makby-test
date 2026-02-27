

import matplotlib.pyplot as plt
import numpy as np

"""
Args:
1. Polygons: Dictionary of polygons. The keys are polygon names and the values are lists of (x, y) tuples 
representing the vertices of the polygons.  
"""
def visualize_polygons(polygons_dict: dict, title="Exercise 1 polygon visualization") -> None:
  num_plots = len(polygons_dict)
  fig, axes = plt.subplots(1, num_plots, figsize=(5 * num_plots, 5))
  
  if num_plots == 1:
    axes = [axes]

  for idx, (name, polygons) in enumerate(polygons_dict.items()):
    ax = axes[idx]

    # Handle single polygon vs. list of polygons. 
    if polygons and not isinstance(polygons[0], (list, tuple)):
      polygons = [polygons]

    # Plot each polygon.
    for polygon in polygons:
      if polygon:
        poly_array = np.array(polygon + [polygon[0]])
        ax.plot(poly_array[:, 0], poly_array[:, 1], 'o-', linewidth=2)
        ax.fill(poly_array[:, 0], poly_array[:, 1], alpha=0.3)
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(name)

  plt.suptitle(title)
  #plt.tight_layout()
  plt.show()