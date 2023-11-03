import csv

def write_judges_to_csv(data, header, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(header)
        # Write the data
        for row in data:
            name = row[0]
            categories = row[1]
            num_companies = row[2]
            num_matching = row[3]
            num_fill_in = row[4]
            companies = row[5]
            written_row = [name, ", ".join(categories), num_companies, num_matching, num_fill_in]
            written_row.extend(companies)
            csv_writer.writerow(written_row)

def write_judges_reasoning_to_csv(data, header, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(header)
        # Write the data
        for row in data:
            name = row[0]
            categories = row[1]
            num_companies = row[2]
            num_matching = row[3]
            num_fill_in = row[4]
            companies = row[6]
            written_row = [name, ", ".join(categories), num_companies, num_matching, num_fill_in]
            written_row.extend(companies)
            csv_writer.writerow(written_row)

def write_companies_to_csv(data, header, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(header)
        # Write the data
        for row in data:
            name = row[0]
            category = row[1]
            queue = row[2]
            num_judges = row[3]
            num_matching = row[4]
            num_fill_in = row[5]
            judges = row[7]
            written_row = [name, category, queue, num_judges, num_matching, num_fill_in]
            written_row.extend(judges)
            csv_writer.writerow(written_row)

def write_companies_reasoning_to_csv(data, header, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(header)
        # Write the data
        for row in data:
            name = row[0]
            category = row[1]
            queue = row[6]
            num_judges = row[3]
            num_matching = row[4]
            num_fill_in = row[5]
            judges = row[8]
            written_row = [name, category, queue, num_judges, num_matching, num_fill_in]
            written_row.extend(judges)
            csv_writer.writerow(written_row)