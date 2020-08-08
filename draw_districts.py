from matplotlib import pyplot as plt
from matplotlib import cm, colors
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.ticker import Formatter, FuncFormatter, FixedFormatter

from get_basemap import get_basemap_and_district_info

import math
import numpy as np

def get_small_value(is_percent_data):
  if is_percent_data:
    return 0.0001
  else:
    return 0.01

def get_text_size(big_text):
  if big_text:
    return 15
  else:
    return 10

def get_shrink_factor(big_text):
  if big_text:
    return 0.8
  else:
    return 0.9

def replace_small_values(data, small_value):
  out_data = {}

  for d in data:
    if data[d] > small_value:
      out_data[d] = data[d]
    else:
      out_data[d] = small_value

  return out_data

def show_linear_map(map_ax, map_data, cmap, title, is_percent_data, log_scale, big_text, big_legend_text):
  map_ax.set_title(title, fontsize = get_text_size(big_text))

  _, districts = get_basemap_and_district_info(show_background_map = False)

  map_data = replace_small_values(map_data, get_small_value(is_percent_data))

  min_val = min(map_data.values())
  max_val = max(map_data.values())
  if log_scale:
    norm = colors.SymLogNorm(vmin = min_val, vmax = max_val, linthresh = get_small_value(is_percent_data), base = 10)
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
  cbar = plt.colorbar(cm.ScalarMappable(cmap=cmap, norm = norm), ticks = ticks, format = formatter, fraction = 0.1, shrink = get_shrink_factor(big_text))
  cbar.ax.tick_params(labelsize = get_text_size(big_legend_text))

  if log_scale:
    colorbar_title = 'Log Scale'
  else:
    colorbar_title = 'Scale'
  cbar.ax.set_title(colorbar_title, fontsize = get_text_size(big_text), pad = 20.0) 

def show_categorical_map(map_ax, map_data, cmap, title, big_text, big_legend_text):
  map_ax.set_title(title, fontsize = get_text_size(big_text))

  _, districts = get_basemap_and_district_info(show_background_map = False)

  distinct_values = sorted(set(map_data.values()))
  distinct_values.reverse()
  value_to_index = {}
  index_to_value = {}
  for i, v in enumerate(distinct_values):
    value_to_index[v] = i
    index_to_value[i] = v

  map_shapes = []
  map_colors = []
  alpha = 1
  for d in map_data:
    for s in districts[d]['shapes']:
      map_shapes.append(Polygon(np.array(s), closed = True))
      map_colors.append(cmap(value_to_index[map_data[d]]))
        
  patch_collection = PatchCollection(map_shapes, edgecolor = 'white', linewidths = 0, facecolors = map_colors, zorder = 2, alpha = alpha)
  map_ax.add_collection(patch_collection)

  tick_interval = 1 / len(distinct_values)
  ticks = [t + tick_interval / 2 for t in np.linspace(0, 1 - tick_interval, len(distinct_values))]
  formatter = FixedFormatter([v.title() for v in distinct_values])

  cbar = plt.colorbar(cm.ScalarMappable(cmap=cmap), ticks = ticks, format = formatter, fraction = 0.1, shrink = get_shrink_factor(big_text), alpha = alpha)
  cbar.ax.tick_params(labelsize = get_text_size(big_legend_text))
  cbar.ax.set_title('Legend', fontsize = get_text_size(big_text), pad = 20.0) 

def show_map(map_ax, map_data, cmap, title, is_percent_data = True, log_scale = False, big_text = False, big_legend_text = False, is_categorical = False):
  if is_categorical:
    if is_percent_data or log_scale:
      assert False, 'Categorical data cannot have percent or log data'
    show_categorical_map(map_ax, map_data, cmap, title, big_text, big_legend_text)
  else:
    show_linear_map(map_ax, map_data, cmap, title, is_percent_data, log_scale, big_text, big_legend_text)

