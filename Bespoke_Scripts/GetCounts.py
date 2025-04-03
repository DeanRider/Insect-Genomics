def compare_lines_with_next(file_path, output_file_path):
    # Open the input file and output file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(output_file_path, 'w') as output_file:
        # Iterate through each line except the last one
        for i in range(len(lines) - 1):
            current_line = lines[i].strip()
            next_line = lines[i + 1].strip()

            # Split lines into words
            current_words = set(current_line.split())
            next_words = set(next_line.split())

            # Find intersection of words
            matching_words = current_words.intersection(next_words)

            # Write the original line followed by the count of matching words
            output_file.write(f"{current_line} | Matching words with next line: {len(matching_words)}\n")

# Example usage
input_file_path = 'HomologNames.txt'  # Replace with your input file path
output_file_path = 'HomologNamesCompared.txt'  # Replace with your desired output file path
compare_lines_with_next(input_file_path, output_file_path)

