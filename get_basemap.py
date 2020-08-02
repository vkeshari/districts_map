from mpl_toolkits import basemap

def get_basemap_and_district_info(show_background_map):
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

  return m, districts

