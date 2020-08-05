from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from get_basemap import get_basemap_and_district_info

import numpy as np

def normalize_range(district_data):
  min_value = min(district_data.values())
  max_value = max(district_data.values())
  diff = max_value - min_value
  return { dist: (val - min_value) / diff for (dist, val) in district_data.items() }

def show_map(map_ax, map_data, cmap, title):
  map_ax.set_title(title)
  _, districts = get_basemap_and_district_info(show_background_map = False)

  map_shapes = []
  map_colors = []
  for d in map_data:
    for s in districts[d]['shapes']:
      map_shapes.append(Polygon(np.array(s), closed = True))
      map_colors.append(cmap(map_data[d]))
        
  map_ax.add_collection(PatchCollection(map_shapes, edgecolor='white', linewidths=0, facecolors = map_colors, zorder=2))

