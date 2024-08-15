"""
Завдання 5. Візуалізація обходу бінарного дерева

Використовуючи код із завдання 4 для побудови бінарного дерева, необхідно створити програму на Python, яка візуалізує обходи дерева: у глибину та в ширину.

Вона повинна відображати кожен крок у вузлах з різними кольорами, використовуючи 16-систему RGB (приклад #1296F0). Кольори вузлів мають змінюватися від темних до світлих відтінків, залежно від послідовності обходу. Кожен вузол при його відвідуванні має отримувати унікальний колір, який візуально відображає порядок обходу.

Примітка. Використовуйте стек та чергу, НЕ рекурсію
"""

import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

class HeapNode:
    """
    Клас для представлення вузла в бінарному дереві.
    Кожен вузол має значення, колір (для візуалізації), 
    посилання на лівого та правого нащадка, та унікальний ідентифікатор.
    """
    def __init__(self, key, color="#FFFFFF"):
        self.left = None  # Лівий дочірній вузол
        self.right = None  # Правий дочірній вузол
        self.val = key  # Значення вузла
        self.color = color  # Колір вузла для візуалізації (за замовчуванням білий)
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор вузла

def heap_to_tree(heap):
    """
    Перетворює список-купу в бінарне дерево.
    
    Args:
    heap (list): Список, що представляє мінімальну купу.
    
    Returns:
    HeapNode: Кореневий вузол побудованого бінарного дерева.
    
    Примітка: В купі, лівий дочірній елемент знаходиться за індексом 2i+1, 
    а правий - за індексом 2i+2, де i - індекс батьківського елемента.
    """
    nodes = [HeapNode(val) for val in heap]  # Створюємо вузли для кожного елемента купи
    for i in range(len(nodes)):
        left_child = 2 * i + 1
        right_child = 2 * i + 2
        # Встановлюємо зв'язки між вузлами
        if left_child < len(nodes):
            nodes[i].left = nodes[left_child]
        if right_child < len(nodes):
            nodes[i].right = nodes[right_child]
    return nodes[0] if nodes else None  # Повертаємо корінь дерева або None, якщо купа порожня

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
    
    Примітка: Ця функція також обчислює позиції вузлів для візуалізації.
    """
    if node is not None:
        # Додаємо вузол до графа
        graph.add_node(node.id, color=node.color, label=node.val)
        
        # Обробляємо лівого нащадка
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer  # Обчислюємо x-координату для лівого нащадка
            pos[node.left.id] = (l, y - 1)  # Встановлюємо позицію лівого нащадка
            # Рекурсивно обробляємо ліве піддерево
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        
        # Обробляємо правого нащадка
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer  # Обчислюємо x-координату для правого нащадка
            pos[node.right.id] = (r, y - 1)  # Встановлюємо позицію правого нащадка
            # Рекурсивно обробляємо праве піддерево
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    
    return graph

def generate_color(step, total_steps):
    """
    Генерує колір для вузла на основі кроку обходу.
    
    Args:
    step (int): Поточний крок обходу.
    total_steps (int): Загальна кількість кроків.
    
    Returns:
    str: Колір у форматі HTML (#RRGGBB).
    
    Примітка: Колір змінюється від темного до світлого відтінку базового кольору.
    """
    base_color = (18, 150, 240)  # Базовий колір #1296F0
    r, g, b = base_color
    # Змінюємо яскравість кольору залежно від кроку
    # Тепер перші кроки будуть темнішими, а останні - світлішими
    factor = 0.3 + (step / total_steps) * 0.7  # Змінюємо яскравість від 30% до 100%
    return f"#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}"

def dfs_traversal(root):
    """
    Виконує обхід дерева в глибину (DFS).
    
    Args:
    root (HeapNode): Кореневий вузол дерева.
    
    Returns:
    list: Список відвіданих вузлів у порядку обходу.
    
    Примітка: Використовується стек для реалізації DFS без рекурсії.
    """
    if not root:
        return []
    
    stack = [root]  # Ініціалізуємо стек кореневим вузлом
    visited = []  # Список для зберігання відвіданих вузлів
    
    while stack:
        node = stack.pop()  # Беремо вузол з вершини стеку
        if node not in visited:
            visited.append(node)
            # Додаємо правого нащадка першим, щоб лівий був оброблений раніше
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
    
    return visited

def bfs_traversal(root):
    """
    Виконує обхід дерева в ширину (BFS).
    
    Args:
    root (HeapNode): Кореневий вузол дерева.
    
    Returns:
    list: Список відвіданих вузлів у порядку обходу.
    
    Примітка: Використовується черга для реалізації BFS.
    """
    if not root:
        return []
    
    queue = deque([root])  # Ініціалізуємо чергу кореневим вузлом
    visited = []  # Список для зберігання відвіданих вузлів
    
    while queue:
        node = queue.popleft()  # Беремо вузол з початку черги
        if node not in visited:
            visited.append(node)
            # Додаємо лівого і правого нащадка до черги
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return visited

def create_tree_layout(root):
    """
    Створює макет дерева для візуалізації.
    
    Args:
    root (HeapNode): Кореневий вузол дерева.
    
    Returns:
    tuple: (nx.DiGraph, dict) - граф NetworkX та словник позицій вузлів.
    
    Примітка: Ця функція використовує add_edges для створення графа та обчислення позицій вузлів.
    """
    tree = nx.DiGraph()  # Створюємо направлений граф
    pos = {root.id: (0, 0)}  # Початкова позиція кореня
    tree = add_edges(tree, root, pos)  # Додаємо всі вузли та ребра до графа
    return tree, pos

def update(frame, tree, pos, visited_nodes, ax, traversal_type):
    """
    Оновлює візуалізацію для кожного кадру анімації.
    
    Args:
    frame (int): Номер поточного кадру.
    tree (nx.DiGraph): Граф дерева.
    pos (dict): Словник позицій вузлів.
    visited_nodes (list): Список відвіданих вузлів.
    ax (matplotlib.axes.Axes): Об'єкт осей для малювання.
    traversal_type (str): Тип обходу ('DFS' або 'BFS').
    
    Примітка: Ця функція викликається для кожного кадру анімації.
    """
    ax.clear()  # Очищуємо попередній кадр
    colors = []
    labels = {}
    
    # Оновлюємо кольори та мітки вузлів
    for node in tree.nodes(data=True):
        node_id = node[0]
        node_data = node[1]
        if node_data['label'] in [vn.val for vn in visited_nodes[:frame+1]]:
            # Якщо вузол вже відвіданий, генеруємо для нього колір
            node_data['color'] = generate_color(
                [vn.val for vn in visited_nodes].index(node_data['label']) + 1, 
                len(visited_nodes)
            )
        else:
            node_data['color'] = "#FFFFFF"  # Білий колір для невідвіданих вузлів
        colors.append(node_data['color'])
        labels[node_id] = node_data['label']
    
    # Малюємо граф
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors, ax=ax)
    
    # Додаємо текст, який показує поточний стан стеку/черги
    if traversal_type == "DFS":
        stack_text = f"Стек: {[node.val for node in visited_nodes[frame+1:][::-1]]}"
        ax.text(0.05, -0.1, stack_text, transform=ax.transAxes, fontsize=10, verticalalignment='top')
    else:  # BFS
        queue_text = f"Черга: {[node.val for node in visited_nodes[frame+1:]]}"
        ax.text(0.05, -0.1, queue_text, transform=ax.transAxes, fontsize=10, verticalalignment='top')
    
    ax.set_title(f"{traversal_type}: Крок {frame+1}/{len(visited_nodes)}")
    
    # Прибираємо осі координат
    ax.axis('off')

def animate_traversal(root, traversal_func, title, traversal_type):
    """
    Створює анімацію обходу дерева.
    
    Args:
    root (HeapNode): Кореневий вузол дерева.
    traversal_func (function): Функція обходу (dfs_traversal або bfs_traversal).
    title (str): Заголовок анімації.
    traversal_type (str): Тип обходу ('DFS' або 'BFS').
    
    Примітка: Ця функція створює та відображає анімацію обходу дерева.
    """
    tree, pos = create_tree_layout(root)
    visited_nodes = traversal_func(root)
    
    # Використовуємо constrained_layout для автоматичного налаштування відступів
    fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)
    
    # Прибираємо осі координат для всього графіка
    plt.axis('off')
    
    # Створюємо анімацію
    ani = FuncAnimation(fig, update, frames=len(visited_nodes), fargs=(tree, pos, visited_nodes, ax, traversal_type),
                        interval=1000, repeat=False)
    
    plt.title(title)
    plt.show()

# Приклад використання
original_list = [100, 19, 36, 17, 10, 22, 3, 25, 33, 1, 77, 2, 7, 99, 4]
heap = []
for value in original_list:
    heapq.heappush(heap, value)  # Створюємо мінімальну купу

root = heap_to_tree(heap)  # Перетворюємо купу на дерево

# Анімація DFS
animate_traversal(root, dfs_traversal, "Обхід у глибину (DFS)", "DFS")

# Анімація BFS
animate_traversal(root, bfs_traversal, "Обхід у ширину (BFS)", "BFS")
