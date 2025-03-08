import math
import pyhop

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
    'Huelva': {'X': 25, 'Y': 275}, 'Cadiz': {'X': 200, 'Y': 50}, 'Sevilla': {'X': 250, 'Y': 325},
    'Cordoba': {'X': 475, 'Y': 450}, 'Malaga': {'X': 550, 'Y': 100}, 'Jaen': {'X': 750, 'Y': 425},
    'Granada': {'X': 800, 'Y': 250}, 'Almeria': {'X': 1000, 'Y': 150}
}
 
state1.connections = {
    'L1': ['L2', 'L3'],
    'L2': ['L3', 'L5'],
    'L3': ['L4'],
    'L4': ['L5'],
    'L5': ['L6'],
    'L6': []
}

#operators

def distance(c1, c2):
    x = pow(c1['X'] - c2['X'], 2)
    y = pow(c1['Y'] - c2['Y'], 2)
    return math.sqrt(x + y)

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


