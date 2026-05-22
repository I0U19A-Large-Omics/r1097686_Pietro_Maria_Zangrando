#!/usr/bin/env python3
import sys
import csv
import time
from multiprocessing import Pool, set_start_method
import vcfpy
from fake_enformer import predict

NOPRO = 40  # 40 processes is a safe number that won't overwhelm the node
CHUNKSIZE = 50 # Process SNPs in chunks of 50 to reduce overhead

def process_snps(snplist):
    """Worker function to predict scores for a chunk of SNPs."""
    rv = []
    for snp in snplist:
        # Appends a dictionary for easy TSV writing later
        rv.append({"coordinate": snp, "score": predict(snp)})
    return rv

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_enformer.py <path_to_vcf>")
        sys.exit(1)

    vcf_path = sys.argv[1]
    output_file = "enformer_results.tsv"

    print(f"Parsing VCF: {vcf_path}...")
    reader = vcfpy.Reader.from_path(vcf_path)
    
    # 1. Extract UNIQUE coordinates using a set
    unique_snps = set()
    for record in reader:
        # Some records might have multiple alternate alleles
        for alt in record.ALT:
            # Format expected by fake_enformer based on prof's script
            snp_name = f"hg38:{record.CHROM}:{record.POS}:{record.REF}:{alt.value}"
            unique_snps.add(snp_name)
    
    unique_snps = list(unique_snps)
    print(f"Found {len(unique_snps)} unique SNPs to process.")

    # 2. Chunk the data for the multiprocessing Pool
    # This creates a list of lists (each sublist is length CHUNKSIZE)
    ALLSNPS = [unique_snps[i:i + CHUNKSIZE] for i in range(0, len(unique_snps), CHUNKSIZE)]

    print(f"Starting multiprocessing pool with {NOPRO} workers...")
    start_time = time.time()
    
    # 3. Execute concurrently
    # set_start_method('fork') used in example script for Unix systems
    try:
        set_start_method('fork')
    except RuntimeError:
        pass # Prevents crash if context is already set
        
    with Pool(NOPRO) as P:
        # map returns a list of lists because our worker returns a list of dicts
        all_results_nested = P.map(process_snps, ALLSNPS)
    
    end_time = time.time()

    # Flatten the nested list into a single list of dictionaries
    flat_results = [item for sublist in all_results_nested for item in sublist]

    # 4. Write to TSV
    print(f"Writing results to {output_file}...")
    with open(output_file, 'w', newline='') as tsvfile:
        writer = csv.DictWriter(tsvfile, fieldnames=["coordinate", "score"], delimiter='\t')
        writer.writeheader()
        writer.writerows(flat_results)

    total_time = end_time - start_time
    print(f"Done! Processed {len(flat_results)} SNPs in {total_time:.2f} seconds.")
    print("Approach: Multiprocessing Pool with chunking to bypass artificial I/O sleep latency.")

if __name__ == "__main__":
    main()
