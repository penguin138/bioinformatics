#! /usr/bin/env python3


def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        return None
    distance = 0
    for symbol1, symbol2 in zip(str1, str2):
        if symbol1 != symbol2:
            distance += 1
    return distance


def find_matches(pattern, genome, tolerance):
    pattern_length = len(pattern)
    indices = []
    for i in range(len(genome)):
        if (i + pattern_length - 1 < len(genome) and
                hamming_distance(genome[i: i + pattern_length], pattern) <= tolerance):
            indices.append(i)
    return indices


def main():
    pattern = input()
    genome = input()
    tolerance = int(input())
    indices = find_matches(pattern, genome, tolerance)
    print(" ".join(map(str, indices)))


if __name__ == "__main__":
    main()
