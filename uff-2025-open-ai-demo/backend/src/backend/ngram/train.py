from pathlib import Path

from backend.ngram.model import NGramLanguageModel


def train(documents_path: str) -> Path:

    documents_path = Path(documents_path)
    print(f"Training N-gram model with documents from {documents_path.resolve()}")

    documents = []
    for file_path in documents_path.rglob("*.txt"):
        print(f"Reading file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            documents.append(file.read())

    model = NGramLanguageModel()
    model.train(n=2, documents=documents)