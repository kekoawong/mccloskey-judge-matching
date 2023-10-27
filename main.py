import csv
import sys

# Check if the correct number of command line arguments is provided
if len(sys.argv) != 5:
    print("Usage: python main.py -j <judges_csv_file> -c <companies_csv_file>")
    sys.exit(1)

# Get the CSV file paths from the command line arguments
judges_file = None
companies_file = None

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

# define the dictionaries
judges = {} # will be of struture { judge_name: [judge_categories] }
companies = {} # will be of struture { company_name: company_category }
categories = {} # will be of struture { category: { companies: number; judges: number; } }

try:
    # Open judges CSV file in read mode
    with open(judges_file, 'r') as judges_csv_file:
        # Create a CSV reader object for judges
        judges_csv_reader = csv.reader(judges_csv_file)
        
        print("Judges CSV Contents:")
        for row in judges_csv_reader:
            # get the judge name
            judge_name = row[0]

            # get the categories
            judge_categories = [category.strip() for category in row[2].split(',')]

            # add to judge dictionary
            judges[judge_name] = judge_categories

            # increment num judges in category
            for category in judge_categories:
                if category not in categories:
                    categories[category] = { "num_companies": 0, "num_judges": 0 }
                categories[category]["num_judges"] += 1
    
    # Open companies CSV file in read mode
    with open(companies_file, 'r') as companies_csv_file:
        # Create a CSV reader object for companies
        companies_csv_reader = csv.reader(companies_csv_file)
        
        print("\nCompanies CSV Contents:")
        for row in companies_csv_reader:
            # get the judge name
            company_name = row[0]

            # add to companies dictionar

            # get the categories
            company_category = row[1].strip()

            # add to judge dictionary
            companies[company_name] = company_category

            # increment num companies in category
            for category in judge_categories:
                if category not in categories:
                    categories[category] = { "num_companies": 0, "num_judges": 0 }
                categories[category]["num_companies"] += 1
            
except FileNotFoundError as e:
    print(f"File was not found error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
