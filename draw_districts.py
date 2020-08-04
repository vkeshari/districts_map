import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib import cm

from get_basemap import get_basemap_and_district_info
from build_data import get_populations, get_age_groups

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
  for d in populations:
    for s in districts[d]['shapes']:
      map_shapes.append(Polygon(np.array(s), closed = True))
      map_colors.append(cmap(map_data[d]))
        
  map_ax.add_collection(PatchCollection(map_shapes, edgecolor='white', linewidths=0, facecolors = map_colors, zorder=2))

# Plots
fig = plt.figure(figsize=(19.2, 10.8), tight_layout=True)

populations = get_populations()
age_groups = get_age_groups()

# Literacy
map_ax = fig.add_subplot(121)
cmap = cm.get_cmap('YlGn')

map_data = {}
for d in populations:
  map_data[d] = populations[d]['literates'] / populations[d]['population']
map_data = normalize_range(map_data)

show_map(map_ax, map_data, cmap, "Districts of India by Literacy Rate")

# 0-5 population
map_ax = fig.add_subplot(122)
cmap = cm.get_cmap('PuBu')

map_data = {}
for d in populations:
  map_data[d] = age_groups[d][0]['total'] / populations[d]['population']
map_data = normalize_range(map_data)

show_map(map_ax, map_data, cmap, "Districts of India by % population < 5 years old")

plt.show()

