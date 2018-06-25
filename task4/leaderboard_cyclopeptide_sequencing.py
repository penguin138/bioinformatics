#! /usr/bin/env python3
from collections import Counter

amino_acid_masses = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115,
                     128, 129, 131, 137, 147, 156, 163, 186]


def extend_peptides(peptides):
    new_peptides = set()
    for peptide in peptides:
        for amino_acid_mass in amino_acid_masses:
            new_peptides.add(peptide + (amino_acid_mass,))
    return new_peptides


def theoretical_spectrum(peptide):
    spectrum = set([0])
    double_peptide = peptide
    double_peptide += peptide
    peptide_length = len(peptide)
    for i in range(peptide_length):
        for j in range(1, peptide_length):
            spectrum.add(sum(double_peptide[i: i + j]))
    spectrum.add(sum(peptide))
    return spectrum


def mass(peptide):
    total = 0
    for mass in peptide:
        total += mass
    return total


def score(peptide_spectrum, spectrum):
    return len(peptide_spectrum & spectrum)


def cut(leaderboard, scores, spectrum, n):
    sorted_leaderboard = sorted(leaderboard, key=lambda x: -scores[x])
    cut_leaderboard = set()
    last_item = None
    for idx, item in enumerate(sorted_leaderboard):
        if idx >= n and item != last_item:
            break
        cut_leaderboard.add(item)
        last_item = item
    return cut_leaderboard


def find_cyclopeptide(spectrum, n):
    leaderboard = set([()])
    parent_mass = max(spectrum)
    leader_score = 1
    leader_peptide = ()
    while leaderboard:
        leaderboard = extend_peptides(leaderboard)
        old_leaderboard = set(leaderboard)
        scores = dict()
        for peptide in old_leaderboard:
            peptide_spectrum = theoretical_spectrum(peptide)
            scores[peptide] = score(peptide_spectrum, spectrum)
            peptide_mass = mass(peptide)
            if peptide_mass == parent_mass:
                if scores[peptide] >= leader_score:
                    leader_peptide = peptide
                    leader_score = scores[peptide]
            elif peptide_mass > parent_mass:
                leaderboard.remove(peptide)
        leaderboard = cut(leaderboard, scores, spectrum, n)
    return leader_peptide


def main():
    n = int(input())
    spectrum = set((map(int, input().split())))
    print("-".join(map(str, find_cyclopeptide(spectrum, n))))


if __name__ == "__main__":
    main()
