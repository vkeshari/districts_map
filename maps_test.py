import matplotlib.pyplot as plt
from matplotlib import cm

from build_data import get_populations, get_age_groups, get_religions, get_education, get_languages
from draw_districts import show_map

import numpy as np

# Plots
fig = plt.figure(figsize=(19.2, 10.8), tight_layout=True)

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

# 0-5 population
map_ax = fig.add_subplot(232)
cmap = cm.get_cmap('PuBu')

map_data = {}
for d in populations:
  map_data[d] = age_groups[d][0]['total'] / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by % population < 5 years old")

# {Religion} population
religion = 'hindu'
map_ax = fig.add_subplot(233)
cmap = cm.get_cmap('YlOrRd')

map_data = {}
for d in populations:
  map_data[d] = religions[d][religion] / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by % " + religion + " population")

# Graduates
map_ax = fig.add_subplot(234)
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

# Age > {Age Limit}
age_limit = 60
map_ax = fig.add_subplot(235)
cmap = cm.get_cmap('BuGn')

map_data = {}
for d in populations:
  age_groups_sum = 0
  for age in age_groups[d]:
    if age < age_limit:
      continue
    age_groups_sum += age_groups[d][age]['total']
  map_data[d] = age_groups_sum / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by % population > " + str(age_limit) + " yrs old")

# {Language} Speakers
language = 'hindi'
map_ax = fig.add_subplot(236)
cmap = cm.get_cmap('Wistia')

map_data = {}
for d in populations:
  map_data[d] = languages[d][language] / populations[d]['population']

show_map(map_ax, map_data, cmap, "Districts of India by % with mother tounge " + language)

plt.show()

