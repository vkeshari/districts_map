import matplotlib.pyplot as plt
from matplotlib import cm

from build_data import get_district_info, get_populations, get_languages
from draw_districts import show_map

districts = get_district_info()
populations = get_populations()
languages = get_languages()

# Plots
for log_scale in [True, False]:
  all_languages = languages[1].keys()
  for language in all_languages:
    fig = plt.figure(figsize=(10.8, 10.8), tight_layout=True)
    map_ax = fig.add_subplot(111)
    cmap = cm.get_cmap('gist_earth').reversed()

    map_data = {}
    for d in districts:
      map_data[d] = languages[d][language] / populations[d]['population']

    title = "Districts of India by % Population with Mother Tongue: " + language.title()
    show_map(map_ax, map_data, cmap, title, log_scale = log_scale, big_text = True)

    file_name = 'output/language/'
    if log_scale:
      file_name += 'log_'
    file_name += 'language_' + language + '.png'
    plt.savefig(file_name)

    plt.close(fig)
    print(file_name)

