"""Menu driven calculator"""


def add(x: float, y: float) -> float:
    return x+y

def subtract(x: float, y: float) -> float:
    return x - y

def multiply(x: float, y: float) -> float:
    return x * y

def divide(x: float, y: float) -> float:
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

# main flow
def calculator():
    print(f"{"THE CALCULATOR":^20}")
    print()
    
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    
    choice = ""
    while choice not in ("1", "2", "3", "4"):
        choice = input("Enter a valid choice (1-4): ")
    
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))
    
    if choice == "1":
        result = add(num1, num2)
        print(f"{num1} + {num2} = {result}")
    elif choice == "2":
        result = subtract(num1, num2)
        print(f"{num1} - {num2} = {result}")
    elif choice == "3":
        result = multiply(num1, num2)
        print(f"{num1} * {num2} = {result}")
    elif choice == "4":
        result = divide(num1, num2)
        print(f"{num1} / {num2} = {result}")

calculator()