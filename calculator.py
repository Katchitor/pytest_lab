class Calculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Деление на ноль")
        return a / b

    def is_even(self, n):
        return n % 2 == 0