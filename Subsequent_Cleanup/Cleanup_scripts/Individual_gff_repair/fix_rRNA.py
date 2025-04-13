'''
modified older script used for tRNA processing
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

            # Skip lines with partials
            if "partial" in columns[8]:
                continue
                
            # Skip lines with short 28s
            if "28S" in columns[8] and abs(int(columns[4]) - int(columns[3])) < 3000:
                continue
                
            # Process rRNA lines
            if "rRNA" in columns[2]:
                # First make rRNA gene
                parts = columns[8].split(';')
                new_col9 = ""
                for part in parts:
                    if part.startswith("Name="):
                        name = part.split('=')[1]
                        new_col9 = f"ID={name}_gene_{count};"
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
                    if part.startswith("Name="):
                        name = part.split('=')[1]
                        new_col9 += f"ID={name}_{count};parent={name}_gene_{count};"
                    elif part.startswith("product="):
                        key, value = part.split("=", 1)
                        # may need to fix if partial is not allowed
                        if value.endswith(" (partial)"):
                            cleaned_text = value.replace(" (partial)", "")
                            new_col9 += f"product={cleaned_text};"
                        else:
                            new_col9 += f"product={value};"
                    elif part.startswith("Note="):
                        key, value = part.split("=", 1)
                        new_col9 += f"Note={value};"
                new_line_2 = '\t'.join(columns[0:8] + [new_col9])
                outfile.write(new_line_2 + '\n')
                count += 1  # Increment line count
            # Process exon lines
            elif "exon" in columns[2]:
                outfile.write(line)
            
# Example usage
input_file = 'BDFB_principal_pybarrnap.gff'  # Replace with your input file name
output_file = 'fixed_rRNA_long.gff3'  # Replace with your output file name
process_file(input_file, output_file)


'''

if value.endswith(" (partial)"):
                            cleaned_text = value.replace(" (partial)", "")
                            new_col9 += f"product={cleaned_text};"
                        else:
                            
                            
                            
'''
