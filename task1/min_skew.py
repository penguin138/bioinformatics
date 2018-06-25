#! /usr/bin/env python3


def find_min_skew(genome):
    cumulative_skew = 0
    min_skew = 0
    cumulative_skews = [0]
    for symbol in genome:
        if symbol == "C":
            cumulative_skew -= 1
        elif symbol == "G":
            cumulative_skew += 1
        cumulative_skews.append(cumulative_skew)
        if cumulative_skew < min_skew:
            min_skew = cumulative_skew
    min_skew_indices = []
    for idx, skew in enumerate(cumulative_skews):
        if skew == min_skew:
            min_skew_indices.append(idx)
    return min_skew_indices


def main():
    genome = input()
    min_skew_indices = find_min_skew(genome)
    print(" ".join(map(str, min_skew_indices)))


if __name__ == "__main__":
    main()
