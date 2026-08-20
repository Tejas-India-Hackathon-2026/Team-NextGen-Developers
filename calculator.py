"""
Simple Calculator Application
Supports basic arithmetic operations and more
"""

def add(x, y):
    """Add two numbers"""
    return x + y

def subtract(x, y):
    """Subtract two numbers"""
    return x - y

def multiply(x, y):
    """Multiply two numbers"""
    return x * y

def divide(x, y):
    """Divide two numbers"""
    if y == 0:
        return "Error: Cannot divide by zero"
    return x / y

def power(x, y):
    """Raise x to the power of y"""
    return x ** y

def modulus(x, y):
    """Return remainder of x divided by y"""
    if y == 0:
        return "Error: Cannot divide by zero"
    return x % y

def calculator():
    """Main calculator function with menu"""
    print("\n" + "="*40)
    print("        SIMPLE CALCULATOR")
    print("="*40)
    print("\nOperations available:")
    print("  1. Add              (+)")
    print("  2. Subtract         (-)")
    print("  3. Multiply         (*)")
    print("  4. Divide           (/)")
    print("  5. Power            (**)")
    print("  6. Modulus          (%)")
    print("  0. Exit")
    print("="*40)
    
    while True:
        try:
            choice = input("\nEnter operation (0-6): ").strip()
            
            if choice == '0':
                print("\nThank you for using the calculator. Goodbye!")
                break
            
            if choice not in ['1', '2', '3', '4', '5', '6']:
                print("Invalid choice. Please enter a number between 0 and 6.")
                continue
            
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == '1':
                print(f"\n{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"\n{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"\n{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                result = divide(num1, num2)
                print(f"\n{num1} / {num2} = {result}")
            elif choice == '5':
                print(f"\n{num1} ** {num2} = {power(num1, num2)}")
            elif choice == '6':
                result = modulus(num1, num2)
                print(f"\n{num1} % {num2} = {result}")
        
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    calculator()
