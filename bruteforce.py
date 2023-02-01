import itertools
import csv
import functools

MAX_COST = 500


# MODELS
class Share:
    def __init__(self, name, price, profit):
        self.name = name
        self.price = price
        self.profit = profit

    def get_actual_profit(self):
        return self.price * self.profit / 100


# CONTROLLERS
# Share controllers
def get_shares():
    """ Take a csv file name and return a list of Share objects"""
    csvfile = get_file()
    shares = []
    with open(csvfile) as csvfile:
        shares_from_file = csv.reader(csvfile)
        first_row = True
        for row in shares_from_file:
            if first_row:
                while row[0] != "name" and row[1] != "price" and row[2] != "profit":
                    print("Use a file with three columns named 'names', 'price' and 'profit'")
                    get_shares()
                first_row = False
            else:
                share = Share(row[0], float(row[1]), float(row[2]))
                shares.append(share)
    return shares


def get_total_price(shares):
    """ Take a collection of Share objects
    and return the accumulated price of the collection"""
    return functools.reduce(lambda acc, sh: acc + sh.price, shares, 0)


def get_total_actual_profit(shares):
    """ Take a collection of Share objects
    and return the accumulated actual profit of the collection"""
    return functools.reduce(lambda acc, sh: acc + sh.get_actual_profit(), shares, 0)


def buy_shares(shares, wallet=MAX_COST):
    shares_bought = []
    for share in shares:
        if wallet >= share.price:
            shares_bought.append(share)
            wallet -= share.price
        elif wallet == 0:
            break
    return shares_bought


# Combination controllers
def get_combinations(shares):
    """ Take a lit of Share objects and
    return all possible combinations in a combinations object
    as tuples of Share objects"""
    list_of_combinations = []
    for length in range(len(shares)):
        for combination in itertools.combinations(shares, length):
            if get_total_price(combination) <= MAX_COST:
                list_of_combinations.append(combination)
    return list_of_combinations


def sort_combinations_by_profit(combinations):
    """ Take a collection of collections of share Objects
    and sort the collections by their actual profit"""
    combinations.sort(key=get_total_actual_profit, reverse=True)


# VIEWS
def print_shares(shares):
    print(list(map(lambda x: x.name, shares)))
    print("total price", get_total_price(shares))
    print("total profit", get_total_actual_profit(shares))


def get_file():
    print("Please enter the path and name of the file containing the shares")
    print("or choose one of these:")
    print("A. original_dataset.csv")
    print("B. dataset1_Python+P7.csv")
    print("C. dataset2_Python+P7.csv")
    file_name = input()
    match file_name.lower():
        case "a":
            return "./share_files/original_dataset.csv"
        case "b":
            return "./share_files/dataset1_Python+P7.csv"
        case "c":
            return "./share_files/dataset2_Python+P7.csv"
        case _:
            return file_name



list_of_shares = get_shares()
all_combinations = get_combinations(list_of_shares)
print(len(all_combinations))
sort_combinations_by_profit(all_combinations)

for i in range(5):
    print("Combination " + str(i+1) + "/" + str(len(all_combinations)))
    print_shares(all_combinations[i])
