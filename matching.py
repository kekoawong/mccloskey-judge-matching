from typing import Tuple, List, Dict, Union

def get_next_category(categories={}):
    ratios = {}
    for cat, val in categories:
        if val["num_judges"] == 0:
            return None
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
    company_judges = {}

    # loop through the companies, make a list of companies in categories
    company_categories = {}
    for name, cat in companies:
        if cat not in company_categories:
            company_categories[cat] = []
        company_categories[cat].append(name)
    
    # loop through and add the judges to the company
    initial_category = 

    return