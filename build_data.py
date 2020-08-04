def get_populations():
  populations = {}

  pop_file = open('data/populations.csv', 'r').readlines()
  labels = pop_file[0].strip().split(',')
  for l in pop_file[1:]:
    parts = l.strip().split(',')

    dist_id = eval(parts[0])
    populations[dist_id] = {}

    for i, l in enumerate(labels):
      if i == 0:
        continue
      populations[dist_id][l] = eval(parts[i])

  return populations

def get_age_groups():
  age_groups = {}

  age_group_file = open('data/age_groups.csv', 'r').readlines()
  labels = age_group_file[0].strip().split(',')
  for l in age_group_file[1:]:
    parts = l.strip().split(',')

    dist_id = eval(parts[0])
    age_groups[dist_id] = {}

    for i, l in enumerate(labels):
      if i == 0:
        continue

      label_parts = l.split('_')
      group = label_parts[0]
      age_str = label_parts[1]
      if age_str == 'none':
        age = -1
      else:
        age = eval(age_str)

      if age not in age_groups[dist_id]:
        age_groups[dist_id][age] = {}
      age_groups[dist_id][age][group] = eval(parts[i])

  return age_groups

def get_religions():
  religions = {}

  religions_file = open('data/religions.csv', 'r').readlines()
  labels = religions_file[0].strip().split(',')
  for l in religions_file[1:]:
    parts = l.strip().split(',')

    dist_id = eval(parts[0])
    religions[dist_id] = {}

    for i, l in enumerate(labels):
      if i == 0:
        continue

      religions[dist_id][l] = eval(parts[i])

  return religions
 
