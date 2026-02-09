from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RuleRetriever:
    def __init__(self, rules_path):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.rules = self._load_rules(rules_path)
        self.embeddings = self.model.encode(self.rules)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def _load_rules(self, path):
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]

    def retrieve(self, query, k=3):
        q_emb = self.model.encode([query])
        _, indices = self.index.search(q_emb, k)
        return [self.rules[i] for i in indices[0]]
