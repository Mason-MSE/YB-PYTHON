class MathSeries:

    __splot__ = ('n')

    def __init__(self,n):
        self.n=n
    # @staticmethod
    def factorial_recursive(self,n):
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        if n in (0, 1):
            return 1
        return n * self.factorial_recursive(n - 1)



    # @staticmethod
    def fibonacci_recursive(self,n):
        if n < 0:
            raise ValueError("Fibonacci is not defined for negative numbers.")
        if n == 0:
            return 0
        if n == 1:
            return 1
        return (self.fibonacci_recursive(n - 1) + self.fibonacci_recursive(n - 2))


if __name__ == "__main__":
    n = 5

    mathSeries = MathSeries(n)
    print("Factorial (recursive):", mathSeries.factorial_recursive(n))
    print("Fibonacci (recursive):", mathSeries.fibonacci_recursive(n))
