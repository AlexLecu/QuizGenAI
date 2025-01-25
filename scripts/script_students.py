import pandas as pd
import matplotlib.pyplot as plt

PATH = ""

survey_data = pd.read_excel(PATH)

data_no_text = survey_data.drop(columns=["Text"])

data_no_text.set_index("Question", inplace=True)

data_no_text["Total_Answers"] = data_no_text.sum(axis=1)

level_mapping = {
    "Q1": "Level 1", "Q2": "Level 1", "Q3": "Level 1",
    "Q4": "Level 2", "Q5": "Level 2", "Q6": "Level 2",
    "Q7": "Level 3", "Q8": "Level 3", "Q9": "Level 3"
}

levels = [level_mapping[q] for q in data_no_text.index]

grouped_labels = ["Level 1", "Level 2", "Level 3"]
question_groups = [["Q1", "Q2", "Q3"], ["Q4", "Q5", "Q6"], ["Q7", "Q8", "Q9"]]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(
    data_no_text.index,
    data_no_text["Total_Answers"],
    color=["skyblue" if level == "Level 1" else "lightgreen" if level == "Level 2" else "salmon" for level in levels],
    edgecolor="black"
)

plt.title("")
plt.xlabel("")
plt.ylabel("Total Correct Answers", fontsize=14)
plt.yticks(fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)

ax.set_xticks(range(len(data_no_text.index)))
ax.set_xticklabels(data_no_text.index, fontsize=12, rotation=0)

for group_idx, (group, label) in enumerate(zip(question_groups, grouped_labels)):
    group_start = data_no_text.index.tolist().index(group[0])
    group_end = data_no_text.index.tolist().index(group[-1])
    group_center = (group_start + group_end) / 2
    ax.text(
        group_center, -0.8,
        label,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold"
    )

plt.tight_layout()
plt.show()



