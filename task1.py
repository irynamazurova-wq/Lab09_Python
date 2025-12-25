import string

class Alphabet:

    __UA_LETTERS = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

    def __init__(self, lang="UA", letters=__UA_LETTERS):
        self.lang = lang
        self.letters = list(letters)

    def print_alphabet(self):
        print(f"Алфавіт мови {self.lang}: {self.letters}")

    def letters_num(self):
        return len(self.letters)

    def is_ua_lang(self, text):

        text = text.lower()
        valid_chars = self.__UA_LETTERS + string.punctuation + string.whitespace + "0123456789"

        for char in text:
            if char not in valid_chars:
                return False
        return True


class EngAlphabet(Alphabet):
    __en_letters_num = 26

    def __init__(self):
        super().__init__("En", string.ascii_lowercase)

    def is_en_letter(self, letter):
        if letter.lower() in self.letters:
            return True
        return False

    def letters_num(self):
        return EngAlphabet.__en_letters_num

    @staticmethod
    def example():
        return "The quick brown fox jumps over the lazy dog."


eng = EngAlphabet()
print("--- 1. Створення об'єкту EngAlphabet")

print("\n--- 2. Вивід алфавіту")
eng.print_alphabet()

print("\n--- 3. Кількість букв")
print(f"Кількість літер (Eng): {eng.letters_num()}")

print("\n--- 4. Перевірка букви 'J' (is_en_letter) ---")
j_check = eng.is_en_letter('J')
print(f"Чи є 'J' англійською: {j_check}")
print(f"Чи є 'Щ' англійською: {eng.is_en_letter('Щ')}")

print("\n--- 5. Перевірка букви 'Щ' (is_ua_lang) ---")
ua_check = eng.is_ua_lang('Щ')
print(f"Чи є 'Щ' українською: {ua_check}")
print(f"Чи є 'Hello' українським словом: {eng.is_ua_lang('Hello')}")

print("\n--- 6. Статичний метод example() ---")
print(eng.example())