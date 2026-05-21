#!/bin/bash
#SBATCH --job-name=PMZ_010_jupyter_run
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

# 3. Add the course tools to your PATH so the notebook can find them
export PATH=/lustre1/project/stg_00079/teaching/I0U19a_conda_2026/bin/:$PATH

# 4. Define your directory and navigate directly to it
REPO_DIR="$VSC_DATA/large_omics/r1097686_Pietro_Maria_Zangrando/010_manual_snpcall"

cd $REPO_DIR

# 5. Activate your Conda environment
echo "--- ACTIVATING CONDA ENVIRONMENT ---"
# Make sure this matches the environment you created for the 010 assignment!
# (I adjusted your 030 environment name as a placeholder)
source activate env_large_omics_010_PMZ

# 6. Execute the notebook
echo "--- EXECUTING JUPYTER NOTEBOOK ---"
# This runs the notebook from top to bottom and saves the outputs directly into the file
jupyter nbconvert --to notebook --execute --inplace manual_snp_calling_workflow.ipynb

echo "--- PIPELINE COMPLETE ---"
