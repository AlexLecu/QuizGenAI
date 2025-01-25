import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_heatmap_from_excel(file_path):
    df = pd.read_excel(file_path)

    df.rename(columns={"Unnamed: 0": "Tool"}, inplace=True)

    df_filtered = df[["Tool", "Alex", "Alex.1", "Average"]].copy()

    df_filtered.columns = ["Tool", "Dimension", "Type", "Average"]

    pivot_df = df_filtered.pivot_table(
        index=["Tool", "Type"],
        columns="Dimension",
        values="Average",
        aggfunc="mean"
    )

    custom_column_names = {
        "Easy": "Level 1",
        "Hard": "Level 3",
        "Context": "Level 2"
    }
    pivot_df.rename(columns=custom_column_names, inplace=True)

    desired_order = ["Level 1", "Level 2", "Level 3"]
    pivot_df = pivot_df.reindex(columns=desired_order)

    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        pivot_df,
        annot=True,
        cmap="YlGnBu",
        fmt=".1f",
        linewidths=0.5
    )

    plt.title("")
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)

    plt.tight_layout()
    plt.show()


file_path = ""
create_heatmap_from_excel(file_path)
