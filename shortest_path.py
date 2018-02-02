#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import yaml

def find_shortest_path(graph):
    """
    Computes the shortest path to each node in every level of the graph.
    """
    levels, nodes, distances, weights = parse_graph_repr(graph)
    for level in range(2, levels + 2):
        distances[level] = [0] * nodes
        for next_level_node in range(0, nodes):
            local_distances = []
            for node in range(0, nodes - 1):
                dist = distances[level - 1][node] + weights[level - 1][node][next_level_node]
                local_distances.append(dist)
            distances[level][next_level_node] = min(local_distances)
    print(distances)

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