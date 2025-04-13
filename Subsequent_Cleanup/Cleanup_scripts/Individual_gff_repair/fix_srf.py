'''
I have a tab delimited file
column 1 is an index
column 2 is a start position
column 3 is an end position
column 4 contains a string
column 7 contains a number
columns 5 and 6 and 8 are not needed

I want to revise the file to include 9 columns

I want to keep column 1 as the index, 
I want a new column 2 (source) and a new column 3 (primary_tag) 
fill column 2 with "SRF" and column 3 with "repeat_region"
the new column 4 should be the old start position but incremented by 1
the new column 5 should be the old end position incremented by 1
insert new columns 6-8 and fill each with periods
for the new column 9, start with the string from old column 4 and replace "BDFBp#circ" with the following:
"ID=BDFB_satellite_region_", followed by a number that increments higher on each row, followed by ";Name=BFDB_satellite_repeat_" 
then replace the dash with ";note=monomer length of "
and then add " nt;" at the very end of the column
as an example, BDFBp#circ26-9 should become ID=satellite_region_1_type_26;note=monomer length of 9 nt;
save tab delimited text file as BDFB_principal_srf.gff3
'''
import csv
import re

# Input and output file paths
input_file = 'BDFB.principal_ctg_srf.bed'  # Change this to your actual input file name
output_file = 'fixed_srf.gff3' # Change this to your desired output file name

# Initialize variables
counter = 1

# Open the input file for reading
with open(input_file, 'r') as infile:
    reader = csv.reader(infile, delimiter='\t')
    rows = []

    # Read each row and process
    for row in reader:
        # Extract the required columns
        index = row[0]
        start = int(row[1])
        end = int(row[2])
        string = row[3]
        
        # Create new columns
        new_row = []
        
        # Column 1: Index remains the same
        new_row.append(index)
        
        # Column 2: Add "SRF"
        new_row.append("SRF")
        
        # Column 3: Add "repeat_region"
        new_row.append("repeat_region")
        
        # Column 4: Start position + 1 because bed format is zero-based half-open, start positions are off by one compared to gff
        new_row.append(str(start + 1))
        
        # Column 5: End position + 0 because 0-based bed and 1-based gff end positions are identical
        new_row.append(str(end + 0))
        
        # Column 6-8: Periods (".")
        new_row.append(".")
        new_row.append(".")
        new_row.append(".")
        
        # Column 9: Process string and apply the transformation
        # Find the original number after "BDFBp#circ" using regex / modify if different in other srf runs
        match = re.search(r'BDFBp#circ(\d+)-(\d+)', string)
        if match:
            region_number = match.group(1)  # The number after BDFBp#circ (e.g., 26)
            monomer_length = int(match.group(2))  # The number after the dash (e.g., 9)

            # Construct the new formatted string / modify for different genomes
            new_string = f"ID=BFDB_satellite_region_{counter};note=BDFB repeat type {region_number}, monomer length of {monomer_length} nt;"
        else:
            # If the pattern is not found, keep the original string
            new_string = string
        
        new_row.append(new_string)
        
        # Add the row to the list of rows
        rows.append(new_row)
        
        # Increment the counter for the next row's unique number
        counter += 1

# Write the modified data to the output file
with open(output_file, 'w', newline='') as outfile:
    outfile.write("##gff-version 3"'\n')
    writer = csv.writer(outfile, delimiter='\t')
    writer.writerows(rows)

print(f"File has been saved as {output_file}")

