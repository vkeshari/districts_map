from matplotlib import pyplot as plt
from matplotlib import cm, colors
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.ticker import Formatter, FuncFormatter

from get_basemap import get_basemap_and_district_info

import math
import numpy as np

VERY_SMALL = 0.0001

def replace_zeroes(data):
  out_data = {}
  for d in data:
    if data[d] > VERY_SMALL:
      out_data[d] = data[d]
    else:
      out_data[d] = VERY_SMALL

  return out_data

def show_map(map_ax, map_data, cmap, title, is_percent_data = True, log_scale = False):
  map_ax.set_title(title)
  _, districts = get_basemap_and_district_info(show_background_map = False)

  map_data = replace_zeroes(map_data)

  min_val = min(map_data.values())
  max_val = max(map_data.values())
  if log_scale:
    norm = colors.SymLogNorm(vmin = min_val, vmax = max_val, linthresh = VERY_SMALL, base = 10)
    ticks = np.logspace(math.log(min_val, 10), math.log(max_val, 10), num = 10)
  else:
    norm = colors.Normalize(vmin = min_val, vmax = max_val)
    ticks = np.linspace(min_val, max_val, num = 10)

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
  plt.colorbar(cm.ScalarMappable(cmap=cmap, norm = norm), ticks = ticks, format = formatter, shrink = 0.9)

