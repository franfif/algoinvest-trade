import itertools
import csv

MAX_COST = 500


class Share:
    def __init__(self, name, price, profit):
        self.name = name
        self.price = price
        self.profit = profit

    def get_actual_profit(self):
        return self.price * self.profit / 100


def get_shares(csvfile):
    """ Take a csv file name and return a list of Share objects"""
    list_of_shares = []
    with open(csvfile) as csvfile:
        shares_from_file = csv.reader(csvfile)
        first_row = True
        for row in shares_from_file:
            if first_row:
                if row[0] != "name" and row[1] != "price" and row[2] != "profit":
                    return None
                first_row = False
            else:
                share = Share(row[0], float(row[1]), float(row[2]))
                list_of_shares.append(share)
    return list_of_shares

def get_combinations(shares):
    """ Take a lit of Share objects and
    return all possible combinations in a combinations object
    as tuples of Share objects"""
    list_of_combinations = []
    for length in range(len(shares) + 1):
        for combination in itertools.combinations(shares, length):
            if get_total_price(combination) <= MAX_COST:
                list_of_combinations.append(combination)
    return list_of_combinations


def get_total_price(combination):
    """ Take a combination (a tuple) of Share objects
    and return the accumulated value of the key of each share in the combination"""
    total_value = 0
    for sh in combination:
        total_value += sh.price
    return total_value


def get_combination_profit(combination):
    combination_profit = 0
    for sh in combination:
        combination_profit += sh.get_actual_profit()
    return combination_profit


def sort_by_profit(combinations):
    combinations.sort(key=get_combination_profit, reverse=True)
    return combinations


def print_comb(combination):
    print(list(map(lambda x: [x.name, x.price, x.profit], combination)))


list_of_shares = get_shares('./share_files/original_dataset.csv')
all_combinations = get_combinations(list_of_shares)
print(len(all_combinations))
sort_by_profit(all_combinations)

for i in range(5):
    print_comb(all_combinations[i])
    print("total price", get_total_price(all_combinations[i]))
    print("total profit", get_combination_profit(all_combinations[i]))
