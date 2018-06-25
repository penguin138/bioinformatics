#! /usr/bin/env python3
from collections import defaultdict
import sys
import itertools


def build_graph(first_genome, second_genome):
    node_to_synteny_block = dict()
    synteny_block_to_nodes = dict()
    adjacency_lists = defaultdict(list)
    last_node = -1
    for cycle in first_genome:
        for signed_synteny_block in cycle:
            synteny_block = abs(signed_synteny_block)
            if synteny_block not in synteny_block_to_nodes:
                start_node = last_node + 1
                end_node = last_node + 2
                synteny_block_to_nodes[synteny_block] = (start_node, end_node)
                node_to_synteny_block[start_node] = synteny_block
                node_to_synteny_block[end_node] = synteny_block
                last_node = end_node
    for cycle in itertools.chain(first_genome, second_genome):
        start, end = synteny_block_to_nodes[abs(cycle[0])]
        prev_node = end if cycle[0] > 0 else start
        extended_cycle = cycle[1:] + [cycle[0]]
        for current_block in extended_cycle:
            start, end = synteny_block_to_nodes[abs(current_block)]
            current_node = start if current_block > 0 else end
            adjacency_lists[current_node].append(prev_node)
            adjacency_lists[prev_node].append(current_node)
            prev_node = start if current_node == end else end
    num_synteny_blocks = len(synteny_block_to_nodes)
    return adjacency_lists, num_synteny_blocks


def dfs(node, adjacency_lists, visited):
    visited.add(node)
    for child in adjacency_lists[node]:
        if child not in visited:
            dfs(child, adjacency_lists, visited)


def parse_genome(str):
    tokens = str.split(")(")
    tokens[0] = tokens[0][1:]
    tokens[-1] = tokens[-1][:-1]
    genome = []
    for token in tokens:
        genome.append(list(map(int, token.split())))
    return genome


def main():
    first_genome = parse_genome(input())
    second_genome = parse_genome(input())
    adjacency_lists, num_blocks = build_graph(first_genome, second_genome)
    visited = set()
    num_cycles = 0
    sys.setrecursionlimit(2 * num_blocks)
    for node in adjacency_lists:
        if node not in visited:
            dfs(node, adjacency_lists, visited)
            num_cycles += 1
    print(num_blocks - num_cycles)


if __name__ == "__main__":
    main()
