#! /usr/bin/env python3
from itertools import combinations, product
from collections import defaultdict


def complement(pattern):
    complement = {"A": "T", "G": "C", "T": "A", "C": "G"}
    new_pattern = ""
    for symbol in pattern:
        new_pattern += complement[symbol]
    return new_pattern


def reverse_complement(pattern):
    return complement("".join(reversed(pattern)))


def pattern_alterations(pattern, tolerance, alphabet):
    alterations = set([pattern])
    for num_alterations in range(1, tolerance + 1):
        for altered_indices in combinations(range(len(pattern)), num_alterations):
            for new_symbols in product(alphabet, repeat=num_alterations):
                new_pattern = list(pattern)
                for idx, symbol in zip(altered_indices, new_symbols):
                    new_pattern[idx] = symbol
                new_pattern = "".join(new_pattern)
                alterations.add(new_pattern)
    return alterations


def find_most_frequent_patterns(genome, pattern_length, tolerance):
    counter = defaultdict(int)
    for i in range(len(genome)):
        if i + pattern_length - 1 < len(genome):
            for new_pattern in pattern_alterations(genome[i: i + pattern_length],
                                                   tolerance, ["A", "T", "G", "C"]):
                counter[new_pattern] += 1
            for new_pattern in pattern_alterations(
                reverse_complement(genome[i: i + pattern_length]), tolerance,
                    ["A", "T", "G", "C"]):
                counter[new_pattern] += 1
    max_count = 0
    for pattern in counter:
        if counter[pattern] > max_count:
            max_count = counter[pattern]
    patterns = []
    for pattern in counter:
        if counter[pattern] == max_count:
            patterns.append(pattern)
    return patterns


def main():
    genome = input()
    pattern_length, tolerance = list(map(int, input().split()))
    patterns = find_most_frequent_patterns(genome, pattern_length, tolerance)
    print(" ".join(patterns))


if __name__ == "__main__":
    main()
