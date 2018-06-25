#! /usr/bin/env python3
from collections import defaultdict

amino_acid_masses = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115,
                     128, 129, 131, 137, 147, 156, 163, 186]

num_peptides = defaultdict(int)

num_peptides[0] = 1


def num_peptides_of_mass(total_mass):
    if total_mass in num_peptides:
        return num_peptides[total_mass]
    total = 0
    for mass in amino_acid_masses:
        if total_mass - mass >= 0:
            total += num_peptides_of_mass(total_mass - mass)
    num_peptides[total_mass] = total
    return total


def main():
    mass = int(input())
    print(num_peptides_of_mass(mass))


if __name__ == "__main__":
    main()
