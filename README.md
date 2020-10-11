# Fire station placement

Formulate a linear integer problem and solve using [Gurobi optimizer](https://www.gurobi.com/products/gurobi-optimizer/)

Honors option for CSE 440: Artificial Intelligence

## Problem
A city is reviewing the location of its fire stations. The city is made up of a number of neighborhoods.
A fire station can be placed in any neighborhood. It is able to handle the fires for both its
neighborhood and any adjacent neighborhood (any neighborhood with a non-zero border with its home neighborhood).

The objective is to minimize the number of fire stations used. We are asked to find a set of such subsets of 
neighborhoods that covers the set of all neighborhoods in the sense that every neighborhood appears in the service 
subset associated with at least one fire station. We want to formulate this problem as an integer linear program 
and solve it in python using the an underlying solver. We want to use Gurobi as the underlying solver.

## Files
* cities.json - represent cities and physical connections between them
* honors.py - script to solve problem using Gurobi
* output.txt - print results
* output.png - plot results showing connections between stations
