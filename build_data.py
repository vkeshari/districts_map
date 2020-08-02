def get_populations():
  populations = {}

  pop_file = open('data/populations.csv', 'r')
  for l in pop_file.readlines()[1:]:
    parts = l.split(',')

    dist_id = eval(parts[0])
    populations[dist_id] = {}

    populations[dist_id]['population'] = eval(parts[1])
    populations[dist_id]['males'] = eval(parts[2])
    populations[dist_id]['females'] = eval(parts[3])
    populations[dist_id]['literates'] = eval(parts[4])
    populations[dist_id]['literate_males'] = eval(parts[5])
    populations[dist_id]['literate_females'] = eval(parts[6])
    populations[dist_id]['working'] = eval(parts[7])
    populations[dist_id]['working_males'] = eval(parts[8])
    populations[dist_id]['working_females'] = eval(parts[9])
    populations[dist_id]['non_working'] = eval(parts[10])
    populations[dist_id]['non_working_males'] = eval(parts[11])
    populations[dist_id]['non_working_females'] = eval(parts[12])

  return populations

