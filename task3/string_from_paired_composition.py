#! /usr/bin/env python3


class Node:

    def __init__(self, data):
        self.data = data
        self.children = []
        self.parents = []

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parents.append(parent)

    def delete_child(self, child):
        self.children.remove(child)

    def __repr__(self):
        return str(self.data)


def has_eulerian_cycle_or_path(graph):
    odd_nodes = []
    for node in graph:
        if len(node.children) != len(node.parents):
            odd_nodes.append(node)
    start = graph[0]
    if len(odd_nodes) == 0:
        return True, True, start
    if len(odd_nodes) != 2:
        return False, False, start
    first, second = odd_nodes
    if len(first.children) < len(first.parents):
        first.add_child(second)
        start = second
    else:
        second.add_child(first)
        start = first
    return False, True, start


def find_eulerian_cycle_or_path(graph):
    has_cycle, has_path, start = has_eulerian_cycle_or_path(graph)
    if not (has_cycle or has_path):
        return None
    path = []
    current_path = []
    start_node = start
    while True:
        current_node = start_node
        temp_current_path = [current_node]
        while current_node.children != []:
            child = current_node.children[0]
            temp_current_path.append(child)
            current_node.delete_child(child)
            current_node = child
        current_path = temp_current_path + current_path
        all_visited = True
        for idx, node in enumerate(current_path):
            if node.children == []:
                path.append(node)
            else:
                current_path = current_path[idx + 1:]
                all_visited = False
                start_node = node
                break
        if all_visited:
            break
    if has_path and not has_cycle:
        path = path[:-1]
    return path


def build_graph_from_k_mer_pairs(k_mer_pairs):
    if k_mer_pairs == []:
        return []
    nodes = dict()
    for first_k_mer, second_k_mer in k_mer_pairs:
        prefix_pair = (first_k_mer[:-1], second_k_mer[:-1])
        suffix_pair = (first_k_mer[1:], second_k_mer[1:])
        if prefix_pair not in nodes:
            nodes[prefix_pair] = Node(prefix_pair)
        if suffix_pair not in nodes:
            nodes[suffix_pair] = Node(suffix_pair)
        nodes[prefix_pair].add_child(nodes[suffix_pair])
        nodes[suffix_pair].add_parent(nodes[prefix_pair])

    return list(nodes.values())


def reconstruct_string_from_path(path, d, k):
    if path == []:
        return ""
    prefix_string, suffix_string = path[0].data
    for node in path[1:]:
        prefix_string += node.data[0][-1]
        suffix_string += node.data[1][-1]
    return prefix_string + suffix_string[-d - k:]


def main():
    k, d = list(map(int, input().split()))
    k_mer_pairs = []
    while(True):
        try:
            line = input()
            if (line == ""):
                break
            k_mer_pair = line.split("|")
            k_mer_pairs.append(k_mer_pair)
        except EOFError:
            break
    graph = build_graph_from_k_mer_pairs(k_mer_pairs)
    path = find_eulerian_cycle_or_path(graph)
    if path is None:
        print("Graph is not eulerian.")
        return
    print(reconstruct_string_from_path(path, d, k))


if __name__ == "__main__":
    main()
