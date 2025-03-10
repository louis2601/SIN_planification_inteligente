import math
import pyhop
import networkx as nx

class NoHospitalFoundException(Exception):
    """
    Custom exception raised when no hospital can be found for a given victim.
    """
    def __init__(self, victim, victim_location):
        self.victim = victim
        self.victim_location = victim_location
        super().__init__(f"No hospital found for victim {victim} at location {victim_location}")


# ------------------------------------------------------------------------------------
# Sample States
# ------------------------------------------------------------------------------------
# Possible values for ambulance state: "available", "to_victim", "to_hospital"
# Possible values for victim state:    "waiting", "ambulance_assigned", "treated"

# State 1
state1 = pyhop.State('state1')
state1.ambulances = {
    'A1': {'location': 'L2', 'capacity': 5, 'path': [], 'state': "available",
           'current_path': [], 'victim': None, 'hospital': None},
}
state1.victims = {
    'V1': {'location': 'L1', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},
    'V2': {'location': 'L2', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},
}
state1.hospitals = {
    'H1': {'location': 'L3'},
}
state1.coordinates = {
    'L1': {'X': 50, 'Y': 50},
    'L2': {'X': 75, 'Y': 50},
    'L3': {'X': 25, 'Y': 50},
}
state1.connections = {
    'L1': ['L2', 'L3'],
    'L2': ['L1'],
    'L3': ['L1'],
}


# State 2
state2 = pyhop.State('state1')
state2.ambulances = {
    'A1': {'location': 'L4', 'capacity': 5, 'path': [], 'state': "available",
           'current_path': [], 'victim': None, 'hospital': None},
}
state2.victims = {
    'V1': {'location': 'L1', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},
    'V2': {'location': 'L2', 'severity': 4, 'first_aid_done': False, 'state': "waiting"},
}
state2.hospitals = {
    'H1': {'location': 'L3'},
}
state2.coordinates = {
    'L1': {'X': 50, 'Y': 50},
    'L2': {'X': 75, 'Y': 50},
    'L3': {'X': 100, 'Y': 50},
    'L4': {'X': 25, 'Y': 50},
}
state2.connections = {
    'L1': ['L2', 'L4'],
    'L2': ['L1', 'L3'],
    'L3': ['L2'],
    'L4': ['L1'],
}


# State 3 (Paper example)
state3 = pyhop.State('state3')
state3.ambulances = {
    'A1': {'location': 'L7', 'capacity': 9, 'path': [], 'state': "available",
           'current_path': [], 'victim': None, 'hospital': None},
    'A2': {'location': 'L5', 'capacity': 6, 'path': [], 'state': "available",
           'current_path': [], 'victim': None, 'hospital': None},
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
    'L1': {'X': 10, 'Y': 20}, 'L2': {'X': 20, 'Y': 20}, 'L3': {'X': 30, 'Y': 20},
    'L4': {'X': 20, 'Y': 10}, 'L5': {'X': 10, 'Y': 0},  'L6': {'X': 30, 'Y': 0},
    'L7': {'X': 40, 'Y': 10}, 'L8': {'X': 0,  'Y': 10},
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


# State 4 (Paper) - bigger example
state4 = pyhop.State('state4')
state4.ambulances = {
    'A1': {'location': 'L5', 'capacity': 10, 'path': [], 'state': "available",
           'current_path': [], 'victim': None, 'hospital': None},
    'A2': {'location': 'L7', 'capacity': 7, 'path': [], 'state': "available",
           'current_path': [], 'victim': None, 'hospital': None},
    'A3': {'location': 'L4', 'capacity': 4, 'path': [], 'state': "available",
           'current_path': [], 'victim': None, 'hospital': None},
}
state4.victims = {
    'V1': {'location': 'L2',  'severity': 9, 'first_aid_done': False, 'state': "waiting"},
    'V2': {'location': 'L2',  'severity': 8, 'first_aid_done': False, 'state': "waiting"},
    'V3': {'location': 'L8',  'severity': 6, 'first_aid_done': False, 'state': "waiting"},
    'V4': {'location': 'L9',  'severity': 3, 'first_aid_done': False, 'state': "waiting"},
    'V5': {'location': 'L14', 'severity': 2, 'first_aid_done': False, 'state': "waiting"},
    'V6': {'location': 'L13', 'severity': 5, 'first_aid_done': False, 'state': "waiting"},
}
state4.hospitals = {
    'H1': {'location': 'L4'},
    'H2': {'location': 'L5'},
    'H3': {'location': 'L7'},
}
state4.coordinates = {
    'L1':  {'X': 1,  'Y': 20},
    'L2':  {'X': 7,  'Y': 20},
    'L3':  {'X': 13, 'Y': 20},
    'L4':  {'X': 20, 'Y': 20},
    'L5':  {'X': 0,  'Y': 15},
    'L6':  {'X': 10, 'Y': 0},
    'L7':  {'X': 10, 'Y': 26},
    'L8':  {'X': 3,  'Y': 24},
    'L9':  {'X': 15, 'Y': 7},
    'L10': {'X': 14, 'Y': 16},
    'L11': {'X': 19, 'Y': 14},
    'L12': {'X': 6,  'Y': 16},
    'L13': {'X': 11, 'Y': 13},
    'L14': {'X': 5,  'Y': 10},
}
state4.connections = {
    'L1':  ['L2', 'L5', 'L8'],
    'L2':  ['L1', 'L3', 'L5', 'L7', 'L8', 'L12'],
    'L3':  ['L2', 'L4', 'L7', 'L10'],
    'L4':  ['L3', 'L11'],
    'L5':  ['L1', 'L2', 'L14'],
    'L6':  ['L9', 'L14'],
    'L7':  ['L2', 'L3'],
    'L8':  ['L1', 'L2'],
    'L9':  ['L6', 'L10', 'L11'],
    'L10': ['L3', 'L9', 'L13'],
    'L11': ['L4', 'L9'],
    'L12': ['L2', 'L13'],
    'L13': ['L10', 'L12'],
    'L14': ['L5', 'L6'],
}


# ------------------------------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------------------------------

def distance(c1, c2):
    """
    Compute Euclidean distance between two points c1 and c2.
    """
    x = (c1['X'] - c2['X'])**2
    y = (c1['Y'] - c2['Y'])**2
    return math.sqrt(x + y)


def create_graph(state):
    """
    Create a NetworkX graph for the given state's map layout.
    Each node is a location, and edges are weighted by Euclidean distance.
    """
    G = nx.Graph()
    for node in state.coordinates:
        G.add_node(node)

    for node, neighbors in state.connections.items():
        for neighbor in neighbors:
            dist = distance(state.coordinates[node], state.coordinates[neighbor])
            G.add_edge(node, neighbor, weight=dist)
    return G


def shortest_path(state, start, goal):
    """
    Find the shortest path (and its cost) between 'start' and 'goal'
    using Dijkstra's algorithm on the state's graph.
    Returns (path[1:], cost) so the first step is the next location.
    If no path is found, returns (None, infinity).
    """
    try:
        path = nx.shortest_path(state.graph, source=start, target=goal, weight='weight')
        cost = nx.shortest_path_length(state.graph, source=start, target=goal, weight='weight')
        return path[1:], cost
    except nx.NetworkXNoPath:
        return None, float('inf')

def assign_hospital(state, victim):
    """
    Find the nearest hospital to the given victim. Raises NoHospitalFoundException if none exists.
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

# Build graphs for each sample state
state1.graph = create_graph(state1)
state2.graph = create_graph(state2)
state3.graph = create_graph(state3)
state4.graph = create_graph(state4)


# ------------------------------------------------------------------------------------
# Operators
# ------------------------------------------------------------------------------------

def op_assign_victim(state, ambulance, victim):
    """
    Operator: Assign a waiting victim to an available ambulance if capacity allows.
    Updates the ambulance's state to 'to_victim' and the victim's state to 'ambulance_assigned'.
    Also sets the ambulance's current path to the victim's location.
    Returns the updated state or False if preconditions are not met.
    """
    if (state.victims[victim]['state'] == "waiting" and
        state.ambulances[ambulance]['state'] == "available" and
        state.victims[victim]['severity'] <= state.ambulances[ambulance]['capacity']):

        # State changes
        state.ambulances[ambulance]['state'] = "to_victim"
        state.ambulances[ambulance]['victim'] = victim
        state.victims[victim]['state'] = "ambulance_assigned"

        # Compute path to victim
        amb_loc = state.ambulances[ambulance]['location']
        vic_loc = state.victims[victim]['location']
        path, _ = shortest_path(state, amb_loc, vic_loc)
        state.ambulances[ambulance]['current_path'] = path
        return state

    return False

def load_victim_op(state, ambulance):
    """
    Operator: Load a victim into the ambulance if the ambulance has reached the victim.
    Assigns a path to the nearest hospital and updates the ambulance's state to 'to_hospital'.
    """
    victim_id = state.ambulances[ambulance]['victim']
    victim = state.victims[victim_id]
    amb_loc = state.ambulances[ambulance]['location']

    if (victim['location'] == amb_loc and
        state.ambulances[ambulance]['state'] == 'to_victim' and
        victim['severity'] <= state.ambulances[ambulance]['capacity']):

        hospital = assign_hospital(state, victim)
        path, cost = shortest_path(state, victim['location'], state.hospitals[hospital]['location'])
        if path:
            state.ambulances[ambulance]['current_path'] = path
        else:
            print(f"No path found for ambulance {ambulance} to hospital {hospital}")
            return []

        state.ambulances[ambulance]['state'] = "to_hospital"
        state.ambulances[ambulance]['hospital'] = hospital
        state.victims[victim_id]['location'] = ambulance
        return state

    print(f"Victim {victim} is not at the same location as ambulance {ambulance}")
    return False


def unload_victim_op(state, ambulance):
    """
    Operator: Unload a victim at the hospital if the ambulance has reached the hospital.
    Updates the victim's state to 'treated' and frees the ambulance (back to 'available').
    """
    amb_loc = state.ambulances[ambulance]['location']
    victim_id = state.ambulances[ambulance]['victim']
    hospital = state.hospitals[state.ambulances[ambulance]['hospital']]

    if amb_loc == hospital['location'] and ambulance == state.victims[victim_id]['location']:
        state.victims[victim_id]['location'] = hospital
        state.ambulances[ambulance]['victim'] = None
        state.ambulances[ambulance]['hospital'] = None
        state.ambulances[ambulance]['state'] = "available"
        state.victims[victim_id]['state'] = "treated"
        return state

    print(f"Victim {victim_id} is not at the same location as hospital {hospital}")
    return False


def move_ambulance_op(state, ambulance, loc):
    """
    Operator: Move an ambulance from its current location to 'y' if connected.
    Appends 'y' to the ambulance's path history.
    """
    x = state.ambulances[ambulance]['location']
    y = state.ambulances[ambulance]["current_path"][0]
    if y in state.connections[x]:
        state.ambulances[ambulance]['location'] = y
        state.ambulances[ambulance]['path'].append(y)
        state.ambulances[ambulance]["current_path"].pop(0)
        return state
    else:
        print(f"Ambulance {ambulance} cannot move to location {y}")
        return False


def provide_first_aid_op(state, victim):
    """
    Operator: Provide first aid to a victim, setting 'first_aid_done' to True.
    """
    state.victims[victim]['first_aid_done'] = True
    return state

pyhop.declare_operators(
    op_assign_victim,
    move_ambulance_op,
    provide_first_aid_op,
    load_victim_op,
    unload_victim_op
)


# ------------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------------

def assign_victim(state, ambulance):
    """
    Find the nearest waiting victim that the ambulance can handle, given capacity.
    Returns the victim ID or False if none is found.
    """
    min_cost = float('inf')
    best_victim = None
    ambulance_loc = state.ambulances[ambulance]['location']

    for victim, data in state.victims.items():
        if (data['state'] == "waiting" and
            state.ambulances[ambulance]['state'] == "available" and
            data['severity'] <= state.ambulances[ambulance]['capacity']):

            _, cost = shortest_path(state, ambulance_loc, data['location'])
            if cost < min_cost:
                min_cost = cost
                best_victim = victim

    return best_victim or False

def assign_goals(state):
    """
    Compound task: Assign an available ambulance to any waiting victim.
    - If no victim is waiting, returns [] (nothing to do).
    - If an ambulance can be assigned, returns op_assign_victim + (assign_goals).
    - Otherwise returns empty list.
    """
    any_waiting = any(data['state'] == "waiting" for data in state.victims.values())

    if not any_waiting:
        return []

    for ambulance, a_data in state.ambulances.items():
        if a_data["state"] == "available":
            victim = assign_victim(state, ambulance)
            if victim:
                return [
                    ('op_assign_victim', ambulance, victim),
                    ('assign_goals',)
                ]
    return []


def first_aid_if_necessary(state, victim, ambulance):
    """
    Compound task: Provide first aid if victim's severity >= 7, not yet helped, and ambulance is present.
    Returns the operator or an empty list if conditions are not met.
    """
    if (state.victims[victim]['severity'] >= 7 and
        not state.victims[victim]['first_aid_done'] and
        state.ambulances[ambulance]['location'] == state.victims[victim]['location'] and
        state.ambulances[ambulance]['capacity'] >= state.victims[victim]['severity']):
        return [('provide_first_aid_op', victim)]
    return []


pyhop.declare_methods('first_aid_necessary', first_aid_if_necessary)


def do_step(state):
    """
    Compound task: Move each ambulance step-by-step along its current path.
    When a path is finished, handle goal completion (loading/unloading victims).
    Returns a list of move operations + the goal completion tasks.
    """
    moves = []
    for ambulance, data in state.ambulances.items():
        print(f"Ambulance {ambulance} is at {data['location']} with path {data['current_path']}")
        if len(data["current_path"]) > 0:
            moves.append(('move_ambulance_op', ambulance, data["current_path"][0]))

        if not data["current_path"] and data["state"] in ["to_victim", "to_hospital"]:
            moves.extend(handle_goal_completion(state, ambulance))
    return moves if moves else []


def handle_goal_completion(state, ambulance):
    """
    Compound task: Checks if the ambulance has arrived at a victim or a hospital,
    then returns first-aid and load/unload tasks as needed.
    """
    moves = []
    if state.ambulances[ambulance]['state'] == "to_victim":
        victim_id = state.ambulances[ambulance]['victim']
        first_aid_action = first_aid_if_necessary(state, victim_id, ambulance)
        if first_aid_action:
            moves.extend(first_aid_action)

        moves.append(('first_aid_necessary', victim_id, ambulance))
        moves.append(('load_victim_op', ambulance))

    elif state.ambulances[ambulance]['state'] == "to_hospital":
        moves.append(('unload_victim_op', ambulance))

    return moves


def treat_all_victims(state):
    """
    Compound task: Continues until all victims are in 'treated' state.
    1) If all are treated, returns [].
    2) Otherwise, returns:
       - ('assign_goals',)
       - ('do_step',)
       - ('treat_all_victims',)
    """
    #print state of all victims to check
    if all(v_data['state'] == "treated" for v_data in state.victims.values()):
        return []
    return [
        ('assign_goals',),
        ('do_step',),
        ('treat_all_victims',)
    ]

def all_victims_treated(state):
    """
    Operator-like checker: returns True if all victims are in 'treated' state, else False.
    """
    for victim, data in state.victims.items():
        if data['state'] != "treated":
            print(f"Victim {victim} is not treated")
            return False
    return True

pyhop.declare_methods('treat_all_victims', treat_all_victims)
pyhop.declare_methods('do_step', do_step)
pyhop.declare_methods('handle_goal_completion', handle_goal_completion)
pyhop.declare_methods('assign_goals', assign_goals)
pyhop.declare_methods('all_victims_treated', all_victims_treated)


# ------------------------------------------------------------------------------------
# Example Usage
# ------------------------------------------------------------------------------------
goal = [('treat_all_victims',)]
pyhop.pyhop(state4, goal, verbose=3)
