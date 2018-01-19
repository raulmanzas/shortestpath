#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import yaml
from mpi4py import MPI

def find_shortest_path(graph):
    """
    Computes the shortest path to each node in every level of the graph.
    """
    levels, nodes, distances, weights = parse_graph_repr(graph)
    comm = MPI.COMM_WORLD

    for level in range(2, levels + 1):
        distances[level] = [];


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