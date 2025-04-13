'''
I have a file and i want to search each line of the file for a list of strings in another file. If none of the strings are present in the line, put that line in a new file. if a string is found, then check if the string if followed immediately by a new line character and if it is, do not put that line into the new file. then check if the string is followed immediately by a period (dot) and if it is do not put the line into the new file. otherwise, put the line into the file. please write a script to do this.

if the list contains "dean"
and the file contained:

i am dean
i am not dean. dean is fine
i am not dean, dean is fine

then the first line would be excluded because dean if followed by new line
the second line would be excluded because dean is followed by period
the third line would be printed because dean is not followed by new line or period
'''

def read_strings(file_path):
    # Read the list of strings from the file and return them as a list
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def process_file(input_file, strings_list, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Flag to check if the line should be written to the output file
            write_line = True
            for string in strings_list:
                if string in line:
                    # Check if the string is followed by a period or newline (end of line) or semicolon
                    if line.endswith(f"{string}\n") or line.endswith(f"{string};\n") or f"{string}." in line:
                        write_line = False
                        break
            
            # If no conditions matched, write the line to the output file
            if write_line:
                outfile.write(line)

# Define file paths
input_file = 'BDFB_principal_2.gff3'
strings_file = 'genes_to_kill.txt'
output_file = 'BDFB_principal_3.gff3'

# Read the list of strings from the strings file
strings_list = read_strings(strings_file)

# Process the input file and write the result to the output file
process_file(input_file, strings_list, output_file)

print("File processing complete. The filtered lines have been written to:", output_file)
