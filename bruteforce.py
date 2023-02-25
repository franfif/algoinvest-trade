import itertools
import csv
import functools
from time import perf_counter

MAX_COST = 500


# MODELS
class Share:
    def __init__(self, name, price, profit):
        self.name = name
        self.price = price
        self.profit = profit

    def get_actual_profit(self):
        return self.price * self.profit / 100


class WrongColumnsError(BaseException):
    pass


# CONTROLLERS
# Share controllers
def get_shares():
    """ Take a csv file name and return a list of Share objects"""
    while True:
        csvfile = get_file()
        shares = []
        try:
            with open(csvfile) as csvfile:
                shares_from_file = csv.reader(csvfile)
                first_row = True
                for row in shares_from_file:
                    if first_row:
                        if row[0] != "name" or row[1] != "price" or row[2] != "profit":
                            csvfile.close()
                            raise WrongColumnsError
                        first_row = False
                    else:
                        share = Share(row[0], float(row[1]), float(row[2]))
                        shares.append(share)
            break
        except OSError:
            print(csvfile, "could be found, make sure to enter the path as well.")
        except WrongColumnsError:
            print("Use a file with three columns named 'names', 'price' and 'profit'")
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
    """ Take a collection of collections of Share objects
    and sort the collections by their actual profit"""
    combinations.sort(key=get_total_actual_profit, reverse=True)


# VIEWS
def print_shares(shares):
    print(list(map(lambda x: x.name, shares)))
    print("total price", get_total_price(shares))
    print("total profit", get_total_actual_profit(shares))


def show_combinations(combinations):
    show_results = 5
    if len(all_combinations) < 5:
        show_results = len(all_combinations)

    for i in range(show_results):
        print("Combination", str(i + 1), "/", str(len(all_combinations)))
        print_shares(all_combinations[i])


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
time_start = perf_counter()
all_combinations = get_combinations(list_of_shares)
sort_combinations_by_profit(all_combinations)
show_combinations(all_combinations)

time_stop = perf_counter()
print(f"Elapsed time during the whole program in seconds: {time_stop - time_start}")