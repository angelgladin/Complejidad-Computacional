import random


def bin_packing(items, n, capacity):
    items.sort(reverse=True)

    min_bins = 0
    bins_l = [0]*n

    for i in range(n):
        j = 0
        while j < min_bins:
            if bins_l[j] >= items[i]:
                bins_l[j] = bins_l[j] - items[i]
                break
            j += 1

        if min_bins == j:
            bins_l[min_bins] = capacity - items[i]
            min_bins += 1

    return min_bins


if __name__ == "__main__":
    RANDOM_NUMBERS_N = 20
    LOWER_BOUND = .1
    UPPER_BOUND = .9

    random_numbers = []

    for _ in range(RANDOM_NUMBERS_N):
        x = random.uniform(LOWER_BOUND, UPPER_BOUND)
        random_numbers.append(x)

    print('Lote: {}'.format(random_numbers))
    print('Número de lotes necesarios: {}'.format(
        bin_packing(random_numbers, RANDOM_NUMBERS_N, 1)))
