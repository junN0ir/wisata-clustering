from sklearn.cluster import KMeans

def run_kmeans(X, k=3):
    model = KMeans(n_clusters=k, random_state=42)
    labels = model.fit_predict(X)
    return model, labels
