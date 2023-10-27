import random

def get_next_category(categories={}):
    '''
    Function will get the next category depending on the highest ratio of companies to available judges
    '''
    ratios = {}
    for cat, val in categories.items():
        if val["num_judges"] == 0:
            ratios[cat] = 0
        else:
            ratios[cat] = val["num_companies"] / val["num_judges"]

    max_ratio_key = max(ratios, key=lambda k: ratios[k])
    return max_ratio_key

def match_judges(judges={}, companies={}, categories={}, min_company_judges=8, max_judge_companies=10):
    '''
    Function will take in the judges, companies, and categories \n
    Will output the following list of lists. \n
    Judge List: [judge_name, [categories], [companies], [companies-with-reasoning]] \n
    Company List: [company_name, category, queue_number, queue_number_with_reasoning [judges], [judges-with-reasoning]]
    '''
    judge_companies = {}
    judge_companies_with_reasoning = {}
    company_list = []
    new_judges = 0

    # loop through the companies, make a list of companies in categories
    company_categories = {}
    for name, cat in companies.items():
        if cat not in company_categories:
            company_categories[cat] = []
        company_categories[cat].append(name)

    # add judges to new data structure
    available_category_judges = {}
    for judge_name, cat_list in judges.items():
        for cat in cat_list:
            if cat not in available_category_judges:
                available_category_judges[cat] = []
            available_category_judges[cat].append(judge_name)
    
    # loop through and add the judges to each company
    remaining_companies = len(companies.keys())
    while remaining_companies > 0:
        # get next company
        next_category = get_next_category(categories=categories)
        next_company = company_categories[next_category].pop(0)

        # set queue variables
        queue_num = len(companies.keys()) - remaining_companies
        queue_str = f'{queue_num} since {categories[next_category]["num_companies"]} {next_category} companies and {categories[next_category]["num_judges"]} available judges'
        
        # decrement companies in that category
        categories[next_category]["num_companies"] -= 1

        # shuffle the list order for judges
        random.shuffle(available_category_judges[next_category])

        # add judges to company
        company_judges = []
        company_judges_with_reasoning = []
        for n in range(min_company_judges):
            judge_name = None
            # if within range of category judges, add existing judge
            if n < len(available_category_judges[next_category]):
                judge_name = available_category_judges[next_category][n]
                company_judges.append(judge_name)
                company_judges_with_reasoning.append(f'{judge_name} - {next_category}. All interests are {", ".join(judges[judge_name])}')

            # if not, add a new judge
            else:
                judge_name = f"new-judge-{new_judges}"
                # add new judge to the category list
                available_category_judges[next_category].append(judge_name)
                company_judges.append(judge_name)
                company_judges_with_reasoning.append(f'{judge_name} - {next_category}. All interests are {", ".join(judges[judge_name])}')

                # add judge to overall judges
                judges[judge_name] = [next_category]

            # add company to judge list
            if judge_name not in judge_companies:
                judge_companies[judge_name] = []
            judge_companies[judge_name].append(next_company)

            if judge_name not in judge_companies_with_reasoning:
                judge_companies_with_reasoning[judge_name] = []
            judge_companies_with_reasoning[judge_name].append(f'{next_company} - {next_category}')

            # if judge has met max number, remove them from all category availibilty
            if max_judge_companies <= len(judge_companies[judge_name]):
                for cat in judges[judge_name]:
                    if judge_name in available_category_judges[cat]:
                        available_category_judges[cat].remove(judge_name)
                    
                    # decrement judges in that category
                    categories[cat]["num_judges"] -= 1
    
        company_list.append([next_company, next_category, queue_num, queue_str, company_judges, company_judges_with_reasoning])

        # decrement remaining companies
        remaining_companies -= 1
    return [[name, judges[name], judge_companies[name], judge_companies_with_reasoning[name]] for name in judge_companies], company_list