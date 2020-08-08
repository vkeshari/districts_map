import os
import xlrd

from get_basemap import get_basemap_and_district_info

def check_districts_equal(base, built, label):
  missing_districts = set()
  extra_districts = set()
  for d in base:
    if d not in built:
      missing_districts.add(d)
  for d in built:
    if d not in base:
      extra_districts.add(d)

  print ("Check Districts for " + label)
  print ("Missing districts: " + str(missing_districts))
  print ("Extra districts: " + str(extra_districts))

def parse_district_id(raw_string):
    dist_id_string = raw_string.lstrip('0')
    if len(dist_id_string) == 0:
      return 0
    return eval(dist_id_string)

def parse_district_info(districts_info, out_filename):
  districts = {}

  sheet = xlrd.open_workbook('data/raw_data/A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA.xlsx').sheet_by_index(0)

  for row in range(4, sheet.nrows):
    if sheet.cell_type(row, 0) == 0:
      continue

    dist_id = parse_district_id(sheet.cell_value(row, 1))
    if dist_id == 0:
      continue
    if dist_id not in districts:
      districts[dist_id] = {}

    region_str = sheet.cell_value(row, 3).strip()
    type_str = sheet.cell_value(row, 5).strip()

    if not region_str == 'DISTRICT' or not type_str == 'Total':
      continue

    districts[dist_id]['villages_inhabited'] = int(sheet.cell_value(row, 6))
    districts[dist_id]['villages_uninhabited'] = int(sheet.cell_value(row, 7))
    districts[dist_id]['towns'] = int(sheet.cell_value(row, 8))
    districts[dist_id]['area'] = sheet.cell_value(row, 13)

  check_districts_equal([d['censuscode'] for d in districts_info if d['censuscode'] > 0], districts.keys(), 'District data')

  for d in districts_info:
    dist_id = d['censuscode']
    if dist_id == 0:
      continue

    districts[dist_id]['name'] = d['DISTRICT'].strip()
    districts[dist_id]['state_id'] = d['ST_CEN_CD']
    districts[dist_id]['state'] = d['ST_NM'].strip()

  district_info_file = open(out_filename, 'w')

  district_info_file.write('district_id,name,state_id,state,area,towns,villages_inhabited,villages_uninhabited' + '\n')
  for d in sorted(districts.keys()):
    district_info_file.write(str(d) + ',' + districts[d]['name'] + ',' +
                             str(districts[d]['state_id']) + ',' + districts[d]['state'] + ',' +
                             str('{area:.2f}'.format(area = districts[d]['area'])) + ',' + str(districts[d]['towns']) + ',' +
                             str(districts[d]['villages_inhabited']) + ',' + str(districts[d]['villages_uninhabited']) + '\n')
  
  district_info_file.close()

def parse_population_data(district_keys, out_filename):
  sheet = xlrd.open_workbook('data/raw_data/DDW_PCA0000_2011_Indiastatedist.xlsx').sheet_by_index(0)

  populations_file = open(out_filename, 'w')
  populations_file.write('district_id,' +
                         'population,males,females,' +
                         'literates,literate_males,literate_females,' +
                         'working,working_males,working_females,' + 
                         'non_working,non_working_males,non_working_females' + '\n')

  all_district_ids = set([])
  for row in range(1, sheet.nrows):
    dist_id = parse_district_id(sheet.cell_value(row, 1))
    if dist_id == 0:
      continue
    if dist_id not in all_district_ids:
      all_district_ids.add(dist_id)

    if not sheet.cell_value(row, 8) == 'Total':
      continue

    populations_file.write(str(dist_id) + ',' +
                           str(int(sheet.cell_value(row, 10))) + ',' +
                           str(int(sheet.cell_value(row, 11))) + ',' +
                           str(int(sheet.cell_value(row, 12))) + ',' +
                           str(int(sheet.cell_value(row, 22))) + ',' +
                           str(int(sheet.cell_value(row, 23))) + ',' +
                           str(int(sheet.cell_value(row, 24))) + ',' +
                           str(int(sheet.cell_value(row, 28))) + ',' +
                           str(int(sheet.cell_value(row, 29))) + ',' +
                           str(int(sheet.cell_value(row, 30))) + ',' +
                           str(int(sheet.cell_value(row, -3))) + ',' +
                           str(int(sheet.cell_value(row, -2))) + ',' +
                           str(int(sheet.cell_value(row, -1))) + '\n')

  check_districts_equal(district_keys, all_district_ids, 'populations')

  populations_file.close()

def parse_age_data(district_keys, out_filename):
  age_data = {}

  files = os.listdir('data/raw_data/age')
  for f in files:
    print (f)
    sheet = xlrd.open_workbook('data/raw_data/age/' + f).sheet_by_index(0)
    
    for row in range(5, sheet.nrows):
      dist_id = parse_district_id(sheet.cell_value(row, 2))
      if dist_id == 0:
        continue
      if dist_id not in age_data:
        age_data[dist_id] = {}
 
      age_str = str(sheet.cell_value(row, 4))
      if 'All ages' in age_str:
        continue

      if 'Age not stated' in age_str:
        age = -1
      elif '100+' in age_str:
        age = 100
      else:
        age = int(eval(age_str))
      if age not in age_data[dist_id]:
        age_data[dist_id][age] = {}

      age_data[dist_id][age]['total'] = int(sheet.cell_value(row, 5))
      age_data[dist_id][age]['male'] = int(sheet.cell_value(row, 6))
      age_data[dist_id][age]['female'] = int(sheet.cell_value(row, 7))

  ages_file = open(out_filename, 'w')
  prefixes = ['total', 'male', 'female']

  heading = "district_id,"
  for p in prefixes:
    heading += p + '_none,'
    for a in range(0, 100, 5):
      heading += p + '_' + str(a) + ','
    heading += p + '_' + '100' + ','
  ages_file.write(heading[:-1] + '\n')

  for d in sorted(age_data.keys()):
    data_line = str(d) + ','
    for p in prefixes:
      data_line += str(age_data[d][-1][p]) + ','
      for a in range(0, 100, 5):
        group_sum = 0
        for i in range(5):
          group_sum += age_data[d][a + i][p]
        data_line += str(group_sum) + ','
      data_line += str(age_data[d][100][p]) + ','
    ages_file.write(data_line[:-1] + '\n')

  check_districts_equal(district_keys, age_data.keys(), 'age_groups')

  ages_file.close()

def parse_religion_data(district_keys, out_filename):
  religion_file = open(out_filename, 'w')
  religion_file.write('district_id,hindu,muslim,christian,sikh,buddhist,jain,other,none' + '\n')

  all_district_ids = set()
  files = os.listdir('data/raw_data/religion')
  for f in files:
    print (f)
    sheet = xlrd.open_workbook('data/raw_data/religion/' + f).sheet_by_index(0)
    
    for row in range(5, sheet.nrows):
      dist_id = parse_district_id(sheet.cell_value(row, 2))
      if dist_id == 0:
        continue
      if dist_id not in all_district_ids:
        all_district_ids.add(dist_id)

      tripura_dist_ids = range(289, 293)

      district_str = sheet.cell_value(row, 5).strip()
      region_str = sheet.cell_value(row, 6).strip()
      if (not region_str == 'Total' or
          dist_id in tripura_dist_ids and
            (district_str.startswith('State') or
             district_str.startswith('Sub-District') or
             district_str.endswith(')') or
             district_str == 'Area not under any Sub-district') or
          dist_id not in tripura_dist_ids and
            not district_str.split('-')[0].strip() == 'District'):
        continue

      religion_file.write(str(dist_id) + ',' +
                          str(int(sheet.cell_value(row, 10))) + ',' +
                          str(int(sheet.cell_value(row, 13))) + ',' +
                          str(int(sheet.cell_value(row, 16))) + ',' +
                          str(int(sheet.cell_value(row, 19))) + ',' +
                          str(int(sheet.cell_value(row, 22))) + ',' +
                          str(int(sheet.cell_value(row, 25))) + ',' +
                          str(int(sheet.cell_value(row, 28))) + ',' +
                          str(int(sheet.cell_value(row, 31))) + '\n')

  check_districts_equal(district_keys, all_district_ids, 'religions')

  religion_file.close()

def parse_education_data(district_keys, out_filename):
  education_file = open(out_filename, 'w')
  education_file.write('district_id,illiterate,only_literate,below_primary,primary,middle,secondary,' +
                       'intermediate,non_tech_diploma,tech_diploma,graduate,unknown' + '\n')

  all_district_ids = set()
  files = os.listdir('data/raw_data/education')
  for f in files:
    print (f)
    sheet = xlrd.open_workbook('data/raw_data/education/' + f).sheet_by_index(0)
    
    for row in range(5, sheet.nrows):
      dist_id = parse_district_id(sheet.cell_value(row, 2))
      if dist_id == 0:
        continue
      if dist_id not in all_district_ids:
        all_district_ids.add(dist_id)

      region_str = sheet.cell_value(row, 4).strip()
      age_str = str(sheet.cell_value(row, 5)).strip()
      if (not region_str == 'Total' or
          not age_str == 'All ages'):
        continue

      education_file.write(str(dist_id) + ',' +
                           str(int(sheet.cell_value(row, 9))) + ',' +
                           str(int(sheet.cell_value(row, 15))) + ',' +
                           str(int(sheet.cell_value(row, 18))) + ',' +
                           str(int(sheet.cell_value(row, 21))) + ',' +
                           str(int(sheet.cell_value(row, 24))) + ',' +
                           str(int(sheet.cell_value(row, 27))) + ',' +
                           str(int(sheet.cell_value(row, 30))) + ',' +
                           str(int(sheet.cell_value(row, 33))) + ',' +
                           str(int(sheet.cell_value(row, 36))) + ',' +
                           str(int(sheet.cell_value(row, 39))) + ',' +
                           str(int(sheet.cell_value(row, 42))) + '\n')

  check_districts_equal(district_keys, all_district_ids, 'education')

  education_file.close()

def parse_language_data(district_keys, out_filename):
  languages = {}

  all_languages = set()
  files = os.listdir('data/raw_data/language')
  for f in files:
    print (f)
    sheet = xlrd.open_workbook('data/raw_data/language/' + f).sheet_by_index(0)
    
    for row in range(5, sheet.nrows):
      dist_id = parse_district_id(sheet.cell_value(row, 2))
      if dist_id == 0:
        continue
      if dist_id not in languages:
        languages[dist_id] = {}

      sub_dist_id = parse_district_id(sheet.cell_value(row, 3))
      if not sub_dist_id == 0:
        continue
      
      language_str = sheet.cell_value(row, 6)
      parts = language_str.strip().split(' ')
      if not len(parts) == 2 or not parts[0].isnumeric() or not parts[1].isalpha() or parts[1] == 'Others':
        continue

      lang = parts[1].lower().split('/')[0].strip()
      if not lang in all_languages:
        all_languages.add(lang)
      if not lang in languages[dist_id]:
        languages[dist_id][lang] = 0
      languages[dist_id][lang] += int(sheet.cell_value(row, 7))

  languages_file = open(out_filename, 'w')
  heading = 'district_id,'
  for l in sorted(all_languages):
    heading += l + ','
  languages_file.write(heading[:-1] + '\n')

  for d in sorted(languages.keys()):
    dist_line = str(d) + ','
    for l in sorted(all_languages):
      if l in languages[d]:
        dist_line += str(int(languages[d][l])) + ','
      else:
        dist_line += '0,'
    languages_file.write(dist_line[:-1] + '\n')

  check_districts_equal(district_keys, languages.keys(), label = 'languages')

  languages_file.close()
  

m, districts = get_basemap_and_district_info(show_background_map = False)

# parse_district_info(m.districts_info, out_filename = 'data/districts.csv')
# parse_population_data(districts.keys(), out_filename = 'data/populations.csv')
# parse_age_data(districts.keys(), out_filename = 'data/age_groups.csv')
# parse_religion_data(districts.keys(), out_filename = 'data/religions.csv')
# parse_education_data(districts.keys(), out_filename = 'data/education.csv')
# parse_language_data(districts.keys(), out_filename = 'data/languages.csv')

