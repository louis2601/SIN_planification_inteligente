import math
import pyhop

state1 = pyhop.State('state1')
state1.ambulances = {
    'A1': {'location': 'L1', 'capacity': 5, 'available': True},
    'A2': {'location': 'L3', 'capacity': 7, 'available': True},
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
    {'Huelva': {'X': 25, 'Y': 275}, 'Cadiz': {'X': 200, 'Y': 50}, 'Sevilla': {'X': 250, 'Y': 325},
    'Cordoba': {'X': 475, 'Y': 450}, 'Malaga': {'X': 550, 'Y': 100}, 'Jaen': {'X': 750, 'Y': 425},
    'Granada': {'X': 800, 'Y': 250}, 'Almeria': {'X': 1000, 'Y': 150}}
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
        state.amubulances[ambulance]['location'] = y
        state.path.append(y)
        state.cost += distance(state.coordinates[x], state.coordinates[y])
        return state
    else:
        return False
     
def provide_treatment(state, ambulance, victim):
    if (state.ambulances[ambulance]['location'] == state.victims[victim]['location'] and
        state.victims[victim]['first_aid_done'] == False and
        state.victims[victim]['treated'] == False and
        state.victim['severity'] >= 7):
        state.victims[victim]['first_aid_done'] = True
        return state
    else:
        return False 

pyhop.declare_operators(move_ambulance, provide_treatment, load_victim, unload_victim)
