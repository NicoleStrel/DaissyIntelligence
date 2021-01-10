def correctingrewards(file_of_rewards):
    array1 = []
    file_of_rewards = open(file_of_rewards, "r")
    lines = file_of_rewards.readlines()
    for line in lines:
        line = line.rstrip()
        array1.append(float(line))
    return array1

def state_values(filename):
    array1 = []
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        array1.append(int(line))
    return array1

def action_values(filename):
    array1 = []
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        temp_array = []
        for item in line:
            if item != " ":
                temp_array.append(int(item))
        array1.append(temp_array)
    return array1

def q_table(states, actions, rewards):
    q_table = []
    for i in range(0, len(states)):
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
    for key1 in state_dict.keys(): # item[0] = key
        sub_dict = {}
        ll = state_dict[key1] # [item[2], item[1]] list
        for thing in ll: # [item[2], item[1]]
            if isinstance(thing, float):
                sub_dict.update({ll[0]: ll[1]})
                break
            else:
                if thing[0] not in sub_dict.keys():
                    sub_dict.update({thing[0]: thing[1]})
                else:
                    sub_dict[thing[0]].append(thing[1])
        indices_for_state = find_two_indices_for_state(sub_dict)
        data = [str(key1), str(indices_for_state[0]), str(indices_for_state[1])]
        qdata = open("MLdata.txt", "a")
        qdata.write(" ".join(data))
        qdata.write("\n")
        qdata.close()
        answers.update({key1: indices_for_state})
    return answers

def find_two_indices_for_state(sub_dict):
    sorted_list = sub_dict.keys()
    # if only one item in list
    if len(sorted_list) == 1:
        return find_most_repeated(sub_dict.values())
    y = sorted(sorted_list)
    y.reverse()
    top_20th = int(len(y)/5) + 1
    top_20_data = []
    for i in range(top_20th):
        top_20_data.append(sub_dict[y[i]])
    return find_most_repeated(top_20_data)

def find_most_repeated(nested_list):
    num_list = [0,0,0,0,0,0,0,0,0,0]
    for l in nested_list: # l = [1, 0]
        for j in range(10):
            if l[0] == j or l[1] == j:
                num_list[j] += 1
    copy = num_list.copy()
    x = sorted(copy)
    if x[8] == x[9]:
        one = num_list.index(x[9])
        num_list[one] = 0
        two = num_list.index(x[8])
        return one, two
    return num_list.index(x[9]), num_list.index(x[8])

if __name__ == "__main__":
    rewardfile = "q_rewards.txt"
    rewards = correctingrewards(rewardfile)
    print(rewards)
    statefile = "q_states.txt"
    states = state_values(statefile)
    print(states)
    actionfile = "q_actions.txt"
    actions = action_values(actionfile)
    print(actions)
    q_table = q_table(states, actions, rewards)
    answer = process_data(q_table)
    print(answer)