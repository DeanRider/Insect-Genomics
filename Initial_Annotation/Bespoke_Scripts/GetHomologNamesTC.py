# Define the file paths
file2_path = 'genomes/GCF_031307605.1_icTriCast1.1_protein.faa'  # Replace with the path to your first file
file1_path = 'TC_BDFB_compRuns1/augustus.hints.aa/homologs_awk.txt'  # Replace with the path to your second file
output_file_path = 'HomologNamesTC.txt'  # Replace with the desired output file path

# Open the second file and load it into memory for searching
with open(file2_path, 'r') as file2:
    file2_lines = file2.readlines()

# Open the output file in append mode
with open(output_file_path, 'a') as output_file:
    # Open the first file and iterate through its lines
    with open(file1_path, 'r') as file1:
        for line1 in file1:
            # Split the line from the first file into columns
            columns1 = line1.strip().split(' ')  # Assuming tab-delimited files
            
            # Extract the string from the second column of the first file
            search_str = columns1[1]
            
            # Search for a matching line in the second file
            for line2 in file2_lines:
                if search_str in line2:
                    # If a match is found, write the result to the output file
                    output_line = f"{columns1[0]}\t{columns1[1]}\t{line2.strip()}\n"
                    output_file.write(output_line)
                    break  # Stop after the first match is found
