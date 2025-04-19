import sqlite3
import pandas as pd
from models.config import db_path, file_path

def convert_excel_to_sql(file_path, db_path):
    # Load the Excel file
    xls = pd.ExcelFile(file_path)
    conn = sqlite3.connect(db_path)

    for sheet_name in xls.sheet_names:
        print(f"Processing sheet: {sheet_name}")
        df = xls.parse(sheet_name, header=[0, 1])

        # Flatten multi-level headers
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
        else:
            df.columns = [str(col).strip() for col in df.columns]

        # Remove unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Try converting numeric-like columns to numbers
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')

        # Write to SQL directly
        df.to_sql(sheet_name, conn, if_exists='replace', index=False)
        print(f"Saved sheet '{sheet_name}' to database.")

    conn.close()
    print("All sheets processed and saved.")

# Usage
convert_excel_to_sql(
    file_path = file_path,
    db_path = db_path
)
