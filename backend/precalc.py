import pandas as pd
import numpy as np
import networkx as nx
import pickle
import heapq
from math import radians, sin, cos, sqrt, atan2

# Load graph
with open(r'C:\Users\Aditya\OneDrive\Desktop\hack\RouteSyncAI\Ter\backend\graph_final_8_precalc.pkl', "rb") as G:
    roadsn = pickle.load(G)

# Transportation mode benchmarks (more realistic values)
MODE_SPEED = {
    'air': 800,      # km/h
    'sea': 35,       # km/h
    'land': 70       # km/h
}

MODE_COST = {
    'air': 0.5,      # $ per km
    'sea': 0.1,      # $ per km
    'land': 0.25     # $ per km
}

# Recalculate times and prices based on more accurate benchmarks
for u, v, data in roadsn.edges(data=True):
    mode = data.get('mode', 'land')  # Default to land if mode is missing
    distance = data.get('distance', 0)
    
    # Calculate more realistic time based on mode and distance
    if mode in MODE_SPEED:
        # Convert to hours and add small delay for shorter segments
        data['time'] = distance / MODE_SPEED[mode] + 0.5
    else:
        # Fallback calculation
        data['time'] = distance / 70 + 0.5
    
    # Calculate more realistic price based on mode and distance
    if mode in MODE_COST:
        # Base cost plus distance-based cost
        data['price'] = 10 + distance * MODE_COST[mode]
    else:
        # Fallback calculation
        data['price'] = 10 + distance * 0.25

# Collect updated time and price values
time_list = []
price_list = []
for u, v, data in roadsn.edges(data=True):
    time_list.append(data['time'])
    price_list.append(data['price'])

time_array = np.array(time_list)
price_array = np.array(price_list)

# Compute min and max for each attribute
time_min, time_max = time_array.min(), time_array.max()
price_min, price_max = price_array.min(), price_array.max()

# Add normalized values to edges
for u, v, data in roadsn.edges(data=True):
    data['time_norm'] = (data['time'] - time_min) / (time_max - time_min) * 100
    data['price_norm'] = (data['price'] - price_min) / (price_max - price_min) * 100

# Print statistics for verification
print(f"Time range: {time_min:.2f} to {time_max:.2f} hours")
print(f"Price range: ${price_min:.2f} to ${price_max:.2f}")

# Add additional edge attribute for routing optimization
for u, v, data in roadsn.edges(data=True):
    # Calculate a weighted efficiency score (lower is better)
    data['efficiency'] = (data['time_norm'] * 0.5) + (data['price_norm'] * 0.5)

# Save updated graph with corrected calculations
with open(r'C:\Users\Aditya\OneDrive\Desktop\hack\RouteSyncAI\Ter\backend\graph_final_8_precalc.pkl', "wb") as G:
    pickle.dump(roadsn, G)

print("Graph updated with more accurate time and cost calculations.")


