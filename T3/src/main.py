from collections import deque
import sys


class Edge:
    def __init__(self, to, rev, capacity):
        self.to = to
        self.rev = rev
        self.capacity = capacity
        self.original_capacity = capacity


def add_edge(graph, u, v, capacity):
    forward = Edge(v, len(graph[v]), capacity)
    backward = Edge(u, len(graph[u]), 0)
    graph[u].append(forward)
    graph[v].append(backward)
    return len(graph[u]) - 1


def bfs(graph, source, sink, parent):
    for i in range(len(parent)):
        parent[i] = None

    queue = deque([source])
    parent[source] = (-1, -1)

    while queue:
        u = queue.popleft()

        for edge_index, edge in enumerate(graph[u]):
            if parent[edge.to] is None and edge.capacity > 0:
                parent[edge.to] = (u, edge_index)
                if edge.to == sink:
                    return True
                queue.append(edge.to)

    return False


def edmonds_karp(graph, source, sink):
    flow = 0
    parent = [None] * len(graph)

    while bfs(graph, source, sink, parent):
        path_flow = 10**18
        current = sink

        while current != source:
            previous, edge_index = parent[current]
            path_flow = min(path_flow, graph[previous][edge_index].capacity)
            current = previous

        current = sink

        while current != source:
            previous, edge_index = parent[current]
            edge = graph[previous][edge_index]
            reverse_edge = graph[edge.to][edge.rev]

            edge.capacity -= path_flow
            reverse_edge.capacity += path_flow

            current = previous

        flow += path_flow

    return flow


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    iterator = iter(data)
    n = int(next(iterator))
    m = int(next(iterator))
    k = int(next(iterator))

    source = 0
    boys_start = 1
    girls_start = boys_start + n
    sink = girls_start + m
    total_vertices = sink + 1

    graph = [[] for _ in range(total_vertices)]
    pair_edges = []

    for boy in range(1, n + 1):
        add_edge(graph, source, boys_start + boy - 1, 1)

    for girl in range(1, m + 1):
        add_edge(graph, girls_start + girl - 1, sink, 1)

    for _ in range(k):
        boy = int(next(iterator))
        girl = int(next(iterator))
        boy_vertex = boys_start + boy - 1
        girl_vertex = girls_start + girl - 1
        edge_index = add_edge(graph, boy_vertex, girl_vertex, 1)
        pair_edges.append((boy, girl, boy_vertex, edge_index))

    maximum_pairs = edmonds_karp(graph, source, sink)

    chosen_pairs = []
    for boy, girl, boy_vertex, edge_index in pair_edges:
        edge = graph[boy_vertex][edge_index]
        if edge.original_capacity == 1 and edge.capacity == 0:
            chosen_pairs.append((boy, girl))

    output = [str(maximum_pairs)]
    output.extend(f"{boy} {girl}" for boy, girl in chosen_pairs)
    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()
