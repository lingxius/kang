#!/usr/bin/env python3
"""
Simple calculator module with some intentional bugs for demonstration
"""

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a, b):
        # Fixed: Added check for division by zero
        if b == 0:
            error_msg = f"Error: Cannot divide {a} by zero"
            self.history.append(error_msg)
            raise ValueError("Division by zero is not allowed")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base, exponent):
        # Fixed: Properly handle negative exponents
        if exponent == 0:
            return 1
        elif exponent > 0:
            return base * self.power(base, exponent - 1)
        else:
            # For negative exponents: x^(-n) = 1 / (x^n)
            if base == 0:
                raise ValueError("Cannot raise 0 to a negative power")
            return 1 / self.power(base, -exponent)
    
    def factorial(self, n):
        # Fixed: Properly handle negative numbers and non-integers
        if not isinstance(n, int):
            raise TypeError("Factorial is only defined for integers")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n == 0 or n == 1:
            return 1
        else:
            return n * self.factorial(n - 1)
    
    def get_history(self):
        return self.history
    
    def clear_history(self):
        self.history = []

def main():
    calc = Calculator()
    
    # Test operations
    print("Calculator Demo")
    print("===============")
    
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    
    # Test division by zero (fixed)
    try:
        result = calc.divide(8, 0)
        print(f"8 / 0 = {result}")
    except ValueError as e:
        print(f"Division error: {e}")
    
    # Test power operations including negative exponents
    print(f"2^3 = {calc.power(2, 3)}")
    print(f"2^(-2) = {calc.power(2, -2)}")
    
    # Test factorial
    print(f"5! = {calc.factorial(5)}")
    try:
        print(f"(-3)! = {calc.factorial(-3)}")
    except ValueError as e:
        print(f"Factorial error: {e}")
    
    print("\nHistory:")
    for entry in calc.get_history():
        print(entry)

if __name__ == "__main__":
    main()