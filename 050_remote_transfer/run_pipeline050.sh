#!/bin/bash 
#SBATCH --job-name=PMZ_050_snakemake_run
#SBATCH --output=my_run_%j.out 
#SBATCH --error=my_run_%j.err 
#SBATCH --time=01:00:00 
#SBATCH --mem=8G              
#SBATCH --cpus-per-task=4 
#SBATCH --clusters=wice                 
#SBATCH --account=lp_edu_large_omics

echo "--- INITIALIZING JOB ---"
module purge 
module load cluster/wice/batch          

# Add the course tools to your PATH
export PATH=/lustre1/project/stg_00079/teaching/I0U19a_conda_2026/bin/:$PATH

cd /scratch/leuven/381/vsc38184/large_omics/r1097686_Pietro_Maria_Zangrando/050_remote_transfer

echo "--- AUTHENTICATING MANGO ---"
# This allows the compute node to securely use your saved login session
iron auth --non-interactive

echo "--- STARTING DRY RUN ---"
snakemake -n

echo "--- STARTING COMPLETE RUN ---"
snakemake -c 4

echo "--- PIPELINE COMPLETE ---"
