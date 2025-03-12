import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap


def clean_response(raw_value):
    if not isinstance(raw_value, str) or not raw_value.strip():
        return "No response"

    val = raw_value.strip().lower()

    val = (
        val.replace("stronlgy", "strongly")
           .replace("agre", "agree")
           .replace("dissagree", "disagree")
    )

    if "strongly disagree" in val:
        return "Strongly disagree"
    elif "disagree" in val and "strongly" not in val:
        return "Disagree"
    elif "neutral" in val:
        return "Neutral"
    elif "strongly agree" in val:
        return "Strongly agree"
    elif "agree" in val:
        return "Agree"
    else:
        return "No response"


def visualize_likert_survey(
    excel_file_path,
    sheet_name=None,
    keywords_for_questions=None,
    expected_respondents=None,
    drop_zero_columns=True
):

    if sheet_name:
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    else:
        df = pd.read_excel(excel_file_path)

    if keywords_for_questions is None:
        keywords_for_questions = ["PEoU", "PU", "A", "BI", "AU"]

    question_cols = [
        col for col in df.columns if any(col.startswith(keyword) for keyword in keywords_for_questions)
    ]

    df_filtered = df[question_cols].copy()

    df_filtered.rename(
        columns={col: col.split('.')[0] for col in question_cols}, inplace=True
    )
    original_question_order = df_filtered.columns.tolist()

    for col in df_filtered.columns:
        df_filtered[col] = df_filtered[col].apply(clean_response)

    df_melt = df_filtered.reset_index(drop=True).melt(
        var_name="Question",
        value_name="Response"
    )

    grouped = df_melt.groupby(["Question", "Response"]).size().reset_index(name="Count")
    pivot_df = grouped.pivot_table(
        index="Question",
        columns="Response",
        values="Count",
        fill_value=0
    )

    likert_scale = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
    pivot_df = pivot_df.reindex(columns=likert_scale, fill_value=0)

    pivot_df = pivot_df.reindex(index=original_question_order)

    if drop_zero_columns:
        pivot_df = pivot_df.loc[:, pivot_df.sum(axis=0) != 0]

    if expected_respondents is not None:
        sums_per_question = pivot_df.sum(axis=1)
        for question, total in sums_per_question.items():
            if total != expected_respondents:
                print(f"[WARNING] '{question}' has {total} total responses, expected {expected_respondents}.")

    sns.set_style("whitegrid")
    sns.set_context("talk")
    custom_colors = [
        "#d73027",
        "#fc8d59",
        "#ffffbf",
        "#91cf60",
        "#1a9850"
    ]
    cmap = ListedColormap(custom_colors[: pivot_df.shape[1]])

    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_df.plot(kind="bar", stacked=True, colormap=cmap, edgecolor="none", ax=ax)

    plt.title("")
    plt.xlabel("")
    plt.ylabel("Number of Responses")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Response", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    excel_path = "../data/Teachers/teachers_tam.xlsx"

    visualize_likert_survey(
        excel_file_path=excel_path,
        keywords_for_questions=["PEoU", "PU", "A", "BI", "AU"],
        expected_respondents=5,
        drop_zero_columns=True
    )
