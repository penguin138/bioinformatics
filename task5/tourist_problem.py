#! /usr/bin/env python3
import numpy as np


def find_longest_path(n, m, down, right):
    longest_path = np.zeros(shape=(n + 1, m + 1))
    for i in range(0, n + 1):
        for j in range(0, m + 1):
            prev_down = 0
            prev_right = 0
            path_right = 0
            path_down = 0
            if i > 0:
                prev_down = longest_path[i - 1, j]
                path_down = down[i - 1, j]
            if j > 0:
                prev_right = longest_path[i, j - 1]
                path_right = right[i, j - 1]
            longest_path[i, j] = max(prev_down + path_down, prev_right + path_right)
    return longest_path[n, m]


def main():
    n, m = list(map(int, input().split()))
    down = np.empty(shape=(n, m + 1))
    for i in range(n):
        down[i, :] = list(map(int, input().split()))
    input()
    right = np.empty(shape=(n + 1, m))
    for i in range(n + 1):
        right[i, :] = list(map(int, input().split()))
    print(int(find_longest_path(n, m, down, right)))


if __name__ == "__main__":
    main()
