import sys
from parse import parse_data
from matching import match_judges

# Check if the correct number of command line arguments is provided
if len(sys.argv) != 5:
    print("Usage: python main.py -j <judges_csv_file> -c <companies_csv_file>")
    sys.exit(1)

# Get the CSV file paths from the command line arguments
judges_file = None
companies_file = None
min_company_judges = 8
max_judge_companies = 10

# Parse command line arguments
for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == '-j':
        judges_file = sys.argv[i + 1]
    elif sys.argv[i] == '-c':
        companies_file = sys.argv[i + 1]

# Check if both judges and companies files are provided
if not (judges_file and companies_file):
    print("Error: Both judges and companies files must be provided.")
    sys.exit(1)

# parse the data from the csv
result = parse_data(judges_file=judges_file, companies_file=companies_file)
judges, companies, categories = result

# match judges
match_judges(judges, companies, categories)

# output data
# print(judges)
# print(companies)
for c in categories.keys():
    print(c)

