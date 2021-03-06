from pyserini.search import SimpleSearcher


class BM25Retriever:
    def __init__(self, dataset):
        self._searcher = SimpleSearcher(dataset)

    def set_rm3(self, a, b, c):
        self._searcher.set_rm3(a, b, c)

    def set_bm25(self, a, b):
        self._searcher.set_bm25(a, b)

    def query(self, query_text, k=100):
        hits = self._searcher.search(query_text, k=k)
        return hits
