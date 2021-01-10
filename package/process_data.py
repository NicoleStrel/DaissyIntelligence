def correctingrewards(file_of_rewards):
  array1 = []
    f = open(file_of_rewards, "r")
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        array1.append(line)
    # get rid of first number
    # array1.pop(0)
    # replace false zeros with NONE
    for i in range(9, len(array1), 9):
      array1[i] = NONE
    return array1

def state_values(filename):
    array1 = []
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        array1.append(line)
    return array1

def action_values(filename):
    array1 = []
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        temp_array = []
        for item in line:
            temp_array.append(item)
        array1.append(temp_array)
    return array1

def q_table(states, actions, rewards):
  q_table = []
  for i in range(len(states)):
    new_data = [states[i], actions[i], rewards[i]]
    q_table.append(new_data)
  return q_table

def process_data(q_table):
  # split data into states
  state_dict = {}
  answers = {}
  for item in q_table:
    if item[0] not in state_dict.keys():
      state_dict.update({item[0]: [item[2], item[1]]})
    else:
      state_dict[item[0]].append([item[2], item[1]])
      #{item[0]: [item[2], item[1]],[item[2], item[1]]}
  for key1 in state_dict.keys(): # item[0] = key
    sub_dict = {}
    ll = state_dict[key1] # [item[2], item[1]] list
    for thing in ll: # [item[2], item[1]]
      if thing[0] not in sub_dict.keys():
        sub_dict.update({thing[0]: thing[1]})
      else:
        sub_dict[thing[0]].append(thing[1])
      #sub_dict = {reward: [], [], reward: [], []}
    indices_for_state = find_two_indicies_for_state(sub_dict)
    answers.update({key1: indicies_for_state})
  return answers

def find_two_indicies_for_state(sub_dict)
  # sort
  sorted_list = sub_dict.keys()
  sorted(sorted_list)
  top_20th = int(len(sorted_list)/5)
  top_20_data = []
  for reward in top_20th:
    top_20_data.append(sub_dict[reward])
    #[[indices], [indices], ...]
  top_indices_for_this_state = def find_most_repeated(top_20_data)
  
def find_most_repeated(nested_list):
  num_list = [0,0,0,0,0,0,0,0,0,0]
  for l in nested_list: # l = [1, 0]
    for j in len(10):
      if l[0] == j or l[1] == j:
        num_list[j] += 1
  copy = num_list
  sorted(copy)

  if copy[8] == copy[9]:
    one = num_list.index(copy[8])
    num_list[one]= 0
    two = num_list.index(copy[9])
    return one, two
    
  return num_list.index(copy[9]), num_list.index(copy[8])



run = "echo hello word"
rewardfile = "data/q_rewards.txt"
rewards = correctingrewards(rewardfile)
statefile = "data/q_states.txt"
states = state_values(statefile)
actionfile = "data/q_action.txt"
actions = action_values(actionfile)
q_table = q_table(states, actions, rewards)
answer = process_data(q_table)
print(answer)