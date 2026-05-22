import math
import sys


class UnionFind:

    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a

        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1

        return True


def euclidean_distance(point_a, point_b):
    dx = point_a[0] - point_b[0]
    dy = point_a[1] - point_b[1]
    return math.sqrt(dx * dx + dy * dy)


def minimum_new_cable_length(n, k, existing_cables, coordinates):
    uf = UnionFind(n)

    # As primeiras K casas sao acessiveis por terra, entao ja pertencem
    # ao mesmo componente conectado sem custo de cabo novo.
    for house in range(1, k):
        uf.union(0, house)

    # Cabos existentes tambem tem custo zero.
    for u, v in existing_cables:
        uf.union(u - 1, v - 1)

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            distance = euclidean_distance(coordinates[i], coordinates[j])
            edges.append((distance, i, j))

    edges.sort()

    total = 0.0
    for distance, u, v in edges:
        if uf.union(u, v):
            total += distance

    return total


def main():
    tokens = sys.stdin.read().strip().split()
    if not tokens:
        return

    index = 0
    n = int(tokens[index])
    index += 1
    k = int(tokens[index])
    index += 1
    m = int(tokens[index])
    index += 1

    coordinates = []
    for _ in range(n):
        x = float(tokens[index])
        y = float(tokens[index + 1])
        index += 2
        coordinates.append((x, y))

    existing_cables = []
    for _ in range(m):
        u = int(tokens[index])
        v = int(tokens[index + 1])
        index += 2
        existing_cables.append((u, v))

    answer = minimum_new_cable_length(n, k, existing_cables, coordinates)
    print(f"{answer:.6f}")


if __name__ == "__main__":
    main()
