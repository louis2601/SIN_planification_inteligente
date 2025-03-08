import math
import pyhop

state1 = pyhop.State('state1')
state1.ambulances = {
    'A1': {'location': 'L1', 'capacity': 5, 'available': True},
    'A2': {'location': 'L3', 'capacity': 7, 'available': True},
}
state1.victims = {
    'V1': {'location': 'L2', 'severity': 4, 'treated': False},
    'V2': {'location': 'L4', 'severity': 6, 'treated': False},
}
state1.hospitals = {
    'H1': {'location': 'L5'},
    'H2': {'location': 'L6'},
}
state1.coordinates = {
    'L1': (0, 0),
    'L2': (3, 4),
    'L3': (5, 1),
    'L4': (7, 6),
    'L5': (10, 2),
    'L6': (12, 8)
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


