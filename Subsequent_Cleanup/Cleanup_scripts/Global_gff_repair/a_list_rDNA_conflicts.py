'''
first copy rDNA conflict regions and paste into another file - problem is mixed tRNA and rRNA
try egrep ':rRNA' -A1 BDFB_principal_2.dr > rDNA_conflict_regions.txt
second, grep CDS from that file
grep 'CDS' rDNA_conflict_regions.txt > rDNA_CDS_conflicts.txt
third, make script to identify genes involved

I have a four column tab delimited file
I need test from the fourth column between lcl| and : to represent column one in a new file
I need the content between the : and the first dash as the second column in the new file. if this content starts with a letter, remove the letter and keep only the numbers.
I need the content between the dash and the next separator, which may be "," or tab. if this content starts with a letter, remove the letter and keep only the numbers. place this content in the third column of the new file.

for example
BDFB_principal_2.sqn:CDS	hypothetical protein	[lcl|JBANDU010000010.1:23464213-23464430, 23464611-23464761, 23465144-23465287]	V5W00_016243
BDFB_principal_2.sqn:CDS	hypothetical protein	lcl|JBANDU010000010.1:c23468658-23468056	V5W00_016249

should produce:
JBANDU010000010.1	23464213	23464430
JBANDU010000010.1	23468658	23468056
'''

import re

# Read the file
with open('BDFB_principal_2.dr', 'r') as infile:
    lines = infile.readlines()

# Extract lines matching ':rRNA' and the line after each match
conflict_regions = []
i = 0
while i < len(lines):
    if ':rRNA' in lines[i]:
        conflict_regions.append(lines[i])
        if i + 1 < len(lines):
            conflict_regions.append(lines[i + 1])
        i += 2  # Skip the next line since we already included it
    else:
        i += 1

# Save to rDNA_conflict_regions.txt
with open('rDNA_conflict_regions.txt', 'w') as outfile:
    outfile.writelines(conflict_regions)

# Now extract lines containing 'CDS' from that file
cds_conflicts = [line for line in conflict_regions if 'CDS' in line]

# Save to rDNA_CDS_conflicts.txt
with open('rDNA_CDS_conflicts.txt', 'w') as outfile:
    outfile.writelines(cds_conflicts)


# Function to process the content
def process_line(line):
    # Split the line by tab characters
    columns = line.strip().split('\t')

    # Ensure there are at least three columns before trying to access the third column
    if len(columns) < 3:
        return None  # Skip lines with fewer than 3 columns

    # Extract the 3rd column content (lcl| and beyond)
    third_column = columns[2]

    # Regular expression to match the parts
    match = re.search(r'lcl\|([A-Za-z0-9\.]+):([0-9c]+)-([0-9c]+)', third_column)
    
    if match:
        # Extract the values for column 1 (lcl), column 2 (first range), and column 3 (second range)
        column1 = match.group(1)
        
        # Remove leading "c" from the ranges (if present)
        column2 = match.group(2).lstrip('c')
        column3 = match.group(3).lstrip('c')

        return f"{column1}\t{column2}\t{column3}"
    return None  # Return None if no match is found

# Read input file and process
input_file = "rDNA_CDS_conflicts.txt"  # Replace with your actual input file
output_file = "rDNA_CDS_hitlist.txt"  # Replace with desired output file

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        processed_line = process_line(line)
        if processed_line:
            outfile.write(processed_line + '\n')

print("File processing complete.")

