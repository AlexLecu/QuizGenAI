import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

PATH = "../data/Students/students_perception_copilot.xlsx"
# PATH = "../data/Students/students_perception_gpt.xlsx"
# PATH = "../data/Students/students_perception_claude.xlsx"

df = pd.read_excel(
    PATH,
    index_col=0
)
df.index.name = "Question"

relevant_cols = [
    col for col in df.columns
    if col.startswith("Easy") or col.startswith("Context") or col.startswith("Hard")
]

df_melt = df[relevant_cols].melt(
    ignore_index=False,
    var_name="DimensionCol",
    value_name="Response"
)

def classify_dimension(col_name):
    if col_name.startswith("Easy"):
        return "Easy"
    elif col_name.startswith("Context"):
        return "Context"
    elif col_name.startswith("Hard"):
        return "Hard"
    else:
        return "Other"


df_melt["Dimension"] = df_melt["DimensionCol"].apply(classify_dimension)

counts = (
    df_melt
    .groupby([df_melt.index, "Dimension", "Response"])
    .size()
    .reset_index(name="Count")
)

pivot_df = counts.pivot_table(
    index="Question",
    columns=["Dimension", "Response"],
    values="Count",
    fill_value=0
)

likert_order = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
dimension_order = ["Easy", "Context", "Hard"]

ordered_cols = [
    (dim, resp)
    for dim in dimension_order
    for resp in likert_order
]
pivot_df = pivot_df.reindex(
    columns=pd.MultiIndex.from_tuples(ordered_cols, names=["Dimension", "Response"]),
    fill_value=0
)

padded_data = {}
for dim in dimension_order:
    sub_df = pivot_df[dim]
    sub_df = sub_df.reindex(index=pivot_df.index, columns=likert_order, fill_value=0)
    padded_data[dim] = sub_df

fig, axes = plt.subplots(
    nrows=1,
    ncols=3,
    figsize=(14, 5),
    sharey=True,
    gridspec_kw={"wspace": 0.02}
)
sns.set_style("whitegrid")

max_count = pivot_df.values.max()
norm = mcolors.Normalize(vmin=0, vmax=max_count)
cmap = "Blues"

for i, dim in enumerate(dimension_order):
    ax = axes[i]
    sub_df = padded_data[dim]

    sns.heatmap(
        sub_df,
        annot=True,
        fmt=".0f",
        cmap=cmap,
        norm=norm,
        ax=ax,
        cbar=False,
        linewidths=1,
        linecolor="white"
    )

    ax.tick_params(axis="y", labelsize=14)
    ax.tick_params(axis="x", labelsize=14)

    ax.set_aspect("equal", adjustable="box")

    ax.set_title(f"Level {i + 1}", fontsize=14)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])
cbar = fig.colorbar(sm, ax=axes, orientation="vertical", fraction=0.02, pad=0.02)
cbar.set_label("Count", fontsize=12)

plt.tight_layout()
plt.show()


