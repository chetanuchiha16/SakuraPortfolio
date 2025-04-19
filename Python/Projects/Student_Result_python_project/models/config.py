db_path = "Outputs/student_data.db"
file_path=r"Inputs\ExcelSheet\result list project.xlsx"

from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
db_path = base_dir / "Outputs" / "student_data.db"

print(f"[DEBUG] Using DB path: {db_path}")
print(f"[DEBUG] Exists? {db_path.exists()}")
