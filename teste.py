import csv

# create a csv file object and open
with open('sample.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, sep=';', )
    # Add the header row
    writer.writerow(['Odd', 'Even'])
    for i in range(1,20,2):
        # Add the data row
        writer.writerow([i, i+1])