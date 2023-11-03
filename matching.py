import random

def get_next_category(categories={}):
    '''
    Function will get the next category depending on the highest ratio of companies to available judges
    '''
    ratios = {}
    for cat, val in categories.items():
        if len(val["judges"]) == 0:
            ratios[cat] = 99999999
        else:
            ratios[cat] = len(val["companies"]) / len(val["judges"])

    max_ratio_key = max(ratios, key=lambda k: ratios[k])
    # print(f'{max_ratio_key} with ratio {ratios[max_ratio_key]} and {len(categories[max_ratio_key]["companies"])} companies and {len(categories[max_ratio_key]["judges"])} judges')
    return max_ratio_key


def match_judges(judges={}, companies={}, max_judge_companies=10):
    '''
    Function will take in the judges, companies, and categories \n
        judges = { judge_name: [judge_categories] } \n
        companies = { company_name: company_category } \n
        categories = { category: { num_companies: number; num_judges: number; } } \n
    Will output the following list of lists. \n
    Judge List: [judge_name, [categories], num_companies, num_matching_companies, num_fill_in_companies, [companies], [companies-with-reasoning]] \n
    Company List: [company_name, category, queue_number, num_judges, num_matching_judges, num_fill_in_judges, queue_number_with_reasoning, [judges], [judges-with-reasoning]]
    '''
    # set constraints
    total_judges = len(judges.keys())
    total_companies = len(companies.keys())
    min_judges = (total_judges * max_judge_companies) / total_companies

    # create categories object
    # of the structure { category: { companies: [], judges: [] }}
    categories = {}

    # add judges
    for judge, judge_categories in judges.items():
        for judge_category in judge_categories:
            if judge_category not in categories:
                categories[judge_category] = { "companies": [], "judges": [] }
            categories[judge_category]["judges"].append(judge)

    # return objects
    return_judges = {}
    return_companies = {}

    # define adding a judge to a company
    def add_judge_to_company(judge, company, within_category=True):
        '''
        Function will add the judge to the company
        '''
        # add company to judge database
        if judge not in return_judges:
            return_judges[judge] = { "companies": [], "companies_with_reasoning": [], "categories": judges[judge], "num_companies": 0, "num_matching_companies": 0, "num_fill_in_companies": 0 }
        return_judges[judge]["companies"].append(f'{company if within_category else company + " - Fill-in"}')
        return_judges[judge]["companies_with_reasoning"].append(f'{company} - {target_category if within_category else "Fill-in"}.')
        return_judges[judge]["num_companies"] += 1
        # increment matching companies
        if within_category:
            return_judges[judge]["num_matching_companies"] +=1 
        else:
            return_judges[judge]["num_fill_in_companies"] +=1
        
        # add judge to company database
        if company not in return_companies:
            return_companies[company] = { "queue_number": 0, "queue_number_with_reasoning": "", "judges": [], "judges_with_reasoning": [], "num_judges": 0, "num_matching_judges": 0, "num_fill_in_judges": 0 }
        return_companies[company]["judges"].append(f'{judge if within_category else judge + " - Fill-in"}')
        return_companies[company]["judges_with_reasoning"].append(f'{judge} - {target_category if within_category else "Fill-in"}. All interests are {", ".join(judges[judge])}')
        return_companies[company]["num_judges"] += 1
        # increment matching companies
        if within_category:
            return_companies[company]["num_matching_judges"] +=1 
        else:
            return_companies[company]["num_fill_in_judges"] +=1

        # remove judge from being available if hits max number
        if len(return_judges[judge]["companies"]) >= max_judge_companies:
            for category in judges[judge]:
                # remove judge from category
                categories[category]["judges"].remove(judge)

            # delete judge from availibility
            del judges[judge]
            # print(f"deleted judge {judge} with companies {return_judges[judge]["companies"]}")

    # loop through each judge iteration
    for n in range(int(min_judges)):
        # add companies to categories
        for company_name, comp_category in companies.items():
            if comp_category not in categories:
                categories[comp_category] = { "companies": [], "judges": [] }
            categories[comp_category]["companies"].append(company_name)
        print([f"{x}: {len(v['companies'])} companies and {len(v['judges'])} judges" for x, v in categories.items()])
        # loop through and add a judge to each company
        remaining_companies = len(companies.keys())
        while remaining_companies > 0:
            # get next category and company
            target_category = get_next_category(categories=categories)
            try:
                target_company = categories[target_category]["companies"].pop(0)
            except IndexError:
                print("Error")
                print(categories[target_category])
                print([(cc, categories[cc]["companies"]) for cc in categories.keys()])
                # exit()

            # add the values to the dictionary
            queue_num = len(companies.keys()) - remaining_companies
            queue_num_with_reasoning = f'{queue_num} since {len(categories[target_category]["companies"]) + 1} {target_category} companies and {len(categories[target_category]["judges"])} available judges'

            # assign variables for judge loop
            judges_shuffled = list(random.sample(list(judges.items()), len(judges.keys())))
            num_extra_judges_needed = min_judges - len(categories[target_category]["judges"])

            # match the judge that has the lowest number of categories and contains the category
            # print(judges_shuffled)
            # exit()
            # judge_name = next((judge_n for judge_n, judge_c in judges_shuffled if target_category in judge_c), None)
            # print(remaining_companies)
            # get remaining avalailable judges in company
            available_category_judges = [judge_n for judge_n, judge_categories in judges.items() if target_category in judge_categories]
            sorted_available_judges = sorted(available_category_judges, key=lambda x: (len(judges[x]), random.random()))
            
            # add judge if it is not currently in the list
            company_judges = [] if target_company not in return_companies else return_companies[target_company]["judges"]
            judge_name = next((judge_n for judge_n in sorted_available_judges if judge_n not in company_judges), None)
            # judge_name = min((name for name, categories in judges.items() if target_category in categories), key=lambda name: len(judges[name])) if any(target_category in categories for categories in judges.values()) else None
            if judge_name:
                add_judge_to_company(judge_name, target_company, True)

            # loop through judges
            # for judge in judges_shuffled:
            #     # if the judge is available and has the category, assign to company
            #     if judge in judges and target_category in judges[judge]:
            #         add_judge_to_company(judge, target_company, True)
            #     # if judge is available and company needs a random judge, assign to company
            #     # elif judge in judges and num_extra_judges_needed > 0:
            #     #     add_judge_to_company(judge, target_company, False)
            #     #     num_extra_judges_needed -= 1

            #     # break from loop if num judges met
            #     if target_company in return_companies and len(return_companies[target_company]["judges"]) >= min_judges:
            #         break

            # set values in dictionary
            return_companies[target_company]["queue_number"] = queue_num
            return_companies[target_company]["queue_number_with_reasoning"] = queue_num_with_reasoning

            # decrement remaining companies
            remaining_companies -= 1

    # loop through all companies again and add filler judges

    # return the data
    return_judge_list = [[judge_name, judge_value["categories"], judge_value["num_companies"], judge_value["num_matching_companies"], judge_value["num_fill_in_companies"], judge_value["companies"], judge_value["companies_with_reasoning"]] for judge_name, judge_value in return_judges.items()]
    return_company_list = [[company_name, companies[company_name], company_value["queue_number"], company_value["num_judges"], company_value["num_matching_judges"], company_value["num_fill_in_judges"], company_value["queue_number_with_reasoning"], company_value["judges"], company_value["judges_with_reasoning"]] for company_name, company_value in return_companies.items()]
    return return_judge_list, return_company_list, int(min_judges)
            
    

def match_judges_old(judges={}, companies={}, categories={}, max_judge_companies=10):
    '''
    Function will take in the judges, companies, and categories \n
    Will output the following list of lists. \n
    Judge List: [judge_name, [categories], [companies], [companies_with_reasoning]] \n
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
        # check this later on
        # if (len(company_categories[next_category])):
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
                # add judge to overall judges
                judges[judge_name] = [next_category]
                
                # add new judge to the category list
                available_category_judges[next_category].append(judge_name)
                company_judges.append(judge_name)
                company_judges_with_reasoning.append(f'{judge_name} - {next_category}. All interests are {", ".join(judges[judge_name])}')

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