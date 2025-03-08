import math
import pyhop
import networkx as nx

class NoHospitalFoundException(Exception):
    def __init__(self, victim, victim_location):
        self.victim = victim
        self.victim_location = victim_location
        super().__init__(f"No hospital found for victim {victim} at location {victim_location}")

#possible values(ambulance) for state are: "available", "to_victim", "to_hospital"
#possible values(victim) for state are: "waiting", "ambulance_assigned", "treated"
state1 = pyhop.State('state1')
state1.ambulances = {
    'A1': {'location': 'L2', 'capacity': 5, 'path': ['L1'], 'state': "available", 'current_path': [], 'victim': None, 'hospital': None},
}
state1.victims = {
    'V1': {'location': 'L1', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},
}
state1.hospitals = {
    'H1': {'location': 'L3'},
}
state1.coordinates = {
    'L1': {'X': 50, 'Y': 50}, 'L2': {'X': 75, 'Y': 50}, 'L3': {'X': 25, 'Y': 50},
}

state1.connections = {
    'L1': ['L2', 'L3'],
    'L2': ['L1'],
    'L3': ['L1'],
}

# utilities

def distance(c1, c2):
    x = pow(c1['X'] - c2['X'], 2)
    y = pow(c1['Y'] - c2['Y'], 2)
    return math.sqrt(x + y)

# Create graph and add edges with Euclidean distance as weight
def create_graph(state):
    G = nx.Graph()
    for node in state.coordinates:
        G.add_node(node)

    for node, neighbors in state.connections.items():
        for neighbor in neighbors:
            dist = distance(state.coordinates[node], state.coordinates[neighbor])
            G.add_edge(node, neighbor, weight=dist)

    return G

state1.graph = create_graph(state1)

# Find shortest path using Dijkstra
def shortest_path(state, start, goal):
    try:
        path = nx.shortest_path(state.graph, source=start, target=goal, weight='weight')
        cost = nx.shortest_path_length(state.graph, source=start, target=goal, weight='weight')
        return path, cost
    except nx.NetworkXNoPath:
        return None, float('inf')

#operators

def all_victims_treated(state):
    for victim, data in state.victims.items():
        if data['state'] != "treated":
            return False
    return True

def load_victim_op(state, victim, ambulance):
    x = state.victims[victim]['location']
    y = state.ambulances[ambulance]['location']
    if x == y and state.ambulances[ambulance]['state'] == 'available' and state.victims[victim]['severity'] <= state.ambulances[ambulance]['capacity']:
        state.victims[victim]['location'] = ambulance
        state.ambulances[ambulance]['state'] = "to_hospital"
        return state
    else:
        return False

def unload_victim_op(state, victim, ambulance, hospital):
    x = state.ambulances[ambulance]['location']
    if x == state.hospitals[hospital]['location'] and state.victims[victim]['location'] == ambulance:
        state.victims[victim]['location'] = hospital
        state.ambulances[ambulance]['state'] = "available"
        return state
    else:
        return False

def move_ambulance_op(state, ambulance, y):
    x = state.ambulances[ambulance]['location']
    if y in state.connections[x]:
        state.ambulances[ambulance]['location'] = y
        state.ambulances[ambulance]['path'].append(y)
        return state
    else:
        return False

def provide_first_aid_op(state, victim):
    state.victims[victim]['first_aid_done'] = True
    return state

pyhop.declare_operators(move_ambulance_op, provide_first_aid_op, load_victim_op, unload_victim_op, all_victims_treated)

#methods

def assign_victim(state, ambulance):
    """
    Find the nearest victim that the ambulance can handle.

    Args:
        state (State): Current problem state.
        ambulance (str): ID of the ambulance.

    Returns:
        str | bool: Assigned victim ID or False if none found.
    """
    min_distance = float('inf')
    best_victim = None
    ambulance_loc = state.ambulances[ambulance]['location']

    for victim, data in state.victims.items():
        if (data['severity'] <= state.ambulances[ambulance]['capacity'] and
                data['state'] == "waiting" and state.ambulances[ambulance]['state'] == "available"):

            dist = distance(state.coordinates[ambulance_loc], state.coordinates[data['location']])
            if dist < min_distance:
                min_distance = dist
                best_victim = victim

    return best_victim or False


def assign_hospital(state, victim):
    """
    Find the nearest hospital to the victim.

    Args:
        state (State): Current problem state.
        victim (str): ID of the victim.

    Returns:
        str: Hospital ID.

    Raises:
        NoHospitalFoundException: If no hospital is found.
    """
    min_distance = float('inf')
    best_hospital = None
    victim_loc = state.victims[victim]['location']
    for hospital, data in state.hospitals.items():
        if victim_loc in state.coordinates and data['location'] in state.coordinates:
            dist = distance(state.coordinates[victim_loc], state.coordinates[data['location']])
            if dist < min_distance:
                min_distance = dist
                best_hospital = hospital

    if best_hospital is None:
        raise NoHospitalFoundException(victim, victim_loc)

    return best_hospital

def assign_goals(state):
    #see if any victim is waiting
    victims_waiting = False
    for victim, data in state.victims.items():
        if data['state'] == "waiting":
            victims_waiting = True
            break
    if victims_waiting:
        for ambulance, data in state.ambulances.items():
            #any ambulance is available
            if data["state"] == "available":
                victim = assign_victim(state, ambulance)
                if victim:
                    #assign victim to ambulance
                    state.ambulances[ambulance]['state'] = "to_victim"
                    state.ambulances[ambulance]['victim'] = victim
                    state.victims[victim]['state'] = "ambulance_assigned"
                    #add the path to the ambulance
                    path, _ = shortest_path(state, data['location'], state.victims[victim]['location'])
                    state.ambulances[ambulance]['current_path'] = path[1:]

def first_aid_if_necessary(state, victim, ambulance):
    """
    Return action to provide first aid if conditions are met.

    Args:
        state (State): Current problem state.
        victim (str): Victim ID.
        ambulance (str): Ambulance ID.

    Returns:
        list | bool: Action list or False.
    """
    if (state.victims[victim]['severity'] >= 7 and
        not state.victims[victim]['first_aid_done'] and
        state.ambulances[ambulance]['location'] == state.victims[victim]['location'] and
        state.ambulances[ambulance]['capacity'] >= state.victims[victim]['severity']):
        return [('provide_first_aid_op', ambulance, victim)]
    return False

def do_step(state):
    moves = []
    for ambulance, data in state.ambulances.items():
        if len(data["current_path"]) > 0:
            next_loc = data["current_path"].pop(0)
            moves.append(('move_ambulance_op', ambulance, next_loc))
            state.ambulances[ambulance]['location'] = next_loc

            if not data["current_path"]:
                moves.extend(handle_goal_completion(state, ambulance))
    return moves if moves else []

#This should check if the ambulance reached the victim or reached the hospital and handle it
def handle_goal_completion(state, ambulance):
    moves = []
    if state.ambulances[ambulance]['state'] == "to_victim":
        #first aid
        first_aid_action = first_aid_if_necessary(state, state.ambulances[ambulance]['victim'], ambulance)
        if first_aid_action:
            moves.extend(first_aid_action)
        #load victim
        moves.append(('load_victim_op', state.ambulances[ambulance]['victim'], ambulance))
        #update state and path
        hospital = assign_hospital(state, state.ambulances[ambulance]['victim'])
        path, cost = shortest_path(state, state.victims[state.ambulances[ambulance]['victim']]['location'], state.hospitals[hospital]['location'])
        if path:
            state.ambulances[ambulance]['current_path'] = path
        else:
            print(f"No path found for ambulance {ambulance} to hospital {hospital}")
            return []
        state.ambulances[ambulance]['current_path'] = path
        state.ambulances[ambulance]['state'] = "to_hospital"
        state.ambulances[ambulance]['hospital'] = hospital
    elif state.ambulances[ambulance]['state'] == "to_hospital":
        #unload
        moves.append(('unload_victim_op', state, state.victims[state.ambulances[ambulance]['victim']], ambulance, state.ambulances[ambulance]['hospital']))
        #update state, patient treated
        state.victims[state.ambulances[ambulance]['victim']]['state'] = "treated"
        state.ambulances[ambulance]['state'] = "available"
        state.ambulances[ambulance]['victim'] = None
        state.ambulances[ambulance]['hospital'] = None
    return moves
        #ambulance available

def treat_all_victims(state):
    # Check if all victims are treated
    if all(data['state'] == "treated" for data in state.victims.values()):
        return []  # Goal satisfied → No more actions needed
    assign_goals(state)
    #print the updated states
    for ambulance, data in state.ambulances.items():
        print(ambulance, data)
    return [('do_step',), ('treat_all_victims',)]


import pyhop

# Declarar métodos para la tarea 'treat_all_victims'
pyhop.declare_methods('treat_all_victims', treat_all_victims)

# Declarar métodos para la tarea 'do_step'
pyhop.declare_methods('do_step', do_step)

# Declarar métodos para la tarea 'handle_goal_completion'
pyhop.declare_methods('handle_goal_completion', handle_goal_completion)

# Declarar métodos para la tarea 'assign_goals'
pyhop.declare_methods('assign_goals', assign_goals)


goal = [('treat_all_victims',)]

pyhop.pyhop(state1, goal, verbose=3)
