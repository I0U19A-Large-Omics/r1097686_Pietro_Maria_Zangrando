#!/bin/bash 
#SBATCH --job-name=PMZ_030_snakemake_run
#SBATCH --output=my_run_%j.out 
#SBATCH --error=my_run_%j.err 
#SBATCH --time=01:00:00 
#SBATCH --mem=4G              
#SBATCH --cpus-per-task=1 
#SBATCH --clusters=wice                 
#SBATCH --account=lp_edu_large_omics

echo "--- INITIALIZING JOB ---"

# 1. Clear previous modules and load WICE cluster architecture
module purge 
module load cluster/wice/batch          

# 2. Load Conda from the HPC module system
module load Miniconda3

# 3. Add the course tools to your PATH so Snakemake can find BWA/SnpEff/vt/etc.
export PATH=/lustre1/project/stg_00079/teaching/I0U19a_conda_2026/bin/:$PATH

# 4. Define your directories
REPO_DIR="$VSC_DATA/large_omics/r1097686_Pietro_Maria_Zangrando/030_snakemake_snpcalling"
WORK_DIR="$VSC_SCRATCH/large_omics/030_work"

# 5. Navigate to the SCRATCH directory (where outputs will be generated)
cd $WORK_DIR

# 6. Activate your new Conda environment
echo "--- ACTIVATING CONDA ENVIRONMENT ---"
source activate env_large_omics_030_PMZ

# 7. Execute the dry run (pointing -s to the Snakefile in VSC_DATA)
echo "--- STARTING DRY RUN (snakemake -n) ---"
snakemake -s $REPO_DIR/Snakefile -n

# 8. Execute the complete run
echo "--- STARTING COMPLETE RUN (snakemake -c1) ---"
snakemake -s $REPO_DIR/Snakefile -c1

echo "--- PIPELINE COMPLETE ---"
