from heapq import heappop, heappush
import sys


INF = 10 ** 18


def read_all_input():
    try:
        return sys.stdin.buffer.read().split()
    except AttributeError:
        return sys.stdin.read().split()


def dijkstra(graph, source, target, distance, mark, run_id):
    if source == target:
        return 0

    distance[source] = 0
    mark[source] = run_id

    heap = [(0, source)]

    while heap:
        cost, city = heappop(heap)

        if mark[city] != run_id or cost != distance[city]:
            continue

        if city == target:
            return cost

        adjacency = graph[city]
        adjacency_size = len(adjacency)
        i = 0

        while i < adjacency_size:
            neighbor = adjacency[i]
            edge_cost = adjacency[i + 1]
            i += 2

            new_cost = cost + edge_cost

            if mark[neighbor] != run_id or new_cost < distance[neighbor]:
                mark[neighbor] = run_id
                distance[neighbor] = new_cost
                heappush(heap, (new_cost, neighbor))

    return INF


def main():
    data = read_all_input()
    if not data:
        return

    pos = 0
    output = []

    test_count = int(data[pos])
    pos += 1
    run_id = 0

    for _ in range(test_count):
        city_count = int(data[pos])
        pos += 1

        name_to_index = {}
        graph = [[] for _ in range(city_count)]

        for city in range(city_count):
            name_to_index[data[pos]] = city
            pos += 1

            neighbor_count = int(data[pos])
            pos += 1

            adjacency = graph[city]
            for _ in range(neighbor_count):
                neighbor = int(data[pos]) - 1
                cost = int(data[pos + 1])
                pos += 2
                adjacency.append(neighbor)
                adjacency.append(cost)

        distance = [0] * city_count
        mark = [0] * city_count

        query_count = int(data[pos])
        pos += 1

        for _ in range(query_count):
            source = name_to_index[data[pos]]
            target = name_to_index[data[pos + 1]]
            pos += 2

            run_id += 1
            output.append(str(dijkstra(graph, source, target, distance, mark, run_id)))

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()
