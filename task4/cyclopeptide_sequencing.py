#! /usr/bin/env python3

amino_acid_masses = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115,
                     128, 129, 131, 137, 147, 156, 163, 186]


def extend_peptides(peptides):
    new_peptides = set()
    for peptide in peptides:
        for amino_acid_mass in amino_acid_masses:
            new_peptides.add(peptide + (amino_acid_mass,))
    return new_peptides


def theoretical_spectrum(peptide):
    spectrum = [0]
    double_peptide = peptide
    double_peptide += peptide
    peptide_length = len(peptide)
    for i in range(peptide_length):
        for j in range(1, peptide_length):
            spectrum.append(sum(double_peptide[i: i + j]))
    spectrum.append(sum(peptide))
    return sorted(spectrum)


def consistent(peptide, spectrum):
    spectrum_set = set(spectrum)
    peptide_length = len(peptide)
    for i in range(peptide_length):
        for j in range(1, peptide_length + 1):
            if sum(peptide[i:i + j]) not in spectrum_set:
                return False
    return True


def mass(peptide):
    total = 0
    for mass in peptide:
        total += mass
    return total


def find_cyclopeptides(spectrum):
    peptides = set([()])
    parent_mass = max(spectrum)
    while peptides:
        peptides = extend_peptides(peptides)
        old_peptides = peptides.copy()
        for peptide in old_peptides:
            peptide_spectrum = theoretical_spectrum(peptide)
            if mass(peptide) == parent_mass:
                if peptide_spectrum == spectrum:
                    yield peptide
                peptides.remove(peptide)
            elif not consistent(peptide, spectrum):
                peptides.remove(peptide)


def main():
    spectrum = list(map(int, input().split()))
    for item in find_cyclopeptides(spectrum):
        print("-".join(map(str, item)), end=" ")


if __name__ == "__main__":
    main()
