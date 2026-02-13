from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import json

# === Paths & Config ===
json_dir = r"D:\Study\Projects\contextAG\json_subs"
db_dir = "./chroma_question_db"
embedding_model = "mxbai-embed-large"
collection_name = "question_parts"

# === Embeddings & Chroma Init ===
embeddings = OllamaEmbeddings(model=embedding_model)
vector_store = Chroma(
    collection_name=collection_name,
    persist_directory=db_dir,
    embedding_function=embeddings
)

# === Rebuild vector DB if not already initialized ===
if not os.path.exists(db_dir):
    documents = []
    ids = []
    doc_id = 0

    for filename in os.listdir(json_dir):
        if not filename.endswith(".json"):
            continue

        subject = filename.replace(".json", "")
        file_path = os.path.join(json_dir, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            exams = json.load(f)

        for exam in exams:
            meta_common = {
                "university": exam.get("university"),
                "year": exam.get("year"),
                "exam_type": exam.get("exam_type"),
                "semester": exam.get("semester"),
                "programme": exam.get("programme"),
                "branch": exam.get("branch"),
                "subject": subject,
                "subject_name": exam.get("subject_name"),
                "subject_code": exam.get("subject_code"),
                "duration": exam.get("duration"),
                "full_marks": exam.get("full_marks"),
                "question_paper_code": exam.get("question_paper_code"),
            }

            # Check if the exam has question blocks
            if "questions" in exam:
                for qblock in exam["questions"]:
                    for part in qblock.get("question_parts", []):
                        question_text = part.get("text", "").strip()
                        if not question_text or len(question_text) < 10:
                            continue

                        full_meta = {
                            **meta_common,
                            "question_number": qblock.get("question_number"),
                            "question_section": qblock.get("question_section"),
                            "part_id": part.get("part_id"),
                            "marks": part.get("marks"),
                        }

                        documents.append(Document(
                            page_content=question_text,
                            metadata=full_meta
                        ))
                        ids.append(f"{subject}_{doc_id}")
                        doc_id += 1

    vector_store.add_documents(documents, ids)
    vector_store.persist()
    print(f"✅ {len(documents)} question parts added to vector store.")

# === Export retriever ===
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
