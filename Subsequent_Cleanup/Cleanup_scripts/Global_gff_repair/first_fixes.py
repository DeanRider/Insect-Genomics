'''
Please write a script to replace strings "predicted protein" with "hypothetical protein" and
"ID=JBANDU010000" with "ID=misa_repeat_" in a file and output it to a new file

update the script to check for "product=" in column 9 and if it exists, look for any commas after it. if they exist, replace them with %2C but stop replacements of commas if a semicolon is encountered in the text after "product=" The script still needs to replace strings "predicted protein" with "hypothetical protein" and
"ID=JBANDU010000" with "ID=misa_repeat_"


# Function to replace the strings and output to a new file
def replace_strings(input_file, output_file):
    try:
        # Open the input file in read mode
        with open(input_file, 'r') as file:
            file_content = file.read()
        
        # Replace the specified strings
        file_content = file_content.replace("predicted protein", "hypothetical protein")
        file_content = file_content.replace("ID=JBANDU010000", "ID=misa_repeat_")
        
        # Write the modified content to the output file
        with open(output_file, 'w') as output:
            output.write(file_content)
        
        print(f"Replacement complete. The modified file is saved as {output_file}.")
    
    except FileNotFoundError:
        print(f"The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_filename = "BDFB_principal.gff3"  # Replace with your actual input file path
output_filename = "BDFB_principal_2.gff3"  # Replace with your desired output file path

replace_strings(input_filename, output_filename)

def replace_strings(input_file, output_file):
    try:
        # Open the input file in read mode
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Process each line
        updated_lines = []
        for line in lines:
            # Skip header lines (those starting with '#')
            if line.startswith('#'):
                updated_lines.append(line)
                continue
            
            # Split the line into columns by tab
            columns = line.strip().split('\t')
            
            # Check if there's a "product=" in column 9 (index 8)
            if len(columns) > 8 and "product=" in columns[8]:
                # Find the "product=" part and check for commas after it
                product_part = columns[8]
                product_index = product_part.find("product=")
                
                # Extract the part after "product="
                product_value = product_part[product_index + len("product="):]
                
                # Replace commas with %2C unless a semicolon is encountered
                updated_product_value = []
                comma_replaced = False
                for char in product_value:
                    if char == ',' and not comma_replaced:
                        updated_product_value.append('%2C')
                    elif char == ';':
                        updated_product_value.append(char)
                        comma_replaced = True
                    else:
                        updated_product_value.append(char)
                
                # Rebuild the product string with the modified value
                columns[8] = product_part[:product_index + len("product=")] + ''.join(updated_product_value)

            # Replace "predicted protein" with "hypothetical protein"
            line = line.replace("predicted protein", "hypothetical protein")
            
            # Replace "ID=JBANDU010000" with "ID=misa_repeat_"
            line = line.replace("ID=JBANDU010000", "ID=misa_repeat_")
            
            # Replace "proteases" with "protease"
            line = line.replace("proteases", "protease")
            
            # Reassemble the line with the modified column values
            updated_lines.append("\t".join(columns) + "\n")

        # Write the modified content to the output file
        with open(output_file, 'w') as output:
            output.writelines(updated_lines)

        print(f"Replacement complete. The modified file is saved as {output_file}.")

    except FileNotFoundError:
        print(f"The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_filename = "BDFB_principal.gff3"  # Replace with your actual input file path
output_filename = "BDFB_principal_2.gff3"  # Replace with your desired output file path

replace_strings(input_filename, output_filename)
'''
def replace_strings(input_file, output_file):
    try:
        # Open the input file in read mode
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Process each line
        updated_lines = []
        for line in lines:
            # Skip header lines (those starting with '#')
            if line.startswith('#'):
                updated_lines.append(line)
                continue
            
            # Split the line into columns by tab
            columns = line.strip().split('\t')
            
            # Check if there's a "product=" in column 9 (index 8)
            if len(columns) > 8 and "product=" in columns[8]:
                # Find the "product=" part and check for commas after it
                product_part = columns[8]
                product_index = product_part.find("product=")
                
                # Extract the part after "product="
                product_value = product_part[product_index + len("product="):]
                
                # Replace commas with %2C unless a semicolon is encountered
                updated_product_value = []
                comma_replaced = False
                for char in product_value:
                    if char == ',' and not comma_replaced:
                        updated_product_value.append('%2C')
                    elif char == ';':
                        updated_product_value.append(char)
                        comma_replaced = True
                    else:
                        updated_product_value.append(char)
                
                # Rebuild the product string with the modified value
                columns[8] = product_part[:product_index + len("product=")] + ''.join(updated_product_value)

            # Reassemble the columns back into a line for further replacements
            modified_line = "\t".join(columns)

            # Perform the global replacements on the whole line, including the columns
            modified_line = modified_line.replace("predicted protein", "hypothetical protein")
            # modified_line = modified_line.replace("ID=JBANDU010000", "ID=misa_repeat_")
            modified_line = modified_line.replace("proteases", "protease")
            modified_line = modified_line.replace("%2C other", "-like protein")
            modified_line = modified_line.replace("homeo domain", "homeodomain")
            modified_line = modified_line.replace("apolipophorins", "apolipophorin")
            modified_line = modified_line.replace(" and related kinases", "")
            modified_line = modified_line.replace(" synthesizing storage lipids", "")
            modified_line = modified_line.replace(" and related proteins", "")
            modified_line = modified_line.replace(" homolog", "")
            modified_line = modified_line.replace(" gene family,", " protein family")
            modified_line = modified_line.replace("Uncharacterized protein C3orf38 (DUF4518) protein", "putative C3orf38 (DUF4518) protein")
            modified_line = modified_line.replace("Uncharacterized protein KIAA1143-like protein", "KIAA1143-like protein")
            modified_line = modified_line.replace("Uncharacterized protein family%2C CD034/YQF4 protein", "CD034/YQF4 family protein")
            modified_line = modified_line.replace("%2C partial", "-like")
            modified_line = modified_line.replace("Myosin S1 fragment", "Myosin S1")
            modified_line = modified_line.replace(" ortholog", "")
            modified_line = modified_line.replace("Reverse transcriptase/retrotransposon-derived protein%2C RNase H-like domain", "putative retrotransposon-derived protein")
            modified_line = modified_line.replace("P-loop containing nucleoside triphosphate hydrolase", "P-loop containing NTPase")
            modified_line = modified_line.replace("ribosomal RNA (partial)","ribosomal RNA")
            modified_line = modified_line.replace("fatty acid synthase%2C animal type","fatty acid synthase")
            modified_line = modified_line.replace("probable","putative")
            modified_line = modified_line.replace("Haemolymph","hemolymph")
            modified_line = modified_line.replace("protein protein","protein")
            # these are names specifically having lots of numbers in them, often fly, fish, or mosquito homologs that carried from other uncorrected beetle refseq names
            modified_line = modified_line.replace("E3 ubiquitin-protein ligase RNF216", "E3 ubiquitin-protein ligase")
            modified_line = modified_line.replace("proton-coupled amino acid transporter-like protein CG1139", "proton-coupled amino acid transporter-like protein")
            modified_line = modified_line.replace("proton-coupled amino acid transporter-like protein CG1139 isoform X1", "proton-coupled amino acid transporter-like protein isoform X1")
            modified_line = modified_line.replace("putative cytochrome P450 303a1 isoform X2", "putative cytochrome P450 303a1 isoform X2")
            modified_line = modified_line.replace("putative G-protein coupled receptor B0563.6", "putative G-protein coupled receptor")
            modified_line = modified_line.replace("transmembrane protein 184B isoform X1", "transmembrane protein 184B isoform X1")
            modified_line = modified_line.replace("ribosome biogenesis protein C1orf109", "ribosome biogenesis protein")
            modified_line = modified_line.replace("transmembrane protein 179", "transmembrane protein 179")
            modified_line = modified_line.replace("TM2 domain-containing protein CG10795", "TM2 domain-containing protein")
            modified_line = modified_line.replace("very long chain fatty acid elongase AAEL008004-like", "very long chain fatty acid elongase")
            modified_line = modified_line.replace("PHAF1 protein CG7083 isoform X2", "PHAF1 protein isoform X2")
            modified_line = modified_line.replace("zinc finger protein TC009515", "zinc finger protein")
            modified_line = modified_line.replace("zinc finger protein TC009514", "zinc finger protein")
            modified_line = modified_line.replace("protein FAM161A", "protein FAM161A-like")
            modified_line = modified_line.replace("centrosomal protein of 104 kDa", "centrosomal protein")
            modified_line = modified_line.replace("kxDL motif-containing protein CG10681", "kxDL motif-containing protein")
            modified_line = modified_line.replace("putative gamma-glutamylcyclotransferase CG2811 isoform X2", "putative gamma-glutamylcyclotransferase isoform X2")
            modified_line = modified_line.replace("putative gamma-glutamylcyclotransferase CG2811 isoform X1", "putative gamma-glutamylcyclotransferase isoform X1")
            modified_line = modified_line.replace("protein FAM136A", "protein FAM136A-like")
            modified_line = modified_line.replace("putative Rho GTPase-activating protein CG5521 isoform X1", "putative Rho GTPase-activating protein isoform X1")
            modified_line = modified_line.replace("putative leucine-rich repeat-containing protein DDB_G0290503 isoform X1", "putative leucine-rich repeat-containing protein isoform X1")
            modified_line = modified_line.replace("asparagine synthetase domain-containing protein CG17486 isoform X1", "asparagine synthetase domain-containing protein isoform X1")
            modified_line = modified_line.replace("UPF0669 protein v1g209471", "UPF0669 protein")
            modified_line = modified_line.replace("putative leucine-rich repeat-containing protein DDB_G0290503 isoform X6", "putative leucine-rich repeat-containing protein isoform X6")
            modified_line = modified_line.replace("116 kDa U5 small nuclear ribonucleoprotein component", "U5 small nuclear ribonucleoprotein subunit")
            modified_line = modified_line.replace("transmembrane protein 145 isoform X1", "transmembrane protein 145 isoform X1")
            modified_line = modified_line.replace("WSCD family member AGAP003962", "WSCD family member protein")
            modified_line = modified_line.replace("PP2C-like domain-containing protein CG9801 isoform X2", "PP2C-like domain-containing protein isoform X2")
            modified_line = modified_line.replace("putative fatty acyl-CoA reductase CG8306", "putative fatty acyl-CoA reductase")
            modified_line = modified_line.replace("putative fatty acyl-CoA reductase CG5065", "putative fatty acyl-CoA reductase")
            modified_line = modified_line.replace("band 7 protein AGAP004871-like", "band 7-like protein")
            modified_line = modified_line.replace("putative fatty acyl-CoA reductase CG5065", "putative fatty acyl-CoA reductase")
            modified_line = modified_line.replace("very long chain fatty acid elongase AAEL008004-like", "very long chain fatty acid elongase")
            modified_line = modified_line.replace("putative ankyrin repeat protein RF_0381", "putative ankyrin repeat protein")
            modified_line = modified_line.replace("putative fatty acyl-CoA reductase CG5065", "putative fatty acyl-CoA reductase")
            modified_line = modified_line.replace("putative ankyrin repeat protein RF_0381 isoform X2", "putative ankyrin repeat protein isoform X2")
            modified_line = modified_line.replace("centriolar coiled-coil protein of 110 kDa", "centriolar coiled-coil protein")
            modified_line = modified_line.replace("Centrosome-associated protein 350 protein", "Centrosome-associated protein 350")
            modified_line = modified_line.replace("cold shock domain-containing protein CG9705", "cold shock domain-containing protein")
            modified_line = modified_line.replace("putative fatty acyl-CoA reductase CG5065", "putative fatty acyl-CoA reductase")
            modified_line = modified_line.replace("WD repeat-containing protein CG11141 isoform X2", "WD repeat-containing protein isoform X2")
            modified_line = modified_line.replace("putative G-protein coupled receptor B0563.6", "putative G-protein coupled receptor")
            modified_line = modified_line.replace("endoribonuclease CG2145", "endoribonuclease")
            modified_line = modified_line.replace("NKAP family protein CG6066", "NKAP family protein")
            modified_line = modified_line.replace("rhodanese domain-containing protein CG4456", "rhodanese domain-containing protein")
            modified_line = modified_line.replace("serine/threonine-protein kinase GL21140", "serine/threonine-protein kinase")
            modified_line = modified_line.replace("putative ATP-dependent RNA helicase CG8611", "putative ATP-dependent RNA helicase")
            modified_line = modified_line.replace("bolA-like protein DDB_G0274169", "bolA-like protein")
            modified_line = modified_line.replace("CIMIP2 protein CG18335-like", "Ciliary Microtubule Inner Protein 2-like")
            modified_line = modified_line.replace("putative leucine-rich repeat-containing protein DDB_G0290503 isoform X2", "putative leucine-rich repeat-containing protein isoform X2")
            modified_line = modified_line.replace("collagen alpha chain CG42342 isoform X1", "collagen alpha chain isoform X1")
            modified_line = modified_line.replace("dynamin-like 120 kDa protein, mitochondrial isoform X1", "dynamin-like protein, mitochondrial isoform X1")
            modified_line = modified_line.replace("ubiquitin-conjugating enzyme E2Q-like protein CG4502", "ubiquitin-conjugating enzyme E2Q-like protein")
            modified_line = modified_line.replace("MPN domain-containing protein CG4751-like isoform X1", "MPN domain-containing protein isoform X1")
            modified_line = modified_line.replace("UPF0598 protein CG30010", "UPF0598 protein")
            modified_line = modified_line.replace("UPF0430 protein CG31712", "UPF0430 protein")
            modified_line = modified_line.replace("thioredoxin reductase-like selenoprotein T CG3887", "thioredoxin reductase-like selenoprotein T")
            modified_line = modified_line.replace("PITH domain-containing protein GA19395", "PITH domain-containing protein")
            modified_line = modified_line.replace("coiled-coil domain-containing protein AGAP005037 isoform X6", "coiled-coil domain-containing protein isoform X6")
            modified_line = modified_line.replace("UPF0184 protein AAEL002161", "UPF0184 protein")
            modified_line = modified_line.replace("protein fem-1 CG6966 isoform X1", "protein fem-1 isoform X1")
            modified_line = modified_line.replace("CG13597-like amine receptor", "amine receptor-like protein")
            modified_line = modified_line.replace("TM2 domain-containing protein CG11103", "TM2 domain-containing protein")
            modified_line = modified_line.replace("U5 small nuclear ribonucleoprotein 200 kDa helicase", "U5 small nuclear ribonucleoprotein helicase")
            modified_line = modified_line.replace("V-type ATPase, V0 complex, 116kDa subunit family protein", "V-type ATPase, V0 complex subunit family protein")
            modified_line = modified_line.replace("V-type proton ATPase 116 kDa subunit a 1 isoform X1", "V-type proton ATPase subunit a 1 isoform X1")
            modified_line = modified_line.replace("V-type proton ATPase 116 kDa subunit a 1 isoform X4", "V-type proton ATPase subunit a 1 isoform X4")
            modified_line = modified_line.replace("centrosomal protein of 290 kDa isoform X2", "centrosomal protein isoform X2")
            modified_line = modified_line.replace("V-type proton ATPase 116 kDa subunit a 1-like", "V-type proton ATPase subunit a 1-like")
            modified_line = modified_line.replace("FHIP family protein AGAP011705", "FHIP family protein")
            modified_line = modified_line.replace("UPF0430 protein CG31712-like isoform X2", "UPF0430 protein-like isoform X2")
            modified_line = modified_line.replace("very long chain fatty acid elongase AAEL008004-like", "very long chain fatty acid elongase-like")
            modified_line = modified_line.replace("very long chain fatty acid elongase AAEL008004-like isoform X1", "very long chain fatty acid elongase-like isoform X1")
            modified_line = modified_line.replace("very long chain fatty acid elongase AAEL008004", "very long chain fatty acid elongase")
            modified_line = modified_line.replace("very long chain fatty acid elongase AAEL008004 isoform X2", "very long chain fatty acid elongase isoform X2")
            modified_line = modified_line.replace("very long chain fatty acid elongase AAEL008004", "very long chain fatty acid elongase")
            modified_line = modified_line.replace("very long chain fatty acid elongase AAEL008004 isoform X2", "very long chain fatty acid elongase isoform X2")
            modified_line = modified_line.replace("putative cytosolic Fe-S cluster assembly factor CPIJ010948", "putative cytosolic Fe-S cluster assembly factor")
            modified_line = modified_line.replace("putative sodium/potassium/calcium exchanger CG1090 isoform X1", "putative sodium/potassium/calcium exchanger isoform X1")
            modified_line = modified_line.replace("muscle-specific protein 300 kDa isoform X1", "muscle-specific protein isoform X1")
            modified_line = modified_line.replace("kinesin-like protein CG14535 isoform X2", "kinesin-like protein isoform X2")
            modified_line = modified_line.replace("centrosomal protein of 164 kDa isoform X1", "centrosomal protein")
            modified_line = modified_line.replace("glutaredoxin domain-containing cysteine-rich protein CG12206-like", "glutaredoxin domain-containing cysteine-rich protein")
            modified_line = modified_line.replace("troponin C, isoallergen Bla g 6.0101", "troponin C, isoallergen Bla g 6.0101-like")
            modified_line = modified_line.replace("echinoderm microtubule-associated protein-like CG42247 isoform X2", "echinoderm microtubule-associated protein-like isoform X2")
            modified_line = modified_line.replace("205 kDa microtubule-associated protein", "microtubule-associated protein")
            modified_line = modified_line.replace("putative ankyrin repeat protein RF_0381", "putative ankyrin repeat protein")
            modified_line = modified_line.replace("NECAP-like protein CG9132", "NECAP-like protein")
            modified_line = modified_line.replace("centrosomal protein of 164 kDa isoform X1", "centrosomal protein")
            modified_line = modified_line.replace("kinase D-interacting substrate of 220 kDa B isoform X2", "kinase D-interacting substrate")
            modified_line = modified_line.replace("putative leucine-rich repeat-containing protein DDB_G0290503 isoform X2", "putative leucine-rich repeat-containing protein isoform X2")
            modified_line = modified_line.replace("zinc finger matrin-type protein CG9776 isoform X1", "zinc finger matrin-type protein isoform X1")
            modified_line = modified_line.replace("UPF0587 protein CG4646", "UPF0587 protein")
            modified_line = modified_line.replace("proton-coupled amino acid transporter-like protein CG1139", "proton-coupled amino acid transporter-like protein")
            modified_line = modified_line.replace("centrosomal protein of 135 kDa isoform X1", "centrosomal protein")
            modified_line = modified_line.replace("esterase AGAP003155 isoform X2", "esterase isoform X2")
            modified_line = modified_line.replace("dyslexia-associated protein KIAA0319-like protein", "dyslexia-associated-like protein")
            modified_line = modified_line.replace("heat shock protein TC005094", "heat shock protein")
            modified_line = modified_line.replace("centrosomal protein of 290 kDa-like isoform X1", "centrosomal protein")
            modified_line = modified_line.replace("centrosomal protein of 131 kDa", "centrosomal protein")
            modified_line = modified_line.replace("extracellular serine/threonine protein CG31145 isoform X2", "extracellular serine/threonine protein  isoform X2")
            modified_line = modified_line.replace("protein CFAP276", "Cilia And Flagella Associated Protein 276")
            modified_line = modified_line.replace("putative G-protein coupled receptor CG31760 isoform X1", "putative G-protein coupled receptor")
            modified_line = modified_line.replace("putative leucine-rich repeat-containing protein DDB_G0290503 isoform X1", "putative leucine-rich repeat-containing protein isoform X1")
            modified_line = modified_line.replace("putative leucine-rich repeat-containing protein DDB_G0290503 isoform X6", "putative leucine-rich repeat-containing protein isoform X6")
            modified_line = modified_line.replace("putative ankyrin repeat protein RF_0381", "putative ankyrin repeat protein")
            modified_line = modified_line.replace("putative ankyrin repeat protein RF_0381 isoform X2", "putative ankyrin repeat protein isoform X2")
            modified_line = modified_line.replace("bolA-like protein DDB_G0274169", "bolA-like protein")
            modified_line = modified_line.replace("somatostatin-like receptor F_48D10.1", "somatostatin-like receptor")
            modified_line = modified_line.replace("putative leucine-rich repeat-containing protein DDB_G0290503 isoform X2", "putative leucine-rich repeat-containing protein isoform X2")
            modified_line = modified_line.replace("putative ankyrin repeat protein RF_0381", "putative ankyrin repeat protein")
            modified_line = modified_line.replace("putative leucine-rich repeat-containing protein DDB_G0290503 isoform X2", "putative leucine-rich repeat-containing protein isoform X2")
            modified_line = modified_line.replace("TAF5-like RNA polymerase II p300/CBP-associated factor-associated factor 65 kDa subunit 5L", "TAF5-like RNA polymerase II p300/CBP-associated factor subunit 5L")
            modified_line = modified_line.replace("dynamin-like 120 kDa protein, mitochondrial isoform X1","dynamin-like protein, mitochondrial isoform X1")
            modified_line = modified_line.replace("centrosomal protein of 120 kDa","centrosomal protein")
            modified_line = modified_line.replace("dynamin-like 120 kDa protein, mitochondrial isoform X1","dynamin-like protein, mitochondrial isoform X1")
            modified_line = modified_line.replace("V-type ATPase, V0 complex, 116kDa subunit family protein","V-type ATPase subunit, V0 complex family protein")
            modified_line = modified_line.replace("centrosomal protein of 162 kDa isoform X1","centrosomal protein isoform X1")
                        
            # Append the modified line to updated_lines
            updated_lines.append(modified_line + "\n")

        # Write the modified content to the output file
        with open(output_file, 'w') as output:
            output.writelines(updated_lines)

        print(f"Replacement complete. The modified file is saved as {output_file}.")

    except FileNotFoundError:
        print(f"The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_filename = "BDFB_principal_1.gff3"  # Replace with your actual input file path
output_filename = "BDFB_principal_2.gff3"  # Replace with your desired output file path

replace_strings(input_filename, output_filename)


