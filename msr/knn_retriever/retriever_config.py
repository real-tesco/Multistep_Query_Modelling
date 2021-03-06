import argparse
import logging


logger = logging.getLogger()


def str2bool(v):
    return v.lower() in ('yes', 'true', 't', '1', 'y')


def get_args(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser()
        parser.register('type', 'bool', str2bool)

    parser.add_argument('-pretrain', type=str, default='bert-base-uncased')
    parser.add_argument('-max_query_len', type=int, default=64)
    parser.add_argument('-max_doc_len', type=int, default=512)
    parser.add_argument('-M', type=int, default=84)
    parser.add_argument('-efc', type=int, default=500)
    parser.add_argument('-similarity', type=str, default='ip')
    parser.add_argument('-dim_hidden', type=int, default=768)
    parser.add_argument('-index_mapping', type=str, default='./data/indexes/mapping_docid2indexid.json')
    parser.add_argument('-index_file', type=str, default='./data/indexes/msmarco_knn_index_M_84_efc_500.bin')
    parser.add_argument('-remainP', type='bool', default=False)
    parser.add_argument('-projection_dim', type=int, default=0,
                        help='if > 0 then a projection is learned with given dim')

    args = parser.parse_args()

    return args
