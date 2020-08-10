from matplotlib import ticker

import numpy as np

def pretty_number(n):
  cr = n / 10000000
  lk = n / 100000
  th = n / 1000
  if cr >= 1.0:
    ns = "{:.2f}".format(cr) + ' crore'
  elif lk >= 1.0:
    ns = "{:.2f}".format(lk) + ' lakh'
  elif th >= 1.0:
    ns = "{:.2f}".format(th) + ' th'
  else:
    ns = str(n)
  return ns

def pretty_text(label, value):
  return label.title() + ' ' + '(' + pretty_number(value) + ')'

def get_text_size(big_text):
  if big_text:
    return 15
  else:
    return 10

def show_chart(chart_ax, chart_data, max_bars, cmap, title, big_text):
  chart_ax.set_title(title, fontsize = get_text_size(big_text))

  valkey = [(v, k) for k, v in chart_data.items()]
  ordered = sorted(valkey)
  top_ordered = ordered[-min(max_bars, len(ordered)):]

  top_values = [v for v, _ in top_ordered]
  top_labels = [pretty_text(k, v) for v, k in top_ordered]
  top_colors = [cmap(i) for i in np.linspace(0, 1, len(top_values))]

  chart_ax.spines['right'].set_color('none')
  chart_ax.spines['left'].set_color('none')
  chart_ax.spines['top'].set_color('none')
  chart_ax.spines['bottom'].set_color('none')
  chart_ax.xaxis.set_major_locator(ticker.NullLocator())
  chart_ax.yaxis.set_major_locator(ticker.NullLocator())
  chart_ax.xaxis.set_major_formatter(ticker.NullFormatter())
  chart_ax.xaxis.set_major_formatter(ticker.NullFormatter())
  
  chart_ax.barh(top_labels, top_values, alpha = 0.5, color = top_colors)
  for l in top_labels:
    chart_ax.annotate(l, xy=(0.1, l), va = 'center', size = get_text_size(big_text))

