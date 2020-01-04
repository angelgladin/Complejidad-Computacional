# -*- coding: utf-8 -*-

from typing import List, Tuple, Dict, Set
from enum import Enum, auto
from dataclasses import dataclass

import matplotlib.pyplot as plt
import networkx as nx

import random
import math

from constants import *


@dataclass
class ColourClass:
    colour: int
    vertices_with_that_colour: List[int]


def create_k_partitte_graph(n: int, k: int) -> nx.classes.graph.Graph:
    return nx.turan_graph(n, k)


def initialise_trail_matrix(n: int) -> List[List[float]]:
    m: List[List[float]] = [[1]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                m[i][j] = n
    return m


def initialise_trail_update_matrix(n: int) -> List[List[float]]:
    m: List[List[float]] = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                m[i][j] = n
    return m


def select_random_vertex(F: List[int]) -> int:
    return random.choice(F)


def update_trail_update_matrix(G, delta, k) -> None:
    increase_factor: float = 1 / (k+1)
    for i in range(len(delta)):
        for j in range(len(delta[i])):
            if i != j and G.nodes[i]['color'] == G.nodes[k]['color']:
                delta[i][j] += increase_factor


def update_trail_matrix(G, delta, t, rho) -> None:
    for i in range(len(delta)):
        for j in range(len(delta[i])):
            if i != j:
                t[i][j] = t[i][j] * rho + delta[i][j]


def get_color_class(colour_classes: List[ColourClass], k: int) -> ColourClass:
    for x in colour_classes:
        if x.colour == k:
            return x
    return None


def gamma_f(G, F, i):
    neighbors = []
    for v in F:
        if v in G.adj[i]:
            neighbors.append(v)
    return neighbors


def colour_vertex(G, i, k, F, X, colour_classes) -> None:
    diff: List = lambda l1, l2: [x for x in l1 if x not in l2]
    union: List = lambda l1, l2: list(set(l1) | set(l2))

    G.nodes[i]['color'] = k
    C_k = get_color_class(colour_classes, k)
    gamma: List[int] = gamma_f(G, F, i)

    X.remove(i)
    C_k.vertices_with_that_colour.append(i)
    F = diff(F, union(gamma, [i]))


def vertex_map_vertex_id_color(k: int) -> str:
    l = ['indigo', 'lime', 'coral', 'brown', 'green',
         'fuchsia', 'aqua', 'gold', 'magenta', 'orange', 'tomato', 'teal']
    return l[k]


def ant_col(G, n_cycles, n_ants, alpha, beta, rho) -> None:

    colour_class_list: List[ColourClass] = []

    V: List[int] = list(G.nodes())
    n: int = len(V)
    t: List[List[float]] = initialise_trail_matrix(n)

    for cycle in range(1, n_cycles+1):
        delta: List[List[float]] = initialise_trail_update_matrix(n)

        for ant in range(1, n_ants+1):
            X: List[int] = V
            k: int = 0
            while X:
                k: int = k + 1
                C_k: ColourClass = ColourClass(k, [])
                colour_class_list.append(C_k)
                F: List[int] = X

                i: int = select_random_vertex(F)

                colour_vertex(G, i, k, F, X, colour_class_list)

                while F:
                    i: int = select_random_vertex(F)
                    colour_vertex(G, i, k, F, X, colour_class_list)

            update_trail_update_matrix(G, delta, k)
        update_trail_matrix(G, delta, t, rho)


def color_graph(G, k) -> Tuple[List[ColourClass], int]:
    def n_empty_lists(l):
        ans = 0
        for x in l:
            ans += 1 if x else 0
        return ans

    colour_classes = None
    colors_used = 0
    while colors_used <= k:
        candidate = random.randint(k, MAX_K_PARTITE_GRAPH_SIZE)
        colour_classes = [None] * candidate
        for i in range(k+1):
            new = ColourClass(i, [])
            colour_classes[i] = new
        for v in G.nodes:
            aux = random.randrange(len(colour_classes))
            colour_classes[aux].vertices_with_that_colour.append(v)
            G.nodes[v]['color'] = aux
        colors_used = n_empty_lists(colour_classes)
    return (colour_classes, colors_used,)

def colors_for_graph(G, colour_classes) -> List[str]:
    n = len(G.nodes)
    l = [0]*n
    for x in colour_classes:
        for v in x.vertices_with_that_colour:
            l[v] = x.colour
    aux = []
    for i in l:
        aux.append(vertex_map_vertex_id_color(i))
    return aux


if __name__ == "__main__":
    random.seed(RANDOM_SEED)

    k: int = random.randint(MIN_K_PARTITE_GRAPH_SIZE, MAX_K_PARTITE_GRAPH_SIZE)
    G = create_k_partitte_graph(N_GRAPH_VERTICES, k)

    print('Gráfica k-partita aleatoria generada')
    print('Para ejecutar la heurística, cerrar la ventana que muestra la gráfica')
    nx.draw(G, with_labels=True)
    plt.show()

    ant_col(G, N_CYCLES, N_ANTS, PARAM_ALPHA, PARAM_BETA, PARAM_RHO)

    (colour_classes, colors_used,) = color_graph(G, k)

    print(f'Gráfica propuesta con {colors_used} colores usados')
    vertices_colors = colors_for_graph(G, colour_classes)
    nx.draw(G, with_labels=True, node_color=vertices_colors)
    plt.show()
