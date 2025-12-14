import numpy as np
import math
from collections import Counter, defaultdict

class TfidfVectorizer:
    """
    Implementasi manual TF-IDF Vectorizer
    Tidak menggunakan sklearn
    """
    
    def __init__(self, min_df=2, max_df=0.85, ngram_range=(1, 2), max_features=500):
        """
        Parameters:
        - min_df: minimum document frequency (kata harus muncul di minimal n dokumen)
        - max_df: maximum document frequency (kata maksimal di proporsi dokumen)
        - ngram_range: tuple (min_n, max_n) untuk n-gram
        - max_features: jumlah fitur maksimal
        """
        self.min_df = min_df
        self.max_df = max_df
        self.ngram_range = ngram_range
        self.max_features = max_features
        
        self.vocabulary_ = {}  # {term: index}
        self.idf_ = {}  # {term: idf_value}
        self.feature_names_ = []
        
    def _generate_ngrams(self, tokens, n):
        """Generate n-grams dari list tokens"""
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i+n])
            ngrams.append(ngram)
        return ngrams
    
    def _extract_terms(self, text):
        """Ekstrak terms (unigram dan bigram) dari teks"""
        tokens = text.split()
        terms = []
        
        # Generate n-grams sesuai range
        for n in range(self.ngram_range[0], self.ngram_range[1] + 1):
            if n == 1:
                terms.extend(tokens)
            else:
                terms.extend(self._generate_ngrams(tokens, n))
        
        return terms
    
    def _compute_term_frequency(self, terms):
        """Hitung Term Frequency (TF)"""
        term_count = Counter(terms)
        total_terms = len(terms)
        
        tf = {}
        for term, count in term_count.items():
            tf[term] = count / total_terms if total_terms > 0 else 0
        
        return tf
    
    def _compute_document_frequency(self, documents):
        """Hitung Document Frequency (DF) untuk setiap term"""
        df = defaultdict(int)
        
        for doc in documents:
            terms = set(self._extract_terms(doc))
            for term in terms:
                df[term] += 1
        
        return df
    
    def _compute_idf(self, df, n_documents):
        """Hitung Inverse Document Frequency (IDF)"""
        idf = {}
        
        for term, doc_freq in df.items():
            # IDF = log((N + 1) / (df + 1)) + 1
            # +1 untuk smoothing (avoid division by zero)
            idf[term] = math.log((n_documents + 1) / (doc_freq + 1)) + 1
        
        return idf
    
    def _filter_terms(self, df, n_documents):
        """Filter terms berdasarkan min_df dan max_df"""
        filtered_terms = []
        
        max_doc_count = int(self.max_df * n_documents)
        
        for term, doc_freq in df.items():
            # Filter berdasarkan min_df dan max_df
            if doc_freq >= self.min_df and doc_freq <= max_doc_count:
                filtered_terms.append(term)
        
        return filtered_terms
    
    def _select_top_features(self, terms, df):
        """Pilih top features berdasarkan document frequency"""
        if len(terms) <= self.max_features:
            return terms
        
        # Sort berdasarkan DF (descending)
        sorted_terms = sorted(terms, key=lambda t: df[t], reverse=True)
        return sorted_terms[:self.max_features]
    
    def fit(self, documents):
        """
        Fit vectorizer pada dokumen
        
        Parameters:
        - documents: list of strings
        """
        n_documents = len(documents)
        
        # Hitung document frequency
        df = self._compute_document_frequency(documents)
        
        # Filter terms
        filtered_terms = self._filter_terms(df, n_documents)
        
        # Select top features
        selected_terms = self._select_top_features(filtered_terms, df)
        
        # Build vocabulary
        self.vocabulary_ = {term: idx for idx, term in enumerate(sorted(selected_terms))}
        self.feature_names_ = sorted(selected_terms)
        
        # Compute IDF
        self.idf_ = self._compute_idf(df, n_documents)
        
        return self
    
    def transform(self, documents):
        """
        Transform dokumen menjadi TF-IDF matrix
        
        Returns:
        - numpy array of shape (n_documents, n_features)
        """
        n_documents = len(documents)
        n_features = len(self.vocabulary_)
        
        # Initialize matrix
        tfidf_matrix = np.zeros((n_documents, n_features))
        
        for doc_idx, doc in enumerate(documents):
            # Extract terms
            terms = self._extract_terms(doc)
            
            # Compute TF
            tf = self._compute_term_frequency(terms)
            
            # Compute TF-IDF
            for term, tf_value in tf.items():
                if term in self.vocabulary_:
                    term_idx = self.vocabulary_[term]
                    idf_value = self.idf_.get(term, 0)
                    tfidf_matrix[doc_idx, term_idx] = tf_value * idf_value
        
        # L2 normalization (normalize each row)
        for i in range(n_documents):
            norm = np.linalg.norm(tfidf_matrix[i])
            if norm > 0:
                tfidf_matrix[i] = tfidf_matrix[i] / norm
        
        return tfidf_matrix
    
    def fit_transform(self, documents):
        """Fit dan transform sekaligus"""
        self.fit(documents)
        return self.transform(documents)
    
    def get_feature_names_out(self):
        """Get feature names (untuk compatibility)"""
        return np.array(self.feature_names_)


def vectorize_text(texts):
    """
    Fungsi wrapper untuk compatibility dengan kode lama
    
    Parameters:
    - texts: list/series teks yang sudah dibersihkan
    
    Returns:
    - vectorizer: object TfidfVectorizer yang sudah di-fit
    - X: numpy array hasil TF-IDF
    """
    # Convert to list if pandas Series
    if hasattr(texts, 'tolist'):
        texts = texts.tolist()
    
    vectorizer = TfidfVectorizer(
        min_df=2,
        max_df=0.85,
        ngram_range=(1, 2),
        max_features=500
    )
    
    X = vectorizer.fit_transform(texts)
    
    return vectorizer, X