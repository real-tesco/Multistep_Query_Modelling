import hnswlib
import torch
import torch.nn as nn
import logging
import torch.optim as optim
import copy
from transformers import AutoTokenizer

logger = logging.getLogger()


class KnnIndex:
    def __init__(self, args, model):
        self._args = args
        self._seq_max_len = args.max_doc_len
        self._query_max_len = args.query_max_len
        self._index = hnswlib.Index(space=args.similarity, dim=args.dim_hidden)
        self._tokenizer = AutoTokenizer.from_pretrained(args.vocab)
        self._model = model

    def knn_query(self, query, k=1):
        q_input_ids, q_segment_ids, q_input_mask = self.tokenize(query)
        query_embedding = self._model.calculate_embedding(q_input_ids, q_segment_ids, q_input_mask, doc=False)
        labels, distances = self._index.knn_query(query=query_embedding, k=k)
        return labels, distances

    def tokenize(self, query):
        tokens = self._tokenizer.tokenize(query)
        input_tokens = [self._tokenizer.cls_token] + tokens + [self._tokenizer.sep_token]
        input_ids = self._tokenizer.convert_tokens_to_ids(input_tokens)
        segment_ids = [1] * len(input_ids)
        input_mask = [1] * len(input_ids)

        padding_len = self._seq_max_len - len(input_ids)

        input_ids = input_ids + [self._tokenizer.pad_token_id] * padding_len
        input_mask = input_mask + [0] * padding_len
        segment_ids = segment_ids + [0] * padding_len

        assert len(input_ids) == self._seq_max_len
        assert len(input_mask) == self._seq_max_len
        assert len(segment_ids) == self._seq_max_len
        return input_ids, segment_ids, input_mask

    def load_index(self):
        logger.info('Loading KNN index...')
        self._index.load_index(self._args.index_file)

    def get_document(self, pid):
        # check if works, else pid needs to be N dim np array
        return self._index.get_items(pid)


