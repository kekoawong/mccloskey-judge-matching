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
        return_companies[company]["judges_with_reasoning"].append(f'{judge} - {target_category if within_category else "Fill-in"}. All interests are {", ".join(return_judges[judge]["categories"])}')
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
        # print([f"{x}: {len(v['companies'])} companies and {len(v['judges'])} judges" for x, v in categories.items()])
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
                pass

            # add the values to the dictionary
            queue_num = len(companies.keys()) - remaining_companies
            queue_num_with_reasoning = f'{queue_num} since {len(categories[target_category]["companies"]) + 1} {target_category} companies and {len(categories[target_category]["judges"])} available judges'

            # get remaining avalailable judges in company
            available_category_judges = [judge_n for judge_n, judge_categories in judges.items() if target_category in judge_categories]
            sorted_available_judges = sorted(available_category_judges, key=lambda x: (len(judges[x]), random.random()))
            
            # add judge if it is not currently in the list
            company_judges = [] if target_company not in return_companies else return_companies[target_company]["judges"]
            judge_name = next((judge_n for judge_n in sorted_available_judges if judge_n not in company_judges), None)
            # judge_name = min((name for name, categories in judges.items() if target_category in categories), key=lambda name: len(judges[name])) if any(target_category in categories for categories in judges.values()) else None
            if judge_name:
                add_judge_to_company(judge_name, target_company, True)

            # set values in dictionary
            return_companies[target_company]["queue_number"] = queue_num
            return_companies[target_company]["queue_number_with_reasoning"] = queue_num_with_reasoning

            # decrement remaining companies
            remaining_companies -= 1

    # loop through remaining judges and add them to companies that may have a match
    MIN_DIFFERENCE = 3
    filtered_and_sorted_judges = sorted(
        (judge_n for judge_n in judges.keys()),
        key=lambda j: len(judges[j])
    )
    
    # assign the judges with their interests
    for underused_judge in filtered_and_sorted_judges:
        # filter and sort the companies
        min_length = min(values["num_judges"] for values in return_companies.values())
        filtered_and_sorted_companies = sorted(
            (comp for comp, data in return_companies.items() if len(data['judges']) < min_length + (MIN_DIFFERENCE - 1)),
            key=lambda c: len(return_companies[c]['judges'])
        )
        # loop through companies and assign judges if there is an overlap, and they are not in the judges already
        for comp in filtered_and_sorted_companies:
            if companies[comp] in judges[underused_judge] and underused_judge not in return_companies[comp]["judges"]:
                add_judge_to_company(underused_judge, comp, True)
            # break if the judge has more than the necessary amount of companies
            if underused_judge in return_judges and return_judges[underused_judge]["num_companies"] >= max_judge_companies:
                break

    # assign the rest of the judges
    filtered_and_sorted_judges = sorted(
        (judge_n for judge_n in judges.keys()),
        key=lambda j: len(judges[j])
    )
    # assign the judges just by if htey are not in there
    unmatched_spots = 0
    for underused_judge in filtered_and_sorted_judges:
        # filter and sort the companies
        min_length = min(values["num_judges"] for values in return_companies.values())
        filtered_and_sorted_companies = sorted(
            (comp for comp, data in return_companies.items() if len(data['judges']) < min_length + (MIN_DIFFERENCE - 1)),
            key=lambda c: len(return_companies[c]['judges'])
        )
        # loop through companies and assign judges if they are not in the judges already
        for comp in filtered_and_sorted_companies:
            if underused_judge not in return_companies[comp]["judges"]:
                add_judge_to_company(underused_judge, comp, False)
                unmatched_spots += 1
            # break if the judge has more than the necessary amount of companies
            if underused_judge in return_judges and return_judges[underused_judge]["num_companies"] >= max_judge_companies:
                break

    # return the data
    return_judge_list = [[judge_name, judge_value["categories"], judge_value["num_companies"], judge_value["num_matching_companies"], judge_value["num_fill_in_companies"], judge_value["companies"], judge_value["companies_with_reasoning"]] for judge_name, judge_value in return_judges.items()]
    return_company_list = [[company_name, companies[company_name], company_value["queue_number"], company_value["num_judges"], company_value["num_matching_judges"], company_value["num_fill_in_judges"], company_value["queue_number_with_reasoning"], company_value["judges"], company_value["judges_with_reasoning"]] for company_name, company_value in return_companies.items()]
    return return_judge_list, return_company_list, int(min_judges), 1 - (unmatched_spots/(total_judges * max_judge_companies))
            
