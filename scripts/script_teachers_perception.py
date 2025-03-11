import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap
import numpy as np

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

vmin = min(pivot_df_1.min().min(), pivot_df_2.min().min(), pivot_df_3.min().min())
vmax = max(pivot_df_1.max().max(), pivot_df_2.max().max(), pivot_df_3.max().max())

fig = plt.figure(figsize=(25, 8))
gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 0.05], wspace=0)

axes = [fig.add_subplot(gs[0, i]) for i in range(3)]
cbar_ax = fig.add_subplot(gs[0, 3])

sns.heatmap(
    pivot_df_1,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar=False,
    ax=axes[0],
    vmin=vmin, vmax=vmax,
    annot_kws={"size": 14}
)
axes[0].set_title("Copilot", fontsize=18)
axes[0].set_xlabel("")
axes[0].set_ylabel("")

wrapped_labels = ['\n'.join(textwrap.wrap(label, width=25)) for label in pivot_df_1.index]
axes[0].set_yticklabels(wrapped_labels, rotation=0)
axes[0].tick_params(axis='y', labelsize=14)
axes[0].tick_params(axis='x', labelsize=14)

sns.heatmap(
    pivot_df_2,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar=False,
    ax=axes[1],
    vmin=vmin, vmax=vmax,
    annot_kws={"size": 14}
)
axes[1].set_title("GPT", fontsize=18)
axes[1].set_xlabel("")
axes[1].set_ylabel("")
axes[1].set_yticks([])
axes[1].tick_params(axis='x', labelsize=14)

sns.heatmap(
    pivot_df_3,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar=True,
    cbar_ax=cbar_ax,
    ax=axes[2],
    vmin=vmin, vmax=vmax,
    annot_kws={"size": 14}
)
axes[2].set_title("Claude", fontsize=18)
axes[2].set_xlabel("")
axes[2].set_ylabel("")
axes[2].set_yticks([])
axes[2].tick_params(axis='x', labelsize=14)

cbar = axes[2].collections[0].colorbar
cbar.ax.tick_params(labelsize=14)

plt.tight_layout(w_pad=0)

plt.show()
