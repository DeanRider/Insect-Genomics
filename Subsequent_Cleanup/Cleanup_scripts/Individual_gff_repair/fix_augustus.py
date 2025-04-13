'''
i have a tab delimited file. Within the first column, i want to eliminate the first underscore and everything that comes after it but leave all other columns in tact.
'''
import csv

# Open the input file and output file
with open('augustus.named.gff3', 'r') as infile, open('fixed_augustus.gff3', 'w', newline='') as outfile:
    outfile.write("##gff-version 3"'\n')
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile, delimiter='\t')

    # Iterate through each row
    for row in reader:
        # Modify the first column by removing the first underscore and everything after it
        if row:  # Check if the row is not empty
            row[0] = row[0].split(' ', 1)[0]  # Split at the first underscore and take the part before it
        # Write the modified row to the output file
        writer.writerow(row)

