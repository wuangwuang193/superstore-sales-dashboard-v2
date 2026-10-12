import pandas as pd


def apply_filters(
    df,
    year=None,
    region=None,
    category=None,
    segment=None
):

    filtered_df = df.copy()

    if year is not None and year != "All":
        filtered_df = filtered_df[
            filtered_df["Year"] == year
        ]

    if region is not None and region != "All":
        filtered_df = filtered_df[
            filtered_df["Region"] == region
        ]

    if category is not None and category != "All":
        filtered_df = filtered_df[
            filtered_df["Category"] == category
        ]

    if segment is not None and segment != "All":
        filtered_df = filtered_df[
            filtered_df["Segment"] == segment
        ]

    return filtered_df