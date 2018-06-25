#! /usr/bin/env python3
from collections import defaultdict


def find_clumps(genome, l, k, t):
    counter = defaultdict(lambda: defaultdict(int))
    for i in range(len(genome)):
        if i + l - 1 < len(genome):
            for j in range(i, i + l):
                if j + k < i + l + 1:
                    region = genome[i: i + l]
                    pattern = genome[j: j + k]
                    counter[region][pattern] += 1
    clumps = [pattern for region in counter
              for pattern in counter[region] if counter[region][pattern] >= t]
    return set(clumps)


def main():
    genome = input()
    k, l, t = list(map(int, input().split()))
    print(" ".join(find_clumps(genome, l, k, t)))


if __name__ == "__main__":
    main()
