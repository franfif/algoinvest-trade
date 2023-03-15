<h1 align="center">
AlgoInvest&Trade - Solve Problems Using Algorithms in Python
<br/>
<img alt="JustStreamIt logo" src="img/AlgoInvest_Trade_Logo.png" width="224px"/>
</h1>

## Introduction
AlgoInvest&Trade is a (fictional - for education purposes) finance company specializing in investment. <br>It is seeking to optimize its investment strategies using algorithms in order to gain more client profits.

The goal of this project is to design two algorithms:
1. A [brute-force solution](./bruteforce.py) that will analyse any possible combination of shares, their profit, and buy the best combination with the money available.
2. An [optimized solution](./optimized.py) that will not look over every combination but will buy the best combination possible in a very short time (less than a second).

## Installation
Clone this project to a local repository.
Python3 is needed to execute these algorithms.
No virtual environment is needed at this time.

## How to use the algorithms
In the terminal, from the cloned repository, use one the following commands:
```bash
$ python3 bruteforce.py
```
or 
```bash
$ python3 optimized.py
```
The program will ask to enter the path and name of a file containing the shares, or select one of the following datasets:
- [original_dataset.csv](./share_files/original_dataset.csv) (original list of 20 shares)
- [dataset1_Python+P7.csv](./share_files/dataset1_Python+P7.csv) (Sienna's first dataset of 1001 shares)
- [dataset2_Python+P7.csv](./share_files/dataset2_Python+P7.csv) (Sienna's second dataset of 1000 shares)

If you choose to enter another file's path and name, it must:
- be a csv file
- have three columns respectively named 'share', 'price', and 'profit' with each share's name, price and profit in the rows below.

## Brute-force solution
The brute-force solution uses the itertools module to get all the possible combinations of shares. 
It then looks over each of them, excluding the combinations too expensive to be bought, and compare their actual profit over two years.
The 5 best combinations are picked out and provided to the user.

This solution has an exponential time complexity of O(2<sup>n</sup>), which makes it not usable for a large number of shares.
Space complexity is linear: O(n).

## Optimized solution
The optimized solution orders the shares by their profit percentage, then proceeds to buy the shares in order from the biggest profit percentage, until there is not enough money left to buy any more share.

This solution has a similar space complexity than the brute-force solution (linear space complexity, O(n)). 
It is much faster than the brute-force solution, with a linearithmic time complexity of O(n log n).

However, this solution only looks for one combination, based on the ordered list of available shares and the cost of each share.

Buying a share with a higher profit percentage might prevent the buying of multiple shares with a lower profit percentage that could bring a better global actual profit.

For instance, for a wallet limited to 500€:

| Name    | Price | Profit % | Actual profit |
|---------|-------|----------|---------------|
| Share A | 400   | 0.2      | 80            |
| Share B | 140   | 0.19     | 26.6          |
| Share C | 110   | 0.18     | 19.8          |
| Share D | 120   | 0.17     | 20.4          |
| Share E | 130   | 0.15     | 19.5          |

The optimized solution would start by buying the share with the best profit percentage, 
Share A, and would not be able to buy any other share. 

The actual profit would be 80€.
However, the best solution would be to buy Shares B, C, D and E, who have a lower profit 
percentage but together yield a better actual profit (86.30€).

In this second situation, for a wallet limited to 500€, the optimized solution would buy Share A with a higher profit percentage.

| Name    | Price | Profit % | Actual profit |
|---------|-------|----------|---------------|
| Share A | 150   | 0.2      | 30            |
| Share B | 400   | 0.19     | 76            |
 
Doing so would prevent buying the next share with a much larger actual profit, because the amount of money left is then too low.
In this situation, the share with a lower percentage profit would have been much more profitable, simply because the cost is higher.
