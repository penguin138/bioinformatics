#! /usr/bin/env python3
import numpy as np


def profile(motifs):
    profile = np.ones((4, len(motifs[0])))
    for motif in motifs:
        for idx, symbol in enumerate(motif):
            symbol_idx = "ATGC".index(symbol)
            profile[symbol_idx, idx] += 1 / (2 * len(motifs))
    return profile


def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        return None
    distance = 0
    for symbol1, symbol2 in zip(str1, str2):
        if symbol1 != symbol2:
            distance += 1
    return distance


def k_mer_probability(k_mer, profile):
    probability = 1
    for idx, symbol in enumerate(k_mer):
        symbol_idx = "ATGC".index(symbol)
        probability *= profile[symbol_idx, idx]
    return probability


def profile_most_probable_k_mer(dna_str, profile, k):
    most_probable_k_mer = dna_str[:k]
    highest_probability = k_mer_probability(most_probable_k_mer, profile)
    for i in range(len(dna_str) - k + 1):
        k_mer = dna_str[i: i + k]
        prob = k_mer_probability(k_mer, profile)
        if prob > highest_probability:
            highest_probability = prob
            most_probable_k_mer = k_mer
    return most_probable_k_mer


def score(motifs):
    profile_ = profile(motifs)
    symbols = "ATGC"
    consensus_string = "".join(map(lambda x: symbols[x], np.argmax(profile_, axis=0)))
    score = 0
    for motif in motifs:
        score += hamming_distance(motif, consensus_string)
    return score


def motifs(profile, dna, k):
    motifs = []
    for str_ in dna:
        motifs.append(profile_most_probable_k_mer(str_, profile, k))
    return motifs


def randomized_motif_search(dna, k, t):
    best_motifs = []
    for str_ in dna:
        start_idx = np.random.choice(len(str_) - k + 1)
        best_motifs.append(str_[start_idx: start_idx + k])
    best_score = score(best_motifs)
    current_motifs = best_motifs
    while True:
        profile_ = profile(current_motifs)
        current_motifs = motifs(profile_, dna, k)
        current_score = score(current_motifs)
        if current_score < best_score:
            best_score = current_score
            best_motifs = current_motifs
        else:
            return best_motifs


def main():
    k, t = list(map(int, input().split()))
    dna = []
    for i in range(t):
        dna.append(input())
    best_motifs = randomized_motif_search(dna, k, t)
    best_score = score(best_motifs)
    for i in range(999):
        motifs = randomized_motif_search(dna, k, t)
        current_score = score(motifs)
        if current_score < best_score:
            best_score = current_score
            best_motifs = motifs
    for motif in best_motifs:
        print(motif)


if __name__ == "__main__":
    main()
