import networkx as nx
import matplotlib.pyplot as plt



# Створення графу для моделювання транспортної мережі міста
G = nx.Graph()
nodes = ["A", "B", "C", "D", "E", "F", "G"]
G.add_nodes_from(nodes)
edges = [
    ("A", "B", 5),  
    ("A", "C", 7),
    ("B", "D", 3),
    ("C", "D", 4),
    ("C", "E", 6),
    ("D", "F", 2),
    ("E", "F", 8),
    ("E", "G", 5),
    ("F", "G", 3)
]
G.add_weighted_edges_from(edges)

# Реалізація алгоритму DFS
def dfs_recursive(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    visited.add(vertex)
    print(vertex, end=' ')  # Відвідуємо вершину
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
    return visited

#  Реалізація алгоритму BFS
from collections import deque

def bfs_iterative(graph, start):
    # Ініціалізація порожньої множини для зберігання відвіданих вершин
    visited = set()
    # Ініціалізація черги з початковою вершиною
    queue = deque([start])

    while queue:  # Поки черга не порожня, продовжуємо обхід
        # Вилучаємо першу вершину з черги
        vertex = queue.popleft()
        # Перевіряємо, чи була вершина відвідана раніше
        if vertex not in visited:
            # Якщо не була відвідана, друкуємо її
            print(vertex, end=" ")
            # Додаємо вершину до множини відвіданих вершин
            visited.add(vertex)
            # Додаємо всіх невідвіданих сусідів вершини до кінця черги
            # Операція різниці множин вилучає вже відвідані вершини зі списку сусідів
            queue.extend(set(graph[vertex]) - visited)
    # Повертаємо множину відвіданих вершин після завершення обходу
    return visited  




# Візуалізація графу
pos = nx.spring_layout(G, seed=42)  # Фіксоване розташування для стабільності
plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Транспортна мережа міста")
plt.show()

# Аналіз характеристик графу
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degrees = dict(G.degree())

print("Основні характеристики графу:")
print(f"Кількість вузлів: {num_nodes}")
print(f"Кількість ребер: {num_edges}")
print("Ступінь кожної вершини:")
for node, degree in degrees.items():
    print(f"  Вершина {node}: ступінь {degree}")


print("\nDFS (від вершини A):")
visited_dfs = dfs_recursive(G, "A")
print(f"\nВідвідані вершини (DFS): {visited_dfs}")

print("\nBFS (від вершини A):")
visited_bfs = bfs_iterative(G, "A")
print(f"\nВідвідані вершини (BFS): {visited_bfs}")


# Алгоритм Дейкстри
def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph.nodes}
    previous_nodes = {node: None for node in graph.nodes}
    distances[start] = 0
    unvisited = set(graph.nodes)

    while unvisited:
        # Знаходження вершини з найменшою відстанню серед невідвіданих
        current_node = min(unvisited, key=lambda node: distances[node])

        # Якщо поточна відстань нескінченність, завершити цикл
        if distances[current_node] == float('infinity'):
            break

        # Оновлення відстаней до сусідів
        for neighbor, attributes in graph[current_node].items():
            weight = attributes['weight']
            distance = distances[current_node] + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node

        unvisited.remove(current_node)

    # Формування шляхів
    paths = {node: [] for node in graph.nodes}
    for node in graph.nodes:
        current = node
        while current is not None:
            paths[node].insert(0, current)
            current = previous_nodes[current]

    return distances, paths


# Виконання алгоритму Дейкстри від вершини 'A'
distances, paths = dijkstra(G, "A")

# Виведення результатів
print("\nРезультати виконання алгоритму Дейкстри (від вершини 'A'):")
print("----------------------------------------------------------")
print(f"{'Цільова вершина':<15}  {'Довжина шляху':<15}{'Шлях'}")
print("----------------------------------------------------------")
for target in G.nodes:
    print(f"{target:<15}{distances[target]:<15}{' -> '.join(paths[target])}")

    


