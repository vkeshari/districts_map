import matplotlib.pyplot as plt
from matplotlib import cm

from build_data import get_district_info, get_populations, get_age_groups, get_religions, get_education, get_languages
from draw_districts import show_map

import numpy as np

# Plots
fig = plt.figure(figsize=(19.2, 10.8), tight_layout=True)

districts = get_district_info()
populations = get_populations()
age_groups = get_age_groups()
religions = get_religions()
education = get_education()
languages = get_languages()

# Literacy
map_ax = fig.add_subplot(231)
cmap = cm.get_cmap('YlGn')

map_data = {}
for d in populations:
  map_data[d] = populations[d]['literates'] / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by Literacy Rate")

# Population Density
map_ax = fig.add_subplot(232)
cmap = cm.get_cmap('pink').reversed()

map_data = {}
for d in populations:
  map_data[d] = populations[d]['population'] / districts[d]['area']

show_map(map_ax, map_data, cmap, "Districts of India by Population / sq km", is_percent_data = False, log_scale = True)

# {Religion} population
religion = 'muslim'
map_ax = fig.add_subplot(233)
cmap = cm.get_cmap('YlOrRd')

map_data = {}
for d in populations:
  map_data[d] = religions[d][religion] / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by % " + religion + " population", log_scale = True)

# Graduates
map_ax = fig.add_subplot(234)
cmap = cm.get_cmap('PuBu')

map_data = {}
for d in populations:
  twenty_plus_pop = 0
  for age in age_groups[d]:
    if age < 20:
      continue
    twenty_plus_pop += age_groups[d][age]['total']
  map_data[d] = education[d]['graduate'] / twenty_plus_pop

show_map(map_ax, map_data, cmap, "Districts of India by % Graduate Adults", log_scale = True)

# Uninhabited Villages
map_ax = fig.add_subplot(235)
cmap = cm.get_cmap('BuGn')

map_data = {}
for d in districts:
  total_villages = districts[d]['villages_uninhabited'] + districts[d]['villages_inhabited']
  if total_villages == 0:
    map_data[d] = 0
  else:
    map_data[d] = districts[d]['villages_uninhabited'] / total_villages

show_map(map_ax, map_data, cmap, "Districts of India by % uninhabited villages", log_scale = True)

# {Language} Speakers
language = 'hindi'
map_ax = fig.add_subplot(236)
cmap = cm.get_cmap('gist_earth').reversed()

map_data = {}
for d in populations:
  map_data[d] = languages[d][language] / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by % with mother tongue " + language, log_scale = True)

plt.show()

