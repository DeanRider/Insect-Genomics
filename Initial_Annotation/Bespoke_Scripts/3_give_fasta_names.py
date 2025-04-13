'''
I have two files. One file contains fasta formatted protein sequences with identifiers. The other file is a tab delimited file that has a list of identifiers in column one and names in column two. I would like a script that will find matches to the identifiers in the fasta file by using the identifiers in the tab delimited file and if a match is found, add the name after the identifier in the fasta file. if there is no match in the tab delimited file, add "predicted protein" after the identifier in the fasta file. output the result to a file. 
'''

# Function to read the tab-delimited file and return a dictionary of identifiers to names
def load_identifier_mapping(tab_file):
    identifier_map = {}
    with open(tab_file, 'r') as f:
        for line in f:
            columns = line.strip().split('\t')
            identifier_map[columns[0]] = columns[1]
    return identifier_map

# Function to process the FASTA file and add names based on the identifiers
def process_fasta(fasta_file, identifier_map, output_file):
    with open(fasta_file, 'r') as fasta, open(output_file, 'w') as out:
        sequence = []
        for line in fasta:
            if line.startswith(">"):  # It's a header line
                # Extract identifier (the part after '>')
                identifier = line[1:].strip().split()[0]
                # Add the corresponding name or "predicted protein"
                if identifier in identifier_map:
                    name = identifier_map[identifier]
                else:
                    name = "predicted protein"
                # Write header with name appended and add to names dictionary
                out.write(f">{identifier} {name}\n")
                f = open("augustus.dictionary.txt", "a")
                f.write(f"{identifier}\t{name}\n")
                f.close()
            else:
                # It's a sequence line
                out.write(line)

# Main execution
def main():
    fasta_file = 'BDFB2025.augustus.fasta'  # Input FASTA file
    tab_file = 'augustus.named.proteins.txt'    # Tab-delimited file with identifiers and names
    output_file = 'augustus.named.proteins.fasta'  # Output FASTA file

    # Load the identifier-name mapping
    identifier_map = load_identifier_mapping(tab_file)
    
    # Process the FASTA file and write the result to the output file
    process_fasta(fasta_file, identifier_map, output_file)
    print(f"Processed FASTA file saved as '{output_file}'")

if __name__ == "__main__":
    main()

