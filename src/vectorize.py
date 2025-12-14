from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_text(texts):
    """
    Mengubah teks menjadi vektor TF-IDF
    
    Parameters:
    - texts: list/series teks yang sudah dibersihkan
    
    Returns:
    - vectorizer: object TfidfVectorizer yang sudah di-fit
    - X: sparse matrix hasil TF-IDF
    """
    vectorizer = TfidfVectorizer(
        # Tidak perlu stopwords karena sudah dibersihkan di preprocess
        min_df=2,           # Kata harus muncul minimal di 2 dokumen
        max_df=0.85,        # Kata maksimal muncul di 85% dokumen
        ngram_range=(1, 2), # Unigram dan bigram
        max_features=500    # Batasi fitur untuk performa lebih baik
    )
    
    X = vectorizer.fit_transform(texts)
    
    return vectorizer, X