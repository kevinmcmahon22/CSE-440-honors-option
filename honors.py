# CSE 440 Honors Project
# Kevin McMahon
# 12/4/19


# A city is reviewing the location of its fire stations. The city is made up of a number of neighborhoods.
# A fire station can be placed in any neighborhood. It is able to handle the fires for both its
# neighborhood and any adjacent neighborhood (any neighborhood with a non-zero border with its home neighborhood).

# The objective is to minimize the number of fire stations used. We are asked to find a set of such subsets of 
# neighborhoods that covers the set of all neighborhoods in the sense that every neighborhood appears in the service 
# subset associated with at least one fire station. We want to formulate this problem as an integer linear program 
# and solve it in python using the an underlying solver. We want to use Gurobi as the underlying solver.


# cities.json represents cities and physical connections between them
# python file takes json, creates gurobi model and optimizes it

import json
import networkx as nx
import matplotlib.pyplot as plt
from gurobipy import *

# Get data for problem
# Undirected graph, all edges are bidirectional 
fp = open('./cities.json')
cities = json.load(fp)

try:
    G = nx.Graph()
    city_to_var = {}
    m = Model("mip1")
    objective = LinExpr()

    for city in cities:
        city_str = f"city{city}"
        # add node to graph for each city
        G.add_node(city_str)

        # add variable, represents a city
        var = m.addVar(vtype = GRB.INTEGER, name = city_str)

        # add variable to linear expression, used in setting objective
        objective += var

        # add to city/var dict for adding constraints
        city_to_var[city_str] = var

    # add objective, minimize number of total stations
    m.setObjective(objective, GRB.MINIMIZE)

    # constraint_count = 1
    constraint_list = []
    for city in cities:
        for connected_city in cities[city]:
            city1_str = f"city{city}"
            city2_str = f"city{connected_city}"
            # add edges to graph
            G.add_edge(city1_str, city2_str)

            # get the gurobi variable for each city in edge
            # city1 = city_to_var[city1_str]
            # city2 = city_to_var[city2_str]

            # add constraint, each edge must have at least one city that contatins a station
            # m.addConstr(city1 + city2 == 1, f"c{constraint_count}")
            # constraint_count += 1
            
            # write constraints in a logical form rather than linear form 
            constraint_list.append(f"if {city1_str} then not {city2_str}")

    # create optimization model implicitly
    # add constraints to model from linear form in list
    for con in constraint_list:
        con_list = con.split()
        city1 = con_list[1]
        city2 = con_list[4]
        var1 = city_to_var[city1]
        var2 = city_to_var[city2]
        m.addConstr(var1 + var2 == 1, "con")

    m.optimize()

    print()
    for var in m.getVars():
        name = var.getAttr("VarName")
        value = var.getAttr("x")
        if value == 1.0:
            print(f"{name} Fire Station")
        else:
            print(f"{name}")
    print()

    # output graph for debugging purposes
    nx.draw(G, with_labels=True,font_weight='bold')
    plt.show()

except GurobiError as e:
    print(f"Error code {str(e.errno)}: {str(e)}")

except AttributeError:
    print('Encountered an attribute error')
