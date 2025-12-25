class House:
    def __init__(self, area, price):
        self._area = area
        self._price = price

    def final_price(self, discount):
        final = self._price * (100 - discount) / 100
        return final


class SmallHouse(House):
    def __init__(self, price):
        super().__init__(40, price)


class Human:
    default_name = "NoName"
    default_age = 0

    def __init__(self, name=default_name, age=default_age):
        self.name = name
        self.age = age
        self.__money = 0
        self.__house = None

    def info(self):
        print(f"Ім'я: {self.name}")
        print(f"Вік: {self.age}")
        print(f"Гроші: {self.__money}")
        print(f"Будинок: {self.__house}")

    @staticmethod
    def default_info():
        print(f"Default Name: {Human.default_name}")
        print(f"Default Age: {Human.default_age}")

    def __make_deal(self, house, price):
        self.__money -= price
        self.__house = house

    def earn_money(self, amount):
        self.__money += amount
        print(f"Зароблено {amount} грошей. Поточний рахунок: {self.__money}")

    def buy_house(self, house, discount=10):
        price = house.final_price(discount)

        if self.__money >= price:
            self.__make_deal(house, price)
            print(f"Будинок успішно придбано! Ціна зі знижкою: {price}")
        else:
            print(f"Недостатньо грошей! Потрібно {price}, а є {self.__money}")


print("--- 1. Статичний метод")
Human.default_info()

print("\n--- 2. Створення об'єкта Human")
user = Human("Катя", 25)
user.info()

print("\n--- 3. Створення будинку і спроба покупки (без грошей)")
small_house = SmallHouse(8500)

user.buy_house(small_house, discount=10)

print("\n--- 4. Заробіток грошей")

user.earn_money(10000)
user.info()

print("\n--- 5. Повторна спроба покупки")

user.buy_house(small_house, discount=10)

print("\n--- 6. Фінальний стан")

user.info()