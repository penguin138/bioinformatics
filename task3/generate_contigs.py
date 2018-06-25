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


def traverse_nonbranching_path(node):
    # assuming that graph is not eulerian
    path = []
    while len(node.children) == 1 and len(node.parents) == 1:
        path.append(node)
        node = node.children[0]
    path.append(node)
    return path


def find_contigs(graph):
    # assuming that graph is not eulerian
    contigs = []
    for node in graph:
        contig = []
        if len(node.children) > 0 and not (len(node.parents) == 1 and len(node.children) == 1):
            for child in node.children:
                contig = [node]
                path = traverse_nonbranching_path(child)
                contig.extend(path)
                contigs.append(contig)
    return contigs


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
    contigs = find_contigs(graph)
    print(" ".join(map(reconstruct_string_from_path, contigs)))


if __name__ == "__main__":
    main()
