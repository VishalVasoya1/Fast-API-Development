def add(num1: int, num2:int):
    return num1 + num2

def substract(num1: int, num2:int):
    return num1 - num2

def multiply(num1: int, num2:int):
    return num1 * num2

def divide(num1: int, num2:int):
    return num1 // num2


class BankAccount():
    
    def __init__(self, balance=0) -> None:
        self.balance = balance