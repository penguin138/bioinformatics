#! /usr/bin/env python3
import re


def calculate_change(money, coins):
    coins = set(coins)
    change = [0] * (money + 1)
    for amount in range(1, money + 1):
        if amount in coins:
            change[amount] = 1
        else:
            change[amount] = min(change[amount - coin] + 1
                                 for coin in coins if (amount - coin) >= 0)
    return change[money]


def main():
    money = int(input())
    coins = list(map(int, re.split("\s*,\s*", input())))
    print(calculate_change(money, coins))


if __name__ == "__main__":
    main()
