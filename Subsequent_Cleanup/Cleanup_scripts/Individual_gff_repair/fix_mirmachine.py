'''
write a script to do the following:
start a count for each line read
read a line of tab delimited text from infile
write the following to outfile:
the first two columns,
print "gene" as the third column
print columns 4 through 8
for column 9, print "ID=mirmachine_miRNA_" followed by the {count}
then a newline character
then print columns 1-8 again
now split column 9 into parts at semicolons
if part starts with "gene_id" then 
 split at "="
 make the new part contain "ID=" followed by the part after "=" followed by "_mirmachine_miRNA_{count};parent=mirmachine_miRNA_{count};" followed by "product=" then the part after the "=" followed by a semicolon

if part starts with "sequence_with_30nt"
 split at "=" then
 make the new part contain "note=sequence with 30nt is" followed by the part after the "="
then print a new line character

iterate through the file and increment the counter for each line read
modify to skip lines with less than 9 columns
'''

# Open the input and output files
with open('mirmachine.gff', 'r') as infile, open('fixed_mirmachine.gff3', 'w') as outfile:
    # Initialize the count
    count = 1
    outfile.write("##gff-version 3"'\n')
    # Iterate through each line in the input file
    for line in infile:
        # Split the line by tabs into a list of columns
        columns = line.strip().split('\t')

        # Skip lines with less than 9 columns
        if len(columns) < 9:
            continue

        # Write the first two columns and "gene" as the third column
        outfile.write(f"{columns[0]}\t{columns[1]}\tgene\t")

        # Write columns 4 through 8
        outfile.write("\t".join(columns[3:8]) + "\t")

        # Write "ID=mirmachine_miRNA_" followed by the count for column 9
        outfile.write(f"ID=mirmachine_miRNA_{count}\n")

        # Now print columns 1-8 again
        outfile.write("\t".join(columns[:8]) + "\t")

        # Split column 9 into parts at semicolons
        parts = columns[8].split(';')

        for part in parts:
            # Check if the part starts with "gene_id"
            if part.startswith("gene_id"):
                gene_id_part = part.split("=")
                gene_id_value = gene_id_part[1]
                # Construct the new gene_id part and write it
                outfile.write(f"ID={gene_id_value}_mirmachine_miRNA_{count};parent=mirmachine_miRNA_{count};product={gene_id_value};")

            # Check if the part starts with "sequence_with_30nt"
            elif part.startswith("sequence_with_30nt"):
                sequence_part = part.split("=")
                sequence_value = sequence_part[1]
                # Construct the new sequence part and write it
                outfile.write(f"note=sequence with 30nt is {sequence_value};")

        # Print a new line character after processing column 9
        outfile.write("\n")

        # Increment the count for the next line
        count += 1
