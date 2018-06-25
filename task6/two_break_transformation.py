#! /usr/bin/env python3
from collections import defaultdict
import sys


def build_graph(first_genome, second_genome):
    node_to_synteny_block = dict()
    synteny_block_to_nodes = dict()
    blue_edges = set()
    red_edges = set()
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

    def add_genome_edges(genome, color):
        for cycle in genome:
            start, end = synteny_block_to_nodes[abs(cycle[0])]
            prev_node = end if cycle[0] > 0 else start
            extended_cycle = cycle[1:] + [cycle[0]]
            for current_block in extended_cycle:
                start, end = synteny_block_to_nodes[abs(current_block)]
                current_node = start if current_block > 0 else end
                adjacency_lists[current_node].append(prev_node)
                adjacency_lists[prev_node].append(current_node)
                if color == "red":
                    red_edges.add((prev_node, current_node))
                    red_edges.add((current_node, prev_node))
                else:
                    blue_edges.add((current_node, prev_node))
                    blue_edges.add((prev_node, current_node))
                prev_node = start if current_node == end else end

    add_genome_edges(first_genome, "red")
    add_genome_edges(second_genome, "blue")
    return adjacency_lists, red_edges, blue_edges, synteny_block_to_nodes, node_to_synteny_block


def dfs(node, adjacency_lists, visited, cycle):
    visited.add(node)
    cycle.append(node)
    for child in adjacency_lists[node]:
        if child not in visited:
            dfs(child, adjacency_lists, visited, cycle)


def print_genome(genome):
    genome_str = ""
    for cycle in genome:
        genome_str += "(" + " ".join(map(lambda x: "%+d" % x, cycle)) + ")"
    print(genome_str)


def parse_genome(str):
    tokens = str.split(")(")
    tokens[0] = tokens[0][1:]
    tokens[-1] = tokens[-1][:-1]
    genome = []
    for token in tokens:
        genome.append(list(map(int, token.split())))
    return genome


def node_is_end_of_synteny_block(node, node_to_synteny_block, synteny_block_to_nodes):
    synteny_block = node_to_synteny_block[node]
    start, end = synteny_block_to_nodes[synteny_block]
    return node == end


def traverse_black_edge(node, node_to_synteny_block, synteny_block_to_nodes):
    synteny_block = node_to_synteny_block[node]
    start, end = synteny_block_to_nodes[synteny_block]
    if node_is_end_of_synteny_block(node, node_to_synteny_block, synteny_block_to_nodes):
        synteny_block *= -1
        next_node = start
    else:
        next_node = end
    return next_node, synteny_block


def traverse_red_edge(node, adjacency_lists, red_edges, visited):
    for adj_node in adjacency_lists[node]:
        if (node, adj_node) in red_edges:
            if adj_node not in visited:
                return adj_node


def genome_from_graph(adjacency_lists,
                      synteny_block_to_nodes,
                      node_to_synteny_block,
                      red_edges):
    visited = set()
    genome = []
    for start_node in adjacency_lists:
        if start_node not in visited:
            genome_cycle = []
            prev_color = "red"
            current_node = start_node
            while(True):
                visited.add(current_node)
                if prev_color == "red":
                    current_node, synteny_block = traverse_black_edge(
                        current_node, node_to_synteny_block, synteny_block_to_nodes)
                    if current_node in visited:
                        break
                    prev_color = "black"
                    genome_cycle.append(synteny_block)
                else:
                    current_node = traverse_red_edge(current_node, adjacency_lists,
                                                     red_edges, visited)
                    if current_node is None:
                        break
                    prev_color = "red"
            genome.append(genome_cycle)
    return genome


def find_cycle_longer_than(adjacency_lists, num_vertices):
    visited = set()
    for node in adjacency_lists:
        if node not in visited:
            cycle = []
            dfs(node, adjacency_lists, visited, cycle)
            if len(cycle) > num_vertices:
                return cycle


def add_edge(adjacency_lists, red_edges, blue_edges, edge, color):
    start, end = edge
    adjacency_lists[start].append(end)
    adjacency_lists[end].append(start)
    if color == "red":
        red_edges.add((start, end))
        red_edges.add((end, start))
    else:
        blue_edges.add((start, end))
        blue_edges.add((end, start))


def remove_edge(adjacency_lists, edges, edge):
    start, end = edge
    adjacency_lists[start].remove(end)
    adjacency_lists[end].remove(start)
    edges.remove((start, end))
    edges.remove((end, start))


def main():
    first_genome = parse_genome(input())
    second_genome = parse_genome(input())
    (adjacency_lists, red_edges, blue_edges,
     synteny_block_to_nodes, node_to_synteny_block) = build_graph(first_genome,
                                                                  second_genome)
    sys.setrecursionlimit(100000)
    current_genome = genome_from_graph(adjacency_lists, synteny_block_to_nodes,
                                       node_to_synteny_block, red_edges)
    print_genome(current_genome)
    while(True):
        cycle = find_cycle_longer_than(adjacency_lists, 2)
        if cycle is None:
            break
        red_edge = (cycle[0], cycle[1])
        second_red_edge = (cycle[2], cycle[3])
        if red_edge not in red_edges:
            red_edge = (cycle[1], cycle[2])
            if len(cycle) > 4:
                second_red_edge = (cycle[3], cycle[4])
            else:
                second_red_edge = (cycle[3], cycle[0])
        remove_edge(adjacency_lists, red_edges, red_edge)
        remove_edge(adjacency_lists, red_edges, second_red_edge)
        add_edge(adjacency_lists, red_edges, blue_edges, (red_edge[0], second_red_edge[1]), "red")
        add_edge(adjacency_lists, red_edges, blue_edges, (red_edge[1], second_red_edge[0]), "red")
        current_genome = genome_from_graph(adjacency_lists, synteny_block_to_nodes,
                                           node_to_synteny_block, red_edges)
        print_genome(current_genome)


if __name__ == "__main__":
    main()
