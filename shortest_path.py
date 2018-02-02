#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import yaml
from mpi4py import MPI

DISTANCES = 1
WEIGHTS = 2
NODE = 3

def find_shortest_path(graph):
    """
    Computes the shortest path to each node in every level of the graph.
    """
    comm = MPI.COMM_WORLD
    # this implementation assumes the number of processes to be equal the 
    # number of nodes in a level + 1
    num_processes = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        levels, nodes, distances, weights = parse_graph_repr(graph)
        for level in range(2, levels + 1):
            # initializes the distance array for this level
            distances[level] = [0] * nodes
            for next_level_node in range(0, nodes):
                destination = next_level_node + 1
                comm.send(distances[level - 1], dest = destination, tag = DISTANCES)
                comm.send(weights[level - 1], dest = destination, tag = WEIGHTS)
                comm.send(next_level_node, dest = destination, tag = NODE)
            
            for next_level_node in range(0, nodes):
                shortest_path = comm.recv(source = next_level_node + 1)
                distances[level][next_level_node] = shortest_path
    else:
        # Receives from master process all data needed to find the shortest path
        # to node next_level_node
        distances = comm.recv(source = 0, tag = DISTANCES)
        weights = comm.recv(source = 0, tag = WEIGHTS)
        next_level_node = comm.recv(source = 0, tag = NODE)
        local_distances = []

        for node in range(0, num_processes - 1):
            dist = distances[node] + weights[node][next_level_node]
            local_distances.append(dist)
        
        # Computes the shorstest path to next_level_node and sends it back
        comm.send(min(local_distances), 0)

def parse_graph_repr(path):
    with open(path, 'r') as file:
        representation = yaml.load(file)
    levels = representation['Levels']
    nodes = representation['NodesPerLevel']
    source_dist = representation['SourceDistances']
    weights = representation['Weights']
    dist = {}
    dist[1] = source_dist
    return levels, nodes, dist, weights

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', help='yaml graph representation')
    args = parser.parse_args()
    if args:
        find_shortest_path(args.graph)
    else:
        print('You must pass an graph\'s yaml representation')