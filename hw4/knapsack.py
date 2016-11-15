import random
import heapq

WEIGHTS = []
COSTS = []

P = 1000
R = 100
M = 10

MAX_WEIGHT, N = tuple(map(int, input().split()))

# first cost then weight
for i in range(N):
    ci, wi = tuple(map(int, input().split()))
    COSTS.append(ci)
    WEIGHTS.append(wi)


def gen_random_individuals():
    individuals = []
    for i in range(P):
        individual = []
        for k in range(len(WEIGHTS)):
            individual.append(random.randint(0, 1))
        individuals.append(individual)
    return individuals


def calculate_individual_cost(individual):
    weight = sum([a * b for a, b in zip(individual, WEIGHTS)])
    if weight > MAX_WEIGHT:
        cost = 0
    else:
        cost = sum([a * b for a, b in zip(individual, COSTS)])
    return cost


def get_n_largest(individuals, n):
    return heapq.nlargest(n, individuals, key=calculate_individual_cost)


def cross_over(individuals_new, r):
    crossed = []
    for i in range(r // 2):
        x= random.sample(individuals_new, 2)
        crossed += cross(*x)
    return crossed


def cross(i_a, i_b):
    cross_point = random.randint(0, len(i_a) - 1)
    a1 = i_a[0:cross_point]
    a2 = i_a[cross_point:len(i_a)]
    b1 = i_b[0:cross_point]
    b2 = i_b[cross_point: len(i_b)]
    return [a1 + b2, b1 + a2]


def mutate(individuals_new, j):
    indecies_to_mutate = random.sample(range(0, len(individuals_new)), j)
    for idx in indecies_to_mutate:
        bit = random.randint(0, len(individuals_new[idx]) - 1)
        individuals_new[idx][bit] += 1
        individuals_new[idx][bit] %= 2


def solve(p, r, m):
    population = gen_random_individuals()
    max_cost = 0
    number_of_sames = 0
    while number_of_sames < 200:
        p_new = get_n_largest(population, p - r)
        x = cross_over(p_new, r)
        mutate(x, m)
        p_new += x
        population = p_new
        max_cost_previous = max_cost
        max_cost = calculate_individual_cost(get_n_largest(population, 1)[0])
        if max_cost == max_cost_previous:
            number_of_sames += 1
        else:
            number_of_sames = 0
    return max_cost

print(solve(P, R, M))