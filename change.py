import time

memo = {}
COIN_VALUES = [25, 10, 5, 1]

def make_change(total, num_q=0, num_d=0, num_n=0, num_p=0):
    cache = memo.get((num_q, num_d, num_n, num_p))
    if cache is not None:
        return cache
    amount = num_q*25+num_d*10+num_n*5+num_p*1
    if amount == total:
        return [(num_q, num_d, num_n, num_p)]
    elif amount > total:
        return []

    change_possibilites = set()
    add_q = make_change(total, num_q+1, num_d, num_n, num_p)
    add_d = make_change(total, num_q, num_d+1, num_n, num_p)
    add_n = make_change(total, num_q, num_d, num_n+1, num_p)
    add_p = make_change(total, num_q, num_d, num_n, num_p+1)

    for x in add_q, add_d, add_n, add_p:
        for p in x:
            change_possibilites.add(p)
            if memo.get((num_q, num_d, num_n, num_p)) is None:
                memo[(num_q, num_d, num_n, num_p)] = set()
            memo[(num_q, num_d, num_n, num_p)].add(p)


    return change_possibilites

def change_largest_values(total):
    num_coins = []
    for i, coin_value in enumerate(COIN_VALUES):
        num_coins.append(total//coin_value)
        total -= (num_coins[i] * coin_value)
    return num_coins


memo2 = {}
def make_change2(total):
    if total in memo2:
        return memo2.get(total)
    if total < 0:
        return []
    if total == 0:
        return [(0, 0, 0, 0)]
    if total < 5:
        return [(0, 0, 0, total)]

    change = set()
    for i, coin_value in enumerate(COIN_VALUES):
        r_result = make_change2(total-coin_value)
        for change_option in r_result:
            added_coin = [coin for coin in change_option]
            added_coin[i] += 1
            added_coin_tuple = (added_coin[0], added_coin[1], added_coin[2], added_coin[3])
            if added_coin_tuple not in change:
                change.add(added_coin_tuple)

    memo2[total] = change
    return change

if __name__ == '__main__':
    TOTAL = 100

    # # ORIG
    time_start = time.time()
    result = make_change(TOTAL)
    time_end = time.time()
    print(result, '\nTIME:', time_end-time_start)

    # LARGEST VALUE
    time_start = time.time()
    result = change_largest_values(TOTAL)
    time_end = time.time()
    print(result, '\nTIME:', time_end-time_start)

    # COUNTDOWN
    time_start = time.time()
    result = make_change2(TOTAL)
    time_end = time.time()
    print(result, '\nTIME:', time_end-time_start)
