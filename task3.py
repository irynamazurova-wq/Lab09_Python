class Apple:

    states = ["Відсутнє", "Цвітіння", "Зелене", "Червоне"]

    def __init__(self, index):
        self._index = index        # Номер яблука
        self._state = 0            # Початковий стан (індекс 0 -> "Відсутнє")

    def grow(self):

        if self._state < len(Apple.states) - 1:
            self._state += 1

    def is_ripe(self):

        return self._state == len(Apple.states) - 1

    def get_status(self):

        return Apple.states[self._state]


class AppleTree:
    def __init__(self, amount):

        self.apples = [Apple(i) for i in range(amount)]

    def grow_all(self):

        for apple in self.apples:
            apple.grow()

    def all_are_ripe(self):

        return all([apple.is_ripe() for apple in self.apples])

    def give_away_all(self):

        self.apples = []


class Gardener:
    def __init__(self, name, tree):
        self.name = name
        self._tree = tree

    def work(self):
        print(f"Садівник {self.name} працює...")
        self._tree.grow_all()
        if self._tree.apples:
             print(f"--> Стан яблук покращився: {self._tree.apples[0].get_status()}")

    def harvest(self):
        print(f"Садівник {self.name} перевіряє яблука...")
        if self._tree.apples and self._tree.all_are_ripe():
            self._tree.give_away_all()
            print("Врожай зібрано. Дерево пусте.")
        else:
            print("Яблука ще не дозріли або їх немає.")

    @staticmethod
    def apple_base(tree):
        print("\n--- Apple Base (Довідка)")
        if not tree.apples:
            print("Дерево пусте.")
        else:
            print(f"Кількість яблук: {len(tree.apples)}")
            print(f"Поточна стадія: {tree.apples[0].get_status()}")
        print("----------------------------\n")

print("--- 1. Створення окремих яблук (Тест класу Apple)")
a1 = Apple(1)
a2 = Apple(2)
print(f"Яблуко 1: {a1.get_status()}")
a1.grow()
print(f"Яблуко 1 після росту: {a1.get_status()}")

print("\n--- 2. Створення Дерева та Садівника")
tree = AppleTree(10)          # Дерево з 10 яблуками
gardener = Gardener("Олег", tree)

Gardener.apple_base(tree)

print("--- 3. Робота садівника (Цикл росту)")
gardener.harvest()

gardener.work()
gardener.work()
print("\nСпроба зібрати зелені яблука:")
gardener.harvest()

print("\nПрацюємо далі...")
gardener.work()

print("\n--- 4. Збір врожаю")
Gardener.apple_base(tree)
gardener.harvest()
Gardener.apple_base(tree)