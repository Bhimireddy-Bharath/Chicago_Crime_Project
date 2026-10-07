# Chicago_Crime_Project
Name :Bhimireddy Bharath Kumar Reddy
Email : bhimireddy.bharath99@gmail.com

CHICAGO CRIME ANALYSIS PROJECT
===============================

PROJECT OVERVIEW
----------------
This project analyzes the Chicago Crime Dataset to understand crime patterns,
crime intensity, community-level crime distribution, and arrest trends.

The project covers data preparation, database management, SQL analysis,
Pandas-based analysis, visualization, and a simple Flask dashboard.

PROJECT STRUCTURE
-----------------
Project_bharath/
│
├── database/
│   └── chicago_crime.db
│
├── Graphs/
│   ├── Use Case II graphs
│   ├── Use Case III graphs
│   └── Use Case IV graphs
│
└── Web_app/
    ├── app.py
    ├── templates/
    │   └── index.html
    ├── requirements.txt
    └── README.txt

USE CASE 1 - DATA LOADING, CLEANING AND DATABASE INSERTION
-----------------------------------------------------------
Use Case 1 prepares the Chicago Crime Dataset for analysis.

The raw dataset is loaded and examined to understand its structure and
contents. The data is cleaned by handling missing or unsuitable values,
checking the required fields, and preparing the data for database storage.

After cleaning, the processed records are inserted into the SQLite database.
This provides a reliable data source for the remaining use cases.

Main activities:
- Load the Chicago Crime Dataset.
- Examine the records and fields.
- Clean and prepare the data.
- Handle missing or invalid values.
- Prepare the required fields.
- Store the cleaned records in SQLite.


USE CASE 2 - CRIME PATTERN ANALYSIS
-----------------------------------
Use Case 2 identifies the main patterns present in Chicago crime data.

The analysis examines how crime changes over time, which crime categories
occur most frequently, how crime is distributed across communities, and how
arrests relate to reported crimes.

The analysis covers yearly crime trends, major crime categories, crime by
month and day, community-level crime distribution, and arrest analysis.

Main analysis areas:
- Total number of crimes by year.
- Top crime categories.
- Crime distribution by month and day of the week.
- Crime distribution across community areas.
- Arrest analysis.


USE CASE 3 - CRIME INTENSITY ANALYSIS
-------------------------------------
Use Case 3 studies the intensity and concentration of crime.

The analysis focuses on the time of day and community areas. It helps identify
periods when crime occurs more frequently and areas with higher numbers of
reported crimes.

Main analysis areas:
- Number of crimes by hour.
- Crime count by community area.
- Identification of periods with higher crime activity.
- Identification of communities with higher crime counts.


USE CASE 4 - DATABASE AND ARREST ANALYSIS
-----------------------------------------
Use Case 4 performs advanced analysis using the SQLite database.

Summary information is organized for yearly crime and arrest data and for
crime categories. SQL analysis is used to determine yearly crime counts,
common crime types, their percentages, and yearly arrest counts.

Database views are used to provide reusable analytical information. The
yearly view contains total crimes, total arrests, and arrest rate for each
year. The crime-category view contains crime counts and the percentage
contribution of each crime category.

The results are then used to study the relationship between crimes and
arrests, changes in arrest rates, and the distribution of crime categories.

Main analysis areas:
- Crime count per year.
- Top crime types and their percentages.
- Arrest count per year.
- Crimes compared with arrests per year.
- Arrest rate per year.
- Crime distribution by category.
- Database summary tables.
- Database stored views.
- Pandas integration with database information.


DATABASE
--------
SQLite is used as the database system.

The main crime table stores the cleaned Chicago Crime Dataset. The database
also supports summary tables and analytical views required by the use cases.

The database provides a structured way to store, retrieve, update, and
analyze crime records.


DASHBOARD
---------
A simple Flask dashboard presents the project information and the prepared
graph images.

The dashboard contains:
- Dashboard
- Crime Pattern
- Crime Intensity
- Database Analysis
- Manage Records
- About

The dashboard displays the existing analysis graph images instead of creating
new graphs every time the page is opened.

The application also provides REST API functionality for managing database
records.


REST API AND CRUD
-----------------
The application supports database operations through a REST API.

CRUD means:
- Create: add a new crime record.
- Read: retrieve existing crime records.
- Update: modify an existing crime record.
- Delete: remove a crime record.

These operations allow crime records to be managed through the dashboard.


PROJECT OBJECTIVE
-----------------
The overall objective is to transform raw Chicago crime data into useful
information through data preparation, database management, analysis, and
visualization.

The project helps understand:
- How crime changes over time.
- Which crime categories are most common.
- When crime occurs more frequently.
- Which community areas have higher crime counts.
- How arrests compare with reported crimes.
- How arrest rates change over time.


CONCLUSION
----------
The Chicago Crime Analysis Project provides an end-to-end approach to crime
data analysis.

Use Case 1 prepares and stores the data.
Use Case 2 identifies general crime patterns.
Use Case 3 examines crime intensity by time and community.
Use Case 4 performs database-based analysis of crimes, arrests, rates, and
crime categories.

Together, these use cases provide a structured understanding of the Chicago
Crime Dataset and support analysis through the Flask dashboard.
