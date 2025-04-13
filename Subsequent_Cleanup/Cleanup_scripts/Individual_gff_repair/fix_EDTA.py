'''
if column 3 says "Gypsy_LTR_retrotransposon", replace column 3 with "mobile_element" and place ";mobile_element_type=Gypsy_LTR_retrotransposon"  at the end of column 9
if column 3 says "hAT_TIR_transposon", replace column 3 with "mobile_element" and place ";mobile_element_type=hAT_TIR_transposon"  at the end of column 9
if column 3 says "CACTA_TIR_transposon", replace column 3 with "mobile_element" and place ";mobile_element_type=CACTA_TIR_transposon"  at the end of column 9
if column 3 says "Mutator_TIR_transposon", replace column 3 with "mobile_element" and place ";mobile_element_type=Mutator_TIR_transposon"  at the end of column 9
if column 3 says "PIF_Harbinger_TIR_transposon", replace column 3 with "mobile_element" and place ";mobile_element_type=PIF_Harbinger_TIR_transposon"  at the end of column 9
if column 3 says "LTR_retrotransposon", replace column 3 with "mobile_element" and place ";mobile_element_type=LTR_retrotransposon"  at the end of column 9
if column 3 says "helitron", replace column 3 with "mobile_element" and place ";mobile_element_type=helitron"  at the end of column 9
if column 3 says "Tc1_Mariner_TIR_transposon", replace column 3 with "mobile_element" and place ";mobile_element_type=Tc1_Mariner_TIR_transposon"  at the end of column 9
if column 3 says "Copia_LTR_retrotransposon", replace column 3 with "mobile_element" and place ";mobile_element_type=Copia_LTR_retrotransposon"  at the end of column 9
if column 3 says "target_site_duplication", replace column 3 with "repeat_region" and place ";repeat_type=target_site_duplication" at the end of column 9

need to also remove any lines containing repeat_region_67 or repeat_region_69

'''
import csv

# Function to modify the content of each row
def modify_row(row):
    # Dictionary to map the conditions to their replacements
    replacements = {
        "Gypsy_LTR_retrotransposon": ("mobile_genetic_element", ";mobile_element_type=retrotransposon;note=Gypsy_LTR_retrotransposon"),
        "hAT_TIR_transposon": ("mobile_genetic_element", ";mobile_element_type=transposon;note=hAT_TIR_transposon"),
        "CACTA_TIR_transposon": ("mobile_genetic_element", ";mobile_element_type=transposon;note=CACTA_TIR_transposon"),
        "Mutator_TIR_transposon": ("mobile_genetic_element", ";mobile_element_type=transposon;note=Mutator_TIR_transposon"),
        "PIF_Harbinger_TIR_transposon": ("mobile_genetic_element", ";mobile_element_type=transposon;note=PIF_Harbinger_TIR_transposon"),
        "LTR_retrotransposon": ("mobile_genetic_element", ";mobile_element_type=retrotransposon;note=LTR_retrotransposon"),
        "helitron": ("mobile_genetic_element", ";mobile_element_type=transposon;note=helitron"),
        "Tc1_Mariner_TIR_transposon": ("mobile_genetic_element", ";mobile_element_type=transposon;note=Tc1_Mariner_TIR_transposon"),
        "Copia_LTR_retrotransposon": ("mobile_genetic_element", ";mobile_element_type=retrotransposon;note=Copia_LTR_retrotransposon"),
        "target_site_duplication": ("repeat_region", ";rpt_type=direct"),
        "long_terminal_repeat": ("repeat_region", ";rpt_type=long_terminal_repeat"),
        "repeat_region": ("biological_region", ";note=transposable element")
    }

    # Check if the value in column 3 matches any key in the dictionary
    if len(row) > 2 and row[2] in replacements:
        new_type, note = replacements[row[2]]
        row[2] = new_type
        if len(row) > 8:
            if row[8]:
                row[8] += f" {note}"
            else:
                row[8] = note

    return row

# Input and output file paths
input_file = 'BDFB_principal_renamed.fasta.mod.EDTA.intact.gff3'
output_file = 'fixed_EDTA.gff3'

# Read the input file and process each row
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    outfile.write("##gff-version 3"'\n')
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile, delimiter='\t')

    # Process each row
    for row in reader:
        # Skip rows containing "repeat_region_67" or "repeat_region_69"
        if any("repeat_region_67" in col or "repeat_region_69" in col for col in row):
            continue
        modified_row = modify_row(row)
        writer.writerow(modified_row)

print(f"File processing complete. The modified data has been written to {output_file}.")


