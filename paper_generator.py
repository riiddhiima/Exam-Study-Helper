import os
import json
import random

json_dir = r"D:\Study\Projects\contextAG\json_subs"

def generate_sample_paper(subject, year_filter=None, exam_type_filter=None):
    file_path = os.path.join(json_dir, f"{subject}.json")
    if not os.path.exists(file_path):
        return f"❌ No exam data found for subject: {subject}"

    with open(file_path, "r", encoding="utf-8") as f:
        exams = json.load(f)

    questions_pool = []

    for exam in exams:
        if year_filter and exam.get("year") != year_filter:
            continue
        if exam_type_filter and exam.get("exam_type") != exam_type_filter:
            continue

        # Simulate Q parsing by pulling "other_instructions" and metadata
        instructions = exam.get("instructions", {})
        section = instructions.get("compulsory_section", "Section A")
        base_question = {
            "meta": f"{exam.get('year')} - {exam.get('exam_type')}",
            "text": f"{exam.get('subject_name')} ({exam.get('subject_code')}) - {section}",
            "questions": []
        }

        for info in instructions.get("other_instructions", []):
            if len(info) > 30:
                base_question["questions"].append(info)

        if base_question["questions"]:
            questions_pool.append(base_question)

    if not questions_pool:
        return "⚠️ No questions available for this filter."

    # Pick 1-2 from each of the top 5
    random.shuffle(questions_pool)
    sample_questions = []
    for qset in questions_pool[:5]:
        picked = random.sample(qset["questions"], min(2, len(qset["questions"])))
        sample_questions.extend(picked)

    # Format sample paper
    paper = f"Sample Paper for {subject}\n\n"
    paper += "Section A (Compulsory)\n"
    for i, q in enumerate(sample_questions[:4], start=1):
        paper += f"{i}. {q}\n"

    paper += "\nSection B (Answer any 3)\n"
    for i, q in enumerate(sample_questions[4:8], start=5):
        paper += f"{i}. {q}\n"

    return paper
