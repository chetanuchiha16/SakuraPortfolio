from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

db_path = str(base_dir / "Outputs" / "student_data.db")
pdf_dir = str(base_dir / "Outputs" / "PDFs")
img_dir = str(base_dir / "Outputs" / "Images")
logo_path = str(base_dir / "Inputs" / "Images" / "logo.png")

# print(logo_path)
# print(base_dir)
# print(f"[DEBUG] Using DB path: {db_path}")
# print(f"[DEBUG] Exists? {Path(db_path).exists()}")
