import pathlib
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from fpdf import FPDF
from reportlab.lib.pagesizes import letter, landscape
import customtkinter as ctk
import textwrap
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle ,Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
# os.chdir(r"C:\Users\CHEKI\Documents\VS coding\Python\Student Result python project")

# Load Excel file and read all sheets
file_path = r"Inputs\ExcelSheet\result list project.xlsx"  # Update with your Excel file path
# Load the Excel file
xls = pd.ExcelFile(file_path)  
conn = sqlite3.connect('Outputs/student_data.db')  

# Load the sheets into the database (this part you might run only once)
for sheet_name in xls.sheet_names:
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
    print(f"Sheet '{sheet_name}' written to database as table '{sheet_name}'")

# Fetch and display the first 10 rows of each table (run this separately when needed)
for sheet_name in xls.sheet_names:
    df_from_db = pd.read_sql_query(f"SELECT * FROM '{sheet_name}' LIMIT 10 OFFSET 0", conn)
    print(f"\nData from table '{sheet_name}' (10 rows and 10 columns):")
    print(df_from_db.iloc[:10, :10])

# Close the connection when done
conn.close()

'''#temporary function
def get_column_names(table_name, db_path="Outputs/student_data.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute PRAGMA command to get column info
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()  # Fetch all column info

        # Extract column names
        column_names = [col[1] for col in columns_info]  # col[1] contains the column name

        conn.close()
        return column_names  # Return the list of column names

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
        return None

# Example usage
table_name = "Sheet1"  # Replace with your actual table name
column_names = get_column_names(table_name)
print("Column names in the table:", column_names)'''

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



# Path to your SQLite database
db_path = "Outputs/student_data.db"

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
    print("Schema updated successfully.")
    
except Exception as e:
    # Rollback in case of an error
    connection.rollback()
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

# Output the verification result
if rows_with_nulls:
    print("Some NULL values remain:")
    for row in rows_with_nulls:
        print(row)
else:
    print("All NULL values have been replaced, and columns are type-cast successfully.")


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

# Debug: Check if any None values are still present
print("Fetched rows:")
for row in rows:
    print(row)

# Close the connection
connection.close()

# Function to fetch data from the database with error handling for missing USN
def fetch_student_data(usn, semester, db_path="Outputs/student_data.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Make sure the query uses the correct semester table
        query = f"""
        SELECT *
        FROM {semester}
        WHERE "Subject_Code_USN" = ?
        """
        cursor.execute(query, (usn,))
        rows = cursor.fetchall()
        conn.close()

        # Check if rows are found
        if not rows:
            return None  # Return None if no data is found for the USN in that semester

        # Extract data from the row
        student_data = rows[0]

        # Extracting internal marks, external marks, and credits
        subject_code=[]
        ia_marks = []
        see_marks = []
        credits = []

        # Iterate through the columns to extract marks and credits
        for i in range(2, len(student_data)):  # Start from the 3rd column (index 2)
            column_name = cursor.description[i][0]  # Get the column name

            # Only check columns that contain marks or credits
            if 'INTERNALS' in column_name:
                ia_marks.append(student_data[i])
                subject_code.append(column_name.split('_')[0])
            elif 'EXTERNALS' in column_name:
                see_marks.append(student_data[i])
            elif 'CREDITS' in column_name:
                credits.append(student_data[i])

        return {
            "name": student_data[1],  # Student Name
            "usn": usn,
            "subject_code": subject_code,
            "ia_marks": ia_marks,
            "see_marks": see_marks,
            "credits": credits,
        }

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
        return None


#test the above function
'''student_data = fetch_student_data('1JS22CS001')  # Replace with a valid USN
if student_data:
    print(student_data)
else:
    print("No data found for the specified USN.")'''


# Define Student class
class Student:
    def __init__(self, usn, semester, db_path="Outputs/student_data.db"):
        self.db_path = db_path
        self.semester=semester
        student_info = fetch_student_data(usn, semester, self.db_path)
        if student_info is None:
            raise ValueError("Student data not found")
        self.usn = usn
        self.name = student_info["name"]
        self.subject_codes=student_info["subject_code"]
        self.ia_marks = student_info["ia_marks"]
        self.see_marks = student_info["see_marks"]
        self.credits = student_info["credits"]
        self.total_marks = sum(self.ia_marks) + sum(self.see_marks)
        self.obtained_credits=0
        #self.obtained_credits = self.calculate_obtained_credits()
        self.sgpa = None
        self.sgpa = self.calculate_sgpa()
        self.cgpa = None
        previous_sgpas = self.fetch_previous_sgpas()
        self.cgpa = self.calculate_cgpa(previous_sgpas)
        self.percentage = self.calculate_percentage()
        self.pass_fail = self.calculate_pass_fail()

    def calculate_pass_fail(self):
        """
        Calculates pass/fail status for each subject and handles edge cases like SCR and No Credits.
        """
        pass_fail_subjects = []
        for ia, see, credits in zip(self.ia_marks, self.see_marks, self.credits):
            if credits == 0:
                pass_fail_subjects.append("No Credits")  # Subject has no credits
            elif see == 0:
                pass_fail_subjects.append("SCR")  # Student skipped SEE
            elif ia >= 20 and see >= 18:
                pass_fail_subjects.append("Pass")  # Passed both IA and SEE
            else:
                pass_fail_subjects.append("Fail")  # Failed IA or SEE
        self.pass_fail = pass_fail_subjects
        return pass_fail_subjects
    
    def categorize(self):
        """
        Categorize the student into FCD, FC, or SC based on percentage or CGPA.

        Returns:
            str: The category of the student (FCD, FC, or SC).
        """
        if self.percentage >= 70:
            return "First Class with Distinction (FCD)"
        elif 60 <= self.percentage < 69:
            return "First Class (FC)"
        elif 35 <= self.percentage < 59:
            return "Second Class (SC)"
        elif 'Fail' in self.pass_fail:
            return 'Fail'


    def calculate_obtained_credits(self):
        obtained_credits = 0
        for ia, see, credit in zip(self.ia_marks, self.see_marks, self.credits):
            # Check eligibility for subject
            if self.credits==0:
                continue
            total_score = ia + see
            
            # Assign grade points based on total score
            if total_score >= 90:
                grade_points = 10
            elif total_score >= 80:
                grade_points = 9
            elif total_score >= 70:
                grade_points = 8
            elif total_score >= 60:
                grade_points = 7
            elif total_score >= 50:
                grade_points = 6
            elif total_score >= 40:
                grade_points = 5
            elif total_score >= 30:
                grade_points = 3
            elif total_score >= 20:
                grade_points = 2
            elif total_score >= 10:
                grade_points = 1
            else:
                grade_points = 0

                # Calculate subject credit score
            subject_credit_score = grade_points * credit
            obtained_credits += subject_credit_score
            
        self.obtained_credits = obtained_credits
        return obtained_credits
    
    def fetch_previous_sgpas(self):
        """
        Fetch the SGPAs for all previous semesters by iterating through semester numbers.
        """
        previous_sgpas = []
        semno=int(self.semester[-1])
        for sem in range(1, semno):  # Iterate through previous semesters
            try:
                student_info = fetch_student_data(self.usn,f"SEM{sem}" , self.db_path)
                if student_info:
                    # Calculate SGPA for the semester
                    ia_marks = student_info["ia_marks"]
                    see_marks = student_info["see_marks"]
                    credits = student_info["credits"]
                    sgpa = self.calculate_sgpa_for_semester(ia_marks, see_marks, credits)
                    previous_sgpas.append(sgpa)
            except Exception as e:
                print(f"Error fetching SGPA for semester {sem}: {e}")
        return previous_sgpas

    def calculate_sgpa_for_semester(self, ia_marks, see_marks, credits):
        """
        Calculate SGPA for a specific semester based on IA marks, SEE marks, and credits.
        """
        obtained_credits = 0
        total_credits = sum(credits)

        for ia, see, credit in zip(ia_marks, see_marks, credits):
            total_score = ia + see
            if total_score >= 90:
                grade_points = 10
            elif total_score >= 80:
                grade_points = 9
            elif total_score >= 70:
                grade_points = 8
            elif total_score >= 60:
                grade_points = 7
            elif total_score >= 50:
                grade_points = 6
            elif total_score >= 40:
                grade_points = 5
            elif total_score >= 30:
                grade_points = 3
            elif total_score >= 20:
                grade_points = 2
            elif total_score >= 10:
                grade_points = 1
            else:
                grade_points = 0

            subject_credit_score = grade_points * credit
            obtained_credits += subject_credit_score

        return obtained_credits / total_credits if total_credits > 0 else 0

    def calculate_sgpa(self):
        """
        Calculate SGPA for the current semester.
        """
        self.calculate_obtained_credits()
        total_credits = sum(self.credits)
        if total_credits > 0:
            self.sgpa = self.obtained_credits / total_credits
        else:
            self.sgpa = 0
        return self.sgpa

    def calculate_cgpa(self, previous_sgpas):
        """
        Calculate CGPA based on previous SGPAs and the current semester SGPA.
        """
        if self.sgpa is None:
            raise ValueError("SGPA must be calculated before CGPA.")

        all_sgpas = previous_sgpas + [self.sgpa]
        self.cgpa = sum(all_sgpas) / len(all_sgpas)
        return self.cgpa
    
    def calculate_percentage(self):
        max_total_marks = 100 * len(self.credits)
        return (self.total_marks / max_total_marks) * 100
    
    
    def display_student_info(self):
        str =( 
            f"Name: {self.name}\n"
            f"USN: {self.usn}\n"
            f"Total Marks: {self.total_marks}\n"
            f"Percentage: {self.percentage:.2f}%\n"
            f"Credits: {self.credits}\n"
            f"Credits Obtained: {self.obtained_credits}\n"
            f"SGPA: {self.sgpa}\n"
            f"CGPA: {self.cgpa:.2f}\n"
            f"Subject-wise Marks:\n"
        )

        print(str)
        #print(self.subject_codes))
        # Display subject-wise details using the subject codes
        for i,(subject_code,ia, see, credit, status) in enumerate(zip(self.subject_codes,self.ia_marks, self.see_marks, self.credits, self.pass_fail)):
            print(f" {i+1}  {subject_code}: IA Marks = {ia}, SEE Marks = {see}, Total Marks = {ia + see}, Credits = {credit}, Status = {status}")
            #self.plot_subject_marks()

    def plot_subject_marks(self):
        """Bar graph showing IA and SEE marks for each subject."""
        subjects = [f" {subject_code}" for subject_code in self.subject_codes]

        fig=plt.figure(figsize=(10, 6))
        plt.bar(subjects, self.ia_marks, label='IA Marks', color='skyblue', alpha=0.7)
        plt.bar(subjects, self.see_marks, label='SEE Marks', color='salmon', alpha=0.7, bottom=self.ia_marks)
        plt.xlabel('Subjects')
        plt.ylabel('Marks')
        plt.title(f'Subject-wise IA and SEE Marks for {self.name}')
        plt.legend()
        graph_path="Outputs/Images/plot_subject_marks.png"
        plt.savefig(graph_path)
        #plt.show()
        return fig,graph_path
        #self.plot_subject_marks() #optional

import sqlite3

class University:
    def __init__(self, db_path="Outputs/student_data.db"):
        self.db_path = db_path
        self.students = []

    def fetch_semester_tables(self):
        """
        Fetch all semester tables (e.g., SEM1, SEM2, etc.) from the database.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'SEM%'")
            tables = cursor.fetchall()
            conn.close()
            return [table[0] for table in tables]
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            return []

    def fetch_students(self, semester):
        """
        Fetch all unique USNs from a given semester table.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            query = f"SELECT DISTINCT Subject_Code_USN FROM {semester}"
            cursor.execute(query)
            usns = [row[0] for row in cursor.fetchall()]
            conn.close()
            return usns
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            return []

    def add_students(self,selected_semester):
        """
        Add all students from all semester tables into the University class.
        """
        semester_tables = self.fetch_semester_tables()
        if not semester_tables:
            print("No semester tables found in the database.")
            return

        all_usns = set()  # To ensure no duplicates
        for semester in semester_tables:
            usns = self.fetch_students(semester)
            all_usns.update(usns)

        # Create Student objects for each unique USN and add to the university's student list
        for usn in all_usns:
            try:
                # Using SEM1 as a sample semester here, it can be changed based on your requirement
                student = Student(usn, selected_semester, self.db_path)
                self.students.append(student)
            except ValueError as e:
                pass
                #print(f"Error fetching data for USN {usn}: {e}")

    def display_students(self):
        """
        Display all students and their details.
        """
        if not self.students:
            print("No students in the university.")
            return

        for student in self.students:
            print("\n" + "=" * 50)
            student.display_student_info()
            print("=" * 50)


    def calculate_all_sgpa_and_cgpa(self, previous_sgpas_list):
        """Calculates SGPA and CGPA for each student, using corresponding previous SGPA lists."""
        for student, previous_sgpas in zip(self.students, previous_sgpas_list):
            student.calculate_sgpa()  # Ensure SGPA is calculated
            student.calculate_cgpa(previous_sgpas)

    def calculate_academic_performance_by_semester(self, selected_semester, db_path="Outputs/student_data.db"):
        """
        Calculates academic performance for all students in the selected semester.

        Parameters:
            selected_semester (str): The selected semester to filter students.
            db_path (str): Path to the student database.

        Returns:
            list: List of dictionaries containing student academic details for the selected semester.
        """
        try:
            # Connect to the database and get all semester tables
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            semesters = [table[0] for table in tables if table[0].startswith('SEM')]
            conn.close()

            if not semesters:
                return [{"error": "No semester data available."}]

            semester_results = []

            for semester in sorted(semesters):  # Process semesters in order
                if semester != selected_semester:
                    continue  # Skip semesters that do not match the selected semester

                try:
                    # Fetch all students for the selected semester
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT SUBJECT_CODE_USN FROM {semester} WHERE SUBJECT_CODE_USN IS NOT NULL;")
                    student_usns = cursor.fetchall()
                    conn.close()

                    for student_usn in student_usns:
                        usn = student_usn[0]
                        # Create a Student object for the semester
                        student = Student(usn, semester, db_path=db_path)

                        # Ensure the student exists in the semester table
                        if not student.name:
                            continue  # Skip if student not found in this semester

                        # Retrieve the specific student's previous SGPAs (reset for each student)
                        #student_previous_sgpas = self.get_previous_sgpas(student.usn, selected_semester)

                        # Calculate SGPA and CGPA
                        student.calculate_sgpa()
                        student.calculate_cgpa(student.fetch_previous_sgpas())

                        # Store results
                        semester_results.append({
                            "semester": semester,
                            "usn": student.usn,
                            "name": student.name,
                            "obtained_credits": student.obtained_credits,
                            "sgpa": student.sgpa,
                            "cgpa": student.cgpa,
                            "percentage": student.percentage,
                            "ia_marks": student.ia_marks,
                            "see_marks": student.see_marks,
                            "total_marks": student.total_marks,
                            "pass_fail": student.pass_fail,
                        })

                except ValueError as e:
                    # Handle errors for a specific semester
                    semester_results.append({"semester": selected_semester, "error": str(e)})
            
            return semester_results

        except Exception as e:
            return [{"error": f"Error occurred: {str(e)}"}]
        

    def find_failed_students(self, selected_semester):
        """
        Find students who failed in the selected semester and the subjects they failed.

        Parameters:
            selected_semester (str): The semester to check for failed students.

        Returns:
            dict: A dictionary where keys are student USNs, and values are lists of subjects the student failed.
        """
        failed_students = {}

        try:
            # Fetch all students for the selected semester
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT SUBJECT_CODE_USN FROM {selected_semester}")
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                usn = row[0]
                # Create a student object for this USN and selected semester
                student = Student(usn, selected_semester, self.db_path)

                # Get the pass/fail status for all subjects of the student
                pass_fail_subjects = student.calculate_pass_fail()

                # Check each subject's pass/fail status
                for subject_index, status in enumerate(pass_fail_subjects):
                    if status == "Fail":
                        if usn not in failed_students:
                            failed_students[usn] = []
                        # Assuming that the subject codes are stored in a list
                        subject_code = student.subject_codes[subject_index]  # Example, assuming `subject_codes` is a list
                        failed_students[usn].append(subject_code)

            return failed_students

        except Exception as e:
            print(f"Error occurred while fetching failed students: {str(e)}")
            return {}

    def display_failed_students(self, selected_semester):
        failed_students = self.find_failed_students(selected_semester)

        if not failed_students:
            print("No failed students in the selected semester.")
            return

        print(f"Failed students in {selected_semester}:")
        for usn, subjects in failed_students.items():
            print(f"USN: {usn}, Subjects Failed: {', '.join(subjects)}")    


    def plot_student_totals(self, selected_semester, mode='top_n', n=10, bins=10):
        """
        Generates a bar graph or histogram of total marks for students in the selected semester.
        
        Parameters:
            selected_semester (str): The semester to filter students.
            mode (str): 'top_n' to plot top n students, 'histogram' to group into bins.
            n (int): Number of top students to display (used when mode='top_n').
            bins (int): Number of bins for grouping marks (used when mode='histogram').
            
        Returns:
            fig (matplotlib.figure.Figure): The generated figure.
            graph_path (str): Path to the saved graph image.
        """
        # Filter students by the selected semester
        filtered_students = [student for student in self.students if student.semester == selected_semester]
        
        if not filtered_students:
            print(f"No student data available for {selected_semester}.")
            return plt.figure()  # Return an empty figure if no data
        
        # Get total marks and names for the filtered semester
        student_names = [student.name for student in filtered_students]
        total_marks = [student.total_marks for student in filtered_students]

        fig = plt.figure(figsize=(12, 6))
        
        if mode == 'top_n':
            # Sort students by total marks and select the top n
            sorted_data = sorted(zip(student_names, total_marks), key=lambda x: x[1], reverse=True)[:n]
            top_names, top_marks = zip(*sorted_data)
            plt.bar(top_names, top_marks, color='orange', alpha=0.7)
            plt.xlabel('Students')
            plt.ylabel('Total Marks')
            plt.title(f'Top {n} Students in {selected_semester}')
            plt.xticks(rotation=45, ha='right')
        
        elif mode == 'histogram':
            # Create bins for total marks
            plt.hist(total_marks, bins=bins, color='orange', alpha=0.7, edgecolor='black')
            plt.xlabel('Marks Range')
            plt.ylabel('Number of Students')
            plt.title(f'Total Marks Distribution in {selected_semester}')
        
        else:
            print("Invalid mode. Choose 'top_n' or 'histogram'.")
            return plt.figure()  # Return an empty figure if mode is invalid

        # Save the plot
        plt.tight_layout()
        graph_path = "Outputs/Images/plot_student_totals.png"
        plt.savefig(graph_path)
        
        return fig, graph_path  # Return figure and saved path

    def get_toppers(self, selected_semester, n=5):
        """
        Generate a list of top N students based on total marks for the selected semester.
        
        Parameters:
            selected_semester (str): The semester to get toppers from.
            n (int): Number of toppers to list (default is 5).

        Returns:
            list: List of dictionaries containing topper details.
        """
        # Filter students by the selected semester
        filtered_students = [student for student in self.students if student.semester == selected_semester]

        if not filtered_students:
            print(f"No student data available for {selected_semester}.")
            return []

        # Sort students by total marks in descending order
        sorted_students = sorted(filtered_students, key=lambda x: x.total_marks, reverse=True)

        # Get the top N students
        toppers = sorted_students[:n]

        # Prepare topper details for display
        toppers_list = []
        for topper in toppers:
            toppers_list.append({
                "usn": topper.usn,
                "name": topper.name,
                "total_marks": topper.total_marks,
                "sgpa": topper.sgpa,
                "cgpa": topper.cgpa,
            })

        # Print topper details for debugging or console display
        print(f"\nTop {n} Students in {selected_semester}:")
        for rank, topper in enumerate(toppers_list, start=1):
            print(f"Rank {rank}: {topper['name']} (USN: {topper['usn']}, Marks: {topper['total_marks']}, SGPA: {topper['sgpa']})")

        return toppers_list
    
    
        
    
# SubjectResult class
class SubjectResult:
    def __init__(self, subject_code, semester, university):
        self.subject_code = subject_code
        self.semester = semester
        self.university = university  # Instance of the University class
        self.students_data = self.fetch_students_data()
        self.total_students = len(university.students)  # Total students for the semester
        self.present_students = len(self.students_data)
        self.absent_students = self.total_students - self.present_students
        self.pass_count, self.fail_count = self.fetch_subject_stats()
        self.fcd_count, self.fc_count, self.sc_count = self.fetch_performance_categories()
        self.pass_percentage = self.calculate_pass_percentage()

    def fetch_students_data(self):
        """
        Fetch student data for the specific subject and semester.
        """
        students_data = []
        # Filter students from the University instance by semester
        filtered_students = [student for student in self.university.students if student.semester == self.semester]
        for student in filtered_students:
            if self.subject_code in student.subject_codes:
                index = student.subject_codes.index(self.subject_code)
                students_data.append({
                    "name": student.name ,
                    "USN": student.usn,
                    "ia": student.ia_marks[index] ,
                    "see": student.see_marks[index] ,
                    "Total_Marks": student.ia_marks[index] + student.see_marks[index],
                    "Credits": student.credits[index]
                })
        return students_data

    def fetch_subject_stats(self):
        """
        Calculate pass and fail counts for the subject.
        """
        pass_count = sum(1 for student in self.students_data if (student["ia"]>=20 and student["see"]>=18))
        fail_count = self.present_students - pass_count
        for student in self.students_data:
            if (student["ia"]<20 and student["see"]<18):
                print("failed students",student["name"])
                                              
        return pass_count, fail_count

    def fetch_performance_categories(self):
        """
        Calculate counts for performance categories (FCD, FC, SC).
        """
        fcd_count = sum(1 for student in self.students_data if student["Total_Marks"] >= 70)
        fc_count = sum(1 for student in self.students_data if 60 <= student["Total_Marks"] < 70)
        sc_count = sum(1 for student in self.students_data if 50 <= student["Total_Marks"] < 60)
        return fcd_count, fc_count, sc_count

    def calculate_pass_percentage(self):
        """
        Calculate the pass percentage for the subject.
        """
        return (self.pass_count / self.present_students * 100) if self.present_students > 0 else 0

    def display_subject_results(self, output_widget=None):
        """
        Display the results for the subject, either to the console or to a widget.
        """
        result_str = (
            f"Results for Subject: {self.subject_code} in {self.semester}\n"
            f"Total Students: {self.total_students}\n"
            f"Present: {self.present_students}, Absent: {self.absent_students}\n"
            f"Passed: {self.pass_count}, Failed: {self.fail_count}\n"
            f"Pass Percentage: {self.pass_percentage:.2f}%\n"
            f"FCD (>70%): {self.fcd_count}\n"
            f"FC (60-70%): {self.fc_count}\n"
            f"SC (50-60%): {self.sc_count}\n"
            + "-" * 50 + "\n"
            f"PDF Saved"
        )

        if output_widget:
            output_widget.configure(state="normal")
            output_widget.delete("1.0", ctk.END)  # Clear previous content
            output_widget.insert(ctk.END, result_str)
            output_widget.configure(state="disabled")
        else:
            print(result_str)

    def plot_performance_pie_chart(self):
        """
        Plot a pie chart for performance distribution across categories.
        """
        import matplotlib.pyplot as plt
        categories = ['FCD (>70%)', 'FC (60-70%)', 'SC (50-60%)']
        values = [self.fcd_count, self.fc_count, self.sc_count]

        fig=plt.figure(figsize=(4, 4))
        plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140, 
                colors=['#ff9999', '#66b3ff', '#99ff99'])
        plt.title(f'Performance Distribution in {self.subject_code}')
        graph_path="Outputs/Images/performance_pie_chart.png"
        plt.savefig(graph_path)
        #plt.show()
        return fig,graph_path

    def plot_attendance_pie_chart(self):
        """
        Plot a pie chart for attendance distribution.
        """
        import matplotlib.pyplot as plt
        labels = ['Present', 'Absent']
        values = [self.present_students, self.absent_students]

        fig=plt.figure(figsize=(4, 4))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, 
                colors=['#66b3ff', '#ffcc99'])
        plt.title(f'Attendance Distribution in {self.subject_code}')
        graph_path="Outputs/Images/attendance_pie_chart.png"
        plt.savefig(graph_path)
        #plt.show()
        return fig,graph_path


'''Will have to check everything from here'''
# Function to generate and display a chart in Tkinter for Student class
def plot_student_marks(student, root):
    fig, ax = plt.subplots()
    subjects = [f"Subject {i + 1}" for i in range(len(student['ia_marks']))]
    ia_marks = student['ia_marks']
    see_marks = student['see_marks']

    ax.bar(subjects, ia_marks, label="IA Marks", color='b')
    ax.bar(subjects, see_marks, bottom=ia_marks, label="SEE Marks", color='r')
    ax.set_title("Subject-wise Marks")
    ax.set_ylabel("Marks")
    ax.legend()

    # Embed plot in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Save plot as image for PDF export
    fig.savefig("Outputs/Images/student_subject_marks.png")
    plt.close(fig)  # Close the figure to free memory

# Function to generate and display a chart for University class
def plot_university_totals(university, root):
    fig, ax = plt.subplots()
    student_names = [student.name for student in university.students]
    total_marks = [student.total_marks for student in university.students]

    ax.bar(student_names, total_marks, color='purple', alpha=0.6)
    ax.set_title("Total Marks for Each Student")
    ax.set_ylabel("Total Marks")
    ax.set_xticks(range(len(student_names)))
    ax.set_xticklabels(student_names, rotation=45)

    # Embed plot in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Save plot as image for PDF export
    fig.savefig("Outputs/Images/university_totals.png")
    plt.close(fig)  # Close the figure to free memory

# Function to generate and display a chart for SubjectResult class
def plot_subject_result_performance(subject_result, root):
    fig, ax = plt.subplots()
    categories = ['Passed', 'Failed']
    values = [subject_result.pass_count, subject_result.pass_count - len(subject_result.students_data)]

    ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
    ax.set_title(f'Performance Distribution in {subject_result.subject_name}')

    # Embed plot in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Save the plot as a PNG image for PDF export
    fig.savefig("Outputs/Images/subject_result_performance.png")

# Function to generate PDF with ReportLab

def create_student_report(student, file_path="Outputs/PDFs/student_report.pdf"):
    """
    Create a PDF report for an individual student with graphs, resembling a marks card.
    """
    # Generate a graph for subject-wise marks
    fig, ax = plt.subplots()
    ax.bar(student.subject_codes, [ia + see for ia, see in zip(student.ia_marks, student.see_marks)], color="#5E40BE")
    ax.set_title(f"Performance of {student.name}")
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Total Marks")
    graph_path = "Outputs/Images/student_graph.png"
    plt.savefig(graph_path)
    plt.close()

    # Create the PDF
    c = canvas.Canvas(file_path, pagesize=letter)

    # Add College Name and Logo
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, 780, "JSS ACADEMY OF TECHNICAL EDUCATION, BENGALURU")  # Centered title
    try:
        c.drawImage("Inputs/Images/logo.png", 50, 750, width=50, height=50)  # Add logo on the top-left
    except Exception as e:
        print(f"Warning: Could not load logo image. {e}")

    # Add Report Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 730, f"Student Marks Card")
    c.line(50, 720, 550, 720)  # Add a horizontal line below the header

    # Add Student Details
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Name: {student.name}")
    c.drawString(50, 680, f"USN: {student.usn}")
    c.drawString(50, 660, f"Semester: {student.semester}")
    c.drawString(50, 640, f"Total Marks: {student.total_marks}")
    c.drawString(50, 620, f"Percentage: {student.percentage:.2f}%")
    c.drawString(50, 600, f"SGPA: {student.sgpa:.2f}")
    c.drawString(50, 580, f"CGPA: {student.cgpa:.2f}")

    # Add Subject-wise Results Table
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 560, "Subject-wise Results:")
    y_position = 540
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Sl.No")
    c.drawString(100, y_position, "Subject Code")
    c.drawString(200, y_position, "IA Marks")
    c.drawString(300, y_position, "SEE Marks")
    c.drawString(400, y_position, "Total Marks")
    c.drawString(500, y_position, "Credits")
    c.drawString(550, y_position, "Status")
    y_position -= 20
    c.line(50, y_position + 10, 550, y_position + 10)  # Horizontal line for table header

    line_spacing = 20
    for i, (subject_code, ia, see, credit, status) in enumerate(
        zip(student.subject_codes, student.ia_marks, student.see_marks, student.credits, student.pass_fail)
    ):
        c.drawString(50, y_position, str(i + 1))
        c.drawString(100, y_position, subject_code)
        c.drawString(200, y_position, str(ia))
        c.drawString(300, y_position, str(see))
        c.drawString(400, y_position, str(ia + see))
        c.drawString(500, y_position, str(credit))
        c.drawString(550, y_position, status)
        y_position -= line_spacing

        # Start a new page if space runs out
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 10)  # Reset font
            y_position = 750  # Reset position for the new page

    # Add Performance Graph
    c.drawImage(graph_path, 100, 100, width=400, height=200)
    # Finalize PDF
    c.save()
    print(f"Student Marks Card PDF saved successfully as {pathlib.Path(file_path).resolve()}")


def create_university_report(university, selected_semester, file_path="Outputs/PDFs/university_report.pdf"):
    """
    Create a PDF report for the university's academic performance with graphs.
    """
    # Generate a graph for SGPA distribution
    sgpa_list = [student.sgpa for student in university.students if student.semester == selected_semester]
    fig, ax = plt.subplots()
    ax.hist(sgpa_list, bins=10, range=(0, 10), color='skyblue', edgecolor='black')
    ax.set_title("SGPA Distribution")
    ax.set_xlabel("SGPA")
    ax.set_ylabel("Number of Students")
    graph_path = "Outputs/Images/university_graph.png"
    plt.savefig(graph_path)
    plt.close()

    # Generate the second graph
    gpath = university.plot_student_totals(selected_semester, mode='histogram', n=10, bins=10)[1]

    # Create the PDF
    c = canvas.Canvas(file_path, pagesize=letter)

    # Add College Name and Logo
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 730, "JSS ACADEMY OF TECHNICAL EDUCATION, BENGALURU")
    
    try:
        # Add logo to the top left
        logo = Image("Inputs/Images/logo.png", width=50, height=50)
        c.drawImage("Inputs/Images/logo.png", 50, 710, width=50, height=50)
    except Exception as e:
        print(f"Warning: Could not load logo image. {e}")

    # Title for University Report
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 680, f"University Report for {selected_semester}")

    # Insert the bar chart for SGPA distribution
    c.drawImage(graph_path, 100, 500, width=400, height=200)

    # Insert the second chart
    c.drawImage(gpath, 100, 300, width=400, height=200)

    # Add a header for student details
    c.setFont("Helvetica", 12)
    c.drawString(100, 270, f"=== Academic Performance for Semester: {selected_semester} ===")

    y = 250  # Start below the chart area
    for student in university.students:
        if student.semester == selected_semester:
            y -= 20  # Start below the previous paragraph or reset for a new page

            if y < 100:  # Check if there's enough space; if not, start a new page
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 750  # Reset y position for the new page

            # Add the student's details in a paragraph-style format
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, f"USN: {student.usn} | Name: {student.name}")
            y -= 15  # Reduced space between student header and details

            c.setFont("Helvetica", 12)
            details = (
                f"Total Marks: {student.total_marks}\n"
                f"Percentage: {student.percentage:.2f}%\n"
                f"SGPA: {student.sgpa:.2f}, CGPA: {student.cgpa:.2f}\n"
                f"Pass/Fail Status: {student.pass_fail}\n"
            )

            # Split the details into lines and render them
            for line in details.split("\n"):
                if y < 100:  # Start a new page if space runs out
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750

                c.drawString(50, y, line.strip())
                y -= 15  # Reduced spacing between lines

            y -= 20  # Reduced space before the next student's details

            if y < 100:  # Start a new page if there's not enough space for the next student
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 750

    # Save the PDF
    c.save()
    print(f"University Report PDF saved successfully as {pathlib.Path(file_path).resolve()}")

from fpdf.enums import XPos, YPos  # Import enums for positioning

def create_toppers_list_pdf(toppers, selected_semester, file_path="Outputs/PDFs/toppers_list.pdf"):
    """
    Generates a PDF for the toppers list.

    Parameters:
        toppers (list): List of dictionaries containing toppers' details.
        selected_semester (str): The semester for which the toppers list is generated.
        file_path (str): The path where the PDF will be saved.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)  # Use Helvetica explicitly

    # Title
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, f"Toppers List - {selected_semester}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(10)  # Add some vertical space

    # Table Header
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(10, 10, "No.", border=1, align="C")
    pdf.cell(40, 10, "USN", border=1, align="C")
    pdf.cell(80, 10, "Name", border=1, align="C")
    pdf.cell(30, 10, "Percentage", border=1, align="C")
    pdf.ln()

    # Table Rows
    pdf.set_font("Helvetica", size=12)
    for i, topper in enumerate(toppers, start=1):
        pdf.cell(10, 10, str(i), border=1, align="C")
        pdf.cell(40, 10, topper['usn'], border=1, align="C")
        pdf.cell(80, 10, topper['name'], border=1, align="L")
        pdf.cell(30, 10, f"{topper['percentage']:.2f}%", border=1, align="C")
        pdf.ln()

    # Save PDF
    pdf.output(file_path)
    print(f"Toppers list saved to {pathlib.Path(file_path).resolve()}")

def create_subject_report(subject_result, file_path="Outputs/PDFs/subject_report.pdf"):
    """
    Create a PDF report for subject-wise performance with graphs.
    """
    # Generate a graph for subject-wise pass/fail count
    labels = ['Pass', 'Fail']
    counts = [subject_result.pass_count, subject_result.fail_count]
    fig, ax = plt.subplots()
    ax.bar(labels, counts, color=['green', 'red'])
    ax.set_title(f"Performance in {subject_result.subject_code}")
    ax.set_ylabel("Number of Students")
    graph_path = "Outputs/Images/subject_graph.png"
    plt.savefig(graph_path)
    plt.close()

    # Get the pie chart images for performance and attendance
    perpath = subject_result.plot_performance_pie_chart()[1]
    attpath = subject_result.plot_attendance_pie_chart()[1]

    # Create the PDF
    c = canvas.Canvas(file_path, pagesize=letter)
    
    # Add College Name and Logo
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "JSS ACADEMY OF TECHNICAL EDUCATION, BENGALURU")
    
    try:
        # Add logo to the top left
        logo = Image("Inputs/Images/logo.png", width=50, height=50)
        c.drawImage("Inputs/Images/logo.png", 50, 735, width=50, height=50)
    except Exception as e:
        print(f"Warning: Could not load logo image. {e}")
    
    # Title for Subject Report
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 715, f"Subject Report for {subject_result.subject_code} ({subject_result.semester})")

    # Insert the bar chart for performance
    c.drawImage(graph_path, 100, 500, width=400, height=200)
    
    # Insert pie charts for performance and attendance
    c.drawImage(perpath, 100, 300, width=200, height=200)
    c.drawImage(attpath, 300, 300, width=200, height=200)

    # Insert the subject performance data
    c.setFont("Helvetica", 12)
    c.drawString(100, 280, f"Total Students: {subject_result.total_students}")
    c.drawString(100, 260, f"Present: {subject_result.present_students} Absent: {subject_result.absent_students}")
    c.drawString(100, 240, f"Pass: {subject_result.pass_count}, Fail: {subject_result.fail_count}")
    c.drawString(100, 220, f"Pass Percentage: {subject_result.pass_percentage:.2f}%")
    c.drawString(100, 200, f"FCD (>70%): {subject_result.fcd_count}")
    c.drawString(100, 180, f"FC (60-70%): {subject_result.fc_count}")
    c.drawString(100, 160, f"SC (50-60%): {subject_result.sc_count}")
    
    # Save the PDF
    c.save()
    print(f"Subject Report PDF saved successfully as {pathlib.Path(file_path).resolve()}")

def generate_sem_pdf(selected_semester, university, semester_subject_mapping, output_path):
    try:
        subjects = semester_subject_mapping.get(selected_semester, [])
        if not subjects:
            raise ValueError("No subjects found for the selected semester.")
        
        doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        elements = []

        styles = getSampleStyleSheet()

       
        # Add logo
        try:
            logo = Image("Inputs/Images/logo.png", width=50, height=50)  # Adjust size as needed
            elements.append(logo)
        except Exception as e:
            print(f"Warning: Could not load logo image. {e}")

         # Add college name
        title = Paragraph(f"<b>{"JSS ACADEMY OF TECHNICAL EDUCATION, BENGALURU"}</b>", styles['Title'])
        elements.append(title)


        # Add a gap
        elements.append(Spacer(1, 20))

        # Add semester title
        sem_title = Paragraph(f"<b>Semester-Wise Results: {selected_semester}</b>", styles['Heading2'])
        elements.append(sem_title)
        elements.append(Spacer(1, 12))

        headers = ["Subject Code", "Total Students", "Present", "Absent", "Pass %", "FCD", "FC", "SC", "Fail"]
        column_widths = [80, 90, 70, 70, 60, 50, 50, 50, 50]  # Adjust column widths to fit

        data = [headers]

        # Process each subject
        for subject_code in subjects:
            subject_result = SubjectResult(subject_code, selected_semester, university)
            row = [
                subject_code,
                subject_result.total_students,
                subject_result.present_students,
                subject_result.absent_students,
                f"{subject_result.pass_percentage:.2f}%",
                subject_result.fcd_count,
                subject_result.fc_count,
                subject_result.sc_count,
                subject_result.fail_count,
            ]
            data.append(row)

        # Create the table
        table = Table(data, colWidths=column_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),  # Adjust font size for better fit
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(table)

        # Add totals summary
        elements.append(Spacer(1, 12))

        totals_headers = ["Total Students", "FCD", "FC", "SC", "Fail", "Pass %"]
        total_students = len([student for student in university.students if student.semester == selected_semester])
        total_fcd = sum(student.categorize() == "First Class with Distinction (FCD)" for student in university.students if student.semester == selected_semester)
        total_fc = sum(student.categorize() == "First Class (FC)" for student in university.students if student.semester == selected_semester)
        total_sc = sum(student.categorize() == "Second Class (SC)" for student in university.students if student.semester == selected_semester)
        total_fail = sum("Fail" in student.pass_fail for student in university.students if student.semester == selected_semester)
        total_present = total_students - total_fail
        pass_percentage = (total_present / total_students) * 100 if total_students > 0 else 0.0

        totals_data = [
            totals_headers,
            [
                total_students,
                total_fcd,
                total_fc,
                total_sc,
                total_fail,
                f"{pass_percentage:.2f}%",
            ],
        ]

        totals_table = Table(totals_data, colWidths=column_widths[:len(totals_headers)])
        totals_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),  # Adjust font size
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(totals_table)
        elements.append(Spacer(1, 20))

        result = university.calculate_academic_performance_by_semester(selected_semester, db_path=db_path)
        toppers = sorted(result, key=lambda x: x['percentage'], reverse=True)[:10]  # Get top 10 students by percentage

        topper_title = Paragraph(f"<b> Toppers  {selected_semester}</b>", styles['Heading2'])
        elements.append(topper_title)
        elements.append(Spacer(1, 12))


        topper_headers = ["No", "USN", "Name", "Percentage"]
        column_widths = [80, 90, 130, 70]  # Adjust column widths to fit

        topper_data = [topper_headers]

        # Process each subject
        for i, topper in enumerate(toppers, start=1):
            
            row1 = [
                str(i),
                topper['usn'],
                topper['name'],
                topper['percentage'],
            ]
            topper_data.append(row1)

        # Create the table
        topper_table = Table(topper_data, colWidths=column_widths)
        topper_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),  # Adjust font size for better fit
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(topper_table)


        # Display failed students
        
        failed_students = university.find_failed_students(selected_semester)
        fail_title = Paragraph(f"<b> Slow Learners  {selected_semester}</b>", styles['Heading2'])
        elements.append(fail_title)
        elements.append(Spacer(1, 12))


        fail_headers = ["USN", "Subjects failed"]
        column_widths = [90, 130]  # Adjust column widths to fit

        fail_data = [fail_headers]

        for usn, subjects in failed_students.items():
            row2 = [
                f"{usn}",
                f"{subjects}",
            ]
            fail_data.append(row2)

         # Create the table
        fail_table = Table(fail_data, colWidths=column_widths)
        fail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),  # Adjust font size for better fit
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(fail_table)


        # Build the PDF
        doc.build(elements)
        print(f"PDF report generated successfully at {pathlib.Path(output_path).resolve()}.")
    except Exception as e:
        print(f"Error generating PDF: {e}")



#temp function to print table names
def print_table_names(db_path="Outputs/student_data.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Print table names
        print("Tables in the database:")
        for table in tables:
            print(table[0])

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        conn.close()

# Example usage
#print_table_names()

#temp function to print table columns

def print_column_names(db_path="Outputs/student_data.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Loop through each table and get column names
        for table in tables:
            table_name = table[0]
            print(f"/nColumns in table '{table_name}':")
            
            # Get column names for the current table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            for column in columns:
                print(column[1])  # Column name is the second item in each row of PRAGMA result

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        conn.close()

# Example usage
print_column_names()

#temp function to print Student class  dat
def print_student_data_by_usn(usn, db_path="Outputs/student_data.db"):
    try:
        # Get list of semesters from the database (filter for tables that start with 'SEM')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        semesters = [table[0] for table in tables if table[0].startswith('SEM')]  # Filter only tables starting with "SEM"
        conn.close()

        # Check if there are any semesters to display
        if not semesters:
            print("No semester data available.")
            return

        # Loop through each semester and fetch student data
        for semester in semesters:
            # Fetch student data for the given USN and semester
            student_info = fetch_student_data(usn, semester, db_path)
            if student_info:
                # Create a Student object for the current semester
                student = Student(usn=usn, semester=semester, db_path=db_path)

                # Display the student's information for the current semester
                print(f"\nData for {semester}:")
                student.display_student_info()  # Using the display method from the Student class

            else:
                print(f"No data found for USN {usn} in {semester}.")

    except Exception as e:
        print(f"Error occurred: {e}")

# Usage
usn_to_search = "1JS22CS006"  # Replace with the actual USN you want to look up
print_student_data_by_usn(usn_to_search)

#temp function to print university class data
def test_university_class(selected_semester, db_path="Outputs/student_data.db"):
    try:
        # Initialize the University class
        university = University(db_path=db_path)

        # Add all students from the database
        university.add_students(selected_semester)

        # Display all students and their semester details (optional, for debugging)
        university.display_students()

        # Calculate academic performance for all students in the selected semester
        result = university.calculate_academic_performance_by_semester(selected_semester, db_path=db_path)

        # Display the results in the terminal (optional, for debugging)
        print(f"\n=== Calculating Academic Performance for Semester: {selected_semester} ===")
        print(result)
        
        # Plot total marks for all students
        print("\n=== Plotting Total Marks for All Students ===")
        fig = university.plot_student_totals(selected_semester)
        #fig.show()

    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage
test_university_class(selected_semester="SEM3", db_path="Outputs/student_data.db")

#toppers list
# Create an instance of University and load students
university = University(db_path="Outputs/student_data.db")
selected_semester = "SEM1"
university.add_students(selected_semester)

# Generate the toppers list
toppers_list = university.get_toppers(selected_semester, n=3)  # Get top 3 students

# Further actions with toppers_list (e.g., display in GUI or save to a file)

#test failed students
university = University(db_path="Outputs/student_data.db")
selected_semester = "SEM1"
university.display_failed_students(selected_semester)

#test subjectresult class
university = University("Outputs/student_data.db")
university.add_students(selected_semester="SEM1")

subject_result = SubjectResult("BMATS101", "SEM1", university)

# Display results
subject_result.display_subject_results()
subject_result.fetch_subject_stats()
# Plot charts
subject_result.plot_performance_pie_chart()
subject_result.plot_attendance_pie_chart()

#test pdf
'''student = Student(usn="1JS22CS001", semester="SEM1", db_path="Outputs/student_data.db")
create_student_report(student, file_path="student_report_1JS22CS001.pdf")

university = University(db_path="Outputs/student_data.db")
university.add_students(selected_semester="SEM1")
create_university_report(university, selected_semester="SEM1", file_path="university_report_SEM1.pdf")

university = University(db_path="Outputs/student_data.db")
university.add_students(selected_semester="SEM1")
subject_result = SubjectResult(subject_code="BMATS101", semester="SEM1", university=university)
create_subject_report(subject_result, file_path="subject_report_BMATS101.pdf")'''

#ctkinter
def test_university_class(selected_semester, show_toppers=False, show_failed=False):
    try:
        db_path = "Outputs/student_data.db"
        university = University(db_path=db_path)
        university.add_students(selected_semester)

        # Calculate academic performance for all students in the selected semester
        result = university.calculate_academic_performance_by_semester(selected_semester, db_path=db_path)

        # Clear and update the text display in the "Overall Result" tab
        overall_result_text.configure(state="normal")
        overall_result_text.delete("1.0", ctk.END)

        if show_toppers:
            # Display toppers' list
            overall_result_text.insert(ctk.END, f"=== Toppers List for Semester: {selected_semester} ===\n\n")
            toppers = sorted(result, key=lambda x: x['percentage'], reverse=True)[:10]  # Get top 10 students by percentage
            for i, topper in enumerate(toppers, start=1):
                overall_result_text.insert(ctk.END, f"{i}. USN: {topper['usn']}\n Name: {topper['name']}\nTotal marks: {topper['total_marks']} \tPercentage: {topper['percentage']:.2f}%\n sgpa: {topper['sgpa']:.2f}%\tcgpa: {topper['cgpa']:.2f}%\n\n")
            overall_result_text.insert(ctk.END, "-" * 50 + "\n")
            # Create PDF for toppers
            create_toppers_list_pdf(toppers, selected_semester, file_path=f"Outputs/PDFs/{selected_semester}_toppers_list.pdf")
        elif show_failed:
            # Display failed students
            overall_result_text.insert(ctk.END, f"=== Failed Students List for Semester: {selected_semester} ===\n\n")
            failed_students = university.find_failed_students(selected_semester)
            for usn, subjects in failed_students.items():
                overall_result_text.insert(ctk.END, f"USN: {usn}, Subjects Failed: {', '.join(subjects)}\n")
            overall_result_text.insert(ctk.END, "-" * 50 + "\n")
        else:
            # Display academic performance
            overall_result_text.insert(ctk.END, f"=== Academic Performance for Semester: {selected_semester} ===\n\n")
            for sem_result in result:
                overall_result_text.insert(ctk.END, f"USN: {sem_result['usn']}\n")  # Print USN
                overall_result_text.insert(ctk.END, f"Name: {sem_result['name']}\n")
                
                overall_result_text.insert(ctk.END, f"IA Marks: {sem_result['ia_marks']}\n")
                overall_result_text.insert(ctk.END, f"SEE Marks: {sem_result['see_marks']}\n")
                overall_result_text.insert(ctk.END, f"Total Marks: {sem_result['total_marks']}\n")
                overall_result_text.insert(ctk.END, f"Percentage: {sem_result['percentage']:.2f}%\n")
                overall_result_text.insert(ctk.END, f"Obtained Credits: {sem_result['obtained_credits']}\n")
                overall_result_text.insert(ctk.END, f"SGPA: {sem_result['sgpa']:.2f}, CGPA: {sem_result['cgpa']:.2f}\n")
                
                overall_result_text.insert(ctk.END, f"Pass/Fail Status: {', '.join(sem_result['pass_fail'])}\n")
                overall_result_text.insert(ctk.END, "-" * 50 + "\n")

        overall_result_text.configure(state="disabled")

        if not show_toppers and not show_failed:
            # Plot total marks for all students in the selected semester
            fig = university.plot_student_totals(selected_semester, mode='histogram', n=10, bins=10)[0]
            fig.set_size_inches(10, 6)
            fig.set_dpi(65)
            for widget in overall_result_graph.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=overall_result_graph)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)

            create_university_report(university, selected_semester, file_path=f"Outputs/PDFs/{selected_semester}_report.pdf")

            # Switch to the "Overall Result" tab
            tabview.set("Overall Result")

    except Exception as e:
        overall_result_text.configure(state="normal")
        overall_result_text.insert(ctk.END, f"Error: {str(e)}\n")
        overall_result_text.configure(state="disabled")


def display_student_info(usn, semester):
    try:
        student = Student(usn=usn, semester=semester, db_path="Outputs/student_data.db")
        
        info_text.configure(state="normal")
        info_text.delete("1.0", ctk.END)
        
        info_text.insert(ctk.END, f"Name: {student.name}\n")
        info_text.insert(ctk.END, f"USN: {student.usn}\n")
        info_text.insert(ctk.END, f"Total Marks: {student.total_marks}\n")
        info_text.insert(ctk.END, f"Percentage: {student.percentage:.2f}%\n")
        info_text.insert(ctk.END, f"Credits Obtained: {student.obtained_credits}\n")
        info_text.insert(ctk.END, f"SGPA: {student.sgpa:.2f}\n")
        info_text.insert(ctk.END, f"CGPA: {student.cgpa:.2f}\n")
        info_text.insert(ctk.END, "Subject-wise Marks:\n")

        for i, (subject_code,ia, see, credit, status) in enumerate(zip(student.subject_codes,student.ia_marks, student.see_marks, student.credits, student.pass_fail), 1):
            info_text.insert(ctk.END, f"  {i} {subject_code}: IA Marks = {ia}, SEE Marks = {see}, Total Marks = {ia + see}, Credits = {credit}, Status = {status}\n")
        
        fig = student.plot_subject_marks()[0]
        fig.set_size_inches(10, 6)
        fig.set_dpi(65)
        for widget in student_info_graph.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=student_info_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        create_student_report(student, file_path=f"Outputs/PDFs/{student.name}_{semester}_report.pdf")

        info_text.configure(state="disabled")

    except Exception as e:
        info_text.configure(state="normal")
        info_text.insert(ctk.END, f"Error: {str(e)}\n")
        info_text.configure(state="disabled")


def on_submit():
    usn = usn_entry.get()
    semester = semester_dropdown.get()
    display_student_info(usn, semester)
    tabview.set("Student Info")

# Function to handle subject-wise results
def display_subjectwise_result():
    try:
        selected_semester = subjectwise_semester_dropdown.get()
        selected_subject = subjectwise_subject_dropdown.get()

        if not selected_semester or not selected_subject:
            raise ValueError("Please select both semester and subject code.")

        university = University("Outputs/student_data.db")
        university.add_students(selected_semester=selected_semester)

        subject_result = SubjectResult(selected_subject, selected_semester, university)

        # Clear and update the text display
        subjectwise_result_text.configure(state="normal")
        subjectwise_result_text.delete("1.0", ctk.END)
        subjectwise_result_text.insert(ctk.END, f"=== Subject-wise Results for {selected_subject} ({selected_semester}) ===\n\n")
        create_subject_report(subject_result, file_path=f"Outputs/PDFs/subject_report_{selected_semester}_{selected_subject}.pdf")
        subject_result.display_subject_results(output_widget=subjectwise_result_text)
        subjectwise_result_text.configure(state="disabled")

        

        # Plot charts
        for widget in subjectwise_result_graph.winfo_children():
            widget.destroy()

        # Plot Performance Chart
        pie_chart1 = subject_result.plot_performance_pie_chart()[0]
        pie_chart1.set_size_inches(10, 6)
        pie_chart1.set_dpi(70)
        canvas1 = FigureCanvasTkAgg(pie_chart1, master=subjectwise_result_graph)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, ipadx=0.5, ipady=0.5, sticky="nsew")

        # Plot Attendance Chart
        pie_chart2 = subject_result.plot_attendance_pie_chart()[0]
        pie_chart2.set_size_inches(10, 6)
        pie_chart2.set_dpi(70)
        canvas2 = FigureCanvasTkAgg(pie_chart2, master=subjectwise_result_graph)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, ipadx=0.1, ipady=0.1, sticky="nsew")
        
        

    except Exception as e:
        subjectwise_result_text.configure(state="normal")
        subjectwise_result_text.insert(ctk.END, f"Error: {str(e)}\n")
        subjectwise_result_text.configure(state="disabled")


# Mapping for semesters and subject codes
semester_subject_mapping = {
    "SEM1": ["BMATS101", "BCHES102", "BCEDK103", "BENGK106", "BICOK107", "BIDTK158", "BESCK104A", "BETCK105H"],
    "SEM2": ["BMAT201", "BPHYS202", "BPOPS203", "BPWSK206", "BKSKK207", "BSFHK258", "BPLCK205B", "BESCK204C"],
    "SEM3": ["BCS301", "BCS302", "BCS303", "BCS304", "BCSL305", "BSCK307", "BNSK359", "BCS306A", "BCS358D"],
    "SEM4": ["BCS401", "BCS402", "BCS403", "BCSL404", "BBOC407", "BUHK408", "BPEK459 (Physical Education)/BNSK459(NSS)", "BCS405B"]
}

# Function to update subject dropdown based on the selected semester
def update_subject_dropdown(selected_semester):
    # Clear the subject code dropdown
    subjectwise_subject_dropdown.set("")  # Reset selection
    # Update values based on selected semester
    if selected_semester in semester_subject_mapping:
        subjectwise_subject_dropdown.configure(values=semester_subject_mapping[selected_semester])


# Function to display semester-wise results
def display_semesterwise_results(selected_semester):
    try:
        if not selected_semester:
            raise ValueError("Please select a semester.")

        university = University("Outputs/student_data.db")
        university.add_students(selected_semester=selected_semester)

        subjects = semester_subject_mapping.get(selected_semester, [])
        if not subjects:
            raise ValueError("No subjects found for the selected semester.")

        for widget in semesterwise_result_table.winfo_children():
            widget.destroy()

        headers = ["Subject Code", "Total Students", "Present", "Absent", "Pass %", "FCD", "FC", "SC", "Fail"]

        # Header row
        for col_index, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                semesterwise_result_table,
                text=header,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="center",
                fg_color="grey",  # Navy blue background
                text_color="black",  # White text for contrast
                corner_radius=3,
            )
            header_label.grid(row=0, column=col_index, padx=0.5, pady=0.5, sticky="nsew")

        total_present = total_absent = total_fcd = total_fc = total_sc = total_fail = total_students = 0

        for student in university.students:
            if student.semester != selected_semester:
                continue

            total_students += 1
            student.calculate_pass_fail()
            category = student.categorize()

            if category == "First Class with Distinction (FCD)":
                total_fcd += 1
            elif category == "First Class (FC)":
                total_fc += 1
            elif category == "Second Class (SC)":
                total_sc += 1

            fail_count = student.pass_fail.count("Fail")
            if fail_count > 0:
                total_fail += 1
                total_absent += 1
            else:
                total_present += 1

        pass_percentage = (
            (total_students-total_fail) / total_students * 100
            if total_students > 0
            else 0.0
        )

        # Data rows
        for row_index, subject_code in enumerate(subjects, start=1):
            subject_result = SubjectResult(subject_code, selected_semester, university)
            data = [
                subject_code,
                subject_result.total_students,
                subject_result.present_students,
                subject_result.absent_students,
                f"{subject_result.pass_percentage:.2f}%",
                subject_result.fcd_count,
                subject_result.fc_count,
                subject_result.sc_count,
                subject_result.fail_count,
            ]

            # Alternate row colors for readability
            row_bg = "black" if row_index % 2 == 0 else "black"  # Light blue shades
            for col_index, value in enumerate(data):
                data_label = ctk.CTkLabel(
                    semesterwise_result_table,
                    text=value,
                    font=ctk.CTkFont(size=12),
                    anchor="center",
                    fg_color=row_bg,  # Subtle color difference
                    text_color="white",
                    #corner_radius=8,
                )
                data_label.grid(row=row_index, column=col_index, padx=0.5, pady=0.5, sticky="nsew")

        # Totals row
        total_headers = [
            "Total Students Appeared",
            "No. of FCD",
            "No. of FC",
            "No. of SC",
            "No. of Fail",
            "Total pass %",
        ]
        total_values = [
            total_students,
            total_fcd,
            total_fc,
            total_sc,
            total_fail,
            f"{pass_percentage:.2f}",
        ]

        for col_index, header in enumerate(total_headers):
            header_label = ctk.CTkLabel(
                semesterwise_result_table,
                text=header,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="center",
                fg_color="grey",  # Light green background for totals
                text_color="black",
                corner_radius=3,
            )
            header_label.grid(row=len(subjects) + 1, column=col_index, padx=0.5, pady=0.5, sticky="nsew")

        for col_index, value in enumerate(total_values):
            value_label = ctk.CTkLabel(
                semesterwise_result_table,
                text=value,
                font=ctk.CTkFont(size=12),
                anchor="center",
                fg_color="black", # Lighter green shade
                text_color="white", 
                #corner_radius=8,
            )
            value_label.grid(row=len(subjects) + 2, column=col_index, padx=0.5, pady=0.5, sticky="nsew")

        # Uniform grid configuration
        for col_index in range(len(headers)):
            semesterwise_result_table.grid_columnconfigure(col_index, weight=1)

        for row_index in range(len(subjects) + 3):
            semesterwise_result_table.grid_rowconfigure(row_index, weight=1)

        generate_sem_pdf(selected_semester, university, semester_subject_mapping, output_path=f"Outputs/PDFs/{selected_semester}_results.pdf")
    except Exception as e:
        # Display error message using messagebox
        ctk.messagebox.showerror("Error", str(e))

def display_semesterwise_results_console(selected_semester):
    try:
        if not selected_semester:
            raise ValueError("Please select a semester.")

        university = University("Outputs/student_data.db")
        university.add_students(selected_semester=selected_semester)

        subjects = semester_subject_mapping.get(selected_semester, [])
        if not subjects:
            raise ValueError("No subjects found for the selected semester.")

        headers = ["Subject Code", "Total Students", "Present", "Absent", "Pass %", "FCD", "FC", "SC", "Fail"]
        
        # Print header
        print("\nSemester-Wise Results")
        print("=" * 80)
        print("{:<15} {:<15} {:<10} {:<10} {:<10} {:<5} {:<5} {:<5} {:<5}".format(*headers))
        print("-" * 80)

        total_present = total_absent = total_fcd = total_fc = total_sc = total_fail = total_students = 0

        # Process students
        for student in university.students:
            if student.semester != selected_semester:
                continue

            total_students += 1
            student.calculate_pass_fail()
            category = student.categorize()

            if category == "First Class with Distinction (FCD)":
                total_fcd += 1
            elif category == "First Class (FC)":
                total_fc += 1
            elif category == "Second Class (SC)":
                total_sc += 1

            fail_count = student.pass_fail.count("Fail")
            if fail_count > 0:
                total_fail += 1
                total_absent += 1
            else:
                total_present += 1

        pass_percentage = (
            (total_fcd + total_fc + total_sc) / total_students * 100
            if total_students > 0
            else 0.0
        )

        # Print data rows
        for subject_code in subjects:
            subject_result = SubjectResult(subject_code, selected_semester, university)
            data = [
                subject_code,
                subject_result.total_students,
                subject_result.present_students,
                subject_result.absent_students,
                f"{subject_result.pass_percentage:.2f}%",
                subject_result.fcd_count,
                subject_result.fc_count,
                subject_result.sc_count,
                subject_result.fail_count,
            ]
            print("{:<15} {:<15} {:<10} {:<10} {:<10} {:<5} {:<5} {:<5} {:<5}".format(*data))

        # Print totals
        print("-" * 80)
        total_headers = [
            "Total Students",
            "FCD",
            "FC",
            "SC",
            "Fail",
            "Pass %",
        ]
        total_values = [
            total_students,
            total_fcd,
            total_fc,
            total_sc,
            total_fail,
            f"{pass_percentage:.2f}%",
        ]

        print("{:<15} {:<15} {:<10} {:<10} {:<10} {:<5}".format(*total_headers))
        print("{:<15} {:<15} {:<10} {:<10} {:<10} {:<5}".format(*total_values))
        print("=" * 80)

        # Optionally, generate a PDF report
        #generate_sem_pdf(selected_semester, university, semester_subject_mapping, output_path=f"{selected_semester}_results.pdf")
    except Exception as e:
        print(f"Error: {e}")


# Call the function with a valid semester
#display_semesterwise_results_console("SEM1")


# Main window setup
root = ctk.CTk()
root.title("JSS Academy Of Technical Education Bengaluru-560060")
root.geometry("900x600")

title_label = ctk.CTkLabel(root, text="JSS Academy Of Technical Education Bengaluru-560060", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

tabview = ctk.CTkTabview(root, width=850, height=500)
tabview.pack(expand=True, fill="both", padx=20, pady=10)

# Home Tab
home_tab = tabview.add("Home")
home_tab.grid_rowconfigure([0, 1, 2, 3], weight=1)  # Configure rows for alignment
home_tab.grid_columnconfigure(0, weight=1)  # Center align content in the column

# Buttons in Home Tab (closer spacing)
student_result_button = ctk.CTkButton(home_tab, text="Student Result", command=lambda: tabview.set("Enter USN"))
student_result_button.grid(row=0, rowspan=4,column=0, pady=5, padx=20, sticky="n")


overall_result_button = ctk.CTkButton(home_tab, text="Overall Result", command=lambda: tabview.set("Overall Result"))
overall_result_button.grid(row=1,rowspan=4, column=0, pady=5, padx=20, sticky="n")

subjectwise_result_button = ctk.CTkButton(home_tab, text="Subject-wise Result", command=lambda: tabview.set("Subject-wise Result"))
subjectwise_result_button.grid(row=2, rowspan=4,column=0, pady=5, padx=20, sticky="n")

sem_result_button = ctk.CTkButton(home_tab, text="Sem Result", command=lambda: tabview.set("Sem Result"))
sem_result_button.grid(row=3, rowspan=4,column=0, pady=5, padx=20, sticky="n")

# Enter USN Tab
usn_tab = tabview.add("Enter USN")
usn_tab.grid_rowconfigure(0, weight=1)
usn_tab.grid_columnconfigure(0, weight=1)

usn_label = ctk.CTkLabel(usn_tab, text="Enter USN:")
usn_label.grid(row=0, column=0, pady=10)

usn_entry = ctk.CTkEntry(usn_tab)
usn_entry.grid(row=1, column=0, pady=10)

semester_label = ctk.CTkLabel(usn_tab, text="Select Semester:")
semester_label.grid(row=2, column=0, pady=10)

semester_dropdown = ctk.CTkOptionMenu(usn_tab, values=["SEM1", "SEM2", "SEM3", "SEM4", "SEM5", "SEM6", "SEM7", "SEM8"])
semester_dropdown.grid(row=3, column=0, pady=10)

submit_button = ctk.CTkButton(usn_tab, text="Submit", command=on_submit)
submit_button.grid(row=4, column=0, pady=20)

# Overall Result Tab
# Overall Result Tab
overall_result_tab = tabview.add("Overall Result")
overall_result_tab.grid_rowconfigure(0, weight=1)
overall_result_tab.grid_rowconfigure(1, weight=1)
overall_result_tab.grid_columnconfigure(0, weight=1)
overall_result_tab.grid_columnconfigure(1, weight=1)

semester_label_overall = ctk.CTkLabel(overall_result_tab, text="Select Semester for Academic Performance:")
semester_label_overall.grid(row=0, column=0, pady=10, columnspan=2)

semester_dropdown_overall = ctk.CTkOptionMenu(overall_result_tab, values=["SEM1", "SEM2", "SEM3", "SEM4", "SEM5", "SEM6", "SEM7", "SEM8"])
semester_dropdown_overall.grid(row=1, column=0, pady=10, columnspan=2)

overall_submit_button = ctk.CTkButton(overall_result_tab, text="Submit and save PDF", command=lambda: test_university_class(semester_dropdown_overall.get()))
overall_submit_button.grid(row=2, column=0, pady=10, columnspan=2)

# Add a button for generating the toppers list in the same tab
toppers_button = ctk.CTkButton(
    overall_result_tab,
    text="Toppers List",
    command=lambda: test_university_class(semester_dropdown_overall.get(), show_toppers=True)
)
toppers_button.grid(row=2, column=1, pady=10)

overall_result_text = ctk.CTkTextbox(overall_result_tab, width=400, height=300)
overall_result_text.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
overall_result_text.configure(state="disabled")

overall_result_graph = ctk.CTkFrame(overall_result_tab, width=400, height=300)
overall_result_graph.grid(row=3, column=1, pady=10, padx=10, sticky="nsew")

# Add a button for showing failed students and their subjects
failed_button = ctk.CTkButton(
    overall_result_tab,
    text="Failed Students List",
    command=lambda: test_university_class(semester_dropdown_overall.get(), show_failed=True)
)
failed_button.grid(row=2, column=2, pady=10)

#semwise
  # For Treeview if CTkTreeview is unavailable

# Define the tab
semwise_tab = tabview.add("Sem Result")
semwise_tab.grid_rowconfigure(0, weight=1)
semwise_tab.grid_rowconfigure(1, weight=1)
semwise_tab.grid_rowconfigure(3, weight=5)
semwise_tab.grid_columnconfigure(0, weight=1)
semwise_tab.grid_columnconfigure(1, weight=1)

# Dropdown for selecting semester
semester_label_semwise = ctk.CTkLabel(semwise_tab, text="Select Semester for Academic Performance:")
semester_label_semwise.grid(row=0, column=0, pady=10, columnspan=2)

semester_label_semwise = ctk.CTkOptionMenu(
    semwise_tab, 
    values=["SEM1", "SEM2", "SEM3", "SEM4", "SEM5", "SEM6", "SEM7", "SEM8"]
)
semester_label_semwise.grid(row=1, column=0, pady=10, columnspan=2)

# Submit button to display semester-wise results
semwise_submit_button = ctk.CTkButton(
    semwise_tab, 
    text="Submit and Display Results",
    command=lambda: display_semesterwise_results(semester_label_semwise.get())
)
semwise_submit_button.grid(row=2, column=0, pady=10, columnspan=2)



# Treeview table for displaying semester-wise results
semesterwise_result_table = ctk.CTkFrame(semwise_tab, width=400, height=300)
semesterwise_result_table.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

# Graph display area
semwise_graph = ctk.CTkFrame(semwise_tab, width=400, height=300)
semwise_graph.grid(row=3, column=1, pady=10, padx=10, sticky="nsew")



# Subject-wise Result Tab
subjectwise_result_tab = tabview.add("Subject-wise Result")
subjectwise_result_tab.grid_rowconfigure(0, weight=1)
subjectwise_result_tab.grid_rowconfigure(1, weight=1)
subjectwise_result_tab.grid_rowconfigure(2, weight=1)
subjectwise_result_tab.grid_rowconfigure(3, weight=2)  # Allocate more space for results and graphs
subjectwise_result_tab.grid_columnconfigure(0, weight=1)
subjectwise_result_tab.grid_columnconfigure(1, weight=1)

# Dropdown to select semester
#subjectwise_semester_label = ctk.CTkLabel(subjectwise_result_tab, text="Select Semester:")
#subjectwise_semester_label.grid(row=0, column=0, pady=10, padx=10)

subjectwise_semester_dropdown = ctk.CTkOptionMenu(
    subjectwise_result_tab,
    values=list(semester_subject_mapping.keys()),
    command=update_subject_dropdown  # Link update function here
)
subjectwise_semester_dropdown.grid(row=0, column=0, columnspan=2, pady=10,sticky="N")
subjectwise_semester_dropdown.set("Select semester")  # Set to empty initially

# Dropdown to select subject code
#subjectwise_subject_label = ctk.CTkLabel(subjectwise_result_tab, text="Select Subject Code:")
#subjectwise_subject_label.grid(row=1, column=0, pady=10, padx=10)

subjectwise_subject_dropdown = ctk.CTkOptionMenu(subjectwise_result_tab, values=[])
subjectwise_subject_dropdown.grid(row=1, column=0, columnspan=2, pady=10,sticky="N")
subjectwise_subject_dropdown.set("Select subject code")


# Submit button for subject-wise result
subjectwise_submit_button = ctk.CTkButton(subjectwise_result_tab, text="Submit and save PDF", command=display_subjectwise_result)
subjectwise_submit_button.grid(row=2, column=0, columnspan=2, pady=10,sticky="N")

# Textbox to display results
subjectwise_result_text = ctk.CTkTextbox(subjectwise_result_tab, width=400, height=300)
subjectwise_result_text.grid(row=3, column=0, pady=10, padx=10,sticky="nsew")
subjectwise_result_text.configure(state="disabled")

# Frame to display subject-wise graphs (Performance and Attendance Pie Charts)
subjectwise_result_graph = ctk.CTkFrame(subjectwise_result_tab, width=400, height=300)
subjectwise_result_graph.grid(row=3, column=1, pady=10, padx=10,sticky="nsew")

# Configure the graph frame for displaying two charts side by side
subjectwise_result_graph.grid_rowconfigure(0, weight=0)
subjectwise_result_graph.grid_columnconfigure(0, weight=1)
subjectwise_result_graph.grid_columnconfigure(1, weight=1)


# Student Info Tab
# Student Info Tab
student_info_tab = tabview.add("Student Info")
student_info_tab.grid_rowconfigure(0, weight=1)
student_info_tab.grid_columnconfigure(0, weight=1)
student_info_tab.grid_columnconfigure(1, weight=1)

info_text = ctk.CTkTextbox(student_info_tab, width=400, height=300)
info_text.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
info_text.configure(state="disabled")

student_info_graph = ctk.CTkFrame(student_info_tab, width=400, height=300)
student_info_graph.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

# Run the GUI
root.mainloop()
