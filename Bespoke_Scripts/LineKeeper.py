# Open the input file for reading and output file for writing
with open('HomologNamesComparedTab.txt', 'r') as infile, open('output_file.txt', 'w') as outfile:
    # Read all lines from the input file
    lines = infile.readlines()

    # Iterate through each line in the file except for the last one
    for i in range(len(lines) - 1):
        # Split each line by the tab character and get the value of the third column (index 2)
        columns_current = lines[i].strip().split('\t')
        columns_next = lines[i + 1].strip().split('\t')

        # Check if column three of both current and next lines is 2 or greater
        if float(columns_current[2]) >= 2 and float(columns_next[2]) >= 2:
            # If the condition is met, write the current line to the output file
            outfile.write(lines[i])

