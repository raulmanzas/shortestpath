#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import yaml
from mpi4py import MPI

def find_shortest_path(graph):
    """
    Computes the shortest path to each node in every level of the graph.
    """
    levels = 0
    nodes = 0
    distances = {}
    weights = {}

    comm = MPI.COMM_WORLD
    # this implementation assumes the number of processes to be equal the number of nodes in a level + 1
    num_processes = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        levels, nodes, distances, weights = parse_graph_repr(graph)
        for level in range(2, levels + 1):
            for next_level_node in range(0, nodes):
                destination = next_level_node + 1
                comm.send(distances[level - 1], dest = destination)
                comm.send(weights[level - 1], dest = destination)
                comm.send(next_level_node, dest = destination)
    else:
        distances = comm.recv(source = 0)
        weights = comm.recv(source = 0)
        next_level_node = comm.recv(source = 0)
        # data distribution between processes works fine
        local_distances = []
        for node in range(0, len(distances)):
            dist = distances[node] + weights[node][next_level_node]
            local_distances.append(dist)
        
        
        print('I am process ' + str(rank) + ' and I received node ' + str(next_level_node))
        print('Distances: ')
        print(weights)


    # for level in range(2, levels + 1):
    #     distances[level] = []
    #     # main process needs to send a copy of distances array and weights matrix to 'worker processes'
    #     for next_level_node in range(0, nodes):
    #         node_distances = [] # local in each process
    #         for current_level_node in range(0, nodes):
    #             # only the copy in this level should be sent to worker processes to save memory and comm time
    #             distance = weights[level][current_level_node][next_level_node] + distances[level - 1][current_level_node]
    #             node_distances.append(distance)
    #         # after calculating all distances, find the smallest one and send to main process
    #         shortest_path = min(node_distances)
    #         distances[level].append(shortest_path)
    
    # print(distances)



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
        print('You must pass an graph\' yaml representation')