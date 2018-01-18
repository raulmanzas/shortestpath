#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import yaml
from mpi4py import MPI

def find_shortest_path(graph):
    levels, nodes, source_dist, weights = parse_graph_repr(graph)
    

def parse_graph_repr(path):
    with open(path, 'r') as file:
        representation = yaml.load(file)
    levels = representation['Levels']
    nodes = representation['NodesPerLevel']
    source_dist = representation['SourceDistances']
    weights = representation['Weights']
    return levels, nodes, source_dist, weights

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', help='yaml graph representation')
    args = parser.parse_args()
    if args:
        find_shortest_path(args.graph)
    else:
        print('You must pass an graph\' yaml representation')