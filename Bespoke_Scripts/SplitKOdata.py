import csv

# Define the input and output file paths
input_file = 'All_user_ko_definition.tsv'  # Change this to the path of your input file
output_file = 'All_user_ko_splitCols.txt'  # Change this to the desired output file path

# Open the input file for reading and the output file for writing
with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    # Create a CSV reader and writer to handle tab-delimited data
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile, delimiter='\t')
    
    # Iterate through each row in the input file
    for row in reader:
        # Modify the third column (index 2) by replacing ";" and " [EC:"
        if len(row) >= 3:  # Ensure the row has at least 3 columns
            row[2] = row[2].replace("; ", "\t").replace(" [EC:", "\t[EC:")
        
        # Write the modified row to the output file
        writer.writerow(row)

print("File processed successfully!")
