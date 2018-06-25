#! /usr/bin/env python3
from collections import defaultdict

amino_acid_masses = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115,
                     128, 129, 131, 137, 147, 156, 163, 186]

promising_amino_acids = []


def identify_promising_amino_acids(spectrum, m):
    global promising_amino_acids
    spectrum = sorted(spectrum)
    # print(spectrum)
    convolution = defaultdict(int)
    for mass1 in spectrum:
        for mass2 in spectrum:
            if mass1 < mass2:
                convolution[mass2 - mass1] += 1
    for mass in convolution:
        if 57 <= mass <= 200:
            promising_amino_acids.append(mass)
    promising_amino_acids = sorted(promising_amino_acids, key=lambda x: -convolution[x])
    for last_idx in range(m, len(promising_amino_acids) - 1):
        if (convolution[promising_amino_acids[last_idx + 1]] !=
                convolution[promising_amino_acids[last_idx]]):
            promising_amino_acids = promising_amino_acids[:last_idx]
            break


def extend_peptides(peptides):
    new_peptides = set()
    for peptide in peptides:
        for amino_acid_mass in promising_amino_acids:
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
    cut_leaderboard = []
    last_item = None
    for idx, item in enumerate(sorted_leaderboard):
        if idx >= n and scores[item] != scores[last_item]:
            break
        cut_leaderboard.append(item)
        last_item = item
    return cut_leaderboard


def find_cyclopeptide(spectrum, n):
    leaderboard = [()]
    parent_mass = max(spectrum)
    leader_score = 0
    leader_peptide = ()

    while leaderboard:
        scores = dict()
        leaderboard = extend_peptides(leaderboard)
        old_leaderboard = leaderboard.copy()
        for peptide in old_leaderboard:
            peptide_spectrum = theoretical_spectrum(peptide)
            scores[peptide] = score(peptide_spectrum, spectrum)
            peptide_mass = mass(peptide)
            if peptide_mass == parent_mass:
                if scores[peptide] >= leader_score:
                    leader_peptide = peptide
                    leader_score = scores[peptide]
                leaderboard.remove(peptide)
            if peptide_mass > parent_mass:
                leaderboard.remove(peptide)
        leaderboard = cut(leaderboard, scores, spectrum, n)
    return leader_peptide


def main():
    m = int(input())
    n = int(input())
    spectrum = set((map(int, input().split())))
    identify_promising_amino_acids(spectrum, m)
    print("-".join(map(str, find_cyclopeptide(spectrum, n))))


if __name__ == "__main__":
    main()
