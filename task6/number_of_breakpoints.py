#! /usr/bin/env python3


def num_breakpoints(permutation):
    num_adjacencies = 0
    old_permutation_length = len(permutation)
    permutation = [0] + permutation + [old_permutation_length + 1]
    for i in range(len(permutation)):
        if i + 1 < len(permutation):
            if permutation[i + 1] == permutation[i] + 1:
                num_adjacencies += 1
    return old_permutation_length + 1 - num_adjacencies


def main():
    input_permutation = list(map(int, input().strip()[1:-1].split()))
    print(num_breakpoints(input_permutation))


if __name__ == "__main__":
    main()
