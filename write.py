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
            companies = row[2]
            written_row = [name, ", ".join(categories)]
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
            judges = row[3]
            written_row = [name, category, queue]
            written_row.extend(judges)
            csv_writer.writerow(written_row)