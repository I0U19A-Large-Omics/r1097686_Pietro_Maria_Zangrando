import sys
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    if len(sys.argv) != 4:
        print("Usage: python visualize_snps.py <db_path> <fig1_out> <fig2_out>")
        sys.exit(1)

    db_path = sys.argv[1]
    fig1_path = sys.argv[2]
    fig2_path = sys.argv[3]

    # Ensure output directory exists
    os.makedirs(os.path.dirname(fig1_path), exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(db_path)

    # ---------------------------------------------------------
    # Figure 1: SNP impact severity per sample
    # ---------------------------------------------------------
    query1 = """
    SELECT c.sample, e.impact, COUNT(DISTINCT s.snp_id) as snp_count
    FROM SNP s
    JOIN Effect e ON s.snp_id = e.snp_id
    JOIN Call c ON s.snp_id = c.snp_id
    GROUP BY c.sample, e.impact
    """
    df1 = pd.read_sql_query(query1, conn)

    # Enforce specific order for impact categories
    impact_order = ["HIGH", "MODERATE", "LOW", "MODIFIER"]
    df1['impact'] = pd.Categorical(df1['impact'], categories=impact_order, ordered=True)

    plt.figure(figsize=(8, 6))
    # Using a colorblind safe palette (colorblind)
    sns.barplot(data=df1, x='impact', y='snp_count', hue='sample', palette='colorblind')
    
    plt.title('SNP Impact Severity Per Sample', fontsize=14)
    plt.xlabel('Impact Category', fontsize=12)
    plt.ylabel('Distinct SNP Count', fontsize=12)
    plt.ylim(bottom=0) # Proportional ink principle: y-axis must start at zero
    plt.legend(title='Sample')
    
    plt.tight_layout()
    plt.savefig(fig1_path, format='svg')
    plt.close()

    # ---------------------------------------------------------
    # Figure 2: Quality score distribution across impact categories
    # Justification: A boxplot helps reveal if HIGH impact variants have systematically lower quality scores, which could indicate false positive biases in severe calls.
    # ---------------------------------------------------------
    query2 = """
    SELECT e.impact, s.qual
    FROM SNP s
    JOIN Effect e ON s.snp_id = e.snp_id
    WHERE s.qual IS NOT NULL
    """
    df2 = pd.read_sql_query(query2, conn)
    df2['impact'] = pd.Categorical(df2['impact'], categories=impact_order, ordered=True)

    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df2, x='impact', y='qual', hue='impact', palette='colorblind', legend=False)
    
    plt.title('Distribution of SNP Quality Scores Across Impact Categories', fontsize=14)
    plt.xlabel('Impact Category', fontsize=12)
    plt.ylabel('SNP Quality Score', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(fig2_path, format='svg')
    plt.close()

    conn.close()

if __name__ == "__main__":
    main()
