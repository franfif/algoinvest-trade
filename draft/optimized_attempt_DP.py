import csv
import functools
from time import perf_counter


MAX_COST = 50000


# MODELS
class Share:
    def __init__(self, name, price, profit):
        self.name = name
        self.price = int(abs(price) * 100)
        self.profit = profit

    def get_actual_profit(self):
        return self.price * self.profit / 10000


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


def buy_shares(share_list, wallet, max_share_profits, shares_bought):
    for euros in range(wallet + 1):
        max_profit = 0.0
        new_share = None
        # for j in [s for s in share_list if s.price <= euros]:
        for j in [s for s in share_list if s.price <= euros and not was_bought(s, euros - s.price, shares_bought)]:
            try:
                current_profit = max_share_profits[euros - j.price] + j.get_actual_profit()
                if current_profit > max_profit:
                    max_profit = current_profit
                    new_share = j
            except IndexError:
                print(f"euros: {euros}, j.price: {j.price}, euros-j.price:{euros-j.price}")
        max_share_profits[euros] = max_profit
        shares_bought[euros] = new_share
    return max_share_profits[wallet]


def was_bought(share, wallet, shares_bought):
    euros = wallet
    while euros > 0:
        this_share = shares_bought[euros]
        if not this_share:
            return False
        if this_share == share:
            return True
        else:
            euros = euros - this_share.price
    return False


# VIEWS
def print_share_comb(shares):
    print(list(map(print_or_skip, shares)))
    # print("Total price", get_total_price(shares))
    # print("Total profit", get_total_actual_profit(shares))


def print_or_skip(share):
    if share is None or share == 0:
        return ""
    return share.name


def print_one_share(share):
    print(f"[Name: {share.name}, Price: {share.price}, Profit: {share.profit}%]")


def print_shares(shares_used, wallet):
    euros = wallet
    while euros > 0:
        this_share = shares_used[euros]
        if this_share is None:
            break
        print_one_share(this_share)
        euros = euros - this_share.price


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


def main():
    list_of_shares = get_shares()
    amount = 63
    clist = [1, 5, 10, 21, 25]
    coins_used = [0] * (amount + 1)
    coin_count = [0] * (amount + 1)
    max_shares_profits = [0] * (MAX_COST + 1)
    shares_bought = [None] * (MAX_COST + 1)
    time_start = perf_counter()
    print(f"Best combination of shares for {MAX_COST} euros yields:")
    print(buy_shares(list_of_shares, MAX_COST, max_shares_profits, shares_bought), "euros")
    print("They are:")
    print_shares(shares_bought, MAX_COST)

    time_stop = perf_counter()
    print(f"Elapsed time during the whole program in seconds: {time_stop - time_start}")

    # print("The used list is as follows:")
    # print(shares_bought)

    # print("List of the shares yielding one of the best profits for 500€ or less:")
    # quick_best_shares = buy_shares(sort_by_profit_percentage(list_of_shares))
    # print_shares(quick_best_shares)


main()
