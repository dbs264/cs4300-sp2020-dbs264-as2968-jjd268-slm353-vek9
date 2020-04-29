import numpy as np
import config
import random
import json
import re
from collections import Counter
from app.irsystem.services import search_helpers as helpers
from app.irsystem.services import cosine_sim_search as cosine_sim
from app.irsystem.services import distance_from


def search(bar_name, city, price, location_string):

    details = helpers.load_details_with_clusters(city)
    bar_names = [x["name"]for x in details]
    bar_names_set = set(bar_names)
    meta_data = helpers.load_meta_data(city)
    inv_ind = meta_data["inverted_index"]
    idf = meta_data["idf"]
    doc_norms = np.array(meta_data["doc_norms"])

    bar_query = ""
    bar_cluster = 0
    if bar_name in bar_names_set:
        bar_ind = bar_names.index(bar_name)
        bar_query = details[bar_ind]["agg_reviews"]
        bar_cluster = details[bar_ind]["cluster"]

    scores = cosine_sim.index_search(bar_query, inv_ind, idf, doc_norms)

    for ind, score in enumerate(scores):
        details[ind]["score"] = score
    if location_string:
        details = distance_from.add_distances(details, location_string, city)
        distance_from.update_scores_for_distance(details)

    filtered_results = helpers.filter_by_attributes(
        details, price, bar_cluster)
    filtered_results = list(filter(lambda x:
                                   x["name"] != bar_name, filtered_results))
    top_results = helpers.sort_by_score(filtered_results)

    return [helpers.format_output(x) for x in top_results]
