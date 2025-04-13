'''
i have a tab delimited file. write a script to change the third column to "repeat_region" unless the string is "region" and also do not print any line that begins with "#"
'''
# Python script to process the tab-delimited file

def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        outfile.write("##gff-version 3"'\n')
        for line in infile:
            # Skip lines that start with '#'
            if line.startswith('#'):
                continue

            # Split the line into columns using tab as delimiter
            columns = line.strip().split('\t')
            
            # Skip the line if the third column is "region"
            if columns[2] == "region":
                continue

            # Change the third column to "repeat_region" unless it's "region"
            if columns[2] != "region":
                columns[2] = "repeat_region"
            
            # Write the updated line to the output file
            outfile.write('\t'.join(columns) + '\n')

# Example usage:
input_file = 'misa.gff3'  # Replace with your input file name
output_file = 'fixed_misa.gff3'  # Replace with your desired output file name
process_file(input_file, output_file)

