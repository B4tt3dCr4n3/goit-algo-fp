"""
Завдання 4. Візуалізація піраміди

Наступний код виконує побудову бінарних дерев. Виконайте аналіз коду, щоб зрозуміти, як він працює.

Використовуючи як базу цей код, побудуйте функцію, що буде візуалізувати бінарну купу.
"""

import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class HeapNode:
    """
    Клас, що представляє вузол у бінарній купі.
    """
    def __init__(self, key, color="skyblue"):
        self.left = None  # Лівий дочірній вузол
        self.right = None  # Правий дочірній вузол
        self.val = key  # Значення вузла
        self.color = color  # Колір вузла для візуалізації
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор вузла

def heap_to_tree(heap):
    """
    Перетворює список-купу в бінарне дерево.
    
    Args:
    heap (list): Список, що представляє мінімальну купу.
    
    Returns:
    HeapNode: Кореневий вузол побудованого бінарного дерева.
    """
    # Створюємо вузли для кожного елемента купи
    nodes = [HeapNode(val) for val in heap]
    
    # Встановлюємо зв'язки між вузлами
    for i in range(len(nodes)):
        left_child = 2 * i + 1
        right_child = 2 * i + 2
        # Якщо існує лівий дочірній вузол, встановлюємо зв'язок
        if left_child < len(nodes):
            nodes[i].left = nodes[left_child]
        # Якщо існує правий дочірній вузол, встановлюємо зв'язок
        if right_child < len(nodes):
            nodes[i].right = nodes[right_child]
    
    # Повертаємо кореневий вузол або None, якщо купа порожня
    return nodes[0] if nodes else None

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """
    Рекурсивно додає ребра та вузли до графа.
    
    Args:
    graph (nx.DiGraph): Граф NetworkX.
    node (HeapNode): Поточний вузол.
    pos (dict): Словник позицій вузлів.
    x, y (float): Координати поточного вузла.
    layer (int): Поточний рівень дерева.
    
    Returns:
    nx.DiGraph: Оновлений граф з доданими вузлами та ребрами.
    """
    if node is not None:
        # Додаємо вузол до графа
        graph.add_node(node.id, color=node.color, label=node.val)
        
        # Обробляємо лівого нащадка
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        
        # Обробляємо правого нащадка
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    
    return graph

def draw_heap(heap):
    """
    Візуалізує мінімальну купу.
    
    Args:
    heap (list): Список, що представляє мінімальну купу.
    """
    if not heap:
        print("Купа порожня")
        return

    # Перетворюємо купу на дерево
    root = heap_to_tree(heap)
    
    # Створюємо направлений граф
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}  # Початкова позиція кореня
    
    # Додаємо вузли та ребра до графа
    tree = add_edges(tree, root, pos)

    # Отримуємо кольори та мітки вузлів
    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    # Створюємо візуалізацію
    plt.figure(figsize=(12, 8))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.title("Візуалізація мінімальної купи")
    plt.show()

# Приклад використання
original_list = [100, 19, 36, 17, 10, 22, 3, 25, 33, 1, 77, 2, 7, 99, 4]

# Створення мінімальної купи за допомогою heapq
heap = []
for value in original_list:
    heapq.heappush(heap, value)  # Додаємо кожен елемент до купи

print("Оригінальний список:", original_list)
print("Мінімальна купа:", heap)

# Візуалізація мінімальної купи
draw_heap(heap)
