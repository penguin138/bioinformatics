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


def build_graph_from_k_mers(k_mers):
    if k_mers == []:
        return []
    k_mer_nodes = dict()
    for k_mer in k_mers:
        if k_mer[1:] not in k_mer_nodes:
            k_mer_nodes[k_mer[1:]] = Node(k_mer[1:])
        if k_mer[:-1] not in k_mer_nodes:
            k_mer_nodes[k_mer[:-1]] = Node(k_mer[:-1])
        k_mer_nodes[k_mer[:-1]].add_child(k_mer_nodes[k_mer[1:]])
        k_mer_nodes[k_mer[1:]].add_parent(k_mer_nodes[k_mer[:-1]])

    return list(k_mer_nodes.values())


def reconstruct_string_from_path(path):
    if path == []:
        return ""
    string_ = path[0].data
    for node in path[1:]:
        string_ += node.data[-1]
    return string_


def main():
    k = int(input())
    k_mers = []
    while(True):
        try:
            k_mer = input()
            if (k_mer == ""):
                break
            k_mers.append(k_mer)
        except EOFError:
            break
    graph = build_graph_from_k_mers(k_mers)
    path = find_eulerian_cycle_or_path(graph)
    if path is None:
        print("Graph is not eulerian.")
        return
    print(reconstruct_string_from_path(path))


if __name__ == "__main__":
    main()
