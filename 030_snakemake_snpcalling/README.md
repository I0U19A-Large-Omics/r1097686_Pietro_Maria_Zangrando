1. Open an interactive session on the VSC cluster.
2. Export the conda environment path:
   `export PATH=/lustre1/project/stg_00079/teaching/I0U19a_conda_2026/bin/:$PATH`
3. Navigate to your scratch work folder where the input FASTQ files are located:
   `cd /scratch/leuven/381/vsc38184/large_omics/`
4. Execute the workflow by pointing to the Snakefile:
   `snakemake --snakefile /data/leuven/381/vsc38184/large_omics/r1097686_Pietro_Maria_Zangrando/030_snakemake_snpcalling/Snakefile -c 4`
5. Look for the final results in the `100.final/` directory within your scratch folder.
