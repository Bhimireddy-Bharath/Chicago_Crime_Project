"""
Chicago Crime Analysis
USE CASE - 3

Objective:
Perform numerical and visual analysis to identify
patterns and deeper insights from crime data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# ---------------------------------------------------------
# DATASET LOCATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
CSV_FILE = BASE_DIR / "dataset" / "chicago_crime_cleaned.csv"


# ---------------------------------------------------------
# DISPLAY FUNCTIONS
# ---------------------------------------------------------

def show_title(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def show_section(text):
    print("\n" + text)
    print("-" * 70)


# ---------------------------------------------------------
# LOAD AND PREPARE DATA
# ---------------------------------------------------------

def load_crime_data():

    data = pd.read_csv(CSV_FILE)

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    data["Hour"] = data["date"].dt.hour

    print("Cleaned Chicago Crime Dataset loaded successfully.")

    return data


# =========================================================
# 1. CRIME INTENSITY BY TIME
# =========================================================

def analyze_hourly_crimes(data):
    show_title("1. CRIME INTENSITY BY TIME")
    show_section("1.1 HOURLY CRIME DISTRIBUTION")
    hourly_count = (
        data["Hour"]
        .value_counts()
        .sort_index()
    )
    print(hourly_count.to_string())

    show_section("1.2 LINE PLOT OF CRIMES PER HOUR OF DAY")

    hours = hourly_count.index
    counts = hourly_count.values

    plt.figure(figsize=(9, 5))

    plt.plot(
        hours,
        counts,
        marker="o",
        color="green"
    )

    plt.title("Number of Crimes by Hour of Day")
    plt.xlabel("Hour")
    plt.ylabel("Crime Count")
    plt.xticks(range(24))
    plt.grid()

    plt.tight_layout()
    plt.show()


# =========================================================
# 2. COMMUNITY AREA ANALYSIS
# =========================================================

def analyze_community_crimes(data):

    show_title("2. COMMUNITY AREA CLUSTERS USING NUMPY")

    community_counts = (
        data.loc[data["community_code"].notna()]
        .groupby("community_code")
        .size()
    )

    crime_values = community_counts.to_numpy()

    # -----------------------------------------------------
    # Mean
    # -----------------------------------------------------

    show_section("2.1 MEAN CRIME PER COMMUNITY AREA")

    average = np.mean(crime_values)

    print(
        f"Mean crime per community area: {average:.2f}"
    )

    # -----------------------------------------------------
    # IQR Outlier Analysis
    # -----------------------------------------------------

    show_section("2.2 EXTREME OUTLIERS USING IQR METHOD")
    quartiles = np.percentile(
        crime_values,
        [25, 75]
    )
    first_quartile = quartiles[0]
    third_quartile = quartiles[1]
    spread = third_quartile - first_quartile
    minimum_limit = first_quartile - (1.5 * spread)
    maximum_limit = third_quartile + (1.5 * spread)
    unusual_areas = community_counts[
        (community_counts < minimum_limit) |
        (community_counts > maximum_limit)
    ]
    print(f"Q1: {first_quartile:.2f}")
    print(f"Q3: {third_quartile:.2f}")
    print(f"IQR: {spread:.2f}")
    print(f"Lower fence: {minimum_limit:.2f}")
    print(f"Upper fence: {maximum_limit:.2f}")
    print("\nOutlier community areas:")
    print(unusual_areas.to_string())

    # -----------------------------------------------------
    # Box Plot
    # -----------------------------------------------------

    plt.figure(figsize=(8, 6))
    plt.boxplot(
        crime_values,
        vert=True
    )
    plt.title("Crime Count per Community Area")
    plt.ylabel("Crime Count")
    plt.xticks(
        [1],
        ["All Community Areas"])
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()
# =========================================================
# 3. CRIME CROSS-CORRELATION
# =========================================================

def calculate_correlations(data):
    show_title("3. CRIME CROSS-CORRELATION")
    # Convert arrest values to integers
    data["arrest_int"] = (data["arrest"].astype(int))
    selected_features = [ "Year", "Month", "Hour",
                          "beat_num", "district_code", "ward_no",
                          "community_code", "latitude", "longitude",
                          "arrest_int"
                        ]

    show_section("3.1 CORRELATION OF NUMERIC FEATURES")
    correlation_table = (data[selected_features].corr())
    print(correlation_table.round(2).to_string())
    
    show_section("3.2 CORRELATION MATRIX WITH HEATMAP")
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        correlation_table,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0
    )
    plt.title( "Correlation Matrix of Crime Features")
    plt.tight_layout()
    plt.show()


# =========================================================
# MAIN PROGRAM
# =========================================================

def run_use_case():

    show_title("USE CASE 3")

    crime_data = load_crime_data()

    analyze_hourly_crimes(crime_data)

    analyze_community_crimes(crime_data)

    calculate_correlations(crime_data)

    show_title("USE CASE 3 IS COMPLETED")


# ---------------------------------------------------------
# PROGRAM START
# ---------------------------------------------------------

if __name__ == "__main__":
    run_use_case()
