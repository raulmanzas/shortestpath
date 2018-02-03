#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import yaml
import random

RANDOM_MAX = 200

def generate_graph_representation(levels, nodes, file_name):
    representation = "Levels: {0}\nNodesPerLevel: {1}\n".format(levels, nodes)
    representation += "SourceDistances:\n"
    for node in range(0, nodes):
        value = random.randint(1, RANDOM_MAX)
        representation += "  - {0}\n".format(value)
    
    representation += "Weights:\n"
    for level in range(0, levels):
        representation += "  {0}:\n    -\n".format(level + 1)
        for node in range(0, nodes):
            value = random.randint(1, RANDOM_MAX)
            representation += "      - {0}\n".format(value)
    
    with open(file_name, 'w') as file:
        file.write(representation)
    print("Done!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--levels', help='Number of levels')
    parser.add_argument('--nodes', help='Number of nodes per level')
    parser.add_argument('--name', help='Graph\'s representation name')
    args = parser.parse_args()
    if args:
        levels = int(args.levels)
        nodes = int(args.nodes)
        file_name = args.name
        generate_graph_representation(levels, nodes, file_name)
    else:
        print('You must pass levels, nodes and file name')