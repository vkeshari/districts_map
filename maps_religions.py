import matplotlib.pyplot as plt
from matplotlib import cm

from build_data import get_district_info, get_populations, get_religions
from draw_districts import show_map

def map_religions(log_scale):
  all_religions = religions[1].keys()
  for religion in all_religions:
    fig = plt.figure(figsize=(10.8, 10.8), tight_layout=True)
    map_ax = fig.add_subplot(111)
    cmap = cm.get_cmap('gist_earth').reversed()

    map_data = {}
    for d in districts:
      map_data[d] = religions[d][religion] / populations[d]['population']

    title = "Districts of India by % Population with Religion: " + religion.title()
    show_map(map_ax, map_data, cmap, title, log_scale = log_scale, big_text = True)

    file_name = 'output/religion/'
    if log_scale:
      file_name += 'log_'
    file_name += 'religion_' + religion + '.png'
    plt.savefig(file_name)

    plt.close(fig)
    print (file_name)

def map_popular_religions():
  popular_religions = {}
  for d in districts:
    max_val = 0
    max_religion = ''
    for r in religions[d]:
      pop = religions[d][r]
      if pop > max_val:
        max_val = pop
        max_religion = r
    popular_religions[d] = max_religion

  fig = plt.figure(figsize=(10.8, 10.8), tight_layout=True)
  map_ax = fig.add_subplot(111)
  cmap = cm.get_cmap('nipy_spectral', len(set(popular_religions.values())))

  map_data = popular_religions
  title = "Districts of India by Most popular Religion"
  show_map(map_ax, map_data, cmap, title, is_percent_data = False, log_scale = False, big_text = True, big_legend_text = True, is_categorical = True)

  file_name = 'output/religion/'
  file_name += 'popular_religions_map.png'
  plt.savefig(file_name)

  plt.close(fig)
  print (file_name)

districts = get_district_info()
populations = get_populations()
religions = get_religions()

# Plots
# map_religions(log_scale = False)
# map_religions(log_scale = True)

map_popular_religions()
