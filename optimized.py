import csv
import functools
from time import perf_counter

MAX_COST = 500


# MODELS
class Share:
    def __init__(self, name, price, profit):
        self.name = name
        self.price = abs(price)
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
                rows = csv.reader(csvfile)
                first_row = True
                for row in rows:
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
            print("Use a file with three columns named 'name', 'price' and 'profit'")
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


def sort_by_profit_percentage(shares):
    """take a list of Share objects
    return a new list with the same objects, sorted by their individual profit"""
    sorted_shares = list(shares)
    sorted_shares.sort(key=lambda x: x.profit, reverse=True)
    return sorted_shares


# VIEWS
def print_shares(shares):
    print(list(map(lambda x: x.name, shares)))
    print("Total price", get_total_price(shares))
    print("Total profit", get_total_actual_profit(shares))


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

print("List of the shares yielding one of the best profits for 500€ or less:")
quick_best_shares = buy_shares(sort_by_profit_percentage(list_of_shares))
print_shares(quick_best_shares)

time_stop = perf_counter()
print(f"Elapsed time during the whole program in seconds: {time_stop-time_start}")
