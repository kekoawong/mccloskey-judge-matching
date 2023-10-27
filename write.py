import csv

def write_to_csv(data, header, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(header)
        # Write the data
        csv_writer.writerows(data)