import sys
from parse import parse_data
from matching import match_judges
from write import write_judges_to_csv, write_judges_reasoning_to_csv, write_companies_to_csv, write_companies_reasoning_to_csv

# Check if the correct number of command line arguments is provided
if len(sys.argv) != 5:
    print("Usage: python main.py -j <judges_csv_file> -c <companies_csv_file>")
    sys.exit(1)

# Get the CSV file paths from the command line arguments
judges_file = None
companies_file = None
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
judges, companies, categories = parse_data(judges_file=judges_file, companies_file=companies_file)
# judges, companies = result

# match judges
judge_list, company_list, min_company_judges = match_judges(judges, companies, max_judge_companies=max_judge_companies)

# sort lists
judge_list = sorted(judge_list, key=lambda x: x[1])
company_list = sorted(company_list, key=lambda x: x[1])

# define file names
judges_file_name="csv/output_judges.csv"
judges_reasoning_file_name="csv/output_judges_reasoning.csv"
companies_file_name="csv/output_companies.csv"
companies__reasoning_file_name="csv/output_companies_reasoning.csv"

# write to files
header1 = ["Judge Name", "Categories"]
header1.extend([f'Company {n+1}' for n in range(max_judge_companies + 2)])
write_judges_to_csv(judge_list, header1, judges_file_name)
write_judges_reasoning_to_csv(judge_list, header1, judges_reasoning_file_name)
header2 = ["Company", "Category", "Queue Number"]
header2.extend([f'Judge {n+1}' for n in range(min_company_judges + 2)])
write_companies_to_csv(company_list, header2, companies_file_name)
write_companies_reasoning_to_csv(company_list, header2, companies__reasoning_file_name)

# for row in company_list:
#     print(row)

# output data
# print(judges)
# print(companies)
# for c in categories.keys():
#     print(c)

