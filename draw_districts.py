import matplotlib.pyplot as plt
from mpl_toolkits import basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib import cm

import numpy as np

def get_basemap_and_population_data(show_background_map):
  # Basemap
  m = basemap.Basemap(projection='aeqd', resolution='l',
                      lat_0=20, lon_0=80,
                      llcrnrlat=5, llcrnrlon=68, urcrnrlat=35, urcrnrlon=100)
  if show_background_map:
    m.drawlsmask(land_color='white', ocean_color='lightskyblue', zorder = 1);
  m.readshapefile('data/districts_2011/2011_Dist', 'districts', linewidth = 0, color = 'white', antialiased = True, zorder = 0)

  # Shape Data
  districts = {}
  for d, s in zip(m.districts_info, m.districts):
    dist_id = d['censuscode']
    if dist_id not in districts:
      districts[dist_id] = {}
      districts[dist_id]['name'] = d['DISTRICT']
      districts[dist_id]['state'] = d['ST_NM']
      districts[dist_id]['state_id'] = d['ST_CEN_CD']
      districts[dist_id]['shape_id'] = d['SHAPENUM']
      districts[dist_id]['shapes'] = []
    districts[dist_id]['shapes'].append(s)
  del(districts[0])

  # Population Data
  population_file = open('data/district_populations.csv', 'r')
  for l in population_file.readlines()[1:]:
    parts = l.split(',')
    if not parts[8] == 'Total':
      continue

    dist_id_string = parts[1].lstrip('0')
    if len(dist_id_string) == 0:
      continue
    dist_id = eval(dist_id_string)

    districts[dist_id]['population'] = eval(parts[10])
    districts[dist_id]['males'] = eval(parts[11])
    districts[dist_id]['females'] = eval(parts[12])
    districts[dist_id]['literates'] = eval(parts[22])

  population_file.close()

  return (m, districts)

# Plots
fig = plt.figure(figsize=(10.8, 10.8), tight_layout=True)

_, districts = get_basemap_and_population_data(show_background_map = True)

map_ax = fig.add_subplot(111)
map_ax.set_title("Districts of India by Literacy Rate")

cmap = cm.get_cmap('YlGn')
map_shapes = []
map_data = []
map_colors = []

for d in districts:
  for s in districts[d]['shapes']:
    map_shapes.append(Polygon(np.array(s), closed = True))

    data_to_plot = districts[d]['literates'] * 1.0 / districts[d]['population']
    map_data.append(data_to_plot)
    map_colors.append(cmap(data_to_plot))
        
map_ax.add_collection(PatchCollection(map_shapes, edgecolor='white', linewidths=0, facecolors = map_colors, zorder=2))

plt.show()

