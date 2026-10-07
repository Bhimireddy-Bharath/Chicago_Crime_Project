"""
Chicago Crime Capstone Project
USE CASE 2 - Crime Trend and Pattern Analysis
"""

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Get the project folder
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Locate the community CSV dynamically
community_file = os.path.join(
    project_path,
    "dataset",
    "chicago_city_community.csv"
)

community_df = pd.read_csv(community_file)

# ------------------------------------------------------------
# FILE LOCATION
# ------------------------------------------------------------

BASE_PATH = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_PATH / "dataset" / "chicago_crime_cleaned.csv"

from pathlib import Path

def find_dataset_file(filename):
    current = Path.cwd()

    # Check current folder and its parent folders
    for folder in [current] + list(current.parents):
        file_path = folder / "dataset" / filename

        if file_path.exists():
            return file_path

    raise FileNotFoundError(
        f"{filename} was not found in the project dataset folder."
    )
# ------------------------------------------------------------
# OUTPUT FORMATTING
# ------------------------------------------------------------

def print_title(text):
    print("\n" + "*" * 70)
    print(text)
    print("*" * 70)


def print_task(number, text):
    print(f"\n{number} {text}")
    print("-" * 70)


# ------------------------------------------------------------
# COMMON GRAPH FUNCTION
# ------------------------------------------------------------

def display_graph(x, y, title, x_label, y_label,
                  graph_type="line"):

    plt.figure(figsize=(10, 5))

    if graph_type == "line":
        plt.plot(x, y, marker="o")
    else:
        plt.bar(x, y)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45, ha="right")
    plt.grid()
    plt.tight_layout()
    plt.show()


# ============================================================
# 1. CRIME TREND OVER YEARS
# ============================================================

def analyze_yearly_crimes(data):
    print_title("1. CRIME TREND OVER YEARS")
    print_task("1.1","PLOT TOTAL NUMBER OF CRIMES PER YEAR")
    yearly_count =(data.groupby("Year").size().sort_index())
    print(yearly_count.to_string())
    display_graph(yearly_count.index, yearly_count.values,
        "Total Number of Crimes per Year", "Year",
        "Number of Crimes")
    print_task("1.2",
        "VISUAL INTERPRETATION : IS CRIME RATE RISING OR DECREASING ?" )
    # Calculate the slope of the yearly crime trend
    years = yearly_count.index.to_numpy()
    crime_values = yearly_count.values
    slope = np.polyfit(years, crime_values, 1)[0]
    if slope > 0:
        print("Overall crime trend is rising.")
    elif slope < 0:
        print("Overall crime trend is decreasing.")
    else:
        print("Overall crime trend is stable.")

# ============================================================
# 2. CRIME DISTRIBUTION BY CATEGORY
# ============================================================

def study_crime_categories(data):
    print_title("2. CRIME DISTRIBUTION BY CATEGORY")
    crime_frequency = (data["primary_type"].value_counts())
    highest_ten = crime_frequency.iloc[:10]
    print_task( "2.1","BAR CHART TOP 10 CRIME CATEGORIES (PRIMARY TYPE)")
    print(highest_ten.to_string())
    display_graph(highest_ten.index,highest_ten.values,
        "Top 10 Crime Categories","Primary Type",
        "Crime Count",graph_type="bar")
    print_task("2.2","CALCULATE COUNTS AND PERCENTAGE FOR EACH")
    percentage_values = (crime_frequency.div(len(data))
        .mul(100).round(2))
    category_summary = pd.concat(
        [
        crime_frequency.rename("Count"),percentage_values.rename("Percentage")
        ],axis=1)
    print(category_summary.to_string())


# ============================================================
# 3. ARREST ANALYSIS
# ============================================================

def examine_arrests(data):
    print_title("3. ARRESTS AND CRIME OUTCOMES")
    arrest_values = data["arrest"]
    arrest_percentage = (arrest_values.sum()/ len(arrest_values)* 100)
    print_task("3.1","WHAT PERCENTAGE OF CRIME RESULTS IN ARREST?")
    print(f"Arrest percentage: {arrest_percentage:.2f}%")

    print_task("3.2","DISPLAY ARREST PERCENTAGE")
    print(f"arrest_rate = {arrest_percentage:.2f}%")


# ============================================================
# 4. MONTH AND DAY ANALYSIS
# ============================================================

def create_crime_heatmap(data):
    print_title("4. HEATMAP OF CRIME BY MONTH AND DAY OF WEEK")
    print_task( "4.1","USE SEABORN HEATMAP OF CRIME FREQUENCY "
        "PIVOTED BY MONTH VS DAYOFWEEK")
# Support either spelling used by the cleaned dataset
    if "DayOfWeek" in data.columns:
        weekday_column = "DayOfWeek"
    else:
        weekday_column = "Dayofweek"
    weekday_order = [ "Monday", "Tuesday", "Wednesday",
                      "Thursday", "Friday","Saturday","Sunday"]
    month_day_table = pd.crosstab(data["Month"],data[weekday_column])
    month_day_table = month_day_table.reindex( columns=weekday_order,
        fill_value=0)
    print(month_day_table.to_string())
    plt.figure(figsize=(10, 6))
    sns.heatmap(month_day_table,annot=True,fmt="d", cmap="YlGnBu")
    plt.title("Crime by Month and Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Month")
    plt.tight_layout()
    plt.show()


# ============================================================
# 5. COMMUNITY AREA ANALYSIS
# ============================================================
def community_analysis(df):
    print("\n" + "=" * 70)
    print("COMMUNITY AREA ANALYSIS")
    print("=" * 70)
    # Find community CSV without using an absolute path
    community_file = find_dataset_file("chicago_city_community.csv")
    community_df = pd.read_csv(community_file)
    print("\nAvailable columns:")
    print(community_df.columns.tolist())
    # Select required columns
    community_df = community_df[["community_code", "community_name"]].copy()
    # Convert codes to numeric
    df["community_code"] = pd.to_numeric(df["community_code"],errors="coerce")
    community_df["community_code"] = pd.to_numeric(community_df["community_code"],
        errors="coerce")
    # Add community names to crime data
    merged_df = df.merge(community_df,on="community_code",how="left")
    # Top 10 communities
    top_10 = (merged_df.groupby("community_name").size()
        .sort_values(ascending=False).head(10))
    print("\nTop 10 Community Areas:")
    print(top_10)
    # Graph
    plt.figure(figsize=(12, 6))
    top_10.sort_values().plot(kind="barh")
    plt.title("Top 10 Community Areas by Number of Crimes")
    plt.xlabel("Number of Crimes")
    plt.ylabel("Community Name")
    plt.tight_layout()
    plt.show()
    return merged_df

# ============================================================
# QUESTIONS
# ============================================================

def solve_questions(data):
    print_title("QUESTIONS")
    # --------------------------------------------------------
    # Q1
    # --------------------------------------------------------
    print_task("Q1.","WHICH CRIME CATEGORY IS MOST FREQUENT?")
    crime_counts = data["primary_type"].value_counts()
    most_common = crime_counts.index[0]
    print(f"Most frequent crime category: {most_common}")

    # --------------------------------------------------------
    # Q2
    # --------------------------------------------------------

    print_task("Q2.","IS THE ARREST RATE CONSISTENT ACROSS DIFFERENT YEARS?")
    yearly_arrests = (data.groupby("Year")["arrest"]
        .mean().mul(100).round(2))
    print(yearly_arrests.to_string())
    difference = (yearly_arrests.max() - yearly_arrests.min())
    if difference <= 5:
        print("Arrest rate is relatively consistent.")
    else:
        print("Arrest rate is not consistent.")

    # --------------------------------------------------------
    # Q3
    # --------------------------------------------------------

    print_task("Q3.", "WHICH MONTH HAS THE HIGHEST CRIME FREQUENCY?")
    month_frequency = (data["Month"].value_counts().sort_index())
    highest_month = month_frequency.idxmax()
    print(f"Month: {highest_month}")


# ============================================================
# DATA LOADING
# ============================================================

def get_data():

    if not CSV_PATH.exists():

        print("Cleaned dataset could not be located.")
        print("Expected file:", CSV_PATH)

        return None

    frame = pd.read_csv(CSV_PATH)

    print(
        "Cleaned Chicago Crime Dataset loaded successfully."
    )

    return frame


# ============================================================
# PROGRAM CONTROLLER
# ============================================================

def run_analysis():

    print_title("USE CASE 2")

    dataset = get_data()

    if dataset is None:
        return

    analyze_yearly_crimes(dataset)

    study_crime_categories(dataset)

    examine_arrests(dataset)

    create_crime_heatmap(dataset)

    community_analysis(dataset)

    solve_questions(dataset)

    print_title("USE CASE 2 IS COMPLETED")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    run_analysis()
