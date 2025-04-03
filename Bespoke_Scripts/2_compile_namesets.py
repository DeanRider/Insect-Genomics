'''
I have three tab delimited files. Each has two columns.
I want all entries from the first file put into a new file, including columns 1 and columns 2.
Then compare the entries in the first column of each file to: 
a) identify those entries that are unique to file 2 but not in file 1 and
for each of those unique entries, add those entries to the new file, including columns 1 and columns 2.
b) then identify those entries that are unique to file 3 that are not in either file 1 or file 2 and
for each of those entries, add those entries to the new file, including columns 1 and columns 2.
'''

# Function to read a tab-delimited file into a list of rows and a set of the first column
def read_file(file_path):
    rows = []
    first_column = set()
    with open(file_path, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            rows.append(columns)
            first_column.add(columns[0])
    return rows, first_column

# Read the three files
file1_rows, file1_first_col = read_file('BestReciprocalHomologNames.txt')
file2_rows, file2_first_col = read_file('KO_names.txt')
file3_rows, file3_first_col = read_file('Interpro.Named_proteins.txt')

# Write the new file
with open('augustus.named.proteins.txt', 'w') as new_file:
    # Write all rows from file1
    for row in file1_rows:
        new_file.write('\t'.join(row) + '\n')

    # Add rows from file2 that are unique (not in file1)
    for row in file2_rows:
        if row[0] not in file1_first_col:
            new_file.write('\t'.join(row) + '\n')

    # Add rows from file3 that are unique (not in file1 or file2)
    for row in file3_rows:
        if row[0] not in file1_first_col and row[0] not in file2_first_col:
            new_file.write('\t'.join(row) + '\n')

print("New file has been created: augustus.names.output.txt")
