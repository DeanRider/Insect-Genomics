#####################################################################
#
# THIS IS A PIPELINE FOR TURNING INTERPROSCAN RESULTS INTO PROTEIN
# NAMES FOR GENOME ANNOTATION. IT WAS GENERATED AS A SERIES OF
# INQUIRIES WITH CHAT GPT AND EACH RESULT WAS MODIFIED TO GENERATE 
# THE DESIRED RESULTS. THE PROMPTS ARE INCLUDED FOR REFERENCE.
#
# THE VERSION OF INTERPROSCAN USED FOR INPUT WAS 5.63-95.0 
#
#####################################################################


#####################################################################
#
# Fixes remaining = dash space in certain instances but not all
#
#####################################################################

'''
#####################################################################
#
# Begin to Clean Interproscan Output
#
#####################################################################
import csv

# Input and output file names
input_file = 'BDFB2025.augustus.fasta.tsv' # Replace with the path to your input file
output_file = 'InterproCleaned.tsv' # Replace with the path to your output file

# Open input file for reading and output file for writing
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    # Create CSV readers and writers
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile, delimiter='\t')

    # Iterate through each row in the input file
    for row in reader:
    # Check the value in the 12th column (index 11)
        column_12 = row[11]
        
        # Handle cases based on the value of column 12
        if column_12.startswith("IPR"):
            writer.writerow([row[0], row[12], row[11], row[6], row[7], row[8]])
            
print("Cleaning columns is complete.")
#####################################################################
'''
#####################################################################
#
# I changed my approach to be using the JSON dataset and focus on only 
# IPR that are not INCOMPLETE ... debated on N and C terminal ones
#
#####################################################################

import json
import csv

# Function to load and parse JSON from a file
def parse_json_file(file_path):
    try:
        # Open the JSON file
        with open(file_path, 'r') as file:
            # Parse the JSON data
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to convert JSON to TSV format grouped by 'id'
def json_to_tsv_grouped_by_id(json_data, output_file_path):
    try:
        # Open the output TSV file
        with open(output_file_path, 'w', newline='') as tsv_file:
            writer = csv.writer(tsv_file, delimiter='\t')
            
            # Write the header row for the TSV file
            header = [
                'id', 'entry_description', 'entry_accession', 
                'location_start', 'location_end', 'completeness'
            ]
            writer.writerow(header)
            
            # Iterate through each result and extract the necessary data
            for result in json_data['results']:
                # sequence = result['sequence']
                # md5 = result['md5']
                
                # If there are matches, we loop through them
                if result['matches']:
                    for match in result['matches']:
                        signature = match['signature']
                        if signature['entry']:
                            signature_entry = signature['entry']
                            entry_accession = signature['entry'].get('accession', '-')
                            entry_description = signature['entry'].get('description', '-')
                        else:
                            signature_entry = '-'
                            entry_accession = '-'
                            entry_description = '-'
                        
                        # Loop through locations inside each match
                        for location in match['locations']:
                            location_start = location.get('start', '')
                            location_end = location.get('end', '')
                            location_bound = location.get('hmmBounds', '')  # Use .get() to handle missing hmmBounds
                            
                            # Handle location-fragments (dc-status)
                            location_dc_status = location.get('location-fragments', [{}])[0].get('dc-status', '')
                            
                            # Extract xref details (they are outside of the match)
                            xref_name = result['xref'][0]['name']
                            xref_id = result['xref'][0]['id']
                            
                            # Write a row for each match and location combination
                            row = [
                                xref_id, entry_description, entry_accession, 
                                location_start, location_end, location_bound
                            ]
                            writer.writerow(row)
                else:
                    # If no matches, write a row with empty match data
                    for xref in result['xref']:
                        row = [
                            xref['id'], '-', '-', '-', '-', '-'
                        ]
                        writer.writerow(row)
                
        print(f"TSV file saved as {output_file_path}")
    
    except Exception as e:
        print(f"An error occurred while writing to TSV: {e}")

# Example usage
if __name__ == "__main__":
    json_file_path = "BDFB2025.augustus.fasta.json"  # Replace with your JSON file path
    tsv_file_path = "augustus.json.parts.tsv"     # Path for the output TSV file
    
    # Parse the JSON data
    parsed_data = parse_json_file(json_file_path)
    
    if parsed_data:
        # Convert to TSV grouped by "id"
        json_to_tsv_grouped_by_id(parsed_data, tsv_file_path)

#####################################################################
#
# Next Keep only COMPLETE and _COMPLETE domains
# 
#####################################################################
'''i have a tab delimited file with six columns. I want to keep only lines where the sixth column contains "COMPLETE" or where part of the string says "_COMPLETE" but avoid ones where the entry contains in whole or in part "INCOMPLETE" or is empty and outpu this to a new file

can you modify the script to eliminate lines where column 2 is empty or contains only a dash
'''
# import csv

# Input and output file paths
input_file = 'augustus.json.parts.tsv'  # replace with your actual input file path
output_file = 'augustus.json.complete.tsv'  # replace with your desired output file path

# Open the input file and output file
with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    # Create a CSV reader and writer
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile, delimiter='\t')

    # Iterate through each row in the input file
    for row in reader:
        # Check if column 2 is empty or contains only a dash
        if not row[1] or row[1] == '-':
            continue  # Skip this row if the condition is met
        
        # Check the condition for the sixth column
        sixth_column = row[5]  # Since columns are zero-indexed, column 6 is at index 5
        
        if sixth_column:
            if "COMPLETE" in sixth_column and "INCOMPLETE" not in sixth_column:
                # Write the row to the output file
                writer.writerow(row)



#####################################################################
#
# Next Fix the before and after text
#
#####################################################################
'''
This script was generated by ChatGPT with the following prompt:

I have a tab delimited file. write a script that will examine the content of the second column and do the following:
If the column begins with ‚"Similar to‚" then remove that beginning phrase
If the column begins with ‚"Similar to‚" then remove that beginning phrase
If the column begins with ‚"AGAP‚" then replace entire cell with "uncharacterized protein"
If the column contains only ‚"-‚" then replace entire cell with "uncharacterized protein"
If the column begins with ‚"Si:‚" then replace entire cell with "uncharacterized protein"
If the column begins with ‚"SI:‚" then replace entire cell with "uncharacterized protein"
If the column ends with ‚"DOMAIN-CONTAINING‚" then replace that ending with "DOMAIN-CONTAINING PROTEIN‚"
If the column ends with ‚"family‚" then replace that ending with ‚"family protein"
If the column ends with ‚" RELATED‚" then replace that ending with ‚"-LIKE PROTEIN‚"
If the column ends with ‚"-RELATED‚" then replace that ending with ‚"-LIKE PROTEIN‚"
If the column ends with ‚"-RELATED PROTEIN‚" then replace that ending with ‚"-LIKE PROTEIN‚"
If the column ends with ‚"domain‚" then replace that ending with ‚"domain-containing protein‚"
If the column ends with ‚"transmembrane‚" then replace that ending with ‚"transmembrane protein‚"
If the column ends with ‚" homolog‚" then replace that ending with ‚"-like protein‚"
If the column ends with ‚", putative‚" then remove that ending phrase
If the column ends with ‚"FAMILY‚" then replace that ending with ‚"FAMILY PROTEIN‚"
If the column ends with ‚"PROTEIN FAMILY‚" then replace that ending with ‚"FAMILY PROTEIN‚"
If the column ends with ‚"MEMBER‚" then replace that ending with 
If the column ends with ‚"repeat‚" then replace that ending with ‚"repeat-containing protein‚"
If the column ends with ‚"WITH COILED-COIL‚" then replace that ending with WITH COILED-COIL MOTIF
If the column ends with ‚" PROTEIN-RELATED-RELATED‚" then replace that ending with ‚"-LIKE PROTEIN‚"
If the column ends with ‚"UNCHARACTERIZED‚" then replace that ending with ‚"UNCHARACTERIZED PROTEIN‚"
If the column ends with ‚" HOMOLOG‚" then replace that ending with ‚"-LIKE PROTEIN‚"
If the column ends with ‚"finger‚" then replace that ending with ‚"finger protein‚"
If the column ends with ‚"STRUCTURAL CONTITUENT OF CUTICLE‚" then replace that ending with ‚"STRUCTURAL CONSTITUENT OF CUTICLE"
If the column ends with ‚"MEMEBER‚" then replace that ending with 
If the column ends with ‚"DOMAIN-CONTAINING PROTEIN-RELATED‚" then replace that ending with 

Store the altered content into a new file

Most of these conditions were deleted when I switched to IPR-only designations and column 13 names
'''

# import csv
import re

# Function to process the second column
def process_column(value):

    if value.endswith("protein"):
        return value
    elif value.endswith(" proteins"):
        return value.replace(" proteins", " protein")
    elif value.endswith(" PROTEINS"):
        return value.replace(" PROTEINS", " PROTEIN")
    elif value.endswith("PROTEIN"):
        return value
    elif value.endswith("Protein"):
        return value
    elif value.endswith("enzyme"):
        return value
    elif value.endswith("ENZYME"):
        return value
    # changed uppercase to ignore and use lower case protein at end of
    elif value.isupper():
        return value + " protein"
    else:
        return value + " protein"

# Read the original tab-delimited file, process it, and write to a new file
def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            if len(row) >= 2:  # Ensure there's at least 2 columns
                # Process the second column
                row[1] = process_column(row[1])
            # Write the modified row to the output file
            writer.writerow(row)

# Specify your input and output file paths
input_file = 'augustus.json.complete.tsv'  # Change to your input file path
output_file = 'PrefixSuffix.tsv'  # Change to your desired output file path

process_file(input_file, output_file)

print(f"Name revision complete. The modified file is saved as {output_file}.")
#####################################################################



#####################################################################
#
# Next Select Longest Non-Overlapping domains
#
#####################################################################
'''
This script was generated by ChatGPT with the following prompt:

I have a tab delimited file with lines that contain
parent string name
substring name
method used to identify the substring
e value
start position of the substring within the parent string
end position of the substring within the parent string

please write a script that will:
1) first group entries by parent string
2) find all substrings that overlap each other and keep only the names of the substrings with the smallest e values
3) output the lines that have the non-overlaping substrings with the highest e values for each parent string

A prompt was made to alter the file so that the longest sub_string was kept instead of the one with the smallest e-value

other modifications were made by S. Dean Rider Jr. in March, 2025
'''
import pandas as pd

# Function to find overlapping substrings
def is_overlapping(start1, end1, start2, end2):
    # Check if two ranges [start1, end1] and [start2, end2] overlap
    return not (end1 <= start2 or end2 <= start1)

# Read the tab-delimited file into a pandas DataFrame
def process_file(file_path):
    # Read the data from the file
    df = pd.read_csv(file_path, sep='\t', header=None, names=[
        'parent_string', 'substring_name', 'method', 'start_pos', 'end_pos', 'completeness'
    ])
    
    # Convert 'start_pos', and 'end_pos' to numeric types
    df['start_pos'] = pd.to_numeric(df['start_pos'], errors='coerce')
    df['end_pos'] = pd.to_numeric(df['end_pos'], errors='coerce')
    
    # Group by 'parent_string'
    grouped = df.groupby('parent_string')
    
    # To store the final filtered results
    final_results = []
    
    for parent, group in grouped:
        # Sort group by the length of the substring (longest first)
        group['length'] = group['end_pos'] - group['start_pos']
        group_sorted = group.sort_values(by='length', ascending=False)
        
        # List to keep track of the non-overlapping substrings
        non_overlapping = []
        
        # Iterate over sorted group and find non-overlapping substrings
        for idx, row in group_sorted.iterrows():
            # Check if the current substring overlaps with any in the non-overlapping list
            overlap_found = False
            for existing_row in non_overlapping:
                if is_overlapping(row['start_pos'], row['end_pos'], existing_row['start_pos'], existing_row['end_pos']):
                    overlap_found = True
                    break
            if not overlap_found:
                non_overlapping.append(row)
        
        # Append the non-overlapping substrings for this parent string to the final results
        final_results.extend(non_overlapping)
    
    # Convert the final results back to a DataFrame
    final_df = pd.DataFrame(final_results)
    
    # Output the final results
    return final_df

# Output the results to a new file (optional)
def save_results(final_df, output_path):
    final_df.to_csv(output_path, sep='\t', index=False, header=False)

# Main function to process the file
if __name__ == '__main__':
    input_file = 'PrefixSuffix.tsv'  # Replace with the actual input file path
    output_file = 'LongDomains.tsv'  # Replace with the desired output file path
    
    final_df = process_file(input_file)
    
    # Output results to the console
    print(final_df)
    
    # Optionally save to file
    save_results(final_df, output_file)
    
print("Longest Domains Identified.")
#####################################################################    


#####################################################################
#
# Next Remove Domains with very similar names (these are suspicious)
#
#####################################################################
'''
This script was generated by ChatGPT with the following prompt:

I have a tab delimited input file that contains:
parent_string
sub_string
method
start_pos
end_pos
e_value

write a script that will do the following:
read the input file and group entries by parent_string
if a group has only one entry, output it to a file called OneDomain.tsv
if a group has multiple entries, examine sub_strings and if there are duplicates, keep the ones with the smallest e_values
for the entries that remain, identify the two sub_strings with the longest lengths using the start_pos and end_pos
then determine if the two sub_strings share any words in common, and if they do, flag them as "suspicious"
output these two entries to a file called MultiDomains.tsv including the entire original lines with a new column for the suspicious flag

please further modify the script so that the not suspicious entries go to one new file and the suspicious ones go to another new file

modify the script so that for the suspicious ones, keep only the sub_string with the longest entry for output to the file
'''

# import csv
from collections import defaultdict

# Function to get the length of a sub_string from start_pos and end_pos
def get_substring_length(start_pos, end_pos):
    return int(end_pos) - int(start_pos)

# Function to check if two sub_strings share any common words
'''
def are_suspicious(sub_string1, sub_string2):
    words1 = set(sub_string1.split())  # Split by whitespace to get individual words
    words2 = set(sub_string2.split())
    return not words1.isdisjoint(words2)  # Return True if they share common words
'''    
# I want to revise this function to ignore common words and return true if at least half the words are the same

'''
def are_suspicious(sub_string1, sub_string2):
    # Split the sub_strings into words and remove "protein"
    words1 = set(word for word in sub_string1.split() if word.lower() != "protein")
    words2 = set(word for word in sub_string2.split() if word.lower() != "protein")
    
    # Find the common words between both sets
    common_words = words1.intersection(words2)
    
    # Calculate the threshold for at least half of the words in either string
    half_words1 = len(words1) / 2
    half_words2 = len(words2) / 2
    
    # Return True if at least half of the words in either sub_string are common
    return len(common_words) >= half_words1 or len(common_words) >= half_words2
'''

def are_suspicious(sub_string1, sub_string2):
    # List of words to ignore
    ignore_words = {
        "domain", "superfamily", "protein", "C-terminal", "N-terminal", "site",
        "family", "subunit", "repeat", "receptor", "motif", "type", "synthase",
        "region", "kinase", "finger", "factor", "Protein"
    }
    
    # Split the sub_strings into words and remove any of the ignore words
    words1 = set(word for word in sub_string1.split() if word.lower() not in ignore_words)
    words2 = set(word for word in sub_string2.split() if word.lower() not in ignore_words)
    
    # Find the common words between both sets
    common_words = words1.intersection(words2)
    
    # Calculate the threshold for at least half of the words in either string
    half_words1 = len(words1) / 2
    half_words2 = len(words2) / 2
    
    # Return True if at least half of the words in either sub_string are common
    return len(common_words) >= half_words1 or len(common_words) >= half_words2


# Function to read the input file and process the data
def process_file(input_filename):
    # Define the column names since the input file has no header
    fieldnames = ['parent_string', 'sub_string', 'method', 'start_pos', 'end_pos', 'e_value']
    
    # Create dictionaries to store the results
    one_domain = []
    suspicious_domains = []
    not_suspicious_domains = []
    
    # Read the input file
    with open(input_filename, 'r') as infile:
        reader = csv.reader(infile, delimiter='\t')
        
        # Group entries by parent_string
        grouped_entries = defaultdict(list)
        for row in reader:
            # Map the row to the respective column names
            entry = dict(zip(fieldnames, row))
            
            # Convert e_value to float, if possible
            try:
                entry['e_value'] = float(entry['e_value'])
            except ValueError:
                # Handle the case where e_value cannot be converted to a float
                entry['e_value'] = float('inf')  # Assign a large value to invalid e_value
            
            grouped_entries[entry['parent_string']].append(entry)
        
        # Process each group
        for parent_string, entries in grouped_entries.items():
            if len(entries) == 1:
                # If only one entry, append it to OneDomain.tsv
                one_domain.append(entries[0])
            else:
                # For multiple entries, filter duplicates based on sub_string and keep smallest e_value
                seen_sub_strings = {}
                for entry in entries:
                    sub_string = entry['sub_string']
                    e_value = entry['e_value']
                    
                    # If we haven't seen the sub_string or the e_value is smaller, store the entry
                    if sub_string not in seen_sub_strings or e_value < seen_sub_strings[sub_string]['e_value']:
                        seen_sub_strings[sub_string] = entry
                
                # Now we have the unique sub_strings with the smallest e_values
                remaining_entries = list(seen_sub_strings.values())
                
                # Sort entries based on the length of sub_strings (start_pos and end_pos)
                remaining_entries.sort(key=lambda x: get_substring_length(x['start_pos'], x['end_pos']), reverse=True)
                
                # Get the two longest sub_strings
                if len(remaining_entries) >= 2:
                    sub_string1 = remaining_entries[0]['sub_string']
                    sub_string2 = remaining_entries[1]['sub_string']
                    
                    # Check if these two sub_strings are suspicious
                    suspicious_flag = 'suspicious' if are_suspicious(sub_string1, sub_string2) else 'not_suspicious'
                    
                    # Add the suspicious flag to the entries
                    remaining_entries[0]['suspicious'] = suspicious_flag
                    remaining_entries[1]['suspicious'] = suspicious_flag
                    
                    # Append the entries to the appropriate file list
                    if suspicious_flag == 'suspicious':
                        # Keep only the entry with the longest sub_string for suspicious
                        longer_entry = remaining_entries[0] if get_substring_length(remaining_entries[0]['start_pos'], remaining_entries[0]['end_pos']) > get_substring_length(remaining_entries[1]['start_pos'], remaining_entries[1]['end_pos']) else remaining_entries[1]
                        suspicious_domains.append(longer_entry)
                    else:
                        not_suspicious_domains.extend(remaining_entries[:2])
    
    # Write the results to OneDomain.tsv
    with open('OneDomain.tsv', 'w', newline='') as one_domain_file:
        writer = csv.DictWriter(one_domain_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(one_domain)
    
    # Write suspicious entries to SuspiciousDomains.tsv
    fieldnames.append('suspicious')  # Add the suspicious column to the header
    with open('SuspiciousDomains.tsv', 'w', newline='') as suspicious_file:
        writer = csv.DictWriter(suspicious_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(suspicious_domains)

    # Write not suspicious entries to NotSuspiciousDomains.tsv
    with open('NotSuspiciousDomains.tsv', 'w', newline='') as not_suspicious_file:
        writer = csv.DictWriter(not_suspicious_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(not_suspicious_domains)

# Call the function with the input filename
process_file('LongDomains.tsv')

print("Similarly named regions have been removed.")
#####################################################################


#####################################################################
#
# Next Combine Domains for Multidomain Proteins
#
#####################################################################
'''
I used ChatGPT to write this initial script using the following prompt:

I have a tab delimited file with the following 7 columns:
parent_string
sub_string
method
start_pos
end_pos
e_value
suspicious

The columns have headers.

write a python script that will do the following
read the file and group entries by parent_string
check that each parent_string has only two entries with different sub_string
if they do not pass this test, print all the entries for this parent_string to a file called rejects
If they do apss the test, do the following:
sort the two entries by start_pos in ascending order
examine the first substring and if it ends in the word "protein", remove the word "protein". The test of the word "protein" is case insensitive.
now combine the modified substring with the second substring using a slash "/" between the two substrings.
for example combined_substring = sub_string1 / sub_string2
now write two columns to an output file that contains the parent_string and combined_substring in tab-delimited format.

now modify to handle the following:
DeprecationWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.



The script was modified as needed in March 2025 by S. Dean Rider Jr.
'''

# OPTION 3 more made by Dean
# Option 3 was made because it appeared Option 2 did not work. It turns out Python was appending the original output file.
# Thus, It looked as if the data was unchanged in the output if you only view the head. The good data was at the bottom of the file and worked as desired.
'''
import pandas as pd
import re

# Read the input file into a DataFrame
input_file = "NotSuspiciousDomains.tsv"  # Replace with your actual file path
df = pd.read_csv(input_file, sep='\t')

# Create a function to process the first substring (removing "protein" from the end)
def process_first_substring(sub_string):
    # Remove " protein" (case insensitive) from the end of the substring
    sub_string = re.sub(r' protein$', '', sub_string, flags=re.IGNORECASE).strip()
    return sub_string

# Function to process the first name
def process_first(value):
    if value.endswith(" PROTEIN"):
        return value.replace(" PROTEIN", "")
    elif value.endswith(" Protein"):
        return value.replace(" Protein", "")
    elif value.endswith(" protein"):
        return value.replace(" protein", "")
    elif value.endswith("enzyme"):
        return value
    elif value.endswith("ENZYME"):
        return value
    else:
        return value
               
# Create a function to handle each parent_string group
def handle_parent_group(group):
    # Check if there are exactly two distinct sub_strings
    if len(group['sub_string'].unique()) != 2:
        # Write the parent_string entries to rejects file
        group.to_csv('Multidomain_rejects.txt', sep='\t', header=True, index=False, mode='a')
    else:
        # Sort by start_pos in ascending order
        group = group.sort_values(by='start_pos')

        # Get the two substrings
        sub_string1 = group.iloc[0]['sub_string']
        sub_string2 = group.iloc[1]['sub_string']

        # Combine the substrings
        combined_substring = f"{process_first(sub_string1)} / {sub_string2}"
        
        # Write the result to the output file
        with open('Multidomain_output.txt', 'a') as f_out:
            f_out.write(f"{group.iloc[0]['parent_string']}\t{combined_substring}\n")

# Group by parent_string and apply the processing function to each group
# Select the grouping columns explicitly to avoid deprecation warning
grouped = df.groupby('parent_string', as_index=False)

# Apply the function to each group
for name, group in grouped:
    handle_parent_group(group)

print("Processing complete. Check the 'output.txt' and 'rejects.txt' files.")


'''
# OPTION 2 Revised GPT version
# import pandas as pd
# import re

# Create output file with headers
with open('Multidomain_output.txt', 'a') as f_out:
            f_out.write(f"parent_string\tcombined_substring\n")
            
# Read the input file into a DataFrame
input_file = "NotSuspiciousDomains.tsv"  # Replace with your actual file path
df = pd.read_csv(input_file, sep='\t')

# Create a function to process the substrings
def process_substring(sub_string):
    # Remove " protein" (case insensitive) from the end of the substring
    sub_string = re.sub(r' protein$', '', sub_string, flags=re.IGNORECASE).strip()
    return sub_string

# Create a function to handle each parent_string group
def handle_parent_group(group):
    # Check if there are exactly two distinct sub_strings
    if len(group['sub_string'].unique()) != 2:
        # Write the parent_string entries to rejects file
        group.to_csv('rejects.txt', sep='\t', header=True, index=False, mode='a')
    else:
        # Sort by start_pos in ascending order
        group = group.sort_values(by='start_pos')

        # Get the two substrings
        sub_string1 = group.iloc[0]['sub_string']
        sub_string2 = group.iloc[1]['sub_string']

        # Process the substrings
        sub_string1 = process_substring(sub_string1)
        # sub_string2 = process_substring(sub_string2)

        # Combine the substrings
        combined_substring = f"{sub_string1} / {sub_string2}"

        # Write the result to the output file (ignore uppercase)
        with open('Multidomain_output.txt', 'a') as f_out:
            f_out.write(f"{group.iloc[0]['parent_string']}\t{combined_substring}\n")

# Group by parent_string and apply the processing function to each group
# Select the grouping columns explicitly to avoid deprecation warning
grouped = df.groupby('parent_string', as_index=False)

# Apply the function to each group
for name, group in grouped:
    handle_parent_group(group)

print("Multidomain processing completed.")


# OPTION 1 Made by Chat GPT
'''
import pandas as pd
import re

# Read the input file into a DataFrame
input_file = "NotSuspiciousDomains.tsv"  # Replace with your actual file path
df = pd.read_csv(input_file, sep='\t')

# Create a function to process the substrings
def process_substring(sub_string):
    # Remove "protein" (case insensitive) from the end of the substring
    sub_string = re.sub(r'protein$', '', sub_string, flags=re.IGNORECASE).strip()
    return sub_string

# Create a function to handle each parent_string group
def handle_parent_group(group):
    # Check if there are exactly two distinct sub_strings
    if len(group['sub_string'].unique()) != 2:
        # Write the parent_string entries to rejects file
        group.to_csv('rejects.txt', sep='\t', header=True, index=False, mode='a')
    else:
        # Sort by start_pos in ascending order
        group = group.sort_values(by='start_pos')

        # Get the two substrings
        sub_string1 = group.iloc[0]['sub_string']
        sub_string2 = group.iloc[1]['sub_string']

        # Process the substrings
        sub_string1 = process_substring(sub_string1)
        sub_string2 = process_substring(sub_string2)

        # Combine the substrings
        combined_substring = f"{sub_string1} / {sub_string2}"

        # Write the result to the output file
        with open('Multidomain_output.txt', 'a') as f_out:
            f_out.write(f"{group.iloc[0]['parent_string']}\t{combined_substring}\n")

# Group by parent_string and apply the processing function to each group
df.groupby('parent_string').apply(handle_parent_group)

print("Processing complete. Check the 'output.txt' and 'rejects.txt' files.")
'''
#####################################################################


#####################################################################
#
# Next Combine three lists of domain names into one complete list
#
#####################################################################
'''
This was written using the chat GPT prompt:
I have three different tab delimited files. I want to combine the content of all three, but I only need the first two columns. I also want the second column to be in all upper case. write a script in python to do this and output the result in a file.

modify the doce so that it removes all instances of souble space in column 2 and leaves only single spaces
further modify the code so that all instances of under score are replaced by a single space
modify the script taking into account that the files have headers

Program further modified by Dean Rider March 2025
'''

def combine_files(file1, file2, file3, output_file):
    with open(output_file, 'w') as out_file:
        # Flag to indicate if the header has been written
        header_written = False

        # Open the three input files
        for file_path in [file1, file2, file3]:
            with open(file_path, 'r') as in_file:
                # Read the header line
                header = in_file.readline().strip()
                '''
                # Write the header to the output file (only once)
                if not header_written:
                    out_file.write(f"{header}\n")
                    header_written = True
                '''
                # Process each subsequent line in the file
                for line in in_file:
                    # Split the line by tab
                    columns = line.strip().split('\t')
                    
                    # Ensure that there are at least two columns
                    if len(columns) >= 2:
                        # Get the first column
                        first_col = columns[0]
                        
                        # Get the second column, convert to uppercase, remove extra spaces,
                        # and replace underscores with a single space
                        #second_col = ' '.join(columns[1].upper().split()).replace('_', ' ')
                        second_col = ' '.join(columns[1].split()).replace('_', ' ')
                        # Write the first two columns to the output file with a tab delimiter
                        out_file.write(f"{first_col}\t{second_col}\n")


# Example usage:
combine_files('OneDomain.tsv', 'SuspiciousDomains.tsv', 'Multidomain_output.txt', 'Interpro.Named_proteins.txt')
#####################################################################


#####################################################################
#
# Next Clean up any extra spaces before dash or space
#
#####################################################################

# Open the file in read mode and read its contents
with open('Interpro.Named_proteins.txt', 'r') as file:
    content = file.read()

# Remove spaces before dashes and replace double spaces with single spaces and americanize uncharacterised
content = content.replace(' -', '-').replace('  ', ' ').replace('characterised', 'characterized')

# Open the file in write mode and save the modified content
with open('Interpro.Named_proteins.txt', 'w') as file:
    file.write(content)

print("File has been updated.")
#####################################################################


#####################################################################
#
# Next Remove intermediate files
#
#####################################################################

import os

# List of files to delete
files_to_delete = ['OneDomain.tsv', 'SuspiciousDomains.tsv', 'Multidomain_output.txt', 'NotSuspiciousDomains.tsv', 'LongDomains.tsv', 'PrefixSuffix.tsv', 'augustus.json.complete.tsv', 'augustus.json.parts.tsv' ]

# Loop through the list and delete each file
for file in files_to_delete:
    try:
        os.remove(file)
        print(f'{file} has been deleted.')
    except FileNotFoundError:
        print(f'{file} not found, skipping.')
    except Exception as e:
        print(f'Error deleting {file}: {e}')
#####################################################################
print("J'ai fini")


