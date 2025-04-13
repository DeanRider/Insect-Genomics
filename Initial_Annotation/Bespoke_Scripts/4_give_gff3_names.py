'''
I have two files that are tab delimited
file 1 has an index in the first column and a list of names in the second column
for each index entry in the first file, I want to search column 9 of the second file for a match
if there is a match, then look at the third column of the second file for "CDS" and if there is a match, then
I want to append column 9 of the second file with the content of the second column of the first file and follow that content with a semicolon
please write a script to accomlplish this

modify this code so that column 1 will have underscores replaced with space   
the replacement is to take place in the column 1 of the output file
'''
import csv

# Read the first file (file1) into a dictionary for fast lookup
file1 = {}
with open('augustus.dictionary.txt', 'r') as f1:
    reader = csv.reader(f1, delimiter='\t')
    for row in reader:
        index = row[0]  # First column: index
        name = row[1]   # Second column: name
        file1[index] = name

# Open the second file (file2) for reading and writing
with open('augustus.out.gff3', 'r') as f2:
    lines = f2.readlines()

# Process the second file line by line
modified_lines = []
for line in lines:
    columns = line.strip().split('\t')
    if len(columns) >= 9:
        col9 = columns[8]  # Column 9 (index 8 in 0-based index)
        col3 = columns[2]  # Column 3 (index 2 in 0-based index)
        
        # Check if index in file1 exists as a substring in column 9 of file2
        # and if column 3 is "CDS"
        for index, name in file1.items():
            if index in col9 and col3 == "CDS":
                # Append the name from file1 to column 9 with a semicolon
                columns[8] += f"product={name};"
                break  # Once we find a match, we can stop checking other indices
        
        # Replace underscores with spaces in column 1 (index 0)
        columns[0] = columns[0].replace('_', ' ')

    # Append the modified line to the list
    modified_lines.append("\t".join(columns))

# Write the modified content back to a new file
with open('augustus.named.gff3', 'w') as output_file:
    output_file.write("\n".join(modified_lines) + "\n")

print("Modification completed and saved to 'augustus.named.gff3'")

