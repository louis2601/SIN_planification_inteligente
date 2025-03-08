import math
import pyhop
import networkx as nx

state1 = pyhop.State('state1')
state1.ambulances = {
    'A1': {'location': 'L1', 'capacity': 5, 'available': True, 'path': ['L1']},
    'A2': {'location': 'L3', 'capacity': 7, 'available': True, 'path': ['L3']},
}
state1.victims = {
    'V1': {'location': 'L2', 'severity': 4, 'first_aid_done': False, 'treated': False},
    'V2': {'location': 'L4', 'severity': 6, 'first_aid_done': False, 'treated': False},
}
state1.hospitals = {
    'H1': {'location': 'L5'},
    'H2': {'location': 'L6'},
}
state1.coordinates = {
    'L1': {'X': 25, 'Y': 275}, 'L2': {'X': 200, 'Y': 50}, 'L3': {'X': 250, 'Y': 325},
    'L4': {'X': 475, 'Y': 450}, 'L5': {'X': 550, 'Y': 100}, 'L6': {'X': 750, 'Y': 425},
}
state1.connections = {
    'L1': ['L2', 'L3'],
    'L2': ['L3', 'L5'],
    'L3': ['L4'],
    'L4': ['L5'],
    'L5': ['L6','L2'],
    'L6': ['L5'],
}

# utility

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

#operators

def select_new_city(state, x, y):
    best = math.inf



def load_victim(state, victim, ambulance):
    x = state.victims[victim]['location']
    y = state.ambulances[ambulance]['location']
    if x == y and state.ambulances[ambulance]['available'] and state.victims[victim]['severity'] <= state.ambulances[ambulance]['capacity']:
        state.victims[victim]['location'] = ambulance
        state.ambulances[ambulance]['available'] = False
        return state
    else:
        return False

def unload_victim(state, victim, ambulance, hospital):
    x = state.ambulances[ambulance]['location']
    if x == state.hospitals[hospital]['location'] and state.victims[victim]['location'] == ambulance:
        state.victims[victim]['location'] = hospital
        state.ambulances[ambulance]['available'] = True
        return state
    else:
        return False

def move_ambulance(state, ambulance, y):
    x = state.ambulances[ambulance]['location']  
    if y in state.connection[x]:
        state.ambulances[ambulance]['location'] = y
        state.ambulances[ambulance]['path'].append(y)
        return state
    else:
        return False
     
def provide_first_aid(state, victim):
    state.victims[victim]['first_aid_done'] = True
    return state

pyhop.declare_operators(move_ambulance, provide_first_aid, load_victim, unload_victim)

#methods


def assign_ambulance(state, victim):
    """
    Find the nearest available ambulance that can handle the victim's severity.

    Args:
        state (State): Current problem state.
        victim (str): ID of the victim.

    Returns:
        str | bool: Assigned ambulance ID or False if none found.
    """
    min_distance = float('inf')
    best_ambulance = None
    victim_loc = state.victims[victim]['location']

    for ambulance, data in state.ambulances.items():
        if (data['available'] and
                state.victims[victim]['severity'] <= data['capacity'] and
                victim_loc in state.coordinates and data['location'] in state.coordinates):

            dist = distance(state.coordinates[victim_loc], state.coordinates[data['location']])
            if dist < min_distance:
                min_distance = dist
                best_ambulance = ambulance

    return best_ambulance or False

def assign_hospital(state, victim):
    """
    Find the nearest hospital to the victim.

    Args:
        state (State): Current problem state.
        victim (str): ID of the victim.

    Returns:
        str | bool: Hospital ID or False if none found.
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

    return best_hospital or False

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
        return [('provide_first_aid', ambulance, victim)]
    return False

def travel_m(state, ambulance, destination):
    x = state.ambulances[ambulance]['location']
    op_list = []
    path, cost = shortest_path(state, x, destination)
    if path:
        for place in path:
            op_list.append(('move_ambulance', ambulance, place))
        return op_list
    return False

pyhop.declare_methods('travel', travel_m, first_aid_if_necessary)

def move_ambulance_m(state, ambulance, victim):
    x = state.ambulances[ambulance]['location']
    y = state.victims[victim]['location']
    if x != y:
        z = select_new_city(state, y)
        return [('move_ambulance', ambulance, z)]


def deliver_victim(state, victim):
    hospital = assign_hospital(state, victim)
    ambulance = assign_ambulance(state, victim)
    if not hospital or not ambulance:
        return False

# Find shortest path using Dijkstra
def shortest_path(state, start, goal):
    try:
        path = nx.shortest_path(state.graph, source=start, target=goal, weight='weight')
        cost = nx.shortest_path_length(state.graph, source=start, target=goal, weight='weight')
        return path, cost
    except nx.NetworkXNoPath:
        return None, float('inf')

# Example usage
opList = travel_m(state1, 'A1', 'L5')
print(opList)
opList = travel_m(state1, 'A1', 'L6')
print(opList)