#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import yaml
import math
from mpi4py import MPI

# This algortihm assumes that the number of processes is limited
# in [2, number of nodes].

SYNC_LEVEL = 1

def find_shortest_path(graph):
    """
    Computes the shortest path to each node in every level of the graph.
    """
    comm = MPI.COMM_WORLD
    num_processes = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        levels, nodes, distances, weights = parse_graph_repr(graph)
        start_time = MPI.Wtime()
        # How many nodes each process receives
        nodes_per_proc = math.ceil(nodes/(num_processes - 1))
        for level in range(2, levels + 2):
            node_index = 0
            destination = 1
            while(node_index < nodes):
                nodes_to_compute = range(node_index, node_index + nodes_per_proc)
                message = [distances[level -1], weights[level - 1], nodes_to_compute]
                comm.send(True, dest = destination, tag = SYNC_LEVEL)
                comm.send(message, dest = destination)
                destination += 1
                node_index += nodes_per_proc
            
            distances[level] = []
            for worker_process in range(1, destination):
                shortest_paths = comm.recv(source = worker_process)
                for key in shortest_paths:
                    distances[level].append(shortest_paths[key])
        # Tells other processes to stop waiting for new tasks
        for node in range(1, num_processes):
            comm.send(False, dest = node, tag = SYNC_LEVEL)
        end_time = MPI.Wtime()
        print(end_time - start_time)
    else:
        # All process wait for requests from master process
        new_level = comm.recv(source = 0, tag = SYNC_LEVEL)
        while(new_level):
            # Receives from master process all data needed to find the shortest path
            # to node next_level_node
            message = comm.recv(source = 0)
            distances = message[0]
            weights = message[1]
            next_level_nodes = message[2]
            shortest_distances = {}
            for next_level_node in next_level_nodes:
                local_distances = []
                for node in range(0, len(weights[0])):
                    dist = distances[node] + weights[node][next_level_node]
                    local_distances.append(dist)
                shortest_distances[next_level_node] = min(local_distances)
            # Computes the shorstest path to next_level_node and sends it back
            comm.send(shortest_distances, dest = 0)
            new_level = comm.recv(source = 0, tag = SYNC_LEVEL)

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