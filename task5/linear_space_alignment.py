#! /usr/bin/env python3

"""
    Pseudocode for linear space alignment problem:

    LinearSpaceAlignment(top, bottom, left, right)
        if left = right
            return alignment formed by bottom − top vertical edges
        if top = bottom
            return alignment formed by right − left horizontal edges
        middle ← ⌊ (left + right)/2⌋
        midNode ← MiddleNode(top, bottom, left, right)
        midEdge ← MiddleEdge(top, bottom, left, right)
        LinearSpaceAlignment(top, midNode, left, middle)
        output midEdge
        if midEdge = "→" or midEdge = "↘"
            middle ← middle + 1
        if midEdge = "↓" or midEdge ="↘"
            midNode ← midNode + 1
        LinearSpaceAlignment(midNode, bottom, middle, right)
"""

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
        tokens = line.strip().split()
        for idx, score_ in enumerate(map(int, tokens[1:])):
            score[(letters[idx], tokens[0])] = score_


def linear_space_alignment(first_str, second_str):
    if first_str == "":
        return "-" * len(second_str), second_str
    if second_str == "":
        return first_str, "-" * len(first_str)
    middle_node = find_middle_node(first_str, second_str)
    first_str_mid, second_str_mid, after_first_str_mid, after_second_str_mid = middle_node

    first_part = linear_space_alignment(first_str[:first_str_mid],
                                        second_str[:second_str_mid])

    second_part = linear_space_alignment(first_str[after_first_str_mid:],
                                         second_str[after_second_str_mid:])

    diff_first = after_first_str_mid - first_str_mid
    diff_second = after_second_str_mid - second_str_mid
    middle_ch_first = "-"
    middle_ch_second = "-"
    if diff_first == 1 and diff_second == 1:
        middle_ch_first = first_str[first_str_mid]
        middle_ch_second = second_str[second_str_mid]
    if diff_first == 1 and diff_second == 0:
        middle_ch_first = first_str[first_str_mid]
    if diff_first == 0 and diff_second == 1:
        middle_ch_second = second_str[second_str_mid]
    return (first_part[0] + middle_ch_first + second_part[0],
            first_part[1] + middle_ch_second + second_part[1])


def calc_last_alignment_col(first_str, second_str):
    sigma = 5
    alignment_score = [[0, 0] for i in range(len(first_str) + 1)]
    for j in range(len(second_str) + 1):
        for i in range(len(first_str) + 1):
            if i == 0 and j == 0:
                continue
            diag = 0
            diag_score = 0
            left = 0
            up = 0
            if i > 0 and j > 0:
                diag = alignment_score[i - 1][0]
                ch1 = first_str[i - 1]
                ch2 = second_str[j - 1]
                diag_score = score[(ch1, ch2)]
                up = alignment_score[i - 1][1]
                left = alignment_score[i][0]
                alignment_score[i][1] = max(diag + diag_score, left - sigma, up - sigma)
            if i > 0 and j == 0:
                up = alignment_score[i - 1][1]
                alignment_score[i][1] = up - sigma
            if j > 0 and i == 0:
                left = alignment_score[i][0]
                alignment_score[i][1] = left - sigma
        if j == len(second_str):
            return alignment_score
        for l in alignment_score:
            l[0] = l[1]


def argmax(array):
    max_ = array[0]
    max_idx = 0
    for idx, item in enumerate(array):
        if item > max_:
            max_ = item
            max_idx = idx
    return max_idx


def find_middle_node(first_str, second_str):
    sigma = 5
    middle_idx = len(second_str) // 2
    alignment_score = calc_last_alignment_col(first_str, second_str[:middle_idx])
    middle_score_part1 = [list_[1] for list_ in alignment_score]

    alignment_score = calc_last_alignment_col(first_str[::-1],
                                              second_str[middle_idx:][::-1])[::-1]
    middle_score_part2 = [list_[1] for list_ in alignment_score]
    middle_node_idx = argmax([item1 + item2
                              for item1, item2 in zip(middle_score_part1, middle_score_part2)])
    after_middle_node_idx = middle_node_idx
    after_middle_col = middle_idx + 1
    best_score = alignment_score[middle_node_idx][0] - sigma

    if (middle_node_idx < len(first_str) and
            middle_score_part2[middle_node_idx + 1] - sigma > best_score):
        after_middle_node_idx = middle_node_idx + 1
        after_middle_col = middle_idx
        best_score = middle_score_part2[middle_node_idx + 1] - sigma
    if (middle_node_idx < len(first_str) and
            alignment_score[middle_node_idx + 1][0] +
            score[(first_str[middle_node_idx], second_str[middle_idx])] > best_score):
        after_middle_node_idx = middle_node_idx + 1
        after_middle_col = middle_idx + 1
    return middle_node_idx, middle_idx,  after_middle_node_idx, after_middle_col


def calc_score(first_aligned, second_aligned):
    sigma = 5
    score_ = 0
    for ch1, ch2 in zip(first_aligned, second_aligned):
        if ch1 != "-" and ch2 != "-":
            score_ += score[(ch1, ch2)]
        else:
            score_ -= sigma
    return score_


def main():
    first_str = input()
    second_str = input()
    parse_score_str()
    first_aligned, second_aligned = linear_space_alignment(first_str, second_str)
    score_ = calc_score(first_aligned, second_aligned)
    print("\n".join([str(score_), first_aligned, second_aligned]))


if __name__ == "__main__":
    main()
