import csv
import sys

# Check if the correct number of command line arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <csv_file>")
    sys.exit(1)

# Replace 'your_file.csv' with the path to your CSV file
filePath = sys.argv[1]

try:
    # Open the CSV file in read mode
    with open(filePath, 'r') as csvFile:
        # Create a CSV reader object
        csvReader = csv.reader(csvFile)
        
        # Iterate through each row in the CSV file and print it
        for row in csvReader:
            print(', '.join(row))  # Assuming the CSV has comma as delimiter, adjust if necessary

except FileNotFoundError:
    print(f"The file '{filePath}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")