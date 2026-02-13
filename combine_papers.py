import os

base_dir = r"D:\Study\Projects\contextAG\data\text_chunks"
output_dir = r"D:\Study\Projects\contextAG\data\combined_subjects"
os.makedirs(output_dir, exist_ok=True)

# Loop through all subjects like AI, ML, UHV, CC
for subject in os.listdir(base_dir):
    subject_path = os.path.join(base_dir, subject)
    if not os.path.isdir(subject_path):
        continue

    output_path = os.path.join(output_dir, f"{subject}_combined.txt")

    with open(output_path, "w", encoding="utf-8") as outfile:
        for exam_type in ["Endsem", "Midsem"]:
            exam_path = os.path.join(subject_path, exam_type)
            if not os.path.exists(exam_path):
                continue

            for filename in os.listdir(exam_path):
                if filename.endswith(".txt"):
                    year = filename.split(".")[0]
                    file_path = os.path.join(exam_path, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        marker = f"\n\n--- START OF {year.upper()} {exam_type.upper()} ---\n\n"
                        end_marker = f"\n\n--- END OF {year.upper()} {exam_type.upper()} ---\n\n"
                        outfile.write(marker + content + end_marker)

    print(f"✅ Merged files for subject: {subject} → {output_path}")
