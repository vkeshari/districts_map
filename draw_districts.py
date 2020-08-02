import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib import cm

from get_basemap import get_basemap_and_district_info
from build_data import get_populations

import numpy as np

# Plots
fig = plt.figure(figsize=(10.8, 10.8), tight_layout=True)

_, districts = get_basemap_and_district_info(show_background_map = False)
populations = get_populations()

map_ax = fig.add_subplot(111)
map_ax.set_title("Districts of India by Literacy Rate")

cmap = cm.get_cmap('YlGn')
map_shapes = []
map_data = []
map_colors = []

for d in districts:
  for s in districts[d]['shapes']:
    map_shapes.append(Polygon(np.array(s), closed = True))

    data_to_plot = populations[d]['literates'] / populations[d]['population']
    map_data.append(data_to_plot)
    map_colors.append(cmap(data_to_plot))
        
map_ax.add_collection(PatchCollection(map_shapes, edgecolor='white', linewidths=0, facecolors = map_colors, zorder=2))

plt.show()

