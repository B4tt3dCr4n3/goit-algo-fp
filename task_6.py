"""
Завдання 6. Жадібні алгоритми та динамічне програмування

Необхідно написати програму на Python, яка використовує два підходи — жадібний 
алгоритм та алгоритм динамічного програмування для розв’язання задачі вибору їжі 
з найбільшою сумарною калорійністю в межах обмеженого бюджету.

Кожен вид їжі має вказану вартість і калорійність. Дані про їжу представлені у 
вигляді словника, де ключ — назва страви, а значення — це словник з вартістю та 
калорійністю.

Розробіть функцію greedy_algorithm жадібного алгоритму, яка вибирає страви, 
максимізуючи співвідношення калорій до вартості, не перевищуючи заданий бюджет.
Для реалізації алгоритму динамічного програмування створіть функцію 
dynamic_programming, яка обчислює оптимальний набір страв для максимізації 
калорійності при заданому бюджеті.
"""

# Дані про їжу: словник, де ключ - назва страви, 
# а значення - словник з вартістю та калорійністю
items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}

def greedy_algorithm(budget, items):
    """
    Жадібний алгоритм для вибору страв.
    
    Аргументи:
    budget -- доступний бюджет
    items -- словник з інформацією про страви
    
    Повертає:
    Кортеж з трьох елементів: список вибраних страв, загальна вартість, загальна калорійність
    """
    # Сортуємо страви за співвідношенням калорій до вартості у спадаючому порядку
    # Використовуємо lambda-функцію для обчислення цього співвідношення
    sorted_items = sorted(items.items(), key=lambda x: x[1]['calories'] / x[1]['cost'], reverse=True)
    
    selected_items = []
    total_cost = 0
    total_calories = 0
    
    # Проходимо по відсортованому списку страв
    for item, info in sorted_items:
        # Якщо можемо дозволити собі страву в межах залишку бюджету
        if total_cost + info['cost'] <= budget:
            selected_items.append(item)
            total_cost += info['cost']
            total_calories += info['calories']
    
    return selected_items, total_cost, total_calories

def dynamic_programming(budget, items):
    """
    Алгоритм динамічного програмування для вибору страв.
    
    Аргументи:
    budget -- доступний бюджет
    items -- словник з інформацією про страви
    
    Повертає:
    Кортеж з трьох елементів: список вибраних страв, загальна вартість, загальна калорійність
    """
    # Створюємо двовимірну таблицю для динамічного програмування
    # Рядки відповідають стравам, стовпці - можливим значенням бюджету
    dp = [[0 for _ in range(budget + 1)] for _ in range(len(items) + 1)]
    
    # Заповнюємо таблицю
    for i, (item, info) in enumerate(items.items(), 1):
        for j in range(1, budget + 1):
            if info['cost'] <= j:
                # Вибираємо максимум між:
                # 1) не брати поточну страву (dp[i-1][j])
                # 2) взяти поточну страву (dp[i-1][j-info['cost']] + info['calories'])
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-info['cost']] + info['calories'])
            else:
                # Якщо страва занадто дорога, просто копіюємо попереднє значення
                dp[i][j] = dp[i-1][j]
    
    # Відновлюємо вибрані страви
    selected_items = []
    j = budget
    for i in range(len(items), 0, -1):
        if dp[i][j] != dp[i-1][j]:
            # Якщо значення змінилося, значить ми взяли цю страву
            item = list(items.keys())[i-1]
            selected_items.append(item)
            j -= items[item]['cost']
    
    # Загальна калорійність - це останній елемент таблиці dp
    total_calories = dp[-1][-1]
    # Загальна вартість - сума вартостей вибраних страв
    total_cost = sum(items[item]['cost'] for item in selected_items)
    
    return selected_items, total_cost, total_calories

# Тестування алгоритмів
budget = 100

print("Жадібний алгоритм:")
greedy_result = greedy_algorithm(budget, items)
print(f"Вибрані страви: {greedy_result[0]}")
print(f"Загальна вартість: {greedy_result[1]}")
print(f"Загальна калорійність: {greedy_result[2]}")

print("\nДинамічне програмування:")
dp_result = dynamic_programming(budget, items)
print(f"Вибрані страви: {dp_result[0]}")
print(f"Загальна вартість: {dp_result[1]}")
print(f"Загальна калорійність: {dp_result[2]}")
