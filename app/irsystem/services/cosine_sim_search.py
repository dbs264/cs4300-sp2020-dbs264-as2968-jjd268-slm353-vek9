import numpy as np
import config
import random
import json
import re
from collections import Counter
from app.irsystem.services import search_helpers as helpers
from nltk.tokenize import TreebankWordTokenizer
from app.irsystem.services import distance_from
from nltk.stem import PorterStemmer

ps = PorterStemmer()
tokenizer = TreebankWordTokenizer()


def index_search(query, index, idf, doc_norms):
    query_tokens = tokenizer.tokenize(query.lower())
    query_norm = 0
    result = np.zeros(len(doc_norms))
    inverted_query = {}
    for token in query_tokens:
        stem = ps.stem(token)
        if stem in inverted_query:
            inverted_query[stem] += 1
        else:
            inverted_query[stem] = 1

    for stem, q_count in inverted_query.items():
        if stem in idf:
            query_norm += (q_count*idf[stem])**2
            for doc, count in index[stem]:
                result[doc] += (q_count*count)*idf[stem]**2

    query_norm = query_norm ** .5
    new_doc_norms = (query_norm*doc_norms)
    results = np.divide(result, new_doc_norms, out=np.zeros_like(
        result), where=new_doc_norms != 0)

    return results


def search(query, city, price, location_string):
    details = helpers.load_details(city)
    meta_data = helpers.load_meta_data(city)
    inv_ind = meta_data["inverted_index"]
    idf = meta_data["idf"]
    doc_norms = np.array(meta_data["doc_norms"])

    scores = index_search(query, inv_ind, idf, doc_norms)
    for ind, score in enumerate(scores):
        details[ind]["score"] = score
    if location_string:
        details = distance_from.add_distances(details, location_string, city)
        distance_from.update_scores_for_distance(details)
    top_results = helpers.sort_by_score(
        helpers.filter_by_attributes(details, price))

    return [helpers.format_output(x) for x in top_results]
