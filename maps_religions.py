import matplotlib.pyplot as plt
from matplotlib import cm

from build_data import get_district_info, get_populations, get_religions
from draw_districts import show_map

districts = get_district_info()
populations = get_populations()
religions = get_religions()

# Plots
for log_scale in [True, False]:
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

