import random


def trim(l, delta):
    m = len(l)
    l_prime = [l[0]]
    last = l[0]
    for i in range(1, m):
        if l[i] > last * (1 + delta):
            l_prime.append(l[i])
            last = l[i]
    return l_prime


def merge_lists(l1, l2):
    i, j = 0, 0
    ans = []
    while i < len(l1) and j < len(l2):
        if l1[i] == l2[j]:
            ans.append(l1[i])
            i += 1
            j += 1
        elif l1[i] < l2[j]:
            ans.append(l1[i])
            i += 1
        else:
            ans.append(l2[j])
            j += 1

    while i < len(l1):
        ans.append(l1[i])
        i += 1

    while j < len(l2):
        ans.append(l2[j])
        j += 1

    return ans


def approx_subset_sum(s, t, epsilon):
    n = len(s)
    l = [0]
    for i in range(n):
        print('L_{} = {}'.format(i, l))
        l = merge_lists(l, [x + s[i] for x in l])
        l = trim(l, epsilon/(2*n))
        l = list(filter(lambda x: x < t, l))
    print('L_{} = {}'.format(n, l))

    return max(l)


if __name__ == "__main__":
    LOWER_BOUND = 0
    UPPER_BOUND = 200
    RANDOM_NUMBERS = 15
    EPSILON_VALUES_NUMBER = 3

    s = []
    epsilon_l = []

    while len(s) != RANDOM_NUMBERS:
        x = random.randint(LOWER_BOUND, UPPER_BOUND)
        if x not in s:
            s.append(x)

    s.sort()

    print('Conjunto: {}'.format(s))

    for _ in range(EPSILON_VALUES_NUMBER):
        epsilon_l.append(random.random())

    for epsilon in epsilon_l:
        k = random.randint(1, RANDOM_NUMBERS)

        chosen_subset = random.sample(s, k)
        exact_sum = sum(chosen_subset)
        print('Conjunto {}'.format(s))
        print('El subconjunto seleccionado es {} que suma {}'.format(
            chosen_subset, exact_sum))

        z = approx_subset_sum(s, exact_sum, epsilon)

        print('El valor de z* es : {}'.format(z))
