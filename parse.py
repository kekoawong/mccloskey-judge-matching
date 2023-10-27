def parse_data(judges_file, companies_file):
    # define the dictionaries 
    judges = {} # will be of struture { judge_name: [judge_categories] }
    companies = {} # will be of struture { company_name: company_category }
    categories = {} # will be of struture { category: { companies: number; judges: number; } }

    try:
        # Open judges CSV file in read mode
        with open(judges_file, 'r') as judges_csv_file:
            # Create a CSV reader object for judges
            judges_csv_reader = csv.reader(judges_csv_file)
            # skip header row
            next(judges_csv_reader, None)
            
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
            # skip header row
            next(companies_csv_reader, None)
            
            print("\nCompanies CSV Contents:")
            for row in companies_csv_reader:
                # get the judge name
                company_name = row[0]

                # add to companies dictionar

                # get the categories
                company_category = row[1].strip()

                # add to judge dictionary
                companies[company_name] = company_category

                # add company to category
                if company_category not in categories:
                    categories[category] = { "num_companies": 0, "num_judges": 0 }
                categories[category]["num_companies"] += 1 

    # create exceptions 
    except FileNotFoundError as e:
        print(f"File was not found error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")