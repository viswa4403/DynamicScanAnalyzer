# LineScanAnalyzer

# Problem Statement:
The problem statement for the project involves designing a system that emulates a line scan camera used in applications like detecting defects in newspaper printing or textile industries. The goal is to process a continuously scanned 2D array of data representing a long paper or cloth roll, detecting defective pixels in real time. The system consists of two main processing blocks:

Data Generation Block: Simulates a line scan camera that outputs pixel values continuously. It processes two consecutive elements at a time for each iteration. The system must handle both real and test mode inputs, including random number generation and reading from a .csv file.

Filter & Threshold Block: Cleans noisy data by applying a filter to a sliding window of nine elements around the current pixel. The filtered value is calculated using a dot product with predefined filter coefficients, followed by thresholding to flag defective pixels.

# What is the purpose of using parallel programming?

The system is designed to operate in parallel to achieve real-time processing requirements. By parallelizing the processing blocks, the system can simultaneously perform data acquisition, filtering, and thresholding without waiting for the completion of previous steps. This approach ensures:

Real-time Performance: Parallel processing reduces latency, allowing each block to work on data as soon as it's available, ensuring that the system works as efficient as possible.

Scalability: Adding more processing blocks or features can be done with minimal changes, as each block functions independently and processes data concurrently.

Efficient Resource Utilization: Distributing the workload across multiple blocks maximizes hardware usage, leading to faster and more efficient processing.
