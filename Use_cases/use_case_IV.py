"""
Chicago Crime Project
USE CASE - 4
"""
import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# PATH CONFIGURATION
# ------------------------------------------------------------
def database_location():
    project_dir = Path(__file__).resolve().parents[1]
    return project_dir / "database" / "chicago_crime.db"

# ------------------------------------------------------------
# DISPLAY FUNCTIONS
# ------------------------------------------------------------
def show_title(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)
def show_section(text):
    print("\n" + text)
    print("-" * 70)

# ------------------------------------------------------------
# DATABASE HELPER
# ------------------------------------------------------------
def fetch_data(connection, statement):
    return pd.read_sql_query(statement, connection)

# ------------------------------------------------------------
# CREATE SUMMARY TABLES
# ------------------------------------------------------------
def build_summary_tables(connection):
    sql_commands = """
    DROP TABLE IF EXISTS summary_crime_yearly;
    CREATE TABLE summary_crime_yearly AS
    SELECT
        Year,
        COUNT(*) AS total_crimes,
        SUM(arrest) AS total_arrests
    FROM chicago_crime
    GROUP BY Year;

    DROP TABLE IF EXISTS summary_crime_category;
    CREATE TABLE summary_crime_category AS
    SELECT
        primary_type,
        COUNT(*) AS crime_count,
        ROUND(
            COUNT(*) * 100.0 /
            (SELECT COUNT(*) FROM chicago_crime),
            2
        ) AS percentage
    FROM chicago_crime
    GROUP BY primary_type
    ORDER BY crime_count DESC;
    """
    connection.executescript(sql_commands)
    connection.commit()
    print("Summary tables created and populated successfully.")
    
# ------------------------------------------------------------
# SQLITE QUERIES
# ------------------------------------------------------------
def run_sql_queries(connection):
    show_section("2.1 CRIME COUNT PER YEAR")
    yearly_data = fetch_data(
        connection,
        """
        SELECT
            Year,
            COUNT(*) AS crime_count
        FROM chicago_crime
        GROUP BY Year
        ORDER BY Year;
        """
    )
    print(yearly_data.to_string(index=False))
    show_section("2.2 TOP 5 CRIME TYPES AND THEIR PERCENTAGES")
    crime_types = fetch_data(
        connection,
        """
        SELECT
            primary_type,
            COUNT(*) AS crime_count,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*) FROM chicago_crime),
                2
            ) AS percentage
        FROM chicago_crime
        GROUP BY primary_type
        ORDER BY crime_count DESC
        LIMIT 5;
        """
    )
    print(crime_types.to_string(index=False))
    show_section("2.3 ARREST COUNT PER YEAR")
    arrest_data = fetch_data(
        connection,
        """
        SELECT
            Year,
            SUM(arrest) AS arrest_count
        FROM chicago_crime
        GROUP BY Year
        ORDER BY Year;
        """
    )
    print(arrest_data.to_string(index=False))

# ------------------------------------------------------------
# CREATE DATABASE VIEWS
# ------------------------------------------------------------
def create_views(connection):
    connection.execute(
        "DROP VIEW IF EXISTS vw_crime_yearly"
    )
    connection.execute(
        """
        CREATE VIEW vw_crime_yearly AS
        SELECT
            Year,
            COUNT(*) AS total_crimes,
            SUM(arrest) AS total_arrests,
            ROUND(
                SUM(arrest) * 100.0 / COUNT(*),
                2
            ) AS arrest_rate_pct
        FROM chicago_crime
        GROUP BY Year
        ORDER BY Year;
        """
    )
    connection.execute(
        "DROP VIEW IF EXISTS vw_crime_by_category"
    )
    connection.execute(
        """
        CREATE VIEW vw_crime_by_category AS
        SELECT
            primary_type,
            COUNT(*) AS crime_count,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*) FROM chicago_crime),
                2
            ) AS percentage
        FROM chicago_crime
        GROUP BY primary_type
        ORDER BY crime_count DESC;
        """
    )
    connection.commit()
    print("Database views created successfully.")

# ------------------------------------------------------------
# DISPLAY VIEW DATA
# ------------------------------------------------------------
def display_views(connection):
    yearly = fetch_data(
        connection,
        "SELECT * FROM vw_crime_yearly"
    )
    categories = fetch_data(
        connection,
        "SELECT * FROM vw_crime_by_category"
    )
    print("\nVW_CRIME_YEARLY")
    print(yearly.to_string(index=False))
    print("\nVW_CRIME_BY_CATEGORY")
    print(categories.to_string(index=False))
    return yearly, categories

# ------------------------------------------------------------
# GRAPH 1
# ------------------------------------------------------------
def plot_crimes_and_arrests(data):
    show_section("5.1 CRIMES VS ARRESTS PER YEAR")
    years = data["Year"].astype(str)
    positions = list(range(len(data)))
    width = 0.35
    plt.figure(figsize=(12, 6))
    plt.bar(
        [p - width / 2 for p in positions],
        data["total_crimes"],
        width=width,
        label="Total Crimes"
    )
    plt.bar(
        [p + width / 2 for p in positions],
        data["total_arrests"],
        width=width,
        label="Total Arrests"
    )
    plt.xticks(positions, years)
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.title("Crimes vs Arrests Per Year (VW_crime_yearly)")
    plt.legend()
    plt.tight_layout()
    plt.show()

# ------------------------------------------------------------
# GRAPH 2
# ------------------------------------------------------------
def plot_arrest_rate(data):
    show_section("5.2 ARREST RATE PER YEAR")
    plt.figure(figsize=(12, 6))
    plt.plot(
        data["Year"],
        data["arrest_rate_pct"],
        marker="D"
    )
    for year, rate in zip(
        data["Year"],
        data["arrest_rate_pct"]
    ):
        plt.annotate(
            f"{rate:.2f}%",
            (year, rate),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center"
        )
    plt.xlabel("Year")
    plt.ylabel("Arrest Rate (%)")
    plt.title("Arrest Rate (%) Per Year")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

# ------------------------------------------------------------
# GRAPH 3
# ------------------------------------------------------------
def plot_crime_categories(data):
    show_section("5.3 CRIME CATEGORIES")
    plt.figure(figsize=(12, 8))
    bars = plt.barh(
        data["primary_type"],
        data["crime_count"]
    )
    for bar, percentage in zip(
        bars,
        data["percentage"]
    ):
        plt.text(
            bar.get_width() + 2,
            bar.get_y() + bar.get_height() / 2,
            f"{percentage}%",
            va="center"
        )
    plt.xlabel("Crime Count")
    plt.ylabel("Crime Type")
    plt.title("All Crime Types - VW_crime_by_category")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def execute_use_case():
    show_title("USE CASE 4")
    db_path = database_location()
    if not db_path.is_file():
        raise FileNotFoundError(
            f"Database not found:\n{db_path}"
        )
    connection = sqlite3.connect(db_path)
    try:
        print("SQLite database connected successfully.")
        # 1. Summary tables
        show_title("1. DESIGN & POPULATE SUMMARY TABLES")
        show_section("1.1 CREATE TABLES AND LOAD THE DATA")
        build_summary_tables(connection)
        # 2. SQL operations
        show_title("2. SQLITE QUERIES")
        run_sql_queries(connection)
        # 3. Views
        show_title("3. DATABASE STORED VIEWS")
        show_section("3.1 VW_CRIME_YEARLY")
        show_section("3.2 VW_CRIME_BY_CATEGORY")
        create_views(connection)
        # 4. Pandas
        show_title("4. PANDAS INTEGRATION")
        show_section("4.1 READ VIEWS INTO PANDAS DATAFRAMES")
        yearly_df, category_df = display_views(connection)
        # 5. Visualization
        show_title("5. VISUALIZATION FROM SQLITE DATA")
        plot_crimes_and_arrests(yearly_df)
        plot_arrest_rate(yearly_df)
        plot_crime_categories(category_df)
    finally:
        connection.close()
        print("\nSQLite database connection closed.")
    show_title("USE CASE 4 IS COMPLETED")

if __name__ == "__main__":
    execute_use_case()
