import sys

n = 2

#take cmd argument - how many frogs on each side
if len(sys.argv) == 2:
    n = int(sys.argv[1])
else:
    raise Exception("Number of frogs must be specified")

field = n * ">" + "_" + n * "<"
target_field = n * "<" + "_" + n * ">"

#get all possible moves from a given state of the field
def get_all_children(state):
    children = []
    for i in range(len(state)):
        child = list(state)
        if state[i] == ">" and i + 1 < len(state) and state[i + 1] == "_":
            child[i], child[i + 1] = child[i + 1], child[i]
        elif state[i] == ">" and i + 2 < len(state) and state[i + 2] == "_":
            child[i], child[i + 2] = child[i + 2], child[i]
        elif state[i] == "<" and i - 1 >=0  and state[i - 1] == "_":
            child[i], child[i - 1] = child[i - 1], child[i]
        elif state[i] == "<" and i - 2 >= 0  and state[i - 2] == "_":
            child[i], child[i - 2] = child[i - 2], child[i]
        if child != state:
            children.append(child)
    return children

def find_solution(current, path):
    if current == list(target_field):
        return path
    for child in get_all_children(current):
        path_so_far = find_solution(child, path + [child])
        if path_so_far != None:
            return path_so_far

def frogs():
    for x in ["".join(x) for x in find_solution(list(field), [field])]:
        print(x)

frogs()
