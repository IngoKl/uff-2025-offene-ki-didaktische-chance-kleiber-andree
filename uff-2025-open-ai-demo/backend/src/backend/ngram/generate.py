from pathlib import Path

from backend.ngram.model import NGramLanguageModel


def generate(text: str, length: int = 50) -> str:

    model = NGramLanguageModel()
    model.load()
    reply = model.generate(text=text, length=length)

    return reply
