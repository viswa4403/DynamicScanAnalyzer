from random import randint
import time

# Constants
WEIGHTS = [
    0.00025177, 0.008666992, 0.078025818, 0.24130249, 
    0.343757629, 0.24130249, 0.078025818, 0.008666992, 
    0.000125885
]  # Weights used for the filtering operation
THRESHOLD = 40  # Threshold value for the filter to determine the output

class Input:
    """
    This class handles input generation from a file or by generating random values.
    If a file is specified, it reads input values from the file.
    Otherwise, it generates random pairs of integers.
    """
    def __init__(self, fileName=None, M=12, N=10):
        self.fileName = fileName
        self.f = None  # File handle
        self.currentLine = []  # List to store the current line values
        self.numberOfRows = 0  # Counter for the number of rows processed
        self.N = float('inf')  # Total number of rows allowed (default: infinite)
        self.M = float('inf')  # Total number of columns (default: infinite)

        # If a file is provided, open the file and read the first line
        if fileName is not None:
            self.f = open(fileName, 'r')
            self.currentLine = self.f.readline().split(',')
            if len(self.currentLine[0]) == 0:  # End of file check
                self.close()
                raise Exception("End of file reached.")
            self.currentLine = [int(x) for x in self.currentLine]  # Convert line values to integers
            self.M = len(self.currentLine)  # Set M to the length of the first line
            return
        
        # If no file is provided, use user-specified or default values
        self.M = M  # Number of columns
        self.N = N  # Number of rows

    def generate(self, seen):
        """
        Generates a pair of input values.
        If reading from a file, retrieves values from the current line.
        Otherwise, generates random values.
        """
        if self.numberOfRows >= self.N:
            raise Exception("Number of rows exceeded.")  # Raise exception if row limit is reached
        
        if seen >= self.M - 4:
            return [0, 0]  # Return zeros if the buffer is close to being full
        
        if self.f is not None:
            if len(self.currentLine) == 0:  # Read a new line if the current line is empty
                self.currentLine = self.f.readline().split(',')
                if len(self.currentLine[0]) == 0:  # End of file
                    self.close()
                    raise Exception("End of file reached.")
                self.currentLine = [int(x) for x in self.currentLine]  # Convert line values to integers
            
            # Extract the next pair of values from the current line
            [x, y] = [int(self.currentLine[0]), int(self.currentLine[1])]
            self.currentLine = self.currentLine[2:]  # Remove the processed values
            return [x, y]

        # Generate random values if not using a file
        return [randint(0, 255), randint(0, 255)]
    
    def close(self):
        """Closes the file if it was opened."""
        if self.f is not None:
            self.f.close()

def filter(buffer):
    """
    Applies a weighted filter to the buffer.
    The weighted sum is calculated using the pre-defined WEIGHTS.
    If the sum exceeds the THRESHOLD, it returns 1, otherwise 0.
    """
    sum = 0
    for i in range(len(WEIGHTS)):
        sum += buffer[i] * WEIGHTS[i]  # Calculate weighted sum
    
    buffer.pop(0)  # Remove the oldest value from the buffer

    # Determine the output based on the threshold
    if sum > THRESHOLD:
        return 1
    return 0

# Main execution
input = Input('input.csv')  # Initialize the Input class with a file

try:
    while True:
        start = time.time_ns()  # Record the start time for performance measurement
        input.numberOfRows += 1  # Increment the number of rows processed
        buffer = [0, 0, 0, 0]  # Initialize the buffer with four zeros
        seen = 0  # Track the number of input values seen

        # Generate three pairs of input values and add them to the buffer
        for i in range(3):
            buffer.extend(input.generate(seen))
            seen += 2  # Update the seen count for the input generation

        filtered = []  # List to store the filtered results
        # Continue filtering until the number of filtered results reaches M
        while len(filtered) < input.M:
            filtered.append(filter(buffer))  # Apply the filter and add the result to the list
            filtered.append(filter(buffer))  # Apply the filter again for a second result
            buffer.extend(input.generate(len(filtered)))  # Update the buffer with new input values

        # Output the time taken for processing and the filtered results
        print("Time: ", time.time_ns() - start)
        print(filtered)
        print()
except Exception as e:
    # Handle the end of file or other exceptions gracefully
    print("Rows processed: ", input.numberOfRows - 1)  
    print("Exception: ", e)
