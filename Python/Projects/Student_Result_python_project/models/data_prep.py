import sqlite3
import pandas as pd
from models.config import db_path

# Load Excel file and read all sheets
file_path = r"Inputs\ExcelSheet\result list project.xlsx"  # Update with your Excel file path
# Load the Excel file
xls = pd.ExcelFile(file_path)  
conn = sqlite3.connect('Outputs/student_data.db')  

# Load the sheets into the database (this part you might run only once)
for sheet_name in xls.sheet_names:
    if __name__ == "__main__":
        print(f"Loading sheet: {sheet_name}")
    df = xls.parse(sheet_name, header=[0, 1], skiprows=0)  # Load the sheet into DataFrame

    # Flatten multi-level columns if needed
    if isinstance(df.columns, pd.MultiIndex):
        try:
            df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
        except Exception as e:
            print(f"Error flattening multi-level columns for sheet '{sheet_name}': {e}")
            continue  # Skip this sheet if there's an issue
    else:
        df.columns = [str(col).strip() for col in df.columns]

    # Remove columns with 'Unnamed'
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Write DataFrame into SQL
    df.to_sql(sheet_name, conn, if_exists='replace', index=False)
    if __name__ == "__main__":
        print(f"Sheet '{sheet_name}' written to database as table '{sheet_name}'")


# Close the connection when done
conn.close()


#temporary function to fetch sem 2 data
# Connect to the database file
conn = sqlite3.connect("Outputs/student_data.db")
cursor = conn.cursor()

# Fetch and display the schema of the sem2 table to check column types
cursor.execute("PRAGMA table_info(SEM2);")
sem2_schema = cursor.fetchall()

# Close the connection
conn.close()

sem2_schema

# Reconnect to the database to retry operations with corrected column names
conn = sqlite3.connect('Outputs/student_data.db')
cursor = conn.cursor()

# Step 1: Create a temporary table with correct INTEGER types for "EXTERNALS" columns, quoting special columns
create_temp_table_query_corrected = """
CREATE TABLE IF NOT EXISTS SEM2_temp AS
SELECT 
    "SUBJECT_CODE_USN",
    "SUBJECT_CODE_Student Name",
    BMAT201_INTERNALS,
    CAST(BMAT201_EXTERNALS AS INTEGER) AS BMAT201_EXTERNALS,
    BMAT201_TOTAL,
    BMAT201_CREDITS,
    BPHYS202_INTERNALS,
    CAST(BPHYS202_EXTERNALS AS INTEGER) AS BPHYS202_EXTERNALS,
    BPHYS202_TOTAL,
    BPHYS202_CREDITS,
    BPOPS203_INTERNALS,
    CAST(BPOPS203_EXTERNALS AS INTEGER) AS BPOPS203_EXTERNALS,
    BPOPS203_TOTAL,
    BPOPS203_CREDITS,
    BPWSK206_INTERNALS,
    CAST(BPWSK206_EXTERNALS AS INTEGER) AS BPWSK206_EXTERNALS,
    BPWSK206_TOTAL,
    BPWSK206_CREDITS,
    BKSKK207_INTERNALS,
    CAST(BKSKK207_EXTERNALS AS INTEGER) AS BKSKK207_EXTERNALS,
    BKSKK207_TOTAL,
    BKSKK207_CREDITS,
    BSFHK258_INTERNALS,
    CAST(BSFHK258_EXTERNALS AS INTEGER) AS BSFHK258_EXTERNALS,
    BSFHK258_TOTAL,
    BSFHK258_CREDITS,
    BPLCK205B_INTERNALS,
    CAST(BPLCK205B_EXTERNALS AS INTEGER) AS BPLCK205B_EXTERNALS,
    BPLCK205B_TOTAL,
    BPLCK205B_CREDITS,
    BESCK204C_INTERNALS,
    CAST(BESCK204C_EXTERNALS AS INTEGER) AS BESCK204C_EXTERNALS,
    BESCK204C_TOTAL,
    BESCK204C_CREDITS,
    "TOTAL MARKS_Unnamed: 35_level_1",
    "TOTAL MARKS_Total failed subjects",
    "TOTAL MARKS_PERCENTAGE"
FROM SEM2;
"""

# Execute the query to create the temporary table
cursor.execute(create_temp_table_query_corrected)

# Step 2: Drop the original sem2 table
cursor.execute("DROP TABLE SEM2;")

# Step 3: Rename the temp table to sem2
cursor.execute("ALTER TABLE SEM2_temp RENAME TO SEM2;")

# Commit changes and close the connection
conn.commit()
conn.close()

"Conversion and renaming complete."


#for sem4
# Reconnect to the database to make changes
conn = sqlite3.connect('Outputs/student_data.db')
cursor = conn.cursor()

# Step 1: Create a new table with corrected INTEGER types for the required fields
query = """
    CREATE TABLE IF NOT EXISTS SEM4_new AS
    SELECT 
        "SUBJECT_CODE_USN",
        "SUBJECT_CODE_Student Name",
        CAST("BCS401_INTERNALS" AS INTEGER) AS "BCS401_INTERNALS",
        CAST("BCS401_EXTERNALS" AS INTEGER) AS "BCS401_EXTERNALS",
        CAST("BCS401_TOTAL" AS INTEGER) AS "BCS401_TOTAL",
        CAST("BCS401_CREDITS" AS INTEGER) AS "BCS401_CREDITS",
        CAST("BCS402_INTERNALS" AS INTEGER) AS "BCS402_INTERNALS",
        CAST("BCS402_EXTERNALS" AS INTEGER) AS "BCS402_EXTERNALS",
        CAST("BCS402_TOTAL" AS INTEGER) AS "BCS402_TOTAL",
        CAST("BCS402_CREDITS" AS INTEGER) AS "BCS402_CREDITS",
        CAST("BCS403_INTERNALS" AS INTEGER) AS "BCS403_INTERNALS",
        CAST("BCS403_EXTERNALS" AS INTEGER) AS "BCS403_EXTERNALS",
        CAST("BCS403_TOTAL" AS INTEGER) AS "BCS403_TOTAL",
        CAST("BCS403_CREDITS" AS INTEGER) AS "BCS403_CREDITS",
        CAST("BCSL404_INTERNALS" AS INTEGER) AS "BCSL404_INTERNALS",
        CAST("BCSL404_EXTERNALS" AS INTEGER) AS "BCSL404_EXTERNALS",
        CAST("BCSL404_TOTAL" AS INTEGER) AS "BCSL404_TOTAL",
        CAST("BCSL404_CREDITS" AS INTEGER) AS "BCSL404_CREDITS",
        CAST("BBOC407_INTERNALS" AS INTEGER) AS "BBOC407_INTERNALS",
        CAST("BBOC407_EXTERNALS" AS INTEGER) AS "BBOC407_EXTERNALS",
        CAST("BBOC407_TOTAL" AS INTEGER) AS "BBOC407_TOTAL",
        CAST("BBOC407_CREDITS" AS INTEGER) AS "BBOC407_CREDITS",
        CAST("BUHK408_INTERNALS" AS INTEGER) AS "BUHK408_INTERNALS",
        CAST("BUHK408_EXTERNALS" AS INTEGER) AS "BUHK408_EXTERNALS",
        CAST("BUHK408_TOTAL" AS INTEGER) AS "BUHK408_TOTAL",
        CAST("BUHK408_CREDITS" AS INTEGER) AS "BUHK408_CREDITS",
        CAST("BPEK459 (Physical Education)/BNSK459(NSS)_INTERNALS" AS INTEGER) AS "BPEK459 (Physical Education)/BNSK459(NSS)_INTERNALS",
        CAST("BPEK459 (Physical Education)/BNSK459(NSS)_EXTERNALS" AS REAL) AS "BPEK459 (Physical Education)/BNSK459(NSS)_EXTERNALS",
        CAST("BPEK459 (Physical Education)/BNSK459(NSS)_TOTAL" AS INTEGER) AS "BPEK459 (Physical Education)/BNSK459(NSS)_TOTAL",
        CAST("BPEK459 (Physical Education)/BNSK459(NSS)_CREDITS" AS INTEGER) AS "BPEK459 (Physical Education)/BNSK459(NSS)_CREDITS",
        CAST("BCS405B_INTERNALS" AS INTEGER) AS "BCS405B_INTERNALS",
        CAST("BCS405B_EXTERNALS" AS INTEGER) AS "BCS405B_EXTERNALS",
        CAST("BCS405B_TOTAL" AS INTEGER) AS "BCS405B_TOTAL",
        CAST("BCS405B_CREDITS" AS INTEGER) AS "BCS405B _CREDITS",
        CAST("BCS405B_INTERNALS.1" AS INTEGER) AS "BCS405B_INTERNALS.1",
        CAST("BCS405B_EXTERNALS.1" AS INTEGER) AS "BCS405B_EXTERNALS.1",
        CAST("BCS405B_TOTAL.1" AS INTEGER) AS "BCS405B_TOTAL.1",
        CAST("BCS405B_CREDITS.1" AS INTEGER) AS "BCS405B_CREDITS.1",
        CAST("TOTAL Marks_Unnamed: 39_level_1" AS INTEGER) AS "TOTAL Marks_Unnamed: 39_level_1",
        CAST("TOTAL Marks_TOTAL failed subjects" AS INTEGER) AS "TOTAL Marks_TOTAL failed subjects",
        CAST("TOTAL Marks_PERCENTAGE" AS INTEGER) AS "TOTAL Marks_PERCENTAGE"
    FROM SEM4;
"""

# Execute the corrected query to create the new table
cursor.execute(query)

# Step 2: Drop the original table and rename the new table
cursor.execute("DROP TABLE IF EXISTS SEM4;")
cursor.execute("ALTER TABLE SEM4_new RENAME TO SEM4;")

# Commit the changes and close the connection
conn.commit()
conn.close()

"Conversion and table replacement completed successfully."

"Conversion and table replacement completed."


# Connect to the SQLite database
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

try:
    # Begin transaction
    cursor.execute("BEGIN TRANSACTION;")

    # Step 1: Rename the original table
    cursor.execute("ALTER TABLE SEM3 RENAME TO SEM3_OLD;")

    # Step 2: Create a new table with the correct schema
    cursor.execute("""
        CREATE TABLE SEM3 (
            SUBJECT_CODE_USN TEXT,
            "SUBJECT_CODE_Student Name" TEXT,
            BCS301_INTERNALS INTEGER,
            BCS301_EXTERNALS INTEGER,
            BCS301_TOTAL INTEGER,
            BCS301_CREDITS INTEGER,
            BCS302_INTERNALS INTEGER,
            BCS302_EXTERNALS INTEGER,
            BCS302_TOTAL INTEGER,
            BCS302_CREDITS INTEGER,
            BCS303_INTERNALS INTEGER,
            BCS303_EXTERNALS INTEGER,
            BCS303_TOTAL INTEGER,
            BCS303_CREDITS INTEGER,
            BCS304_INTERNALS INTEGER,
            BCS304_EXTERNALS INTEGER,
            BCS304_TOTAL INTEGER,
            BCS304_CREDITS INTEGER,
            BCSL305_INTERNALS INTEGER,
            BCSL305_EXTERNALS INTEGER,
            BCSL305_TOTAL INTEGER,
            BCSL305_CREDITS INTEGER,
            BSCK307_INTERNALS INTEGER,
            BSCK307_EXTERNALS INTEGER,
            BSCK307_TOTAL INTEGER,
            BSCK307_CREDITS INTEGER,
            BNSK359_INTERNALS INTEGER,
            BNSK359_EXTERNALS INTEGER,
            BNSK359_TOTAL INTEGER,
            BNSK359_CREDITS INTEGER,
            BCS306A_INTERNALS INTEGER,
            BCS306A_EXTERNALS INTEGER,
            BCS306A_TOTAL INTEGER,
            BCS306A_CREDITS INTEGER,
            BCS358D_INTERNALS INTEGER,
            BCS358D_EXTERNALS INTEGER,
            BCS358D_TOTAL INTEGER,
            BCS358D_CREDITS INTEGER,
            "TOTAL Marks_Unnamed: 39_level_1" INTEGER,
            "TOTAL Marks_Total failed subjects" INTEGER,
            "TOTAL Marks_PERCENTAGE" INTEGER
        );
    """)

    # Step 3: Copy data from the old table to the new table
    cursor.execute("""
        INSERT INTO SEM3 (
            SUBJECT_CODE_USN,
            "SUBJECT_CODE_Student Name",
            BCS301_INTERNALS,
            BCS301_EXTERNALS,
            BCS301_TOTAL,
            BCS301_CREDITS,
            BCS302_INTERNALS,
            BCS302_EXTERNALS,
            BCS302_TOTAL,
            BCS302_CREDITS,
            BCS303_INTERNALS,
            BCS303_EXTERNALS,
            BCS303_TOTAL,
            BCS303_CREDITS,
            BCS304_INTERNALS,
            BCS304_EXTERNALS,
            BCS304_TOTAL,
            BCS304_CREDITS,
            BCSL305_INTERNALS,
            BCSL305_EXTERNALS,
            BCSL305_TOTAL,
            BCSL305_CREDITS,
            BSCK307_INTERNALS,
            BSCK307_EXTERNALS,
            BSCK307_TOTAL,
            BSCK307_CREDITS,
            BNSK359_INTERNALS,
            BNSK359_EXTERNALS,
            BNSK359_TOTAL,
            BNSK359_CREDITS,
            BCS306A_INTERNALS,
            BCS306A_EXTERNALS,
            BCS306A_TOTAL,
            BCS306A_CREDITS,
            BCS358D_INTERNALS,
            BCS358D_EXTERNALS,
            BCS358D_TOTAL,
            BCS358D_CREDITS,
            "TOTAL Marks_Unnamed: 39_level_1",
            "TOTAL Marks_Total failed subjects",
            "TOTAL Marks_PERCENTAGE"
        )
        SELECT 
            SUBJECT_CODE_USN,
            "SUBJECT_CODE_Student Name",
            CAST(BCS301_INTERNALS AS INTEGER),
            CAST(BCS301_EXTERNALS AS INTEGER),
            CAST(BCS301_TOTAL AS INTEGER),
            CAST(BCS301_CREDITS AS INTEGER),
            CAST(BCS302_INTERNALS AS INTEGER),
            CAST(BCS302_EXTERNALS AS INTEGER),
            CAST(BCS302_TOTAL AS INTEGER),
            CAST(BCS302_CREDITS AS INTEGER),
            CAST(BCS303_INTERNALS AS INTEGER),
            CAST(BCS303_EXTERNALS AS INTEGER),
            CAST(BCS303_TOTAL AS INTEGER),
            CAST(BCS303_CREDITS AS INTEGER),
            CAST(BCS304_INTERNALS AS INTEGER),
            CAST(BCS304_EXTERNALS AS INTEGER),
            CAST(BCS304_TOTAL AS INTEGER),
            CAST(BCS304_CREDITS AS INTEGER),
            CAST(BCSL305_INTERNALS AS INTEGER),
            CAST(BCSL305_EXTERNALS AS INTEGER),
            CAST(BCSL305_TOTAL AS INTEGER),
            CAST(BCSL305_CREDITS AS INTEGER),
            CAST(BSCK307_INTERNALS AS INTEGER),
            CAST(BSCK307_EXTERNALS AS INTEGER),
            CAST(BSCK307_TOTAL AS INTEGER),
            CAST(BSCK307_CREDITS AS INTEGER),
            CAST(BNSK359_INTERNALS AS INTEGER),
            CAST(BNSK359_EXTERNALS AS INTEGER),
            CAST(BNSK359_TOTAL AS INTEGER),
            CAST(BNSK359_CREDITS AS INTEGER),
            CAST(BCS306A_INTERNALS AS INTEGER),
            CAST(BCS306A_EXTERNALS AS INTEGER),
            CAST(BCS306A_TOTAL AS INTEGER),
            CAST(BCS306A_CREDITS AS INTEGER),
            CAST(BCS358D_INTERNALS AS INTEGER),
            CAST(BCS358D_EXTERNALS AS INTEGER),
            CAST(BCS358D_TOTAL AS INTEGER),
            CAST(BCS358D_CREDITS AS INTEGER),
            CAST("TOTAL Marks_Unnamed: 39_level_1" AS INTEGER),
            CAST("TOTAL Marks_Total failed subjects" AS INTEGER),
            CAST("TOTAL Marks_PERCENTAGE" AS INTEGER)
        FROM SEM3_OLD;
    """)

    # Step 4: Drop the old table
    cursor.execute("DROP TABLE SEM3_OLD;")

    # Commit transaction
    connection.commit()
    if __name__ == "__main__":
        print("Schema updated successfully.")
    
except Exception as e:
    # Rollback in case of an error
    connection.rollback()
    if __name__ == "__main__":
        print(f"Error occurred: {e}")

finally:
    # Close the connection
    connection.close()


    
# Path to your database
db_path = "Outputs/student_data.db"  # Update this path if needed

# Connect to the database
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Columns to update
columns_to_update = [
    "BCS301_TOTAL", "BCS302_TOTAL", "BCS303_TOTAL", "BCS304_TOTAL",
    "BCSL305_TOTAL", "BSCK307_TOTAL", "BNSK359_TOTAL",
    "BCS306A_TOTAL", "BCS358D_TOTAL"
]

# Update each column: Replace NULL with 0 and ensure type-cast to INTEGER
for column in columns_to_update:
    query = f"""
    UPDATE SEM3
    SET {column} = CAST(COALESCE({column}, 0) AS INTEGER);
    """
    cursor.execute(query)

# Commit changes
connection.commit()

# Verify the update by checking for any remaining NULL values
verification_query = f"""
SELECT * FROM SEM3
WHERE {' OR '.join([f"{col} IS NULL" for col in columns_to_update])};
"""
cursor.execute(verification_query)
rows_with_nulls = cursor.fetchall()

# Close the connection
connection.close()



# Path to your database
db_path = "Outputs/student_data.db"  # Update this path if necessary

# Connect to the database
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Fetch data using COALESCE to replace NULL with 0
query = """
SELECT 
    COALESCE(BCS301_TOTAL, 0) AS BCS301_TOTAL,
    COALESCE("BCS302_TOTAL", 0) AS BCS302_TOTAL,
    COALESCE(BCS303_TOTAL, 0) AS BCS303_TOTAL,
    COALESCE(BCS304_TOTAL, 0) AS BCS304_TOTAL,
    COALESCE("BCSL305_TOTAL", 0) AS BCSL305_TOTAL,
    COALESCE(BSCK307_TOTAL, 0) AS BSCK307_TOTAL,
    COALESCE("BNSK359_TOTAL", 0) AS BNSK359_TOTAL,
    COALESCE(BCS306A_TOTAL, 0) AS BCS306A_TOTAL,
    COALESCE(BCS358D_TOTAL, 0) AS BCS358D_TOTAL
FROM SEM3;
"""
cursor.execute(query)
rows = cursor.fetchall()
# Close the connection
connection.close()

# Debug: Check if any None values are still present
if __name__ == "__main__":
    # Fetch and display the first 10 rows of each table (run this separately when needed)
    for sheet_name in xls.sheet_names:
        df_from_db = pd.read_sql_query(f"SELECT * FROM '{sheet_name}' LIMIT 10 OFFSET 0", conn)
        print(f"\nData from table '{sheet_name}' (10 rows and 10 columns):")
        print(df_from_db.iloc[:10, :10])

    # Output the verification result
    if rows_with_nulls:
        print("Some NULL values remain:")
        for row in rows_with_nulls:
            print(row)
    else:
        print("All NULL values have been replaced, and columns are type-cast successfully.")
    print("Fetched rows:")
    for row in rows:
        print(row)
