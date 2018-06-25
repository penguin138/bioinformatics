#! /usr/bin/env python3

score_str = """
   A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y
A  2 -2  0  0 -3  1 -1 -1 -1 -2 -1  0  1  0 -2  1  1  0 -6 -3
C -2 12 -5 -5 -4 -3 -3 -2 -5 -6 -5 -4 -3 -5 -4  0 -2 -2 -8  0
D  0 -5  4  3 -6  1  1 -2  0 -4 -3  2 -1  2 -1  0  0 -2 -7 -4
E  0 -5  3  4 -5  0  1 -2  0 -3 -2  1 -1  2 -1  0  0 -2 -7 -4
F -3 -4 -6 -5  9 -5 -2  1 -5  2  0 -3 -5 -5 -4 -3 -3 -1  0  7
G  1 -3  1  0 -5  5 -2 -3 -2 -4 -3  0  0 -1 -3  1  0 -1 -7 -5
H -1 -3  1  1 -2 -2  6 -2  0 -2 -2  2  0  3  2 -1 -1 -2 -3  0
I -1 -2 -2 -2  1 -3 -2  5 -2  2  2 -2 -2 -2 -2 -1  0  4 -5 -1
K -1 -5  0  0 -5 -2  0 -2  5 -3  0  1 -1  1  3  0  0 -2 -3 -4
L -2 -6 -4 -3  2 -4 -2  2 -3  6  4 -3 -3 -2 -3 -3 -2  2 -2 -1
M -1 -5 -3 -2  0 -3 -2  2  0  4  6 -2 -2 -1  0 -2 -1  2 -4 -2
N  0 -4  2  1 -3  0  2 -2  1 -3 -2  2  0  1  0  1  0 -2 -4 -2
P  1 -3 -1 -1 -5  0  0 -2 -1 -3 -2  0  6  0  0  1  0 -1 -6 -5
Q  0 -5  2  2 -5 -1  3 -2  1 -2 -1  1  0  4  1 -1 -1 -2 -5 -4
R -2 -4 -1 -1 -4 -3  2 -2  3 -3  0  0  0  1  6  0 -1 -2  2 -4
S  1  0  0  0 -3  1 -1 -1  0 -3 -2  1  1 -1  0  2  1 -1 -2 -3
T  1 -2  0  0 -3  0 -1  0  0 -2 -1  0  0 -1 -1  1  3  0 -5 -3
V  0 -2 -2 -2 -1 -1 -2  4 -2  2  2 -2 -1 -2 -2 -1  0  4 -6 -2
W -6 -8 -7 -7  0 -7 -3 -5 -3 -2 -4 -4 -6 -5  2 -2 -5 -6 17  0
Y -3  0 -4 -4  7 -5  0 -1 -4 -1 -2 -2 -5 -4 -4 -3 -3 -2  0 10
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
    overall_max_indices = (0, 0)
    overall_max = 0
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
                alignment_score[i][j] = max(diag + diag_score, left - sigma, up - sigma, 0)

                if alignment_score[i][j] == diag + diag_score:
                    parent[i][j] = (i - 1, j - 1)
                elif alignment_score[i][j] == left - sigma:
                    parent[i][j] = (i, j - 1)
                elif alignment_score[i][j] == up - sigma:
                    parent[i][j] = (i - 1, j)
                else:
                    parent[i][j] = None
            if i > 0 and j < 1:
                up = alignment_score[i - 1][j]
                alignment_score[i][j] = max(up - sigma, 0)
                parent[i][j] = (i - 1, j) if alignment_score[i][j] == up - sigma else None
            if j > 0 and i < 1:
                left = alignment_score[i][j - 1]
                alignment_score[i][j] = max(left - sigma, 0)
                parent[i][j] = (i, j - 1) if alignment_score[i][j] == left - sigma else None
            if alignment_score[i][j] > overall_max:
                overall_max = alignment_score[i][j]
                overall_max_indices = (i, j)
    alignment_score[len(first_str)][len(second_str)] = overall_max
    prev_i, prev_j = overall_max_indices
    while prev_i != 0 or prev_j != 0:
        if parent[prev_i][prev_j] == (prev_i - 1, prev_j - 1):
            best_alignment_str1 += first_str[prev_i - 1]
            best_alignment_str2 += second_str[prev_j - 1]
        elif parent[prev_i][prev_j] == (prev_i - 1, prev_j):
            best_alignment_str1 += first_str[prev_i - 1]
            best_alignment_str2 += "-"
        elif parent[prev_i][prev_j] == (prev_i, prev_j - 1):
            best_alignment_str2 += second_str[prev_j - 1]
            best_alignment_str1 += "-"
        else:
            break
        prev_i, prev_j = parent[prev_i][prev_j]
    return (alignment_score[overall_max_indices[0]][overall_max_indices[1]],
            "".join(reversed(best_alignment_str1)), "".join(reversed(best_alignment_str2)))


def main():
    first_str = input()
    second_str = input()
    parse_score_str()
    print("\n".join(map(str, calculate_best_alignment(first_str, second_str))))


if __name__ == "__main__":
    main()
