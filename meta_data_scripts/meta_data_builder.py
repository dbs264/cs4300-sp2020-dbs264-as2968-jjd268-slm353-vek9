from collections import defaultdict
from collections import Counter
import json
import math
import string
import time
import numpy as np
from nltk.tokenize import TreebankWordTokenizer

tokenizer = TreebankWordTokenizer()
data_path = "../data/"


def load_details(city):
    city = city.lower().replace(" ", "_")
    with open(data_path+city+"/"+city+"_details.json") as f:
        return json.load(f)


def flatten_reviews(details):
    for place in details:
        agg_reviews = ""
        if "reviews" in place:
            for review in place["reviews"]:
                agg_reviews += review["text"] + " "
        place["agg_reviews"] = agg_reviews
    return details


def build_inverted_index(details):
    result = {}

    for ind, place in enumerate(details):
        tokens = tokenizer.tokenize(place["agg_reviews"].lower())
        for token in tokens:
            if token in result:
                if ind in result[token]:
                    result[token][ind] += 1
                else:
                    result[token][ind] = 1
            else:
                result[token] = {ind: 1}

    for word, occurences in result.items():
        result[word] = sorted(list(occurences.items()))
    return result


def compute_idf(inv_idx, n_docs, min_df=0, max_df_ratio=1):
    idf = {}
    for word, docs in inv_idx.items():
        if len(docs) >= min_df and len(docs)/n_docs <= max_df_ratio:
            idf[word] = math.log2(n_docs/(1+len(docs)))
    return idf


def compute_doc_norms(index, idf, n_docs):
    normsSquared = np.zeros(n_docs)
    for word, docs in index.items():
        if word in idf:
            for doc in docs:
                normsSquared[doc[0]] += (float(doc[1]) * idf[word])**2

    return normsSquared ** .5


def build_meta_data_file(city):
    details = flatten_reviews(load_details(city))
    inv_ind = build_inverted_index(details)
    idf = compute_idf(inv_ind, len(details))
    doc_norms = compute_doc_norms(inv_ind, idf, len(details))

    meta_data = {}
    meta_data["inverted_index"] = inv_ind
    meta_data["idf"] = idf
    meta_data["doc_norms"] = doc_norms.tolist()

    with open(data_path+city+"/"+city+"_meta_data.json", 'w') as outfile:
        json.dump(meta_data, outfile)


def main():
    build_meta_data_file("new_york")


if __name__ == '__main__':
    main()
