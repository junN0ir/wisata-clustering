import numpy as np

class KMeans:
    """
    Implementasi manual K-Means Clustering
    Tidak menggunakan sklearn
    """
    
    def __init__(self, n_clusters=3, max_iter=300, random_state=42, tol=1e-4):
        """
        Parameters:
        - n_clusters: jumlah cluster
        - max_iter: maksimal iterasi
        - random_state: seed untuk reproducibility
        - tol: tolerance untuk konvergensi
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.tol = tol
        
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None
        self.n_iter_ = 0
        
    def _initialize_centers(self, X):
        """
        Initialize cluster centers menggunakan K-Means++
        Lebih baik daripada random initialization
        """
        np.random.seed(self.random_state)
        n_samples = X.shape[0]
        
        # Pilih centroid pertama secara random
        centers = [X[np.random.randint(n_samples)]]
        
        # Pilih centroid sisanya dengan K-Means++ algorithm
        for _ in range(1, self.n_clusters):
            # Hitung jarak ke centroid terdekat
            distances = np.array([min([self._euclidean_distance(x, c) for c in centers]) 
                                 for x in X])
            
            # Probabilitas pemilihan proporsional dengan jarak kuadrat
            probabilities = distances ** 2
            probabilities /= probabilities.sum()
            
            # Pilih centroid baru
            cumulative_probs = probabilities.cumsum()
            r = np.random.rand()
            
            for idx, prob in enumerate(cumulative_probs):
                if r < prob:
                    centers.append(X[idx])
                    break
        
        return np.array(centers)
    
    def _euclidean_distance(self, x1, x2):
        """Hitung jarak Euclidean antara dua vektor"""
        return np.sqrt(np.sum((x1 - x2) ** 2))
    
    def _assign_clusters(self, X, centers):
        """
        Assign setiap data point ke cluster terdekat
        
        Returns:
        - labels: array of cluster assignments
        """
        n_samples = X.shape[0]
        labels = np.zeros(n_samples, dtype=int)
        
        for idx, x in enumerate(X):
            # Hitung jarak ke semua centroid
            distances = [self._euclidean_distance(x, center) for center in centers]
            # Assign ke cluster terdekat
            labels[idx] = np.argmin(distances)
        
        return labels
    
    def _update_centers(self, X, labels):
        """
        Update posisi centroid berdasarkan mean dari data points di cluster
        
        Returns:
        - new_centers: array of new cluster centers
        """
        n_features = X.shape[1]
        new_centers = np.zeros((self.n_clusters, n_features))
        
        for k in range(self.n_clusters):
            # Ambil semua points yang belong ke cluster k
            cluster_points = X[labels == k]
            
            if len(cluster_points) > 0:
                # Update centroid = mean dari points
                new_centers[k] = cluster_points.mean(axis=0)
            else:
                # Jika cluster kosong, reinitialize dengan random point
                new_centers[k] = X[np.random.randint(X.shape[0])]
        
        return new_centers
    
    def _compute_inertia(self, X, labels, centers):
        """
        Hitung inertia (sum of squared distances ke centroid terdekat)
        Metrik untuk mengukur kualitas clustering
        """
        inertia = 0
        for idx, x in enumerate(X):
            center = centers[labels[idx]]
            inertia += self._euclidean_distance(x, center) ** 2
        
        return inertia
    
    def _has_converged(self, old_centers, new_centers):
        """Check apakah algorithm sudah converge"""
        if old_centers is None:
            return False
        
        # Hitung perubahan centroid
        distances = [self._euclidean_distance(old_centers[i], new_centers[i]) 
                    for i in range(self.n_clusters)]
        
        # Converge jika perubahan < tolerance
        return max(distances) < self.tol
    
    def fit(self, X):
        """
        Fit K-Means model
        
        Parameters:
        - X: numpy array of shape (n_samples, n_features)
        """
        # Initialize centers
        self.cluster_centers_ = self._initialize_centers(X)
        
        old_centers = None
        
        # Iterasi K-Means
        for iteration in range(self.max_iter):
            # Step 1: Assign clusters
            self.labels_ = self._assign_clusters(X, self.cluster_centers_)
            
            # Step 2: Update centers
            new_centers = self._update_centers(X, self.labels_)
            
            # Check convergence
            if self._has_converged(old_centers, new_centers):
                self.n_iter_ = iteration + 1
                break
            
            old_centers = self.cluster_centers_.copy()
            self.cluster_centers_ = new_centers
        
        # Compute final inertia
        self.inertia_ = self._compute_inertia(X, self.labels_, self.cluster_centers_)
        
        return self
    
    def predict(self, X):
        """
        Predict cluster untuk data baru
        
        Parameters:
        - X: numpy array of shape (n_samples, n_features)
        
        Returns:
        - labels: cluster assignments
        """
        return self._assign_clusters(X, self.cluster_centers_)
    
    def fit_predict(self, X):
        """Fit dan predict sekaligus"""
        self.fit(X)
        return self.labels_


def run_kmeans(X, k=3):
    """
    Fungsi wrapper untuk compatibility dengan kode lama
    
    Parameters:
    - X: numpy array hasil TF-IDF
    - k: jumlah cluster
    
    Returns:
    - model: fitted KMeans object
    - labels: cluster assignments
    """
    model = KMeans(n_clusters=k, random_state=42)
    labels = model.fit_predict(X)
    
    return model, labels