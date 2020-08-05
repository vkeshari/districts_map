from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.ticker import Formatter, FuncFormatter

from get_basemap import get_basemap_and_district_info

import numpy as np

def show_map(map_ax, map_data, cmap, title, is_percent_data = True):
  map_ax.set_title(title)
  _, districts = get_basemap_and_district_info(show_background_map = False)

  min_val = min(map_data.values())
  max_val = max(map_data.values())
  norm = plt.Normalize(min_val, max_val)

  map_shapes = []
  map_colors = []
  for d in map_data:
    for s in districts[d]['shapes']:
      map_shapes.append(Polygon(np.array(s), closed = True))
      map_colors.append(cmap(norm(map_data[d])))
        
  patch_collection = PatchCollection(map_shapes, edgecolor = 'white', linewidths = 0, facecolors = map_colors, zorder = 2)
  map_ax.add_collection(patch_collection)

  if not is_percent_data:
    formatter = FuncFormatter(lambda x, _ : '{val:.2f}'.format(val = x))
  else:
    formatter = FuncFormatter(lambda x, _ : '{percent:.2f} %'.format(percent = 100*x))
  ticks = np.linspace(min_val, max_val, num = 10)
  plt.colorbar(cm.ScalarMappable(cmap=cmap, norm = norm), ticks = ticks, format = formatter, shrink = 0.9)

