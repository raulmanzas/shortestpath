# Shortest Path on Single Source Weighted Multi-level Graph

This repository presents three implementations for solving the problem of finding the shortest path on a single source weighted multi-level graph. Both parallel versions were implemented using MPI. All implementations were heavily based in [this paper](http://ieeexplore.ieee.org/document/5403295/).

### Graph Representation

All implementations work with a graph's yaml representation containing the number of levels, number of nodes per level and all distances between nodes from one level to the next. [Here is an example on how to manually define your graph in the yaml representation](https://github.com/raulmanzas/shortestpath/blob/master/graphs/small.yaml). You can also generate a representation of a random generated graph for testing purposes by using the [graph generator](https://github.com/raulmanzas/shortestpath/blob/master/tools/graph_generator.py).

### Parallel implementations

There are two parallel implementations:

* [The first implementation](https://github.com/raulmanzas/shortestpath/blob/master/shortest_path_parallel_v1.py) defines a master-slave relationship amongst the processes, in which the master is responsible for coordinating data distribution and  process synchronization. This behaviour requires p + 1 processes, as the master does not work directly in path computation.

* [The alternative version](https://github.com/raulmanzas/shortestpath/blob/master/shortest_path_parallel_v2.py) considers each process to be able to compute it's own share of input data. Therefore, the algorithm runs without any master, optimizing resource usage and reducing the comunication overhead and using MPI's collective communication functionality, the processes are able to synchronize whenever it is necessary.

### Execution

Before running the commands bellow, please install mpi4py and python3.

#### Graph generator

`$ python3 graph_generator.py --levels 10 --nodes 10 --name 'test.yaml'`

#### Sequential

`$ python3 shortest_path.py --graph graphs/small.yaml `

#### Both parallel versions

`$ mpiexec -np 2 python3 shortest_path_parallel_v1.py --graph graphs/small.yaml`

Make sure to limit the number of processes between 1 and the number of nodes per level.
