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
    'A1': {'location': 'L2', 'capacity': 5, 'path': [], 'state': "available", 'current_path': [], 'victim': None, 'hospital': None},
}
state1.victims = {
    'V1': {'location': 'L1', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},
    'V2': {'location': 'L2', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},
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

#possible values(ambulance) for state are: "available", "to_victim", "to_hospital"
#possible values(victim) for state are: "waiting", "ambulance_assigned", "treated"
state2 = pyhop.State('state1')
state2.ambulances = {
    'A1': {'location': 'L4', 'capacity': 5, 'path': [], 'state': "available", 'current_path': [], 'victim': None, 'hospital': None}

}
state2.victims = {
    'V1': {'location': 'L1', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},
    'V2': {'location': 'L2', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},

}
state2.hospitals = {
    'H1': {'location': 'L3'},
}
state2.coordinates = {
    'L1': {'X': 50, 'Y': 50}, 'L2': {'X': 75, 'Y': 50}, 'L3': {'X': 100, 'Y': 50},'L4': {'X': 25, 'Y': 50},
}

state2.connections = {
    'L1': ['L2', 'L4'],
    'L2': ['L1', 'L3'],
    'L3': ['L2'],
    'L4': ['L1'],
}
#state3 (Paper)
#possible values(ambulance) for state are: "available", "to_victim", "to_hospital"
#possible values(victim) for state are: "waiting", "ambulance_assigned", "treated"
state3 = pyhop.State('state3')
state3.ambulances = {
    'A1': {'location': 'L7', 'capacity': 9, 'path': [], 'state': "available", 'current_path': [], 'victim': None, 'hospital': None},
    'A2': {'location': 'L5', 'capacity': 6, 'path': [], 'state': "available", 'current_path': [], 'victim': None, 'hospital': None},
}
state3.victims = {
    'V1': {'location': 'L1', 'severity': 8, 'first_aid_done': False, 'state': "waiting"},
    'V2': {'location': 'L6', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},
    'V3': {'location': 'L3', 'severity': 6, 'first_aid_done': False, 'state': "waiting"},
}
state3.hospitals = {
    'H1': {'location': 'L7'},
    'H2': {'location': 'L8'},
}
state3.coordinates = {
    'L1': {'X': 10, 'Y': 20}, 'L2': {'X': 20, 'Y': 20}, 'L3': {'X': 30, 'Y': 20}, 'L4': {'X': 20, 'Y': 10}, 'L5': {'X': 10, 'Y': 0},
    'L6': {'X': 30, 'Y': 0}, 'L7': {'X': 40, 'Y': 10}, 'L8': {'X': 0, 'Y': 10}
}

state3.connections = {
    'L1': ['L2', 'L5', 'L8'],
    'L2': ['L1', 'L3', 'L4'],
    'L3': ['L2', 'L6', 'L7'],
    'L4': ['L2', 'L5', 'L6'],
    'L5': ['L1', 'L4', 'L6', 'L8'],
    'L6': ['L3', 'L4', 'L5', 'L7'],
    'L7': ['L3', 'L6'],
    'L8': ['L1', 'L5'],
}
#state4 (Paper) big example
state4 = pyhop.State('state4')
state4.ambulances = {
    'A1': {'location': 'L5', 'capacity': 10, 'path': [], 'state': "available", 'current_path': [], 'victim': None, 'hospital': None},
    'A2': {'location': 'L7', 'capacity': 7, 'path': [], 'state': "available", 'current_path': [], 'victim': None, 'hospital': None},
    'A3': {'location': 'L4', 'capacity': 4, 'path': [], 'state': "available", 'current_path': [], 'victim': None, 'hospital': None},
}
state4.victims = {
    'V1': {'location': 'L2', 'severity': 9, 'first_aid_done': False, 'state': "waiting"},
    'V2': {'location': 'L2', 'severity': 8, 'first_aid_done': False, 'state': "waiting"},
    'V3': {'location': 'L8', 'severity': 6, 'first_aid_done': False, 'state': "waiting"},
    'V4': {'location': 'L9', 'severity': 3, 'first_aid_done': False, 'state': "waiting"},
    'V5': {'location': 'L14', 'severity': 2, 'first_aid_done': False, 'state': "waiting"},
    'V6': {'location': 'L13', 'severity': 5, 'first_aid_done': False, 'state': "waiting"},
}
state4.hospitals = {
    'H1': {'location': 'L4'},
    'H2': {'location': 'L5'},
    'H3': {'location': 'L7'},
}
state4.coordinates = {
    'L1': {'X': 1, 'Y': 20}, 'L2': {'X': 7, 'Y': 20}, 'L3': {'X': 13, 'Y': 20}, 'L4': {'X': 20, 'Y': 20}, 'L5': {'X': 0, 'Y': 15},
    'L6': {'X': 10, 'Y': 0}, 'L7': {'X': 10, 'Y': 26}, 'L8': {'X': 3, 'Y': 24}, 'L9': {'X': 15, 'Y': 7}, 'L10': {'X': 14, 'Y': 16},
    'L11': {'X': 19, 'Y': 14}, 'L12': {'X': 6, 'Y': 16}, 'L13': {'X': 11, 'Y': 13}, 'L14': {'X': 5, 'Y': 10}
}

state4.connections = {
    'L1': ['L2', 'L5', 'L8'],
    'L2': ['L1', 'L3', 'L5', 'L7', 'L8', 'L12'],
    'L3': ['L2', 'L4', 'L7', 'L10'],
    'L4': ['L3', 'L11'],
    'L5': ['L1', 'L2', 'L14'],
    'L6': ['L9', 'L14'],
    'L7': ['L2', 'L3'],
    'L8': ['L1', 'L2'],
    'L9': ['L6', 'L10', 'L11'],
    'L10': ['L3', 'L9', 'L13'],
    'L11': ['L4', 'L9'],
    'L12': ['L2', 'L13'],
    'L13': ['L10', 'L12'],
    'L14': ['L5', 'L6'],
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
state2.graph = create_graph(state2)
state3.graph = create_graph(state3)
state4.graph = create_graph(state4)

# Find shortest path using Dijkstra
def shortest_path(state, start, goal):
    try:
        path = nx.shortest_path(state.graph, source=start, target=goal, weight='weight')
        cost = nx.shortest_path_length(state.graph, source=start, target=goal, weight='weight')
        return path[1:], cost
    except nx.NetworkXNoPath:
        return None, float('inf')

#operators

def all_victims_treated(state):
    for victim, data in state.victims.items():
        if data['state'] != "treated":
            print(f"Victim {victim} is not treated")
            return False
    return True

def load_victim_op(state, ambulance):
    victim = state.victims[state.ambulances[ambulance]['victim']]
    x = victim['location']
    y = state.ambulances[ambulance]['location']
    if x == y and state.ambulances[ambulance]['state'] == 'to_victim' and victim['severity'] <= state.ambulances[ambulance]['capacity']:
        # update state and path
        hospital = assign_hospital(state, victim)
        path, cost = shortest_path(state, victim['location'], state.hospitals[hospital]['location'])
        if path:
            state.ambulances[ambulance]['current_path'] = path
        else:
            print(f"No path found for ambulance {ambulance} to hospital {hospital}")
            return []
        state.ambulances[ambulance]['state'] = "to_hospital"
        state.ambulances[ambulance]['hospital'] = hospital
        state.victims[state.ambulances[ambulance]['victim']]['location'] = ambulance

        return state
    else:
        print(f"Victim {victim} is not at the same location as ambulance {ambulance}")
        return False

def unload_victim_op(state, ambulance):
    x = state.ambulances[ambulance]['location']
    victim = state.ambulances[ambulance]['victim']
    hospital = state.hospitals[state.ambulances[ambulance]['hospital']]
    if x == hospital['location'] and ambulance == state.victims[victim]['location']:
        state.victims[victim]['location'] = hospital
        # update state, patient treated
        state.ambulances[ambulance]['victim'] = None
        state.ambulances[ambulance]['hospital'] = None
        state.ambulances[ambulance]['state'] = "available"
        state.victims[victim]['state'] = "treated"
        return state
    else:
        print(f"Victim {victim} is not at the same location as hospital {hospital}")
        return False

def move_ambulance_op(state, ambulance, y):
    x = state.ambulances[ambulance]['location']
    if y in state.connections[x]:
        state.ambulances[ambulance]['location'] = y
        state.ambulances[ambulance]['path'].append(y)
        return state
    else:
        print(f"Ambulance {ambulance} cannot move to location {y}")
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
    min_cost = float('inf')
    best_victim = None
    ambulance_loc = state.ambulances[ambulance]['location']
    for victim, data in state.victims.items():
        if (data['severity'] <= state.ambulances[ambulance]['capacity'] and
                data['state'] == "waiting" and state.ambulances[ambulance]['state'] == "available"):
            _, cost = shortest_path(state, ambulance_loc, data['location'])
            if cost < min_cost:
                min_cost = cost
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
    min_cost = float('inf')
    best_hospital = None
    victim_loc = victim['location']
    for hospital, data in state.hospitals.items():
        if victim_loc in state.coordinates and data['location'] in state.coordinates:
            _, cost = shortest_path(state, victim_loc, data['location'])
            if cost < min_cost:
                min_cost = cost
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
                    state.ambulances[ambulance]['current_path'] = path

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
        return [('provide_first_aid_op', victim)]
    return []

pyhop.declare_methods('first_aid_necessary', first_aid_if_necessary)

def do_step(state):
    moves = []
    for ambulance, data in state.ambulances.items():
        if len(data["current_path"]) > 0:
            next_loc = data["current_path"].pop(0)
            moves.append(('move_ambulance_op', ambulance, next_loc))

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
        moves.append(('first_aid_necessary', state.ambulances[ambulance]['victim'], ambulance))
        moves.append(('load_victim_op', ambulance))
    elif state.ambulances[ambulance]['state'] == "to_hospital":
        #unload
        moves.append(('unload_victim_op', ambulance))
    return moves
        #ambulance available

def treat_all_victims(state):
    # Check if all victims are treated
    if all(data['state'] == "treated" for data in state.victims.values()):
        return []  # Goal satisfied → No more actions needed
    assign_goals(state)
    return [('do_step',), ('treat_all_victims',)]

pyhop.declare_methods('treat_all_victims', treat_all_victims)
pyhop.declare_methods('do_step', do_step)
pyhop.declare_methods('handle_goal_completion', handle_goal_completion)
pyhop.declare_methods('assign_goals', assign_goals)


goal = [('treat_all_victims',)]

pyhop.pyhop(state4, goal, verbose=3)
