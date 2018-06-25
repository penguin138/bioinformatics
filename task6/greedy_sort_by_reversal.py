#! /usr/bin/env python3
import numpy as np


def find_next_permutation_value(permutation, i):
    try:
        return list(permutation[i:]).index(i + 1) + i
    except ValueError:
        return list(permutation[i:]).index(-i - 1) + i


def sort_by_reversal(permutation):
    for i in range(0, len(permutation)):
        idx = find_next_permutation_value(permutation, i)
        if idx != i:
            permutation[i:idx + 1] = (-1) * permutation[i:idx + 1][::-1]
            yield permutation
        if permutation[i] != (i + 1):
            permutation[i] *= -1
            yield permutation


def print_permutation(permutation):
    print("(" + " ".join(map(lambda x: "%+d" % x, permutation)) + ")")


def main():
    input_permutation = np.array(list(map(int, input().strip()[1:-1].split())))
    for permutation in sort_by_reversal(input_permutation):
        print_permutation(permutation)


if __name__ == "__main__":
    main()
