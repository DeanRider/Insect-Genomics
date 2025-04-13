
'''
fourth, remove those genes from the file and make new file without them
I have a tab delimited file and a second tab delimited file
I need to use the first file and match all three columns to the second file such that column 1 file 1 matched column 1 file2, column 2 file 1 matched column 4 file2, and column 3 file 1 matched column 5 file2. if a match is found, I need the text from column 9 between "ID=" and the first "." Once all those column 9 strings are collected, I want a list of all unique entries placed in a new file.

I need to modify this script so that col2_file1 can match either columns[1] or columns[2] and not worry about matching anything to col3_file1
the reason is that start and end positions are switched in one of the file types (NCBI warnings or the gff) the NCBI numbers with c in front are the complements (backwards start and end)
'''
import re

# Function to extract the ID between "ID=" and the first "." or new line or semicolon
def extract_id(text):
    # match = re.search(r'ID=([^\.]+)', text)
    match = re.search(r'ID=([^\.\n;]+)', text)
    if match:
        return match.group(1)
    return None

# Read both files and process them
def process_files(file1, file2, output_file):
    # Load file2 into a list for easy matching
    file2_data = []
    with open(file2, 'r') as f2:
        for line in f2:
            columns = line.strip().split('\t')
            if len(columns) >= 9:
                file2_data.append(columns)

    # Set to store unique IDs
    unique_ids = set()

    # Process file1 and match it against file2
    with open(file1, 'r') as f1:
        for line in f1:
            columns1 = line.strip().split('\t')
            if len(columns1) >= 3:
                # Extract columns from file1
                col1_file1 = columns1[0]
                col2_file1 = columns1[1]
                col3_file1 = columns1[2]

                # Match the columns from file1 to file2
                for row in file2_data:
                    if (col1_file1 == row[0] and  # Column 1 match
                       (col2_file1 == row[3] or col2_file1 == row[4])):  # Column 2 match
                        # col3_file1 == row[4]):    # Column 3 match

                        # Extract the ID from column 9 of file2
                        column9 = row[8]
                        extracted_id = extract_id(column9)
                        if extracted_id:
                            unique_ids.add(extracted_id)

    # Write the unique IDs to the output file
    with open(output_file, 'w') as out_file:
        for unique_id in sorted(unique_ids):
            out_file.write(unique_id + '\n')

    print(f"File processing complete. Unique IDs saved to {output_file}.")

# File paths (replace these with the actual file paths)
file1 = "rDNA_CDS_hitlist.txt"  # Replace with your file1 path
file2 = "BDFB_principal_2.gff3"  # Replace with your file2 path
output_file = "genes_to_kill.txt"  # Desired output file path

# Process the files
process_files(file1, file2, output_file)

