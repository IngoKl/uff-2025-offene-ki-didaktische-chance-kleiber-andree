import json
import random
from collections import Counter, defaultdict
from pathlib import Path


class NGramLanguageModel:
    def __init__(self):
        self.n = 2
        self.ngrams = defaultdict(dict)

    def save(self):
        path = Path(Path(__file__).parent / "ngram_model.json")

        with open(path, "w") as f:
            serializable_data = {','.join(k): v for k, v in self.ngrams.items()}
            f.write(json.dumps(serializable_data, indent=4))

    def load(self):
        path = Path(Path(__file__).parent / "ngram_model.json")

        with open(path, "r") as f:
            data = f.read()
            if not data:
                return
            loaded = json.loads(data)
            self.ngrams = defaultdict(dict, {tuple(k.split(",")): v for k, v in loaded.items()})

    def train(self, n: int = 2, documents: list = None):
        self.n = n
        counts = defaultdict(Counter)
        
        for doc in documents:
            tokens = self.tokenize(doc)
            for i in range(len(tokens) - self.n + 1):
                prefix = tuple(tokens[i:i+self.n-1])
                next_word = tokens[i+self.n-1].replace(":", "")
                counts[prefix][next_word] += 1

        # Normalize counts to probabilities
        for prefix, counter in counts.items():
            total = sum(counter.values())
            self.ngrams[prefix] = {word: count/total for word, count in counter.items()}

        self.save()

    def generate(self, text: str, length: int = 50) -> str:
        if not self.ngrams:
            return ""

        tokens = self.tokenize(text)
        result = tokens.copy()

        if len(tokens) < self.n - 1:
            prefix = random.choice(list(self.ngrams.keys()))
            result = list(prefix)
        else:
            prefix = tuple(tokens[-(self.n-1):])

        for _ in range(length):
            next_words_probs = self.ngrams.get(prefix)
            if not next_words_probs:
                break

            next_word = self.weighted_choice(next_words_probs)
            result.append(next_word)
            prefix = tuple(result[-self.n+1:])

        return ' '.join(result)

    def weighted_choice(self, choices: dict) -> str:
        words = list(choices.keys())
        probabilities = list(choices.values())
        
        return random.choices(words, probabilities)[0]

    def tokenize(self, text: str) -> list:
        return text.lower().split()