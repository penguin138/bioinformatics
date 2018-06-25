#! /usr/bin/env python3


def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        return None
    distance = 0
    for symbol1, symbol2 in zip(str1, str2):
        if symbol1 != symbol2:
            distance += 1
    return distance


def distance_between_pattern_and_strings(pattern, dna):
    distance = 0
    k = len(pattern)
    for text in dna:
        min_hamming_distance = hamming_distance(pattern, text[:k])
        for i in range(len(text) - k + 1):
            current_hamming_distance = hamming_distance(pattern, text[i: i + k])
            if min_hamming_distance > current_hamming_distance:
                min_hamming_distance = current_hamming_distance
        distance += min_hamming_distance
    return distance


def main():
    pattern = input()
    dna = input().split()
    print(distance_between_pattern_and_strings(pattern, dna))


if __name__ == "__main__":
    main()
