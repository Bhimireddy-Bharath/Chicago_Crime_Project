"""
USE CASE 1 - Load and Clean Chicago Crime Data
"""
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

# ============================================================
# PROJECT CONFIGURATION
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "dataset"
DB_DIR = ROOT_DIR / "database"

SOURCE_CSV = DATA_DIR / "chicago_crime_dataset.csv"
OUTPUT_CSV = DATA_DIR / "chicago_crime_cleaned.csv"
SQLITE_DB = DB_DIR / "chicago_crime.db"

TABLE = "chicago_crime"

# ============================================================
# DISPLAY FUNCTIONS
# ============================================================
def show_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
def show_subsection(title):
    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)

# ============================================================
# 1. LOAD THE DATASET
# ============================================================
def read_dataset():
    show_section("1. LOAD CHICAGO CRIME DATASET")
    if not SOURCE_CSV.is_file():
        print("Dataset file was not found.")
        print("Expected location:", SOURCE_CSV)
        return None
    data = pd.read_csv(SOURCE_CSV)
    # Remove accidental spaces from column names
    data.columns = data.columns.str.strip()
    return data
# ------------------------------------------------------------
# 1.1 Inspect first 10 records and data types
# ------------------------------------------------------------
def inspect_dataset(data):
    show_subsection("1.1 DISPLAY FIRST 10 ROWS AND DATA TYPES")
    print("\nFirst 10 records:")
    print(data.head(10))
    print("\nData types:")
    print(data.dtypes)
    print("\nData Schema:")
    print(data.info())
# ------------------------------------------------------------
# 1.2 Display number of rows and columns
# ------------------------------------------------------------
def dataset_size(data):
    show_subsection("1.2 NUMBER OF ROWS AND COLUMNS")
    row_count, column_count = data.shape
    print("Number of rows    :", row_count)
    print("Number of columns :", column_count)

# ============================================================
# 2. CLEAN THE DATASET
# ============================================================
def clean_dataset(data):
    show_section("2. CLEAN THE DATASET")
    # --------------------------------------------------------
    # 2.1 Convert Date column
    # --------------------------------------------------------
    show_subsection("2.1 CONVERT DATE COLUMN INTO DATETIME")
    date_column = None
    for col in data.columns:
        if col.strip().lower() == "date":
            date_column = col
            break
    if date_column is not None:
        data[date_column] = pd.to_datetime(
            data[date_column],
            errors="coerce"
        )
        print("Date column converted successfully.")
        print("Date data type:", data[date_column].dtype)
    else:
        print("Date column was not found.")
    # --------------------------------------------------------
    # 2.2 Identify and handle missing values
    # --------------------------------------------------------
    show_subsection("2.2 IDENTIFY AND HANDLE MISSING VALUES")
    missing_before = data.isna().sum()
    print("\nMissing values before cleaning:")
    print(missing_before)
    # Columns where text values are normally expected
    text_columns = data.select_dtypes(
        include=["object", "string"]
    ).columns
    for col in text_columns:
        data[col] = data[col].fillna("UNKNOWN")
    # Numeric columns are kept numeric.
    # Missing numeric values are replaced with 0.
    numeric_columns = data.select_dtypes(
        include=[np.number]
    ).columns
    for col in numeric_columns:
        data[col] = data[col].fillna(0)
    print("\nMissing values after cleaning:")
    print(data.isna().sum())
    # --------------------------------------------------------
    # 2.3 Standardize categorical fields
    # --------------------------------------------------------
    show_subsection("2.3 STANDARDIZE CATEGORICAL DATA")
    categorical_columns = data.select_dtypes(
        include=["object", "string"]
    ).columns
    for col in categorical_columns:
        data[col] = (
            data[col]
            .astype("string")
            .str.strip()
            .str.upper()
        )
    print("Categorical fields standardized successfully.")
    return data

# ============================================================
# 3. GENERATE NEW FEATURES
# ============================================================
def create_features(data):
    show_section("3. GENERATE NEW FEATURES")
    # --------------------------------------------------------
    # Protect the existing Year column
    # --------------------------------------------------------
    existing_year = None
    for col in data.columns:
        if col.strip().lower() == "year":
            existing_year = col
            break
    if existing_year is not None and existing_year != "OriginalYear":
        data.rename(
            columns={existing_year: "OriginalYear"},
            inplace=True
        )
        print("Existing year column renamed to OriginalYear.")
    # --------------------------------------------------------
    # Make sure Date exists
    # --------------------------------------------------------
    date_column = None
    for col in data.columns:
        if col.strip().lower() == "date":
            date_column = col
            break
    if date_column is None:
        print("Date column is unavailable.")
        return data
    # --------------------------------------------------------
    # 3.1 Extract Year
    # --------------------------------------------------------
    show_subsection("3.1 EXTRACT YEAR")
    data["Year"] = data[date_column].dt.year
    print("Year feature created.")
    print(data[["Year"]].head(10))
    # --------------------------------------------------------
    # 3.2 Extract Month
    # --------------------------------------------------------
    show_subsection("3.2 EXTRACT MONTH")
    data["Month"] = data[date_column].dt.month
    print("Month feature created.")
    print(data[["Month"]].head(10))

    # --------------------------------------------------------
    # 3.3 Extract Day Of Week
    # --------------------------------------------------------
    show_subsection("3.3 EXTRACT DAY OF WEEK")
    data["DayOfWeek"] = data[date_column].dt.day_name()
    print("DayOfWeek feature created.")
    print(data[["DayOfWeek"]].head(10))
    print("\nNew features generated successfully.")
    return data

# ============================================================
# 4. NUMPY ANALYSIS
# ============================================================
def numpy_analysis(data):
    show_section("4. USE NUMPY")
    # --------------------------------------------------------
    # 4.1 Calculate missing percentage
    # --------------------------------------------------------
    show_subsection("4.1 CALCULATE MISSING VALUE PERCENTAGE")
    total_rows = len(data)
    if total_rows > 0:
        missing_counts = data.isna().sum().to_numpy()
        missing_percent = (
            missing_counts / total_rows
        ) * 100
        missing_report = pd.Series(
            missing_percent,
            index=data.columns
        )
        print("Percentage of missing values per column:\n")
        print(missing_report)
    else:
        print("Dataset contains no rows.")
        missing_report = pd.Series(dtype=float)
    # --------------------------------------------------------
    # 4.2 Check columns with more than 50% missing values
    # --------------------------------------------------------
    show_subsection("4.2 COLUMNS WITH MORE THAN 50% MISSING VALUES")
    high_missing = missing_report[
        missing_report > 50
    ]
    if high_missing.empty:
        print("No columns contain more than 50% missing values.")
    else:
        print("Columns containing more than 50% missing values:")
        print(high_missing)

# ============================================================
# 5. SAVE DATA INTO SQLITE
# ============================================================
def sqlite_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    if pd.api.types.is_float_dtype(series):
        return "REAL"
    if pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    return "TEXT"

# ------------------------------------------------------------
# 5.1 Create SQLite database and table
# ------------------------------------------------------------
def create_sqlite_table(data):
    show_section("5. INSERT CLEANED DATA INTO SQLITE")
    show_subsection("5.1 CREATE SQLITE DATABASE AND TABLE")
    DB_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(SQLITE_DB)
    cursor = connection.cursor()
    # Remove old table so the program can be executed again
    cursor.execute(
        f'DROP TABLE IF EXISTS "{TABLE}"'
    )
    column_definitions = []
    for column in data.columns:
        sql_type = sqlite_type(data[column])
        safe_name = column.replace('"', '""')
        column_definitions.append(
            f'"{safe_name}" {sql_type}'
        )
    create_statement = f'''
        CREATE TABLE "{TABLE}" (
            {", ".join(column_definitions)}
        )
    '''
    cursor.execute(create_statement)
    connection.commit()
    print("SQLite database created successfully.")
    print("Database:", SQLITE_DB)
    print("Table   :", TABLE)
    return connection

# ------------------------------------------------------------
# 5.2 Insert records using sqlite3
# ------------------------------------------------------------
def insert_records(data, connection):
    show_subsection("5.2 INSERT CLEANED RECORDS INTO SQLITE")
    cursor = connection.cursor()
    # Make a separate copy for SQLite insertion
    records_df = data.copy()
    # Convert datetime columns into SQLite-compatible text
    for column in records_df.columns:
        if pd.api.types.is_datetime64_any_dtype(records_df[column]):
            records_df[column] = records_df[column].dt.strftime(
                "%Y-%m-%d %H:%M:%S")
    # Replace missing values with None
    records_df = records_df.astype(object)
    records_df = records_df.where(
        pd.notna(records_df),None)
    # Convert NumPy values into normal Python values
    def convert_value(value):
        if isinstance(value, np.generic):
            return value.item()
        return value
    records = []
    for row in records_df.itertuples(
        index=False,
        name=None):
        converted_row = tuple(convert_value(value)
            for value in row)
        records.append(converted_row)
    # Prepare column names
    column_names = ", ".join('"' + column.replace('"', '""') + '"'
        for column in records_df.columns)
    # Create placeholders
    placeholders = ", ".join("?" for _ in records_df.columns)
    insert_sql = f"""
        INSERT INTO "{TABLE}"
        ({column_names})
        VALUES ({placeholders})
    """
    # Insert all rows
    cursor.executemany(insert_sql,records)
    connection.commit()
    print("Cleaned records inserted successfully.")
    print("Number of records inserted:", len(records))
    # Verify inserted rows
    cursor.execute(f'SELECT COUNT(*) FROM "{TABLE}"')
    total_rows = cursor.fetchone()[0]
    print("Total records in SQLite:", total_rows)

# ============================================================
# 6. QUESTIONS
# ============================================================

def answer_questions(data):
    show_section("QUESTIONS")
    # --------------------------------------------------------
    # 6.1 Number of unique crime types
    # --------------------------------------------------------
    show_subsection("6.1 UNIQUE CRIME TYPES")
    crime_column = None
    for col in data.columns:
        name = col.strip().lower()
        if name in [
            "primary_type",
            "crime_type",
            "type"]:
            crime_column = col
            break
    if crime_column is not None:
        unique_crimes = data[crime_column].nunique()
        print(
            "Number of unique crime types:",
            unique_crimes)
    else:
        print("Crime type column was not found.")
    # --------------------------------------------------------
    # 6.2 Date anomalies and obvious outliers
    # --------------------------------------------------------
    show_subsection("6.2 DATE ANOMALIES AND OBVIOUS OUTLIERS")
    date_column = None
    for col in data.columns:
        if col.strip().lower() == "date":
            date_column = col
            break
    if date_column is not None:
        invalid_dates = data[date_column].isna().sum()
        print("Invalid or missing date values:",invalid_dates)
        valid_dates = data[date_column].dropna()
        if len(valid_dates) > 0:
            print("Earliest date:",valid_dates.min() )
            print("Latest date:",valid_dates.max())
            print("Date values were checked for invalid entries.")
    else:
        print("Date column was not found.")

# ============================================================
# 7. SAVE CLEANED CSV
# ============================================================
def save_cleaned_file(data):
    show_section("SAVE CLEANED DATASET")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data.to_csv(
        OUTPUT_CSV,
        index=False
    )
    print("Cleaned dataset saved successfully.")
    print("File   :", OUTPUT_CSV)
    print("Rows   :", len(data))
    print("Columns:", len(data.columns))

# ============================================================
# MAIN PROGRAM
# ============================================================
def main():
    # 1. Load
    dataframe = read_dataset()
    if dataframe is None:
        return
    inspect_dataset(dataframe)
    dataset_size(dataframe)

    # 2. Clean
    dataframe = clean_dataset(dataframe)

    # Save cleaned data before feature generation
    save_cleaned_file(dataframe)

    # 3. Generate features
    dataframe = create_features(dataframe)

    # 4. NumPy calculations
    numpy_analysis(dataframe)

    # Save final dataset with generated features
    dataframe.to_csv(
        OUTPUT_CSV,
        index=False
    )
    print("\nFinal cleaned dataset updated successfully.")

    # 5. SQLite
    connection = create_sqlite_table(dataframe)
    insert_records(
        dataframe,
        connection
    )
    connection.close()
    print("\nSQLite connection closed.")

    # 6. Questions
    answer_questions(dataframe)
    print("\n" + "=" * 70)
    print("USE CASE 1 COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    main()
