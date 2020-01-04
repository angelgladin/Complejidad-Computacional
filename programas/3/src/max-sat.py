# -*- coding: utf-8 -*-

from typing import List, Tuple, Dict, Set
from enum import Enum, auto
from dataclasses import dataclass

import random
import math


MIN_VARIABLES: int = 5
MAX_VARIABLES: int = 100
MIN_CLAUSES: int = 50
MAX_CLAUSES: int = 60
MIN_CLAUSE_SIZE: int = 3
MAX_CLAUSE_SIZE: int = 5

INITIAL_POPULATION_SIZE: int = 500

MUTATION_PROBABLITY_FACTOR: float = 0.2

STOP_CONDITION_MAX_ITERATIONS: int = int(1e5)
N_ITERATION_SHOW_PROGRESS: int = 250


@dataclass
class Variable:
    name: int
    is_negated: bool

    def __str__(self) -> str:
        return ('¬' if self.is_negated else '') + str(self.name)


@dataclass
class Clause:
    name: int
    variables: List[Variable]

    def __str__(self) -> str:
        return '(' + ' ∨ '.join(map(str, self.variables)) + ')'


@dataclass
class Instance:
    clauses: List[Clause]
    variables_ids: List[int]
    f_matrix: List[List[bool]]

    def __str__(self) -> str:
        s = ''
        s += ' ∧ '.join(map(str, self.clauses))
        s += '\n'
        s += ', '.join(map(str, self.variables_ids))
        s += '\n'
        s += '\n'.join(map(str, self.f_matrix))
        return s


@dataclass
class Individual:
    variable_values: List[bool]

    def __str__(self):
        return ''.join(map(lambda x: '1' if x else '0', self.variable_values))


def generate_random_clause(name: int, size: int, variables_id: List[int]) -> Clause:
    """Genera una cláusula de conjunjunción de variables.
    Se tomarán identificadores de la lista de variables_id para así crear variables
    en cada clásula.

    Arguments:
        name {int} -- El nombre de la cláusula
        variables {List[int]} -- Todas la variables de la instancia en la trabajamos.

    Returns:
        Clause -- Un clásula generada aleatoriamente
    """
    variables_names_sample: List[int] = random.sample(variables_id, size)

    variables: List[Variable] = []
    for x in variables_names_sample:
        variables.append(
            Variable(x, False if random.random() > 0.5 else True))

    return Clause(name, variables)


def random_values_list(n: int) -> List[bool]:
    """Crea un a lista con 'n' booleanos tomados aleatoriamente.

    Arguments:
        n {int} -- El tamaño de la lista a crear.

    Returns:
        List[bool] -- Una lista con booleanos.
    """
    l: List[bool] = [False]*n
    for i in range(n):
        l[i] = True if random.random() > 0.5 else False
    return l


def construct_f_matrix(n: int, m: int, clauses: List[Clause]) -> List[List[bool]]:
    """Matriz F generada de acuerdo a las especificaciones de la tarea.
    Dice si la entrada F_{i,j} de la clásula c_i contiene o no la variable x_j.
    M_1
    Arguments:
        n {int} -- Número de variables
        m {int} -- Número de cláusulas
        clauses {List[Clause]} -- Todas las cláusulas de nuestra instancia.

    Returns:
        List[List[bool]] -- La matriz F
    """
    indicator_matrix: List[List[bool]] = [[False]*n for _ in range(m)]
    for i in range(m):
        variables: List[int] = list(
            map(lambda x: x.name, clauses[i].variables))
        for j in variables:
            indicator_matrix[i][j] = True
    return indicator_matrix


def generate_instance(n: int, m: int) -> Instance:
    variables_ids: List[int] = list(range(n))
    clauses: List[Clause] = []

    for i in range(m):
        clause_size: int = random.randint(MIN_CLAUSE_SIZE, MAX_CLAUSE_SIZE)
        clauses.append(generate_random_clause(i, clause_size, variables_ids))

    f_matrix: List[List[bool]] = construct_f_matrix(n, m, clauses)

    return Instance(clauses, variables_ids, f_matrix)


class Genetic:

    class Crossover(Enum):
        PARTIALLY_MAP = auto()
        ORDERED = auto()

    class Mutation(Enum):
        DISPLACEMENT = auto()
        EXCHANGE = auto()

    class Population:

        def __init__(self, individuals: List[Individual], instance: Instance):
            self.individuals: List[Individual] = individuals
            self.instance: Instance = instance

        @staticmethod
        def generate_initial_population(n: int) -> List[Individual]:
            return [Individual(random_values_list(n))
                    for _ in range(INITIAL_POPULATION_SIZE)]

        def best_individual(self) -> Tuple[Individual, int]:
            best: Tuple[Individual, int] = (None, -math.inf,)
            for x in self.individuals:
                fitness: int = Genetic.fitness(x, self.instance)
                if fitness > best[1]:
                    best = (x, fitness,)
            return best

        def select_random_individual(self) -> Individual:
            n: int = len(self.individuals)
            random_idx: int = random.randint(0, n-1)
            return self.individuals[random_idx]

    @staticmethod
    def fitness(individual: Individual, instance: Instance) -> int:
        r: int = 0

        for c in instance.clauses:
            c_evaluated: bool = False
            for x in c.variables:
                var_name: int = x.name
                var_value: bool = individual.variable_values[var_name]
                var_value: bool = var_value if not x.is_negated else not var_value

                c_evaluated |= var_value
            if c_evaluated:
                r += 1

        return r

    @staticmethod
    def crossover(parent1: Individual, parent2: Individual, operator: Crossover) -> Individual:
        n: int = len(parent1.variable_values)

        if operator == Genetic.Crossover.PARTIALLY_MAP:
            raise NotImplementedError()

        elif operator == Genetic.Crossover.ORDERED:
            rnd_1_pointer: int = random.randint(0, n-1)
            rnd_2_pointer: int = random.randint(0, n-1)

            i: int = min(rnd_1_pointer, rnd_2_pointer)
            j: int = max(rnd_1_pointer, rnd_2_pointer)+1

            child_inherited_chunk: List[bool] = parent1.variable_values[i:j]

            return Individual(parent2.variable_values[:i] + child_inherited_chunk + parent2.variable_values[j:])

    @staticmethod
    def mutation(ind: Individual, operator: Mutation) -> Individual:
        evaluated_vars: List[bool] = ind.variable_values
        n: int = len(evaluated_vars)

        if operator == Genetic.Mutation.DISPLACEMENT:
            rnd_1_pointer: int = random.randint(0, n-1)
            rnd_2_pointer: int = random.randint(0, n-1)

            i: int = min(rnd_1_pointer, rnd_2_pointer)
            j: int = max(rnd_1_pointer, rnd_2_pointer)+1

            subgroup_1: List[bool] = []
            subgroup_2: List[bool] = []

            for idx in range(n):
                if idx > i and idx < j:
                    subgroup_2.append(evaluated_vars[idx])
                else:
                    subgroup_1.append(evaluated_vars[idx])

            rnd_gap: int = random.randint(0, len(subgroup_1)-1)
            mutated_evaluated_vars: List[bool] = \
                subgroup_1[:rnd_gap] + subgroup_2 + subgroup_1[rnd_gap:]

            return Individual(mutated_evaluated_vars)

        elif operator == Genetic.Mutation.EXCHANGE:
            swp_i_pointer: int = random.randint(0, n-1)
            swp_j_pointer: int = random.randint(0, n-1)

            while swp_i_pointer != swp_j_pointer:
                swp_j_pointer: int = random.randint(0, n-1)

            mutated_evaluated_vars: List[bool] = evaluated_vars.copy()
            aux: bool = mutated_evaluated_vars[swp_i_pointer]
            mutated_evaluated_vars[swp_i_pointer] = mutated_evaluated_vars[swp_j_pointer]
            mutated_evaluated_vars[swp_j_pointer] = aux

            return Individual(mutated_evaluated_vars)

    def __init__(self, n: int, m: int):
        self.n: int = n
        self.m: int = m

    def run(self) -> Individual:
        generation: int = 0

        individuals: List[Individual] = Genetic.Population.generate_initial_population(
            self.n)
        instance: Instance = generate_instance(self.n, self.m)

        population: Population = Genetic.Population(individuals, instance)

        best_individual: Tuple[Individual, int] = population.best_individual()

        print(str(population.best_individual()[0]))
        print(str(population.best_individual()[1]))

        for generation in range(STOP_CONDITION_MAX_ITERATIONS):
            if generation % N_ITERATION_SHOW_PROGRESS == 0:
                print(best_individual[0])
                print(best_individual[1])

            individual_1: Individual = population.select_random_individual()
            individual_2: Individual = population.select_random_individual()

            while individual_1 is individual_2:
                individual_2 = population.select_random_individual()

            new_individual: Individual = Genetic.crossover(
                individual_1, individual_2, Genetic.Crossover.ORDERED)

            new_individual_fitnees: int = Genetic.fitness(
                new_individual, instance)
            if new_individual_fitnees >= best_individual[1]:
                idx_random_crossover: int = random.randint(0, self.n-1)
                population.individuals[idx_random_crossover] = new_individual
                best_individual = (new_individual, new_individual_fitnees,)

            if random.random() <= MUTATION_PROBABLITY_FACTOR:
                mutated_individual: Individual = None
                if random.random() > 0.5:
                    mutated_individual: Individual = Genetic.mutation(
                        individual_1, Genetic.Mutation.DISPLACEMENT)
                else:
                    mutated_individual: Individual = Genetic.mutation(
                        individual_1, Genetic.Mutation.EXCHANGE)

                mutated_individual_fitnees: int = Genetic.fitness(
                    mutated_individual, instance)
                if mutated_individual_fitnees >= best_individual[1]:
                    idx_random_mutated: int = random.randint(0, self.n-1)
                    population.individuals[idx_random_mutated] = mutated_individual
                    best_individual = (mutated_individual,
                                       mutated_individual_fitnees,)

        return best_individual


if __name__ == "__main__":
    seed = 42
    random.seed(seed)

    n: int = random.randint(MIN_VARIABLES, MAX_VARIABLES)
    m: int = random.randint(MIN_CLAUSES, MAX_CLAUSES)

    g: Genetic = Genetic(n, m)

    best_found: Instance = g.run()
    print(best_found)
