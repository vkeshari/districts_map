from get_basemap import get_basemap_and_district_info

def parse_district_info(districts_info, out_filename):
  district_info_file = open(out_filename, 'w')
  district_info_file.write('district_id,' +
                           'name,state_id,state' + '\n')
  
  districts = set()
  for d in districts_info:
    dist_id = d['censuscode']
    if dist_id == 0:
      continue

    if dist_id not in districts:
      district_info_file.write(str(dist_id) + ',' +
                               str(d['DISTRICT']) + ',' + str(d['ST_CEN_CD']) + ',' + str(d['ST_NM']) + '\n')
    districts.add(dist_id)

  district_info_file.close()

def parse_population_data(district_keys, out_filename):
  # Population Data
  population_raw_file = open('data/raw_data/district_populations.csv', 'r')

  populations_file = open(out_filename, 'w')
  populations_file.write('district_id,' +
                         'population,males,females,' +
                         'literates,literate_males,literate_females,' +
                         'working,working_males,working_females,' + 
                         'non_working,non_working_males,non_working_females' + '\n')

  all_district_ids = set([])
  for l in population_raw_file.readlines()[1:]:
    parts = l.split(',')
    if not parts[8] == 'Total':
      continue

    dist_id_string = parts[1].lstrip('0')
    if len(dist_id_string) == 0:
      continue
    dist_id = eval(dist_id_string)
    all_district_ids.add(dist_id)

    populations_file.write(dist_id_string + ',' +
                           parts[10].strip() + ',' +  parts[11].strip() + ',' +  parts[12].strip() + ',' +
                           parts[22].strip() + ',' +  parts[23].strip() + ',' +  parts[24].strip() + ',' +
                           parts[28].strip() + ',' +  parts[29].strip() + ',' +  parts[30].strip() + ',' +
                           parts[-3].strip() + ',' +  parts[-2].strip() + ',' +  parts[-1].strip() + '\n')

  population_raw_file.close()

  for d in district_keys:
    assert d in all_district_ids, "Populations missing district: " + str(d)
  for d in all_district_ids:
    assert d in district_keys, "Populations extra district: " + str(d)

  populations_file.close()

m, districts = get_basemap_and_district_info(show_background_map = False)

# parse_district_info(m.districts_info, out_filename = 'data/districts.csv')

# parse_population_data(districts.keys(), out_filename = 'data/populations.csv')

