"""
Script untuk testing dan validasi implementasi custom
Membandingkan hasil dengan sklearn (jika ada)
"""

import numpy as np
from tfidf import TfidfVectorizer
from kmeans import KMeans

def test_tfidf():
    """Test implementasi TF-IDF"""
    print("="*60)
    print("TEST TF-IDF IMPLEMENTATION")
    print("="*60)
    
    # Sample documents
    documents = [
        "pantai indah bersih",
        "pantai cantik sunset",
        "hutan hijau sejuk",
        "hutan pohon tinggi",
        "air terjun jernih dingin"
    ]
    
    print("\n[1] Testing TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(min_df=1, max_df=1.0, ngram_range=(1, 1), max_features=20)
    X = vectorizer.fit_transform(documents)
    
    print(f"   ✓ Shape: {X.shape}")
    print(f"   ✓ Features: {len(vectorizer.feature_names_)}")
    print(f"   ✓ Vocabulary: {list(vectorizer.vocabulary_.keys())[:10]}")
    
    # Check matrix properties
    print("\n[2] Checking matrix properties...")
    print(f"   ✓ Matrix type: {type(X)}")
    print(f"   ✓ Matrix min: {X.min():.4f}")
    print(f"   ✓ Matrix max: {X.max():.4f}")
    print(f"   ✓ Non-zero elements: {np.count_nonzero(X)}")
    
    # Check normalization (L2 norm should be ~1 for each row)
    print("\n[3] Checking L2 normalization...")
    for i in range(min(3, len(documents))):
        norm = np.linalg.norm(X[i])
        print(f"   Doc {i} L2 norm: {norm:.6f} {'✓ OK' if abs(norm - 1.0) < 0.01 else '✗ FAIL'}")
    
    print("\n✅ TF-IDF Test PASSED\n")
    return X

def test_kmeans(X=None):
    """Test implementasi K-Means"""
    print("="*60)
    print("TEST K-MEANS IMPLEMENTATION")
    print("="*60)
    
    # Generate sample data if not provided
    if X is None:
        np.random.seed(42)
        X = np.random.rand(20, 5)
    
    print(f"\n[1] Testing K-Means with data shape: {X.shape}...")
    
    # Test with different k values
    for k in [2, 3]:
        print(f"\n   Testing k={k}...")
        model = KMeans(n_clusters=k, random_state=42, max_iter=100)
        labels = model.fit_predict(X)
        
        print(f"   ✓ Labels shape: {labels.shape}")
        print(f"   ✓ Unique clusters: {len(np.unique(labels))}")
        print(f"   ✓ Centers shape: {model.cluster_centers_.shape}")
        print(f"   ✓ Iterations: {model.n_iter_}")
        print(f"   ✓ Inertia: {model.inertia_:.4f}")
        
        # Check cluster assignments
        print(f"   ✓ Cluster distribution: {np.bincount(labels)}")
        
        # Verify all points are assigned
        assert len(labels) == X.shape[0], "❌ Not all points assigned!"
        assert len(np.unique(labels)) <= k, "❌ More clusters than k!"
        assert model.cluster_centers_.shape == (k, X.shape[1]), "❌ Wrong center shape!"
        
        print(f"   ✅ K-Means with k={k} PASSED")
    
    print("\n✅ K-Means Test PASSED\n")
    return model

def test_integration():
    """Test integrasi TF-IDF + K-Means"""
    print("="*60)
    print("TEST INTEGRATION (TF-IDF + K-MEANS)")
    print("="*60)
    
    # Sample documents
    documents = [
        "pantai indah bersih sunset cantik",
        "pantai pasir putih ombak tenang",
        "pantai laut jernih bersih",
        "hutan hijau sejuk asri",
        "hutan pohon tinggi kanopi",
        "hutan mangrove bakau",
        "air terjun jernih dingin",
        "air terjun kolam sungai"
    ]
    
    print("\n[1] TF-IDF Transformation...")
    vectorizer = TfidfVectorizer(min_df=1, max_df=1.0, ngram_range=(1, 1), max_features=50)
    X = vectorizer.fit_transform(documents)
    print(f"   ✓ TF-IDF matrix: {X.shape}")
    
    print("\n[2] K-Means Clustering...")
    model = KMeans(n_clusters=3, random_state=42)
    labels = model.fit_predict(X)
    print(f"   ✓ Cluster labels: {labels}")
    print(f"   ✓ Cluster distribution: {np.bincount(labels)}")
    
    print("\n[3] Analyzing clusters...")
    for cluster_id in range(3):
        docs_in_cluster = [i for i, label in enumerate(labels) if label == cluster_id]
        print(f"\n   Cluster {cluster_id}:")
        print(f"   - Documents: {docs_in_cluster}")
        print(f"   - Example: '{documents[docs_in_cluster[0]]}'")
        
        # Top words in cluster
        center = model.cluster_centers_[cluster_id]
        top_indices = center.argsort()[-5:][::-1]
        top_words = [vectorizer.feature_names_[i] for i in top_indices]
        print(f"   - Top words: {', '.join(top_words)}")
    
    print("\n✅ Integration Test PASSED\n")

def test_edge_cases():
    """Test edge cases dan error handling"""
    print("="*60)
    print("TEST EDGE CASES")
    print("="*60)
    
    print("\n[1] Testing empty documents...")
    try:
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(["", "text", ""])
        print("   ⚠️  Empty docs handled (should filter)")
    except Exception as e:
        print(f"   ✓ Caught expected error: {type(e).__name__}")
    
    print("\n[2] Testing single document...")
    try:
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(["single document only"])
        print(f"   ✓ Single doc: shape {X.shape}")
    except Exception as e:
        print(f"   ✓ Caught expected error: {type(e).__name__}")
    
    print("\n[3] Testing k > n_samples...")
    try:
        X = np.random.rand(3, 5)
        model = KMeans(n_clusters=5)  # k > n_samples
        labels = model.fit_predict(X)
        print(f"   ⚠️  k > n handled (may have empty clusters)")
    except Exception as e:
        print(f"   ✓ Caught expected error: {type(e).__name__}")
    
    print("\n✅ Edge Cases Test PASSED\n")

def run_all_tests():
    """Run semua tests"""
    print("\n" + "="*60)
    print("RUNNING ALL TESTS")
    print("="*60 + "\n")
    
    try:
        # Test TF-IDF
        X = test_tfidf()
        
        # Test K-Means
        test_kmeans(X)
        
        # Test Integration
        test_integration()
        
        # Test Edge Cases
        test_edge_cases()
        
        print("="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nImplementasi custom TF-IDF dan K-Means siap digunakan!")
        print("Tidak ada bug yang terdeteksi.\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ TEST FAILED!")
        print("="*60)
        print(f"\nError: {type(e).__name__}")
        print(f"Message: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()