import numpy as np

def top_words_per_cluster(vectorizer, model, top_n=10):
    """
    Ekstrak kata-kata dominan per cluster
    Compatible dengan implementasi custom TF-IDF dan K-Means
    
    Parameters:
    - vectorizer: TfidfVectorizer object (custom atau sklearn)
    - model: KMeans object (custom atau sklearn)
    - top_n: jumlah kata teratas yang diambil
    
    Returns:
    - result: dictionary {cluster_id: [list_of_top_words]}
    """
    # Get feature names (vocabulary)
    terms = vectorizer.get_feature_names_out()
    
    # Get cluster centers
    centers = model.cluster_centers_
    
    result = {}
    for i in range(len(centers)):
        # Ambil index kata dengan nilai TF-IDF tertinggi di centroid
        # argsort() mengurutkan ascending, [::-1] untuk reverse (descending)
        top_idx = centers[i].argsort()[::-1][:top_n]
        
        # Ambil kata-kata sesuai index
        result[i] = [terms[j] for j in top_idx]
    
    return result