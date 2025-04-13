'''
find the lines in file BDFB_principal_3.gff3 that contain these sets of items anywhere in the line: 
"Undet"
"JBANDU010000002.1" followed by anything and followed by "1450578" followed by anything and followed by "Leu
"JBANDU010000002.1" followed by anything and followed by "1451609" followed by anything and followed by "Leu
"JBANDU010000002.1" followed by anything and followed by "1567393" followed by anything and followed by "Leu
"JBANDU010000002.1" followed by anything and followed by "1569855" followed by anything and followed by "Leu
"JBANDU010000008.1" followed by anything and followed by "13701794" followed by anything and followed by "Leu
and if the line does have a semicolon on the end, append the line with "pseudo=true;"
or if the line does have a semicolon on the end, append the line with ";pseudo=true;"
or if the line does not contain any of the 6 sets, just output the line unmodified

alternate patterns to search for other than undet may need to be doubled for second exons
    r'JBANDU010000002\.1.*1450578',
    r'JBANDU010000002\.1.*1451609',
    r'JBANDU010000002\.1.*1567393',
    r'JBANDU010000002\.1.*1569855',
    r'JBANDU010000008\.1.*13701794',
'''

import re

# Patterns to search for
patterns = [
    r'JBANDU010000012\.1.*13123988',

]

# Compile for efficiency
compiled_patterns = [re.compile(p) for p in patterns]

input_file = 'BDFB_principal_3.gff3'
output_file = 'BDFB_principal_4.gff3'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.rstrip('\n')

        # Check if the line matches any of the patterns
        if any(p.search(line) for p in compiled_patterns):
            if line.endswith(';'):
                line += 'pseudo=true;'
            # not sure next elif should be ends with new line or just an else or as written
            elif ';' in line:
                line += ';pseudo=true;'
            # If no matches at all, leave the line unmodified
        outfile.write(line + '\n')

