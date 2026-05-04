import sys
import vcfpy
import pandas as pd
import sqlite3

# Get the input VCF and output DB paths from the command line
input_vcf = sys.argv[1]
output_db = sys.argv[2]

# Open the VCF file using vcfpy
reader = vcfpy.Reader.from_path(input_vcf)

snp_data = []
effect_data = []
call_data = []

# Counters to act as our unique IDs
snp_id_counter = 1
effect_id_counter = 1
call_id_counter = 1

for record in reader:
    # 1. Standardize ALT alleles into a single comma-separated string
    alts = ",".join([alt.value if hasattr(alt, 'value') else str(alt) for alt in record.ALT])

    # 2. Add the row to our SNP list
    snp_data.append({
        'snp_id': snp_id_counter,
        'chrom': record.CHROM,
        'pos': record.POS,
        'ref': record.REF,
        'alt': alts,
        'qual': record.QUAL
    })

    # 3. Process the Calls (Genotypes)
    for call in record.calls:
        # Extract the Genotype (GT). If missing, default to './.'
        gt = call.data.get('GT', './.')

        call_data.append({
            'call_id': call_id_counter,
            'snp_id': snp_id_counter,  # This links back to the SNP table!
            'sample': call.sample,
            'genotype': gt
        })
        call_id_counter += 1

    # 4. Process the Effects (Annotations)
    ann_list = record.INFO.get('ANN', [])
    for ann in ann_list:
        # Split the string by the pipe character
        parts = ann.split('|')
        
        # Safety check: Pad the list with empty strings just in case 
        # a specific annotation is missing some of the 16 fields
        parts += [''] * (16 - len(parts))
        
        effect_data.append({
            'effect_id': effect_id_counter,
            'snp_id': snp_id_counter, # Links back to the SNP table!
            'allele': parts[0],
            'annotation': parts[1],
            'impact': parts[2],
            'gene_name': parts[3],
            'gene_id': parts[4],
            'feature_type': parts[5],
            'transcript_biotype': parts[7],
            'hgvs_c': parts[9],
            'hgvs_p': parts[10],
            'errors_warnings': parts[15]
        })
        effect_id_counter += 1

    # Before moving to the next VCF record, increment the SNP ID!
    snp_id_counter += 1

# Convert lists to DataFrames
df_snp = pd.DataFrame(snp_data)
df_effect = pd.DataFrame(effect_data)
df_call = pd.DataFrame(call_data)

# Connect to SQLite (this creates the file if it doesn't exist)
conn = sqlite3.connect(output_db)

# Write to the database. if_exists='replace' prevents errors if you rerun it.
df_snp.to_sql('SNP', conn, if_exists='replace', index=False)
df_effect.to_sql('Effect', conn, if_exists='replace', index=False)
df_call.to_sql('Call', conn, if_exists='replace', index=False)

conn.close()
print(f"Successfully loaded {len(df_snp)} SNPs into {output_db}")
