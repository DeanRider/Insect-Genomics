This section contains the file Interpro_to_NCBI_list.txt. This file has four columns. The first three are from the original entry.list downloaded from [Interpro](https://www.ebi.ac.uk/interpro/download/) in April 2025. The last column is a new entry that should be compatible with NCBI's table2asn software. 

The list is used to assign names to proteins that have no clear ortholog in a related species or the KEGG database. For example, 'ankyrin repeat-containing protein'. The goal of making this list is so that it handles many discrepancies prior to the creation of a gff3 with protein names, rather than causing a large number of discrepancies in the table2asn run near the end.

Of the ~47,000 entries, about 700 still have troublesome names that cannot be altered in a meaningful way because the domain description is based on genes of unknown function from model organisms. An example is 'At2g29880-like, C-terminal domain-containing protein'. Removal of the 'At2g29880-like' portion leaves the uninformative 'C-terminal domain-containing protein'. Others with functional information were altered to remove references to gene names. An example is where the original 'At2g23090-like, zinc-binding domain' was changed into 'zinc-binding domain-containing protein'.

The original entry list and the scripts to modify the list and create an example gff3 file are in the modify_entry folder. A test case to run with table2asn is in the table2asn_test folder. A command that can be used to run the test case is as follows:
```
./table2asn -M n -J -euk -t Ipro_name_test.sbt -j "[organism=Asbolus verrucosus][gcode=1]" -i Ipro_name_test.fasta -f Ipro_name_test.gff3 -o Ipro_name_test.sqn -Z -locus-tag-prefix V5W00
```
Nearly all discrepancies produced can be ignored, but should be reviewed to give an idea of what might happen in a gff3 dataset for named proteins. The number of errors in the stats should be limited to the project being invalid as the .sbt template contains bogus information on authors, projects and institutions (it is just a demo).
