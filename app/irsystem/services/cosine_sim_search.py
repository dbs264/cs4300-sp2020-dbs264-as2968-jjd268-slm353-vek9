import numpy as np
import config, random, json, re
from collections import Counter
from app.irsystem.services import search_helpers as helpers
from nltk.tokenize import TreebankWordTokenizer

tokenizer = TreebankWordTokenizer()

def index_search(query, index, idf, doc_norms):
	query_tokens = tokenizer.tokenize(query.lower())
	query_norm = 0
	result = np.zeros(len(doc_norms))
	inverted_query = {}
	for token in query_tokens:
		if token in inverted_query:
			inverted_query[token] += 1
		else:
			inverted_query[token] = 1

	for token, q_count in inverted_query.items():
		if token in idf:
			query_norm += (q_count*idf[token])**2
			for doc, count in index[token]:
				result[doc] += (q_count*count)*idf[token]**2
	

	query_norm = query_norm ** .5
	new_doc_norms = (query_norm*doc_norms)
	results = np.divide(result,new_doc_norms, out=np.zeros_like(result), where= new_doc_norms!= 0)

	return results

def search(query, city, price):
	details = helpers.load_details(city)
	meta_data = helpers.load_meta_data(city)
	inv_ind = meta_data["inverted_index"]
	idf = meta_data["idf"]
	doc_norms = np.array(meta_data["doc_norms"])

	scores = index_search(query,inv_ind,idf,doc_norms)
	for ind, score in enumerate(scores):
		details[ind]["score"] = score
	
	top_results = helpers.sort_by_score(helpers.filter_by_attributes(details,price))

	return [ helpers.format_output(x) for x in top_results]