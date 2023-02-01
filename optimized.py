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
def get_shares(csvfile):
    """ Take a csv file name and return a list of Share objects"""
    shares = []
    with open(csvfile) as csvfile:
        shares_from_file = csv.reader(csvfile)
        first_row = True
        for row in shares_from_file:
            if first_row:
                if row[0] != "name" and row[1] != "price" and row[2] != "profit":
                    print("Use a file with three columns named 'names', 'price' and 'profit'")
                    return None
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


list_of_shares = get_shares('./share_files/original_dataset.csv')

print("List of the shares yielding one of the best profits for 500€ or less:")
quick_best_shares = buy_shares(sort_by_profit_percentage(list_of_shares))
print_shares(quick_best_shares)
