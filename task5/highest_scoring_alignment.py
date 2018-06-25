#! /usr/bin/env python3
from pprint import pprint
import numpy as np
score_str = """
   A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y
A  4  0 -2 -1 -2  0 -2 -1 -1 -1 -1 -2 -1 -1 -1  1  0  0 -3 -2
C  0  9 -3 -4 -2 -3 -3 -1 -3 -1 -1 -3 -3 -3 -3 -1 -1 -1 -2 -2
D -2 -3  6  2 -3 -1 -1 -3 -1 -4 -3  1 -1  0 -2  0 -1 -3 -4 -3
E -1 -4  2  5 -3 -2  0 -3  1 -3 -2  0 -1  2  0  0 -1 -2 -3 -2
F -2 -2 -3 -3  6 -3 -1  0 -3  0  0 -3 -4 -3 -3 -2 -2 -1  1  3
G  0 -3 -1 -2 -3  6 -2 -4 -2 -4 -3  0 -2 -2 -2  0 -2 -3 -2 -3
H -2 -3 -1  0 -1 -2  8 -3 -1 -3 -2  1 -2  0  0 -1 -2 -3 -2  2
I -1 -1 -3 -3  0 -4 -3  4 -3  2  1 -3 -3 -3 -3 -2 -1  3 -3 -1
K -1 -3 -1  1 -3 -2 -1 -3  5 -2 -1  0 -1  1  2  0 -1 -2 -3 -2
L -1 -1 -4 -3  0 -4 -3  2 -2  4  2 -3 -3 -2 -2 -2 -1  1 -2 -1
M -1 -1 -3 -2  0 -3 -2  1 -1  2  5 -2 -2  0 -1 -1 -1  1 -1 -1
N -2 -3  1  0 -3  0  1 -3  0 -3 -2  6 -2  0  0  1  0 -3 -4 -2
P -1 -3 -1 -1 -4 -2 -2 -3 -1 -3 -2 -2  7 -1 -2 -1 -1 -2 -4 -3
Q -1 -3  0  2 -3 -2  0 -3  1 -2  0  0 -1  5  1  0 -1 -2 -2 -1
R -1 -3 -2  0 -3 -2  0 -3  2 -2 -1  0 -2  1  5 -1 -1 -3 -3 -2
S  1 -1  0  0 -2  0 -1 -2  0 -2 -1  1 -1  0 -1  4  1 -2 -3 -2
T  0 -1 -1 -1 -2 -2 -2 -1 -1 -1 -1  0 -1 -1 -1  1  5  0 -2 -2
V  0 -1 -3 -2 -1 -3 -3  3 -2  1  1 -3 -2 -2 -3 -2  0  4 -3 -1
W -3 -2 -4 -3  1 -2 -2 -3 -3 -2 -1 -4 -4 -2 -3 -3 -2 -3 11  2
Y -2 -2 -3 -2  3 -3  2 -1 -2 -1 -1 -2 -3 -1 -2 -2 -2 -1  2  7
"""

score = {}


def parse_score_str():
    lines = score_str.strip().split("\n")
    letters = lines[0].strip().split()
    for line in lines[1:]:
        # print(line)
        tokens = line.strip().split()
        for idx, score_ in enumerate(map(int, tokens[1:])):
            score[(letters[idx], tokens[0])] = score_


def calculate_best_alignment(first_str, second_str):
    best_alignment_str1 = ""
    best_alignment_str2 = ""
    sigma = 5
    alignment_score = []
    parent = []
    for i in range(len(first_str) + 1):
        line1 = []
        line2 = []
        for j in range(len(second_str) + 1):
            line1.append(0)
            line2.append((0, 0))
        alignment_score.append(line1)
        parent.append(line2)
    for i in range(len(first_str) + 1):
        for j in range(len(second_str) + 1):
            if i == 0 and j == 0:
                continue
            diag = 0
            diag_score = 0
            left = 0
            up = 0
            if i > 0 and j > 0:
                diag = alignment_score[i - 1][j - 1]
                ch1 = first_str[i - 1]
                ch2 = second_str[j - 1]
                diag_score = score[(ch1, ch2)]
                up = alignment_score[i - 1][j]
                left = alignment_score[i][j - 1]
                alignment_score[i][j] = max(diag + diag_score, left - sigma, up - sigma)
                if alignment_score[i][j] == diag + diag_score:
                    parent[i][j] = (i - 1, j - 1)
                elif alignment_score[i][j] == left - sigma:
                    parent[i][j] = (i, j - 1)
                else:  # alignment_score[i][j] == up - sigma
                    parent[i][j] = (i - 1, j)
            if i > 0 and j < 1:
                up = alignment_score[i - 1][j]
                alignment_score[i][j] = up - sigma
                parent[i][j] = (i - 1, j)
            if j > 0 and i < 1:
                left = alignment_score[i][j - 1]
                alignment_score[i][j] = left - sigma
                parent[i][j] = (i, j - 1)
    pprint(np.array(alignment_score))
    pprint(parent)
    prev_i, prev_j = len(first_str), len(second_str)
    while prev_i != 0 or prev_j != 0:
        # print(prev_i, prev_j)
        if parent[prev_i][prev_j] == (prev_i - 1, prev_j - 1):
            best_alignment_str1 += first_str[prev_i - 1]
            best_alignment_str2 += second_str[prev_j - 1]
        elif parent[prev_i][prev_j] == (prev_i - 1, prev_j):
            best_alignment_str1 += first_str[prev_i - 1]
            best_alignment_str2 += "-"
        else:
            best_alignment_str2 += second_str[prev_j - 1]
            best_alignment_str1 += "-"
        prev_i, prev_j = parent[prev_i][prev_j]
    return (alignment_score[len(first_str)][len(second_str)],
            "".join(reversed(best_alignment_str1)), "".join(reversed(best_alignment_str2)))


def main():
    first_str = input()
    second_str = input()
    parse_score_str()
    print("\n".join(map(str, calculate_best_alignment(first_str, second_str))))
    calculate_best_alignment(first_str[::-1], second_str[::-1])


if __name__ == "__main__":
    main()
