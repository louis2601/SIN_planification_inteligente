import math
import pyhop

state1 = pyhop.State('state1')
state1.cities_coordinates = {}
state1.cities_connection_trucks = {}
state1.cities_connection_foot_bus = {}
state1.drivers = {}
state1.trucks = {}
state1.busses = {}
state1.packages = {}
state1.bus_cost = 0.5
state1.bus_avg_speed = 60
state1.walk_speed = 5
state1.walk_savings = 0.5

def distance(c1, c2):
    x = pow(c1['X'] - c2['X'], 2)
    y = pow(c1['Y'] - c2['Y'], 2)
    return math.sqrt(x + y)

def calculate_bus_cost(state, city_from, city_to):
    base_rate = state.bus_cost
    distance = state.distance(city_from, city_to)
    return base_rate * distance

def calculate_bus_time(state, city_from, city_to):
    speed = state.bus_avg_speed
    distance = state.distance(city_from, city_to)
    return distance / speed

def calculate_walk_time(state, city_from, city_to):
    speed = state.walk_speed
    distance = state.distance(city_from, city_to)
    return distance / speed

def calculate_efficiency(bus_cost, bus_time, walk_time):
    bus_efficiency = bus_cost / bus_time
    walk_efficiency = walk_time * state1.walk_savings
    return bus_efficiency, walk_efficiency

def choose_transport(state, person, city_from, city_to):
    bus_cost = calculate_bus_cost(state, city_from, city_to)
    bus_time = calculate_bus_time(state, city_from, city_to)
    walk_time = calculate_walk_time(state, city_from, city_to)
    
    bus_efficiency, walk_efficiency = calculate_efficiency(bus_cost, bus_time, walk_time)
    
    if bus_cost > state.money[person]:
        return [('walk', person, city_from, city_to)]
    if bus_efficiency < walk_efficiency:
        return [('take_bus', person, city_from, city_to, bus_cost)]
    return [('walk', person, city_from, city_to)]

def take_bus(state, person, city_from, city_to, bus_cost):
    state.money[person] -= bus_cost
    state.location[person] = city_to
    return state

def walk(state, person, city_from, city_to):
    state.location[person] = city_to
    return state

def select_new_city(state, y):  # evaluation function
    x = state.car['location']
    best = inf  # big float
    for c in state.connection.keys():
        if c not in state.path and c in state.connection[x]:
            g = state.cost
            h = distance(state.coordinates[c], state.coordinates[y])
            if g +  h < best:
                best_city = c
                best = g + h
    return best_city

def travel_truck(state, goal):
    x = state.car['location']
    y = goal.final
    if x != y:
        z = select_new_city(state, y)
        g = pyhop.Goal('g')
        g.final = y
        return [('travel_op', z), ('travel_to_city', g)]
    return False