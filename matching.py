def get_next_category(categories={}):
    '''
    Function will get the next category depending on the highest ratio of companies to available judges
    '''
    ratios = {}
    for cat, val in categories:
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
    Judge List: [judge_name, [categories], [companies]] \n
    Company List: [company_name, category, [judges], queue_number]
    '''
    judge_companies = {}
    company_list = []
    new_judges = 0

    # loop through the companies, make a list of companies in categories
    company_categories = {}
    for name, cat in companies:
        if cat not in company_categories:
            company_categories[cat] = []
        company_categories[cat].append(name)

    # add judges to new data structure
    available_category_judges = {}
    for judge_name, cat_list in judges:
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
        
        # decrement companies in that category
        categories[next_category]["num_companies"] -= 1

        # add judges to company
        company_judges = []
        for n in range(min_company_judges):
            # if within range of category judges, add existing judge
            if n < len(available_category_judges[next_category]):
                company_judges.append(available_category_judges[n])

            # if not, add a new judge
            else:
                judge_name = f"new-judge-${new_judges}"
                # add new judge to the category list
                available_category_judges[next_category].append(judge_name)
                company_judges.append(judge_name)

                # add judge to overall judges
                # judges[judge_name] = 

            # if judge has met max number, remove them from all category availibilty

        # decrement remaining companies
        remaining_companies -= 1

    return