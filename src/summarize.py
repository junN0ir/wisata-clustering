import numpy as np

def top_words_per_cluster(vectorizer, model, top_n=10):
    terms = vectorizer.get_feature_names_out()
    centers = model.cluster_centers_

    result = {}
    for i in range(len(centers)):
        top_idx = centers[i].argsort()[::-1][:top_n]
        result[i] = [terms[j] for j in top_idx]
    return result
