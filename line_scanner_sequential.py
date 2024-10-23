from random import randint
import time

WEIGHTS = [0.00025177, 0.008666992, 0.078025818, 0.24130249, 0.343757629, 0.24130249, 0.078025818, 0.008666992, 0.000125885]
THRESHOLD = 40

class Input:
    def __init__(self, fileName=None, M=12, N=10):
        self.fileName = fileName
        self.f = None
        self.currentLine = []
        self.numberOfRows = 0
        self.N = float('inf')
        self.M = float('inf')

        if fileName is not None:
            self.f = open(fileName, 'r')
            self.currentLine = self.f.readline().split(',')
            if len(self.currentLine[0]) == 0:
                self.close()
                raise Exception("End of file reached.")
            self.currentLine = [int(x) for x in self.currentLine]
            self.M = len(self.currentLine)
            return
        
        self.M = M
        self.N = N

    def generate(self, seen):
        if self.numberOfRows >= self.N:
            raise Exception("Number of rows exceeded.")
        
        if seen >= self.M - 4:
            return [0, 0]
        
        if self.f is not None:
            if len(self.currentLine) == 0:
                self.currentLine = self.f.readline().split(',')
                if len(self.currentLine[0]) == 0:
                    self.close()
                    raise Exception("End of file reached.")
                self.currentLine = [int(x) for x in self.currentLine]
            
            [x, y] = [int(self.currentLine[0]), int(self.currentLine[1])]
            self.currentLine = self.currentLine[2:]
            return [x, y]

        return [randint(0, 255), randint(0, 255)]
    
    def close(self):
        if self.f is not None:
            self.f.close()

def filter(buffer):
    sum = 0
    for i in range(len(WEIGHTS)):
        sum += buffer[i] * WEIGHTS[i]
    
    buffer.pop(0)

    if sum > THRESHOLD:
        return 1
    return 0

input = Input('input.csv')

try:
    while True:
        start = time.time_ns()
        input.numberOfRows += 1
        buffer = [0, 0, 0, 0]
        seen = 0

        # Generate 3 pairs by default always.
        for i in range(3):
            buffer.extend(input.generate(seen))
            seen += 2

        filtered = []
        while len(filtered) < input.M:
            filtered.append(filter(buffer))
            filtered.append(filter(buffer))
            buffer.extend(input.generate(len(filtered)))

        print("Time: ", time.time_ns() - start)
        print(filtered)
        print()
except Exception as e:
    print("Rows processed: ", input.numberOfRows - 1)  
    print("Exception: ", e)
