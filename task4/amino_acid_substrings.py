#! /usr/bin/env python3

codons = {"A": ["GCU", "GCC", "GCA", "GCG"],
          "C": ["UGU", "UGC"],
          "D": ["GAU", "GAC"],
          "E": ["GAA", "GAG"],
          "F": ["UUU", "UUC"],
          "G": ["GGU", "GGC", "GGA", "GGG"],
          "H": ["CAU", "CAC"],
          "I": ["AUU", "AUC", "AUA"],
          "K": ["AAA", "AAG"],
          "L": ["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"],
          "M": ["AUG"],
          "N": ["AAU", "AAC"],
          "O": ["UAG"],
          "P": ["CCU", "CCC", "CCA", "CCG"],
          "Q": ["CAA", "CAG"],
          "R": ["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"],
          "S": ["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"],
          "T": ["ACU", "ACC", "ACA", "ACG"],
          "U": ["UGA"],
          "V": ["GUU", "GUC", "GUA", "GUG"],
          "W": ["UGG"],
          "Y": ["UAU", "UAC"],
          "*": ["UAA"]
          }

amino_acids = {codon: amino_acid for amino_acid, codons in codons.items() for codon in codons}


def complement(pattern):
    complement = {"A": "T", "G": "C", "T": "A", "C": "G"}
    new_pattern = ""
    for symbol in pattern:
        new_pattern += complement[symbol]
    return new_pattern


def dna_to_rna(dna):
    rna = ""
    for symbol in dna:
        if symbol == "T":
            rna += "U"
        else:
            rna += symbol
    return rna


def rna_to_amino_acids(rna):
    amino_acids_string = ""
    for idx in range(0, len(rna), 3):
        triplet = rna[idx: idx + 3]
        if len(triplet) == 3:
            amino_acids_string += amino_acids[triplet]
    return amino_acids_string


def find_matches_in_rna(rna, peptide):
    amino_acids_str = rna_to_amino_acids(rna)
    num_amino_acids = len(peptide)
    indices = []
    current_start = amino_acids_str.find(peptide)
    while current_start > -1:
        indices.append((current_start * 3, (num_amino_acids + current_start) * 3))
        current_start = amino_acids_str.find(peptide, current_start + 1)
    return indices


def find_matches(dna, peptide):
    matches = []
    rna = dna_to_rna(dna)
    dna_reverse_complement = "".join(reversed(complement(dna)))
    rna_reverse_complement = dna_to_rna(dna_reverse_complement)
    for start_idx in [0, 1, 2]:
        for start, end in find_matches_in_rna(rna[start_idx:], peptide):
            matches.append(dna[start_idx + start: start_idx + end])
        for start, end in find_matches_in_rna(rna_reverse_complement[start_idx:], peptide):
            matches.append("".join(reversed(complement(
                dna_reverse_complement[start_idx + start: start_idx + end]))))
    return matches


def main():
    dna = input()
    peptide = input()
    print("\n".join(find_matches(dna, peptide)))


if __name__ == "__main__":
    main()
