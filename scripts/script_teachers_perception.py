import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_path_1 = "../data/Teachers/teachers_perception_copilot.xlsx"
data_path_2 = "../data/Teachers/teachers_perception_gpt.xlsx"
data_path_3 = "../data/Teachers/teachers_perception_claude.xlsx"

def process_excel(file_path):
    df = pd.read_excel(file_path, index_col=0)
    df.index.name = "Question"

    aggregated_data = {
        "Easy": df[[col for col in df.columns if col.startswith("Easy")]].mean(axis=1),
        "Context": df[[col for col in df.columns if col.startswith("Context")]].mean(axis=1),
        "Hard": df[[col for col in df.columns if col.startswith("Hard")]].mean(axis=1),
    }

    df_aggregated = pd.DataFrame(aggregated_data)

    df_melt = df_aggregated.reset_index().melt(
        id_vars="Question",
        var_name="Dimension",
        value_name="Average Response"
    )

    pivot_df = df_melt.pivot(
        index="Question",
        columns="Dimension",
        values="Average Response"
    )

    pivot_df = pivot_df.reindex(
        index=df_aggregated.index,
        columns=["Easy", "Context", "Hard"]
    )

    custom_column_names = {
        "Easy": "Level 1",
        "Hard": "Level 3",
        "Context": "Level 2"
    }
    pivot_df.rename(columns=custom_column_names, inplace=True)

    desired_order = ["Level 1", "Level 2", "Level 3"]
    pivot_df = pivot_df.reindex(columns=desired_order)

    return pivot_df

pivot_df_1 = process_excel(data_path_1)
pivot_df_2 = process_excel(data_path_2)
pivot_df_3 = process_excel(data_path_3)

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(24, 8))

vmin = min(pivot_df_1.min().min(), pivot_df_2.min().min(), pivot_df_3.min().min())
vmax = max(pivot_df_1.max().max(), pivot_df_2.max().max(), pivot_df_3.max().max())

sns.heatmap(
    pivot_df_1,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar=False,
    ax=axes[0],
    vmin=vmin, vmax=vmax
)
axes[0].set_title("Copilot", fontsize=14)
axes[0].set_xlabel("")
axes[0].set_ylabel("")
axes[0].set_aspect("equal")

sns.heatmap(
    pivot_df_2,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar=False,
    ax=axes[1],
    vmin=vmin, vmax=vmax
)
axes[1].set_title("GPT", fontsize=14)
axes[1].set_xlabel("")
axes[1].set_ylabel("")
axes[1].set_yticks([])
axes[1].set_aspect("equal")

sns.heatmap(
    pivot_df_3,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar=True,
    ax=axes[2],
    vmin=vmin, vmax=vmax
)
axes[2].set_title("Claude", fontsize=14)
axes[2].set_xlabel("")
axes[2].set_ylabel("")
axes[2].set_yticks([])
axes[2].set_aspect("equal")

plt.subplots_adjust(wspace=0)

plt.tight_layout()
plt.show()
