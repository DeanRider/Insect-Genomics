'''
make a script to do the following:
start a counter
write the first line of ##gff-version 3 to a file called IproTest.gff3
read lines from Interpro_to_NCBI_list.txt
create an output line with
column 1 = "Fakechrom1"
column 2 = "iproname"
column 3 = "gene"
column 4 = (count*770)+239
column 5 = (count*770)+239+296
column 6 = "."
column 7 = "+"
column 8 = "."
column 9 = "ID=gene.{count}"

create a second output line with
column 1 = "Fakechrom1"
column 2 = "iproname"
column 3 = "CDS"
column 4 = count*200
column 5 = (count*200)+100
column 6 = "."
column 7 = "+"
column 8 = "."
column 9 = "ID=gene.{count}.cds;parent=gene.{count};product=" followed by the content from column four of the line read from Interpro_to_NCBI_list.txt and a newline character

output the two lines to the file called IproTest.gff3
increment the count and continue with reading in the next line of Interpro_to_NCBI.txt
'''


# File: generate_gff3.py

def generate_gff3(input_file="Interpro_to_NCBI.txt", output_file="Ipro_name_test.gff3"):
    count = 1
    with open(output_file, "w") as out_f:
        # Write the GFF3 version header
        out_f.write("##gff-version 3\n")
        
        # Read input lines
        with open(input_file, "r") as in_f:
            for line in in_f:
                fields = line.strip().split("\t")  # assuming tab-delimited input
                if len(fields) < 4:
                    continue  # skip lines that don't have at least 4 columns
                
                start = (count * 770)+248
                end = start + 287
                gene_id = f"gene.{count}"
                product = fields[3].replace(",", "%2C")

                # Gene line
                gene_line = "\t".join([
                    "Fakechrom1", "iproname", "gene", str(start), str(end),
                    ".", "+", ".", f"ID={gene_id}"
                ]) + "\n"

                # CDS line
                cds_line = "\t".join([
                    "Fakechrom1", "iproname", "CDS", str(start), str(end),
                    ".", "+", ".", f"ID={gene_id}.cds;parent={gene_id};product={product}"
                ]) + "\n"

                # Write both lines
                out_f.write(gene_line)
                out_f.write(cds_line)

                count += 1

if __name__ == "__main__":
    generate_gff3()
