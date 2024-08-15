"""
Завдання 1. Структури даних. Сортування. Робота з однозв'язним списком

Для реалізації однозв'язного списку (приклад реалізації можна взяти з конспекту) необхідно:
написати функцію, яка реалізує реверсування однозв'язного списку, змінюючи посилання між вузлами;
розробити алгоритм сортування для однозв'язного списку, наприклад, сортування вставками або злиттям;
написати функцію, що об'єднує два відсортовані однозв'язні списки в один відсортований список."""

class Node:
    """ Клас, що представляє вузол однозв'язного списку. """
    def __init__(self, data=None):
        self.data = data  # Дані вузла
        self.next = None  # Посилання на наступний вузол

class LinkedList:
    """ Клас, що представляє однозв'язний список. """
    def __init__(self):
        self.head = None  # Голова списку (перший елемент)

    def insert_at_beginning(self, data):
        """
        Вставляє новий вузол на початок списку.

        Алгоритм:
        1. Створюємо новий вузол з переданими даними.
        2. Встановлюємо посилання нового вузла на поточну голову списку.
        3. Робимо новий вузол головою списку.

        :param data: Дані для нового вузла
        """
        new_node = Node(data)
        new_node.next = self.head  # Новий вузол вказує на поточну голову
        self.head = new_node  # Новий вузол стає новою головою

    def insert_at_end(self, data):
        """
        Вставляє новий вузол в кінець списку.

        Алгоритм:
        1. Створюємо новий вузол з переданими даними.
        2. Якщо список порожній, робимо новий вузол головою.
        3. Інакше, проходимо до кінця списку і додаємо новий вузол.

        :param data: Дані для нового вузла
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node  # Якщо список порожній, новий вузол стає головою
            return
        last = self.head
        while last.next:  # Знаходимо останній вузол
            last = last.next
        last.next = new_node  # Додаємо новий вузол в кінець

    def insert_after(self, prev_node: Node, data):
        """
        Вставляє новий вузол після вказаного вузла.

        Алгоритм:
        1. Перевіряємо, чи існує попередній вузол.
        2. Створюємо новий вузол з переданими даними.
        3. Змінюємо посилання для вставки нового вузла після попереднього.

        :param prev_node: Вузол, після якого потрібно вставити новий
        :param data: Дані для нового вузла
        """
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next  # Новий вузол вказує на наступний після prev_node
        prev_node.next = new_node  # prev_node тепер вказує на новий вузол

    def delete_node(self, key: int):
        """
        Видаляє перший вузол з вказаним значенням.

        Алгоритм:
        1. Якщо голова містить ключ, видаляємо її.
        2. Інакше, проходимо по списку, шукаючи вузол з ключем.
        3. Якщо знайдено, змінюємо посилання для видалення вузла.

        :param key: Значення вузла для видалення
        """
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next  # Якщо видаляємо голову, другий елемент стає головою
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return  # Елемент не знайдено
        prev.next = cur.next  # Змінюємо посилання, щоб "перестрибнути" видалений вузол
        cur = None

    def search_element(self, data: int) -> Node | None:
        """
        Шукає вузол з вказаним значенням.

        Алгоритм:
        1. Починаємо з голови списку.
        2. Проходимо по списку, порівнюючи дані кожного вузла.
        3. Повертаємо вузол, якщо знайдено, або None.

        :param data: Значення для пошуку
        :return: Знайдений вузол або None, якщо не знайдено
        """
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        """
        Виводить всі елементи списку.

        Алгоритм:
        1. Починаємо з голови списку.
        2. Проходимо по всіх вузлах, виводячи їх дані.
        3. Виводимо новий рядок в кінці.
        """
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print()

    def reverse(self):
        """
        Реверсує зв'язний список, змінюючи напрямок зв'язків між вузлами.

        Алгоритм:
        1. Ініціалізуємо три покажчики: prev, current і next_node.
        2. Ітеруємось по списку, на кожному кроці:
           - Зберігаємо наступний вузол
           - Змінюємо напрямок зв'язку поточного вузла на попередній
           - Рухаємо prev і current на один крок вперед
        3. В кінці, встановлюємо голову списку на останній вузол (який став першим)
        """
        prev = None
        current = self.head
        while current:
            next_node = current.next  # Зберігаємо посилання на наступний вузол
            current.next = prev  # Змінюємо напрямок зв'язку
            prev = current  # Рухаємо prev
            current = next_node  # Рухаємо current
        self.head = prev  # Оновлюємо голову списку

    def insertion_sort(self):
        """
        Сортує зв'язний список за допомогою алгоритму сортування вставками.

        Алгоритм:
        1. Починаємо з другого елемента списку (якщо він є).
        2. Для кожного елемента шукаємо правильну позицію в уже відсортованій частині:
           - Якщо елемент менший за голову, вставляємо його на початок.
           - Інакше, знаходимо правильну позицію і вставляємо елемент.
        3. Повторюємо, поки не дійдемо до кінця списку.
        """
        if not self.head or not self.head.next:
            return  # Список пустий або містить лише один елемент

        sorted_end = self.head
        while sorted_end.next:
            current = sorted_end.next  # Поточний елемент для вставки

            if current.data < self.head.data:
                # Якщо поточний елемент менший за голову, вставляємо його на початок
                sorted_end.next = current.next
                current.next = self.head
                self.head = current
            else:
                # Шукаємо правильну позицію для вставки
                search = self.head
                while search != sorted_end and search.next.data < current.data:
                    search = search.next
                if search != sorted_end:
                    # Вставляємо елемент в середину списку
                    sorted_end.next = current.next
                    current.next = search.next
                    search.next = current
                else:
                    # Елемент вже на правильній позиції
                    sorted_end = sorted_end.next

    @staticmethod
    def merge_sorted_lists(list1, list2):
        """
        Об'єднує два відсортовані зв'язні списки в один відсортований список.

        Алгоритм:
        1. Створюємо фіктивний вузол як початок результуючого списку.
        2. Порівнюємо елементи з обох списків і додаємо менший до результату.
        3. Повторюємо, поки не вичерпаються елементи в обох списках.
        4. Якщо в одному зі списків залишились елементи, додаємо їх до результату.
        5. Повертаємо новий об'єднаний список.

        :param list1: Голова першого відсортованого списку
        :param list2: Голова другого відсортованого списку
        :return: Новий об'єднаний відсортований список
        """
        dummy = Node(0)  # Фіктивний вузол для початку результуючого списку
        tail = dummy  # Хвіст результуючого списку

        while list1 and list2:
            if list1.data <= list2.data:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        
        # Додаємо залишок елементів, якщо вони є
        if list1:
            tail.next = list1
        if list2:
            tail.next = list2
        
        merged_list = LinkedList()
        merged_list.head = dummy.next  # Пропускаємо фіктивний вузол
        return merged_list

# Приклад використання

print("Демонстрація роботи з однозв'язним списком\n")

# Створення та заповнення першого списку
print("Створення першого списку:")
llist1 = LinkedList()
llist1.insert_at_end(3)
llist1.insert_at_end(1)
llist1.insert_at_end(15)
print("Перший список:")
llist1.print_list()

# Створення та заповнення другого списку
print("\nСтворення другого списку:")
llist2 = LinkedList()
llist2.insert_at_end(9)
llist2.insert_at_end(7)
llist2.insert_at_end(20)
print("Другий список:")
llist2.print_list()

# Реверсування першого списку
print("\nРеверсування першого списку:")
llist1.reverse()
print("Перший список після реверсування:")
llist1.print_list()

# Реверсування другого списку
print("\nРеверсування другого списку:")
llist2.reverse()
print("Другий список після реверсування:")
llist2.print_list()

# Сортування першого списку
print("\nСортування першого списку:")
llist1.insertion_sort()
print("Перший список після сортування:")
llist1.print_list()

# Сортування другого списку
print("\nСортування другого списку:")
llist2.insertion_sort()
print("Другий список після сортування:")
llist2.print_list()

# Об'єднання відсортованих списків
print("\nОб'єднання відсортованих списків:")
merged_list = LinkedList.merge_sorted_lists(llist1.head, llist2.head)
print("Об'єднаний відсортований список:")
merged_list.print_list()
