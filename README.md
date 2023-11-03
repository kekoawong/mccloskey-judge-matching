# Matching Judges to Companies 👩‍⚖️👨‍⚖️🤝🏢

This project consists of Python scripts to match judges to companies for a pitch competition based on their interests.

## 📥 Installation

To use these scripts, you need:

- Python 3.6 or higher
- The CSV and random modules (should come standard with Python)

No special installation is required. Simply download or clone the scripts. 

## 📖 Code Overview

- `main.py` handles command line arguments, calls the other modules, and writes the output CSV files
- `parse.py` parses the judge and company CSV data into dictionaries  
- `matching.py` contains the logic to optimally match judges to companies
- `write.py` contains functions to write output CSV files

## 💻 Usage

To run the scripts:

1. Ensure the input CSV files are in the `csv` folder. Sample files are provided:
    - `sample_judges.csv` - Contains judge name and categories
    - `sample_companies.csv` - Contains company name and category
   
2. Run `main.py` with the CSV files:

   ```bash
   python main.py -j csv/sample_judges.csv -c csv/sample_companies.csv
   ```
   
3. The output CSV files will be created in the `csv` folder:
    - `output_judges.csv` - Matched companies per judge  
    - `output_companies.csv` - Matched judges per company
   
The key parameters to set are:

- `-j` - Judges CSV file path
- `-c` - Companies CSV file path 
- `max_judge_companies` - Max companies to assign per judge

Feel free to modify the sample CSV data to test different matching scenarios.

## 📂 CSV File Format

The CSV files must contain specific headers and formats.

### Judges CSV

The judges CSV should have the following headers:

```
Judge,Categories 
```

- **Judge** - The judge's name
- **Categories** - Comma separated list of categories the judge is interested in

*Example:*

```
Judge,Categories  
John Doe,"AI, Healthcare"
Jane Doe,"Manufacturing, Robotics"
```

### Companies CSV 

The companies CSV should have the following headers:

```
Company,Category
```

- **Company** - The company name
- **Category** - The company's category

*Example:* 

```
Company,Category
Acme Inc.,Manufacturing 
ABC Corp.,AI
```

The categories in the companies CSV must match the possible categories in the judges CSV.

## 📤 Output 

Running `main.py` will generate the following output files in the `csv` folder:

### output_judges.csv

This CSV file contains the following columns:

- **Judge Name** - The name of the judge
- **Categories** - Comma separated list of the judge's categories
- **Companies** - Total number of companies assigned to the judge  
- **Matching** - Number of companies matched to the judge's categories
- **Fill-In** - Number of companies not matched to categories (filler)
- **Company X** - Ordered list of companies assigned to the judge

### output_companies.csv

This CSV file contains the following columns:

- **Company** - Name of the company
- **Category** - The company's category
- **Queue Number** - Assigned queue position based on algorithm
- **Judges** - Total number of judges assigned to company
- **Matching** - Number of judges matched to company's category 
- **Fill-in** - Number of judges not matched to category
- **Judge X** - Ordered list of judges assigned to company

### output_judges_reasoning.csv

This CSV file contains the matched companies per judge along with reasoning for each match.

### output_companies_reasoning.csv

This CSV file contains the matched judges per company along with reasoning for each match.