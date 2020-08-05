import matplotlib.pyplot as plt
from matplotlib import cm

from build_data import get_populations, get_age_groups, get_religions, get_education
from draw_districts import show_map

import numpy as np

# Plots
fig = plt.figure(figsize=(10.8, 10.8), tight_layout=True)

populations = get_populations()
age_groups = get_age_groups()
religions = get_religions()
education = get_education()

# Literacy
map_ax = fig.add_subplot(221)
cmap = cm.get_cmap('YlGn')

map_data = {}
for d in populations:
  map_data[d] = populations[d]['literates'] / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by Literacy Rate")

# 0-5 population
map_ax = fig.add_subplot(222)
cmap = cm.get_cmap('PuBu')

map_data = {}
for d in populations:
  map_data[d] = age_groups[d][0]['total'] / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by % population < 5 years old")

# Hindu population
map_ax = fig.add_subplot(223)
cmap = cm.get_cmap('OrRd')

map_data = {}
for d in populations:
  map_data[d] = religions[d]['hindu'] / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by % Hindu population")

# Graduates
map_ax = fig.add_subplot(224)
cmap = cm.get_cmap('RdPu')

map_data = {}
for d in populations:
  twenty_plus_pop = 0
  for age in age_groups[d]:
    if age < 20:
      continue
    twenty_plus_pop += age_groups[d][age]['total']
  map_data[d] = education[d]['graduate'] / twenty_plus_pop

show_map(map_ax, map_data, cmap, "Districts of India by % Graduate Adults")

plt.show()

