import sys
import heapq


INF = 10**18


class Graph:
    def __init__(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices
        self.adjacency_list = [[] for _ in range(number_of_vertices)]

    def add_edge(self, source, destination, cost):
        self.adjacency_list[source].append((destination, cost))

    def dijkstra(self, source, target):
        distances = [INF] * self.number_of_vertices
        distances[source] = 0

        priority_queue = [(0, source)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance != distances[current_vertex]:
                continue

            if current_vertex == target:
                return current_distance

            for neighbor, edge_cost in self.adjacency_list[current_vertex]:
                new_distance = current_distance + edge_cost

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        return distances[target]


def get_next_non_empty_line(lines, index):
    while index < len(lines) and lines[index].strip() == "":
        index += 1

    if index >= len(lines):
        return None, index

    return lines[index].strip(), index + 1


def main():
    lines = sys.stdin.read().splitlines()
    index = 0
    output = []

    line, index = get_next_non_empty_line(lines, index)
    number_of_tests = int(line)

    for _ in range(number_of_tests):
        line, index = get_next_non_empty_line(lines, index)
        number_of_cities = int(line)

        graph = Graph(number_of_cities)
        city_name_to_index = {}

        for city_index in range(number_of_cities):
            city_name, index = get_next_non_empty_line(lines, index)
            city_name_to_index[city_name] = city_index

            line, index = get_next_non_empty_line(lines, index)
            number_of_neighbors = int(line)

            for _ in range(number_of_neighbors):
                line, index = get_next_non_empty_line(lines, index)
                neighbor_index, cost = map(int, line.split())

                destination = neighbor_index - 1
                graph.add_edge(city_index, destination, cost)

        line, index = get_next_non_empty_line(lines, index)
        number_of_queries = int(line)

        for _ in range(number_of_queries):
            line, index = get_next_non_empty_line(lines, index)
            source_name, target_name = line.split()

            source = city_name_to_index[source_name]
            target = city_name_to_index[target_name]

            minimum_cost = graph.dijkstra(source, target)
            output.append(str(minimum_cost))

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()