'''
GPT prompt:
write a script to do the following:
skip lines with less than 9 columns
start a count for each line read
read a line of tab delimited text from infile
if the column 3 contains "tRNA" write the following to outfile:
the first two columns,
print "gene" as the third column
print columns 4 through 8
for column 9, print "ID=tRNA_gene" followed by the {count}
then a newline character
then print columns 1-8 again
now split column 9 into parts at semicolons
if part starts with "ID=" print the part and a semicolon
then print "parent=tRNA_gene" followed by the {count} and a semicolon
if part starts with "isotype=" then 
 split at "="
 make the new part contain "product=" followed by the part after "=" followed by a semicolon
then print a new line character
if the column 3 contains "exon" write the line to outfile:
iterate through the file and increment the counter for each line read


Personally modified the GPT script to actually split the original trna name designation and add .gene for parent identification.

'''

def process_file(infile_path, outfile_path):
    count = 1

    with open(infile_path, 'r') as infile, open(outfile_path, 'w') as outfile:
        outfile.write("##gff-version 3"'\n')
        for line in infile:
            columns = line.strip().split('\t')

            # Skip lines with less than 9 columns
            if len(columns) < 9:
                continue

            # Process tRNA lines
            if "tRNA" in columns[2]:
                # First make tRNA.gene
                parts = columns[8].split(';')
                new_col9 = ""
                for part in parts:
                    if part.startswith("ID="):
                        new_col9 += part + '.gene;'
                # build new line for gene 
                new_line_1 = '\t'.join([
                columns[0],
                columns[1],
                "gene",
                columns[3],
                columns[4],
                columns[5],
                columns[6],
                columns[7],
                new_col9
                ]) 
                outfile.write(new_line_1 + '\n')

                # Second output line (columns 1-8 + processed column 9)
                parts = columns[8].split(';')
                new_col9 = ""
                for part in parts:
                    if part.startswith("ID="):
                        name = part.split('=')[1]
                        new_col9 += f"ID={name};parent={name}.gene;"
                    elif part.startswith("isotype="):
                        key, value = part.split("=", 1)
                        new_col9 += f"product=tRNA-{value};"
                new_line_2 = '\t'.join(columns[0:8] + [new_col9])
                outfile.write(new_line_2 + '\n')
                count += 1  # Increment line count
            # Process exon lines
            elif "exon" in columns[2]:
                parts = columns[8].split(';')
                new_col9 = ""
                for part in parts:
                    if part.startswith("ID="):
                        name = part.split('.')
                        new_col9 = f"ID={name[0]}.{name[1]}.{name[2]}.{name[3]};parent={name[0]}.{name[1]}.{name[2]}.gene;"
                    # else:
                    #     new_col9 += part + ';'
                        
                # build new line for gene 
                new_line_1 = '\t'.join([
                columns[0],
                columns[1],
                columns[2],
                columns[3],
                columns[4],
                columns[5],
                columns[6],
                columns[7],
                new_col9
                ]) 
                outfile.write(new_line_1 + '\n')
            
# Example usage
input_file = 'BDFB_principal_trna.gff'  # Replace with your input file name
output_file = 'fixed_tRNA.gff3'  # Replace with your output file name
process_file(input_file, output_file)



