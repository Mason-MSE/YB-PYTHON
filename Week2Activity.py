class MathSeries:
    # Use __slots__ to limit which attributes instances can have
    # This helps save memory and prevents adding new attributes by mistake
    __slots__ = ('n')

    def __init__(self, n):
        # Store the input number n as an instance attribute
        self.n = n

    def factorial_recursive(self, n):
    
        # Factorial is not defined for negative numbers
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")

        # Base cases: 0! = 1 and 1! = 1
        if n in (0, 1):
            return 1

        # Recursive case: n! = n * (n-1)!
        return n * self.factorial_recursive(n - 1)

    def fibonacci_recursive(self, n):
       
        # Fibonacci numbers are not defined for negative indices
        if n < 0:
            raise ValueError("Fibonacci is not defined for negative numbers.")

        # Base cases: F(0) = 0, F(1) = 1
        if n == 0:
            return 0
        if n == 1:
            return 1

        # Recursive case: F(n) = F(n-1) + F(n-2)
        return self.fibonacci_recursive(n - 1) + self.fibonacci_recursive(n - 2)


if __name__ == "__main__":
    
    n = 5

    # Create an instance of MathSeries with n = 5
    mathSeries = MathSeries(n)

    # Call the recursive factorial method and print the result
    print("Factorial (recursive):", mathSeries.factorial_recursive(n))

    # Call the recursive Fibonacci method and print the result
    print("Fibonacci (recursive):", mathSeries.fibonacci_recursive(n))

