from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import KMeans, MiniBatchKMeans, AgglomerativeClustering, MeanShift, Birch
from matplotlib import pyplot
import meta_data_builder
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from collections import Counter

data_path = "../data/"


def build_model(details):
    documents = [x["agg_reviews"] for x in details]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)

    true_k = len(documents) // 200
    model = MiniBatchKMeans(n_clusters=true_k)
    model.fit(X)
    return model, vectorizer, true_k, X


def main():
    city = "miami"
    details = meta_data_builder.flatten_reviews(
        meta_data_builder.load_details(city))
    model, vectorizer, true_k, X = build_model(details)

    yhat = model.predict(X)

    for ind, place in enumerate(details):
        place["cluster"] = int(yhat[ind])

    with open(data_path+city+"/"+city+"_details_with_clusters.json", 'w') as outfile:
        json.dump(details, outfile)

    results = Counter(yhat)
    print(results)

    # print("Top terms per cluster:")
    # order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    # terms = vectorizer.get_feature_names()
    # for i in range(true_k):
    #     print("Cluster {}:".format(i))
    #     for ind in order_centroids[i, :10]:
    #         print(' {}'.format(terms[ind]))


if __name__ == '__main__':
    main()
