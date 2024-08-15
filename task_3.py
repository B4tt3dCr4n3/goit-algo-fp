"""
Завдання 3. Дерева, алгоритм Дейкстри

Розробіть алгоритм Дейкстри для знаходження найкоротших шляхів у зваженому 
графі, використовуючи бінарну купу. Завдання включає створення графа, використання 
піраміди для оптимізації вибору вершин та обчислення найкоротших шляхів від 
початкової вершини до всіх інших.
"""

import heapq  # Імпортуємо модуль для роботи з бінарною купою

class Graph:
    """ Клас для зберігання графа та обчислення найкоротших шляхів методом Дейкстри """
    def __init__(self):
        self.nodes = set()  # Множина для зберігання вершин графа
        self.edges = {}     # Словник для зберігання ребер графа
        self.distances = {} # Словник для зберігання відстаней між вершинами

    def add_node(self, value):
        """ Додає вершину до графа """
        self.nodes.add(value)  # Додаємо вершину до множини вершин
        self.edges[value] = [] # Ініціалізуємо список суміжності для нової вершини

    def add_edge(self, from_node, to_node, distance):
        """ Додає ребро між двома вершинами """
        # Додаємо ребро між двома вершинами (в обох напрямках для неорієнтованого графа)
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        # Зберігаємо відстань між вершинами (в обох напрямках)
        self.distances[(from_node, to_node)] = distance
        self.distances[(to_node, from_node)] = distance

def dijkstra(graph, initial):
    """ Обчислює найкоротші відстані від початкової вершини до всіх інших вершин графа """
    # Ініціалізуємо відстані до всіх вершин як нескінченність
    distances = {node: float('infinity') for node in graph.nodes}
    distances[initial] = 0  # Відстань до початкової вершини - 0
    # Ініціалізуємо бінарну купу з початковою вершиною
    pq = [(0, initial)]
    # Словник для зберігання попередніх вершин у найкоротшому шляху
    previous_nodes = {node: None for node in graph.nodes}

    while pq:
        # Вибираємо вершину з найменшою відстанню
        current_distance, current_node = heapq.heappop(pq)

        # Якщо знайдено коротший шлях до цієї вершини, пропускаємо її
        if current_distance > distances[current_node]:
            continue

        # Перевіряємо всіх сусідів поточної вершини
        for neighbor in graph.edges[current_node]:
            # Обчислюємо відстань до сусіда через поточну вершину
            distance = current_distance + graph.distances[(current_node, neighbor)]

            # Якщо знайдено коротший шлях, оновлюємо інформацію
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                # Додаємо сусіда до бінарної купи для подальшого розгляду
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous_nodes

def print_result(distances, previous_nodes, start_node):
    """ Виводить результати обчислення найкоротших відстаней та шляхів """
    for node in distances:
        if node != start_node:
            path = []
            current = node
            # Відновлюємо шлях від кінцевої вершини до початкової
            while current is not None:
                path.append(current)
                current = previous_nodes[current]
            path = path[::-1]  # Розгортаємо шлях у правильному порядку
            print(f"Шлях від {start_node} до {node}: {' -> '.join(path)}, Відстань: {distances[node]}")

# Приклад використання
graph = Graph()
for node in ['A', 'B', 'C', 'D', 'E']:
    graph.add_node(node)

# Додаємо ребра з відстанями
graph.add_edge('A', 'B', 4)
graph.add_edge('A', 'C', 2)
graph.add_edge('B', 'D', 3)
graph.add_edge('C', 'D', 1)
graph.add_edge('C', 'E', 5)
graph.add_edge('D', 'E', 2)

start_node = 'A'
distances, previous_nodes = dijkstra(graph, start_node)
print_result(distances, previous_nodes, start_node)
