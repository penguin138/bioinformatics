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
    nodes = []
    while(True):
        try:
            line = input()
            if (line == ""):
                break
            k_mer_pair = line.split("|")
            nodes.append(Node(k_mer_pair))
        except EOFError:
            break
    print(reconstruct_string_from_path(nodes, d, k))


if __name__ == "__main__":
    main()
