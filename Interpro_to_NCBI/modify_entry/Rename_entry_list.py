#########################################################################
#
# THIS SCRIPT CONVERTS THE INTERPRO DESIGNATIONS INTO NCBI COMPATIBLE
# PROTEIN NAMES AND USES THE InterPro entry.list FROM APRIL 2025 
# THE ORIGINAL DISCREPANCY REPORT IS AFTER THE STEP FOR:
# Initial conversion of InterPro domain names into protein names
# A GFF3, FASTA and TEMPLATE ARE AVAILABLE TO TEST WITH TABLE2ASN
# AN INTERPRO TO NCBI LIST IS ALSO AVAILABLE WITH THE CONVERSIONS
#
#########################################################################
'''
Discrepancy Report Results from initial round of testing Interpro_to_NCBI_step_1 names

Summary
COUNT_NUCLEOTIDES: 1 nucleotide Bioseq is present
SOURCE_QUALS: taxname (all present, all unique)
FEATURE_COUNT: CDS: 44166 present
FEATURE_COUNT: gene: 44166 present
FEATURE_COUNT: mRNA: 44166 present
SUSPECT_PRODUCT_NAMES: 1596 product_names contain suspect phrases or characters
	Putative Typo
		282 features start with 'uncharacterized protein'
		13 features start with 'conserved protein'
		74 features May contain plural
		89 features starts with 'gp'. May contain systematic gene product identifiers from phage
		1 feature starts with 'hypothetical protein'
		1 feature contain 'other'. Does the product name include a descriptive phrase?
	Possible parsing error or incorrect formatting; remove inappropriate symbols
		FATAL: 1 feature starts with 'with'
		FATAL: 1 feature starts with ','
		FATAL: 1 feature starts with '-'
		FATAL: 3 features contain unbalanced brackets or parentheses
		FATAL: 5 features contain '. '
		FATAL: 2 features contain 'genome'
	Suspicious phrase; should this be nonfunctional?
		5 features contain 'unknown'
		4 features contain 'frame'
		2 features contain 'frameshift'
		2 features contain 'interrupt'
		FATAL: 3 features contain 'open reading frame'
		2 features contain 'orphan protein'
		FATAL: 2 features contain 'partial'
	May contain database identifier more appropriate in note; remove from product name
		655 features contains three or more numbers together that may be identifiers more appropriate in note
		123 features contain underscore
		2 features contain 'COG'
		1 feature contain 'et al'. Is this a publication reference instead of a protein name?
		1 feature contains 'FOG'
	Implies evolutionary relationship; change to -like protein
		74 features contain 'Homolog'
		49 features contain 'Homologue'
		3 features contain 'ortholog'
		3 features contain 'orthologue'
		1 feature contains 'paralog'
		3 features contain 'paralogue'
	Use short product name instead of descriptive phrase
		208 features Is longer than 100 characters. Remove descriptive phrases or synonyms from product names. Keep valid long product names, eg long enzyme names
		3 features contain 'novel'
		7 features contain 'residue'
	use protein instead of gene as appropriate
		67 features contain 'gene'
		5 features contain 'genes'
###################################################################

read an input file called entry.list.txt

if column 2 endswith "site" or "PTM"
check if column 3 ends with "site"
if it does, create new column 4 with the content of column 3 appended with "-containing protein"
else create new column 4 with the content of column 3 appended with " site-containing protein"

if column 2 contains "Domain"
check if column 3 ends with "Domain"
if it does, create new column 4 with the content of column 3 appended with "-containing protein"
else create new column 4 with the content of column 3 appended with " domain-containing protein"

if column 2 contains "Family"
check if column 3 ends with "Family"
if it does, create new column 4 with the content of column 3 appended with " protein"
else create new column 4 with the content of column 3 appended with " family protein"

if column 2 contains "superfamily"
check if column 3 ends with "site"
if it does, create new column 4 with the content of column 3 appended with " protein"
else create new column 4 with the content of column 3 appended with " superfamily protein"

if column 2 contains "Repeat"
check if column 3 ends with "Repeat"
if it does, create new column 4 with the content of column 3 appended with "-containing protein"
else create new column 4 with the content of column 3 appended with " repeat-containing protein"

for each condition, print resulting columns 1-4 to a file called "Interpro_to_NCBI.txt"

'''
####################################
#
# Initial conversion of InterPro domain names into protein names
#
####################################

# Read input and process it
input_file = "entry.list.txt"
output_file = "Interpro_to_NCBI_step_1.txt"

# using .lower() turns text into lowercase so we can ignore case when looking and avoid trying many variants
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        cols = line.split('\t')
        if len(cols) < 3:
            continue  # skip malformed lines

        col1, col2, col3 = cols[0], cols[1], cols[2]
        col4 = ""

        if col2.endswith("site") or col2.endswith("PTM"):
            if col3.lower().endswith("site"):
                col4 = f"{col3}-containing protein"
            else:
                col4 = f"{col3} site-containing protein"

        elif "Domain" in col2:
            if col3.lower().endswith("Domain"):
                col4 = f"{col3}-containing protein"
            else:
                col4 = f"{col3} domain-containing protein"

        elif "Family" in col2:
            if col3.lower().endswith("Family"):
                col4 = f"{col3} protein"
            else:
                col4 = f"{col3} family protein"

        elif "superfamily" in col2:
            if col3.lower().endswith("superfamily"):
                col4 = f"{col3} protein"
            elif col3.lower().endswith("protein"):
                col4 = f"{col3}"
            else:
                col4 = f"{col3} superfamily protein"

        elif "Repeat" in col2:
            if col3.lower().endswith("Repeat"):
                col4 = f"{col3}-containing protein"
            else:
                col4 = f"{col3} repeat-containing protein"

        if col4:
            outfile.write(f"{col1}\t{col2}\t{col3}\t{col4}\n")

# Initial conversion to proteins is done
print("Initial conversion to proteins is done")

####################################
#
# Handling some changes to American English conventions
# and then
# Handling "starts with" discrepancies under Putative Typo and Possible parsing error
#
#  SUSPECT_PRODUCT_NAMES: 282 features start with 'uncharacterized protein'
#  SUSPECT_PRODUCT_NAMES: 13 features start with 'conserved protein'
#  SUSPECT_PRODUCT_NAMES: 89 features starts with 'gp'. May contain systematic gene product identifiers from phage
#      IGNORE GPCR AND GP because spelling out g-protein coupled receptor and glycoprotein makes long names
#  SUSPECT_PRODUCT_NAMES: 11 features start with 'hypothetical protein'
#  FATAL: SUSPECT_PRODUCT_NAMES: 1 feature starts with 'with'
#  FATAL: SUSPECT_PRODUCT_NAMES: 1 feature starts with ','
#  FATAL: SUSPECT_PRODUCT_NAMES: 1 feature starts with '-'
#
# And then a few NCBI-specific name changes
#
####################################
'''
("Uncharacterized protein family, ", "")
("Uncharacterized protein family ", "")
("Uncharacterized protein, ", "")
("Uncharacterized protein ", "")
("putative conserved protein with", "putative ")
("putative conserved protein ", "putative ")
("putative conserved protein, ", "putative ")
("Hypothetical protein ","")
("With No Lysine (K) ","WNK (with no lysine) ")
("Putative, 10TM","Putative 10TM")
("-alpha-acetyltransferase 35","alpha-acetyltransferase 35")
'''

# Read input and process it
input_file = "Interpro_to_NCBI_step_1.txt"
output_file = "Interpro_to_NCBI_step_2.txt"

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        cols = line.split('\t')
        if len(cols) < 4:
            continue  # skip malformed lines

        col1, col2, col3, col4 = cols[0], cols[1], cols[2], cols[3]

        # test problem conditions and make replacements
        if "characteris" in col4:
            col4 = col4.replace("characteris", "characteriz")

        if "imeris" in col4:
            col4 = col4.replace("imeris", "imeriz")

        if "Haem-" in col4:
            col4 = col4.replace("Haem-", "Heme-")

        if "haem-" in col4:
            col4 = col4.replace("haem-", "heme-")

        if "Haem" in col4:
            col4 = col4.replace("Haem", "Hem")

        if "haem" in col4:
            col4 = col4.replace("haem", "hem")

        if "ulph" in col4:
            col4 = col4.replace("ulph", "ulf")

        if "dases heam-" in col4:
            col4 = col4.replace("dases heam-", "dase heme-")

        if "dimerisation" in col4:
            col4 = col4.replace("dimerisation","dimerization")

        if "fibre" in col4:
            col4 = col4.replace("fibre","fiber")

        if "hydrolysing" in col4:
            col4 = col4.replace("hydrolysing","hydrolyzing")

        if "localisation" in col4:
            col4 = col4.replace("localisation","localization")

        if "novel" in col4:
            col4 = col4.replace("novel","putative")

        if "organisation" in col4:
            col4 = col4.replace("organisation","organization")

        if "probable" in col4:
            col4 = col4.replace("probable","putative")

        if "repeats" in col4:
            col4 = col4.replace("repeats","repeat")

        if "signalling" in col4:
            col4 = col4.replace("signalling","signaling")

        if "tumour" in col4 or "Tumour" in col4:
            col4 = col4.replace("umour","umor")

        if "Anaemia" in col4:
            col4 = col4.replace("Anaemia","anemia")
        if "anaemia" in col4:
            col4 = col4.replace("anaemia","anemia")
        if "oligomerisation" in col4:
            col4 = col4.replace("oligomerisation","oligomerization")
        if "tetramerisation" in col4:
            col4 = col4.replace("tetramerisation","tetramerization")
        if "localisation" in col4:
            col4 = col4.replace("localisation","localization")
        if "Thiamin/thiamin " in col4:
            col4 = col4.replace("Thiamin/thiamin ","Thiamine/thiamine ")
        if "Thiamin " in col4 or "Thiamin/" in col4:
            col4 = col4.replace("Thiamin","Thiamine")
        if "thiaminee/thiamine " in col4:
            col4 = col4.replace("thiaminee","thiamine")
        if "thiamin " in col4 or "Thiamine/thiamin " in col4:
            col4 = col4.replace("thiamin ","thiamine ")
        if "utilisation" in col4:
            col4 = col4.replace("utilisation","utilization")
        if "unkown" in col4:
            col4 = col4.replace("unkown","unknown")
        if "stabilisation" in col4:
            col4 = col4.replace("stabilisation","stabilization")
        if "tumour-associated" in col4:
            col4 = col4.replace("tumour-associated","tumor-associated")
        if "GTP-utilising" in col4:
            col4 = col4.replace("GTP-utilising","GTP-utilizing")
        if "heptamerisation" in col4:
            col4 = col4.replace("heptamerisation","heptamerization")
        if "heteromerisation" in col4:
            col4 = col4.replace("heteromerisation","heteromerization")
        if "mobilisation" in col4:
            col4 = col4.replace("mobilisation","mobilization")
        if "octamerisation" in col4:
            col4 = col4.replace("octamerisation","octamerization")
        if "organiser" in col4:
            col4 = col4.replace("organiser","organizer")
        if "tetramerisation-type" in col4:
            col4 = col4.replace("tetramerisation-type","tetramerization-type")
        if "Domain of unknown function" in col4:
            col4 = col4.replace("Domain of unknown function","unknown function")
        if "domain of unknown function" in col4:
            col4 = col4.replace("domain of ","")
        if "Domain of Unknown Function" in col4:
            col4 = col4.replace("Domain of Unknown Function","unknown function")
        if "depolymerising" in col4:
            col4 = col4.replace("depolymerising","depolymerizing")
        if "utilising" in col4:
            col4 = col4.replace("utilising","utilizing")
        if "Mobilisation" in col4:
            col4 = col4.replace("Mobilisation","Mobilization")
        if "cyclisation" in col4:
            col4 = col4.replace("cyclisation","cyclization")
        if "PEP-utilising" in col4:
            col4 = col4.replace("PEP-utilising","PEP-utilizing")
        if "canalisation" in col4:
            col4 = col4.replace("canalisation","canalization")
        if "oxidoreducase" in col4:
            col4 = col4.replace("oxidoreducase","oxidoreductase")
        if "glycosyltranferase" in col4:
            col4 = col4.replace("glycosyltranferase","glycosyltransferase")
        if "Lipoxigenase" in col4:
            col4 = col4.replace("Lipoxigenase","Lipoxygenase")
        if "monoxygenase" in col4:
            col4 = col4.replace("monoxygenase","monooxygenase")



        if col4.startswith("Uncharacterized protein with "):
            col4 = col4.replace("Uncharacterized protein with ","")

        if "Uncharacterized protein family, " in col4:
            col4 = col4.replace("Uncharacterized protein family, ", "")

        if "Uncharacterized protein family " in col4:
            col4 = col4.replace("Uncharacterized protein family ", "")

        if "Uncharacterized protein, " in col4:
            col4 = col4.replace("Uncharacterized protein, ", "")

        if "Uncharacterized protein " in col4:
            col4 = col4.replace("Uncharacterized protein ", "")

        if "putative conserved protein with" in col4:
            col4 = col4.replace("putative conserved protein with", "putative ")

        if "putative conserved protein " in col4:
            col4 = col4.replace("putative conserved protein ", "putative ")

        if "putative conserved protein, " in col4:
            col4 = col4.replace("putative conserved protein, ", "putative ")

        if "Uncharacterized conserved protein " in col4:
            col4 = col4.replace("Uncharacterized conserved protein ", "")

        if col4.lower().startswith("hypothetical protein "):
            col4 = col4.replace("Hypothetical protein ","")

        if col4.startswith("With No Lysine (K) "):
            col4 = col4.replace("With No Lysine (K) ","WNK (with no lysine) ")

        if col4.startswith("Putative, 10TM"):
            col4 = col4.replace("Putative, 10TM","Putative 10TM")

        if col4.startswith("-alpha-acetyltransferase 35"):
            col4 = col4.replace("-alpha-acetyltransferase 35","alpha-acetyltransferase 35")



        if "Probable" in col4:
            col4 = col4.replace("Probable","putative")
        if "Predicted" in col4:
            col4 = col4.replace("Predicted","putative")
        if "Uncharacterized" in col4:
            col4 = col4.replace("Uncharacterized","putative")
        if "Novel" in col4:
            col4 = col4.replace("Novel","putative")
        if "Hypothetical" in col4:
            col4 = col4.replace("Hypothetical","putative")
        if "Potential" in col4:
            col4 = col4.replace("Potential","putative")
        if col4.startswith("Unique"):
            col4 = col4.replace("Unique","putative")


        if "domain domain" in col4:
            col4 = col4.replace("domain domain","domain")
        if "protein protein" in col4:
            col4 = col4.replace("protein protein","protein")
        if "family family" in col4:
            col4 = col4.replace("family family","family")
        if "Family family" in col4:
            col4 = col4.replace("Family family","family")
        if "superfamily family" in col4:
            col4 = col4.replace("superfamily family","superfamily")
        if ", fungi family" in col4:
            col4 = col4.replace(", fungi family"," family")
        if "domain, fungi domain" in col4:
            col4 = col4.replace("domain, fungi domain","domain")
        if ", fungi domain" in col4:
            col4 = col4.replace(", fungi domain"," domain")
        if "repeat repeat" in col4:
            col4 = col4.replace("repeat repeat","repeat")

        # print line to file
        outfile.write(f"{col1}\t{col2}\t{col3}\t{col4}\n")

print("Words are now Americanized for NCBI")

####################################
#
# Handling "plural" and "other" discrepancies under Putative Typo
#
#  SUSPECT_PRODUCT_NAMES: 74 features May contain plural
#  SUSPECT_PRODUCT_NAMES: 1 feature contain 'other'.
#
# Also finish off Parsing errors
#  FATAL: 3 features contain unbalanced brackets or parentheses
#  FATAL: 5 features contain '. '
#  FATAL: 2 features contain 'genome'
#
####################################
'''
('ases", "ase")
("systems", "system")
("transporters", "trasporter")
("cyclins", "cyclin")
("metalloenzymes, ", "metalloenzyme, ")
("lectins", "lectin")
("vertebrates", "vertebrate")
("proteins", "protein")
("factors", "factor")
("reductas, ", "reductase,")
("receptors", "receptor")
("subdomains", "subdomain")
("channels", "channel")
("regulators", "regulator")
'''
# Read input and process it
input_file = "Interpro_to_NCBI_step_2.txt"
output_file = "Interpro_to_NCBI_step_3.txt"

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        cols = line.split('\t')
        if len(cols) < 4:
            continue  # skip malformed lines

        col1, col2, col3, col4 = cols[0], cols[1], cols[2], cols[3]

        # test problem conditions and make replacements
        if "ases" in col4.lower():
            col4 = col4.replace("ases", "ase")

        if "systems" in col4.lower():
            col4 = col4.replace("systems", "system")

        if "transporters" in col4.lower():
            col4 = col4.replace("transporters", "transporter")

        if "Cyclins" in col4:
            col4 = col4.replace("Cyclins", "cyclin")

        if "metalloenzymes" in col4.lower():
            col4 = col4.replace("metalloenzymes", "metalloenzyme")

        if "lectins" in col4.lower():
            col4 = col4.replace("lectins", "lectin")

        if "vertebrates" in col4.lower():
            col4 = col4.replace("vertebrates", "vertebrate")

        if "proteins" in col4.lower():
            col4 = col4.replace("proteins", "protein")

        if "factors" in col4.lower():
            col4 = col4.replace("factors", "factor")

        if "reductas, " in col4.lower():
            col4 = col4.replace("reductas, ", "reductase, ")

        if "receptors" in col4.lower():
            col4 = col4.replace("receptors", "receptor")

        if "subdomains" in col4.lower():
            col4 = col4.replace("subdomains", "subdomain")

        if "channels" in col4.lower():
            col4 = col4.replace("channels", "channel")

        if "regulators" in col4.lower():
            col4 = col4.replace("regulators", "regulator")

        #  SUSPECT_PRODUCT_NAMES: 1 feature contain 'other'

        if "aspartate/other" in col4.lower():
            col4 = col4.replace("Aspartate/other", "Aspartate")

        #  FATAL: 3 features contain unbalanced brackets or parentheses #########################
        # Need more specific fixes as these produce an additional 127 more problems with braces
        # if ") family protein" in col4.lower():
        #     col4 = col4.replace(")", "")

        # if "unknown function (" in col4.lower():
        #     col4 = col4.replace("(", "")				#############################

        #  FATAL: 5 features contain '. '

        if ", s. mansonii-type" in col4.lower():
            col4 = col4.replace(", S. mansonii-type", "")

        if ", neisseria sp. " in col4.lower():
            col4 = col4.replace(", Neisseria sp.", "")

        if "DUF3566. " in col4.lower():
            col4 = col4.replace("DUF3566. ", "DUF3566 ") 

        if "like. bbp2" in col4.lower():
            col4 = col4.replace("like. bbp2", "like bbp2") 

        if "factor. bacterial" in col4.lower():
            col4 = col4.replace("factor. bacterial", "factor") 

        #  FATAL: 2 features contain 'genome'

        if "Genome polyprotein, Flavivirus " in col4:
            col4 = col4.replace("Genome polyprotein, Flavivirus ", "Flavivirus polyprotein ")

        if "Petuviruses Genome Polyprotein" in col4:
            col4 = col4.replace(" Genome", "") 

        if "Arabinosyltransferas" in col4:
            col4 = col4.replace("Arabinosyltransferas", "Arabinosyltransferase")

        if ", Firmicutes, long form, predicted " in col4:
            col4 = col4.replace(", Firmicutes, long form, predicted", "")

        # print line to file
        outfile.write(f"{col1}\t{col2}\t{col3}\t{col4}\n")

# All Putative Typo and Possible parsing error issues are resolved
print("All Putative Typo and Possible parsing error issues are resolved")


####################################
#
# Handling Suspicious phrase; should this be nonfunctional?
#
####################################
# Read input and process it
input_file = "Interpro_to_NCBI_step_3.txt"
output_file = "Interpro_to_NCBI_step_4.txt"

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        cols = line.split('\t')
        if len(cols) < 4:
            continue  # skip malformed lines

        col1, col2, col3, col4 = cols[0], cols[1], cols[2], cols[3]

        # test problem conditions and make replacements
        # SUSPECT_PRODUCT_NAMES: 5 features contain 'unknown'

        if "Protein with unknown function UPF0154 family protein" in col4:
            col4 = col4.replace("Protein with unknown function UPF0154 family protein", "protein of unknown function UPF0154 domain-containing protein")
        
        if "heam-ligand" in col4:
            col4 = col4.replace("heam-ligand", "heme-ligand")

        if "Cysteine desulfurase-related, unknown function family protein" in col4:
            col4 = col4.replace("Cysteine desulfurase-related, unknown function family protein", "Cysteine desulfurase-like family protein")

        if "Repeat of unknown function XGLTT repeat-containing protein" in col4:
            col4 = col4.replace("Repeat of unknown function XGLTT repeat-containing protein", "XGLTT repeat-containing protein") 

        # SUSPECT_PRODUCT_NAMES: 2 features contain 'Fragment'
        if "Invasin/intimin cell-adhesion fragments superfamily protein" in col4:
            col4 = col4.replace("Invasin/intimin cell-adhesion fragments superfamily protein", "Invasin/intimin cell-adhesion superfamily protein")

        if "Myosin S1 fragment, N-terminal superfamily protein" in col4:
            col4 = col4.replace("Myosin S1 fragment, N-terminal superfamily protein", "Myosin S1 N-terminal superfamily protein")


        # SUSPECT_PRODUCT_NAMES: 4 features contain 'frame'
        if "T-cell receptor gamma alternate reading frame protein family protein" in col4:
            col4 = col4.replace("T-cell receptor gamma alternate reading frame protein family protein", "alternative T-cell receptor protein")

        if "PRKCH upstream open reading frame 2 family protein" in col4:
            col4 = col4.replace("PRKCH upstream open reading frame 2 family protein", "uPEP2 kinase inhibitor-like protein")

        if "ASNSD1 upstream open reading frame protein family protein" in col4:
            col4 = col4.replace("ASNSD1 upstream open reading frame protein family protein", "RPAP3/R2TP/prefoldin-like complex microprotein")

        if "PTEN upstream open reading frame MP31 family protein" in col4:
            col4 = col4.replace("PTEN upstream open reading frame MP31 family protein", "MP31 family protein")


        # SUSPECT_PRODUCT_NAMES: 2 features contain 'frameshift'
        # These do not need changes

        # SUSPECT_PRODUCT_NAMES: 2 features contain 'interrupt'
        # These do not need changes

        # FATAL: SUSPECT_PRODUCT_NAMES: 3 features contain 'open reading frame'
        # These do not need changes because of 'frame' being fixed already

        # SUSPECT_PRODUCT_NAMES: 2 features contain 'orphan protein'
        if "Substrate-binding orphan protein, GRRM family protein" in col4:
            col4 = col4.replace("Substrate-binding orphan protein, GRRM family protein", "extracellular solute-binding protein family 3 protein")

        if "Rad9, Rad1, Hus1-interacting nuclear orphan protein 1 family protein" in col4:
            col4 = col4.replace("Rad9, Rad1, Hus1-interacting nuclear orphan protein 1 family protein", "RHNO1 family protein")


        # FATAL: SUSPECT_PRODUCT_NAMES: 2 features contain 'partial'
        if "Partial AB-hydrolase lipase domain domain-containing protein" in col4:
            col4 = col4.replace("Partial AB-hydrolase lipase domain domain-containing protein", "AB-hydrolase lipase N-terminal domain-containing protein")

        if "Partial cleavage stimulation factor domain domain-containing protein" in col4:
            col4 = col4.replace("Partial cleavage stimulation factor domain domain-containing protein", "cleavage stimulation factor-like amino-terminal domain-containing protein")

        # print line to file
        outfile.write(f"{col1}\t{col2}\t{col3}\t{col4}\n")

# All Suspicious phrase issues are resolved
print("All Suspicious phrase issues are resolved")


####################################
#
# Handling Fixed products from NCBI; names originally included taxonomy and were deprecated to hypothetical protein
#
####################################
# Read input and process it
input_file = "Interpro_to_NCBI_step_4.txt"
output_file = "Interpro_to_NCBI_step_5.txt"

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        cols = line.split('\t')
        if len(cols) < 4:
            continue  # skip malformed lines

        col1, col2, col3, col4 = cols[0], cols[1], cols[2], cols[3]

        # test problem conditions and make replacements
        # SUSPECT_PRODUCT_NAMES: 5 features contain 'unknown'

        if "Proteinase inhibitor I16, Streptomyces subtilisin-type inhibitor, conserved site-containing protein" in col4: col4 = "subtilisin-type inhibitor conserved site-containing protein"
        if "Human immunodeficiency virus 1, envelope glycoprotein Gp120 domain-containing protein" in col4: col4 = "envelope glycoprotein Gp120 domain-containing protein"
        if "Human herpesvirus K1 glycoprotein, C-terminal domain-containing protein" in col4: col4 = "K1 glycoprotein C-terminal domain-containing protein"
        if "Arabidopsis retrotransposon Orf1, C-terminal domain-containing protein" in col4: col4 = "retrotransposon Orf1, C-terminal domain-containing protein"
        if "Mycoplasma lipoprotein, C-terminal domain-containing protein" in col4: col4 = "lipoprotein C-terminal domain-containing protein"
        if "Mycoplasma lipoprotein, central domain-containing protein" in col4: col4 = "lipoprotein central domain-containing protein"
        if "Rickettsial palindromic element 1 domain-containing protein" in col4: col4 = "palindromic element 1 domain-containing protein"
        if "Plasmodium yoelii subtelomeric PYST-C2 domain-containing protein" in col4: col4 = "subtelomeric PYST-C2 domain-containing protein"
        if "Exported protein, PHISTa/b/c, conserved domain, Plasmodium domain-containing protein" in col4: col4 = "PHISTa/b/c domain-containing protein"
        if "Yeast cell wall synthesis Kre9/Knh1, C-terminal domain-containing protein" in col4: col4 = "cell wall synthesis Kre9/Knh1 C-terminal domain-containing protein"
        if "Hemagglutinin, Mycoplasma domain-containing protein" in col4: col4 = "Hemagglutinin domain-containing protein"
        if "Mycoplasma virulence, signal domain-containing protein" in col4: col4 = "virulence signal domain-containing protein"
        if "Salmonella invasion protein A, N-terminal domain-containing protein" in col4: col4 = "invasion protein A, N-terminal domain-containing protein"
        if "Streptomyces killer toxin-like, beta/gamma crystallin domain-containing protein" in col4: col4 = "killer toxin-like, beta/gamma crystallin domain-containing protein"
        if "Yeast cell wall synthesis Kre9/Knh1-like, N-terminal domain-containing protein" in col4: col4 = "cell wall synthesis Kre9/Knh1-like, N-terminal domain-containing protein"
        if "Bacillus phage SPbeta, YonK domain-containing protein" in col4: col4 = "SPbeta, YonK domain-containing protein"
        if "Plasmodium RESA, N-terminal domain-containing protein" in col4: col4 = "RESA, N-terminal domain-containing protein"
        if "Human herpes virus-8, Protein K1, cytoplasmic domain-containing protein" in col4: col4 = "Protein K1, cytoplasmic domain-containing protein"
        if "Tryptophan/threonine-rich plasmodium antigen, C-terminal domain-containing protein" in col4: col4 = "Tryptophan/threonine-rich antigen, C-terminal domain-containing protein"
        if "Outer membrane protein B, passenger domain, Rickettsia domain-containing protein" in col4: col4 = "Outer membrane protein B, passenger domain-containing protein"
        if "Mycoplasma peptidase DUF31 domain-containing protein" in col4: col4 = "peptidase DUF31 domain-containing protein"
        if "Rickettsia palindromic element RPE2 domain-containing protein" in col4: col4 = "palindromic element RPE2 domain-containing protein"
        if "Rickettsia palindromic element RPE3 domain-containing protein" in col4: col4 = "palindromic element RPE3 domain-containing protein"
        if "Rickettsia palindromic element 5 domain-containing protein" in col4: col4 = "palindromic element 5 domain-containing protein"
        if "Rickettsia palindromic element RPE4 domain-containing protein" in col4: col4 = "palindromic element RPE4 domain-containing protein"
        if "Metallothionein domain, yeast domain-containing protein" in col4: col4 = "Metallothionein domain-containing protein"
        if "Transcription factor p53, C-terminal, Drosophila domain-containing protein" in col4: col4 = "Transcription factor p53, C-terminal domain-containing protein"
        if "Tuberculosis necrotizing toxin domain-containing protein" in col4: col4 = "necrotizing toxin domain-containing protein"
        if "Plasmodium falciparum erythrocyte membrane protein-1, N-terminal segment domain-containing protein" in col4: col4 = "erythrocyte membrane protein-1, N-terminal segment domain-containing protein"
        if "Plasmodium falciparum erythrocyte membrane protein 1, acidic terminal segment domain-containing protein" in col4: col4 = "erythrocyte membrane protein 1, acidic terminal segment domain-containing protein"
        if "Adenomatous polyposis coli, N-terminal dimerization domain-containing protein" in col4: col4 = "Adenomatous polyposis coli, N-terminal dimerization domain-containing protein"
        if "Plasmodium falciparum erythrocyte membrane protein 1, N-terminal domain-containing protein" in col4: col4 = "erythrocyte membrane protein 1, N-terminal domain-containing protein"
        if "Fission yeast Sec3, C-terminal domain-containing protein" in col4: col4 = "Sec3, C-terminal domain-containing protein"
        if "Plasmodium host cell traversal SPECT1 domain-containing protein" in col4: col4 = "host cell traversal SPECT1 domain-containing protein"
        if "Chlamydial protease/proteasome-like activity factor, PDZ domain-containing protein" in col4: col4 = "protease/proteasome-like activity factor, PDZ domain-containing protein"
        if "Yeast SAGA-associated factor 11, N-terminal domain-containing protein" in col4: col4 = "SAGA-associated factor 11, N-terminal domain-containing protein"
        if "RNase III, double-stranded RNA binding domain, animal domain-containing protein" in col4: col4 = "RNase III, double-stranded RNA binding domain-containing protein"
        if "Adenylate cyclase, C-terminal, yeast domain-containing protein" in col4: col4 = "Adenylate cyclase, C-terminal domain-containing protein"
        if "DNA-binding protein Rap1, C-terminal, S.pombe domain-containing protein" in col4: col4 = "DNA-binding protein Rap1, C-terminal, domain-containing protein"
        if "Campylobacter invasion antigen D, C-terminal domain-containing protein" in col4: col4 = "invasion antigen D, C-terminal domain-containing protein"
        if "Cysteine peptidase, putative, mycoplasmatota domain-containing protein" in col4: col4 = "putative cysteine peptidase domain-containing protein"
        if "Proteinase inhibitor I16, Streptomyces subtilisin-type inhibitor family protein" in col4: col4 = "Proteinase inhibitor I16, subtilisin-type inhibitor family protein"
        if "Yeast membrane protein DUP/COS family protein" in col4: col4 = "membrane protein DUP/COS family protein"
        if "Mouse mammary tumor virus superantigen family protein" in col4: col4 = "mammary tumor virus superantigen family protein"
        if "Alpha crystallin/Small heat shock protein, animal type family protein" in col4: col4 = "Alpha crystallin/Small heat shock protein family protein"
        if "Mycoplasma-specific lipoprotein, type 3 family protein" in col4: col4 = "lipoprotein type 3 family protein"
        if "Outer membrane protein, Helicobacter family protein" in col4: col4 = "Outer membrane protein family protein"
        if "Salmonella surface presentation of antigen M protein family protein" in col4: col4 = "surface presentation of antigen M protein family protein"
        if "Salmonella invasion protein InvJ family protein" in col4: col4 = "invasion protein InvJ family protein"
        if "Plasmodium circumsporozoite protein family protein" in col4: col4 = "circumsporozoite protein family protein"
        if "Salmonella virulence plasmid 65kDa B protein family protein" in col4: col4 = "virulence plasmid 65kDa B protein family protein"
        if "Salmonella plasmid virulence SpvA family protein" in col4: col4 = "plasmid virulence SpvA family protein"
        if "Salmonella/Shigella invasion protein E family protein" in col4: col4 = "invasion protein E family protein"
        if "Peptidase C58, Yersinia/Hemophilus virulence surface antigen family protein" in col4: col4 = "Peptidase C58 virulence surface antigen family protein"
        if "E3 ubiquitin-protein ligase SINA-like, animal family protein" in col4: col4 = "E3 ubiquitin-protein ligase SINA-like family protein"
        if "Male Drosophila accessory gland secretory protein family protein" in col4: col4 = "Male accessory gland secretory protein family protein"
        if "Bacillus/Clostridium Ger spore germination protein family protein" in col4: col4 = "Ger spore germination protein family protein"
        if "Giardia variant-specific surface protein family protein" in col4: col4 = "variant-specific surface protein family protein"
        if "Human herpesvirus 6 immediate early protein family protein" in col4: col4 = "immediate early protein family protein"
        if "Early transcribed membrane protein, plasmodium family protein" in col4: col4 = "Early transcribed membrane family protein"
        if "Arabidopsis thaliana F-box family protein" in col4: col4 = "F-box family protein"
        if "Arabidopsis F-box/kelch-repeat family protein" in col4: col4 = "F-box/kelch-repeat family protein"
        if "Human Olfactory Receptors family protein" in col4: col4 = "Olfactory Receptors family protein"
        if "Yeast SRP1/TIP1 Cell Wall family protein" in col4: col4 = "SRP1/TIP1 Cell Wall family protein"
        if "Arabidopsis F-box involved in BR signaling family protein" in col4: col4 = "F-box involved in BR signaling family protein"
        if "Arabidopsis Inactive Receptor-like Kinase family protein" in col4: col4 = "Inactive Receptor-like Kinase family protein"
        if "Drosophila Developmental Transcription Regulators family protein" in col4: col4 = "Developmental Transcription Regulators family protein"
        if "Caenorhabditis elegans Orphan Nuclear Receptors family protein" in col4: col4 = "Nuclear Receptors family protein"
        if "Yeast Cell Wall Mannoprotein PIR family protein" in col4: col4 = "Cell Wall Mannoprotein PIR family protein"
        if "Plasmodium Circumsporozoite Invasion Protein family protein" in col4: col4 = "Circumsporozoite Invasion Protein family protein"
        if "Schizosaccharomyces pombe Mam3/Map4 family protein" in col4: col4 = "Mam3/Map4 family protein"
        if "Mouse Killer cell lectin-like receptor family protein" in col4: col4 = "Killer cell lectin-like receptor family protein"
        if "Yeast Metabolic Pathway Regulatory Proteins family protein" in col4: col4 = "Metabolic Pathway Regulatory Proteins family protein"
        if "Arabidopsis DESIGUAL family protein" in col4: col4 = "DESIGUAL family protein"
        if "Caenorhabditis elegans Nuclear Hormone Receptors family protein" in col4: col4 = "Nuclear Hormone Receptors family protein"
        if "Arabidopsis PWWP domain-containing family protein" in col4: col4 = "PWWP domain-containing family protein"
        if "Yeast Multidrug Resistance Regulatory Proteins family protein" in col4: col4 = "Multidrug Resistance Regulatory Proteins family protein"
        if "Bacillus subtilis Transition State Regulators family protein" in col4: col4 = "Transition State Regulators family protein"
        if "C. elegans Developmental and Neuronal Protein family protein" in col4: col4 = "Developmental and Neuronal Protein family protein"
        if "Giardia Variant Surface Antigen family protein" in col4: col4 = "Variant Surface Antigen family protein"
        if "C. elegans Fungus-Induced Response family protein" in col4: col4 = "Fungus-Induced Response family protein"
        if "Chlamydial Translocated Actin-Recruiting Phosphoprotein family protein" in col4: col4 = "Translocated Actin-Recruiting Phosphoprotein family protein"
        if "Plasmodium ABRA-related family protein" in col4: col4 = "ABRA-related family protein"
        if "Virilizer, yeast family protein" in col4: col4 = "Virilizer family protein"
        if "Mycoplasma-type histidine triad protein HinT family protein" in col4: col4 = "histidine triad protein HinT family protein"
        if "SrfA-like, pseudomonas family protein" in col4: col4 = "SrfA-like protein"
        if "Salmonella invasion protein A, C-terminal actin-binding domain superfamily protein" in col4: col4 = "invasion protein A, C-terminal actin-binding domain superfamily protein"
        if "Salmonella invasion protein A, chaperone-binding superfamily protein" in col4: col4 = "invasion protein A, chaperone-binding superfamily protein"
        if "Hem peroxidase domain superfamily, animal type superfamily protein" in col4: col4 = "Hem peroxidase domain superfamily protein"
        if "Drosophila transcription factor p53, C-terminal domain superfamily protein" in col4: col4 = "p53 C-terminal domain superfamily protein"
        if "Plasmodium falciparum UIS3, C-terminal domain superfamily protein" in col4: col4 = "UIS3 C-terminal domain superfamily protein"
        if "Yeast killer toxin superfamily protein" in col4: col4 = "killer toxin superfamily protein"
        if "Human cytomegalovirus, UL16 ectodomain superfamily protein" in col4: col4 = "UL16 ectodomain superfamily protein"
        if "Mycoplasma arthritidis-derived mitogen, C-terminal superfamily protein" in col4: col4 = "mitogen, C-terminal superfamily protein"
        if "Plasmodium RESA, N-terminal helical domain superfamily protein" in col4: col4 = "RESA, N-terminal helical domain superfamily protein"
        if "Plasmodium falciparum erythrocyte membrane protein 1, acidic terminal segment superfamily protein" in col4: col4 = "erythrocyte membrane protein 1, acidic terminal segment superfamily protein"
        if "Plasmodium yoelii repeat of length 46 repeat-containing protein" in col4: col4 = "repeat of length 46 repeat-containing protein"
        if "Plasmodium-MYXSPDY repeat-containing protein" in col4: col4 = "MYXSPDY repeat-containing protein"
        if "Plasmodium repeat of length 46 repeat-containing protein" in col4: col4 = "repeat of length 46 repeat-containing protein"
        if "Dilute domain-containing protein, fungi, CBD domain-containing protein" in col4: col4 = "Dilute domain-containing protein, CBD domain-containing protein"
        if "Homocitrate synthase, catalytic TIM barrel domain, fungi/bacteria domain-containing protein" in col4: col4 = "Homocitrate synthase, catalytic TIM barrel domain-containing protein"
        if "Tetratricopeptide repeat, fungi 2 domain-containing protein" in col4: col4 = "Tetratricopeptide repeat-containing protein"
        if "Protein PBDC1, metazoa/fungi family protein" in col4: col4 = "Protein PBDC1 family protein"
        if "Phosphoribosylaminoimidazole carboxylase, fungi/plant family protein" in col4: col4 = "Phosphoribosylaminoimidazole carboxylase family protein"
        if "Mechanosensitive ion channel MscS-like, plants/fungi family protein" in col4: col4 = "Mechanosensitive ion channel MscS-like family protein"
        if "Checkpoint protein Rad17/Rad24, fungi/metazoa family protein" in col4: col4 = "Checkpoint protein Rad17/Rad24 family protein"
        if "Mediator complex, subunit Med8, fungi/metazoa family protein" in col4: col4 = "Mediator complex, subunit Med8 family protein"
        if "Atypical dual-specificity phosphatase Siw14-like, plant and fungi family protein" in col4: col4 = "Atypical dual-specificity phosphatase Siw14-like family protein"
        if "NADH dehydrogenase [ubiquinone] 1 beta subcomplex subunit 2, plant/fungi family protein" in col4: col4 = "NADH dehydrogenase [ubiquinone] 1 beta subcomplex subunit 2 family protein"
        if "Spc24, Fungi, globular domain superfamily protein" in col4: col4 = "Spc24 globular domain superfamily protein"
        if "Giardia dicer, N-terminal domain-containing protein" in col4: col4 = "dicer, N-terminal domain-containing protein"
        if "Fructose-bisphosphate aldolase, class II, yeast/E. coli subtype family protein" in col4: col4 = "Fructose-bisphosphate aldolase, class II subtype family protein"
        if "Plasmodium yoelii subtelomeric PYST-B family protein" in col4: col4 = "subtelomeric PYST-B family protein"
        if "Plasmodium yoelii subtelomeric PYST-A family protein" in col4: col4 = "subtelomeric PYST-A family protein"
        if "Plasmodium yoelii subtelomeric PYST-D family protein" in col4: col4 = "subtelomeric PYST-D family protein"
        if "Plasmodium subtelomeric PST-A family protein" in col4: col4 = "PST-A family protein"
        if "Polyadenylate binding protein, human types 1, 2, 3, 4 family protein" in col4: col4 = "Polyadenylate binding protein types 1, 2, 3, 4 family protein"
        if "DM11, Drosophila melanogaster family protein" in col4: col4 = "DM11 family protein"
        if "Protein of unknown function DUF1431, cysteine-rich, Drosophila family protein" in col4: col4 = "Protein of unknown function DUF1431, cysteine-rich family protein"
        if "Agrobacterium VirD5 protein family protein" in col4: col4 = "VirD5 protein family protein"
        if "Mycoplasma P48 major surface lipoprotein family protein" in col4: col4 = "P48 major surface lipoprotein family protein"
        if "Outer membrane adhesion, Yersinia family protein" in col4: col4 = "Outer membrane adhesion family protein"
        if "Staphylococcus aureus exotoxin family protein" in col4: col4 = "exotoxin family protein"
        if "Drosophila accessory gland-specific peptide 26Ab family protein" in col4: col4 = "accessory gland-specific peptide 26Ab family protein"
        if "P21 molecular chaperone, Bacillus thuringiensis family protein" in col4: col4 = "P21 molecular chaperone family protein"
        if "Campylobacter major outer membrane family protein" in col4: col4 = "major outer membrane family protein"
        if "Human herpesvirus U15 family protein" in col4: col4 = "U15 family protein"
        if "Helicobacter pylori IceA2 family protein" in col4: col4 = "IceA2 family protein"
        if "Plasmodium histidine-rich family protein" in col4: col4 = "histidine-rich family protein"
        if "Plasmodium vivax Vir family protein" in col4: col4 = "Vir family protein"
        if "Pseudomonas avirulence D family protein" in col4: col4 = "avirulence D family protein"
        if "Salmonella plasmid virulence SpvD family protein" in col4: col4 = "plasmid virulence SpvD family protein"
        if "Yeast trans-acting factor family protein" in col4: col4 = "trans-acting factor family protein"
        if "Bacillus PapR family protein" in col4: col4 = "PapR family protein"
        if "Drosophila roughex family protein" in col4: col4 = "roughex family protein"
        if "S. aureus uracil DNA glycosylase inhibitor family protein" in col4: col4 = "uracil DNA glycosylase inhibitor family protein"
        if "Drosophila ACP53EA family protein" in col4: col4 = "ACP53EA family protein"
        if "ESAT-6-like protein, Mycobacterium family protein" in col4: col4 = "ESAT-6-like family protein"
        if "Human herpesvirus U55 family protein" in col4: col4 = "U55 family protein"
        if "Escherichia phage P2, Tail assembly protein E' family protein" in col4: col4 = "P2, Tail assembly protein E' family protein"
        if "Rhoptry-associated protein 1, plasmodium family protein" in col4: col4 = "Rhoptry-associated protein 1 family protein"
        if "Human herpesvirus U26 family protein" in col4: col4 = "U26 family protein"
        if "Transcription antitermination protein, NusG, mycoplasma-related family protein" in col4: col4 = "Transcription antitermination protein, NusG family protein"
        if "Caenorhabditis elegans ly-6-related family protein" in col4: col4 = "ly-6-related family protein"
        if "Human herpes virus type 4, BALF1 family protein" in col4: col4 = "type 4, BALF1 family protein"
        if "Transcription initiation factor TFIID subunit 1, animal family protein" in col4: col4 = "Transcription initiation factor TFIID subunit 1 family protein"
        if "N-acetylglutamate synthase, animal family protein" in col4: col4 = "N-acetylglutamate synthase family protein"
        if "Mycoplasma MFS transporter family protein" in col4: col4 = "MFS transporter family protein"
        if "Pyrococcus aspartate kinase subunit, putative family protein" in col4: col4 = "putative aspartate kinase subunit family protein"
        if "Cytochrome c, Bacillus subtilis c550-type family protein" in col4: col4 = "Cytochrome c, c550-type family protein"
        if "E3 ubiquitin-protein ligase substrate receptor Mms22, budding yeast family protein" in col4: col4 = "E3 ubiquitin-protein ligase substrate receptor Mms22 family protein"
        if "Cytochrome c oxidase subunit VII, budding yeast family protein" in col4: col4 = "Cytochrome c oxidase subunit VII family protein"
        if "Acid phosphatase, Aspergillus type family protein" in col4: col4 = "Acid phosphatase family protein"
        if "putative membrane protein, Bacillus YphA type family protein" in col4: col4 = "putative membrane protein, YphA type family protein"
        if "putative 26S proteasome regulatory complex, non-ATPase subcomplex, subunit s5a, Plasmodium family protein" in col4: col4 = "putative 26S proteasome regulatory complex, non-ATPase subcomplex, subunit s5a family protein"
        if "Mannosyltransferase/phosphorylase 1-like, Leishmania family protein" in col4: col4 = "Mannosyltransferase/phosphorylase 1-like protein"
        if "Mitogen, Yersinia pseudotuberculosis family protein" in col4: col4 = "Mitogen family protein"
        if "Yeast killer toxin family protein" in col4: col4 = "killer toxin family protein"
        if "CST complex subunit Ten1, animal and plant type family protein" in col4: col4 = "CST complex subunit Ten1 family protein"
        if "Cyclophilin-type peptidyl-prolyl cis-trans isomerase, E. coli cyclophilin A-like family protein" in col4: col4 = "Cyclophilin-type peptidyl-prolyl cis-trans isomerase, cyclophilin A-like family protein"
        if "Yeast cell wall synthesis Kre9/Knh1 family protein" in col4: col4 = "cell wall synthesis Kre9/Knh1 family protein"
        if "CiaI campylobacter virulence factor family protein" in col4: col4 = "virulence factor family protein"
        if "Neutral ceramidase, Mycobacterium family protein" in col4: col4 = "Neutral ceramidase family protein"
        if "Outer membrane protein OmpB, Rickettsia family protein" in col4: col4 = "Outer membrane protein OmpB family protein"
        if "Replication initiator protein, streptomyces family protein" in col4: col4 = "Replication initiator family protein"
        if "Conserved hypothetical protein CHP01519, Plasmodium falciparum (isolate 3D7) family protein" in col4: col4 = "CHP01519 family protein"
        if "Conserved hypothetical protein CHP01609, Plasmodium spp family protein" in col4: col4 = "Conserved hypothetical protein CHP01609,-like"
        if "Mycoplasma P30 family protein" in col4: col4 = "P30 family protein"
        if "Gamete antigen, Plasmodium species family protein" in col4: col4 = "Gamete antigen family protein"
        if "Mycoplasma arthritidis-derived mitogen family protein" in col4: col4 = "mitogen family protein"
        if "Spermine synthase, animal family protein" in col4: col4 = "Spermine synthase family protein"
        if "Surface antigen, Rickettsia type family protein" in col4: col4 = "Surface antigen family protein"
        if "Ribosome assembly protein RSM22, mitochondrial, budding yeast family protein" in col4: col4 = "Ribosome assembly protein RSM22, mitochondrial family protein"
        if "Alpha-(1, 3)-fucosyltransferase/alpha-(1, 4)-fucosyltransferase, Helicobacter family protein" in col4: col4 = "Alpha-(1, 3)-fucosyltransferase/alpha-(1, 4)-fucosyltransferase family protein"
        if "Mitochondrial ATP synthase subunit g, animal family protein" in col4: col4 = "Mitochondrial ATP synthase subunit g protein"
        if "Poly(A) polymerase complex subunit Air1/2, budding yeast family protein" in col4: col4 = "Poly(A) polymerase complex subunit Air1/2 family protein"
        if "Spodoptera frugiperda nuclear polyhedrosis virus (SfNPV), sf27 family protein" in col4: col4 = "nuclear polyhedrosis virus (SfNPV), sf27 family protein"
        if "Transcription initiation factor Rrn11, budding yeast family protein" in col4: col4 = "Transcription initiation factor Rrn11 family protein"
        if "ABC-type oligopeptide transport system, solute-binding component, Mycoplasmataceae, predicted family protein" in col4: col4 = "putative ABC-type oligopeptide transport system, solute-binding component family protein"
        if "DUF34/NIF3, animal family protein" in col4: col4 = "DUF34/NIF3 family protein"
        if "Peptidase S8A, subtilisin-like peptidase 1, plasmodium family protein" in col4: col4 = "Peptidase S8A, subtilisin-like peptidase 1 family protein"
        if "Peptidase S8A, subtilisin-related, campylobacter family protein" in col4: col4 = "Peptidase S8A, subtilisin-related family protein"
        if "Histone deacetylase class II, yeast family protein" in col4: col4 = "Histone deacetylase class II family protein"
        if "Lytic switch protein BZLF1, human herpesvirus 4 family protein" in col4: col4 = "Lytic switch protein BZLF1 family protein"
        if "5 transmembrane protein, Schizosaccharomyces pombe family protein" in col4: col4 = "5 transmembrane protein family protein"
        if "CRISPR-associated protein Cas1, ECOLI subtype family protein" in col4: col4 = "CRISPR-associated protein Cas1 family protein"
        if "Rickettsia surface antigen, 120kDa family protein" in col4: col4 = "surface antigen, 120kDa family protein"
        if "Plasmodium falciparum UIS3 membrane protein family protein" in col4: col4 = "UIS3 membrane protein family protein"
        if "Fam-L/Fam-M-like, plasmodium family protein" in col4: col4 = "Fam-L/Fam-M-like family protein"
        if "Human herpesvirus, UL121 family protein" in col4: col4 = "UL121 family protein"
        if "Salmonella outer protein D family protein" in col4: col4 = "outer protein D family protein"
        if "Protein-glutamine gamma-glutamyltransferase, animal family protein" in col4: col4 = "Protein-glutamine gamma-glutamyltransferase family protein"
        if "Human herpesvirus 5 RL5A/RL6 family protein" in col4: col4 = "RL5A/RL6 family protein"
        if "Ribosomally synthesised peptide in Streptomyces family protein" in col4: col4 = "Ribosomally synthesised peptide family protein"
        if "Suv4-20 family, animal family protein" in col4: col4 = "Suv4-20 family family protein"
        if "Fatty acid synthase alpha subunit, yeast family protein" in col4: col4 = "Fatty acid synthase alpha subunit family protein"
        if "Harbinger transposase-derived nuclease, animal family protein" in col4: col4 = "Harbinger transposase-derived nuclease family protein"
        if "NADH dehydrogenase [ubiquinone] 1 beta subcomplex subunit 2, animal type family protein" in col4: col4 = "NADH dehydrogenase [ubiquinone] 1 beta subcomplex subunit 2 family protein"
        if "Protein translocase subunit SecA 2, Bacillus anthracis-type family protein" in col4: col4 = "Protein translocase subunit SecA 2 family protein"
        if "Helicobacter TNF-alpha-inducing protein family protein" in col4: col4 = "TNF-alpha-inducing protein family protein"
        if "Pathogenicity island protein gp6, Staphylococcus family protein" in col4: col4 = "Pathogenicity island protein gp6, family protein"
        if "Adhesin JlpA, Campylobacter family protein" in col4: col4 = "Adhesin JlpA family protein"
        if "Na+/H+ antiporter, budding yeast family protein" in col4: col4 = "Na+/H+ antiporter family protein"
        if "MICOS complex subunit MIC26/MIC27, animal family protein" in col4: col4 = "MICOS complex subunit MIC26/MIC27 family protein"
        if "Bacillus competence protein S family protein" in col4: col4 = "protein S family protein"
        if "Streptomyces scabies esterase-like family protein" in col4: col4 = "esterase-like family protein"
        if "DNA-Binding protein G5P, Pseudomonas family protein" in col4: col4 = "DNA-Binding protein G5P family protein"
        if "Histone-lysine N-methyltransferase SETD2, animal family protein" in col4: col4 = "Histone-lysine N-methyltransferase SETD2 family protein"
        if "Formin-like protein, animal family protein" in col4: col4 = "Formin-like protein"
        if "Streptococcus phage 7201, Orf18 family protein" in col4: col4 = "phage 7201, Orf18 family protein"
        if "Campylobacter phage CGC-2007, Cje0229 family protein" in col4: col4 = "phage CGC-2007, Cje0229 family protein"
        if "Mycobacterium phage PG1, Gp7 family protein" in col4: col4 = "phage PG1, Gp7 family protein"
        if "Human herpesvirus 5, RL1 family protein" in col4: col4 = "RL1 family protein"
        if "Humanin family protein" in col4: col4 = "microprotein HNM 1 family protein"
        if "Bacillus phage protein-like superfamily protein" in col4: col4 = "phage protein-like superfamily protein"
        if "Plasmodium repeat-containing protein" in col4: col4 = "malaria repeat-containing protein"


        # a few more typos left to take care of as well:
        if " fungi domain-" in col4:
            col4 = col4.replace(" fungi domain-"," domain-")
        if "methyltranferase" in col4: 
            col4 = col4.replace("methyltranferase","methyltransferase")
        if "Possible" in col4:
            col4 = col4.replace("Possible","putative")
        if "Adenomatous polyposis coli," in col4:
            col4 = col4.replace("Adenomatous polyposis coli,","APC")
        if "O-acetyltranferase" in col4:
            col4 = col4.replace("O-acetyltranferase","O-acetyltransferase")
        if "Autotransproter" in col4:
            col4 = col4.replace("Autotransproter","Autotransporter")
        if "K+ potassium" in col4:
            col4 = col4.replace("K+ potassium","potassium")
        if "Fibre" in col4:
            col4 = col4.replace("Fibre","fiber")
        if "resistence" in col4:
            col4 = col4.replace("resistence","resistance")
        if "Dihem" in col4:
            col4 = col4.replace("Dihem","diheme")
        if "Protein of unknwon function" in col4:
            col4 = col4.replace("Protein of unknwon function","unknown function")
        if "family family" in col4:
            col4 = col4.replace("family family","family")
        if "putative putative" in col4:
            col4 = col4.replace("putative putative","putative")
        if "Family family" in col4:
            col4 = col4.replace("Family family","family")
        if "putative conserved protein," in col4:
            col4 = col4.replace("putative conserved protein,","")
        if "Partial AB-hydrolase" in col4:
            col4 = col4.replace("Partial ","")
        if "Partial cleavage" in col4:
            col4 = col4.replace("Partial ","")
        if "DUF3566." in col4:
            col4 = col4.replace("DUF3566.","DUF3566")
        if "DUF3987) family" in col4:
            col4 = col4.replace(")","")
        if "DUF4257) family" in col4:
            col4 = col4.replace(")","")
        if "(DUF4381 family" in col4:
            col4 = col4.replace("(","")
        if " homologue" in col4:
            col4 = col4.replace(" homologue","")
        if " homolog" in col4:
            col4 = col4.replace(" homolog","")
        if " HOMOLOG " in col4:
            col4 = col4.replace(" HOMOLOG","")
        if " Homolog " in col4:
            col4 = col4.replace(" Homolog","")
        if " orthologue" in col4:
            col4 = col4.replace(" orthologue"," ortholog")
        if " ortholog" in col4:
            col4 = col4.replace(" ortholog","")
        if "Spen paralogue/orthologue" in col4:
            col4 = col4.replace("/orthologue","/ortholog")
        if "RAD51 Paralog" in col4:
            col4 = col4.replace(" Paralog","")
        if "Spen paralogue" in col4:
            col4 = col4.replace(" paralogue"," paralog")
        if " paralogue " in col4:
            col4 = col4.replace("  paralogue"," paralog")
        if "M penetrans paralogue 26" in col4:
            col4 = col4.replace("M penetrans paralogue 26","MpPF26")

        # print line to file
        outfile.write(f"{col1}\t{col2}\t{col3}\t{col4}\n")

# All taxonomy-based issues are resolved
print("All taxonomy-based issues are resolved")


####################################
#
# Issues remaining to investigate:
#  781 features contains three or more numbers together that may be identifiers more appropriate in note
#  131 features contain underscore
#
####################################
# Read input and process it
input_file = "Interpro_to_NCBI_step_5.txt"
output_file = "Interpro_to_NCBI_step_6.txt"

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        cols = line.split('\t')
        if len(cols) < 4:
            continue  # skip malformed lines

        col1, col2, col3, col4 = cols[0], cols[1], cols[2], cols[3]

        # test problem conditions and make replacements
        if "_" in col4:
            col4 = col4.replace("_","-")
            # col4 = col4.replace("_"," ")

        # print line to file
        outfile.write(f"{col1}\t{col2}\t{col3}\t{col4}\n")

# All underscores removed
print("All underscores are removed")




####################################
#
# Issues remaining to investigate:
#  781 features contains three or more numbers together 
#  MANY OF THESE ARE LEGIT PROTEIN NAMES
#  Many cannot be changed because they are based on similarity and not function
#  Only about 200 could be modified to conform better
#
####################################
# Read input and process it
input_file = "Interpro_to_NCBI_step_6.txt"
output_file = "Interpro_to_NCBI.txt"

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        cols = line.split('\t')
        if len(cols) < 4:
            continue  # skip malformed lines

        col1, col2, col3, col4 = cols[0], cols[1], cols[2], cols[3]

        # test problem conditions and make replacements
        if "Repeat of uncharacterized protein PH0542 repeat-containing protein" in col4:
            col4 = col4.replace("Repeat of uncharacterized protein PH0542 repeat-containing protein","PH0542-like repeat-containing protein")
        if "116kDa U5 small nuclear ribonucleoprotein component, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("116kDa U5 small nuclear ribonucleoprotein component, C-terminal domain-containing protein","U5 small nuclear ribonucleoprotein subunit, C-terminal domain-containing protein")
        if "116kDa U5 small nuclear ribonucleoprotein component, N-terminal domain-containing protein" in col4:
            col4 = col4.replace("116kDa U5 small nuclear ribonucleoprotein component, N-terminal domain-containing protein","U5 small nuclear ribonucleoprotein subunit, N-terminal domain-containing protein")
        if "A-kinase anchor 110kDa, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("A-kinase anchor 110kDa, C-terminal domain-containing protein","A-kinase anchor, C-terminal domain-containing protein")
        if "Arabinosidase BT 3657-like, N-terminal domain-containing protein" in col4:
            col4 = col4.replace("Arabinosidase BT 3657-like, N-terminal domain-containing protein","Arabinosidase-like, N-terminal domain-containing protein")
        if "At1g61320/AtMIF1, LRR domain-containing protein" in col4:
            col4 = col4.replace("At1g61320/AtMIF1, LRR domain-containing protein","LRR domain-containing protein")
        if "V-type ATPase, V0 complex, 116kDa subunit family protein" in col4:
            col4 = col4.replace("V-type ATPase, V0 complex, 116kDa subunit family protein","V-type ATPase, V0 complex subunit family protein")
        if "Zinc finger protein HVO 2753-like, euryarchaeota family protein" in col4:
            col4 = col4.replace("Zinc finger protein HVO 2753-like, euryarchaeota family protein","Zinc finger family protein")
        if "ZNF706/At2g23090 superfamily protein" in col4:
            col4 = col4.replace("ZNF706/At2g23090 superfamily protein","ZNF706 superfamily protein")
        if "CRISPR system ring nuclease SSO1393-like domain-containing protein" in col4:
            col4 = col4.replace("CRISPR system ring nuclease SSO1393-like domain-containing protein","CRISPR system ring nuclease-like domain-containing protein")
        if "CRISPR system ring nuclease SSO1393-like, winged-helix domain-containing protein" in col4:
            col4 = col4.replace("CRISPR system ring nuclease SSO1393-like, winged-helix domain-containing protein","CRISPR system ring nuclease-like, winged-helix domain-containing protein")
        if "CRISPR system ring nuclease SSO2081-like domain-containing protein" in col4:
            col4 = col4.replace("CRISPR system ring nuclease SSO2081-like domain-containing protein","CRISPR system ring nuclease-like domain-containing protein")
        if "Centrosomal protein 104 kDa-like family protein" in col4:
            col4 = col4.replace("Centrosomal protein 104 kDa-like family protein","Centrosomal protein 104-like family protein")
        if "Sodium/solute symporter, VC2705 subfamily protein" in col4:
            col4 = col4.replace("Sodium/solute symporter, VC2705 subfamily protein","Sodium/solute symporter subfamily protein")
        if "Centrosomal protein of 290kDa, coiled-coil region domain-containing protein" in col4:
            col4 = col4.replace("Centrosomal protein of 290kDa, coiled-coil region domain-containing protein","Centrosomal protein 290 coiled-coil region-containing protein")
        if "Signal transduction histidine kinase, hybrid-type, BC3207, predicted family protein" in col4:
            col4 = col4.replace("Signal transduction histidine kinase, hybrid-type, BC3207, predicted family protein","Signal transduction histidine kinase, hybrid-type family protein")
        if "3'-5' exoribonuclease Rv2179c-like domain-containing protein" in col4:
            col4 = col4.replace("3'-5' exoribonuclease Rv2179c-like domain-containing protein","3'-5' exoribonuclease-like domain-containing protein")
        if "ABC-type uncharacterized transport system, substrate-binding component, TM0202 type family protein" in col4:
            col4 = col4.replace("ABC-type uncharacterized transport system, substrate-binding component, TM0202 type family protein","ABC-type transport system substrate-binding protein")
        if "AP180-like N-terminal domain, plants domain-containing protein" in col4:
            col4 = col4.replace("AP180-like N-terminal domain, plants domain-containing protein","AP180-like N-terminal domain-containing protein")
        if "At2g17340, three-helix bundle domain superfamily protein" in col4:
            col4 = col4.replace("At2g17340, three-helix bundle domain superfamily protein","N-terminal damage-control phosphatase three-helix bundle domain superfamily protein")
        if "At2g23090-like, zinc-binding domain-containing protein" in col4:
            col4 = col4.replace("At2g23090-like, zinc-binding domain-containing protein","zinc-binding domain-containing protein")
        if "At3g06530-like, ARM-repeat domain-containing protein" in col4:
            col4 = col4.replace("At3g06530-like, ARM-repeat domain-containing protein","ARM-repeat domain-containing protein")
        if "At5g42320-like, carboxypeptidase domain-containing protein" in col4:
            col4 = col4.replace("At5g42320-like, carboxypeptidase domain-containing protein","M14 family carboxypeptidase domain-containing protein")
        if "At5g58720/SDE5-like, UBA-like domain-containing protein" in col4:
            col4 = col4.replace("At5g58720/SDE5-like, UBA-like domain-containing protein","SDE5-like, UBA-like domain-containing protein")
        if "ATP-dependent DNA Hel308 helicase family protein" in col4:
            col4 = col4.replace("ATP-dependent DNA Hel308 helicase family protein","ATP-dependent DNA helicase family protein")
        if "ATP-dependent DNA helicase Hel308-like, domain 4 domain-containing protein" in col4:
            col4 = col4.replace("ATP-dependent DNA helicase Hel308-like, domain 4 domain-containing protein","ATP-dependent DNA helicase-like domain-containing protein")
        if "ATPase, Atu1862 type, predicted family protein" in col4:
            col4 = col4.replace("ATPase, Atu1862 type, predicted family protein","putative ATPase family protein")
        if "ATPase, SAG2001, predicted family protein" in col4:
            col4 = col4.replace("ATPase, SAG2001, predicted family protein","ATPase, SAG2001-like family protein")
        if "ATPase, V0 complex, subunit 116kDa, eukaryotic family protein" in col4:
            col4 = col4.replace("ATPase, V0 complex, subunit 116kDa, eukaryotic family protein","ATPase, V0 complex subunit protein")
        if "B-129, C2H2 zinc finger domain-containing protein" in col4:
            col4 = col4.replace("B-129, C2H2 zinc finger domain-containing protein","C2H2 zinc finger domain-containing protein")
        if "BA3454 stress response protein family protein" in col4:
            col4 = col4.replace("BA3454 stress response protein family protein","putative stress response family protein")
        if "Bacteriocin precursor, CLOSPO-01332, putative family protein" in col4:
            col4 = col4.replace("Bacteriocin precursor, CLOSPO-01332, putative family protein","putative bacteriocin precursor family protein")
        if "NUP160, helical domain, plants domain-containing protein" in col4:
            col4 = col4.replace("NUP160, helical domain, plants domain-containing protein","NUP160, helical domain-containing protein")
        if "Obg-like GTPase YGR210-like, G4 motif-containing domain-containing protein" in col4:
            col4 = col4.replace("Obg-like GTPase YGR210-like, G4 motif-containing domain-containing protein","Obg-like GTPase G4 motif-containing protein")
        if "Orsellinic acid/F9775 biosynthesis cluster protein D family protein" in col4:
            col4 = col4.replace("Orsellinic acid/F9775 biosynthesis cluster protein D family protein","Orsellinic acid biosynthesis cluster protein D family protein")
        if "OTT 1508-like deaminase family protein" in col4:
            col4 = col4.replace("OTT 1508-like deaminase family protein","deaminase family protein")
        if "Outer membrane-associated lipoprotein TP0453 domain-containing protein" in col4:
            col4 = col4.replace("Outer membrane-associated lipoprotein TP0453 domain-containing protein","Outer membrane-associated lipoprotein domain-containing protein")
        if "P-loop ATP/GTP binding protein, All4644, predicted family protein" in col4:
            col4 = col4.replace("P-loop ATP/GTP binding protein, All4644, predicted family protein","putative P-loop ATP/GTP binding protein family protein")
        if "T1SS-143 repeat-containing domain-containing protein" in col4:
            col4 = col4.replace("T1SS-143 repeat-containing domain-containing protein","T1SS-143 repeat-containing protein")
        if "Tail protein NMB1110-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Tail protein NMB1110-like, C-terminal domain-containing protein","Tail protein-like, C-terminal domain-containing protein")
        if "Tail protein NMB1110-like, third domain-containing protein" in col4:
            col4 = col4.replace("Tail protein NMB1110-like, third domain-containing protein","Tail protein-like, third domain-containing protein")
        if "TetR transcriptional regulator Rv1219c-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("TetR transcriptional regulator Rv1219c-like, C-terminal domain-containing protein","TetR transcriptional regulator-like C-terminal domain-containing protein")
        if "TetR transcriptional regulator TM 1030-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("TetR transcriptional regulator TM 1030-like, C-terminal domain-containing protein","TetR transcriptional regulator-like C-terminal domain-containing protein")
        if "Tetracyclin repressor SCO1712-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Tetracyclin repressor SCO1712-like, C-terminal domain-containing protein","Tetracycline repressor-like C-terminal domain-containing protein")
        if "Tetracyclin repressor SMU 134-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Tetracyclin repressor SMU 134-like, C-terminal domain-containing protein","Tetracycline repressor-like C-terminal domain-containing protein")
        if "Tetracyclin repressor-like HI 0893, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Tetracyclin repressor-like HI 0893, C-terminal domain-containing protein","Tetracycline repressor-like C-terminal domain-containing protein")
        if "Tetracyclin repressor-like MT0489/Rv0472c, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Tetracyclin repressor-like MT0489/Rv0472c, C-terminal domain-containing protein","Tetracycline repressor-like C-terminal domain-containing protein")
        if "Transcription factor tau 138 kDa subunit, extended winged helix domain-containing protein" in col4:
            col4 = col4.replace("Transcription factor tau 138 kDa subunit, extended winged helix domain-containing protein","Transcription factor tau subunit extended winged helix domain-containing protein")
        if "Type III effector Xcv3220-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Type III effector Xcv3220-like, C-terminal domain-containing protein","Type III effector-like, C-terminal domain-containing protein")
        if "Type IV pilin Tt1218-like domain-containing protein" in col4:
            col4 = col4.replace("Type IV pilin Tt1218-like domain-containing protein","Type IV pilin-like domain-containing protein")
        if "Type IV pilin Tt1219-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Type IV pilin Tt1219-like, C-terminal domain-containing protein","Type IV pilin-like, C-terminal domain-containing protein")
        if "UDP-N-acetylglucosamine--peptide N-acetylglucosaminyltransferase 110kDa subunit family protein" in col4:
            col4 = col4.replace("UDP-N-acetylglucosamine--peptide N-acetylglucosaminyltransferase 110kDa subunit family protein","UDP-N-acetylglucosamine--peptide N-acetylglucosaminyltransferase subunit family protein")
        if "AF 0060, NTP Pyrophosphohydrolase MazG-like domain-containing protein" in col4:
            col4 = col4.replace("AF 0060, NTP Pyrophosphohydrolase MazG-like domain-containing protein","NTP Pyrophosphohydrolase MazG-like domain-containing protein")
        if "AF 0587-like, pre-PUA domain-containing protein" in col4:
            col4 = col4.replace("AF 0587-like, pre-PUA domain-containing protein","pre-PUA domain-containing protein")
        if "Baculovirus Y142 protein family protein" in col4:
            col4 = col4.replace("Baculovirus Y142 protein family protein","Baculovirus Y142 family protein")
        if "Carboxypeptidase Rv3627c-like, N-terminal domain-containing protein" in col4:
            col4 = col4.replace("Carboxypeptidase Rv3627c-like, N-terminal domain-containing protein","Carboxypeptidase-like, N-terminal domain-containing protein")
        if "F-box protein At3g26010-like, beta-propeller domain-containing protein" in col4:
            col4 = col4.replace("F-box protein At3g26010-like, beta-propeller domain-containing protein","F-box protein-like, beta-propeller domain-containing protein")
        if "F-box protein AT5G49610-like, beta-propeller domain-containing protein" in col4:
            col4 = col4.replace("F-box protein AT5G49610-like, beta-propeller domain-containing protein","F-box protein-like, beta-propeller domain-containing protein")
        if "F-box protein At5g52880-like, ARM repeat region domain-containing protein" in col4:
            col4 = col4.replace("F-box protein At5g52880-like, ARM repeat region domain-containing protein","F-box protein-like, ARM repeat region domain-containing protein")
        if "F-box/LRR-repeat protein 15/At3g58940/PEG3-like, LRR domain-containing protein" in col4:
            col4 = col4.replace("F-box/LRR-repeat protein 15/At3g58940/PEG3-like, LRR domain-containing protein","F-box/LRR-repeat protein 15/PEG3-like LRR domain-containing protein")
        if "Fe-S oxidoreductase, radical SAM domain-containing, TM0948, predicted family protein" in col4:
            col4 = col4.replace("Fe-S oxidoreductase, radical SAM domain-containing, TM0948, predicted family protein","Fe-S oxidoreductase, radical SAM domain-containing protein")
        if "Glycoside hydrolase, family 57, Saci1162, predicted family protein" in col4:
            col4 = col4.replace("Glycoside hydrolase, family 57, Saci1162, predicted family protein","Glycoside hydrolase, family 57 protein")
        if "Glyoxalase At5g48480-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Glyoxalase At5g48480-like, C-terminal domain-containing protein","Glyoxalase-like, C-terminal domain-containing protein")
        if "Glyoxalase At5g48480-like, N-terminal domain-containing protein" in col4:
            col4 = col4.replace("Glyoxalase At5g48480-like, N-terminal domain-containing protein","Glyoxalase-like, N-terminal domain-containing protein")
        if "Dehydrase, ECs4332, predicted family protein" in col4:
            col4 = col4.replace("Dehydrase, ECs4332, predicted family protein","Dehydrase family protein")
        if "Transcription regulator HTH, MJ1545, predicted family protein" in col4:
            col4 = col4.replace("Transcription regulator HTH, MJ1545, predicted family protein","putative transcription regulator HTH family protein")
        if "Transcription regulator, MJ0621, predicted family protein" in col4:
            col4 = col4.replace("Transcription regulator, MJ0621, predicted family protein","putative transcription regulator family protein")
        if "Transcriptional regulator DIP2311-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Transcriptional regulator DIP2311-like, C-terminal domain-containing protein","Transcriptional regulator-like, C-terminal domain-containing protein")
        if "Transcriptional regulator Rv0078-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Transcriptional regulator Rv0078-like, C-terminal domain-containing protein","Transcriptional regulator-like, C-terminal domain-containing protein")
        if "Transcriptional regulatory protein PF0864-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Transcriptional regulatory protein PF0864-like, C-terminal domain-containing protein","Transcriptional regulatory protein-like, C-terminal domain-containing protein")
        if "VapC-like Sll0205 protein, PIN domain-containing protein" in col4:
            col4 = col4.replace("VapC-like Sll0205 protein, PIN domain-containing protein","VapC-like, PIN domain-containing protein")
        if "XACb0070, ribbon-helix-helix domain-containing protein" in col4:
            col4 = col4.replace("XACb0070, ribbon-helix-helix domain-containing protein","ribbon-helix-helix domain-containing protein")
        if "YHR202W-like, N-terminal metallophosphatase domain-containing protein" in col4:
            col4 = col4.replace("YHR202W-like, N-terminal metallophosphatase domain-containing protein","N-terminal metallophosphatase domain-containing protein")
        if "YNR034W-A/EGO2 superfamily protein" in col4:
            col4 = col4.replace("YNR034W-A/EGO2 superfamily protein","EGO2 superfamily protein")
        if "Centrosomal protein of 112 kDa family protein" in col4:
            col4 = col4.replace("Centrosomal protein of 112 kDa family protein","Centrosomal protein family protein")
        if "FLiS export co-chaperone, HP1076 superfamily protein" in col4:
            col4 = col4.replace("FLiS export co-chaperone, HP1076 superfamily protein","FLiS export co-chaperone superfamily protein")
        if "Formate-dependent cytochrome c nitrite reductase, c552 subunit family protein" in col4:
            col4 = col4.replace("Formate-dependent cytochrome c nitrite reductase, c552 subunit family protein","Formate-dependent cytochrome c nitrite reductase subunit family protein")
        if "Immunity MXAN 0049 protein domain-containing protein" in col4:
            col4 = col4.replace("Immunity MXAN 0049 protein domain-containing protein","Immunity domain-containing protein")
        if "Isocitrate dehydrogenase/putative protein TT1725, C-terminal domain superfamily protein" in col4:
            col4 = col4.replace("Isocitrate dehydrogenase/putative protein TT1725, C-terminal domain superfamily protein","putative isocitrate dehydrogenase C-terminal domain superfamily protein")
        if "Isocitrate dehydrogenase/putative protein TT1725, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Isocitrate dehydrogenase/putative protein TT1725, C-terminal domain-containing protein","putative isocitrate dehydrogenase C-terminal domain-containing protein")
        if "J517 1871 lipoprotein-like family protein" in col4:
            col4 = col4.replace("J517 1871 lipoprotein-like family protein","lipoprotein-like family protein")
        if "Lipoprotein DVU 2496-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Lipoprotein DVU 2496-like, C-terminal domain-containing protein","Lipoprotein-like, C-terminal domain-containing protein")
        if "Mannosyltransferase, MA4085, predicted family protein" in col4:
            col4 = col4.replace("Mannosyltransferase, MA4085, predicted family protein","putative mannosyltransferase family protein")
        if "Metallophosphatase TT1561 domain-containing protein" in col4:
            col4 = col4.replace("Metallophosphatase TT1561 domain-containing protein","Metallophosphatase domain-containing protein")
        if "Metallophosphoesterase, TT1561-like domain-containing protein" in col4:
            col4 = col4.replace("Metallophosphoesterase, TT1561-like domain-containing protein","Metallophosphoesterase-like domain-containing protein")
        if "Long-chain fatty acyl-CoA thioesterase, Rv0098-like superfamily protein" in col4:
            col4 = col4.replace("Long-chain fatty acyl-CoA thioesterase, Rv0098-like superfamily protein","Long-chain fatty acyl-CoA thioesterase superfamily protein")
        if "Low temperature-induced all0457 homolog family protein" in col4:
            col4 = col4.replace("Low temperature-induced all0457 homolog family protein","Low temperature-induced homolog family protein")
        if "Mimivirus sulfhydryl oxidase R596-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Mimivirus sulfhydryl oxidase R596-like, C-terminal domain-containing protein","Mimivirus sulfhydryl oxidase C-terminal domain-containing protein")
        if "Mobile element protein CD1107-like domain-containing protein" in col4:
            col4 = col4.replace("Mobile element protein CD1107-like domain-containing protein","Mobile element-like domain-containing protein")
        if "Mth938 domain-containing protein family protein" in col4:
            col4 = col4.replace("Mth938 domain-containing protein family protein","Mth938 family protein")
        if "Non-reducing end beta-L-arabinofuranosidase-like, GH127 C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Non-reducing end beta-L-arabinofuranosidase-like, GH127 C-terminal domain-containing protein","Non-reducing end beta-L-arabinofuranosidase-like C-terminal domain-containing protein")
        if "Non-reducing end beta-L-arabinofuranosidase-like, GH127 catalytic domain-containing protein" in col4:
            col4 = col4.replace("Non-reducing end beta-L-arabinofuranosidase-like, GH127 catalytic domain-containing protein","Non-reducing end beta-L-arabinofuranosidase-like catalytic domain-containing protein")
        if "Non-reducing end beta-L-arabinofuranosidase-like, GH127 middle domain-containing protein" in col4:
            col4 = col4.replace("Non-reducing end beta-L-arabinofuranosidase-like, GH127 middle domain-containing protein","Non-reducing end beta-L-arabinofuranosidase-like middle domain-containing protein")
        if "Nucleic acid binding protein, Rv2694c, predicted family protein" in col4:
            col4 = col4.replace("Nucleic acid binding protein, Rv2694c, predicted family protein","putative nucleic acid binding protein family protein")
        if "Nucleoporin NUP120, helical domain, saccharomycetes domain-containing protein" in col4:
            col4 = col4.replace("Nucleoporin NUP120, helical domain, saccharomycetes domain-containing protein","Nucleoporin NUP120, helical domain-containing protein")
        if "SR140, RNA recognition motif domain-containing protein" in col4:
            col4 = col4.replace("SR140, RNA recognition motif domain-containing protein","SR140-like RNA recognition motif domain-containing protein")
        if "RNA polymerase, 132kDa subunit, poxvirus-type family protein" in col4:
            col4 = col4.replace("RNA polymerase, 132kDa subunit, poxvirus-type family protein","RNA polymerase subunit, poxvirus-type family protein")
        if "S-adenosyl-L-methionine binding protein, YMR209C, predicted family protein" in col4:
            col4 = col4.replace("S-adenosyl-L-methionine binding protein, YMR209C, predicted family protein","S-adenosyl-L-methionine binding protein family protein")
        if "AF2226-like SPOUT RNA methylase fused to THUMP family protein" in col4:
            col4 = col4.replace("AF2226-like SPOUT RNA methylase fused to THUMP family protein","SPOUT RNA methylase fused to THUMP family protein")
        if "BL00235/CARNS1, N-terminal domain-containing protein" in col4:
            col4 = col4.replace("BL00235/CARNS1, N-terminal domain-containing protein","CARNS1, N-terminal domain-containing protein")
        if "Bvu 2165-like, IHF-HU-like DNA-binding domain-containing protein" in col4:
            col4 = col4.replace("Bvu 2165-like, IHF-HU-like DNA-binding domain-containing protein","IHF-HU-like DNA-binding domain-containing protein")
        if "C6orf106, UBA-like domain-containing protein" in col4:
            col4 = col4.replace("C6orf106, UBA-like domain-containing protein","UBA-like domain-containing protein")
        if "C883 1060-like, ketoreductase domain, N-terminal domain-containing protein" in col4:
            col4 = col4.replace("C883 1060-like, ketoreductase domain, N-terminal domain-containing protein","ketoreductase domain, N-terminal domain-containing protein")
        if "C962R-like, N-terminal AEP domain-containing protein" in col4:
            col4 = col4.replace("C962R-like, N-terminal AEP domain-containing protein","N-terminal AEP domain-containing protein")
        if "Ca3427-like, PBP 2 domain-containing protein" in col4:
            col4 = col4.replace("Ca3427-like, PBP 2 domain-containing protein","PBP 2 domain-containing protein")
        if "Calcium binding protein SSO6904 domain-containing protein" in col4:
            col4 = col4.replace("Calcium binding protein SSO6904 domain-containing protein","Calcium binding protein domain-containing protein")
        if "CdiA toxin, EC869-like domain-containing protein" in col4:
            col4 = col4.replace("CdiA toxin, EC869-like domain-containing protein","CdiA toxin domain-containing protein")
        if "CDP-alcohol phosphatidyltransferase AF 2299-like, N-terminal domain-containing protein" in col4:
            col4 = col4.replace("CDP-alcohol phosphatidyltransferase AF 2299-like, N-terminal domain-containing protein","CDP-alcohol phosphatidyltransferase N-terminal domain-containing protein")
        if "CFAP184, CAP-like domain-containing protein" in col4:
            col4 = col4.replace("CFAP184, CAP-like domain-containing protein","CAP-like domain-containing protein")
        if "CFAP184, CBM-like domain-containing protein" in col4:
            col4 = col4.replace("CFAP184, CBM-like domain-containing protein","CBM-like domain-containing protein")
        if "CG11883-like, N-terminal metallophosphatase domain-containing protein" in col4:
            col4 = col4.replace("CG11883-like, N-terminal metallophosphatase domain-containing protein","N-terminal metallophosphatase domain-containing protein")
        if "CGI121/TPRKB superfamily protein" in col4:
            col4 = col4.replace("CGI121/TPRKB superfamily protein","TPRKB superfamily protein")
        if "CGL160/ATPI domain-containing protein" in col4:
            col4 = col4.replace("CGL160/ATPI domain-containing protein","ATPI domain-containing protein")
        if "Conserved hypothetical protein CHP02304, F390 synthetase-related family protein" in col4:
            col4 = col4.replace("Conserved hypothetical protein CHP02304, F390 synthetase-related family protein","putative F390 synthetase-related family protein")
        if "CT398-like coiled coil hairpin domain-containing protein" in col4:
            col4 = col4.replace("CT398-like coiled coil hairpin domain-containing protein","coiled coil hairpin domain-containing protein")
        if "Cthe 2314-like HEPN domain-containing protein" in col4:
            col4 = col4.replace("Cthe 2314-like HEPN domain-containing protein","HEPN domain-containing protein")
        if "Cyclic di-GMP binding protein, PA4608 type family protein" in col4:
            col4 = col4.replace("Cyclic di-GMP binding protein, PA4608 type family protein","Cyclic di-GMP binding protein family protein")
        if "Cyclic di-GMP phosphodiesterase VC 1295-like, MASE10 domain-containing protein" in col4:
            col4 = col4.replace("Cyclic di-GMP phosphodiesterase VC 1295-like, MASE10 domain-containing protein","Cyclic di-GMP phosphodiesterase MASE10 domain-containing protein")
        if "Cyclophilin TM1367-like domain-containing protein" in col4:
            col4 = col4.replace("Cyclophilin TM1367-like domain-containing protein","Cyclophilin-like domain-containing protein")
        if "dehydrogenase DR0790 type, predicted family protein" in col4:
            col4 = col4.replace("dehydrogenase DR0790 type, predicted family protein","putative dehydrogenase family protein")
        if "DNA methylase, N-6 adenine-specific, MK1259 type family protein" in col4:
            col4 = col4.replace("DNA methylase, N-6 adenine-specific, MK1259 type family protein","DNA methylase, N-6 adenine-specific family protein")
        if "DNA-binding protein Rv2175c, wHTH domain-containing protein" in col4:
            col4 = col4.replace("DNA-binding protein Rv2175c, wHTH domain-containing protein","DNA-binding protein wHTH domain-containing protein")
        if "DNA-binding protein, MJ1563 type family protein" in col4:
            col4 = col4.replace("DNA-binding protein, MJ1563 type family protein","DNA-binding protein family protein")
        if "DR2241, 4Fe-4S iron-sulfur cluster binding domain-containing protein" in col4:
            col4 = col4.replace("DR2241, 4Fe-4S iron-sulfur cluster binding domain-containing protein","iron-sulfur cluster binding domain-containing protein")
        if "DRAM/TMEM150 Autophagy Modulator family protein" in col4:
            col4 = col4.replace("DRAM/TMEM150 Autophagy Modulator family protein","Autophagy Modulator family protein")
        if "E217 Baseplate component gp38-like family protein" in col4:
            col4 = col4.replace("E217 Baseplate component gp38-like family protein","Baseplate component gp38-like family protein")
        if "EC042 2821-like Restriction Endonuclease-like domain-containing protein" in col4:
            col4 = col4.replace("EC042 2821-like Restriction Endonuclease-like domain-containing protein","Restriction Endonuclease-like domain-containing protein")
        if "Fervidolysin/DR A0283-like, Ig-like domain-containing protein" in col4:
            col4 = col4.replace("Fervidolysin/DR A0283-like, Ig-like domain-containing protein","Fervidolysin-like, Ig-like domain-containing protein")
        if "Filamin/ABP280 repeat-containing protein" in col4:
            col4 = col4.replace("Filamin/ABP280 repeat-containing protein","Filamin repeat-containing protein")
        if "Filamin/ABP280 repeat-like repeat-containing protein" in col4:
            col4 = col4.replace("Filamin/ABP280 repeat-like repeat-containing protein","Filamin repeat-like repeat-containing protein")
        if "Gfd2/YDR514C-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Gfd2/YDR514C-like, C-terminal domain-containing protein","Gfd2-like, C-terminal domain-containing protein")
        if "CC142, N-terminal domain-containing protein" in col4:
            col4 = col4.replace("CC142, N-terminal domain-containing protein","CC142 coiled coil N-terminal domain-containing protein")
        if "CD180, leucine-rich repeat-containing protein" in col4:
            col4 = col4.replace("CD180, leucine-rich repeat-containing protein","CD180 leucine-rich repeat-containing protein")
        if "CD209-like, C-type lectin-like domain-containing protein" in col4:
            col4 = col4.replace("CD209-like, C-type lectin-like domain-containing protein","CD209-like C-type lectin-like domain-containing protein")
        if "CDI inhibitor, Bp1026b-like domain-containing protein" in col4:
            col4 = col4.replace("CDI inhibitor, Bp1026b-like domain-containing protein","CDI inhibitor-like domain-containing protein")
        if "CDI toxin, Bp1026b-like domain-containing protein" in col4:
            col4 = col4.replace("CDI toxin, Bp1026b-like domain-containing protein","CDI toxin-like domain-containing protein")
        if "Growth-regulating ATPase SCO5717-like, N-terminal domain-containing protein" in col4:
            col4 = col4.replace("Growth-regulating ATPase SCO5717-like, N-terminal domain-containing protein","Growth-regulating ATPase N-terminal domain-containing protein")
        if "H-rev107 Phospholipase/Acyltransferase family protein" in col4:
            col4 = col4.replace("H-rev107 Phospholipase/Acyltransferase family protein","Phospholipase/Acyltransferase family protein")
        if "Histone acetyltransferase Rv0428c-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("Histone acetyltransferase Rv0428c-like, C-terminal domain-containing protein","Histone acetyltransferase C-terminal domain-containing protein")
        if "Histone acetyltransferase Rv0428c-like, SH3 domain-containing protein" in col4:
            col4 = col4.replace("Histone acetyltransferase Rv0428c-like, SH3 domain-containing protein","Histone acetyltransferase SH3 domain-containing protein")
        if "Lpg0393-like, VPS9-like domain-containing protein" in col4:
            col4 = col4.replace("Lpg0393-like, VPS9-like domain-containing protein","VPS9-like domain-containing protein")
        if "Lpg0393, helical bundle domain-containing protein" in col4:
            col4 = col4.replace("Lpg0393, helical bundle domain-containing protein","helical bundle domain-containing protein")
        if "LPG0439, HIT-related domain-containing protein" in col4:
            col4 = col4.replace("LPG0439, HIT-related domain-containing protein","HIT-related domain-containing protein")
        if "MJ0421-like THUMP domain-containing protein" in col4:
            col4 = col4.replace("MJ0421-like THUMP domain-containing protein","THUMP domain-containing protein")
        if "MJ0570, ATP-binding family protein" in col4:
            col4 = col4.replace("MJ0570, ATP-binding family protein","ATP-binding family protein")
        if "MJ1316 RNA cyclic group end recognition domain-containing protein" in col4:
            col4 = col4.replace("MJ1316 RNA cyclic group end recognition domain-containing protein","RNA cyclic group end recognition domain-containing protein")
        if "Phosphoesterase, HI0762, predicted family protein" in col4:
            col4 = col4.replace("Phosphoesterase, HI0762, predicted family protein","putative phosphoesterase family protein")
        if "Phosphomutase MSMEG4193, putative family protein" in col4:
            col4 = col4.replace("Phosphomutase MSMEG4193, putative family protein","putative phosphomutase family protein")
        if "putative 5'-nucleotidase, SA0022 type family protein" in col4:
            col4 = col4.replace("putative 5'-nucleotidase, SA0022 type family protein","putative 5'-nucleotidase family protein")
        if "Putative acyltransferase ACT14924-like, acyltransferase domain-containing protein" in col4:
            col4 = col4.replace("Putative acyltransferase ACT14924-like, acyltransferase domain-containing protein","Putative acyltransferase domain-containing protein")
        if "putative amidinotransferase, FN0238 type family protein" in col4:
            col4 = col4.replace("putative amidinotransferase, FN0238 type family protein","putative amidinotransferase family protein")
        if "putative ATP-binding protein MJ1010-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("putative ATP-binding protein MJ1010-like, C-terminal domain-containing protein","putative ATP-binding protein C-terminal domain-containing protein")
        if "Putative ATP-dependent RNA helicase YLR419W-like, UBA domain-containing protein" in col4:
            col4 = col4.replace("Putative ATP-dependent RNA helicase YLR419W-like, UBA domain-containing protein","Putative ATP-dependent RNA helicase-like, UBA domain-containing protein")
        if "putative glycerophosphotransferase, SA2157 type family protein" in col4:
            col4 = col4.replace("putative glycerophosphotransferase, SA2157 type family protein","putative glycerophosphotransferase family protein")
        if "putative membrane protein Ta0354, soluble domain-containing protein" in col4:
            col4 = col4.replace("putative membrane protein Ta0354, soluble domain-containing protein","putative membrane protein soluble domain-containing protein")
        if "Putative membrane protein, NMB1733 type family protein" in col4:
            col4 = col4.replace("Putative membrane protein, NMB1733 type family protein","Putative membrane protein family protein")
        if "Putative nitroreductase TM1586 domain-containing protein" in col4:
            col4 = col4.replace("Putative nitroreductase TM1586 domain-containing protein","Putative nitroreductase domain-containing protein")
        if "putative phosphoesterase, C1039.02 type family protein" in col4:
            col4 = col4.replace("putative phosphoesterase, C1039.02 type family protein","putative phosphoesterase family protein")
        if "putative phosphoesterase, CT488 type family protein" in col4:
            col4 = col4.replace("putative phosphoesterase, CT488 type family protein","putative phosphoesterase family protein")
        if "putative transcriptional regulator, AF1742 type family protein" in col4:
            col4 = col4.replace("putative transcriptional regulator, AF1742 type family protein","putative transcriptional regulator family protein")
        if "Pyrophosphate-dependent phosphofructokinase SMc01852 type family protein" in col4:
            col4 = col4.replace("Pyrophosphate-dependent phosphofructokinase SMc01852 type family protein","Pyrophosphate-dependent phosphofructokinase family protein")
        if "Pyrophosphate-dependent phosphofructokinase TM0289 type family protein" in col4:
            col4 = col4.replace("Pyrophosphate-dependent phosphofructokinase TM0289 type family protein","Pyrophosphate-dependent phosphofructokinase family protein")
        if "Histidine kinase VP0354-like, sensor domain-containing protein" in col4:
            col4 = col4.replace("Histidine kinase VP0354-like, sensor domain-containing protein","Histidine kinase-like, sensor domain-containing protein")
        if "HTH-type transcriptional regulator MT1864/Rv1816-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("HTH-type transcriptional regulator MT1864/Rv1816-like, C-terminal domain-containing protein","HTH-type transcriptional regulator-like, C-terminal domain-containing protein")
        if "HTH-type transcriptional repressor Sco4008, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("HTH-type transcriptional repressor Sco4008, C-terminal domain-containing protein","HTH-type transcriptional repressor C-terminal domain-containing protein")
        if "HVO 0163, N-terminal HTH domain-containing protein" in col4:
            col4 = col4.replace("HVO 0163, N-terminal HTH domain-containing protein","N-terminal HTH domain-containing protein")
        if "HVO 0234-like, beta-propeller domain-containing protein" in col4:
            col4 = col4.replace("HVO 0234-like, beta-propeller domain-containing protein","beta-propeller domain-containing protein")
        if "HVO 1752, TRASH domain-containing protein" in col4:
            col4 = col4.replace("HVO 1752, TRASH domain-containing protein","TRASH domain-containing protein")
        if "Intraflagellar transport protein 122/121 homolog family protein" in col4:
            col4 = col4.replace("Intraflagellar transport protein 122/121 homolog family protein","Intraflagellar transport protein 122/121-like family protein")
        if "KIAA1045, RING finger domain-containing protein" in col4:
            col4 = col4.replace("KIAA1045, RING finger domain-containing protein","RING finger domain-containing protein")
        if "L544-like, helical domain-containing protein" in col4:
            col4 = col4.replace("L544-like, helical domain-containing protein","helical domain-containing protein")
        if "L544-like, nucleotidyltransferase domain-containing protein" in col4:
            col4 = col4.replace("L544-like, nucleotidyltransferase domain-containing protein","nucleotidyltransferase domain-containing protein")
        if "LA 1612 putative O-antigen biosynthesis protein family protein" in col4:
            col4 = col4.replace("LA 1612 putative O-antigen biosynthesis protein family protein","putative O-antigen biosynthesis protein family protein")
        if "LA2681-like HEPN domain-containing protein" in col4:
            col4 = col4.replace("LA2681-like HEPN domain-containing protein","HEPN domain-containing protein")
        if "MSMEG 0567 GNAT N-acetyltransferase domain-containing protein" in col4:
            col4 = col4.replace("MSMEG 0567 GNAT N-acetyltransferase domain-containing protein","GNAT N-acetyltransferase domain-containing protein")
        if "MSMEG 1276-like, nucleoside triphosphate pyrophosphohydrolase domain-containing protein" in col4:
            col4 = col4.replace("MSMEG 1276-like, nucleoside triphosphate pyrophosphohydrolase domain-containing protein","nucleoside triphosphate pyrophosphohydrolase domain-containing protein")
        if "MSMEG 3727, PQQ-associated family protein" in col4:
            col4 = col4.replace("MSMEG 3727, PQQ-associated family protein","PQQ-associated family protein")
        if "Nuclease, putative, TT1808 superfamily protein" in col4:
            col4 = col4.replace("Nuclease, putative, TT1808 superfamily protein","putative nuclease superfamily protein")
        if "O-GlcNAcase BT 4395-like, post-catalytic domain-containing protein" in col4:
            col4 = col4.replace("O-GlcNAcase BT 4395-like, post-catalytic domain-containing protein","O-GlcNAcase-like, post-catalytic domain-containing protein")
        if "UCP036888, signal transduction HD-GYP-like, PA5346 type family protein" in col4:
            col4 = col4.replace("UCP036888, signal transduction HD-GYP-like, PA5346 type family protein","signal transduction HD-GYP-like family protein")
        if "UPF0224 (FAM112) RNA Processing family protein" in col4:
            col4 = col4.replace("UPF0224 (FAM112) RNA Processing family protein","FAM112 RNA Processing family protein")
        if "UPF0425 pyridoxal phosphate-dependent protein MJ0158-like, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("UPF0425 pyridoxal phosphate-dependent protein MJ0158-like, C-terminal domain-containing protein","pyridoxal phosphate-dependent protein MJ0158-like, C-terminal domain-containing protein")
        if "PA4780 RIO1-like protein kinase family protein" in col4:
            col4 = col4.replace("PA4780 RIO1-like protein kinase family protein","RIO1-like protein kinase family protein")
        if "Pae0151-like, PIN domain-containing protein" in col4:
            col4 = col4.replace("Pae0151-like, PIN domain-containing protein","PIN domain-containing protein")
        if "PAE1087-like, metallophosphatase domain-containing protein" in col4:
            col4 = col4.replace("PAE1087-like, metallophosphatase domain-containing protein","metallophosphatase domain-containing protein")
        if "PAV1-137, bromodomain-like domain-containing protein" in col4:
            col4 = col4.replace("PAV1-137, bromodomain-like domain-containing protein","bromodomain-like domain-containing protein")
        if "Pentatricopeptide repeat-containing protein At4g14850-like, plant family protein" in col4:
            col4 = col4.replace("Pentatricopeptide repeat-containing protein At4g14850-like, plant family protein","Pentatricopeptide repeat-containing protein")
        if "PF0610-like, rubredoxin-like zinc beta-ribbon domain-containing protein" in col4:
            col4 = col4.replace("PF0610-like, rubredoxin-like zinc beta-ribbon domain-containing protein","rubredoxin-like zinc beta-ribbon domain-containing protein")
        if "Pput2613-like deaminase family protein" in col4:
            col4 = col4.replace("Pput2613-like deaminase family protein","deaminase family protein")
        if "RecB family nuclease, TM0106, putative family protein" in col4:
            col4 = col4.replace("RecB family nuclease, TM0106, putative family protein","RecB family nuclease protein")
        if "RNA ligase Pab1020, C-terminal domain-containing protein" in col4:
            col4 = col4.replace("RNA ligase Pab1020, C-terminal domain-containing protein","RNA ligase C-terminal domain-containing protein")
        if "Rnh202, triple barrel domain-containing protein" in col4:
            col4 = col4.replace("Rnh202, triple barrel domain-containing protein","triple barrel domain-containing protein")
        if "RPK118-like, kinase domain-containing protein" in col4:
            col4 = col4.replace("RPK118-like, kinase domain-containing protein","kinase domain-containing protein")
        if "Rv0078B-like antitoxin family protein" in col4:
            col4 = col4.replace("Rv0078B-like antitoxin family protein","antitoxin family protein")
        if "Rv2525c-like, glycoside hydrolase-like domain-containing protein" in col4:
            col4 = col4.replace("Rv2525c-like, glycoside hydrolase-like domain-containing protein","glycoside hydrolase-like domain-containing protein")
        if "Rv2567-like, DUF403 domain-containing protein" in col4:
            col4 = col4.replace("Rv2567-like, DUF403 domain-containing protein","uncharacterized DUF403 domain-containing protein")
        if "SA0022-like, N-terminal metallophosphatase domain-containing protein" in col4:
            col4 = col4.replace("SA0022-like, N-terminal metallophosphatase domain-containing protein","N-terminal metallophosphatase domain-containing protein")
        if "SAV 6107-like HEPN domain-containing protein" in col4:
            col4 = col4.replace("SAV 6107-like HEPN domain-containing protein","HEPN domain-containing protein")
        if "SAV2148-like HEPN domain-containing protein" in col4:
            col4 = col4.replace("SAV2148-like HEPN domain-containing protein","HEPN domain-containing protein")
        if "SCO4226, nickel-binding ferredoxin-like monomer superfamily protein" in col4:
            col4 = col4.replace("SCO4226, nickel-binding ferredoxin-like monomer superfamily protein","nickel-binding ferredoxin-like monomer superfamily protein")
        if "Serine/threonine-protein kinase YKL116C, predicted family protein" in col4:
            col4 = col4.replace("Serine/threonine-protein kinase YKL116C, predicted family protein","Serine/threonine-protein kinase family protein")
        if "Signal transduction histidine kinase, STH3221, predicted family protein" in col4:
            col4 = col4.replace("Signal transduction histidine kinase, STH3221, predicted family protein","Signal transduction histidine kinase family protein")
        if "Small zinc finger protein HVO 2753-like, zinc-binding pocket domain-containing protein" in col4:
            col4 = col4.replace("Small zinc finger protein HVO 2753-like, zinc-binding pocket domain-containing protein","Small zinc finger protein, zinc-binding pocket domain-containing protein")
        if "Mu Gam/Sipho Gp157-like domain of the TOTE conflict system domain-containing protein" in col4:
            col4 = col4.replace("Mu Gam/Sipho Gp157-like domain of the TOTE conflict system domain-containing protein","Mu Gam/Sipho Gp157-like domain-containing protein")
        if "SO 2930-like, beta-helix domain-containing protein" in col4:
            col4 = col4.replace("SO 2930-like, beta-helix domain-containing protein","beta-helix domain-containing protein")
        if "SSO1120-like, N-terminal thioredoxin-like domain-containing protein" in col4:
            col4 = col4.replace("SSO1120-like, N-terminal thioredoxin-like domain-containing protein","N-terminal thioredoxin-like domain-containing protein")
        if "ST1585, MBL-fold domain-containing protein" in col4:
            col4 = col4.replace("ST1585, MBL-fold domain-containing protein","MBL-fold domain-containing protein")
        if "STM3845 retron effector protein family protein" in col4:
            col4 = col4.replace("STM3845 retron effector protein family protein","retron effector protein family protein")
        if "STM4013-like hydrolase family protein" in col4:
            col4 = col4.replace("STM4013-like hydrolase family protein","hydrolase family protein")
        if "STY4199-like HEPN domain-containing protein" in col4:
            col4 = col4.replace("STY4199-like HEPN domain-containing protein","HEPN domain-containing protein")
        if "Subtelomeric hrmA-associated cluster protein AFUB 079030/YDR124W-like, helical bundle domain-containing protein" in col4:
            col4 = col4.replace("Subtelomeric hrmA-associated cluster protein AFUB 079030/YDR124W-like, helical bundle domain-containing protein","Subtelomeric hrmA-associated cluster protein helical bundle domain-containing protein")
        if "Thiol ester hydratase, Rv0216, predicted family protein" in col4:
            col4 = col4.replace("Thiol ester hydratase, Rv0216, predicted family protein","putative thiol ester hydratase family protein")
        if "Tip pilin GBS104-like, Ig-like domain-containing protein" in col4:
            col4 = col4.replace("Tip pilin GBS104-like, Ig-like domain-containing protein","Tip pilin-like, Ig-like domain-containing protein")

        # print line to file
        outfile.write(f"{col1}\t{col2}\t{col3}\t{col4}\n")

# Database identifiers resolved
print("All database identifiers are resolved as well as can be expected")

#####################################################################
#
# Next Remove intermediate files
#
#####################################################################

import os

# List of files to delete
files_to_delete = ['Interpro_to_NCBI_step_1.txt', 'Interpro_to_NCBI_step_2.txt', 'Interpro_to_NCBI_step_3.txt', 'Interpro_to_NCBI_step_4.txt', 'Interpro_to_NCBI_step_5.txt', 'Interpro_to_NCBI_step_6.txt' ]

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
