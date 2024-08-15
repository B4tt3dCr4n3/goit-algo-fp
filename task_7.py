"""
Завдання 7. Використання методу Монте-Карло

Необхідно написати програму на Python, яка імітує велику кількість кидків 
кубиків, обчислює суми чисел, які випадають на кубиках, і визначає ймовірність 
кожної можливої суми.

Створіть симуляцію, де два кубики кидаються велику кількість разів. Для кожного 
кидка визначте суму чисел, які випали на обох кубиках. Підрахуйте, скільки разів 
кожна можлива сума (від 2 до 12) з’являється у процесі симуляції. Використовуючи 
ці дані, обчисліть імовірність кожної суми.

На основі проведених імітацій створіть таблицю або графік, який відображає 
ймовірності кожної суми, виявлені за допомогою методу Монте-Карло.

Таблиця ймовірностей сум при киданні двох кубиків виглядає наступним чином.

2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 7: 6/36, 8: 5/36, 9: 4/36, 
10: 3/36, 11: 2/36, 12: 1/36

Порівняйте отримані за допомогою методу Монте-Карло результати з аналітичними 
розрахунками, наведеними в таблиці вище.
"""

import random
import matplotlib.pyplot as plt

def roll_dice():
    """
    Симулює кидок двох кубиків.
    
    Returns:
        int: Сума чисел на двох кубиках (від 2 до 12).
    """
    return random.randint(1, 6) + random.randint(1, 6)

def monte_carlo_simulation(num_rolls):
    """
    Проводить симуляцію методом Монте-Карло для кидків кубиків.
    
    Args:
        num_rolls (int): Кількість кидків для симуляції.
    
    Returns:
        dict: Словник з ймовірностями для кожної можливої суми.
    """
    # Ініціалізуємо словник для підрахунку кількості кожної суми
    sums = {i: 0 for i in range(2, 13)}
    
    # Проводимо симуляцію
    for _ in range(num_rolls):
        roll_sum = roll_dice()
        sums[roll_sum] += 1
    
    # Обчислюємо ймовірності
    probabilities = {k: v / num_rolls for k, v in sums.items()}
    return probabilities

def analytical_probabilities():
    """
    Повертає аналітично розраховані ймовірності для сум при киданні двох кубиків.
    
    Returns:
        dict: Словник з аналітичними ймовірностями для кожної можливої суми.
    """
    return {
        2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 7: 6/36,
        8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
    }

def plot_results(monte_carlo_probs, analytical_probs):
    """
    Створює графік, який порівнює результати методу Монте-Карло з аналітичними розрахунками.
    Ймовірності відображаються у відсотках без підписів над стовпчиками.
    
    Args:
        monte_carlo_probs (dict): Ймовірності, отримані методом Монте-Карло.
        analytical_probs (dict): Аналітично розраховані ймовірності.
    """
    sums = list(range(2, 13))
    
    # Конвертуємо ймовірності у відсотки
    monte_carlo_percentages = {k: v * 100 for k, v in monte_carlo_probs.items()}
    analytical_percentages = {k: v * 100 for k, v in analytical_probs.items()}
    
    plt.figure(figsize=(12, 6))
    # Створюємо групові стовпчики для порівняння
    plt.bar([x - 0.2 for x in sums], monte_carlo_percentages.values(), width=0.4, label='Monte Carlo', align='center')
    plt.bar([x + 0.2 for x in sums], analytical_percentages.values(), width=0.4, label='Analytical', align='center')
    
    plt.xlabel('Сума')
    plt.ylabel('Ймовірність (%)')
    plt.title('Порівняння ймовірностей: Монте-Карло vs Аналітичний розрахунок')
    plt.legend()
    plt.xticks(sums)
    
    plt.ylim(0, max(max(monte_carlo_percentages.values()), max(analytical_percentages.values())) * 1.1)  # Додаємо 10% зверху для кращого вигляду
    plt.show()

def main():
    """
    Головна функція, яка керує процесом симуляції та виведенням результатів.
    """
    # Кількість кидків для симуляції
    num_rolls = 1000000
    
    # Проводимо симуляцію методом Монте-Карло
    monte_carlo_probs = monte_carlo_simulation(num_rolls)
    
    # Отримуємо аналітичні ймовірності
    analytical_probs = analytical_probabilities()
    
    # Виводимо результати
    print("Результати методу Монте-Карло:")
    for sum_value, prob in monte_carlo_probs.items():
        print(f"Сума {sum_value}: {prob*100:.2f}%")
    
    print("\nАналітичні результати:")
    for sum_value, prob in analytical_probs.items():
        print(f"Сума {sum_value}: {prob*100:.2f}%")
    
    # Створюємо графік для порівняння результатів
    plot_results(monte_carlo_probs, analytical_probs)

if __name__ == "__main__":
    main()
