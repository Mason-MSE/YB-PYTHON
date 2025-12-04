class Converter:
    # Convert Celsius to Fahrenheit
    # Formula: F = C * 9/5 + 32
    def convertC(self, c):
        return round(c * 9 / 5 + 32, 2)
    
    # Convert Fahrenheit to Celsius
    # Formula: C = (F - 32) * 5/9F
    def convertF(self, f):
        return round((f - 32) * 5 / 9, 2)
    
if __name__ == "__main__":
    # Infinite loop to repeatedly ask user for input
    while True:
        try:
            # Prompt the user to enter a temperature
            temp_input = input("Enter temperature in Celsius or Fahrenheit (e.g., C25 or F77): ")
            temp = None
            converter = Converter()
            
            # Check if input starts with 'C' (Celsius)
            if temp_input.startswith('C'):
                # Extract numeric part and convert to float
                temp = float(temp_input[1:])
                # Convert Celsius to Fahrenheit and print
                print(f"{temp_input} degrees Celsius is ocnverted to {converter.convertC(temp)} degrees Fahrenheit ")
            
            # Check if input starts with 'F' (Fahrenheit)
            elif temp_input.startswith('F'):
                # Extract numeric part and convert to float
                temp = float(temp_input[1:])
                # Convert Fahrenheit to Celsius and print
                print(f"{temp_input} degrees Fahrenheit is ocnverted to {converter.convertF(temp)} degrees Celsius ")
            
            # Raise error if input format is invalid
            else:
                raise ValueError
        
        # Handle invalid input
        except ValueError:
            print("Invalid input. Please enter the temperature with correct 'C' or 'F' prefix!")