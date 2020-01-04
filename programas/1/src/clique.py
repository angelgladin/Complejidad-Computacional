import random


MAX_GRAPH_VERTICES = 10
MIN_GRAPH_VERTICES = 5


class Vertex:
    def __init__(self, id):
        self.id = id
        self.neighboors = set()

    def __str__(self):
        return 'id:{}, neighboors={}'.format(self.id, [x.id for x in self.neighboors])


class Graph:
    def __init__(self, n):
        self.vertices = dict()
        for i in range(n):
            self.vertices[i] = Vertex(i)

    def add_edge(self, u, v):
        u_vertex = self.vertices[u]
        v_vertex = self.vertices[v]

        u_vertex.neighboors.add(v_vertex)
        v_vertex.neighboors.add(u_vertex)

    def choose_k_random_vertices(self, k):
        vertices = set()
        while len(vertices) != k:
            x = random.randrange(len(self.vertices))
            vertices.add(x)
        return list(vertices)

    def is_complete(self):
        for u in self.vertices:
            for v in self.vertices:
                if u == v:
                    continue
                else:
                    u_neighboors = {x.id for x in self.vertices[u].neighboors}
                    if v not in u_neighboors:
                        return False
        return True

    def __str__(self):
        ans = ''
        for (_, v,) in self.vertices.items():
            ans += '{}\n'.format(v)
        return ans

    @staticmethod
    def induced_graph(graph, vertices):
        new_graph = Graph(0)

        for x in vertices:
            new_graph.vertices[x] = Vertex(x)

        for v in graph.vertices:
            for u in graph.vertices[v].neighboors:
                if v in vertices and u.id in vertices:
                    new_graph.add_edge(u.id, v)

        return new_graph

    @staticmethod
    def generate_random_graph(n):
        graph = Graph(n)

        for u in range(n):
            for v in range(u+1, n):
                add_edge = random.choice([True, False])
                if add_edge:
                    graph.add_edge(u, v)

        return graph


if __name__ == "__main__":
    vertices_n = random.randrange(MIN_GRAPH_VERTICES, MAX_GRAPH_VERTICES+1)
    print('Gráfica con {} vértices'.format(vertices_n))
    graph = Graph.generate_random_graph(vertices_n)
    print(graph)

    clique_n = random.randrange(1, vertices_n+1)
    print('¿G tiene un clan de tamaño {}?'.format(clique_n))
    print('Subconjunto S de vértices de tamaño k={}'.format(clique_n))
    clique_candidate_vertices = graph.choose_k_random_vertices(clique_n)
    print(clique_candidate_vertices)
    print('Gráfica inducida del subconjunto S')
    induced_graph = Graph.induced_graph(graph, clique_candidate_vertices)
    print(induced_graph)

    print('¿El clan dado es una gráfica completa? {}'.format(
        induced_graph.is_complete()))
