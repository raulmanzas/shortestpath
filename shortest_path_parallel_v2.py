#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import yaml
import math
from mpi4py import MPI

def find_shortest_path(graph):
    """
    Computes the shortest path to each node in every level of the graph.
    """
    # MPI infra
    comm = MPI.COMM_WORLD
    num_processes = comm.Get_size()
    rank = comm.Get_rank()
    
    levels = 0
    nodes = 0
    distances = {}
    weights = {}
    
    # Data distribution
    if(rank == 0):
        levels, nodes, distances, weights = parse_graph_repr(graph)
        start_time = MPI.Wtime()
    levels, nodes, distances, weights = comm.bcast([levels, nodes, distances, weights])
    
    # Computes which range of nodes each process is going to use
    nodes_per_process = math.ceil(nodes/num_processes)
    node_offset = nodes_per_process * rank
    nodes_to_compute = range(node_offset, node_offset + nodes_per_process)
    # Computing the shortest path for every level
    for level in range(2, levels + 2):
        distances[level] = {}
        for next_level_node in nodes_to_compute:
            local_distances = []
            for node in range(0, nodes - 1):
                dist = distances[level - 1][node] + weights[level - 1][node][next_level_node]
                local_distances.append(dist)
            distances[level][next_level_node] = min(local_distances)
        
        distances[level] = comm.gather(distances[level])
        if rank == 0:
            distances[level] = { k:v[k] for v in distances[level] for k in v}
        distances[level] = comm.bcast(distances[level], root = 0)
    if rank == 0:
        end_time = MPI.Wtime()
        print(end_time - start_time)
    #     for level in range(2, levels + 2):
    #         print("Level {0}: {1}".format(level, distances[level]))

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